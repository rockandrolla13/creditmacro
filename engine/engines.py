"""
Four engines with real I/O contracts.

REAL — computed here (no LLM, no data feed required):
  compute_omega         Engine 3: E[(Π−τ)+] / E[(τ−Π)-], probability-weighted
  compute_purity        Engine 3: ρ² = R² of expression P&L on axis moves
  score_expression      Engine 3: multiplicative score, gates-before-rank

Engine-2 quant (solve_max_entropy_q, solve_q_tilt, compute_edge, run_pricing) lives
in engine2.py (AR-BND-001) and is RE-EXPORTED here for back-compat.

STUBBED — LLM-call interfaces with typed inputs/outputs:
  engine1_driver_extractor    → Thesis
  engine1_axis_definer        → Axis
  engine2_scenario_proposer   → list[Scenario]
  engine3_expression_enumerator → list[Expression] (pre-scoring)
  engine4_sizer_and_risk      → (Sizing, Risk, PMGate)

Stub contract: each stub documents exactly what the LLM call must return
and what validation the caller should apply before using the result.
"""
from __future__ import annotations

from typing import Optional

import numpy as np

# Engine-2 quant lives in engine2.py (AR-BND-001 — single home). Re-exported here so
# existing imports (`from .engines import run_pricing`, etc.) keep working.
from .engine2 import (  # noqa: F401
    compute_edge,
    run_pricing,
    solve_max_entropy_q,
)
from .schema import (
    Axis,
    AxisHistory,
    CausalChainStep,
    Driver,
    Expression,
    Falsifier,
    PMGate,
    Risk,
    Scenario,
    ScenarioPnL,
    Sizing,
    StopLoss,
    Thesis,
)


# ─────────────────────────────────────────────────────────────────────────────
# QUANT LAYER — all pure functions, no LLM, deterministic given inputs
# ─────────────────────────────────────────────────────────────────────────────

def compute_omega(
    pnl_series: list[float],
    weights: Optional[list[float]] = None,
    tau: float = 0.0,
) -> float:
    """
    Ω(τ) = E[(Π − τ)+] / E[(τ − Π)-]

    If weights are provided (scenario probabilities p_s), expectation is
    probability-weighted. Otherwise, simple average over the series.

    Require Ω >= 2 as a gate (per CLAUDE.md).
    Returns inf if there are no loss scenarios (all upside).
    """
    arr = np.array(pnl_series, dtype=float)
    w = np.array(weights, dtype=float) if weights is not None else np.ones(len(arr)) / len(arr)
    w = w / w.sum()  # normalise

    gain_mask = arr > tau
    loss_mask = arr < tau

    exp_gain = float(np.dot(w[gain_mask], arr[gain_mask] - tau)) if gain_mask.any() else 0.0
    exp_loss = float(np.dot(w[loss_mask], tau - arr[loss_mask])) if loss_mask.any() else 0.0

    if exp_loss < 1e-12:
        return float("inf")
    return exp_gain / exp_loss


def compute_purity(
    expression_pnl: list[float],
    axis_moves: list[float],
) -> float:
    """
    ρ² = β² Var(dX) / (β² Var(dX) + Var(ε))
       = R² of regressing expression P&L on axis moves.

    Measures how purely the expression captures the thesis axis and
    nothing else. ρ² = 1 → perfect hedge; ρ² = 0 → pure noise.
    """
    x = np.array(axis_moves, dtype=float)
    y = np.array(expression_pnl, dtype=float)

    if x.std() < 1e-10:
        return 0.0

    beta = np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1)
    y_hat = beta * x
    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))

    return float(1.0 - ss_res / ss_tot) if ss_tot > 1e-10 else 0.0


def score_expression(
    rho2: float,
    omega: float,
    convexity: float,
    liquidity: float,
    crowding: float,
    capital: float,
    round_trip_cost_bps: float = 0.0,
    expected_pnl_bps: float = 0.0,
    a: float = 0.10,              # convexity weight
    g: float = 0.50,              # crowding decay rate
    omega_min: float = 2.0,
    liquidity_min: float = 0.40,
    cost_fraction_max: float = 0.33,  # Carver: cost must not exceed 1/3 of expected edge
) -> tuple[Optional[float], Optional[str]]:
    """
    Gates FIRST, rank SECOND — "best" is NEVER max E[P&L].

    score = ρ² × Ω × (1 + a·κ) × λ × exp(−g·c) / (1 + capital)

    Returns (score, None) if all gates pass.
    Returns (None, fail_reason) if any gate fails — expression is excluded.

    Gates (per CLAUDE.md scoring rules + Carver cost gate):
      Ω    >= omega_min       (asymmetry)
      λ    >= liquidity_min   (Xantimum liquidity constraint)
      cost <= cost_fraction_max × E[PnL]  (Carver: cost < 1/3 of expected edge)
      finite worst-case enforced by caller before this function is called
    """
    if omega < omega_min:
        return None, f"Ω {omega:.2f} < minimum {omega_min:.1f}"
    if liquidity < liquidity_min:
        return None, f"λ {liquidity:.2f} < minimum {liquidity_min:.2f}"
    if round_trip_cost_bps > 0.0 and expected_pnl_bps > 0.0:
        cost_fraction = round_trip_cost_bps / expected_pnl_bps
        if cost_fraction > cost_fraction_max:
            return None, (
                f"cost {round_trip_cost_bps:.1f}bps = {cost_fraction:.0%} of "
                f"E[PnL] {expected_pnl_bps:.1f}bps > max {cost_fraction_max:.0%}"
            )

    score = (
        rho2
        * omega
        * (1.0 + a * convexity)
        * liquidity
        * np.exp(-g * crowding)
        / (1.0 + capital)
    )
    return float(score), None


# ─────────────────────────────────────────────────────────────────────────────
# GENERATIVE ENGINE STUBS
# ─────────────────────────────────────────────────────────────────────────────

def engine1_driver_extractor(statement: str, universe_text: str) -> Thesis:
    """
    TODO: LLM call.

    Input:
        statement    — the one-sentence theme (Q1)
        universe_text — the scoped universe description (Q2)

    Output: Thesis with:
        drivers[]      — each with name, sign, proxy_observable, mechanism
        causal_chain[] — DAG steps from driver to axis
        direction_of_view — signed claim on the axis

    Validation the caller must apply:
        - Every driver.proxy_observable must be a computable series
        - causal_chain must form a connected path from at least one driver to the axis
        - direction_of_view must be unambiguous (not "depends")
    """
    raise NotImplementedError(
        "engine1_driver_extractor: replace with LLM call → parse into Thesis"
    )


def engine1_axis_definer(thesis: Thesis, universe_text: str) -> Axis:
    """
    TODO: LLM call + data lookup (Bloomberg / index provider).

    Input:
        thesis       — output of driver extractor (drivers anchor the axis choice)
        universe_text — scoped universe for Q2 constraint (L_i >= τ_L, o_i <= o*)

    Output: Axis with:
        definition   — named spread/slope + full universe spec (MUST be computable)
        measurement  — how to compute it: data source, tenor, index/basket
        current_value — live or most recent value
        history       — mean, vol, percentile, regime_tags from historical data

    Gate (hard): reject any axis whose definition is a label not a series.
        FAIL: "AI credit risk"
        PASS: "OAS(30Y IG AI-issuer basket) − OAS(5Y IG AI-issuer basket), bps,
               Bloomberg BICS Tech sector, min $1bn issuance, OAS <= 300bps"
    """
    raise NotImplementedError(
        "engine1_axis_definer: replace with LLM call + data pull → Axis"
    )


def engine2_scenario_proposer(thesis: Thesis, axis: Axis) -> list[Scenario]:
    """
    TODO: LLM call.

    Input:
        thesis — drivers + causal chain
        axis   — current_value + history for anchoring X_s

    Output: list[Scenario] with:
        name           — descriptive label
        p_s            — our probability (must sum to 1.0 across all scenarios)
        driver_path    — which drivers realise, and by how much
        implied_axis_value — X_s = fair value of axis | this state
        pnl_per_unit   — $ P&L per unit notional for the best expression | state

    Validation the caller must apply:
        - sum(p_s) == 1.0 (to tolerance 1e-6)
        - Each scenario's driver_path must reference thesis.drivers by name
        - Cover at least: bull case, base case, bear case, tail risk
    """
    raise NotImplementedError(
        "engine2_scenario_proposer: replace with LLM call → list[Scenario]"
    )


def engine3_expression_enumerator(
    thesis: Thesis,
    axis: Axis,
    scenarios: list[Scenario],
) -> list[Expression]:
    """
    TODO: LLM call + instrument universe lookup.

    Input:
        thesis    — drives what kind of expression makes sense
        axis      — anchors the expression to the right instrument family
        scenarios — needed to compute scenario_pnl for each expression

    Output: list[Expression] — candidates before scoring (score=None).
        For each expression:
            strategy_family  — e.g. "5s30s CDS curve", "cash bond L/S", "CDX basis"
            long_leg / short_leg — specific instrument names
            hedge_ratio      — beta-neutral or DV01-neutral ratio
            scenario_pnl[]   — P&L per scenario (must match scenarios list)
            purity / convexity / carry / liquidity / crowding — from data / quant

    Note: score_expression() is called separately by the orchestrator.
    This stub only enumerates; it does not score.

    Validation the caller must apply:
        - len(scenario_pnl) == len(scenarios) for every expression
        - All instruments must pass the universe liquidity gate (L_i >= τ_L)
    """
    raise NotImplementedError(
        "engine3_expression_enumerator: replace with LLM call + instrument data "
        "→ list[Expression] (pre-scoring)"
    )


def engine4_sizer_and_risk(
    thesis: Thesis,
    axis: Axis,
    pricing: Pricing,
    best_expression: Expression,
    conviction: int,
    aum: float = 100_000_000.0,
    target_return: float = 0.15,
    turnover_period: float = 0.25,
) -> tuple[Sizing, Risk, PMGate]:
    """
    TODO: partially rule-based (implement), partially generative (stub).

    Rule-based (implement here):
        sizing_factor = conviction × liquidity × (E_gain / E_loss) from grid
        target_pnl = aum × target_return × turnover_period × sizing_factor
        stop_loss.level = axis.current_value − 1.5 × axis.history.vol
        max_loss = min(scenario_pnl.pnl) across best_expression.scenario_pnl

    Generative (TODO):
        falsifiers  — LLM proposes observable + threshold per driver
        open_questions — LLM identifies unresolved assumptions for PM

    Input:  all upstream objects + conviction (1–4, from Alaph grid)
    Output: (Sizing, Risk, PMGate)
    """
    raise NotImplementedError(
        "engine4_sizer_and_risk: implement rule-based sizing + "
        "LLM falsifier / open_questions generation"
    )
