"""Phase-1 gate support: fold as the sole constructor (ONTOLOGY §Bitemporal, I5)."""
from __future__ import annotations

from engine.ledger.substrate.events import ThemeEvent, EventType, Provenance
from engine.ledger.substrate.hypothesis import (
    Mechanism, TransmissionEdge, ThemeHypothesis, LifecycleStatus, derived_direction,
)
from engine.ledger.substrate.fold import fold


def _mech(*signed_edges):
    # signed_edges: (v_from, v_to, sign), ...
    return Mechanism(edges=tuple(
        TransmissionEdge(v_from=a, v_to=b, sign=s) for (a, b, s) in signed_edges
    ))


def _created(theme_id="t1", eid="e1", *, mech=None, sigma=1, axis="C0A0_OAS",
             horizon=90, falsifier="F", recorded="2026-02-01T00:00:00+00:00"):
    mech = mech or _mech(("funding_stress", "liquidity_premium", 1),
                         ("liquidity_premium", "credit_spread", 1))
    return ThemeEvent(
        event_id=eid, theme_id=theme_id, event_type=EventType.CREATED,
        payload={"mechanism": mech.model_dump(), "shock_direction": sigma,
                 "operational_axis": axis, "horizon_days": horizon, "falsifier": falsifier},
        effective_at="2026-01-01T00:00:00+00:00", recorded_at=recorded,
        provenance=Provenance.ORPHAN_PROMOTION,
    )


def _event(etype, payload, theme_id="t1", eid="e2", recorded="2026-02-02T00:00:00+00:00"):
    return ThemeEvent(
        event_id=eid, theme_id=theme_id, event_type=etype, payload=payload,
        effective_at="2026-01-01T00:00:00+00:00", recorded_at=recorded,
        provenance=Provenance.SURVEILLANCE,
    )


def test_fold_none_without_created():
    assert fold([_event(EventType.STATUS_CHANGED, {"status": "ACTIVE"})]) is None


def test_fold_single_created_yields_hypothesis():
    theme = fold([_created()])
    assert isinstance(theme, ThemeHypothesis)
    assert theme.theme_id == "t1"
    assert theme.shock_direction == 1
    assert theme.operational_axis == "C0A0_OAS"
    assert theme.horizon_days == 90
    assert theme.status == LifecycleStatus.CANDIDATE
    assert theme.revision == 1
    assert derived_direction(theme) == 1          # σ=+1, sign product = +1


def test_fold_axis_revised_updates_axis_and_revision():
    theme = fold([_created(), _event(EventType.AXIS_REVISED, {"operational_axis": "H0A0_OAS"})])
    assert theme.operational_axis == "H0A0_OAS"
    assert theme.revision == 2


def test_fold_status_changed_to_active():
    theme = fold([_created(), _event(EventType.STATUS_CHANGED, {"status": "ACTIVE"})])
    assert theme.status == LifecycleStatus.ACTIVE


def test_fold_retired_sets_status():
    theme = fold([_created(), _event(EventType.RETIRED, {})])
    assert theme.status == LifecycleStatus.RETIRED


def test_fold_mechanism_revised_updates_mechanism():
    new = _mech(("funding_stress", "dealer_balance_sheet_capacity", -1),
                ("dealer_balance_sheet_capacity", "credit_spread", -1))
    theme = fold([_created(), _event(EventType.MECHANISM_REVISED, {"mechanism": new.model_dump()})])
    assert theme.mechanism.k == 2
    assert theme.mechanism.sign_product() == 1
    assert derived_direction(theme) == 1          # σ=+1 · (−1·−1)=+1
