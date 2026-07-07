"""Scoring VIEW over the EvidenceLink ledger (ONTOLOGY §Scoring, invariant I1).

NOT engine/scoring.py (that is Engine-3 expression scoring). S_θ and B_θ are
PURE functions of (ledger, t); no score is ever stored. Invariant under ledger
append-order permutation at fixed timestamps; evaluating mutates nothing.

    S_θ(t) = clip[-10,10]( Σ_i p_i·s_i·λ^((t−t_i)/h)·ν_i ),  per-institution net ∈ [-3,3]
    B_θ(t) = |{ institutions with net contribution > 0 }|

Phase-5 deliverable — gates: score_order_invariance, novelty_and_caps, score_is_pure.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InstitutionContribution:
    institution: str
    net: float                     # clipped to [-CAP_INST, +CAP_INST]


@dataclass(frozen=True)
class ScoreView:
    theme_id: str
    as_of: str
    S: float                       # clipped to [-SCORE_CLIP, +SCORE_CLIP]
    B: int
    by_institution: tuple[InstitutionContribution, ...] = ()


def score(theme_id: str, as_of: str, ledger) -> ScoreView:
    """Pure. `ledger` is a read-only EvidenceLink+claim join. Never stored (I1)."""
    raise NotImplementedError("Phase 5 — decay λ^((t-t_i)/h), novelty ν, per-inst cap")
