"""
Golden-master regression test — AI-issuance theme.

CHARACTERIZATION test: it pins the numbers `engine.example` produces TODAY, so any
later refactor (case system, engine2 hardening) that moves these is caught
immediately. Per the project's hard constraint, these must hold to 1e-6 before AND
after every change.

The ThemeObject.id / created_at / provenance.last_updated fields are non-
deterministic (uuid4 / now()) and are deliberately NOT asserted here.
"""
from __future__ import annotations

import pytest

# Importing engine.example runs the pipeline at module load and exposes the objects.
from engine.example import (
    expr_etf_basis,
    expr_steepener,
    omega_steepener,
    pricing,
    score_val,
    sizing,
    theme,
)

ABS = 1e-6


def test_scenario_fair_value_is_golden():
    assert pricing.scenario_fv == pytest.approx(75.0, abs=ABS)


def test_priced_in_q_is_golden():
    assert pricing.priced_in.q_s == pytest.approx(
        [0.125512, 0.184417, 0.328452, 0.361619], abs=ABS
    )


def test_priced_in_q_sums_to_one():
    assert sum(pricing.priced_in.q_s) == pytest.approx(1.0, abs=ABS)


def test_residual_edge_is_golden():
    assert pricing.residual_edge == pytest.approx(20.0, abs=ABS)


def test_priced_in_fraction_is_golden():
    assert pricing.priced_in.frac == pytest.approx(-1.0, abs=ABS)


def test_omega_is_golden():
    assert omega_steepener == pytest.approx(7.666666666666667, abs=ABS)


def test_best_expression_score_is_golden():
    assert score_val == pytest.approx(3.918220233274124, abs=ABS)
    assert expr_steepener.score == pytest.approx(3.918220233274124, abs=ABS)


def test_etf_basis_is_gated_out_on_liquidity():
    assert expr_etf_basis.score is None
    assert expr_etf_basis.gate_fail_reason == "λ 0.32 < minimum 0.40"


def test_sizing_vol_scalar_is_golden():
    assert sizing.vol_scalar == pytest.approx(1.25, abs=ABS)


def test_sizing_net_target_pnl_is_golden():
    assert sizing.target_pnl == pytest.approx(750000.0, abs=ABS)
    assert sizing.net_target_pnl == pytest.approx(747000.0, abs=ABS)


def test_all_four_discipline_gates_pass():
    # If any of the 4 discipline gates failed, ThemeObject construction in
    # engine.example would have raised — so a populated theme proves all pass.
    assert theme.statement == "AI issuance will steepen IG credit curves"
    assert theme.pricing.residual_edge == pytest.approx(20.0, abs=ABS)
    assert any(e.score is not None for e in theme.expressions)  # gate 3
    assert len(theme.risk.falsifiers) >= 1                       # gate 4
