"""Unit tests for the DISCOVERY router — engine.discovery.select_strategy_families."""
from __future__ import annotations

import pytest

from engine.discovery import select_strategy_families
from engine.schema import Axis, AxisHistory, Scenario, StrategyFamilyRec

def _curve_axis() -> Axis:
    return Axis(
        definition="IG 5s30s OAS slope = OAS(30Y basket) − OAS(5Y basket), bps",
        measurement="Bloomberg BVAL OAS, daily close",
        current_value=55.0,
        history=AxisHistory(mean=75.0, vol=15.0, percentile=18.0, regime_tags=[]),
    )

def _relative_axis() -> Axis:
    return Axis(
        definition="French-banks-basket senior CDS − France sovereign CDS differential, bps",
        measurement="5Y on-the-run senior CDS mid, daily close",
        current_value=40.0,
        history=AxisHistory(mean=70.0, vol=30.0, percentile=10.0, regime_tags=[]),
    )

def _basis_axis() -> Axis:
    return Axis(
        definition="IG cash bond OAS − matched-tenor CDS spread (cash-CDS basis), bps",
        measurement="asset-swap spread vs CDS mid, daily close",
        current_value=12.0,
        history=AxisHistory(mean=5.0, vol=8.0, percentile=80.0, regime_tags=[]),
    )

def _widening_scenarios() -> list[Scenario]:
    return [
        Scenario(name="Surge", p_s=0.4, driver_path="", implied_axis_value=95.0, pnl_per_unit=40.0),
        Scenario(name="Base", p_s=0.35, driver_path="", implied_axis_value=75.0, pnl_per_unit=20.0),
        Scenario(name="RiskOff", p_s=0.15, driver_path="", implied_axis_value=45.0, pnl_per_unit=-10.0),
        Scenario(name="Pause", p_s=0.1, driver_path="", implied_axis_value=40.0, pnl_per_unit=-15.0),
    ]

def _select(axis, scenarios, sign=1, x_mkt=55.0, **kw):
    n = len(scenarios)
    prior = [1.0 / n] * n if n else []
    return select_strategy_families(axis, scenarios, prior, sign, x_mkt, **kw)

# ── routing: shape + direction → family ──────────────────────────────────────

def test_family_literal_is_exactly_the_routable_set():
    # The declared taxonomy must not overstate capability: every Literal member is reachable
    # by _route_family (re-add a family only when its routing rule lands).
    import typing
    fams = set(typing.get_args(StrategyFamilyRec.model_fields["family"].annotation))
    assert fams == {
        "steepener", "flattener", "long_short", "outright", "cash_cds_basis",
        "credit_vs_equity", "credit_vs_rates", "volatility_convexity", "watchlist_only",
    }

def test_curve_steeper_routes_to_steepener():
    f = _select(_curve_axis(), _widening_scenarios(), sign=1)[0]
    assert isinstance(f, StrategyFamilyRec)
    assert f.family == "steepener"
    assert f.direction == "steeper"

def test_curve_flatter_routes_to_flattener():
    narrowing = [
        Scenario(name="Spike", p_s=0.1, driver_path="", implied_axis_value=80.0, pnl_per_unit=-25.0),
        Scenario(name="Hold", p_s=0.3, driver_path="", implied_axis_value=50.0, pnl_per_unit=5.0),
        Scenario(name="Drift", p_s=0.35, driver_path="", implied_axis_value=40.0, pnl_per_unit=15.0),
        Scenario(name="Compress", p_s=0.25, driver_path="", implied_axis_value=30.0, pnl_per_unit=25.0),
    ]
    f = _select(_curve_axis(), narrowing, sign=-1)[0]
    assert f.family == "flattener"
    assert f.direction == "flatter"

def test_relative_value_routes_to_long_short():
    f = _select(_relative_axis(), _widening_scenarios(), x_mkt=55.0)[0]
    assert f.family == "long_short"

def test_basis_routes_to_cash_cds_basis():
    scen = [
        Scenario(name="Wider", p_s=0.6, driver_path="", implied_axis_value=20.0, pnl_per_unit=8.0),
        Scenario(name="Tighter", p_s=0.4, driver_path="", implied_axis_value=4.0, pnl_per_unit=-8.0),
    ]
    f = _select(_basis_axis(), scen, x_mkt=12.0)[0]  # E_p[X]=13.6 > 12 ⇒ directional edge
    assert f.family == "cash_cds_basis"

# ── decomposed confidence ────────────────────────────────────────────────────

def test_confidence_is_product_of_five_numeric_components_when_uncapped():
    f = _select(_curve_axis(), _widening_scenarios(), sign=1)[0]
    c = f.confidence_components
    assert c.scenario_availability is True
    assert f.why_not is None  # well-formed inputs ⇒ nothing capped
    assert isinstance(c.edge_survival, float)
    expected = (c.causal_confidence * c.axis_fit * c.edge_survival
                * c.purity * c.data_confidence)
    assert f.confidence == pytest.approx(expected)

def test_purity_varies_by_family_and_is_strictly_below_one():
    # A real family never perfectly isolates its axis (basis/leg residual), so purity < 1,
    # and a lower-fidelity family (cross-asset) tracks worse than a high-fidelity curve trade.
    steep = _select(_curve_axis(), _widening_scenarios())[0]              # steepener (high fidelity)
    xasset_axis = Axis(
        definition="IG credit vs equity (CDX IG vs SPX), bps",
        measurement="index spread vs equity-implied, daily close",
        current_value=55.0,
        history=AxisHistory(mean=70.0, vol=20.0, percentile=40.0, regime_tags=[]),
    )
    cross = _select(xasset_axis, _widening_scenarios())[0]               # credit_vs_equity (lower fidelity)
    assert cross.family == "credit_vs_equity"
    assert steep.confidence_components.purity < 1.0
    assert cross.confidence_components.purity < steep.confidence_components.purity

def test_all_six_components_are_stored_and_bounded():
    f = _select(_curve_axis(), _widening_scenarios())[0]
    c = f.confidence_components
    for v in (c.causal_confidence, c.axis_fit, c.purity, c.data_confidence):
        assert 0.0 <= v <= 1.0
    assert isinstance(c.edge_survival, float) and 0.0 <= c.edge_survival <= 1.0
    assert isinstance(c.scenario_availability, bool)
    assert 0.0 <= f.confidence <= 1.0

def test_every_family_carries_downstream_model_and_next_data():
    f = _select(_curve_axis(), _widening_scenarios())[0]
    assert f.required_downstream_model.strip()
    assert f.data_needed_next.strip()
    assert f.rationale.strip()

# ── caps encode "unanswerable", naming the missing input ─────────────────────

def test_no_scenarios_caps_at_0p45_and_marks_unavailable():
    f = _select(_curve_axis(), [], sign=1, x_mkt=55.0)[0]
    # still routed by shape+direction, but capped and flagged
    assert f.family == "steepener"
    assert f.confidence <= 0.45 + 1e-9
    assert f.confidence_components.scenario_availability is False
    assert f.confidence_components.edge_survival == "unknown"
    assert f.why_not and "scenario" in f.why_not.lower()

def test_no_market_value_sets_edge_unknown_and_caps_at_0p60():
    f = _select(_curve_axis(), _widening_scenarios(), has_market_value=False)[0]
    assert f.confidence_components.edge_survival == "unknown"
    assert f.confidence <= 0.60 + 1e-9
    assert f.why_not and "market value" in f.why_not.lower()

def test_no_operational_axis_does_not_route():
    fams = _select(_curve_axis(), _widening_scenarios(), has_operational_axis=False)
    assert fams == []

def test_fully_priced_view_routes_to_watchlist_only():
    # E_p[X] == x_mkt ⇒ residual edge 0 ⇒ no surviving edge ⇒ watchlist_only (route, not fail)
    priced_in = [
        Scenario(name="Up", p_s=0.5, driver_path="", implied_axis_value=80.0, pnl_per_unit=20.0),
        Scenario(name="Down", p_s=0.5, driver_path="", implied_axis_value=40.0, pnl_per_unit=-20.0),
    ]
    f = select_strategy_families(_curve_axis(), priced_in, [0.5, 0.5], 1, 60.0)[0]
    assert f.family == "watchlist_only"
    assert f.confidence == 0.0
    assert f.why_not and "priced in" in f.why_not.lower()
