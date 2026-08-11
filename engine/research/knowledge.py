"""KnowledgeState per V4 spec sections 9.1 through 9.4.

KnowledgeState records what the project already knows about every subquestion.
Spec 9.1: Hypotheses MUST NOT be generated without checking KnowledgeState.
Built exclusively from engine.memory.MemoryRetriever.coverage().

Normative core: HISTORY MAY SET THE AGENDA, IT MAY NOT SUPPLY THE ANSWER.
Call no wall clock (invariant I8).
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from pydantic import BaseModel, ConfigDict, Field

from engine.memory import CoverageEntry, CoverageStatus, MemoryRetriever
from engine.research.question import QuestionDecomposition, SubQuestion


# ── Spec 9.3 Vocabulary ────────────────────────────────────────────────────────

class KnowledgeStatus(str, Enum):
    """Knowledge state vocabulary per V4 spec section 9.3."""
    KNOWN = "known"
    KNOWN_SUPPORTED = "known/supported"
    PARTIALLY_KNOWN = "partially_known"
    CONTESTED = "contested"
    UNKNOWN = "unknown"
    BLOCKED = "blocked"
    UNANSWERABLE_WITH_CURRENT_DATA = "unanswerable_with_current_data"


def map_coverage_status_to_knowledge(status: CoverageStatus, evidence_breadth: int = 0) -> KnowledgeStatus:
    """Map CoverageStatus from MemoryRetriever to spec 9.3 KnowledgeStatus.

    SETTLED means the ground is covered, so it maps to KNOWN (covered ground).
    It must NOT map to SUPPORTED, which is a claim about direction in the world.
    """
    if evidence_breadth == 0:
        return KnowledgeStatus.UNKNOWN
    if status == CoverageStatus.SETTLED:
        return KnowledgeStatus.KNOWN
    if status == CoverageStatus.OPEN:
        return KnowledgeStatus.PARTIALLY_KNOWN
    if status == CoverageStatus.CONTESTED:
        return KnowledgeStatus.CONTESTED
    if status == CoverageStatus.BLOCKED:
        return KnowledgeStatus.BLOCKED
    return KnowledgeStatus.UNKNOWN


# ── Spec 9.4 Research-Worthy Tensions ──────────────────────────────────────────

class TensionType(str, Enum):
    """Types of research-worthy tensions per V4 spec section 9.4."""
    ZERO_EVIDENCE_GAP = "zero_evidence_gap"
    SETTLED_VS_UNKNOWN_SIBLING = "settled_vs_unknown_sibling"
    CONTESTED_COVERAGE = "contested_coverage"
    BLOCKED_PREREQUISITE = "blocked_prerequisite"


class ResearchTension(BaseModel):
    """A research-worthy tension or gap identified in KnowledgeState (spec 9.4)."""
    model_config = ConfigDict(frozen=True)

    subquestion_id: str
    tension_type: TensionType
    description: str
    sibling_subquestion_ids: Tuple[str, ...] = ()


# ── SubQuestion Knowledge Record ───────────────────────────────────────────────

class SubQuestionKnowledge(BaseModel):
    """Knowledge record for a single subquestion (spec 9.1, 9.3)."""
    model_config = ConfigDict(frozen=True)

    subquestion_id: str
    question: str = ""
    state: KnowledgeStatus = KnowledgeStatus.UNKNOWN
    evidence_breadth: int = 0
    matched_coverage_entries: Tuple[CoverageEntry, ...] = ()
    last_updated: Optional[str] = None

    @property
    def is_known(self) -> bool:
        return self.state in (KnowledgeStatus.KNOWN, KnowledgeStatus.KNOWN_SUPPORTED)

    @property
    def is_unknown(self) -> bool:
        return self.state == KnowledgeStatus.UNKNOWN or self.evidence_breadth == 0

    @property
    def is_gap(self) -> bool:
        return self.evidence_breadth == 0 or self.state in (
            KnowledgeStatus.UNKNOWN, KnowledgeStatus.UNANSWERABLE_WITH_CURRENT_DATA
        )


# ── Spec 9.1-9.4 KnowledgeState Aggregate ──────────────────────────────────────

class KnowledgeState(BaseModel):
    """KnowledgeState per V4 spec sections 9.1 through 9.4.

    Records what the project already knows about every subquestion.
    Spec 9.1: Hypotheses MUST NOT be generated without checking KnowledgeState.
    Built exclusively from engine.memory.MemoryRetriever.coverage().
    """
    model_config = ConfigDict(frozen=True)

    research_question_id: str
    subquestion_states: Tuple[SubQuestionKnowledge, ...] = ()
    tensions: Tuple[ResearchTension, ...] = ()

    @property
    def by_subquestion_id(self) -> Dict[str, SubQuestionKnowledge]:
        return {sq.subquestion_id: sq for sq in self.subquestion_states}

    def get_state(self, subquestion_id: str) -> Optional[SubQuestionKnowledge]:
        return self.by_subquestion_id.get(subquestion_id)

    @property
    def gaps(self) -> Tuple[SubQuestionKnowledge, ...]:
        """Return all subquestions with zero evidence breadth or UNKNOWN state."""
        return tuple(sq for sq in self.subquestion_states if sq.is_gap)

    @property
    def research_worthy_tensions(self) -> Tuple[ResearchTension, ...]:
        return self.tensions

    @classmethod
    def from_coverage(
        cls,
        retriever: MemoryRetriever,
        research_question_id: str,
        subquestions: Union[Sequence[Union[SubQuestion, dict, str]], QuestionDecomposition],
        subquestion_slug_map: Optional[Dict[str, Sequence[str]]] = None,
    ) -> KnowledgeState:
        """Build KnowledgeState strictly from retriever.coverage() in Phase A.

        Must NOT call retriever.retrieve() on case slugs or read case page bodies.
        Refuses all case retrieval to maintain firewall integrity.
        """
        # Call retriever.coverage() — the ONLY case memory touch allowed
        coverage_entries = retriever.coverage()
        coverage_by_slug = {entry.slug: entry for entry in coverage_entries}

        # Normalize subquestions input
        sq_list: List[Tuple[str, str]] = []
        if isinstance(subquestions, QuestionDecomposition):
            for sq in subquestions.subquestions:
                sq_list.append((sq.subquestion_id, getattr(sq, "question", "")))
        else:
            for item in subquestions:
                if isinstance(item, SubQuestion):
                    sq_list.append((item.subquestion_id, item.question))
                elif hasattr(item, "subquestion_id"):
                    sq_list.append((item.subquestion_id, getattr(item, "question", "")))
                elif isinstance(item, dict):
                    sq_list.append((item.get("subquestion_id", ""), item.get("question", "")))
                elif isinstance(item, str):
                    sq_list.append((item, ""))

        sub_knowledge_list: List[SubQuestionKnowledge] = []
        for sq_id, sq_q in sq_list:
            matched: List[CoverageEntry] = []

            # Check explicit map if provided
            if subquestion_slug_map and sq_id in subquestion_slug_map:
                target_slugs = subquestion_slug_map[sq_id]
                for slug in target_slugs:
                    if slug in coverage_by_slug:
                        matched.append(coverage_by_slug[slug])
            else:
                # Heuristic matching: exact slug == sq_id or sq_id/slug overlap
                for entry in coverage_entries:
                    if entry.slug == sq_id or entry.slug in sq_id or sq_id in entry.slug:
                        matched.append(entry)

            if not matched:
                sub_state = KnowledgeStatus.UNKNOWN
                breadth = 0
                last_updated = None
            else:
                breadth = sum(e.evidence_breadth for e in matched)

                statuses = {e.status for e in matched}
                if CoverageStatus.CONTESTED in statuses:
                    sub_state = KnowledgeStatus.CONTESTED
                elif CoverageStatus.BLOCKED in statuses:
                    sub_state = KnowledgeStatus.BLOCKED
                elif all(s == CoverageStatus.SETTLED for s in statuses):
                    sub_state = KnowledgeStatus.KNOWN if breadth > 0 else KnowledgeStatus.UNKNOWN
                elif CoverageStatus.OPEN in statuses:
                    sub_state = KnowledgeStatus.PARTIALLY_KNOWN if breadth > 0 else KnowledgeStatus.UNKNOWN
                else:
                    sub_state = KnowledgeStatus.PARTIALLY_KNOWN if breadth > 0 else KnowledgeStatus.UNKNOWN

                updates = [e.last_updated for e in matched if e.last_updated]
                last_updated = max(updates) if updates else None

            sub_k = SubQuestionKnowledge(
                subquestion_id=sq_id,
                question=sq_q,
                state=sub_state,
                evidence_breadth=breadth,
                matched_coverage_entries=tuple(matched),
                last_updated=last_updated,
            )
            sub_knowledge_list.append(sub_k)

        # Build research-worthy tensions (spec 9.4)
        tensions_list: List[ResearchTension] = []
        sq_k_map = {sk.subquestion_id: sk for sk in sub_knowledge_list}
        all_sq_ids = [sk.subquestion_id for sk in sub_knowledge_list]

        for sk in sub_knowledge_list:
            if sk.is_gap:
                tensions_list.append(
                    ResearchTension(
                        subquestion_id=sk.subquestion_id,
                        tension_type=TensionType.ZERO_EVIDENCE_GAP,
                        description=f"Subquestion '{sk.subquestion_id}' has zero evidence breadth or unknown coverage state.",
                    )
                )

            if sk.state == KnowledgeStatus.KNOWN:
                unknown_siblings = [
                    other_id for other_id in all_sq_ids
                    if other_id != sk.subquestion_id and sq_k_map[other_id].is_gap
                ]
                if unknown_siblings:
                    tensions_list.append(
                        ResearchTension(
                            subquestion_id=sk.subquestion_id,
                            tension_type=TensionType.SETTLED_VS_UNKNOWN_SIBLING,
                            description=(
                                f"Subquestion '{sk.subquestion_id}' coverage is settled/known, "
                                f"while sibling subquestion(s) {unknown_siblings} remain unknown."
                            ),
                            sibling_subquestion_ids=tuple(unknown_siblings),
                        )
                    )

            if sk.state == KnowledgeStatus.CONTESTED:
                tensions_list.append(
                    ResearchTension(
                        subquestion_id=sk.subquestion_id,
                        tension_type=TensionType.CONTESTED_COVERAGE,
                        description=f"Subquestion '{sk.subquestion_id}' coverage is contested across prior sources.",
                    )
                )

            if sk.state == KnowledgeStatus.BLOCKED:
                tensions_list.append(
                    ResearchTension(
                        subquestion_id=sk.subquestion_id,
                        tension_type=TensionType.BLOCKED_PREREQUISITE,
                        description=f"Subquestion '{sk.subquestion_id}' is blocked from prior work.",
                    )
                )

        return cls(
            research_question_id=research_question_id,
            subquestion_states=tuple(sub_knowledge_list),
            tensions=tuple(tensions_list),
        )
