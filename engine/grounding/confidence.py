"""G4 — confidence the harness computed, and the abstention when it could not.

Pure and deterministic: no LLM, no I/O, no wall clock. `current_date` is a parameter
everywhere it is needed, exactly as `engine/temporal.py` does it (I8).

**What this replaces.** Confidence today is a product of author-set multipliers —
`causal 1.00 x axis_fit 0.70 x edge 1.00 x purity 0.80 x data 0.50` — a number the code
asserts rather than earns. Here every term is something the harness observed: a span was
located and by which method, the claimed numbers were found in it, how reliable the
source is, how many DISTINCT sources say it, how old it is. The model's own confidence
enters at one point only, as a ceiling.

**Why a weighted average and not a product.** The existing product form means one term
at 0.5 halves everything, so the composite is dominated by whichever factor happens to
be least knowable. Terms here are evidence ABOUT the same claim, not independent
probabilities to be multiplied, and averaging them lets a strongly-grounded claim from
one source outscore a weakly-grounded claim from three without either term vanishing.
The fail-closed cases are handled as verdicts (ungrounded -> 0.0) rather than as small
multipliers, which is what keeps "blocked beats plausible" a rule and not a gradient.

**When it abstains.** Two situations, and they are different answers:

* `ungrounded` — the span was not located. Confidence is exactly 0.0 and the atom is
  excluded from theme support. This is a finding about the evidence.
* `abstained` — the span WAS located, but too few of the weighted terms were
  observable to average honestly (below `MIN_ASSESSED_WEIGHT`). The harness reports no
  number at all. This is a finding about the harness's own knowledge, and it is why
  `AtomConfidence.value` is `Optional`: an abstention that had to render as `0.3` would
  be indistinguishable from a computed 0.3 the moment it was written down.

`preference_key` makes the ordering the plan requires explicit: a confident-but-
ungrounded claim ranks BELOW an abstention.
"""
from __future__ import annotations

from datetime import date
from types import MappingProxyType
from typing import Mapping, Optional

from engine.schema.confidence import (
    AtomConfidence,
    AtomConfidenceComponents,
    ConfidenceSignals,
    Insufficient,
)
from engine.schema.grounding import GroundingMethod, GroundingVerdict

#: D4 — the weights are constants in code with a version string. NOT tunable per run,
#: NOT read from config, NOT settable by the model. Changing any number in this module
#: is a specification change: bump `CONFIDENCE_VERSION` in the same commit, because the
#: version is stamped on every stored score and is the only thing that keeps an old
#: score interpretable after the constants move.
CONFIDENCE_VERSION = "g4.v1"

#: Relative weight of each observable term. Sums to 1.0 (asserted at import).
#:
#: Grounding carries the most because it is the only term that is a fact about the
#: SOURCE rather than a prior about it: a located span either exists or it does not.
#: Reliability is next because claim-kind is the strongest predictor the repo already
#: measures (`RELIABILITY_DEFAULTS`). Entailment is smallest because G3 has not shipped,
#: so it is almost always absent — and a term that is usually absent should not swing a
#: score when it happens to be present.
_WEIGHTS: Mapping[str, float] = MappingProxyType({
    "grounding": 0.35,
    "numbers": 0.15,
    "reliability": 0.20,
    "independence": 0.12,
    "freshness": 0.10,
    "entailment": 0.08,
})

#: How much a located span is worth by the method that located it. An exact character
#: match is the full score; a whitespace/quote-normalized match is nearly so. A
#: human-confirmed loose match (D1 Tier C) is deliberately lower than either: a person
#: agreed the quote supports the claim, which is weaker than the text being identical,
#: and the score should say so rather than laundering a judgement into a match.
_METHOD_SCORE: Mapping[GroundingMethod, float] = MappingProxyType({
    "exact": 1.00,
    "normalized": 0.90,
    "loose_human_confirmed": 0.70,
    "none": 0.00,
})

#: Below this share of total weight, the harness abstains instead of averaging.
#: 0.60 means at least three of the six terms must be observable, and — given the
#: weights above — that grounding alone, or grounding plus one small term, is never
#: enough to produce a number. A score built from two observations reads on a memo
#: exactly like a score built from six.
MIN_ASSESSED_WEIGHT = 0.60

#: Freshness half-life. A source loses half its freshness score each year. This is a
#: decay, not a cliff, because a two-year-old mechanism is often still true while a
#: two-year-old level rarely is, and the harness cannot tell which from the age alone —
#: `engine/temporal.py` owns that distinction and does it properly.
FRESHNESS_HALF_LIFE_DAYS = 365.0

assert abs(sum(_WEIGHTS.values()) - 1.0) < 1e-9, "confidence weights must sum to 1.0"


def weights() -> Mapping[str, float]:
    """The D4 weight table, read-only. Exposed so a memo can print what produced a
    score without any caller being able to change it."""
    return _WEIGHTS


def age_in_days(source_date: Optional[date], current_date: date) -> Optional[int]:
    """Age of a source at the analysis date, or `None` when the source is undated.

    `current_date` is REQUIRED and is a parameter. There is deliberately no default and
    no clock read: a freshness score that quietly means "today" is a fact about when the
    process ran, presented as a fact about the evidence.

    A source dated in the future clamps to 0 rather than scoring above full freshness.
    """
    if source_date is None:
        return None
    return max(0, (current_date - source_date).days)


def _independence_score(distinct_sources: int) -> float:
    """Diminishing credit for corroboration: 1, 2, 3, 4 sources -> 0.50, 0.75, 0.88, 0.94.

    A single source is worth half, not zero — most true claims are first read once. The
    curve is `1 - 2**-n` so the second source is the big move and the fifth is noise,
    which matches how corroboration actually informs a view.
    """
    if distinct_sources <= 0:
        return 0.0
    return 1.0 - 2.0 ** (-float(distinct_sources))


def _freshness_score(age_days: int) -> float:
    return 0.5 ** (max(0, age_days) / FRESHNESS_HALF_LIFE_DAYS)


def signals_from_verdict(
    verdict: GroundingVerdict,
    *,
    source_reliability: Optional[float] = None,
    distinct_sources: Optional[int] = None,
    source_date: Optional[date] = None,
    current_date: Optional[date] = None,
    model_confidence: Optional[float] = None,
    numbers_checked: Optional[bool] = None,
) -> ConfidenceSignals:
    """Build `ConfidenceSignals` from a harness verdict plus context the caller knows.

    Everything the verdict already established is copied, never re-derived. Everything
    it cannot know (who published it, how many other sources say it, what today is) must
    be supplied, and stays `None` when it is not — which is what later makes the
    difference between a low score and an abstention.

    `numbers_checked` defaults to "the check ran unless the verdict says it was skipped",
    inferred from the verdict's own wording only when the caller does not say.
    """
    checked = (
        numbers_checked
        if numbers_checked is not None
        else "not checked by policy" not in verdict.reason
    )
    return ConfidenceSignals(
        grounding_method=verdict.method,
        span_found=verdict.span_found,
        numbers_checked=checked,
        numbers_verified=verdict.numbers_verified,
        entailment_score=verdict.entailment_score,
        source_reliability=source_reliability,
        distinct_sources=distinct_sources,
        age_days=age_in_days(source_date, current_date) if current_date else None,
        model_confidence=model_confidence,
    )


def compute_atom_confidence(signals: ConfidenceSignals) -> AtomConfidence:
    """Score one claim from harness observations, or decline to.

    Returns an `AtomConfidence` whose `outcome` is one of:

    * `ungrounded` — no span. Value exactly 0.0; the claim supports nothing.
    * `abstained` — span found, too little observed to average. Value `None`.
    * `computed` — a weighted average of the observable terms, capped by the model's own
      self-report when that is lower.
    """
    if not signals.span_found or signals.grounding_method == "none":
        return AtomConfidence(
            version=CONFIDENCE_VERSION,
            outcome="ungrounded",
            value=0.0,
            reason="no source span located; the claim supports nothing",
            components=AtomConfidenceComponents(assessed_weight=0.0),
        )

    scores: dict[str, float] = {"grounding": _METHOD_SCORE[signals.grounding_method]}

    if signals.numbers_checked:
        scores["numbers"] = 1.0 if signals.numbers_verified else 0.0
    if signals.source_reliability is not None:
        scores["reliability"] = signals.source_reliability
    if signals.distinct_sources is not None:
        scores["independence"] = _independence_score(signals.distinct_sources)
    if signals.age_days is not None:
        scores["freshness"] = _freshness_score(signals.age_days)
    if signals.entailment_score is not None:
        scores["entailment"] = signals.entailment_score

    assessed_weight = sum(_WEIGHTS[name] for name in scores)
    components = AtomConfidenceComponents(
        assessed_weight=assessed_weight,
        **{name: scores.get(name) for name in _WEIGHTS},
    )

    if assessed_weight < MIN_ASSESSED_WEIGHT:
        observed = ", ".join(sorted(scores)) or "nothing"
        return AtomConfidence(
            version=CONFIDENCE_VERSION,
            outcome="abstained",
            value=None,
            reason=(
                f"only {assessed_weight:.2f} of the weight was observable "
                f"({observed}); below the {MIN_ASSESSED_WEIGHT:.2f} floor, so no "
                "confidence is reported"
            ),
            components=components,
        )

    value = sum(_WEIGHTS[name] * score for name, score in scores.items()) / assessed_weight

    capped = signals.model_confidence is not None and signals.model_confidence < value
    if capped:
        value = float(signals.model_confidence)

    value = max(0.0, min(1.0, value))
    return AtomConfidence(
        version=CONFIDENCE_VERSION,
        outcome="computed",
        value=value,
        reason=(
            f"weighted over {assessed_weight:.2f} of the terms"
            + (
                f"; capped at the model's own {signals.model_confidence:.2f}"
                if capped
                else ""
            )
        ),
        components=components.model_copy(update={"model_cap_applied": capped}),
    )


def preference_key(outcome: AtomConfidence | Insufficient) -> tuple[int, float]:
    """Sort key implementing the plan's ordering: **an abstention beats a confident
    ungrounded answer.**

    Three bands, low to high:

    0. ungrounded, or a computed 0.0 — the claim rests on nothing.
    1. abstained, whether an `AtomConfidence` or a seam-level `Insufficient` — the
       harness declined, which is a better answer than a number it could not support.
    2. computed and positive — ordered by the value.

    Sorting descending puts the best-evidenced claim first and an unsourced one last,
    which is the whole point: fluency must not be able to outrank absence.
    """
    if isinstance(outcome, Insufficient):
        return (1, 0.0)
    if outcome.outcome == "abstained":
        return (1, 0.0)
    value = outcome.value or 0.0
    return ((2, value) if outcome.outcome == "computed" and value > 0.0 else (0, value))


__all__ = [
    "CONFIDENCE_VERSION",
    "FRESHNESS_HALF_LIFE_DAYS",
    "MIN_ASSESSED_WEIGHT",
    "age_in_days",
    "compute_atom_confidence",
    "preference_key",
    "signals_from_verdict",
    "weights",
]
