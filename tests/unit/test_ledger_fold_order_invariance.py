"""Phase-1 GATE: test_fold_order_invariance (property).

ONTOLOGY §Bitemporal: fold is invariant under replay-order permutation among
equal-recorded_at events. Includes two AXIS_REVISED at the SAME timestamp so the
canonical tie-break (by event_id) is exercised, not just disjoint timestamps.
"""
from __future__ import annotations

from hypothesis import given, strategies as st

from engine.ledger.substrate.events import ThemeEvent, EventType, Provenance
from engine.ledger.substrate.hypothesis import Mechanism, TransmissionEdge
from engine.ledger.substrate.fold import fold


def _m():
    return Mechanism(edges=(
        TransmissionEdge(v_from="funding_stress", v_to="liquidity_premium", sign=1),
        TransmissionEdge(v_from="liquidity_premium", v_to="credit_spread", sign=1),
    ))


def _ev(eid, etype, payload, recorded):
    return ThemeEvent(
        event_id=eid, theme_id="t1", event_type=etype, payload=payload,
        effective_at="2026-01-01T00:00:00+00:00", recorded_at=recorded,
        provenance=Provenance.SURVEILLANCE,
    )


BASE = [
    _ev("e1", EventType.CREATED,
        {"mechanism": _m().model_dump(), "shock_direction": 1,
         "operational_axis": "C0A0_OAS", "horizon_days": 90, "falsifier": "F"},
        "2026-02-01T00:00:00+00:00"),
    # two AXIS_REVISED at the SAME recorded_at → tie-break by event_id (e3 wins)
    _ev("e2", EventType.AXIS_REVISED, {"operational_axis": "H0A0_OAS"},
        "2026-02-02T00:00:00+00:00"),
    _ev("e3", EventType.AXIS_REVISED, {"operational_axis": "CDX_IG_5Y"},
        "2026-02-02T00:00:00+00:00"),
    _ev("e4", EventType.STATUS_CHANGED, {"status": "ACTIVE"},
        "2026-02-03T00:00:00+00:00"),
]

REFERENCE = fold(BASE)


def test_reference_reflects_tiebreak():
    # sanity on the fixture: e3 > e2 at the same timestamp, so CDX_IG_5Y wins.
    assert REFERENCE.operational_axis == "CDX_IG_5Y"
    assert REFERENCE.revision == 4


@given(st.permutations(BASE))
def test_fold_order_invariance(perm):
    assert fold(perm) == REFERENCE
