"""run_pricing now populates the deterministic edge enrichments (attribution,"""
from __future__ import annotations

import pytest

from engine.engine2 import run_pricing
from engine.schema import EdgeContribution, Scenario

_PX = [(0.40, 95.0, "AI Surge"), (0.35, 75.0, "Base"),
       (0.15, 45.0, "Risk-Off"), (0.10, 40.0, "Capex Pause")]

def _scenarios():
    return [
        Scenario(name=nm, p_s=p, driver_path="d", implied_axis_value=x, pnl_per_unit=0.0)
        for p, x, nm in _PX
    ]

def test_pricing_golden_numbers_unchanged_with_enrichment():
    pr = run_pricing(_scenarios(), X_mkt=55.0, normal_fv=65.0,
                     thesis_sign=1, sigma_axis=15.0)
    assert pr.scenario_fv == pytest.approx(75.0, abs=1e-6)
    assert pr.residual_edge == pytest.approx(20.0, abs=1e-6)
    assert pr.priced_in.q_s == pytest.approx(
        [0.125512, 0.184417, 0.328452, 0.361619], abs=1e-6
    )

def test_attribution_is_populated_typed_and_sorted():
    pr = run_pricing(_scenarios(), X_mkt=55.0, normal_fv=65.0,
                     thesis_sign=1, sigma_axis=15.0)
    assert pr.edge_attribution is not None
    assert all(isinstance(c, EdgeContribution) for c in pr.edge_attribution)
    contribs = [c.contribution for c in pr.edge_attribution]
    assert contribs == sorted(contribs, reverse=True)
    assert pr.edge_attribution[0].scenario == "AI Surge"

def test_direction_and_basis_and_status():
    pr = run_pricing(_scenarios(), X_mkt=55.0, normal_fv=65.0,
                     thesis_sign=1, sigma_axis=15.0)
    assert pr.edge_direction_ok is True
    assert pr.edge_basis == "gross_of_risk_premium"
    assert pr.q_status == "FEASIBLE"
    assert pr.vol_adjusted_edge == pytest.approx(20.0 / 15.0, abs=1e-6)

def test_mc_fields_are_none_without_opt_in():
    pr = run_pricing(_scenarios(), X_mkt=55.0, normal_fv=65.0,
                     thesis_sign=1, sigma_axis=15.0)
    assert pr.edge_std is None
    assert pr.snr is None

def test_mc_fields_populated_on_opt_in():
    pr = run_pricing(_scenarios(), X_mkt=55.0, normal_fv=65.0,
                     thesis_sign=1, sigma_axis=15.0, run_mc=True, n_draws=300, seed=0)
    assert pr.edge_std is not None
    assert pr.snr is not None
    assert pr.infeasible_fraction is not None

def test_bare_call_leaves_enrichment_none():
    # no thesis_sign / sigma_axis → enrichment stays None (back-compat)
    pr = run_pricing(_scenarios(), X_mkt=55.0, normal_fv=65.0)
    assert pr.edge_direction_ok is None
    assert pr.vol_adjusted_edge is None
