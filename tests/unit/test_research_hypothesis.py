"""Tests for engine/research/hypothesis.py per V4 spec sections 11.1 through 11.4."""
import pytest
from pydantic import ValidationError

from engine.research.hypothesis import (
    CandidateHypothesis,
    HypothesisDerivation,
    HypothesisStatus,
    HypothesisType,
    PrioritizationScores,
    check_activation,
    check_hypothesis_activation,
    prioritize_hypotheses,
)


def _make_valid_derivation() -> HypothesisDerivation:
    return HypothesisDerivation(
        research_model_edge_ids=("edge_001",),
        subquestion_ids=("subq_001",),
    )


def _make_valid_hypothesis(
    hypothesis_id: str = "hyp_001",
    status: HypothesisStatus = HypothesisStatus.CANDIDATE,
    hypothesis_type: HypothesisType = HypothesisType.PRIMARY,
    falsification_criteria: tuple[str, ...] = ("Spread closes < 5bps",),
) -> CandidateHypothesis:
    return CandidateHypothesis(
        hypothesis_id=hypothesis_id,
        research_question_id="rq_001",
        derived_from=_make_valid_derivation(),
        statement="If X increases, Y steepens.",
        mechanism="Demand imbalance forces curve adjustment.",
        predicted_direction="+",
        falsification_criteria=falsification_criteria,
        status=status,
        hypothesis_type=hypothesis_type,
    )


def test_no_falsification_criteria_rejected():
    """Prove that a CandidateHypothesis with empty falsification_criteria is rejected at construction."""
    # Empty tuple
    with pytest.raises((ValidationError, ValueError)):
        CandidateHypothesis(
            hypothesis_id="hyp_no_falsifier",
            research_question_id="rq_001",
            derived_from=_make_valid_derivation(),
            statement="Valid statement",
            mechanism="Valid mechanism",
            predicted_direction="+",
            falsification_criteria=(),
        )

    # Empty list
    with pytest.raises((ValidationError, ValueError)):
        CandidateHypothesis(
            hypothesis_id="hyp_no_falsifier_2",
            research_question_id="rq_001",
            derived_from=_make_valid_derivation(),
            statement="Valid statement",
            mechanism="Valid mechanism",
            predicted_direction="+",
            falsification_criteria=[],
        )

    # Whitespace-only strings
    with pytest.raises((ValidationError, ValueError)):
        CandidateHypothesis(
            hypothesis_id="hyp_no_falsifier_3",
            research_question_id="rq_001",
            derived_from=_make_valid_derivation(),
            statement="Valid statement",
            mechanism="Valid mechanism",
            predicted_direction="+",
            falsification_criteria=["   ", ""],
        )


def test_no_derivation_rejected():
    """Prove that a CandidateHypothesis with no derivation provenance is rejected at construction."""
    # Empty derivation object
    with pytest.raises((ValidationError, ValueError)):
        HypothesisDerivation(
            research_model_edge_ids=(),
            subquestion_ids=(),
        )

    # Passing invalid derivation
    with pytest.raises((ValidationError, ValueError)):
        CandidateHypothesis(
            hypothesis_id="hyp_no_derivation",
            research_question_id="rq_001",
            derived_from=HypothesisDerivation.model_construct(
                research_model_edge_ids=(),
                subquestion_ids=(),
            ),
            statement="Valid statement",
            mechanism="Valid mechanism",
            predicted_direction="+",
            falsification_criteria=("Falsifier 1",),
        )


def test_prioritization_deterministic_across_runs():
    """Prove that prioritization is a pure function and deterministic across multiple runs."""
    h1 = _make_valid_hypothesis("hyp_alpha")
    h2 = _make_valid_hypothesis("hyp_beta")
    h3 = _make_valid_hypothesis("hyp_gamma")

    scores_1 = PrioritizationScores(
        scientific_importance=0.8,
        novelty=0.5,
        decision_relevance=0.9,
        falsifiability=0.7,
        identifiability=0.6,
        data_feasibility=0.8,
        implementation_cost=0.2,
        information_gain=0.9,
        dependency_order=0.5,
        downstream_option_value=0.4,
    )

    scores_2 = PrioritizationScores(
        scientific_importance=0.9,
        novelty=0.8,
        decision_relevance=0.9,
        falsifiability=0.8,
        identifiability=0.8,
        data_feasibility=0.9,
        implementation_cost=0.1,
        information_gain=0.9,
        dependency_order=0.8,
        downstream_option_value=0.7,
    )

    scores_3 = PrioritizationScores(
        scientific_importance=0.3,
        novelty=0.2,
        decision_relevance=0.4,
        falsifiability=0.5,
        identifiability=0.4,
        data_feasibility=0.3,
        implementation_cost=0.8,
        information_gain=0.3,
        dependency_order=0.2,
        downstream_option_value=0.1,
    )

    input_items = [(h1, scores_1), (h2, scores_2), (h3, scores_3)]

    # Run 1
    run_1 = prioritize_hypotheses(input_items)
    # Run 2 (different input order to test stability)
    run_2 = prioritize_hypotheses([(h3, scores_3), (h1, scores_1), (h2, scores_2)])

    ids_1 = [p.hypothesis.hypothesis_id for p in run_1]
    ids_2 = [p.hypothesis.hypothesis_id for p in run_2]
    scores_1_list = [p.score for p in run_1]
    scores_2_list = [p.score for p in run_2]

    assert ids_1 == ids_2
    assert scores_1_list == scores_2_list
    # Highest score should be hyp_beta (scores_2)
    assert ids_1[0] == "hyp_beta"


def test_prioritization_tie_breaking():
    """Prove tie-breaking is deterministic (alphabetical by hypothesis_id)."""
    h_b = _make_valid_hypothesis("hyp_B")
    h_a = _make_valid_hypothesis("hyp_A")

    identical_scores = PrioritizationScores(scientific_importance=1.0)

    res = prioritize_hypotheses([(h_b, identical_scores), (h_a, identical_scores)])
    assert [p.hypothesis.hypothesis_id for p in res] == ["hyp_A", "hyp_B"]


def test_activation_reports_already_answered_rather_than_raising():
    """Prove that activation check reports a hypothesis already answered rather than raising an exception."""
    # Test with terminal status SUPPORTED
    h_supported = _make_valid_hypothesis("hyp_supp", status=HypothesisStatus.SUPPORTED)
    reasons_1 = check_activation(h_supported)

    assert isinstance(reasons_1, list)
    assert len(reasons_1) > 0
    assert any("already answered" in r.lower() for r in reasons_1)

    # Test with terminal status REFUTED
    h_refuted = _make_valid_hypothesis("hyp_ref", status=HypothesisStatus.REFUTED)
    reasons_2 = check_hypothesis_activation(h_refuted)
    assert len(reasons_2) > 0
    assert any("already answered" in r.lower() for r in reasons_2)

    # Test with external already-answered records
    h_cand = _make_valid_hypothesis("hyp_cand", status=HypothesisStatus.CANDIDATE)
    reasons_3 = check_activation(h_cand, already_answered_ids={"hyp_cand"})
    assert len(reasons_3) > 0
    assert any("already answered" in r.lower() for r in reasons_3)

    # Valid candidate pass check
    reasons_pass = check_activation(h_cand)
    assert reasons_pass == []


def test_spec_vocabularies_and_types():
    """Verify all status values and hypothesis types are representable."""
    for st in [
        HypothesisStatus.CANDIDATE,
        HypothesisStatus.ACTIVE,
        HypothesisStatus.SUPPORTED,
        HypothesisStatus.WEAKENED,
        HypothesisStatus.REFUTED,
        HypothesisStatus.SUPERSEDED,
    ]:
        h = _make_valid_hypothesis(status=st)
        assert h.status == st

    for ht in [
        HypothesisType.PRIMARY,
        HypothesisType.COMPETING,
        HypothesisType.NULL,
        HypothesisType.MECHANISM,
        HypothesisType.BOUNDARY_CONDITION,
        HypothesisType.ECONOMIC_VALIDATION,
    ]:
        h = _make_valid_hypothesis(hypothesis_type=ht)
        assert h.hypothesis_type == ht


def test_frozen_model_immutability():
    """Verify CandidateHypothesis is frozen and cannot be mutated."""
    h = _make_valid_hypothesis()
    with pytest.raises(ValidationError):
        h.status = HypothesisStatus.ACTIVE  # type: ignore
