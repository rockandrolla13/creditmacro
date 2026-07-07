"""EvidenceLink — output of Pass B mapping (ONTOLOGY §EvidenceLink).

Frozen, append-only. `polarity` is COMPUTED (claim.direction × d(θ)), never
emitted by an LLM (I3). Corrections are new rows with `supersedes` set (I4).
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class EvidenceLink(BaseModel):
    model_config = ConfigDict(frozen=True)

    link_id: str
    theme_id: str
    theme_revision: int                  # fold count at mapping time
    claim_id: str
    polarity: int                        # ∈ {-1, 0, +1} = claim.direction × d(θ)
    match_confidence: float              # ∈ [0, 1]
    recorded_at: Optional[str] = None    # set by the link store (I7)
    supersedes: Optional[str] = None     # link_id | None
