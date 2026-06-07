"""Unit tests for engine.engine2.solve_q_tilt — the closed-form exponential-tilt q."""
from __future__ import annotations

import math

import pytest

from engine.engine2 import (
    QSolution,
    level_constraint,
    option_constraint,
    solve_q_tilt,
)

# AI-issuance numbers
X_AI = [95.0, 75.0, 45.0, 40.0]
XMKT_AI = 55.0
UNIFORM4 = [0.25, 0.25, 0.25, 0.25]
GOLDEN_Q = [0.125512, 0.184417, 0.328452, 0.361619]
ABS = 1e-6

def test_k1_reproduces_golden_q():
    sol = solve_q_tilt(X_AI, [level_constraint(XMKT_AI)], prior=UNIFORM4)
    assert isinstance(sol, QSolution)
    assert sol.status == "FEASIBLE"
    assert sol.q == pytest.approx(GOLDEN_Q, abs=ABS)

def test_k1_constraint_is_satisfied():
    sol = solve_q_tilt(X_AI, [level_constraint(XMKT_AI)], prior=UNIFORM4)
    e_q_x = sum(q * x for q, x in zip(sol.q, X_AI))
    assert e_q_x == pytest.approx(XMKT_AI, abs=1e-9)

def test_q_sums_to_one_and_is_positive():
    sol = solve_q_tilt(X_AI, [level_constraint(XMKT_AI)], prior=UNIFORM4)
    assert sum(sol.q) == pytest.approx(1.0, abs=1e-12)
    assert all(q > 0 for q in sol.q)

def test_infeasible_when_xmkt_above_span():
    sol = solve_q_tilt(X_AI, [level_constraint(200.0)], prior=UNIFORM4)
    assert sol.status == "INFEASIBLE"
    assert "span" in sol.reason.lower()

def test_infeasible_when_xmkt_below_span():
    sol = solve_q_tilt(X_AI, [level_constraint(10.0)], prior=UNIFORM4)
    assert sol.status == "INFEASIBLE"

def test_infeasible_when_all_xs_equal():
    # degenerate: Var_q[X] == 0 everywhere (AR-TST-001)
    sol = solve_q_tilt([50.0, 50.0, 50.0], [level_constraint(50.0)], prior=[1 / 3] * 3)
    assert sol.status == "INFEASIBLE"

def test_single_scenario_is_infeasible_unless_trivial():
    sol = solve_q_tilt([50.0], [level_constraint(55.0)], prior=[1.0])
    assert sol.status == "INFEASIBLE"

def test_prior_pulls_q_toward_prior():
    # heavier prior on the first scenario should raise q_0 vs the uniform solution
    skewed = [0.7, 0.1, 0.1, 0.1]
    base = solve_q_tilt(X_AI, [level_constraint(XMKT_AI)], prior=UNIFORM4)
    pulled = solve_q_tilt(X_AI, [level_constraint(XMKT_AI)], prior=skewed)
    assert pulled.status == "FEASIBLE"
    assert pulled.q[0] > base.q[0]
    # constraint still holds exactly
    assert sum(q * x for q, x in zip(pulled.q, X_AI)) == pytest.approx(XMKT_AI, abs=1e-9)

def test_k2_option_constraint_is_satisfied():
    # axis-struck call payoff f(X)=max(X-70,0); target=4.0 is interior to the
    # convex hull of (X, payoff) at level 55 (≈1.67 .. 6.82), so jointly feasible.
    strike, target = 70.0, 4.0
    cons = [level_constraint(XMKT_AI), option_constraint(strike, target)]
    sol = solve_q_tilt(X_AI, cons, prior=UNIFORM4)
    assert sol.status == "FEASIBLE"
    e_level = sum(q * x for q, x in zip(sol.q, X_AI))
    e_opt = sum(q * max(x - strike, 0.0) for q, x in zip(sol.q, X_AI))
    assert e_level == pytest.approx(XMKT_AI, abs=1e-6)
    assert e_opt == pytest.approx(target, abs=1e-6)
    assert math.isclose(sum(sol.q), 1.0, abs_tol=1e-12)

def test_k2_jointly_infeasible_target_outside_hull():
    # target option value 8.0 exceeds the hull's upper bound (~6.82) at level 55:
    # no q matches both moments → INFEASIBLE (per-constraint spans alone pass).
    cons = [level_constraint(XMKT_AI), option_constraint(70.0, 8.0)]
    sol = solve_q_tilt(X_AI, cons, prior=UNIFORM4)
    assert sol.status == "INFEASIBLE"
