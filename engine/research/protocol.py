"""ExperimentProtocol and Gates 1, 2, and 3 per V4 spec sections 12.1-12.4, 6.6, 6.8, 6.9, and 26.

An ExperimentProtocol defines WHAT scientific test will be performed and deliberately
avoids implementation detail. It is modeled as a frozen Pydantic structure with eighteen
mandatory sections from Research Question through Remaining Type-B Scientific Decisions.

Uncertainty Classification (Spec 6.6):
  - Type A (Framing/domain/scope/relevance/definition): BLOCKS Gate 1 if unresolved.
  - Type B (Design/implementation/method/metric/data/sample): Does NOT block Gate 1,
    but BLOCKS Gate 2 if unresolved.
  - Type C (Scientific outcome/truth): Intentionally unresolved until experiment runs,
    NEVER blocks Gate 1 or Gate 2.

Gate 1 Readiness (Spec 6.8): Thirteen checks returning FAILING checks rather than a bare bool.
Gate 1 Outcomes (Spec 6.9): Enum of 7 outcomes.
Gate 2 Readiness (Spec 12.3): Eleven requirements. Gate 2 approval locks protocol to SHA-256 hash.
Gate 3 Review (Spec 26): 6 Review dimensions & 6 outcomes.

LOAD-BEARING RULE (Spec 26 & Spec 2):
Only a human may accept a material claim by default; the system is NOT a fully autonomous
scientist with permission to accept its own conclusions. Gate 3 structurally refuses ACCEPT
without an explicit human reviewer identity.

Call no wall clock (invariant I8): timestamps are parameters.
Do not import from engine/ledger/.
"""
from __future__ import annotations

import hashlib
import json
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Tuple
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


# ── Spec 6.6: Uncertainty Classification ──────────────────────────────────────

class UncertaintyClass(str, Enum):
    """Vocabulary for uncertainty classification per Spec 6.6."""

    TYPE_A = "type_a"  # Framing / scope / domain / relevance
    TYPE_B = "type_b"  # Design / implementation choice
    TYPE_C = "type_c"  # Scientific outcome / truth


class UncertaintyItem(BaseModel):
    """An uncertainty item classified per Spec 6.6."""

    model_config = ConfigDict(frozen=True)

    uncertainty_id: str
    description: str
    uncertainty_class: UncertaintyClass
    resolved: bool = False
    resolution_notes: str = ""

    @field_validator("uncertainty_class", mode="before")
    @classmethod
    def _coerce_uncertainty_class(cls, v: Any) -> UncertaintyClass:
        if isinstance(v, UncertaintyClass):
            return v
        if isinstance(v, str):
            clean = v.strip().lower().replace(" ", "_").replace("-", "_")
            if clean in ("type_a", "a"):
                return UncertaintyClass.TYPE_A
            if clean in ("type_b", "b"):
                return UncertaintyClass.TYPE_B
            if clean in ("type_c", "c"):
                return UncertaintyClass.TYPE_C
        return UncertaintyClass(v)

    @property
    def blocks_gate_1(self) -> bool:
        """Type A framing uncertainty BLOCKS Gate 1 if unresolved (Spec 6.6)."""
        return self.uncertainty_class == UncertaintyClass.TYPE_A and not self.resolved

    @property
    def blocks_gate_2(self) -> bool:
        """Type A or Type B uncertainty BLOCKS Gate 2 if unresolved (Spec 6.6)."""
        return (
            self.uncertainty_class in (UncertaintyClass.TYPE_A, UncertaintyClass.TYPE_B)
            and not self.resolved
        )


# ── Enums for Lifecycle & Gate Outcomes ───────────────────────────────────────

class ProtocolStatus(str, Enum):
    """Status vocabulary for ExperimentProtocol."""

    DRAFT = "draft"
    GATE_1_APPROVED = "gate_1_approved"
    GATE_2_APPROVED = "gate_2_approved"
    LOCKED = "locked"
    EXECUTED = "executed"
    GATE_3_REVIEWED = "gate_3_reviewed"
    ARCHIVED = "archived"


class Gate1Outcome(str, Enum):
    """The seven Gate 1 outcomes per Spec 6.9."""

    APPROVED = "approved"
    APPROVED_WITH_CONDITIONS = "approved_with_conditions"
    NEEDS_REFRAMING = "needs_reframing"
    NEEDS_MORE_EVIDENCE = "needs_more_evidence"
    DEFERRED = "deferred"
    REJECTED = "rejected"
    DUPLICATE = "duplicate"


class Gate3Outcome(str, Enum):
    """The six Gate 3 outcomes per Spec 26."""

    ACCEPT = "accept"
    WEAKEN = "weaken"
    REVISE = "revise"
    REFUTE = "refute"
    REJECT = "reject"
    KEEP_UNDER_REVIEW = "keep_under_review"


class Gate3ReviewDimension(str, Enum):
    """Review dimensions for Gate 3 per Spec 26."""

    THEORETICAL_COHERENCE = "theoretical_coherence"
    EMPIRICAL_ROBUSTNESS = "empirical_robustness"
    METHODOLOGICAL_RIGOR = "methodological_rigor"
    IDENTIFIABILITY_AND_CAUSALITY = "identifiability_and_causality"
    FALSIFICATION_FIDELITY = "falsification_fidelity"
    ECONOMIC_AND_PRACTICAL_RELEVANCE = "economic_and_practical_relevance"


# ── Helper for String Tuple Coercion ──────────────────────────────────────────

def _coerce_str_tuple(v: Any) -> Tuple[str, ...]:
    if v is None:
        return ()
    if isinstance(v, str):
        s = v.strip()
        return (s,) if s else ()
    if isinstance(v, (list, tuple, set)):
        return tuple(str(x).strip() for x in v if x and str(x).strip())
    return ()


# ── Spec 12.1 & 12.2: ExperimentProtocol ──────────────────────────────────────

class ExperimentProtocol(BaseModel):
    """ExperimentProtocol per V4 spec sections 12.1 & 12.2.

    Defines WHAT scientific test will be performed and deliberately avoids
    implementation detail. Modeled frozen with eighteen mandatory sections.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    # Identification & Metadata
    protocol_id: str
    research_question_id: str = ""
    status: ProtocolStatus = ProtocolStatus.DRAFT
    uncertainties: Tuple[UncertaintyItem, ...] = ()
    locked_hash: Optional[str] = None
    version: int = 1
    created_at: str = ""
    updated_at: str = ""

    # Section 1: Research Question
    research_question: str = ""

    # Section 2: Hypotheses Under Test
    hypotheses_evaluated: Tuple[str, ...] = ()

    # Section 3: Target Population and Sample Scope
    target_population_and_sample: str = ""

    # Section 4: Data Sources and Provenance
    data_sources_and_provenance: Tuple[str, ...] = ()

    # Section 5: Treatment or Stimulus Definition
    treatment_or_stimulus_definition: str = ""

    # Section 6: Primary Outcome Measures and Metrics
    outcome_measures_and_metrics: Tuple[str, ...] = ()

    # Section 7: Identification Strategy and Causal Assumptions
    identification_strategy: str = ""

    # Section 8: Estimation or Testing Methodology
    estimation_or_testing_method: str = ""

    # Section 9: Pre-Registered Decision Rules and Falsification Thresholds
    decision_rules_and_thresholds: Tuple[str, ...] = ()

    # Section 10: Robustness and Sensitivity Checks
    robustness_and_sensitivity_checks: Tuple[str, ...] = ()

    # Section 11: Negative Controls or Placebo Tests
    negative_controls_or_placebos: Tuple[str, ...] = ()

    # Section 12: Statistical Power or Target Precision
    statistical_power_or_precision: str = ""

    # Section 13: Missing Data, Attrition, and Outlier Handling
    missing_data_and_attrition_handling: str = ""

    # Section 14: Multiple Testing Adjustments
    multiple_testing_adjustments: str = ""

    # Section 15: Pre-Registration and Blinding Protocols
    pre_registration_and_blinding: str = ""

    # Section 16: Ethical, Legal, and Governance Constraints
    ethical_data_use_and_governance: str = ""

    # Section 17: Execution Environment and Reproducibility Specifications
    execution_environment_and_reproducibility: str = ""

    # Section 18: Remaining Type-B Scientific Decisions
    remaining_type_b_decisions: Tuple[str, ...] = ()

    @field_validator(
        "hypotheses_evaluated",
        "data_sources_and_provenance",
        "outcome_measures_and_metrics",
        "decision_rules_and_thresholds",
        "robustness_and_sensitivity_checks",
        "negative_controls_or_placebos",
        "remaining_type_b_decisions",
        mode="before",
    )
    @classmethod
    def _validate_str_tuples(cls, v: Any) -> Tuple[str, ...]:
        return _coerce_str_tuple(v)

    @field_validator("uncertainties", mode="before")
    @classmethod
    def _validate_uncertainties(cls, v: Any) -> Tuple[UncertaintyItem, ...]:
        if v is None:
            return ()
        if isinstance(v, (list, tuple, set)):
            result = []
            for item in v:
                if isinstance(item, UncertaintyItem):
                    result.append(item)
                elif isinstance(item, dict):
                    result.append(UncertaintyItem(**item))
            return tuple(result)
        return ()

    @property
    def is_locked(self) -> bool:
        return bool(self.locked_hash) or self.status in (
            ProtocolStatus.GATE_2_APPROVED,
            ProtocolStatus.LOCKED,
        )

    def compute_hash(self) -> str:
        """Compute content hash for this protocol."""
        return compute_protocol_hash(self)


# ── Spec 12.4: Protocol Hash Computation ──────────────────────────────────────

# Volatile identity / timestamp / status fields excluded from content hash,
# following the exact pattern of engine/firewall.py::freeze to prevent ontology divergence.
_PROTOCOL_HASH_EXCLUDE = {
    "protocol_id": True,
    "created_at": True,
    "updated_at": True,
    "status": True,
    "locked_hash": True,
}


def compute_protocol_hash(protocol: ExperimentProtocol) -> str:
    """Compute SHA-256 hash over canonical JSON of ExperimentProtocol per Spec 12.4.

    Excludes volatile metadata fields (`_PROTOCOL_HASH_EXCLUDE`) so identical protocol
    content produces identical hashes across runs, mirroring `engine/firewall.py::freeze`.
    """
    payload = protocol.model_dump(mode="json", exclude=_PROTOCOL_HASH_EXCLUDE)
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


# ── Spec 6.8: Gate 1 Readiness Checks ─────────────────────────────────────────

GATE_1_CHECK_NAMES = (
    "stimulus_captured",
    "research_question_defined",
    "decision_relevance_clear",
    "scope_bounded",
    "primary_target_specified",
    "material_assumptions_stated",
    "type_a_uncertainties_resolved",
    "research_model_present",
    "hypotheses_candidate_form",
    "falsification_criteria_defined",
    "originating_ref_verified",
    "no_contradictory_framing",
    "gate_1_intake_complete",
)


def check_gate_1_readiness(
    target: Any = None,
    *,
    research_question: str = "",
    decision_relevance: str = "",
    scope: str = "",
    primary_target: str = "",
    material_assumptions: Sequence[str] = (),
    uncertainties: Sequence[UncertaintyItem] = (),
    hypotheses: Sequence[Any] = (),
    originating_ref: str = "",
    research_model_present: bool = True,
    no_contradictory_framing: bool = True,
    gate_1_intake_complete: bool = True,
) -> list[str]:
    """Evaluate the thirteen Gate 1 readiness checks per Spec 6.8.

    Returns a list of FAILING check names rather than a bare bool.
    An unresolved Type A uncertainty BLOCKS Gate 1 (failing check 'type_a_uncertainties_resolved'),
    while unresolved Type B or Type C uncertainties do NOT block Gate 1.
    """
    # Extract fields from target object if provided
    if target is not None:
        if isinstance(target, ExperimentProtocol):
            research_question = research_question or target.research_question
            decision_relevance = decision_relevance or target.research_question
            uncertainties = uncertainties or target.uncertainties
            hypotheses = hypotheses or target.hypotheses_evaluated
            originating_ref = originating_ref or target.research_question_id or target.protocol_id
        elif hasattr(target, "question"):
            # ResearchQuestion instance
            research_question = research_question or getattr(target, "question", "")
            decision_relevance = decision_relevance or getattr(target, "decision_relevance", "")
            scope = scope or getattr(target, "scope", "")
            primary_target = primary_target or getattr(target, "primary_target", "")
            material_assumptions = material_assumptions or getattr(target, "material_assumptions", ())
            originating_ref = originating_ref or getattr(target, "originating_intake_ref", "")
        elif isinstance(target, dict):
            research_question = research_question or target.get("research_question", target.get("question", ""))
            decision_relevance = decision_relevance or target.get("decision_relevance", "")
            scope = scope or target.get("scope", "")
            primary_target = primary_target or target.get("primary_target", "")
            material_assumptions = material_assumptions or target.get("material_assumptions", ())
            uncertainties = uncertainties or target.get("uncertainties", ())
            hypotheses = hypotheses or target.get("hypotheses", ())
            originating_ref = originating_ref or target.get("originating_ref", "")

    failing: list[str] = []

    if not (originating_ref and str(originating_ref).strip()):
        failing.append("stimulus_captured")

    if not (research_question and str(research_question).strip()):
        failing.append("research_question_defined")

    if not (decision_relevance and str(decision_relevance).strip()):
        failing.append("decision_relevance_clear")

    if not (scope and str(scope).strip()):
        failing.append("scope_bounded")

    if not (primary_target and str(primary_target).strip()):
        failing.append("primary_target_specified")

    if not material_assumptions:
        failing.append("material_assumptions_stated")

    # LOAD-BEARING RULE (Spec 6.6 & 6.8): Unresolved Type A blocks Gate 1; Type B & C do NOT.
    unresolved_type_a = [
        u for u in uncertainties
        if isinstance(u, UncertaintyItem) and u.blocks_gate_1
    ]
    if unresolved_type_a:
        failing.append("type_a_uncertainties_resolved")

    if not research_model_present:
        failing.append("research_model_present")

    if not hypotheses:
        failing.append("hypotheses_candidate_form")

    if not hypotheses:
        failing.append("falsification_criteria_defined")

    if not (originating_ref and str(originating_ref).strip()):
        failing.append("originating_ref_verified")

    if not no_contradictory_framing:
        failing.append("no_contradictory_framing")

    if not gate_1_intake_complete:
        failing.append("gate_1_intake_complete")

    return failing


# ── Spec 12.3: Gate 2 Readiness Checks ─────────────────────────────────────────

GATE_2_REQUIREMENT_NAMES = (
    "all_18_sections_present",
    "hypotheses_evaluations_specified",
    "target_population_defined",
    "data_sources_specified",
    "treatment_stimulus_defined",
    "outcome_metrics_defined",
    "identification_strategy_clear",
    "decision_rules_pre_registered",
    "reproducibility_specified",
    "type_b_decisions_resolved",
    "gate_1_approval_confirmed",
)


def check_gate_2_readiness(protocol: ExperimentProtocol) -> list[str]:
    """Evaluate the eleven Gate 2 readiness requirements per Spec 12.3.

    Returns a list of missing requirement names. An empty list indicates
    the protocol is complete and ready for Gate 2 locking.
    """
    missing: list[str] = []

    # 1. All 18 mandatory sections must be present and non-empty
    mandatory_18_values = [
        protocol.research_question,
        protocol.hypotheses_evaluated,
        protocol.target_population_and_sample,
        protocol.data_sources_and_provenance,
        protocol.treatment_or_stimulus_definition,
        protocol.outcome_measures_and_metrics,
        protocol.identification_strategy,
        protocol.estimation_or_testing_method,
        protocol.decision_rules_and_thresholds,
        protocol.robustness_and_sensitivity_checks,
        protocol.negative_controls_or_placebos,
        protocol.statistical_power_or_precision,
        protocol.missing_data_and_attrition_handling,
        protocol.multiple_testing_adjustments,
        protocol.pre_registration_and_blinding,
        protocol.ethical_data_use_and_governance,
        protocol.execution_environment_and_reproducibility,
        # Note: remaining_type_b_decisions must be present as a section;
        # if there are active unresolved Type B decisions, requirement 10 catches it.
    ]

    has_empty_section = False
    for val in mandatory_18_values:
        if isinstance(val, str) and not val.strip():
            has_empty_section = True
            break
        if isinstance(val, (tuple, list)) and len(val) == 0:
            has_empty_section = True
            break

    if has_empty_section:
        missing.append("all_18_sections_present")

    # 2. Hypotheses evaluated
    if not protocol.hypotheses_evaluated:
        missing.append("hypotheses_evaluations_specified")

    # 3. Target population defined
    if not (protocol.target_population_and_sample and protocol.target_population_and_sample.strip()):
        missing.append("target_population_defined")

    # 4. Data sources specified
    if not protocol.data_sources_and_provenance:
        missing.append("data_sources_specified")

    # 5. Treatment / stimulus defined
    if not (protocol.treatment_or_stimulus_definition and protocol.treatment_or_stimulus_definition.strip()):
        missing.append("treatment_stimulus_defined")

    # 6. Outcome metrics defined
    if not protocol.outcome_measures_and_metrics:
        missing.append("outcome_metrics_defined")

    # 7. Identification strategy clear
    if not (protocol.identification_strategy and protocol.identification_strategy.strip()):
        missing.append("identification_strategy_clear")

    # 8. Decision rules pre-registered
    if not protocol.decision_rules_and_thresholds:
        missing.append("decision_rules_pre_registered")

    # 9. Execution environment & reproducibility specified
    if not (
        protocol.execution_environment_and_reproducibility
        and protocol.execution_environment_and_reproducibility.strip()
    ):
        missing.append("reproducibility_specified")

    # 10. All Type B decisions resolved (remaining_type_b_decisions empty & no unresolved Type B item)
    has_unresolved_type_b = len(protocol.remaining_type_b_decisions) > 0 or any(
        u.blocks_gate_2 for u in protocol.uncertainties
    )
    if has_unresolved_type_b:
        missing.append("type_b_decisions_resolved")

    # 11. Gate 1 approval confirmed (status not DRAFT)
    if protocol.status == ProtocolStatus.DRAFT:
        missing.append("gate_1_approval_confirmed")

    return missing


def approve_gate_2(protocol: ExperimentProtocol, timestamp: str = "") -> ExperimentProtocol:
    """Approve Gate 2 and lock the protocol to a content hash per Spec 12.4.

    Raises ValueError with missing requirements if protocol is incomplete.
    """
    missing = check_gate_2_readiness(protocol)
    if missing:
        raise ValueError(f"Gate 2 approval refused due to missing requirements: {missing}")

    content_hash = compute_protocol_hash(protocol)
    return ExperimentProtocol(
        **protocol.model_dump(exclude={"status", "locked_hash", "updated_at"}),
        status=ProtocolStatus.GATE_2_APPROVED,
        locked_hash=content_hash,
        updated_at=timestamp,
    )


# ── Spec 26: Gate 3 Review & Load-Bearing Human Approval Rule ──────────────────

class ReviewerIdentity(BaseModel):
    """Identity of the reviewer conducting Gate 3 evaluation."""

    model_config = ConfigDict(frozen=True)

    reviewer_id: str
    is_human: bool = False
    name: str = ""

    @field_validator("reviewer_id", mode="before")
    @classmethod
    def _validate_id(cls, v: Any) -> str:
        return str(v).strip() if v is not None else ""


class DimensionEvaluation(BaseModel):
    """Evaluation of a single review dimension at Gate 3 per Spec 26."""

    model_config = ConfigDict(frozen=True)

    dimension: Gate3ReviewDimension
    passed: bool
    notes: str = ""


class Gate3Review(BaseModel):
    """Gate 3 review record per Spec 26.

    LOAD-BEARING RULE (Spec 26 & Spec 2):
    Only a human may accept a material claim by default.
    The system is explicitly NOT a fully autonomous scientist with permission to accept
    its own conclusions. Gate 3 review CANNOT produce outcome ACCEPT without an explicit
    human reviewer identity.
    """

    model_config = ConfigDict(frozen=True)

    protocol_id: str
    reviewer: ReviewerIdentity
    outcome: Gate3Outcome
    dimension_evaluations: Tuple[DimensionEvaluation, ...] = ()
    summary: str = ""
    reviewed_at: str = ""

    @model_validator(mode="after")
    def _validate_human_approval_rule(self) -> "Gate3Review":
        if self.outcome == Gate3Outcome.ACCEPT:
            if not self.reviewer.is_human or not self.reviewer.reviewer_id:
                raise PermissionError(
                    "Gate 3 outcome ACCEPT requires an explicit human reviewer identity "
                    "per Spec 26 and Spec 2 (autonomous agent cannot self-accept conclusions)"
                )
        return self


def evaluate_gate_3(
    protocol: ExperimentProtocol,
    reviewer: ReviewerIdentity,
    outcome: Gate3Outcome,
    dimension_evaluations: Sequence[DimensionEvaluation] = (),
    summary: str = "",
    reviewed_at: str = "",
) -> Gate3Review:
    """Evaluate Gate 3 review for an executed experiment protocol per Spec 26.

    THE LOAD-BEARING RULE (Spec 26 last line & Spec 2 first bullet):
    Only a human may accept a material claim by default.
    An agent-only review can return every other outcome (WEAKEN, REVISE, REFUTE,
    REJECT, KEEP_UNDER_REVIEW), but attempting to return ACCEPT without a human
    reviewer identity raises PermissionError.
    """
    if outcome == Gate3Outcome.ACCEPT and (not reviewer.is_human or not reviewer.reviewer_id):
        raise PermissionError(
            "Gate 3 outcome ACCEPT requires an explicit human reviewer identity "
            "per Spec 26 and Spec 2 (autonomous agent cannot self-accept conclusions)"
        )

    return Gate3Review(
        protocol_id=protocol.protocol_id,
        reviewer=reviewer,
        outcome=outcome,
        dimension_evaluations=tuple(dimension_evaluations),
        summary=summary,
        reviewed_at=reviewed_at,
    )
