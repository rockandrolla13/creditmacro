"""Unit tests for ResearchQuestion, SubQuestion, and QuestionDecomposition.

Per V4 spec sections 7, 8.1 through 8.4.
"""
import pytest
from pydantic import ValidationError

from engine.research.question import (
    DependencyCycleError,
    QuestionDecomposition,
    ResearchQuestion,
    ResearchQuestionStatus,
    SubQuestion,
    SubQuestionRole,
    SubQuestionState,
)


def test_research_question_creation_and_frozen():
    """Verify ResearchQuestion fields, frozen immutability, and Gate 1 origin attributes."""
    rq = ResearchQuestion(
        research_question_id="rq_001",
        question="Will US rate hikes trigger a flattener in 10s30s curves?",
        decision_relevance="Determines positioning in duration flattener strategy.",
        scope="US Treasury yield curve 2026-2027",
        primary_target="10s30s UST yield spread",
        material_assumptions=("Fed remains hawkish", "Treasury issuance balanced"),
        originating_intake_ref="gate1_decision_101",
        status=ResearchQuestionStatus.CONFIRMED,
    )

    assert rq.research_question_id == "rq_001"
    assert rq.question == "Will US rate hikes trigger a flattener in 10s30s curves?"
    assert rq.decision_relevance == "Determines positioning in duration flattener strategy."
    assert rq.scope == "US Treasury yield curve 2026-2027"
    assert rq.primary_target == "10s30s UST yield spread"
    assert rq.material_assumptions == ("Fed remains hawkish", "Treasury issuance balanced")
    assert rq.originating_intake_ref == "gate1_decision_101"
    assert rq.originating_gate_ref == "gate1_decision_101"
    assert rq.originating_intake_gate_ref == "gate1_decision_101"
    assert rq.status == ResearchQuestionStatus.CONFIRMED

    # Immutability check
    with pytest.raises(ValidationError):
        rq.status = ResearchQuestionStatus.RESOLVED  # type: ignore


def test_subquestion_fields_and_enum_vocabularies():
    """Verify SubQuestion with exact field list from Spec 8.3 and str Enum enforcement."""
    sq = SubQuestion(
        subquestion_id="sq_001",
        research_question_id="rq_001",
        question="Is policy rate hike pass-through to front-end yields complete?",
        role=SubQuestionRole.NECESSARY_CONDITION,
        dependencies=(),
        current_state=SubQuestionState.PARTIALLY_KNOWN,
    )

    assert sq.subquestion_id == "sq_001"
    assert sq.research_question_id == "rq_001"
    assert sq.role == SubQuestionRole.NECESSARY_CONDITION
    assert sq.role.value == "necessary_condition"
    assert sq.current_state == SubQuestionState.PARTIALLY_KNOWN
    assert sq.current_state.value == "partially_known"

    # Verify all role vocabulary strings work and invalid strings fail
    valid_roles = [
        "necessary_condition",
        "mechanism",
        "intermediate_outcome",
        "endpoint",
        "boundary_condition",
        "robustness",
    ]
    for role_str in valid_roles:
        sq_role = SubQuestion(
            subquestion_id="sq_test",
            research_question_id="rq_001",
            question="Role test?",
            role=role_str,  # type: ignore
        )
        assert sq_role.role == SubQuestionRole(role_str)

    with pytest.raises(ValidationError):
        SubQuestion(
            subquestion_id="sq_bad_role",
            research_question_id="rq_001",
            question="Invalid role?",
            role="invalid_role_string",  # type: ignore
        )

    # Verify all current_state vocabulary strings work and invalid strings fail
    valid_states = ["unknown", "partially_known", "supported", "contested", "refuted", "blocked"]
    for state_str in valid_states:
        sq_state = SubQuestion(
            subquestion_id="sq_test_state",
            research_question_id="rq_001",
            question="State test?",
            role=SubQuestionRole.MECHANISM,
            current_state=state_str,  # type: ignore
        )
        assert sq_state.current_state == SubQuestionState(state_str)

    with pytest.raises(ValidationError):
        SubQuestion(
            subquestion_id="sq_bad_state",
            research_question_id="rq_001",
            question="Invalid state?",
            role=SubQuestionRole.MECHANISM,
            current_state="invalid_state_string",  # type: ignore
        )


def test_rq_decomposes_into_distinct_subquestions():
    """Requirement 1: Prove an RQ decomposes into distinct subquestions."""
    rq = ResearchQuestion(
        research_question_id="rq_100",
        question="Does AI capex lead semiconductor sector margin expansion?",
        decision_relevance="Informs long/short equity expression in tech credit and equity.",
        scope="Global semiconductor hardware supply chain 2025-2027",
        primary_target="Semiconductor gross margin expansion %",
        material_assumptions=("Hyperscaler capex guidance holds",),
        originating_intake_ref="gate1_intake_202",
    )

    sq1 = SubQuestion(
        subquestion_id="sq_101",
        research_question_id="rq_100",
        question="Are hyperscaler capex commitments legally binding?",
        role=SubQuestionRole.NECESSARY_CONDITION,
        current_state=SubQuestionState.SUPPORTED,
    )
    sq2 = SubQuestion(
        subquestion_id="sq_102",
        research_question_id="rq_100",
        question="Does high-bandwidth memory supply lag GPU order growth?",
        role=SubQuestionRole.MECHANISM,
        dependencies=("sq_101",),
        current_state=SubQuestionState.PARTIALLY_KNOWN,
    )
    sq3 = SubQuestion(
        subquestion_id="sq_103",
        research_question_id="rq_100",
        question="Do wafer pricing increases pass through to hyperscalers?",
        role=SubQuestionRole.ENDPOINT,
        dependencies=("sq_102",),
        current_state=SubQuestionState.UNKNOWN,
    )

    decomp = QuestionDecomposition(
        research_question=rq,
        subquestions=(sq1, sq2, sq3),
    )

    assert decomp.research_question_id == "rq_100"
    assert len(decomp.subquestions) == 3
    assert set(sq.subquestion_id for sq in decomp.subquestions) == {"sq_101", "sq_102", "sq_103"}
    assert all(sq.research_question_id == "rq_100" for sq in decomp.subquestions)


def test_dependencies_represented_and_topologically_ordered():
    """Requirement 2: Prove dependencies are represented and topologically ordered."""
    sq_a = SubQuestion(
        subquestion_id="sq_a",
        research_question_id="rq_001",
        question="Root prerequisite question?",
        role=SubQuestionRole.NECESSARY_CONDITION,
        dependencies=(),
    )
    sq_b = SubQuestion(
        subquestion_id="sq_b",
        research_question_id="rq_001",
        question="Intermediate mechanism question?",
        role=SubQuestionRole.MECHANISM,
        dependencies=("sq_a",),
    )
    sq_c = SubQuestion(
        subquestion_id="sq_c",
        research_question_id="rq_001",
        question="Decision endpoint question?",
        role=SubQuestionRole.ENDPOINT,
        dependencies=("sq_b",),
    )

    # Supply subquestions out of topological order
    decomp = QuestionDecomposition(
        subquestions=(sq_c, sq_a, sq_b),
    )

    # Check dependency edge set
    assert ("sq_a", "sq_b") in decomp.dependency_edges
    assert ("sq_b", "sq_c") in decomp.dependency_edges

    # Check topological order
    ordered = decomp.get_subquestions_in_dependency_order()
    ordered_ids = [sq.subquestion_id for sq in ordered]
    assert ordered_ids == ["sq_a", "sq_b", "sq_c"]

    # Verify upstream navigation methods
    assert decomp.is_upstream("sq_a", "sq_b") is True
    assert decomp.is_upstream("sq_a", "sq_c") is True
    assert decomp.is_upstream("sq_c", "sq_a") is False

    upstream_c = [sq.subquestion_id for sq in decomp.get_upstream_subquestions("sq_c")]
    assert upstream_c == ["sq_a", "sq_b"]

    downstream_a = [sq.subquestion_id for sq in decomp.get_downstream_subquestions("sq_a")]
    assert downstream_a == ["sq_b", "sq_c"]


def test_dependency_cycle_raises():
    """Requirement 3: Prove a dependency cycle raises an exception (DependencyCycleError / ValueError)."""
    sq_1 = SubQuestion(
        subquestion_id="sq_cycle_1",
        research_question_id="rq_001",
        question="Question 1 in loop?",
        role=SubQuestionRole.MECHANISM,
        dependencies=("sq_cycle_2",),
    )
    sq_2 = SubQuestion(
        subquestion_id="sq_cycle_2",
        research_question_id="rq_001",
        question="Question 2 in loop?",
        role=SubQuestionRole.MECHANISM,
        dependencies=("sq_cycle_1",),
    )

    decomp = QuestionDecomposition(
        subquestions=(sq_1, sq_2),
    )

    # Must raise DependencyCycleError (which inherits from ValueError)
    with pytest.raises(ValueError) as excinfo:
        decomp.get_subquestions_in_dependency_order()

    assert "Dependency cycle detected" in str(excinfo.value)

    # Test multi-node cycle (1 -> 2 -> 3 -> 1)
    sq_a = SubQuestion(
        subquestion_id="sq_3a",
        research_question_id="rq_001",
        question="Node A",
        role=SubQuestionRole.MECHANISM,
        dependencies=("sq_3c",),
    )
    sq_b = SubQuestion(
        subquestion_id="sq_3b",
        research_question_id="rq_001",
        question="Node B",
        role=SubQuestionRole.MECHANISM,
        dependencies=("sq_3a",),
    )
    sq_c = SubQuestion(
        subquestion_id="sq_3c",
        research_question_id="rq_001",
        question="Node C",
        role=SubQuestionRole.MECHANISM,
        dependencies=("sq_3b",),
    )

    decomp3 = QuestionDecomposition(subquestions=(sq_a, sq_b, sq_c))
    with pytest.raises(DependencyCycleError):
        decomp3.get_subquestions_in_dependency_order()


def test_endpoint_role_distinguishable_from_mechanism_role():
    """Requirement 4: Prove an endpoint role is distinguishable from a mechanism role (Spec 8.4)."""
    sq_necessary = SubQuestion(
        subquestion_id="sq_nec",
        research_question_id="rq_001",
        question="Is credit availability constrained?",
        role=SubQuestionRole.NECESSARY_CONDITION,
    )
    sq_mech1 = SubQuestion(
        subquestion_id="sq_m1",
        research_question_id="rq_001",
        question="Does bank lending channel contract?",
        role=SubQuestionRole.MECHANISM,
        dependencies=("sq_nec",),
    )
    sq_mech2 = SubQuestion(
        subquestion_id="sq_m2",
        research_question_id="rq_001",
        question="Does intermediate spreads widen?",
        role=SubQuestionRole.INTERMEDIATE_OUTCOME,
        dependencies=("sq_m1",),
    )
    sq_endpoint = SubQuestion(
        subquestion_id="sq_end",
        research_question_id="rq_001",
        question="Will high-yield default rates breach 5%?",
        role=SubQuestionRole.ENDPOINT,
        dependencies=("sq_m2",),
    )

    decomp = QuestionDecomposition(
        subquestions=(sq_necessary, sq_mech1, sq_mech2, sq_endpoint)
    )

    # 1. Enums are strictly distinct
    assert SubQuestionRole.ENDPOINT != SubQuestionRole.MECHANISM
    assert SubQuestionRole.ENDPOINT.value == "endpoint"
    assert SubQuestionRole.MECHANISM.value == "mechanism"

    # 2. Spec 8.4 structure exposes intermediate mechanisms vs direct decision endpoints
    mechanisms = decomp.intermediate_mechanisms
    endpoints = decomp.endpoint_subquestions
    direct_decision = decomp.direct_decision_subquestions

    assert len(mechanisms) == 2
    assert set(sq.subquestion_id for sq in mechanisms) == {"sq_m1", "sq_m2"}

    assert len(endpoints) == 1
    assert endpoints[0].subquestion_id == "sq_end"
    assert direct_decision == endpoints

    # 3. Filtering by role
    endpoint_role_sqs = decomp.subquestions_by_role(SubQuestionRole.ENDPOINT)
    assert endpoint_role_sqs == (sq_endpoint,)

    mechanism_role_sqs = decomp.subquestions_by_role(SubQuestionRole.MECHANISM)
    assert mechanism_role_sqs == (sq_mech1,)

    # 4. Upstream roots
    logically_upstream = decomp.logically_upstream_subquestions
    assert any(sq.subquestion_id == "sq_nec" for sq in logically_upstream)
