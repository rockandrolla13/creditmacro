"""Append-only persistence for events and evidence links (ONTOLOGY §Bitemporal, I4).

Only `append()` + read methods exist — there is NO update or delete path, by
construction. `recorded_at` is stamped HERE and only here (I7). Backing store is
append-only JSONL (mirrors engine/outcomes.py). Phase-1 deliverable.
"""
from __future__ import annotations

from typing import Optional, Protocol, Sequence, runtime_checkable

from .events import ThemeEvent


@runtime_checkable
class EventStore(Protocol):
    """Append-only event log. append returns a copy with recorded_at stamped."""
    def append(self, event: ThemeEvent) -> ThemeEvent: ...
    def events_as_of(self, t_x: str) -> Sequence[ThemeEvent]: ...
    def events_for(self, theme_id: str, *, up_to: Optional[str] = None) -> Sequence[ThemeEvent]: ...


class JsonlEventStore:
    """append-only JSONL implementation. NO update/delete methods exist (I4)."""

    def __init__(self, path: str) -> None:
        self._path = path

    def append(self, event: ThemeEvent) -> ThemeEvent:
        raise NotImplementedError("Phase 1 — stamps recorded_at, appends one JSONL line")

    def events_as_of(self, t_x: str) -> Sequence[ThemeEvent]:
        raise NotImplementedError("Phase 1 — read events with recorded_at ≤ t_x")

    def events_for(self, theme_id: str, *, up_to: Optional[str] = None) -> Sequence[ThemeEvent]:
        raise NotImplementedError("Phase 1 — read one theme's stream")


# EvidenceLink store mirrors this shape; defined in ingest/link.py's companion at Phase 4.
