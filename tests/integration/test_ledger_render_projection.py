"""Phase-7 GATES: test_render_parse_roundtrip, test_projection_roundtrip
(ONTOLOGY §Rendered view + the ledger↔engine bridge).
"""
from __future__ import annotations

from engine.ledger.substrate.events import ThemeEvent, EventType, Provenance
from engine.ledger.substrate.hypothesis import (
    Mechanism, TransmissionEdge, LifecycleStatus, derived_direction,
)
from engine.ledger.substrate.fold import fold
from engine.ledger.ingest.scoring_view import ScoreView, InstitutionContribution
from engine.ledger.wiki.render import render, parse, drift_diff
from engine.ledger.projection import to_theme_object

from engine.firewall import freeze


def _mech():
    return Mechanism(edges=(
        TransmissionEdge(v_from="funding_stress", v_to="liquidity_premium", sign=1),
        TransmissionEdge(v_from="liquidity_premium", v_to="credit_spread", sign=1),
    ))


def _created(theme_id="t1", recorded="2026-05-01T00:00:00+00:00"):
    return ThemeEvent(
        event_id="e1", theme_id=theme_id, event_type=EventType.CREATED,
        payload={"mechanism": _mech().model_dump(), "shock_direction": 1,
                 "operational_axis": "C0A0_OAS", "horizon_days": 90,
                 "falsifier": "IG OAS fails to widen 20bp within 60d of a funding-stress print"},
        effective_at="2026-05-01T00:00:00+00:00", recorded_at=recorded,
        provenance=Provenance.ORPHAN_PROMOTION,
    )


def _activate(theme_id="t1", recorded="2026-05-02T00:00:00+00:00"):
    return ThemeEvent(
        event_id="e2", theme_id=theme_id, event_type=EventType.STATUS_CHANGED,
        payload={"status": "ACTIVE"}, effective_at="2026-05-02T00:00:00+00:00",
        recorded_at=recorded, provenance=Provenance.SURVEILLANCE,
    )


def _score(theme_id="t1"):
    return ScoreView(theme_id=theme_id, as_of="2026-05-05", S=6.0, B=2,
                     by_institution=(InstitutionContribution("JPMorgan", 3.0),
                                     InstitutionContribution("GoldmanSachs", 3.0)))


def _structured(th):
    return (th.theme_id, th.mechanism, th.shock_direction, th.operational_axis,
            th.horizon_days, th.falsifier, th.status)


# ── render / parse round-trip (the named gate) ───────────────────────────────
def test_render_parse_roundtrip():
    for events in ([_created()], [_created(), _activate()]):     # CANDIDATE and ACTIVE
        theme = fold(events)
        recovered = parse(render(theme, _score()))
        assert _structured(recovered) == _structured(theme)


def test_render_contains_normative_minimum():
    page = render(fold([_created(), _activate()]), _score())
    for token in ("funding_stress", "credit_spread", "C0A0_OAS", "S_θ", "B_θ",
                  "IG OAS fails", "JPMorgan"):
        assert token in page                                     # §Rendered view minimum


# ── projection bridge round-trip (added gate) ────────────────────────────────
def test_projection_roundtrip():
    theme = fold([_created(), _activate()])
    obj = to_theme_object(theme, as_of="2026-05-05")

    # it is a VALID, freezable engine object (proves ledger + engine are one system)
    snap = freeze(obj)
    assert snap.content_hash

    # discovery content recovered from the ThemeObject equals the hypothesis
    assert obj.id == theme.theme_id
    assert obj.axis.measurement == theme.operational_axis
    assert int(obj.horizon.rstrip("d")) == theme.horizon_days
    assert int(obj.thesis.direction_of_view) == derived_direction(theme)
    nodes = [obj.thesis.causal_chain[0].from_node] + [s.to_node for s in obj.thesis.causal_chain]
    theme_nodes = [theme.mechanism.edges[0].v_from] + [e.v_to for e in theme.mechanism.edges]
    assert nodes == theme_nodes
    assert obj.provenance.evidence[0] == f"falsifier: {theme.falsifier}"


def test_projection_maps_dead_status_to_blocked():
    dead = fold([_created(), ThemeEvent(
        event_id="e3", theme_id="t1", event_type=EventType.RETIRED, payload={},
        effective_at="2026-05-03T00:00:00+00:00", recorded_at="2026-05-03T00:00:00+00:00",
        provenance=Provenance.ANALYST)])
    obj = to_theme_object(dead, as_of="2026-05-05")
    assert obj.status == "blocked"                               # A3 axis mapping


# ── drift-diff → review queue (never auto-applied) ───────────────────────────
def test_drift_diff_emits_analyst_proposed_events():
    theme = fold([_created()])
    expected = render(theme, _score())
    actual = expected.replace("horizon_days: 90", "horizon_days: 45")   # analyst edit
    proposed = drift_diff(expected, actual)
    assert proposed                                              # a change was detected
    assert all(e.provenance == Provenance.ANALYST for e in proposed)
