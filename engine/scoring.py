"""Expression-scoring quant — pure functions, no LLM, deterministic given inputs."""
from __future__ import annotations

from typing import Optional

import numpy as np

def compute_omega(
    pnl_series: list[float],
    weights: Optional[list[float]] = None,
    tau: float = 0.0,
) -> float:
    """Ω(τ) = E[(Π − τ)+] / E[(τ − Π)-]"""
    if not pnl_series:
        raise ValueError("compute_omega: pnl_series is empty — Ω is undefined.")
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
    """ρ² = β² Var(dX) / (β² Var(dX) + Var(ε))"""
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
    """Gates FIRST, rank SECOND — "best" is NEVER max E[P&L]."""
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
