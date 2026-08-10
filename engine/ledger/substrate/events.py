"""ThemeEvent — the atomic, frozen, append-only unit of the ledger
(ONTOLOGY §Bitemporal). Themes are never stored as rows; a theme is a fold
over its event stream. This module holds ONLY the event type + enums — no fold
semantics (see fold.py) and no persistence (see store.py).
"""
from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EventType(str, Enum):
    CREATED = "CREATED"
    MECHANISM_REVISED = "MECHANISM_REVISED"
    AXIS_REVISED = "AXIS_REVISED"
    FALSIFIER_REVISED = "FALSIFIER_REVISED"
    HORIZON_EXTENDED = "HORIZON_EXTENDED"
    STATUS_CHANGED = "STATUS_CHANGED"
    MERGED_INTO = "MERGED_INTO"
    RETIRED = "RETIRED"


class Provenance(str, Enum):
    WIKI_IMPORT = "wiki_import"
    SURVEILLANCE = "surveillance"
    ANALYST = "analyst"
    ORPHAN_PROMOTION = "orphan_promotion"


class ThemeEvent(BaseModel):
    """Frozen event. `recorded_at` is stamped by the persistence layer only (I7);
    callers leave it None and the store returns a stamped copy on append."""
    model_config = ConfigDict(frozen=True)

    event_id: str
    theme_id: str
    event_type: EventType
    payload: dict = Field(default_factory=dict)   # delta only
    effective_at: str                             # ISO; valid-time anchor
    recorded_at: Optional[str] = None             # ISO; set by store.append (I7)
    provenance: Provenance
    supersedes: Optional[str] = None              # event_id | None
