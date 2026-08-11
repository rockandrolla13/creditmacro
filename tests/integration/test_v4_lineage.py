"""Integration proof for V4 spec section 40 lineage recovery."""
from __future__ import annotations

from datetime import datetime, timezone
import json

import pytest

from engine.research.hypothesis import (
    CandidateHypothesis,
    HypothesisDerivation,
    HypothesisStatus,
    HypothesisType,
)
from engine.research.knowledge import KnowledgeState, KnowledgeStatus, SubQuestionKnowledge
from engine.research.lineage import (
    MissingModelEdgeLineageError,
    ResearchLineageContext,
    trace_hypothesis_lineage,
)
from engine.research.model import ElementStatus, ModelEdge, ModelNode, ModelType, ResearchModel
from engine.research.protocol import ExperimentProtocol, ProtocolStatus, approve_gate_2
from engine.research.question import (
    QuestionDecomposition,
    ResearchQuestion,
    ResearchQuestionStatus,
    SubQuestion,
    SubQuestionRole,
    SubQuestionState,
)
from engine.research.stimulus import (
    Capture,
    Content,
    Origin,
    OriginType,
    ResearchStimulus,
)


def _ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


@pytest.fixture
def rs_041_lineage_fixture() -> tuple[
    ResearchLineageContext,
    dict[str, CandidateHypothesis],
]:
    stimulus = ResearchStimulus(
        stimulus_id="RS-041",
        origin=Origin(
            type=OriginType.RESEARCHER,
            actor_id="andreas",
            source_ref="meeting-note:issuer-selection-brainstorm",
        ),
        content=Content(
            raw=(
                "Andreas asked whether issuer-first selection beats sector-first selection "
                "when credit dispersion widens."
            ),
            summary="Researcher-originated question on issuer-first selection in credit.",
        ),
        occurred_at=_ts("2026-03-14T09:30:00Z"),
        captured_by=Capture(
            actor_type="assistant",
            actor_id="research-assistant-v4",
            timestamp=_ts("2026-03-14T09:32:00Z"),
        ),
        context_refs=["desk:credit-research", "notebook:issuer-selection"],
        evidence_refs=["memo:desk-observation-2026-03-14"],
        status="captured",
    )

    intake_ref = "intake:RS-041|gate1:approved"

    research_question = ResearchQuestion(
        research_question_id="RQ-018",
        question=(
            "When dispersion in credit broadens, does issuer-first selection produce "
            "more robust alpha than sector-first selection?"
        ),
        decision_relevance="Determines how the team allocates research effort in IG credit.",
        scope="USD investment-grade primary and secondary issuer selection.",
        primary_target="relative issuer selection hit rate",
        material_assumptions=(
            "Dispersion is observable at the issuer level.",
            "Sector regime effects do not fully dominate issuer effects.",
        ),
        originating_intake_ref=intake_ref,
        status=ResearchQuestionStatus.CONFIRMED,
    )

    sq_1 = SubQuestion(
        subquestion_id="SQ-018-1",
        research_question_id="RQ-018",
        question="Does cross-issuer dispersion rise before sector baskets re-rank?",
        role=SubQuestionRole.NECESSARY_CONDITION,
        current_state=SubQuestionState.PARTIALLY_KNOWN,
    )
    sq_2 = SubQuestion(
        subquestion_id="SQ-018-2",
        research_question_id="RQ-018",
        question="Does earlier issuer triage improve subsequent issuer hit rate?",
        role=SubQuestionRole.MECHANISM,
        dependencies=("SQ-018-1",),
        current_state=SubQuestionState.UNKNOWN,
    )
    sq_3 = SubQuestion(
        subquestion_id="SQ-018-3",
        research_question_id="RQ-018",
        question="Does issuer-first selection outperform sector-first selection on decision utility?",
        role=SubQuestionRole.ENDPOINT,
        dependencies=("SQ-018-2",),
        current_state=SubQuestionState.UNKNOWN,
    )

    decomposition = QuestionDecomposition(
        research_question=research_question,
        subquestions=(sq_1, sq_2, sq_3),
    )

    knowledge_state = KnowledgeState(
        research_question_id="RQ-018",
        subquestion_states=(
            SubQuestionKnowledge(
                subquestion_id="SQ-018-1",
                question=sq_1.question,
                state=KnowledgeStatus.PARTIALLY_KNOWN,
                evidence_breadth=2,
                last_updated="2026-03-12",
            ),
            SubQuestionKnowledge(
                subquestion_id="SQ-018-2",
                question=sq_2.question,
                state=KnowledgeStatus.UNKNOWN,
                evidence_breadth=0,
            ),
            SubQuestionKnowledge(
                subquestion_id="SQ-018-3",
                question=sq_3.question,
                state=KnowledgeStatus.UNKNOWN,
                evidence_breadth=0,
            ),
        ),
    )

    nodes = (
        ModelNode(node_id="dispersion", label="issuer dispersion", status=ElementStatus.RESOLVED),
        ModelNode(node_id="triage", label="issuer-first triage", status=ElementStatus.UNRESOLVED),
        ModelNode(node_id="hit_rate", label="selection hit rate", status=ElementStatus.UNRESOLVED),
    )
    edges = (
        ModelEdge(
            v_from="dispersion",
            v_to="triage",
            sign=1,
            status=ElementStatus.UNRESOLVED,
            claims=("claim:dispersion-precedes-triage",),
        ),
        ModelEdge(
            v_from="triage",
            v_to="hit_rate",
            sign=1,
            status=ElementStatus.UNRESOLVED,
            claims=("claim:triage-improves-hit-rate",),
        ),
    )
    research_model = ResearchModel(
        model_id="RM-018",
        model_type=ModelType.MECHANISM_CHAIN,
        nodes=nodes,
        edges=edges,
        description="Issuer-first selection works through earlier triage when dispersion widens.",
    )

    hypotheses = {
        "H-018-1": CandidateHypothesis(
            hypothesis_id="H-018-1",
            research_question_id="RQ-018",
            derived_from=HypothesisDerivation(
                research_model_edge_ids=(research_model.edges[0].edge_id,),
                subquestion_ids=("SQ-018-1",),
            ),
            statement="Dispersion broadens before sector baskets re-rank.",
            mechanism="Relative issuer dispersion becomes decision-relevant before sector composites move.",
            predicted_direction="positive",
            falsification_criteria=("Issuer dispersion does not lead sector basket re-ranking.",),
            status=HypothesisStatus.ACTIVE,
            hypothesis_type=HypothesisType.MECHANISM,
        ),
        "H-018-2": CandidateHypothesis(
            hypothesis_id="H-018-2",
            research_question_id="RQ-018",
            derived_from=HypothesisDerivation(
                research_model_edge_ids=(research_model.edges[0].edge_id,),
                subquestion_ids=("SQ-018-2",),
            ),
            statement="Earlier issuer triage increases analyst focus on the right names.",
            mechanism="Faster triage reduces time spent on low-signal sector scans.",
            predicted_direction="positive",
            falsification_criteria=("Issuer-first triage does not alter analyst focus or throughput.",),
            status=HypothesisStatus.ACTIVE,
            hypothesis_type=HypothesisType.MECHANISM,
        ),
        "H-018-3": CandidateHypothesis(
            hypothesis_id="H-018-3",
            research_question_id="RQ-018",
            derived_from=HypothesisDerivation(
                research_model_edge_ids=(research_model.edges[1].edge_id,),
                subquestion_ids=("SQ-018-3",),
            ),
            statement="Improved issuer triage increases subsequent selection hit rate.",
            mechanism="Correct early ranking propagates into better issuer selection decisions.",
            predicted_direction="positive",
            falsification_criteria=("Higher triage quality does not improve hit rate.",),
            status=HypothesisStatus.ACTIVE,
            hypothesis_type=HypothesisType.PRIMARY,
        ),
        "H-018-4": CandidateHypothesis(
            hypothesis_id="H-018-4",
            research_question_id="RQ-018",
            derived_from=HypothesisDerivation(
                research_model_edge_ids=(research_model.edges[1].edge_id,),
                subquestion_ids=("SQ-018-3",),
            ),
            statement="Issuer-first selection beats sector-first selection under widened dispersion.",
            mechanism="The advantage appears only when the issuer triage step improves hit rate.",
            predicted_direction="issuer_first_outperforms",
            falsification_criteria=("Issuer-first selection does not beat sector-first selection.",),
            status=HypothesisStatus.ACTIVE,
            hypothesis_type=HypothesisType.PRIMARY,
        ),
    }

    protocol = approve_gate_2(
        ExperimentProtocol(
            protocol_id="E-044",
            research_question_id="RQ-018",
            status=ProtocolStatus.GATE_1_APPROVED,
            created_at="2026-03-15T10:00:00Z",
            updated_at="2026-03-15T10:00:00Z",
            research_question=research_question.question,
            hypotheses_evaluated=tuple(hypotheses.keys()),
            target_population_and_sample="USD IG issuers observed across widening-dispersion windows.",
            data_sources_and_provenance=(
                "internal:issuer-spread-panel",
                "memo:desk-observation-2026-03-14",
            ),
            treatment_or_stimulus_definition="Compare issuer-first vs sector-first selection workflows.",
            outcome_measures_and_metrics=("issuer hit rate", "decision utility score"),
            identification_strategy="Within-window comparison of workflow ordering under matched dispersion regimes.",
            estimation_or_testing_method="Pre-registered matched-window evaluation.",
            decision_rules_and_thresholds=("Issuer-first must improve hit rate by a pre-registered margin.",),
            robustness_and_sensitivity_checks=("Vary widening-dispersion threshold definitions.",),
            negative_controls_or_placebos=("Run the same test in flat-dispersion windows.",),
            statistical_power_or_precision="Pilot precision target sufficient to detect workflow ordering effects.",
            missing_data_and_attrition_handling="Drop windows with incomplete issuer panels and report attrition.",
            multiple_testing_adjustments="Single primary endpoint; secondary outcomes reported descriptively.",
            pre_registration_and_blinding="Protocol frozen before evaluation.",
            ethical_data_use_and_governance="Internal research data only; no personal data.",
            execution_environment_and_reproducibility="Notebook-independent, deterministic batch pipeline.",
            remaining_type_b_decisions=(),
        ),
        timestamp="2026-03-15T12:00:00Z",
    )

    context = ResearchLineageContext(
        stimulus=stimulus,
        intake_ref=intake_ref,
        research_question=research_question,
        decomposition=decomposition,
        knowledge_state=knowledge_state,
        research_model=research_model,
        protocol=protocol,
    )
    return context, hypotheses


def _collect_keys(value: object) -> set[str]:
    if hasattr(value, "model_dump"):
        return _collect_keys(value.model_dump(mode="json"))
    if isinstance(value, dict):
        keys = set(value.keys())
        for child in value.values():
            keys |= _collect_keys(child)
        return keys
    if isinstance(value, (list, tuple)):
        keys: set[str] = set()
        for child in value:
            keys |= _collect_keys(child)
        return keys
    return set()


def test_v4_spec_40_lineage_is_recoverable_backward(rs_041_lineage_fixture: tuple[ResearchLineageContext, dict[str, CandidateHypothesis]]) -> None:
    context, hypotheses = rs_041_lineage_fixture

    lineage = trace_hypothesis_lineage(context, hypotheses["H-018-4"])

    assert lineage.hypothesis.hypothesis_id == "H-018-4"
    assert lineage.model_edge.edge_id == context.research_model.edges[1].edge_id
    assert lineage.subquestion.subquestion_id == "SQ-018-3"
    assert lineage.research_question.research_question_id == "RQ-018"
    assert lineage.stimulus.stimulus_id == "RS-041"
    assert lineage.intake_ref == "intake:RS-041|gate1:approved"
    assert lineage.protocol.protocol_id == "E-044"
    assert lineage.protocol.status == ProtocolStatus.GATE_2_APPROVED
    assert lineage.protocol.locked_hash

    assert lineage.stimulus.origin.type == OriginType.RESEARCHER
    assert lineage.stimulus.origin.actor_id == "andreas"
    assert lineage.stimulus.captured_by.actor_id == "research-assistant-v4"
    assert lineage.stimulus.origin.actor_id != lineage.stimulus.captured_by.actor_id

    keys = _collect_keys(lineage)
    assert "legs" not in keys
    assert "sizing" not in keys
    assert "hedge_ratio" not in keys
    assert "hedge_ratios" not in keys


def test_v4_spec_40_missing_model_edge_is_detected_loudly(rs_041_lineage_fixture: tuple[ResearchLineageContext, dict[str, CandidateHypothesis]]) -> None:
    context, _ = rs_041_lineage_fixture

    broken = CandidateHypothesis(
        hypothesis_id="H-018-broken",
        research_question_id="RQ-018",
        derived_from=HypothesisDerivation(
            research_model_edge_ids=("e:does-not-exist",),
            subquestion_ids=("SQ-018-3",),
        ),
        statement="Broken lineage example.",
        mechanism="A hypothesis cannot be recovered if its edge reference does not resolve.",
        predicted_direction="positive",
        falsification_criteria=("The edge reference resolves.",),
        status=HypothesisStatus.ACTIVE,
        hypothesis_type=HypothesisType.PRIMARY,
    )

    with pytest.raises(MissingModelEdgeLineageError, match="missing ResearchModel edge 'e:does-not-exist'"):
        trace_hypothesis_lineage(context, broken)


def test_v4_spec_40_fixture_stays_within_research_discipline_boundary(
    rs_041_lineage_fixture: tuple[ResearchLineageContext, dict[str, CandidateHypothesis]]
) -> None:
    context, hypotheses = rs_041_lineage_fixture
    lineage = trace_hypothesis_lineage(context, hypotheses["H-018-3"])

    payload = json.dumps(
        {
            "stimulus": context.stimulus.model_dump(mode="json"),
            "research_question": context.research_question.model_dump(mode="json"),
            "decomposition": context.decomposition.model_dump(mode="json"),
            "knowledge_state": context.knowledge_state.model_dump(mode="json"),
            "research_model": context.research_model.model_dump(mode="json"),
            "hypothesis": lineage.hypothesis.model_dump(mode="json"),
            "protocol": lineage.protocol.model_dump(mode="json"),
        },
        sort_keys=True,
    ).lower()

    assert "legs" not in payload
    assert "sizing" not in payload
    assert "hedge ratio" not in payload
    assert "hedge_ratio" not in payload
