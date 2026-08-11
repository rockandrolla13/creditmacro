"""Unit tests for engine/research/protocol.py per V4 spec sections 12.1-12.4, 6.6, 6.8, 6.9, and 26."""

import pytest
from pydantic import ValidationError

from engine.research.protocol import (
    DimensionEvaluation,
    ExperimentProtocol,
    Gate1Outcome,
    Gate3Outcome,
    Gate3Review,
    Gate3ReviewDimension,
    ProtocolStatus,
    ReviewerIdentity,
    UncertaintyClass,
    UncertaintyItem,
    approve_gate_2,
    check_gate_1_readiness,
    check_gate_2_readiness,
    compute_protocol_hash,
    evaluate_gate_3,
)


def _make_valid_uncertainty(
    uncertainty_id: str = "unc_001",
    uncertainty_class: UncertaintyClass = UncertaintyClass.TYPE_A,
    resolved: bool = False,
) -> UncertaintyItem:
    return UncertaintyItem(
        uncertainty_id=uncertainty_id,
        description="Sample uncertainty",
        uncertainty_class=uncertainty_class,
        resolved=resolved,
    )


def _make_complete_protocol(
    protocol_id: str = "proto_001",
    status: ProtocolStatus = ProtocolStatus.GATE_1_APPROVED,
    uncertainties: tuple[UncertaintyItem, ...] = (),
    remaining_type_b: tuple[str, ...] = (),
) -> ExperimentProtocol:
    """Helper creating a complete ExperimentProtocol with all 18 mandatory sections."""
    return ExperimentProtocol(
        protocol_id=protocol_id,
        research_question_id="rq_100",
        status=status,
        uncertainties=uncertainties,
        created_at="2026-08-11T00:00:00Z",
        updated_at="2026-08-11T00:00:00Z",
        research_question="Does US rate slope affect credit spreads?",
        hypotheses_evaluated=("If slope steepens, credit spread widens.",),
        target_population_and_sample="US IG corporate bonds 2010-2025.",
        data_sources_and_provenance=("TRACE bond trades, FRED Treasury yields",),
        treatment_or_stimulus_definition="2s10s yield curve slope change > 10bps.",
        outcome_measures_and_metrics=("OAS spread change in bps",),
        identification_strategy="Difference-in-differences around rate policy shifts.",
        estimation_or_testing_method="Panel regression with firm fixed effects.",
        decision_rules_and_thresholds=("t-stat > 2.5 on slope coefficient",),
        robustness_and_sensitivity_checks=("Subsample 2015-2020", "Exclude financials"),
        negative_controls_or_placebos=("Non-sensitive utility short-duration paper",),
        statistical_power_or_precision="Power = 0.80 for 5bp effect at alpha=0.05",
        missing_data_and_attrition_handling="Linear interpolation for gaps < 3 days; drop otherwise",
        multiple_testing_adjustments="Benjamini-Hochberg FDR at 0.05",
        pre_registration_and_blinding="Protocol pre-registered; data analyst blinded to group labels",
        ethical_data_use_and_governance="Public market data only; no PII",
        execution_environment_and_reproducibility="Python 3.12, statsmodels 0.14, seed 42",
        remaining_type_b_decisions=remaining_type_b,
    )


# ── Spec 6.6: Uncertainty Asymmetry Tests ─────────────────────────────────────

def test_unresolved_type_a_blocks_gate_1():
    """Prove that an unresolved Type A framing uncertainty blocks Gate 1."""
    unc_a_unresolved = _make_valid_uncertainty(
        uncertainty_id="unc_a",
        uncertainty_class=UncertaintyClass.TYPE_A,
        resolved=False,
    )
    assert unc_a_unresolved.blocks_gate_1 is True

    failing = check_gate_1_readiness(
        research_question="Valid question",
        decision_relevance="Valid relevance",
        scope="Valid scope",
        primary_target="Valid target",
        material_assumptions=("Assumption 1",),
        uncertainties=[unc_a_unresolved],
        hypotheses=["Hypothesis 1"],
        originating_ref="ref_001",
    )
    assert "type_a_uncertainties_resolved" in failing


def test_unresolved_type_b_does_not_block_gate_1():
    """Prove that an unresolved Type B design choice does NOT block Gate 1."""
    unc_b_unresolved = _make_valid_uncertainty(
        uncertainty_id="unc_b",
        uncertainty_class=UncertaintyClass.TYPE_B,
        resolved=False,
    )
    assert unc_b_unresolved.blocks_gate_1 is False

    failing = check_gate_1_readiness(
        research_question="Valid question",
        decision_relevance="Valid relevance",
        scope="Valid scope",
        primary_target="Valid target",
        material_assumptions=("Assumption 1",),
        uncertainties=[unc_b_unresolved],
        hypotheses=["Hypothesis 1"],
        originating_ref="ref_001",
    )
    assert "type_a_uncertainties_resolved" not in failing


def test_unresolved_type_c_never_blocks_gate_1_or_gate_2():
    """Prove that Type C scientific outcome uncertainty never blocks Gate 1 or Gate 2."""
    unc_c = _make_valid_uncertainty(
        uncertainty_id="unc_c",
        uncertainty_class=UncertaintyClass.TYPE_C,
        resolved=False,
    )
    assert unc_c.blocks_gate_1 is False
    assert unc_c.blocks_gate_2 is False

    # Gate 1 check passes type_a_uncertainties_resolved
    failing_1 = check_gate_1_readiness(
        research_question="Valid question",
        decision_relevance="Valid relevance",
        scope="Valid scope",
        primary_target="Valid target",
        material_assumptions=("Assumption 1",),
        uncertainties=[unc_c],
        hypotheses=["Hypothesis 1"],
        originating_ref="ref_001",
    )
    assert "type_a_uncertainties_resolved" not in failing_1

    # Gate 2 check passes type_b_decisions_resolved with Type C present
    protocol = _make_complete_protocol(uncertainties=(unc_c,))
    missing_2 = check_gate_2_readiness(protocol)
    assert "type_b_decisions_resolved" not in missing_2


def test_unresolved_type_b_blocks_gate_2():
    """Prove that an unresolved Type B uncertainty blocks Gate 2."""
    unc_b = _make_valid_uncertainty(
        uncertainty_id="unc_b",
        uncertainty_class=UncertaintyClass.TYPE_B,
        resolved=False,
    )
    assert unc_b.blocks_gate_2 is True

    protocol = _make_complete_protocol(uncertainties=(unc_b,))
    missing = check_gate_2_readiness(protocol)
    assert "type_b_decisions_resolved" in missing


# ── Spec 12.1 & 12.2: ExperimentProtocol & Mandatory Sections ────────────────

def test_experiment_protocol_18_sections():
    """Prove ExperimentProtocol has the 18 mandatory sections from Spec 12.2."""
    protocol = _make_complete_protocol()
    
    assert protocol.research_question != ""
    assert len(protocol.hypotheses_evaluated) > 0
    assert protocol.target_population_and_sample != ""
    assert len(protocol.data_sources_and_provenance) > 0
    assert protocol.treatment_or_stimulus_definition != ""
    assert len(protocol.outcome_measures_and_metrics) > 0
    assert protocol.identification_strategy != ""
    assert protocol.estimation_or_testing_method != ""
    assert len(protocol.decision_rules_and_thresholds) > 0
    assert len(protocol.robustness_and_sensitivity_checks) > 0
    assert len(protocol.negative_controls_or_placebos) > 0
    assert protocol.statistical_power_or_precision != ""
    assert protocol.missing_data_and_attrition_handling != ""
    assert protocol.multiple_testing_adjustments != ""
    assert protocol.pre_registration_and_blinding != ""
    assert protocol.ethical_data_use_and_governance != ""
    assert protocol.execution_environment_and_reproducibility != ""
    assert isinstance(protocol.remaining_type_b_decisions, tuple)


# ── Spec 12.3 & 12.4: Gate 2 Refusal and Hash Locking ─────────────────────────

def test_gate_2_refuses_incomplete_protocol_and_returns_missing():
    """Prove that Gate 2 refuses an incomplete protocol and returns missing requirements."""
    incomplete_protocol = ExperimentProtocol(
        protocol_id="proto_incomplete",
        status=ProtocolStatus.DRAFT,  # Draft status causes gate_1_approval_confirmed failure
        research_question="Incomplete question",
        # Leaves remaining mandatory sections empty
    )

    missing = check_gate_2_readiness(incomplete_protocol)
    assert len(missing) > 0
    assert "all_18_sections_present" in missing
    assert "gate_1_approval_confirmed" in missing

    with pytest.raises(ValueError) as exc_info:
        approve_gate_2(incomplete_protocol, timestamp="2026-08-11T00:00:00Z")
    assert "Gate 2 approval refused" in str(exc_info.value)


def test_locking_produces_stable_hash_for_identical_content():
    """Prove that protocol hash locking produces identical hashes for identical content."""
    protocol_a = _make_complete_protocol(protocol_id="proto_AAA", status=ProtocolStatus.GATE_1_APPROVED)
    protocol_b = _make_complete_protocol(protocol_id="proto_BBB", status=ProtocolStatus.GATE_1_APPROVED)

    # Identical content hashes despite different protocol_ids
    hash_a = compute_protocol_hash(protocol_a)
    hash_b = compute_protocol_hash(protocol_b)
    assert hash_a == hash_b

    # Gate 2 approval locks protocol to stable hash
    approved_a = approve_gate_2(protocol_a, timestamp="2026-08-11T12:00:00Z")
    approved_b = approve_gate_2(protocol_b, timestamp="2026-08-11T14:00:00Z")

    assert approved_a.status == ProtocolStatus.GATE_2_APPROVED
    assert approved_b.status == ProtocolStatus.GATE_2_APPROVED
    assert approved_a.locked_hash == hash_a
    assert approved_b.locked_hash == hash_b
    assert approved_a.locked_hash == approved_b.locked_hash


# ── Spec 26 & Spec 2: Gate 3 Review & Load-Bearing Human Approval Rule ────────

def test_gate_3_cannot_return_accept_without_human_reviewer():
    """THE LOAD-BEARING RULE: Gate 3 CANNOT return ACCEPT without a human reviewer."""
    protocol = _make_complete_protocol()
    agent_reviewer = ReviewerIdentity(reviewer_id="agent:gpt4_evaluator", is_human=False, name="Agent Evaluator")

    # Agent reviewer attempting ACCEPT must raise PermissionError
    with pytest.raises(PermissionError) as exc_info:
        evaluate_gate_3(
            protocol=protocol,
            reviewer=agent_reviewer,
            outcome=Gate3Outcome.ACCEPT,
            summary="Autonomous acceptance attempt",
        )
    assert "ACCEPT requires an explicit human reviewer identity" in str(exc_info.value)

    # Direct Gate3Review construction with ACCEPT & agent reviewer also fails
    with pytest.raises(PermissionError):
        Gate3Review(
            protocol_id=protocol.protocol_id,
            reviewer=agent_reviewer,
            outcome=Gate3Outcome.ACCEPT,
        )


def test_gate_3_agent_reviewer_can_return_non_accept_outcomes():
    """Prove that an agent reviewer CAN return any Gate 3 outcome other than ACCEPT."""
    protocol = _make_complete_protocol()
    agent_reviewer = ReviewerIdentity(reviewer_id="agent:gpt4_evaluator", is_human=False)

    non_accept_outcomes = [
        Gate3Outcome.WEAKEN,
        Gate3Outcome.REVISE,
        Gate3Outcome.REFUTE,
        Gate3Outcome.REJECT,
        Gate3Outcome.KEEP_UNDER_REVIEW,
    ]

    for outcome in non_accept_outcomes:
        review = evaluate_gate_3(
            protocol=protocol,
            reviewer=agent_reviewer,
            outcome=outcome,
            summary=f"Agent review returning {outcome.value}",
        )
        assert review.outcome == outcome
        assert review.reviewer.is_human is False


def test_gate_3_human_reviewer_can_return_accept():
    """Prove that a human reviewer CAN return ACCEPT at Gate 3."""
    protocol = _make_complete_protocol()
    human_reviewer = ReviewerIdentity(
        reviewer_id="human:analyst_42",
        is_human=True,
        name="Lead Research Analyst",
    )

    review = evaluate_gate_3(
        protocol=protocol,
        reviewer=human_reviewer,
        outcome=Gate3Outcome.ACCEPT,
        dimension_evaluations=(
            DimensionEvaluation(dimension=Gate3ReviewDimension.THEORETICAL_COHERENCE, passed=True),
            DimensionEvaluation(dimension=Gate3ReviewDimension.EMPIRICAL_ROBUSTNESS, passed=True),
        ),
        summary="Human PM approved thesis findings after review.",
    )

    assert review.outcome == Gate3Outcome.ACCEPT
    assert review.reviewer.is_human is True
    assert review.reviewer.reviewer_id == "human:analyst_42"
