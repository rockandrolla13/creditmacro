"""Temporal edge cases for append-only ledger store read filtering."""
from __future__ import annotations

from engine.ledger.substrate.events import EventType, Provenance, ThemeEvent
from engine.ledger.substrate.store import JsonlEventStore


def _clock(times):
    it = iter(times)
    return lambda: next(it)


def _event(theme_id: str, eid: str) -> ThemeEvent:
    return ThemeEvent(
        event_id=eid,
        theme_id=theme_id,
        event_type=EventType.CREATED,
        payload={},
        effective_at="2026-01-01T00:00:00+00:00",
        provenance=Provenance.ORPHAN_PROMOTION,
    )


def test_events_as_of_date_only_cutoff_includes_same_day_events(tmp_path):
    store = JsonlEventStore(
        str(tmp_path / "events.jsonl"),
        clock=_clock(["2026-08-09T21:30:00+00:00"]),
    )
    store.append(_event("t1", "e1"))

    got = store.events_as_of("2026-08-09")

    assert [e.event_id for e in got] == ["e1"]


def test_events_as_of_compares_non_utc_cutoff_by_instant_not_lexically(tmp_path):
    store = JsonlEventStore(
        str(tmp_path / "events.jsonl"),
        clock=_clock(["2026-08-09T22:15:00+00:00"]),
    )
    store.append(_event("t1", "e1"))

    got = store.events_as_of("2026-08-09T23:00:00+02:00")

    assert got == []
