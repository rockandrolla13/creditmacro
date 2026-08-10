"""Append-only persistence for events and evidence links (ONTOLOGY §Bitemporal, I4).

Only `append()` + read methods exist — there is NO update or delete path, by
construction. `recorded_at` is stamped HERE and only here (I7). Backing store is
append-only JSONL (mirrors engine/outcomes.py). Phase-1 deliverable.
"""
from __future__ import annotations

from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Callable, Optional, Protocol, Sequence, runtime_checkable

from .events import ThemeEvent


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_as_utc(value: str, *, date_only_end_of_day: bool) -> datetime:
    if "T" not in value:
        parsed_date = date.fromisoformat(value)
        parsed_time = time.max if date_only_end_of_day else time.min
        return datetime.combine(parsed_date, parsed_time, tzinfo=timezone.utc)
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _is_recorded_at_or_before(recorded_at: Optional[str], cutoff: str) -> bool:
    if recorded_at is None:
        return False
    return _parse_as_utc(recorded_at, date_only_end_of_day=False) <= _parse_as_utc(
        cutoff,
        date_only_end_of_day=True,
    )


@runtime_checkable
class EventStore(Protocol):
    """Append-only event log. append returns a copy with recorded_at stamped."""
    def append(self, event: ThemeEvent) -> ThemeEvent: ...
    def events_as_of(self, t_x: str) -> Sequence[ThemeEvent]: ...
    def events_for(self, theme_id: str, *, up_to: Optional[str] = None) -> Sequence[ThemeEvent]: ...


class JsonlEventStore:
    """Append-only JSONL implementation. NO update/delete methods exist (I4).

    `recorded_at` is stamped here and only here (I7) via the injected `clock`
    (default: UTC wall-clock; tests inject a deterministic clock).
    """

    def __init__(self, path: str, *, clock: Callable[[], str] = _utc_now_iso) -> None:
        self._path = Path(path)
        self._clock = clock

    def append(self, event: ThemeEvent) -> ThemeEvent:
        stamped = event.model_copy(update={"recorded_at": self._clock()})
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a") as f:
            f.write(stamped.model_dump_json() + "\n")
        return stamped

    def _read_all(self) -> list[ThemeEvent]:
        if not self._path.exists():
            return []
        out: list[ThemeEvent] = []
        for line in self._path.read_text().splitlines():
            line = line.strip()
            if line:
                out.append(ThemeEvent.model_validate_json(line))
        return out

    def events_as_of(self, t_x: str) -> Sequence[ThemeEvent]:
        return [e for e in self._read_all() if _is_recorded_at_or_before(e.recorded_at, t_x)]

    def events_for(self, theme_id: str, *, up_to: Optional[str] = None) -> Sequence[ThemeEvent]:
        return [
            e for e in self._read_all()
            if e.theme_id == theme_id
            and (up_to is None or _is_recorded_at_or_before(e.recorded_at, up_to))
        ]


# EvidenceLink store mirrors this shape; defined in ingest/link.py's companion at Phase 4.
