"""Q4 PART-2b — deterministic evidence-to-scenario mapper.

Routes SUPPLIED, source-backed evidence atoms to SUPPLIED scenarios. It never generates
scenarios and never invents p_s — it only classifies, weights, clusters (to avoid
double-counting), and records warnings for atoms it cannot map. The output (`ScenarioEvidenceMap`
per scenario) is the input to the PART-2c posterior update; the posterior remains an audit
artifact (pricing keeps reading Scenario.p_s), so the golden master is untouched.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Optional

from .schema import (
    EvidenceAtom,
    ProbabilityUpdateAudit,
    Scenario,
    ScenarioEvidenceImpact,
    ScenarioEvidenceMap,
)

# Reliability prior by claim kind (rule 6). PM_assumption is a PRIOR, not evidence support → 0.
RELIABILITY_DEFAULTS: dict[str, float] = {
    "source_fact": 0.90,
    "source_forecast": 0.60,
    "source_opinion": 0.40,
    "agent_synthesis": 0.40,   # bumped when evidence-backed (cites numbers / a source location)
    "model_output": 0.70,
    "PM_assumption": 0.0,
}

_STOP = {
    "the", "and", "for", "with", "from", "into", "that", "this", "are", "was", "were",
    "has", "have", "its", "per", "vs", "versus", "than", "over", "under", "more", "less",
    "rises", "rise", "falls", "fall", "keep", "here", "their", "they", "our",
}
_FORECAST_WORDS = {
    "expect", "expects", "expected", "forecast", "forecasts", "forecasting", "project",
    "projects", "projected", "outlook", "guidance", "anticipate", "anticipates", "estimate",
    "estimates", "likely",
}
_OPINION_WORDS = {
    "think", "thinks", "believe", "believes", "view", "views", "opinion", "attractive",
    "unattractive", "cheap", "rich", "prefer", "prefers", "favour", "favor", "crowded",
    "overvalued", "undervalued", "compelling",
}


@dataclass(frozen=True)
class EvidenceMappingPolicy:
    """Deterministic mapper knobs. `overlap_min` significant shared tokens are required before an
    atom is routed to a scenario (filters incidental single-word matches)."""
    overlap_min: int = 2
    default_freshness: float = 1.0
    synthesis_backed_reliability: float = 0.60


def _tokens(text: str) -> set[str]:
    out: set[str] = set()
    for w in re.findall(r"[a-z0-9]+", (text or "").lower()):
        if w.isdigit():
            if len(w) >= 2:
                out.add(w)
        elif len(w) >= 3 and w not in _STOP:
            out.add(w)
    return out


def _atom_keywords(atom: EvidenceAtom) -> set[str]:
    kw = _tokens(" ".join(atom.market_variables + atom.entities + atom.concepts + atom.themes))
    kw |= {str(int(n)) for n in atom.numbers if float(n).is_integer()}
    return kw


def _scenario_keywords(scn: Scenario) -> set[str]:
    return _tokens(f"{scn.name} {scn.driver_path}")


def _cluster_id(atom: EvidenceAtom) -> str:
    if atom.evidence_cluster_id:
        return atom.evidence_cluster_id
    for field in (atom.themes, atom.concepts, atom.entities):
        if field:
            return field[0]
    return atom.evidence_id or f"atom:{atom.claim[:32]}"


def classify_claim_kind(atom: EvidenceAtom) -> str:
    """Classify an atom's claim_kind (rule 5). Explicit kind wins; then synthesis flag; then
    opinion/forecast vocabulary; else a hard source fact."""
    if atom.claim_kind:
        return atom.claim_kind
    if atom.is_synthesis:
        return "agent_synthesis"
    words = set(re.findall(r"[a-z']+", atom.claim.lower()))
    if words & _OPINION_WORDS:
        return "source_opinion"
    if words & _FORECAST_WORDS:
        return "source_forecast"
    return "source_fact"


def _reliability(kind: str, atom: EvidenceAtom, policy: EvidenceMappingPolicy) -> float:
    base = RELIABILITY_DEFAULTS[kind]
    if kind == "agent_synthesis" and (atom.numbers or atom.source_location):
        base = max(base, policy.synthesis_backed_reliability)
    return base


def map_evidence_to_scenarios(
    scenarios: list[Scenario],
    evidence_atoms: list[EvidenceAtom],
    causal_object=None,
    policy: Optional[EvidenceMappingPolicy] = None,
) -> list[ScenarioEvidenceMap]:
    """Map supplied evidence atoms to supplied scenarios. Returns exactly one
    ScenarioEvidenceMap per scenario (in order). Atoms that overlap no scenario, and
    PM_assumptions (priors, not support), are left unused with a recorded warning."""
    policy = policy or EvidenceMappingPolicy()
    if not scenarios:
        return []

    scn_kw = {s.name: _scenario_keywords(s) for s in scenarios}
    # per scenario: list of (atom, kind, cluster_id) and a warnings list
    mapped: dict[str, list[tuple]] = {s.name: [] for s in scenarios}
    warns: dict[str, list[str]] = {s.name: [] for s in scenarios}

    for atom in evidence_atoms:
        kind = classify_claim_kind(atom)
        akw = _atom_keywords(atom)
        overlaps = {s.name: len(akw & scn_kw[s.name]) for s in scenarios}
        nearest = max(scenarios, key=lambda s: overlaps[s.name]).name
        if overlaps[nearest] == 0:
            nearest = scenarios[0].name
        ident = atom.evidence_id or atom.claim[:40]

        if kind == "PM_assumption":
            warns[nearest].append(f"evidence '{ident}': PM_assumption is a prior, not evidence support — unused")
            continue
        hits = [s.name for s in scenarios if overlaps[s.name] >= policy.overlap_min]
        if not hits:
            warns[nearest].append(f"evidence '{ident}': could not be mapped to any scenario — unused")
            continue
        for name in hits:
            mapped[name].append((atom, kind, _cluster_id(atom)))

    return [_build_map(s.name, mapped[s.name], warns[s.name], scn_kw[s.name], policy)
            for s in scenarios]


def _build_map(scenario_name, rows, warnings, scn_kw, policy) -> ScenarioEvidenceMap:
    cluster_sizes = Counter(cid for _, _, cid in rows)
    impacts: list[ScenarioEvidenceImpact] = []
    for atom, kind, cid in rows:
        direction = atom.direction or "increase"
        akw = _atom_keywords(atom)
        shared = sorted(akw & scn_kw)[:5]
        impacts.append(ScenarioEvidenceImpact(
            scenario_name=scenario_name,
            evidence_id=atom.evidence_id,
            source_slug=atom.source_slug,
            source_location=atom.source_location,
            claim=atom.claim,
            claim_kind=kind,
            direction=direction,
            likelihood_ratio=None,
            strength=atom.confidence,
            reliability=_reliability(kind, atom, policy),
            freshness=atom.freshness if atom.freshness is not None else policy.default_freshness,
            independence_weight=1.0 / cluster_sizes[cid],
            evidence_cluster_id=cid,
            rationale=f"{kind} routed to '{scenario_name}' on shared terms {shared}",
        ))
    for_count = sum(1 for i in impacts if i.direction == "increase")
    against = sum(1 for i in impacts if i.direction == "decrease")
    contra = sum(1 for i in impacts if i.direction == "contradictory")
    weighted = [i.strength * i.reliability * i.freshness * i.independence_weight for i in impacts]
    contra_share = (contra / len(impacts)) if impacts else 0.0
    confidence = (sum(weighted) / len(weighted)) if weighted else 0.0
    confidence = max(0.0, min(1.0, confidence * (1.0 - 0.5 * contra_share)))
    return ScenarioEvidenceMap(
        scenario_name=scenario_name,
        impacts=impacts,
        evidence_for_count=for_count,
        evidence_against_count=against,
        contradiction_count=contra,
        cluster_count=len(cluster_sizes),
        mapping_confidence=confidence,
        warnings=warnings,
    )


# ── Q4 PART-2c: deterministic posterior update ────────────────────────────────

@dataclass(frozen=True)
class ProbabilityUpdatePolicy:
    """Conservative knobs for the evidence→posterior update. The posterior is an AUDIT
    artifact only — pricing still reads Scenario.p_s, so the golden master is untouched."""
    eps: float = 1e-9
    max_log_tilt: float = 0.5            # LR = exp(max_log_tilt * strength) when LR not supplied
    max_posterior_move: float = 0.25     # max |posterior_s - prior_s| after the tilt
    single_source_quality_cap: float = 0.50
    single_cluster_quality_cap: float = 0.60
    contradiction_penalty: float = 0.50
    min_probability_quality: float = 0.0
    default_prior_quality: float = 0.50
    require_sum_to_one_tolerance: float = 1e-6
    no_evidence_quality_cap: float = 0.45
    full_clusters: int = 3               # independent clusters at which the cluster factor saturates

# increase pushes the state up, decrease down; neutral and contradictory carry NO directional
# tilt (contradictory only penalises quality) — the conservative choice.
_SIGN = {"increase": 1.0, "decrease": -1.0, "neutral": 0.0, "contradictory": 0.0}


def _all_impacts(maps: list[ScenarioEvidenceMap]) -> list[ScenarioEvidenceImpact]:
    return [i for m in maps for i in m.impacts]


def _softmax(scores: list[float]) -> list[float]:
    m = max(scores)
    ex = [math.exp(s - m) for s in scores]
    t = sum(ex)
    return [e / t for e in ex]


def _normalize_maps(scenarios: list[Scenario],
                    evidence_maps: Optional[list[ScenarioEvidenceMap]]) -> list[ScenarioEvidenceMap]:
    """One map per scenario, in scenario order; missing scenarios get an empty map."""
    by = {m.scenario_name: m for m in (evidence_maps or [])}
    out = []
    for s in scenarios:
        out.append(by.get(s.name) or ScenarioEvidenceMap(
            scenario_name=s.name, impacts=[], evidence_for_count=0, evidence_against_count=0,
            contradiction_count=0, cluster_count=0, mapping_confidence=0.0))
    return out


def _n_sources(impacts) -> int:
    return len({i.source_slug for i in impacts if i.source_slug})


def _n_clusters(impacts) -> int:
    return len({i.evidence_cluster_id for i in impacts if i.evidence_cluster_id})


def compute_probability_quality(scenarios, evidence_maps, policy=None) -> float:
    """probability_quality from reliability/freshness/mapping-confidence, reduced by
    contradictions and CAPPED for single-source / single-cluster evidence (PART 2 rules)."""
    policy = policy or ProbabilityUpdatePolicy()
    maps = _normalize_maps(scenarios, evidence_maps)
    impacts = _all_impacts(maps)
    if not impacts:
        return min(policy.no_evidence_quality_cap, policy.default_prior_quality)
    rel = sum(i.reliability for i in impacts) / len(impacts)
    fresh = sum(i.freshness for i in impacts) / len(impacts)
    nonempty = [m for m in maps if m.impacts]
    mconf = sum(m.mapping_confidence for m in nonempty) / len(nonempty)
    contra = sum(1 for i in impacts if i.direction == "contradictory") / len(impacts)
    # diversity reward: more INDEPENDENT clusters → higher quality (saturates at full_clusters)
    cluster_factor = min(1.0, _n_clusters(impacts) / policy.full_clusters)
    q = rel * fresh * mconf * cluster_factor * (1.0 - policy.contradiction_penalty * contra)
    if _n_sources(impacts) <= 1:
        q = min(q, policy.single_source_quality_cap)
    if _n_clusters(impacts) <= 1:
        q = min(q, policy.single_cluster_quality_cap)
    return max(policy.min_probability_quality, min(1.0, q))


def _evidence_confidence(maps, policy) -> float:
    """Scalar haircut in [0,1]: how far to move toward the evidence-tilted posterior. Rewards
    reliability, freshness, mapping confidence and independent clusters; penalises single source
    and contradictions, so one cluster / one source cannot dominate."""
    impacts = _all_impacts(maps)
    if not impacts:
        return 0.0
    rel = sum(i.reliability for i in impacts) / len(impacts)
    fresh = sum(i.freshness for i in impacts) / len(impacts)
    nonempty = [m for m in maps if m.impacts]
    mconf = sum(m.mapping_confidence for m in nonempty) / len(nonempty)
    cluster_factor = min(1.0, _n_clusters(impacts) / policy.full_clusters)
    source_factor = min(1.0, _n_sources(impacts) / 2.0)        # single source → 0.5
    contra = sum(1 for i in impacts if i.direction == "contradictory") / len(impacts)
    ec = rel * fresh * mconf * cluster_factor * source_factor * (1.0 - policy.contradiction_penalty * contra)
    return max(0.0, min(1.0, ec))


def _bound_move(prior, post, move):
    """Scale the whole (post-prior) delta so no element moves more than `move`. The delta sums
    to zero (both vectors sum to 1), so scaling preserves sum-to-one without renormalising."""
    delta = [p - q for p, q in zip(post, prior)]
    mx = max((abs(d) for d in delta), default=0.0)
    if mx > move and mx > 0:
        delta = [d * move / mx for d in delta]
    return [q + d for q, d in zip(prior, delta)]


def _quality_warnings(maps, policy) -> list[str]:
    impacts = _all_impacts(maps)
    w = []
    if not impacts:
        return w
    if _n_sources(impacts) <= 1:
        w.append(f"single-source evidence — probability_quality capped at {policy.single_source_quality_cap}")
    if _n_clusters(impacts) <= 1:
        w.append(f"single-cluster evidence — probability_quality capped at {policy.single_cluster_quality_cap}")
    if any(i.direction == "contradictory" for i in impacts):
        w.append("contradictory evidence present — probability_quality reduced")
    return w


def update_probabilities_from_evidence(scenarios, evidence_maps, policy=None) -> ProbabilityUpdateAudit:
    """Convert supplied scenarios + prior p_s + ScenarioEvidenceMap[] into an audited posterior.
    Never generates scenarios, never invents p_s. Posterior is an AUDIT artifact."""
    policy = policy or ProbabilityUpdatePolicy()
    if not scenarios:
        return ProbabilityUpdateAudit(
            prior_vector=[], posterior_vector=[], scenario_names=[], evidence_maps=[],
            update_method="none", probability_quality=0.0,
            warnings=["No supplied scenarios; probability update skipped."])

    names = [s.name for s in scenarios]
    prior = [float(s.p_s) for s in scenarios]
    maps = _normalize_maps(scenarios, evidence_maps)
    impacts = _all_impacts(maps)

    if not impacts:
        return ProbabilityUpdateAudit(
            prior_vector=prior, posterior_vector=list(prior), scenario_names=names,
            evidence_maps=maps, update_method="posterior_equals_prior",
            probability_quality=min(policy.no_evidence_quality_cap, policy.default_prior_quality),
            warnings=["Probabilities supplied but not evidence-weighted."])

    scores = []
    for p, m in zip(prior, maps):
        tilt = 0.0
        for j in m.impacts:
            lr = j.likelihood_ratio if j.likelihood_ratio is not None else math.exp(policy.max_log_tilt * j.strength)
            tilt += _SIGN[j.direction] * math.log(max(lr, policy.eps)) * j.reliability * j.freshness * j.independence_weight
        scores.append(math.log(max(p, policy.eps)) + tilt)

    raw = _softmax(scores)
    ec = _evidence_confidence(maps, policy)
    post = [(1.0 - ec) * prior[i] + ec * raw[i] for i in range(len(names))]
    post = _bound_move(prior, post, policy.max_posterior_move)

    return ProbabilityUpdateAudit(
        prior_vector=prior, posterior_vector=[round(x, 12) for x in post], scenario_names=names,
        evidence_maps=maps, update_method="softmax_evidence_tilt",
        probability_quality=compute_probability_quality(scenarios, maps, policy),
        warnings=_quality_warnings(maps, policy))


def audit_hash(audit: ProbabilityUpdateAudit) -> str:
    """Stable short content hash of a ProbabilityUpdateAudit — for capture/replay provenance and
    the StrategyFamilyRec.probability_update_audit_hash field."""
    import hashlib
    import json
    blob = json.dumps(audit.model_dump(), sort_keys=True, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]
