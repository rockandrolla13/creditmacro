"""Q4 — scenario probability justification: provenance, evidence, confidence, audit trail."""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

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


class ProbabilityEvidenceBundle(BaseModel):
    """Supplied (never generated) evidence input to justify_probabilities: per-scenario
    evidence refs + optional per-scenario prior-source labels."""
    evidence_by_scenario: dict[str, list[ProbabilityEvidenceRef]] = {}
    prior_sources: dict[str, ProbabilitySource] = {}
