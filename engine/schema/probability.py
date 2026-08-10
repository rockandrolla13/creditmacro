"""Q4 — scenario probability justification: provenance, evidence, confidence, audit trail."""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

ProbabilitySource = Literal[
    "PM_assumption", "model_output", "evidence_weighted", "historical_base_rate", "unknown",
]
EvidenceDirection = Literal["increase", "decrease", "neutral", "contradictory"]


class ProbabilityEvidenceRef(BaseModel):
    """One piece of evidence bearing on one scenario's probability."""
    evidence_id: Optional[str] = None
    source_slug: Optional[str] = None
    source_location: Optional[str] = None
    claim: str
    direction: EvidenceDirection
    scenario_impacted: str
    strength: float = Field(ge=0.0, le=1.0)
    reliability: float = Field(ge=0.0, le=1.0)
    freshness: float = Field(ge=0.0, le=1.0)
    rationale: str


class ScenarioProbabilityJustification(BaseModel):
    """Provenance + evidence + confidence for ONE scenario's p_s (audit-only: posterior==prior)."""
    scenario_name: str
    prior_probability: float = Field(ge=0.0, le=1.0)
    prior_source: ProbabilitySource
    posterior_probability: float = Field(ge=0.0, le=1.0)
    posterior_source: ProbabilitySource
    evidence_for: list[ProbabilityEvidenceRef] = []
    evidence_against: list[ProbabilityEvidenceRef] = []
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_cap_reason: Optional[str] = None
    rationale: str
    unresolved_questions: list[str] = []


class ProbabilitySetJustification(BaseModel):
    """Set-level roll-up. effective_probability_vector is the posterior (== supplied p_s when
    no evidence). It is an AUDIT artifact — pricing keeps reading Scenario.p_s."""
    scenario_probabilities: list[ScenarioProbabilityJustification]
    sums_to_one: bool
    probability_quality: float = Field(ge=0.0, le=1.0)
    probability_source_summary: str
    effective_probability_vector: list[float]
    warnings: list[str] = []
    # Q4 PART-2c: the deterministic evidence→posterior audit (None on the legacy/no-evidence path).
    update_audit: Optional["ProbabilityUpdateAudit"] = None


class ProbabilityEvidenceBundle(BaseModel):
    """Supplied (never generated) evidence input to justify_probabilities: per-scenario
    evidence refs + optional per-scenario prior-source labels."""
    evidence_by_scenario: dict[str, list[ProbabilityEvidenceRef]] = {}
    prior_sources: dict[str, ProbabilitySource] = {}


# ── Q4 evidence-to-posterior bridge (PART 1: schema) ──────────────────────────
# A richer, source-backed evidence-atom layer that feeds a deterministic posterior update.
# These models are SHAPE + invariants only; the update MATH lives in the engine (PART 2).

# Same four values as EvidenceDirection — aliased so the bridge layer reads in its own terms
# while keeping a single source of truth.
EvidenceImpactDirection = EvidenceDirection

EvidenceClaimKind = Literal[
    "source_fact", "source_forecast", "source_opinion",
    "agent_synthesis", "PM_assumption", "model_output",
]

ProbabilityUpdateMethod = Literal[
    "none", "posterior_equals_prior", "log_likelihood_ratio", "softmax_evidence_tilt",
]


class EvidenceAtom(BaseModel):
    """A source-backed evidence atom — the (unmapped) INPUT to the evidence→scenario bridge.
    Distinct from ScenarioEvidenceImpact, which is an atom already bound to one scenario.
    `claim_kind` / `direction` may be None: the mapper classifies the kind and defaults the
    direction to 'increase' (corroborates the state it maps to) when they are absent.

    **Frozen.** `PLAN-authoritative-harness.md` §0 already assumes it is, and its guarantees
    depend on it: G1's grounding verdict is "never author-set" and G4 caps the model's own
    confidence rather than trusting it. Both are unenforceable on a mutable model — anything
    downstream could raise `confidence` or stamp a verdict the harness refused. Construct a
    changed atom with `model_copy(update=...)`; do not mutate in place."""
    model_config = ConfigDict(frozen=True)

    evidence_id: Optional[str] = None
    source_slug: Optional[str] = None
    source_location: Optional[str] = None
    claim: str
    claim_kind: Optional[EvidenceClaimKind] = None
    claim_type: Optional[str] = None
    direction: Optional[EvidenceImpactDirection] = None
    entities: list[str] = []
    concepts: list[str] = []
    themes: list[str] = []
    market_variables: list[str] = []
    numbers: list[float] = []
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    freshness: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    evidence_cluster_id: Optional[str] = None
    agent_use: Optional[str] = None      # provenance note (how the agent may use the fact); carried, not used in mapping
    is_synthesis: bool = False

    @classmethod
    def from_record(cls, rec: dict) -> "EvidenceAtom":
        """Adapt a materialized atom dict (evidence_atoms.jsonl / page frontmatter) into the
        engine input. Drops a date-string `freshness` (recency is unknown without a reference
        date) and keeps only known fields; the mapper supplies a default freshness."""
        d = dict(rec)
        if isinstance(d.get("freshness"), str):
            d["freshness"] = None
        return cls.model_validate({k: v for k, v in d.items() if k in cls.model_fields})


class ScenarioEvidenceImpact(BaseModel):
    """One source-backed evidence atom's bearing on ONE scenario's probability. Supplied, never
    invented. `likelihood_ratio` is optional; when present it must be > 0 (a ratio, not a prob)."""
    scenario_name: str
    evidence_id: Optional[str] = None
    source_slug: Optional[str] = None
    source_location: Optional[str] = None
    claim: str
    claim_kind: EvidenceClaimKind
    direction: EvidenceImpactDirection
    likelihood_ratio: Optional[float] = None
    strength: float = Field(ge=0.0, le=1.0)
    reliability: float = Field(ge=0.0, le=1.0)
    freshness: float = Field(ge=0.0, le=1.0)
    independence_weight: float = Field(ge=0.0, le=1.0)
    evidence_cluster_id: Optional[str] = None
    rationale: str

    @model_validator(mode="after")
    def _likelihood_ratio_positive(self) -> "ScenarioEvidenceImpact":
        if self.likelihood_ratio is not None and self.likelihood_ratio <= 0.0:
            raise ValueError("likelihood_ratio must be > 0 when provided")
        return self


class ScenarioEvidenceMap(BaseModel):
    """All evidence impacts bearing on ONE scenario plus summary counts. The contradiction and
    cluster counts are DEFINITIONAL — validated against `impacts` so a map cannot overstate the
    evidence it summarises. for/against counts are bounded by the impact count (their exact
    classification is the engine's, PART 2)."""
    scenario_name: str
    impacts: list[ScenarioEvidenceImpact] = []
    evidence_for_count: int = Field(ge=0)
    evidence_against_count: int = Field(ge=0)
    contradiction_count: int = Field(ge=0)
    cluster_count: int = Field(ge=0)
    mapping_confidence: float = Field(ge=0.0, le=1.0)
    warnings: list[str] = []

    @model_validator(mode="after")
    def _counts_consistent(self) -> "ScenarioEvidenceMap":
        n = len(self.impacts)
        for label, c in (("evidence_for_count", self.evidence_for_count),
                         ("evidence_against_count", self.evidence_against_count),
                         ("contradiction_count", self.contradiction_count),
                         ("cluster_count", self.cluster_count)):
            if c > n:
                raise ValueError(f"{label}={c} exceeds impact count {n}")
        actual_contra = sum(1 for i in self.impacts if i.direction == "contradictory")
        if self.contradiction_count != actual_contra:
            raise ValueError(
                f"contradiction_count={self.contradiction_count} != "
                f"{actual_contra} contradictory impacts")
        actual_clusters = len({i.evidence_cluster_id for i in self.impacts if i.evidence_cluster_id})
        if self.cluster_count != actual_clusters:
            raise ValueError(
                f"cluster_count={self.cluster_count} != {actual_clusters} distinct clusters")
        return self


class ProbabilityUpdateAudit(BaseModel):
    """Deterministic audit of a scenario-probability update (Q4 bridge output). The posterior
    vector is an AUDIT artifact — pricing keeps reading Scenario.p_s. Never invents probabilities
    and never generates scenarios. Enforces the bridge's structural + activation invariants:
      R1  an evidence-weighted method requires >= 1 ScenarioEvidenceImpact.
      R2  no scenarios -> update_method == 'none', empty vectors.
      R3  scenarios but no impacts -> 'posterior_equals_prior' with posterior == prior."""
    prior_vector: list[float] = []
    posterior_vector: list[float] = []
    scenario_names: list[str] = []
    evidence_maps: list[ScenarioEvidenceMap] = []
    update_method: ProbabilityUpdateMethod
    probability_quality: float = Field(ge=0.0, le=1.0)
    warnings: list[str] = []

    @model_validator(mode="after")
    def _structural_and_activation_rules(self) -> "ProbabilityUpdateAudit":
        n = len(self.scenario_names)
        if len(self.prior_vector) != n or len(self.posterior_vector) != n:
            raise ValueError("prior/posterior vector length must match scenario_names")
        if len(self.evidence_maps) != n:
            raise ValueError("exactly one evidence map per scenario is required")
        known = set(self.scenario_names)
        for m in self.evidence_maps:
            if m.scenario_name not in known:
                raise ValueError(
                    f"evidence map scenario '{m.scenario_name}' not in scenario_names")
        total_impacts = sum(len(m.impacts) for m in self.evidence_maps)

        if n == 0:                                            # R2
            if self.update_method != "none":
                raise ValueError("no scenarios supplied: update_method must be 'none'")
            return self
        if self.update_method == "none":
            raise ValueError("update_method 'none' is only valid with no scenarios")
        if self.update_method in ("log_likelihood_ratio", "softmax_evidence_tilt") \
                and total_impacts == 0:                       # R1
            raise ValueError(f"{self.update_method} requires >= 1 ScenarioEvidenceImpact")
        if total_impacts == 0 and self.update_method != "posterior_equals_prior":  # R3
            raise ValueError("no evidence impacts: update_method must be 'posterior_equals_prior'")
        if self.update_method == "posterior_equals_prior":
            if any(abs(a - b) > 1e-9 for a, b in zip(self.prior_vector, self.posterior_vector)):
                raise ValueError("posterior_equals_prior requires posterior == prior")
        return self


# Resolve the forward reference now that ProbabilityUpdateAudit is defined.
ProbabilitySetJustification.model_rebuild()
