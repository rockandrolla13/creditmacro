"""Phase-1 gate support: append-only event store (ONTOLOGY §Bitemporal, I4/I7)."""
from __future__ import annotations

import pytest

from engine.ledger.substrate.events import ThemeEvent, EventType, Provenance
from engine.ledger.substrate.store import JsonlEventStore


def _clock(times):
    it = iter(times)
    return lambda: next(it)


def _event(theme_id, eid, etype=EventType.CREATED, payload=None,
           effective="2026-01-01T00:00:00+00:00"):
    return ThemeEvent(
        event_id=eid, theme_id=theme_id, event_type=etype,
        payload=payload or {}, effective_at=effective,
        provenance=Provenance.ORPHAN_PROMOTION,
    )


def test_append_stamps_recorded_at(tmp_path):
    store = JsonlEventStore(str(tmp_path / "events.jsonl"),
                            clock=_clock(["2026-02-01T00:00:00+00:00"]))
    ev = _event("t1", "e1")
    assert ev.recorded_at is None                     # caller never sets it (I7)
    stored = store.append(ev)
    assert stored.recorded_at == "2026-02-01T00:00:00+00:00"


def test_events_for_reads_back_in_append_order(tmp_path):
    store = JsonlEventStore(str(tmp_path / "events.jsonl"),
                            clock=_clock(["2026-02-01T00:00:00+00:00",
                                          "2026-02-02T00:00:00+00:00"]))
    store.append(_event("t1", "e1"))
    store.append(_event("t1", "e2", etype=EventType.RETIRED))
    got = store.events_for("t1")
    assert [e.event_id for e in got] == ["e1", "e2"]


def test_events_as_of_filters_by_recorded_at(tmp_path):
    store = JsonlEventStore(str(tmp_path / "events.jsonl"),
                            clock=_clock(["2026-02-01T00:00:00+00:00",
                                          "2026-02-03T00:00:00+00:00"]))
    store.append(_event("t1", "e1"))
    store.append(_event("t1", "e2", etype=EventType.RETIRED))
    as_of_feb2 = store.events_as_of("2026-02-02T00:00:00+00:00")
    assert [e.event_id for e in as_of_feb2] == ["e1"]  # e2 recorded later → excluded


def test_store_has_no_mutation_methods():
    # I4: append-only — no update/delete/remove/set path exists.
    for banned in ("update", "delete", "remove", "overwrite"):
        assert not hasattr(JsonlEventStore, banned)
