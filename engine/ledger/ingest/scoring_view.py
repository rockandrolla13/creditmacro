"""Scoring VIEW over the EvidenceLink ledger (ONTOLOGY §Scoring, invariant I1).

NOT engine/scoring.py (that is Engine-3 expression scoring). S_θ and B_θ are PURE
functions of (ledger, t); no score is ever stored. Invariant under ledger append-order
permutation at fixed timestamps; evaluating mutates nothing.

    S_θ(t) = clip[-10,10]( Σ_i p_i·s_i·λ^((t−t_i)/h)·ν_i ),  per-institution net ∈ [-3,3]
    B_θ(t) = |{ institutions with net contribution > 0 }|

with h = H/2, λ = 1/2, ν_i = NOVELTY_DISCOUNT when claim i cosine-repeats an EARLIER
same-institution claim on the same theme (> COS_NOVELTY); cross-institution repeats
keep ν = 1.0. Prior mass (wiki Case-B) adds one decaying term s_prior·λ^((t−t0)/h),
not attributed to any institution (so it never inflates breadth).
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from typing import Callable, Optional, Sequence

from ..constants import (
    CAP_INST, COS_NOVELTY, LAMBDA, NOVELTY_DISCOUNT, SCORE_CLIP,
)
from ..textsim import bow_cosine
from .claim import AtomicClaim
from .link import EvidenceLink


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


def _days(a: str, b: str) -> float:
    """(a − b) in days, from ISO date/datetime strings (date part only)."""
    return (date.fromisoformat(a[:10]) - date.fromisoformat(b[:10])).days


def _decay(as_of: str, t_i: str, horizon_days: int) -> float:
    h = horizon_days / 2.0                       # half-life
    return LAMBDA ** (_days(as_of, t_i) / h)


def _clip(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def score(
    theme_id: str,
    as_of: str,
    links: Sequence[EvidenceLink],
    claims: dict[str, AtomicClaim],
    *,
    horizon_days: int,
    prior_mass: Optional[tuple[int, str]] = None,     # (s_prior, t_import)
    similarity: Callable[[str, str], float] = bow_cosine,
) -> ScoreView:
    """Pure S_θ / B_θ over the ledger (I1). Never stored; evaluating mutates nothing."""
    superseded = {l.supersedes for l in links if l.supersedes}
    active = [
        l for l in links
        if l.theme_id == theme_id and l.link_id not in superseded and l.claim_id in claims
        and _days(as_of, claims[l.claim_id].doc_date) >= 0     # no lookahead (t_i ≤ t)
    ]

    # Deterministic total order for "earlier" (novelty) and reproducibility.
    active.sort(key=lambda l: (claims[l.claim_id].doc_date, l.claim_id))

    seen_by_inst: dict[str, list[AtomicClaim]] = defaultdict(list)
    net_by_inst: dict[str, float] = defaultdict(float)

    for link in active:
        claim = claims[link.claim_id]
        inst = claim.source_institution
        # novelty: discount iff a strictly-earlier same-institution claim is near-identical
        nu = 1.0
        for prior in seen_by_inst[inst]:
            if similarity(claim.text, prior.text) > COS_NOVELTY:
                nu = NOVELTY_DISCOUNT
                break
        contribution = (
            link.polarity * claim.stated_conviction
            * _decay(as_of, claim.doc_date, horizon_days) * nu
        )
        net_by_inst[inst] += contribution
        seen_by_inst[inst].append(claim)

    by_inst = tuple(
        InstitutionContribution(inst, _clip(net, -CAP_INST, CAP_INST))
        for inst, net in sorted(net_by_inst.items())
    )
    total = sum(c.net for c in by_inst)

    if prior_mass is not None:                    # Case-B wiki testimony (not an institution)
        s_prior, t_import = prior_mass
        if _days(as_of, t_import) >= 0:            # no lookahead
            total += s_prior * _decay(as_of, t_import, horizon_days)

    breadth = sum(1 for c in by_inst if c.net > 0)
    return ScoreView(
        theme_id=theme_id, as_of=as_of,
        S=_clip(total, -SCORE_CLIP, SCORE_CLIP), B=breadth, by_institution=by_inst,
    )
