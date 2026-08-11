"""Unit tests for LedgerProvider integrated with run_workflow."""
from __future__ import annotations

import pytest

from engine.cases import PolicyConfig
from engine.ledger_bridge import LedgerProvider, provider_for
from engine.ledger.projection import to_theme_object
from engine.ledger.substrate.events import EventType, Provenance, ThemeEvent
from engine.ledger.substrate.fold import fold
from engine.ledger.substrate.hypothesis import Mechanism, TransmissionEdge
from engine.schema import StrategyFamilyRec, ThemeObject
from engine.workflow import run_workflow

_MECHANISM = Mechanism(edges=(
    TransmissionEdge(v_from="funding_stress", v_to="liquidity_premium", sign=1),
    TransmissionEdge(v_from="liquidity_premium", v_to="credit_spread", sign=1),
))


def _event(event_id: str, event_type: EventType, payload: dict) -> ThemeEvent:
    return ThemeEvent(
        event_id=event_id,
        theme_id="t1",
        event_type=event_type,
        payload=payload,
        effective_at="2026-05-01T00:00:00+00:00",
        recorded_at="2026-05-01T00:00:00+00:00",
        provenance=Provenance.ORPHAN_PROMOTION,
    )


def _projected_with_falsifier(falsifier: str = "IG OAS fails to widen 20bp within 60d") -> ThemeObject:
    payload = {
        "mechanism": _MECHANISM.model_dump(),
        "shock_direction": 1,
        "operational_axis": "C0A0_OAS",
        "horizon_days": 90,
        "falsifier": falsifier,
    }
    events = [_event("e1", EventType.CREATED, payload)]
    return to_theme_object(fold(events), as_of="2026-05-05")


def test_discovery_mode_routes_strategy_family():
    projected = _projected_with_falsifier("IG OAS fails to widen 20bp within 60d")
    provider = provider_for(projected)
    policy = PolicyConfig()

    theme, memo = run_workflow(provider, policy, mode="discovery")

    assert theme.status == "strategy_family_routed"
    assert len(theme.strategy_families) >= 1
    # Check that routed families carry no legs or sizing
    assert theme.expressions == []
    assert theme.sizing is None
    assert theme.risk is None
    assert theme.pm_gate is None

    for sf in theme.strategy_families:
        assert isinstance(sf, StrategyFamilyRec)
        assert hasattr(sf, "family")
        assert hasattr(sf, "confidence")
        # Ensure no leg or sizing attributes on StrategyFamilyRec
        assert not hasattr(sf, "legs")
        assert not hasattr(sf, "sizing")


def test_missing_falsifier_yields_discovery_complete():
    # Pass an empty falsifier string so no valid invalidation evidence is recovered
    projected = _projected_with_falsifier(falsifier="")
    provider = LedgerProvider(projected)
    policy = PolicyConfig()

    theme, memo = run_workflow(provider, policy, mode="discovery")

    assert theme.status == "discovery_complete"
    assert len(theme.strategy_families) == 0


def test_expression_mode_raises_not_supported():
    projected = _projected_with_falsifier()
    provider = LedgerProvider(projected)
    policy = PolicyConfig()

    with pytest.raises(RuntimeError, match="expression_mode_not_supported"):
        run_workflow(provider, policy, mode="expression")


def test_seams_behavior():
    projected = _projected_with_falsifier("Custom test falsifier text")
    provider = LedgerProvider(projected)

    ctx = provider.context()
    assert ctx.x_mkt is None
    assert ctx.statement == projected.statement
    assert ctx.thesis_sign in (1, -1)

    res = provider.parse("raw research")
    assert res.observations == []
    assert res.candidate_themes == []
    assert res.consensus_signals == []
    assert res.ranked_candidates == []

    assert provider.extract_drivers("stmt") == projected.thesis
    main_theme, chain, shared_factor = provider.expand_causal("text", "theme")
    assert main_theme == projected.main_theme
    assert chain == projected.causal_chain
    assert shared_factor == projected.shared_factor

    assert provider.define_axis(projected.thesis) == projected.axis
    assert provider.build_system_map(projected.thesis, chain) is None
    assert provider.critique_mental_model("stmt", chain) is None

    loops = provider.diagnose_loops(None)
    assert loops is not None
    assert loops.dominant_loop_now == "not diagnosed"
    assert loops.possible_loop_shift == "not diagnosed"
    assert loops.decision == "watchlist"
    assert loops.invalidation_evidence == ["Custom test falsifier text"]

    assert provider.propose_scenarios(projected.thesis, projected.axis) == []
    assert provider.critique(projected) == []
