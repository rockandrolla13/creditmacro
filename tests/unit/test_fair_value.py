"""Tests for uncertainty-propagating fair value (Step 3).

scenario_fair_value returns (E[X], sqrt(Var[X])) under the scenario mixture, where
Var[X] = Σ p_s σ_g_s²  (within)  +  Σ p_s (X_s − E[X])²  (between)  — law of total
variance. With all σ_g_s = 0 only the between-scenario dispersion remains.
"""
from __future__ import annotations

import math

import pytest

from engine.engine2 import run_pricing, scenario_fair_value
from engine.schema import Scenario

# AI-issuance scenarios: p=[.4,.35,.15,.1], X=[95,75,45,40], E[X]=75
_PX = [(0.40, 95.0), (0.35, 75.0), (0.15, 45.0), (0.10, 40.0)]
# between-variance = .4*400 + .35*0 + .15*900 + .1*1225 = 417.5
BETWEEN_STD = math.sqrt(417.5)  # 20.43281...


def _scenarios(sigma=0.0):
    return [
        Scenario(
            name=f"s{i}", p_s=p, driver_path="d",
            implied_axis_value=x, pnl_per_unit=0.0, sigma_g_s=sigma,
        )
        for i, (p, x) in enumerate(_PX)
    ]


def test_fv_with_point_scenarios_is_between_dispersion():
    fv, fv_std = scenario_fair_value(_scenarios(sigma=0.0))
    assert fv == pytest.approx(75.0, abs=1e-9)
    assert fv_std == pytest.approx(BETWEEN_STD, abs=1e-9)


def test_fv_adds_within_scenario_variance():
    # σ_g=5 on every scenario adds Σ p σ² = 25 to the variance
    fv, fv_std = scenario_fair_value(_scenarios(sigma=5.0))
    assert fv == pytest.approx(75.0, abs=1e-9)
    assert fv_std == pytest.approx(math.sqrt(417.5 + 25.0), abs=1e-9)


def test_sigma_zero_reduces_to_between_only():
    _, with_zero = scenario_fair_value(_scenarios(sigma=0.0))
    assert with_zero == pytest.approx(BETWEEN_STD, abs=1e-9)


def test_run_pricing_populates_scenario_fv_std():
    pricing = run_pricing(_scenarios(sigma=0.0), X_mkt=55.0, normal_fv=65.0)
    assert pricing.scenario_fv == pytest.approx(75.0, abs=1e-6)
    assert pricing.scenario_fv_std == pytest.approx(round(BETWEEN_STD, 4), abs=1e-6)


def test_scenario_sigma_g_s_defaults_to_zero():
    s = Scenario(name="x", p_s=1.0, driver_path="d", implied_axis_value=1.0, pnl_per_unit=0.0)
    assert s.sigma_g_s == 0.0
