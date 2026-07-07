"""Phase-1 GATES: test_as_of_exact_states, test_no_retroactive_mutation
(ONTOLOGY §Bitemporal). Exercises store → fold → as_of end to end.
"""
from __future__ import annotations

import json

from engine.ledger.substrate.events import ThemeEvent, EventType, Provenance
from engine.ledger.substrate.hypothesis import Mechanism, TransmissionEdge
from engine.ledger.substrate.store import JsonlEventStore
from engine.ledger.substrate.queries import as_of, revision


def _clock(times):
    it = iter(times)
    return lambda: next(it)


def _mech():
    return Mechanism(edges=(
        TransmissionEdge(v_from="funding_stress", v_to="liquidity_premium", sign=1),
        TransmissionEdge(v_from="liquidity_premium", v_to="credit_spread", sign=1),
    ))


def _created(theme_id, eid, axis):
    return ThemeEvent(
        event_id=eid, theme_id=theme_id, event_type=EventType.CREATED,
        payload={"mechanism": _mech().model_dump(), "shock_direction": 1,
                 "operational_axis": axis, "horizon_days": 90, "falsifier": "F"},
        effective_at="2026-01-01T00:00:00+00:00", provenance=Provenance.ORPHAN_PROMOTION,
    )


def _delta(theme_id, eid, etype, payload):
    return ThemeEvent(
        event_id=eid, theme_id=theme_id, event_type=etype, payload=payload,
        effective_at="2026-01-01T00:00:00+00:00", provenance=Provenance.SURVEILLANCE,
    )


def _axis_of(themes):
    return {t.theme_id: t.operational_axis for t in themes}


def _build(tmp_path):
    # recorded_at scripted: e1@feb1, e2@feb3, e3@feb5, e4@feb7
    store = JsonlEventStore(str(tmp_path / "events.jsonl"), clock=_clock([
        "2026-02-01T00:00:00+00:00", "2026-02-03T00:00:00+00:00",
        "2026-02-05T00:00:00+00:00", "2026-02-07T00:00:00+00:00",
    ]))
    store.append(_created("t1", "e1", "C0A0_OAS"))
    store.append(_created("t2", "e2", "H0A0_OAS"))
    store.append(_delta("t1", "e3", EventType.AXIS_REVISED, {"operational_axis": "CDX_IG_5Y"}))
    store.append(_delta("t2", "e4", EventType.RETIRED, {}))
    return store


def test_as_of_exact_states(tmp_path):
    store = _build(tmp_path)
    # feb2: only t1 exists
    assert _axis_of(as_of(store, "2026-02-02T00:00:00+00:00")) == {"t1": "C0A0_OAS"}
    # feb4: t1 + t2 both active
    assert _axis_of(as_of(store, "2026-02-04T00:00:00+00:00")) == {"t1": "C0A0_OAS", "t2": "H0A0_OAS"}
    # feb6: t1 axis revised, t2 still active
    assert _axis_of(as_of(store, "2026-02-06T00:00:00+00:00")) == {"t1": "CDX_IG_5Y", "t2": "H0A0_OAS"}
    # feb8: t2 retired → leaves the registry
    assert _axis_of(as_of(store, "2026-02-08T00:00:00+00:00")) == {"t1": "CDX_IG_5Y"}


def test_no_retroactive_mutation(tmp_path):
    store = _build(tmp_path)
    t_x = "2026-02-06T00:00:00+00:00"
    before = [t.model_dump_json() for t in sorted(as_of(store, t_x), key=lambda t: t.theme_id)]

    # append a LATE event (recorded after t_x)
    store._clock = _clock(["2026-02-10T00:00:00+00:00"])   # noqa: SLF001 (test-only)
    store.append(_delta("t1", "e5", EventType.RETIRED, {}))

    after = [t.model_dump_json() for t in sorted(as_of(store, t_x), key=lambda t: t.theme_id)]
    assert after == before                              # byte-identical: no lookahead


def test_revision_counts_folded_events(tmp_path):
    store = _build(tmp_path)
    # t1 at feb6 has folded CREATED + AXIS_REVISED = 2 events
    assert revision(store, "t1", t_x="2026-02-06T00:00:00+00:00") == 2
    # at feb2 only CREATED is visible
    assert revision(store, "t1", t_x="2026-02-02T00:00:00+00:00") == 1
