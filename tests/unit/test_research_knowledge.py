"""Unit tests for engine/research/knowledge.py per V4 spec sections 9.1 through 9.4."""

import pytest
from engine.memory import CoverageEntry, CoverageStatus, MemoryRetriever, WikiPage
from engine.research.knowledge import (
    KnowledgeState,
    KnowledgeStatus,
    ResearchTension,
    SubQuestionKnowledge,
    TensionType,
    map_coverage_status_to_knowledge,
)
from engine.research.question import (
    QuestionDecomposition,
    SubQuestion,
    SubQuestionRole,
    SubQuestionState,
)


def _make_mock_pages() -> dict[str, WikiPage]:
    """Create a set of mock wiki pages with method and case access classes."""
    return {
        "method-concept-a": WikiPage(
            slug="method-concept-a",
            access_class="method",
            type="concept",
            frontmatter={"slug": "method-concept-a", "access_class": "method", "type": "concept"},
            body="Method page content.",
        ),
        "sq-001": WikiPage(
            slug="sq-001",
            access_class="case",
            type="theme",
            frontmatter={
                "slug": "sq-001",
                "access_class": "case",
                "type": "theme",
                "status": "settled",
                "sources": ["source-1", "source-2"],
                "updated": "2026-08-11",
            },
            body="Case page content for sq-001 (prior conclusion: spreads widen).",
        ),
        "sq-002": WikiPage(
            slug="sq-002",
            access_class="case",
            type="theme",
            frontmatter={
                "slug": "sq-002",
                "access_class": "case",
                "type": "theme",
                "status": "open",
                "sources": [],
                "updated": "2026-08-10",
            },
            body="Case page content for sq-002.",
        ),
        "sq-contested": WikiPage(
            slug="sq-contested",
            access_class="case",
            type="theme",
            frontmatter={
                "slug": "sq-contested",
                "access_class": "case",
                "type": "theme",
                "status": "contested",
                "sources": ["source-3"],
            },
            body="Contested case page.",
        ),
        "sq-blocked": WikiPage(
            slug="sq-blocked",
            access_class="case",
            type="theme",
            frontmatter={
                "slug": "sq-blocked",
                "access_class": "case",
                "type": "theme",
                "status": "blocked",
                "sources": ["source-4"],
            },
            body="Blocked case page.",
        ),
    }


def test_map_coverage_status_to_knowledge():
    """Prove CoverageStatus maps honestly to KnowledgeStatus."""
    # SETTLED maps to KNOWN (covered ground), NEVER to SUPPORTED (direction claim)
    assert map_coverage_status_to_knowledge(CoverageStatus.SETTLED, evidence_breadth=2) == KnowledgeStatus.KNOWN
    assert map_coverage_status_to_knowledge(CoverageStatus.SETTLED, evidence_breadth=0) == KnowledgeStatus.UNKNOWN

    assert map_coverage_status_to_knowledge(CoverageStatus.OPEN, evidence_breadth=1) == KnowledgeStatus.PARTIALLY_KNOWN
    assert map_coverage_status_to_knowledge(CoverageStatus.CONTESTED, evidence_breadth=1) == KnowledgeStatus.CONTESTED
    assert map_coverage_status_to_knowledge(CoverageStatus.BLOCKED, evidence_breadth=1) == KnowledgeStatus.BLOCKED


def test_knowledge_state_builds_from_coverage_alone():
    """Prove KnowledgeState builds strictly from retriever.coverage()."""
    pages = _make_mock_pages()
    retriever = MemoryRetriever(pages, phase="A")

    subquestions = [
        SubQuestion(subquestion_id="sq-001", research_question_id="rq-1", question="What is the capex gap?", role=SubQuestionRole.NECESSARY_CONDITION),
        SubQuestion(subquestion_id="sq-002", research_question_id="rq-1", question="What is the credit impact?", role=SubQuestionRole.MECHANISM),
        SubQuestion(subquestion_id="sq-003-unmapped", research_question_id="rq-1", question="Unmapped question", role=SubQuestionRole.ENDPOINT),
    ]

    k_state = KnowledgeState.from_coverage(
        retriever=retriever,
        research_question_id="rq-1",
        subquestions=subquestions,
    )

    assert k_state.research_question_id == "rq-1"
    assert len(k_state.subquestion_states) == 3

    # Check sq-001: SETTLED coverage with 2 sources -> KNOWN
    sq1_k = k_state.get_state("sq-001")
    assert sq1_k is not None
    assert sq1_k.state == KnowledgeStatus.KNOWN
    assert sq1_k.evidence_breadth == 2
    assert sq1_k.last_updated == "2026-08-11"

    # Check sq-002: OPEN coverage with 0 sources -> UNKNOWN / gap
    sq2_k = k_state.get_state("sq-002")
    assert sq2_k is not None
    assert sq2_k.state == KnowledgeStatus.UNKNOWN
    assert sq2_k.evidence_breadth == 0

    # Check sq-003-unmapped: no coverage entry -> UNKNOWN
    sq3_k = k_state.get_state("sq-003-unmapped")
    assert sq3_k is not None
    assert sq3_k.state == KnowledgeStatus.UNKNOWN
    assert sq3_k.is_gap


def test_zero_evidence_subquestion_surfaces_as_gap_and_tension():
    """Prove zero-evidence subquestions surface as gaps and zero_evidence_gap tensions."""
    pages = _make_mock_pages()
    retriever = MemoryRetriever(pages, phase="A")

    subquestions = [
        SubQuestion(subquestion_id="sq-001", research_question_id="rq-1", question="Settled subq", role=SubQuestionRole.NECESSARY_CONDITION),
        SubQuestion(subquestion_id="sq-gap", research_question_id="rq-1", question="Gap subq", role=SubQuestionRole.MECHANISM),
    ]

    k_state = KnowledgeState.from_coverage(
        retriever=retriever,
        research_question_id="rq-1",
        subquestions=subquestions,
    )

    gaps = k_state.gaps
    assert len(gaps) == 1
    assert gaps[0].subquestion_id == "sq-gap"

    zero_gap_tensions = [
        t for t in k_state.tensions if t.tension_type == TensionType.ZERO_EVIDENCE_GAP
    ]
    assert any(t.subquestion_id == "sq-gap" for t in zero_gap_tensions)


def test_settled_vs_unknown_sibling_tension():
    """Prove a settled subquestion with an unknown sibling surfaces a SETTLED_VS_UNKNOWN_SIBLING tension."""
    pages = _make_mock_pages()
    retriever = MemoryRetriever(pages, phase="A")

    subquestions = [
        SubQuestion(subquestion_id="sq-001", research_question_id="rq-1", question="Settled subq", role=SubQuestionRole.NECESSARY_CONDITION),
        SubQuestion(subquestion_id="sq-unknown-sib", research_question_id="rq-1", question="Unknown sibling", role=SubQuestionRole.MECHANISM),
    ]

    k_state = KnowledgeState.from_coverage(
        retriever=retriever,
        research_question_id="rq-1",
        subquestions=subquestions,
    )

    sibling_tensions = [
        t for t in k_state.tensions if t.tension_type == TensionType.SETTLED_VS_UNKNOWN_SIBLING
    ]
    assert len(sibling_tensions) > 0
    t = sibling_tensions[0]
    assert t.subquestion_id == "sq-001"
    assert "sq-unknown-sib" in t.sibling_subquestion_ids


def test_firewall_intact_after_building_knowledge_state():
    """CRITICAL: Prove that building KnowledgeState leaves the firewall fully intact in Phase A.

    Calling coverage() must NOT allow reading case page bodies or case slugs in Phase A.
    """
    pages = _make_mock_pages()
    retriever = MemoryRetriever(pages, phase="A")

    assert retriever.phase == "A"

    # Build KnowledgeState
    k_state = KnowledgeState.from_coverage(
        retriever=retriever,
        research_question_id="rq-firewall",
        subquestions=["sq-001", "sq-002"],
    )

    assert k_state.research_question_id == "rq-firewall"

    # Verify retriever is STILL in Phase A
    assert retriever.phase == "A"

    # Verify method retrieval STILL succeeds
    method_page = retriever.retrieve("method-concept-a")
    assert method_page is not None
    assert method_page.slug == "method-concept-a"

    # CRITICAL: Verify EVERY case slug is REFUSED in Phase A after building KnowledgeState
    case_slugs = retriever.case_slugs()
    assert len(case_slugs) > 0

    for case_slug in case_slugs:
        result = retriever.retrieve(case_slug)
        assert result is None, f"FIREWALL BREACH: retrieve('{case_slug}') returned case page in Phase A!"
        assert case_slug in retriever.refusals


def test_knowledge_state_with_question_decomposition():
    """Prove KnowledgeState builds seamlessly from a QuestionDecomposition object."""
    pages = _make_mock_pages()
    retriever = MemoryRetriever(pages, phase="A")

    subqs = (
        SubQuestion(
            subquestion_id="sq-001",
            research_question_id="rq-decomp",
            question="What is the driver?",
            role=SubQuestionRole.NECESSARY_CONDITION,
        ),
        SubQuestion(
            subquestion_id="sq-contested",
            research_question_id="rq-decomp",
            question="What is the mechanism?",
            role=SubQuestionRole.MECHANISM,
        ),
    )
    decomp = QuestionDecomposition(
        research_question_id="rq-decomp",
        subquestions=subqs,
    )

    k_state = KnowledgeState.from_coverage(
        retriever=retriever,
        research_question_id="rq-decomp",
        subquestions=decomp,
    )

    assert k_state.get_state("sq-001").state == KnowledgeStatus.KNOWN
    assert k_state.get_state("sq-contested").state == KnowledgeStatus.CONTESTED

    contested_tensions = [t for t in k_state.tensions if t.tension_type == TensionType.CONTESTED_COVERAGE]
    assert len(contested_tensions) == 1
    assert contested_tensions[0].subquestion_id == "sq-contested"
