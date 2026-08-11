"""Integration test for the ledger projection to engine discovery workflow contract.

Proves that:
1. engine.workflow._validate_causal_chain accepts a real projection output.
2. main_theme.is_routable() is True.
3. main_theme.id equals the causal chain's terminal node vk.
4. engine.firewall.freeze succeeds on the projected ThemeObject.
5. The empty-mechanism guard (D-12) continues raising ValueError on empty mechanisms.
6. Non-live status maps to 'blocked' and live status maps to 'discovery_complete' (A3).
7. Unmeasured axis fields stay None.
"""
from __future__ import annotations

import pytest

from engine.firewall import freeze
from engine.ledger.projection import to_theme_object
from engine.ledger.substrate.events import EventType, Provenance, ThemeEvent
from engine.ledger.substrate.fold import fold
from engine.ledger.substrate.hypothesis import Mechanism, TransmissionEdge
from engine.workflow import _validate_causal_chain


def _make_theme(theme_id="t1", status="ACTIVE"):
    mech = Mechanism(edges=(
        TransmissionEdge(v_from="funding_stress", v_to="liquidity_premium", sign=1),
        TransmissionEdge(v_from="liquidity_premium", v_to="credit_spread", sign=1),
    ))
    events = [
        ThemeEvent(
            event_id="e1", theme_id=theme_id, event_type=EventType.CREATED,
            payload={"mechanism": mech.model_dump(), "shock_direction": 1,
                     "operational_axis": "C0A0_OAS", "horizon_days": 90,
                     "falsifier": "falsifier text"},
            effective_at="2026-05-01T00:00:00+00:00", recorded_at="2026-05-01T00:00:00+00:00",
            provenance=Provenance.ORPHAN_PROMOTION,
        )
    ]
    if status != "CANDIDATE":
        events.append(ThemeEvent(
            event_id="e2", theme_id=theme_id, event_type=EventType.STATUS_CHANGED,
            payload={"status": status},
            effective_at="2026-05-02T00:00:00+00:00", recorded_at="2026-05-02T00:00:00+00:00",
            provenance=Provenance.SURVEILLANCE,
        ))
    return fold(events)


def test_projected_theme_object_satisfies_workflow_causal_chain_validation():
    theme = _make_theme()
    obj = to_theme_object(theme, as_of="2026-05-05")

    # 1. _validate_causal_chain accepts a real projection output
    _validate_causal_chain(obj.main_theme, obj.causal_chain)

    # 2. main_theme.is_routable() is True
    assert obj.main_theme.is_routable() is True

    # 3. main_theme.id equals the chain's terminal node
    terminal_node_id = obj.causal_chain.nodes[-1].id
    assert obj.main_theme.id == terminal_node_id
    assert obj.main_theme.id == "credit_spread"

    # 4. freeze succeeds on the projected object
    snap = freeze(obj)
    assert snap.content_hash


def test_empty_mechanism_guard_preserved():
    empty_theme = fold([
        ThemeEvent(
            event_id="e0", theme_id="t-empty", event_type=EventType.CREATED,
            payload={"mechanism": {"edges": []}, "shock_direction": 1,
                     "operational_axis": "C0A0_OAS", "horizon_days": 90,
                     "falsifier": "f"},
            effective_at="2026-05-01T00:00:00+00:00", recorded_at="2026-05-01T00:00:00+00:00",
            provenance=Provenance.ANALYST,
        )
    ])
    with pytest.raises(ValueError, match="no edges"):
        to_theme_object(empty_theme, as_of="2026-05-05")


def test_status_mapping_and_unmeasured_axis_fields_preserved():
    live_theme = _make_theme(status="ACTIVE")
    live_obj = to_theme_object(live_theme, as_of="2026-05-05")
    assert live_obj.status == "discovery_complete"
    assert live_obj.block_reason is None
    assert live_obj.axis.current_value is None
    assert live_obj.axis.history.mean is None
    assert live_obj.axis.history.vol is None

    dead_theme = _make_theme(status="RETIRED")
    dead_obj = to_theme_object(dead_theme, as_of="2026-05-05")
    assert dead_obj.status == "blocked"
    assert dead_obj.block_reason == "ledger status RETIRED"
