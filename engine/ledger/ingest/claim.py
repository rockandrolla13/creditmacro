"""AtomicClaim — output of Pass A blind extraction (ONTOLOGY §AtomicClaim).

Granularity: one claim per (market_variable, direction, horizon). Document-level
stance summaries are forbidden.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class AtomicClaim(BaseModel):
    model_config = ConfigDict(frozen=True)

    claim_id: str
    doc_id: str
    source_institution: str
    doc_date: str                        # ISO date
    text: str                            # one-sentence paraphrase
    market_variable: str                 # tracked-axis registry member or vk vocab
    direction: int                       # ∈ {+1, -1, 0}
    horizon_days: int                    # as stated or inferred
    stated_conviction: int               # ∈ {1, 2, 3}
    mechanism_tags: tuple[str, ...] = Field(default_factory=tuple)   # vocab node_ids
