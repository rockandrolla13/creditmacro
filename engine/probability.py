"""Q4 — justify_probabilities(): label supplied p_s with provenance/evidence/confidence and
cap quality by the WEAKEST source. Pure & audit-only — never invents, mutates, or prices.
Evidence is pre-gated by the caller (workflow), so this module stays firewall-free."""
from __future__ import annotations

from collections import Counter
from typing import Optional

from .schema import (
    ProbabilityEvidenceRef,
    ProbabilitySetJustification,
    ProbabilitySource,
    Scenario,
    ScenarioProbabilityJustification,
)

# The WEAKEST source present caps the whole set's probability_quality (not an average).
_SOURCE_CEILING: dict[str, float] = {
    "evidence_weighted": 1.00, "historical_base_rate": 0.90, "model_output": 0.80,
    "PM_assumption": 0.50, "unknown": 0.25,
}
_SUM_TOL = 1e-6
_UNNORMALISED_QUALITY = 0.25   # a set that doesn't sum to 1 cannot be high quality


def justify_probabilities(
    scenarios: list[Scenario],
    evidence: Optional[dict[str, list[ProbabilityEvidenceRef]]] = None,
    prior_sources: Optional[dict[str, ProbabilitySource]] = None,
) -> ProbabilitySetJustification:
    """Label each supplied p_s; never re-weight (posterior == prior). `evidence` (per scenario
    name) is already firewall-gated by the caller. Returns the audit record."""
    evidence = evidence or {}
    prior_sources = prior_sources or {}
    warnings: list[str] = []
    rows: list[ScenarioProbabilityJustification] = []

    for s in scenarios:
        refs = evidence.get(s.name, [])
        prior_src: ProbabilitySource = prior_sources.get(s.name, "PM_assumption")
        post_src = _resolve_source(s.name, prior_src, refs, warnings)
        conf, cap = _confidence(post_src, refs)
        rows.append(ScenarioProbabilityJustification(
            scenario_name=s.name,
            prior_probability=s.p_s, prior_source=prior_src,
            posterior_probability=s.p_s, posterior_source=post_src,   # audit-only: unchanged
            evidence_for=[r for r in refs if r.direction in ("increase", "neutral")],
            evidence_against=[r for r in refs if r.direction in ("decrease", "contradictory")],
            confidence=conf, confidence_cap_reason=cap,
            rationale=f"supplied p_s labeled {post_src}; not re-weighted (Q4 audit-only)",
            unresolved_questions=[] if refs else [f"What evidence supports p_s for {s.name}?"],
        ))

    vector = [s.p_s for s in scenarios]
    total = sum(vector)
    sums_to_one = abs(total - 1.0) <= _SUM_TOL
    if not sums_to_one:
        warnings.append(f"supplied probabilities sum to {total:.6f}, not 1.0")

    return ProbabilitySetJustification(
        scenario_probabilities=rows,
        sums_to_one=sums_to_one,
        probability_quality=_set_quality(rows, sums_to_one),
        probability_source_summary=_summary(rows),
        effective_probability_vector=vector,
        warnings=warnings,
    )


def _resolve_source(name: str, prior_src: str, refs: list, warnings: list) -> "ProbabilitySource":
    """evidence_weighted requires ≥1 ref; claimed-without-evidence downgrades to unknown."""
    if refs:
        return "evidence_weighted"
    if prior_src == "evidence_weighted":
        warnings.append(f"{name}: evidence_weighted claimed with no evidence -> unknown")
        return "unknown"
    return prior_src  # type: ignore[return-value]


def _confidence(source: str, refs: list) -> tuple[float, Optional[str]]:
    """Per-scenario confidence = evidence weight, capped at the source ceiling."""
    ceiling = _SOURCE_CEILING[source]
    if not refs:
        return ceiling, f"no evidence; source={source} ceiling {ceiling:.2f}"
    # TODO(tune): evidence weight = mean(strength*reliability*freshness) across refs.
    w = sum(r.strength * r.reliability * r.freshness for r in refs) / len(refs)
    capped = min(ceiling, w)
    return capped, (f"capped at {source} ceiling {ceiling:.2f}" if w > ceiling else None)


def _set_quality(rows: list, sums_to_one: bool) -> float:
    """probability_quality = min(weakest-source ceiling, mean confidence); an un-normalised
    set is hard-capped low (it isn't a probability distribution)."""
    if not rows:
        return 0.0
    floor = min(_SOURCE_CEILING[r.posterior_source] for r in rows)
    mean_conf = sum(r.confidence for r in rows) / len(rows)
    q = min(floor, mean_conf)
    return q if sums_to_one else min(q, _UNNORMALISED_QUALITY)


def _summary(rows: list) -> str:
    counts = Counter(r.posterior_source for r in rows)
    return ", ".join(f"{k}:{v}" for k, v in sorted(counts.items()))
