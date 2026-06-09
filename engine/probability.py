"""Q4 probability engine — a PROVENANCE & DISCIPLINE layer over scenario p_s, not a perfect
Bayesian engine. Deterministic. It never generates scenarios and never invents p_s. The
effective (posterior) vector is an AUDIT artifact — pricing keeps reading Scenario.p_s, so
the golden master is unchanged (the golden cases carry no evidence ⇒ posterior == prior).

PART 2 public API: validate_probability_vector, wrap_supplied_probabilities,
apply_evidence_tilt, justify_probabilities, probability_quality."""
from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from typing import Optional

from .schema import (
    ProbabilityEvidenceBundle,
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
_IMPACT: dict[str, float] = {"increase": 1.0, "decrease": -1.0, "neutral": 0.0, "contradictory": 0.0}


@dataclass(frozen=True)
class ProbabilityPolicy:
    """Deterministic tilt/quality knobs. Defaults keep the layer gentle and disciplined."""
    eps: float = 1e-9
    sum_tol: float = 1e-6
    full_evidence_count: int = 3        # ref count at which evidence_confidence saturates
    contradiction_penalty: float = 0.5  # max haircut to confidence/quality from contradictions
    unjustified_warning: str = "Probabilities supplied but not evidence-justified."


# ── 1. validate ───────────────────────────────────────────────────────────────

def validate_probability_vector(
    scenarios: list[Scenario], policy: Optional[ProbabilityPolicy] = None
) -> tuple[bool, list[str]]:
    """Return (sums_to_one, warnings). Never raises — supplied p_s are preserved, not fixed."""
    policy = policy or ProbabilityPolicy()
    warnings: list[str] = []
    for s in scenarios:
        if not (0.0 <= s.p_s <= 1.0):
            warnings.append(f"{s.name}: p_s={s.p_s} out of [0,1]")
    total = sum(s.p_s for s in scenarios)
    sums_to_one = (not scenarios) or abs(total - 1.0) <= policy.sum_tol
    if scenarios and not sums_to_one:
        warnings.append(f"probabilities sum to {total:.6f}, not 1.0")
    return sums_to_one, warnings


# ── 2. wrap (the no-evidence default path) ────────────────────────────────────

def wrap_supplied_probabilities(
    scenarios: list[Scenario], policy: Optional[ProbabilityPolicy] = None
) -> ProbabilitySetJustification:
    """Default behaviour when p_s are supplied but no evidence is given: label PM_assumption,
    posterior == prior, low-to-medium quality, and a warning."""
    policy = policy or ProbabilityPolicy()
    sums_to_one, warnings = validate_probability_vector(scenarios, policy)
    if scenarios:
        warnings.append(policy.unjustified_warning)
    rows = [_row(s, prior_src="PM_assumption", post_src="PM_assumption",
                 posterior=s.p_s, refs=[], evidence_confidence=0.0) for s in scenarios]
    return _assemble(rows, sums_to_one, [s.p_s for s in scenarios], warnings)


# ── 3. evidence tilt (deterministic; softmax + haircut toward prior) ──────────

def apply_evidence_tilt(
    priors: dict[str, float],
    evidence_by_scenario: dict[str, list[ProbabilityEvidenceRef]],
    policy: Optional[ProbabilityPolicy] = None,
) -> tuple[dict[str, float], float]:
    """score_s = log(max(prior_s, eps)) + Σ_j impact·strength·reliability·freshness;
    posterior_raw = softmax(score); posterior = (1-ec)·prior + ec·posterior_raw.
    Returns (posterior_by_name, evidence_confidence). Deterministic in scenario order."""
    policy = policy or ProbabilityPolicy()
    names = list(priors.keys())
    scores, total_refs, contra, rel_fresh = [], 0, 0, []
    for name in names:
        refs = evidence_by_scenario.get(name, [])
        impact = sum(_IMPACT[r.direction] * r.strength * r.reliability * r.freshness for r in refs)
        scores.append(math.log(max(priors[name], policy.eps)) + impact)
        total_refs += len(refs)
        contra += sum(1 for r in refs if r.direction == "contradictory")
        rel_fresh += [r.reliability * r.freshness for r in refs if r.direction != "contradictory"]
    raw = _softmax(scores)
    base = (sum(rel_fresh) / len(rel_fresh)) if rel_fresh else 0.0
    count_factor = min(1.0, total_refs / max(1, policy.full_evidence_count))
    contra_share = (contra / total_refs) if total_refs else 0.0
    ec = _clip01(base * count_factor * (1.0 - policy.contradiction_penalty * contra_share))
    posterior = {n: _clip01((1.0 - ec) * priors[n] + ec * raw[i]) for i, n in enumerate(names)}
    return posterior, ec


# ── 4. justify (orchestrator) ─────────────────────────────────────────────────

def justify_probabilities(
    theme_object,
    scenarios: list[Scenario],
    evidence_bundle: Optional[ProbabilityEvidenceBundle] = None,
    policy: Optional[ProbabilityPolicy] = None,
    *,
    evidence_atoms=None,
    evidence_maps=None,
    causal_object=None,
    update_policy=None,
) -> ProbabilitySetJustification:
    """Label each supplied p_s with provenance/evidence/confidence; tilt only when evidence is
    supplied (else wrap). `theme_object` is reserved context (may be None — the workflow has no
    theme yet when it calls this). Never invents or generates p_s.

    PART-2c bridge: when `evidence_atoms` or `evidence_maps` are supplied, route them through the
    deterministic evidence→posterior engine and return a justification carrying the
    ProbabilityUpdateAudit (the legacy ProbabilityEvidenceRef path is otherwise unchanged)."""
    policy = policy or ProbabilityPolicy()

    if evidence_atoms is not None or evidence_maps is not None:
        from .probability_evidence import map_evidence_to_scenarios, update_probabilities_from_evidence
        maps = evidence_maps
        if maps is None:
            maps = map_evidence_to_scenarios(scenarios, evidence_atoms or [], causal_object)
        audit = update_probabilities_from_evidence(scenarios, maps, update_policy)
        return _assemble_from_audit(scenarios, audit)

    if not scenarios:
        return _assemble([], True, [], [])

    ev = evidence_bundle.evidence_by_scenario if evidence_bundle else {}
    overrides = evidence_bundle.prior_sources if evidence_bundle else {}
    has_evidence = any(ev.get(s.name) for s in scenarios)
    if not has_evidence and not overrides:
        return wrap_supplied_probabilities(scenarios, policy)

    sums_to_one, warnings = validate_probability_vector(scenarios, policy)
    if has_evidence:
        posterior, ec = apply_evidence_tilt({s.name: s.p_s for s in scenarios}, ev, policy)
    else:
        posterior, ec = {s.name: s.p_s for s in scenarios}, 0.0
        warnings.append(policy.unjustified_warning)

    rows = []
    for s in scenarios:
        refs = ev.get(s.name, [])
        prior_src: ProbabilitySource = overrides.get(s.name, "PM_assumption")
        post_src = _posterior_source(prior_src, refs, s.name, warnings)
        rows.append(_row(s, prior_src=prior_src, post_src=post_src,
                         posterior=posterior[s.name], refs=refs, evidence_confidence=ec))
    return _assemble(rows, sums_to_one, [posterior[s.name] for s in scenarios], warnings)


# ── 5. quality ────────────────────────────────────────────────────────────────

def probability_quality(probability_set: ProbabilitySetJustification) -> float:
    """min(weakest-source ceiling, mean confidence), reduced by contradiction share and hard-
    capped low when the set does not sum to 1."""
    rows = probability_set.scenario_probabilities
    return _quality(rows, probability_set.sums_to_one)


# ── internals ─────────────────────────────────────────────────────────────────

def _posterior_source(prior_src, refs, name, warnings) -> "ProbabilitySource":
    if refs:
        return "evidence_weighted"
    if prior_src == "evidence_weighted":                      # claimed but no refs → downgrade
        warnings.append(f"{name}: evidence_weighted claimed with no evidence -> unknown")
        return "unknown"
    return prior_src  # type: ignore[return-value]


def _row(s, *, prior_src, post_src, posterior, refs, evidence_confidence
         ) -> ScenarioProbabilityJustification:
    conf, cap = _scenario_confidence(post_src, refs, evidence_confidence)
    return ScenarioProbabilityJustification(
        scenario_name=s.name,
        prior_probability=s.p_s, prior_source=prior_src,
        posterior_probability=round(_clip01(posterior), 12), posterior_source=post_src,
        evidence_for=[r for r in refs if r.direction in ("increase", "neutral")],
        evidence_against=[r for r in refs if r.direction in ("decrease", "contradictory")],
        confidence=conf, confidence_cap_reason=cap,
        rationale=(f"prior {prior_src} tilted by evidence (ec={evidence_confidence:.2f})"
                   if refs else "supplied p_s, not evidence-justified"),
        unresolved_questions=[] if refs else [f"What evidence supports p_s for {s.name}?"],
    )


def _scenario_confidence(source, refs, ec) -> tuple[float, Optional[str]]:
    ceiling = _SOURCE_CEILING[source]
    if not refs:
        return ceiling, f"no evidence; source={source} ceiling {ceiling:.2f}"
    supportive = [r for r in refs if r.direction != "contradictory"]
    base = (sum(r.strength * r.reliability * r.freshness for r in supportive) / len(supportive)
            if supportive else 0.0)
    contra_local = sum(1 for r in refs if r.direction == "contradictory") / len(refs)
    conf = _clip01(min(ceiling, base) * (1.0 - 0.5 * contra_local))
    return conf, (f"capped at {source} ceiling {ceiling:.2f}" if base > ceiling else None)


def _quality(rows, sums_to_one) -> float:
    if not rows:
        return 0.0
    floor = min(_SOURCE_CEILING[r.posterior_source] for r in rows)
    mean_conf = sum(r.confidence for r in rows) / len(rows)
    contra = sum(1 for row in rows for r in row.evidence_against if r.direction == "contradictory")
    total = sum(len(row.evidence_for) + len(row.evidence_against) for row in rows)
    contra_share = (contra / total) if total else 0.0
    q = min(floor, mean_conf) * (1.0 - 0.5 * contra_share)
    return _clip01(q if sums_to_one else min(q, 0.25))


def _assemble_from_audit(scenarios, audit) -> ProbabilitySetJustification:
    """Wrap a ProbabilityUpdateAudit (PART-2c) as a ProbabilitySetJustification. Posterior is an
    audit artifact; per-scenario rows carry prior→posterior with evidence_weighted provenance
    where the scenario received mapped impacts."""
    rows = []
    for i, s in enumerate(scenarios):
        has_ev = bool(audit.evidence_maps[i].impacts)
        rows.append(ScenarioProbabilityJustification(
            scenario_name=s.name,
            prior_probability=_clip01(audit.prior_vector[i]), prior_source="PM_assumption",
            posterior_probability=round(_clip01(audit.posterior_vector[i]), 12),
            posterior_source="evidence_weighted" if has_ev else "PM_assumption",
            evidence_for=[], evidence_against=[],
            confidence=_clip01(audit.probability_quality),
            confidence_cap_reason=(audit.warnings[0] if audit.warnings else None),
            rationale=f"posterior via {audit.update_method}",
            unresolved_questions=[],
        ))
    vec = list(audit.posterior_vector)
    return ProbabilitySetJustification(
        scenario_probabilities=rows,
        sums_to_one=(abs(sum(vec) - 1.0) <= 1e-6) if vec else True,
        probability_quality=_clip01(audit.probability_quality),
        probability_source_summary=audit.update_method,
        effective_probability_vector=[round(_clip01(v), 12) for v in vec],
        warnings=list(audit.warnings),
        update_audit=audit,
    )


def _assemble(rows, sums_to_one, vector, warnings) -> ProbabilitySetJustification:
    return ProbabilitySetJustification(
        scenario_probabilities=rows,
        sums_to_one=sums_to_one,
        probability_quality=_quality(rows, sums_to_one),
        probability_source_summary=_summary(rows),
        effective_probability_vector=[round(_clip01(v), 12) for v in vector],
        warnings=warnings,
    )


def _summary(rows) -> str:
    counts = Counter(r.posterior_source for r in rows)
    return ", ".join(f"{k}:{v}" for k, v in sorted(counts.items()))


def _softmax(scores: list[float]) -> list[float]:
    if not scores:
        return []
    m = max(scores)
    exps = [math.exp(x - m) for x in scores]
    total = sum(exps)
    return [e / total for e in exps]


def _clip01(x: float) -> float:
    return max(0.0, min(1.0, x))
