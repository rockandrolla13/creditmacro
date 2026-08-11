"""Helpers for recovering backward lineage across V4 research objects.

This module is intentionally additive: phase 1 and 2 created the individual
research objects, while spec section 40 requires that they be traversable as a
single chain from an accepted claim back to the originating question and
evidence.
"""
from __future__ import annotations

from dataclasses import dataclass

from engine.research.hypothesis import CandidateHypothesis
from engine.research.knowledge import KnowledgeState, SubQuestionKnowledge
from engine.research.model import ModelEdge, ResearchModel
from engine.research.protocol import ExperimentProtocol, ProtocolStatus
from engine.research.question import QuestionDecomposition, ResearchQuestion, SubQuestion
from engine.research.stimulus import ResearchStimulus


class LineageTraversalError(ValueError):
    """Base class for lineage traversal failures."""


class MissingModelEdgeLineageError(LineageTraversalError):
    """Raised when a hypothesis names a model edge that cannot be resolved."""


class MissingSubQuestionLineageError(LineageTraversalError):
    """Raised when a hypothesis names a subquestion that cannot be resolved."""


class MissingKnowledgeStateLineageError(LineageTraversalError):
    """Raised when a subquestion has no knowledge-state record."""


class MissingResearchQuestionLineageError(LineageTraversalError):
    """Raised when the objects disagree about the research question identity."""


class MissingStimulusLineageError(LineageTraversalError):
    """Raised when the research question cannot be linked back to its stimulus."""


class MissingProtocolLineageError(LineageTraversalError):
    """Raised when the experiment protocol cannot be linked to the hypothesis."""


@dataclass(frozen=True)
class ResearchLineageContext:
    """The concrete object set that spec section 40 says must stay traversable."""

    stimulus: ResearchStimulus
    intake_ref: str
    research_question: ResearchQuestion
    decomposition: QuestionDecomposition
    knowledge_state: KnowledgeState
    research_model: ResearchModel
    protocol: ExperimentProtocol


@dataclass(frozen=True)
class HypothesisLineage:
    """Backward lineage from a hypothesis to the originating stimulus."""

    hypothesis: CandidateHypothesis
    model_edge: ModelEdge
    subquestion: SubQuestion
    knowledge_state: SubQuestionKnowledge
    research_question: ResearchQuestion
    stimulus: ResearchStimulus
    protocol: ExperimentProtocol
    intake_ref: str


def trace_hypothesis_lineage(
    context: ResearchLineageContext,
    hypothesis: CandidateHypothesis,
) -> HypothesisLineage:
    """Recover spec-40 backward lineage for one hypothesis.

    The function raises typed errors rather than returning partial lineage. A
    broken link is a finding that tests should surface loudly.
    """
    if hypothesis.research_question_id != context.research_question.research_question_id:
        raise MissingResearchQuestionLineageError(
            "Hypothesis research_question_id "
            f"'{hypothesis.research_question_id}' does not match ResearchQuestion "
            f"'{context.research_question.research_question_id}'."
        )

    if context.decomposition.research_question_id != context.research_question.research_question_id:
        raise MissingResearchQuestionLineageError(
            "QuestionDecomposition research_question_id "
            f"'{context.decomposition.research_question_id}' does not match ResearchQuestion "
            f"'{context.research_question.research_question_id}'."
        )

    if context.knowledge_state.research_question_id != context.research_question.research_question_id:
        raise MissingResearchQuestionLineageError(
            "KnowledgeState research_question_id "
            f"'{context.knowledge_state.research_question_id}' does not match ResearchQuestion "
            f"'{context.research_question.research_question_id}'."
        )

    if context.protocol.research_question_id != context.research_question.research_question_id:
        raise MissingProtocolLineageError(
            "ExperimentProtocol research_question_id "
            f"'{context.protocol.research_question_id}' does not match ResearchQuestion "
            f"'{context.research_question.research_question_id}'."
        )

    edge_id = next(iter(hypothesis.derived_from.research_model_edge_ids), "")
    if not edge_id:
        raise MissingModelEdgeLineageError(
            f"Hypothesis '{hypothesis.hypothesis_id}' names no research_model_edge_id."
        )

    model_edge = context.research_model.edge_by_id(edge_id)
    if model_edge is None:
        raise MissingModelEdgeLineageError(
            f"Hypothesis '{hypothesis.hypothesis_id}' references missing ResearchModel edge "
            f"'{edge_id}' in model '{context.research_model.model_id}'."
        )

    subquestion_id = next(iter(hypothesis.derived_from.subquestion_ids), "")
    if not subquestion_id:
        raise MissingSubQuestionLineageError(
            f"Hypothesis '{hypothesis.hypothesis_id}' names no subquestion_id."
        )

    subquestion = context.decomposition.get_subquestion(subquestion_id)
    if subquestion is None:
        raise MissingSubQuestionLineageError(
            f"Hypothesis '{hypothesis.hypothesis_id}' references missing subquestion "
            f"'{subquestion_id}'."
        )

    knowledge_state = context.knowledge_state.get_state(subquestion_id)
    if knowledge_state is None:
        raise MissingKnowledgeStateLineageError(
            f"KnowledgeState has no record for subquestion '{subquestion_id}'."
        )

    if hypothesis.hypothesis_id not in context.protocol.hypotheses_evaluated:
        raise MissingProtocolLineageError(
            f"ExperimentProtocol '{context.protocol.protocol_id}' does not evaluate "
            f"hypothesis '{hypothesis.hypothesis_id}'."
        )

    if context.protocol.status not in (
        ProtocolStatus.GATE_2_APPROVED,
        ProtocolStatus.LOCKED,
        ProtocolStatus.EXECUTED,
        ProtocolStatus.GATE_3_REVIEWED,
        ProtocolStatus.ARCHIVED,
    ):
        raise MissingProtocolLineageError(
            f"ExperimentProtocol '{context.protocol.protocol_id}' is not Gate 2 approved."
        )

    if not context.protocol.locked_hash:
        raise MissingProtocolLineageError(
            f"ExperimentProtocol '{context.protocol.protocol_id}' has no Gate 2 lock hash."
        )

    if context.research_question.originating_intake_ref != context.intake_ref:
        raise MissingStimulusLineageError(
            "ResearchQuestion originating_intake_ref "
            f"'{context.research_question.originating_intake_ref}' does not match intake_ref "
            f"'{context.intake_ref}'."
        )

    if context.stimulus.stimulus_id not in context.intake_ref:
        raise MissingStimulusLineageError(
            f"Intake ref '{context.intake_ref}' does not point back to stimulus "
            f"'{context.stimulus.stimulus_id}'."
        )

    return HypothesisLineage(
        hypothesis=hypothesis,
        model_edge=model_edge,
        subquestion=subquestion,
        knowledge_state=knowledge_state,
        research_question=context.research_question,
        stimulus=context.stimulus,
        protocol=context.protocol,
        intake_ref=context.intake_ref,
    )
