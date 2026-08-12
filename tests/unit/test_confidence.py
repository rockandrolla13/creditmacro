"""G4 — computed confidence and abstention.

The tests that matter here are the ORDERING ones. A weighted average can be re-tuned;
the guarantee that an abstention outranks a confident ungrounded claim cannot, because
that is the property the whole guardrail exists to provide.
"""
from __future__ import annotations

from datetime import date

import pytest

from engine.grounding.confidence import (
    CONFIDENCE_VERSION,
    MIN_ASSESSED_WEIGHT,
    age_in_days,
    compute_atom_confidence,
    preference_key,
    signals_from_verdict,
    weights,
)
from engine.schema.confidence import ConfidenceSignals, Insufficient
from engine.schema.grounding import GroundingVerdict


def _signals(**over) -> ConfidenceSignals:
    """A fully-observed, well-grounded atom. Tests vary one thing at a time from here."""
    base = dict(
        grounding_method="exact",
        span_found=True,
        numbers_checked=True,
        numbers_verified=True,
        source_reliability=0.90,
        distinct_sources=1,
        age_days=0,
    )
    base.update(over)
    return ConfidenceSignals(**base)


# ── D4: the weights are fixed, named, and version-stamped ────────────────────

def test_weights_sum_to_one_and_are_read_only():
    assert abs(sum(weights().values()) - 1.0) < 1e-9
    with pytest.raises(TypeError):
        weights()["grounding"] = 0.99          # MappingProxyType — not tunable per run


def test_every_outcome_stamps_the_version():
    for signals in (_signals(), _signals(span_found=False), _signals(source_reliability=None,
                                                                    distinct_sources=None,
                                                                    age_days=None)):
        assert compute_atom_confidence(signals).version == CONFIDENCE_VERSION


# ── the ordering the plan requires ───────────────────────────────────────────

def test_grounded_independent_fresh_beats_grounded_only_beats_ungrounded():
    best = compute_atom_confidence(_signals(distinct_sources=4, age_days=0))
    middling = compute_atom_confidence(_signals(distinct_sources=1, age_days=1500))
    none = compute_atom_confidence(_signals(span_found=False, grounding_method="none"))

    assert best.value > middling.value > 0.0
    assert none.outcome == "ungrounded"
    assert none.value == 0.0


def test_abstention_outranks_a_confident_ungrounded_claim():
    """The plan's non-negotiable, as an ordering: fluency must not outrank absence."""
    ungrounded_but_certain = compute_atom_confidence(
        _signals(span_found=False, grounding_method="none", model_confidence=1.0)
    )
    abstained = compute_atom_confidence(
        ConfidenceSignals(grounding_method="exact", span_found=True)
    )
    assert abstained.outcome == "abstained"
    assert preference_key(abstained) > preference_key(ungrounded_but_certain)


def test_a_seam_insufficient_ranks_with_an_abstention_and_below_a_real_score():
    insufficient = Insufficient(seam="define_axis", reason="no clean differential",
                                missing=("a second leg with a live series",))
    real = compute_atom_confidence(_signals())
    ungrounded = compute_atom_confidence(_signals(span_found=False, grounding_method="none"))

    assert preference_key(real) > preference_key(insufficient) > preference_key(ungrounded)


def test_sorting_puts_the_best_evidenced_first_and_the_unsourced_last():
    outcomes = [
        compute_atom_confidence(_signals(span_found=False, grounding_method="none")),
        compute_atom_confidence(ConfidenceSignals(grounding_method="exact", span_found=True)),
        compute_atom_confidence(_signals(distinct_sources=4)),
    ]
    ranked = sorted(outcomes, key=preference_key, reverse=True)
    assert [o.outcome for o in ranked] == ["computed", "abstained", "ungrounded"]


# ── abstention: the harness saying "I do not know" ───────────────────────────

def test_too_few_observable_terms_abstains_rather_than_reporting_a_number():
    thin = compute_atom_confidence(
        ConfidenceSignals(grounding_method="exact", span_found=True,
                          numbers_checked=True, numbers_verified=True)
    )
    assert thin.components.assessed_weight < MIN_ASSESSED_WEIGHT
    assert thin.outcome == "abstained"
    assert thin.value is None
    assert "below the" in thin.reason


def test_one_more_observed_term_turns_an_abstention_into_a_score():
    thin = ConfidenceSignals(grounding_method="exact", span_found=True,
                             numbers_checked=True, numbers_verified=True)
    assert compute_atom_confidence(thin).outcome == "abstained"

    thicker = thin.model_copy(update={"source_reliability": 0.9})
    scored = compute_atom_confidence(thicker)
    assert scored.outcome == "computed"
    assert scored.components.assessed_weight >= MIN_ASSESSED_WEIGHT


def test_unassessed_terms_are_none_not_zero():
    """`None` means not established. Scoring an unknown source as 0.0 reliability would
    be inventing a fact about the publisher."""
    c = compute_atom_confidence(_signals(source_reliability=None)).components
    assert c.reliability is None
    assert c.numbers == 1.0


# ── fail-closed ──────────────────────────────────────────────────────────────

def test_ungrounded_scores_exactly_zero_whatever_the_model_claimed():
    for claimed in (0.0, 0.5, 1.0):
        out = compute_atom_confidence(
            _signals(span_found=False, grounding_method="none", model_confidence=claimed)
        )
        assert out.outcome == "ungrounded" and out.value == 0.0


def test_a_caught_transcription_error_costs_the_whole_numbers_term():
    verified = compute_atom_confidence(_signals(numbers_verified=True))
    caught = compute_atom_confidence(_signals(numbers_verified=False))
    assert caught.value < verified.value
    assert caught.components.numbers == 0.0


def test_an_unchecked_number_is_not_scored_as_a_failed_one():
    unchecked = compute_atom_confidence(_signals(numbers_checked=False, numbers_verified=False))
    failed = compute_atom_confidence(_signals(numbers_checked=True, numbers_verified=False))
    assert unchecked.components.numbers is None
    assert failed.components.numbers == 0.0
    assert unchecked.value > failed.value


# ── the model's confidence is a cap, never a lift ────────────────────────────

def test_model_confidence_can_only_lower():
    signals = _signals(distinct_sources=4)
    uncapped = compute_atom_confidence(signals)

    lifted = compute_atom_confidence(signals.model_copy(update={"model_confidence": 1.0}))
    assert lifted.value == uncapped.value
    assert lifted.components.model_cap_applied is False

    lowered = compute_atom_confidence(signals.model_copy(update={"model_confidence": 0.2}))
    assert lowered.value == pytest.approx(0.2)
    assert lowered.components.model_cap_applied is True
    assert "capped" in lowered.reason


# ── monotonicity ─────────────────────────────────────────────────────────────

def test_more_distinct_sources_never_lowers_confidence():
    values = [compute_atom_confidence(_signals(distinct_sources=n)).value for n in range(1, 6)]
    assert values == sorted(values)


def test_an_older_source_never_scores_higher_than_a_newer_one():
    values = [compute_atom_confidence(_signals(age_days=d)).value
              for d in (0, 90, 365, 730, 3650)]
    assert values == sorted(values, reverse=True)


def test_a_weaker_match_method_never_scores_higher():
    values = [compute_atom_confidence(_signals(grounding_method=m)).value
              for m in ("exact", "normalized", "loose_human_confirmed")]
    assert values == sorted(values, reverse=True)


# ── freshness needs a supplied date; there is no clock (I8) ──────────────────

def test_age_in_days_requires_a_supplied_current_date():
    assert age_in_days(date(2025, 1, 1), date(2026, 1, 1)) == 365
    assert age_in_days(None, date(2026, 1, 1)) is None
    with pytest.raises(TypeError):
        age_in_days(date(2025, 1, 1))          # no default "today"


def test_a_future_dated_source_clamps_rather_than_scoring_above_full_freshness():
    assert age_in_days(date(2027, 1, 1), date(2026, 1, 1)) == 0


def test_signals_from_verdict_leaves_freshness_unassessed_without_a_current_date():
    verdict = GroundingVerdict(status="grounded", method="exact", span_found=True,
                               numbers_verified=True, reason="ok")
    assert signals_from_verdict(verdict).age_days is None
    assert signals_from_verdict(verdict, source_date=date(2025, 1, 1),
                                current_date=date(2026, 1, 1)).age_days == 365


def test_signals_from_verdict_copies_the_harness_findings():
    verdict = GroundingVerdict(status="grounded", method="normalized", span_found=True,
                               numbers_verified=True, reason="span located",
                               entailment_score=0.8)
    signals = signals_from_verdict(verdict, source_reliability=0.6, distinct_sources=2)
    assert signals.grounding_method == "normalized"
    assert signals.numbers_checked is True
    assert signals.entailment_score == 0.8


def test_signals_from_verdict_reads_a_policy_skip_as_unchecked():
    skipped = GroundingVerdict(status="grounded", method="exact", span_found=True,
                               numbers_verified=False,
                               reason="span located; numbers not checked by policy")
    assert signals_from_verdict(skipped).numbers_checked is False


# ── the schema refuses to represent an incoherent outcome ────────────────────

def test_an_abstention_cannot_carry_a_value():
    from engine.schema.confidence import AtomConfidence, AtomConfidenceComponents

    with pytest.raises(ValueError):
        AtomConfidence(version="x", outcome="abstained", value=0.3, reason="r",
                       components=AtomConfidenceComponents(assessed_weight=0.1))
    with pytest.raises(ValueError):
        AtomConfidence(version="x", outcome="ungrounded", value=0.3, reason="r",
                       components=AtomConfidenceComponents(assessed_weight=0.0))


def test_a_computed_confidence_is_frozen():
    out = compute_atom_confidence(_signals())
    with pytest.raises(Exception):
        out.value = 0.99
