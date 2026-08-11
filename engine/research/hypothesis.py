"""CandidateHypothesis and prioritization per V4 spec sections 11.1 through 11.4."""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


# ── Spec 11.1 & 11.2 Vocabularies ─────────────────────────────────────────────

class HypothesisStatus(str, Enum):
    """Six-value vocabulary per spec 11.1."""
    CANDIDATE = "candidate"
    ACTIVE = "active"
    SUPPORTED = "supported"
    WEAKENED = "weakened"
    REFUTED = "refuted"
    SUPERSEDED = "superseded"


class HypothesisType(str, Enum):
    """Hypothesis types required by spec 11.2."""
    PRIMARY = "primary"
    COMPETING = "competing"
    NULL = "null"
    MECHANISM = "mechanism"
    BOUNDARY_CONDITION = "boundary-condition"
    ECONOMIC_VALIDATION = "economic-validation"


# ── Spec 11.1 Derivation and Hypothesis Schema ───────────────────────────────

class HypothesisDerivation(BaseModel):
    """Derivation provenance linking hypothesis to research model elements (spec 10.5, 11.1)."""
    model_config = ConfigDict(frozen=True)

    research_model_edge_ids: Tuple[str, ...] = Field(default_factory=tuple)
    subquestion_ids: Tuple[str, ...] = Field(default_factory=tuple)

    @field_validator("research_model_edge_ids", "subquestion_ids", mode="before")
    @classmethod
    def _coerce_to_tuple(cls, v: Any) -> Tuple[str, ...]:
        if v is None:
            return ()
        if isinstance(v, str):
            return (v,) if v.strip() else ()
        if isinstance(v, (list, tuple, set)):
            return tuple(str(x) for x in v if x and str(x).strip())
        return ()

    @model_validator(mode="after")
    def _validate_non_empty(self) -> "HypothesisDerivation":
        if not self.research_model_edge_ids and not self.subquestion_ids:
            raise ValueError(
                "derived_from must be non-empty: at least one research_model_edge_id "
                "or subquestion_id must be provided per spec 10.5 and 11.1"
            )
        return self


class CandidateHypothesis(BaseModel):
    """Frozen CandidateHypothesis per V4 spec 11.1.
    
    LOAD-BEARING RULE (spec 11.1, 11.4 & fourth discipline gate):
    A thesis with no falsifier is not a thesis. CandidateHypothesis with empty
    falsification_criteria must be rejected at construction by a pydantic validator.
    Equally, derived_from must be non-empty for any hypothesis derived from a model.
    """
    model_config = ConfigDict(frozen=True)

    hypothesis_id: str
    research_question_id: str
    derived_from: HypothesisDerivation
    statement: str
    mechanism: str
    predicted_direction: str
    falsification_criteria: Tuple[str, ...]
    status: HypothesisStatus = HypothesisStatus.CANDIDATE
    hypothesis_type: HypothesisType = HypothesisType.PRIMARY

    @field_validator("hypothesis_id", "research_question_id", "statement", "mechanism", mode="before")
    @classmethod
    def _validate_non_empty_str(cls, v: Any, info) -> str:
        if not isinstance(v, str) or not v.strip():
            raise ValueError(f"CandidateHypothesis field '{info.field_name}' must be a non-empty string")
        return v.strip()

    @field_validator("falsification_criteria", mode="before")
    @classmethod
    def _validate_falsification_criteria(cls, v: Any) -> Tuple[str, ...]:
        if not v:
            raise ValueError(
                "CandidateHypothesis must have non-empty falsification_criteria: "
                "a thesis with no falsifier is not a thesis"
            )
        if isinstance(v, str):
            items = [v.strip()] if v.strip() else []
        elif isinstance(v, (list, tuple, set)):
            items = [str(x).strip() for x in v if x and str(x).strip()]
        else:
            items = []

        if not items:
            raise ValueError(
                "CandidateHypothesis must have non-empty falsification_criteria: "
                "a thesis with no falsifier is not a thesis"
            )
        return tuple(items)

    @field_validator("derived_from", mode="before")
    @classmethod
    def _validate_derived_from(cls, v: Any) -> Any:
        if v is None:
            raise ValueError(
                "derived_from must be non-empty: at least one research_model_edge_id "
                "or subquestion_id must be provided per spec 10.5 and 11.1"
            )
        if isinstance(v, dict):
            edge_ids = v.get("research_model_edge_ids", [])
            sub_ids = v.get("subquestion_ids", [])
            if not edge_ids and not sub_ids:
                raise ValueError(
                    "derived_from must be non-empty: at least one research_model_edge_id "
                    "or subquestion_id must be provided per spec 10.5 and 11.1"
                )
        return v


# ── Spec 11.3 Prioritization (10 Dimensions) ─────────────────────────────────

class PrioritizationScores(BaseModel):
    """The 10 named dimensions for hypothesis prioritization per spec 11.3."""
    model_config = ConfigDict(frozen=True)

    scientific_importance: float = 0.0
    novelty: float = 0.0
    decision_relevance: float = 0.0
    falsifiability: float = 0.0
    identifiability: float = 0.0
    data_feasibility: float = 0.0
    implementation_cost: float = 0.0
    information_gain: float = 0.0
    dependency_order: float = 0.0
    downstream_option_value: float = 0.0


DEFAULT_PRIORITIZATION_WEIGHTS: Dict[str, float] = {
    "scientific_importance": 1.0,
    "novelty": 1.0,
    "decision_relevance": 1.0,
    "falsifiability": 1.0,
    "identifiability": 1.0,
    "data_feasibility": 1.0,
    "implementation_cost": -1.0,  # cost penalty
    "information_gain": 1.0,
    "dependency_order": 1.0,
    "downstream_option_value": 1.0,
}


class PrioritizedHypothesis(BaseModel):
    """Result of prioritizing a hypothesis."""
    model_config = ConfigDict(frozen=True)

    hypothesis: CandidateHypothesis
    score: float
    rank: int


def compute_priority_score(
    scores: PrioritizationScores | Dict[str, float],
    weights: Optional[Dict[str, float]] = None,
) -> float:
    """Pure function computing priority score across the 10 named dimensions."""
    w = weights if weights is not None else DEFAULT_PRIORITIZATION_WEIGHTS
    if isinstance(scores, PrioritizationScores):
        s_dict = scores.model_dump()
    elif isinstance(scores, dict):
        s_dict = scores
    else:
        raise TypeError(f"Invalid scores object type: {type(scores)}")

    total = 0.0
    for dim, weight in w.items():
        val = float(s_dict.get(dim, 0.0))
        total += val * weight
    return total


def prioritize_hypotheses(
    hypotheses: Sequence[
        CandidateHypothesis
        | Tuple[CandidateHypothesis, PrioritizationScores | Dict[str, float]]
    ],
    scores_map: Optional[Dict[str, PrioritizationScores | Dict[str, float]]] = None,
    weights: Optional[Dict[str, float]] = None,
) -> List[PrioritizedHypothesis]:
    """Pure function prioritizing candidate hypotheses deterministically (spec 11.3).
    
    Evaluates hypotheses over the ten named dimensions and returns a deterministic ranking.
    No wall clock, no randomness, stable ordering on ties (hypothesis_id ascending).
    """
    scored_list: List[Tuple[CandidateHypothesis, float]] = []

    for item in hypotheses:
        if isinstance(item, tuple) and len(item) == 2:
            hyp, s_obj = item
        elif isinstance(item, CandidateHypothesis):
            hyp = item
            if scores_map and hyp.hypothesis_id in scores_map:
                s_obj = scores_map[hyp.hypothesis_id]
            else:
                s_obj = PrioritizationScores()
        else:
            raise TypeError(f"Invalid hypothesis item for prioritization: {type(item)}")

        score = compute_priority_score(s_obj, weights=weights)
        scored_list.append((hyp, score))

    # Deterministic sorting: higher score first, tie-break by hypothesis_id ascending
    scored_list.sort(key=lambda pair: (-pair[1], pair[0].hypothesis_id))

    return [
        PrioritizedHypothesis(
            hypothesis=hyp,
            score=score,
            rank=idx + 1,
        )
        for idx, (hyp, score) in enumerate(scored_list)
    ]


# ── Spec 11.4 Activation Check ───────────────────────────────────────────────

def check_hypothesis_activation(
    hypothesis: CandidateHypothesis,
    already_answered_ids: Optional[Set[str] | Sequence[str]] = None,
    resolved_questions: Optional[Set[str] | Sequence[str]] = None,
) -> List[str]:
    """Lightweight activation check (spec 11.4).
    
    Explicitly NOT a fourth heavyweight gate; returns a list of failing reasons.
    Does NOT raise an exception on failed checks.
    """
    reasons: List[str] = []

    terminal_statuses = {
        HypothesisStatus.SUPPORTED,
        HypothesisStatus.WEAKENED,
        HypothesisStatus.REFUTED,
        HypothesisStatus.SUPERSEDED,
    }

    if hypothesis.status in terminal_statuses:
        reasons.append(
            f"Hypothesis '{hypothesis.hypothesis_id}' is already answered / resolved "
            f"(status: '{hypothesis.status.value}')"
        )
    elif hypothesis.status == HypothesisStatus.ACTIVE:
        reasons.append(
            f"Hypothesis '{hypothesis.hypothesis_id}' is already active"
        )

    ans_set = set(already_answered_ids) if already_answered_ids else set()
    if hypothesis.hypothesis_id in ans_set:
        reasons.append(
            f"Hypothesis '{hypothesis.hypothesis_id}' is already answered in external records"
        )

    res_q_set = set(resolved_questions) if resolved_questions else set()
    if hypothesis.research_question_id in res_q_set:
        reasons.append(
            f"Research question '{hypothesis.research_question_id}' is already resolved"
        )

    if not hypothesis.falsification_criteria:
        reasons.append(
            f"Hypothesis '{hypothesis.hypothesis_id}' lacks falsification criteria"
        )

    if not hypothesis.derived_from.research_model_edge_ids and not hypothesis.derived_from.subquestion_ids:
        reasons.append(
            f"Hypothesis '{hypothesis.hypothesis_id}' has empty derived_from provenance"
        )

    return reasons


# Alias for convenience
check_activation = check_hypothesis_activation
