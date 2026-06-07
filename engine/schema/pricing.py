"""Engine-2 output: scenarios + max-entropy pricing + edge (Q4–Q7)."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

class Scenario(BaseModel):
    """One state of the world. Engine 2 / Scenario Proposer."""
    name: str
    p_s: float = Field(ge=0.0, le=1.0)   # our probability
    driver_path: str                       # which drivers realise in this state
    implied_axis_value: float              # X_s: fair value of axis | state
    pnl_per_unit: float                    # $ P&L per unit notional if state realises
    # optional — residual std of X_s | state (Step 3). 0.0 → X_s is a point estimate.
    sigma_g_s: float = 0.0
    # optional — unconditional frequency of this state, for prior="historical"
    hist_freq: Optional[float] = None
    # optional — requires macro regime classification (Lancaster / HMM)
    regime_conditional_p_s: Optional[float] = None  # p_s given axis.regime; re-run solver on this when set

class PricedIn(BaseModel):
    """Max-entropy market-implied scenario probabilities. Q6."""
    q_s: list[float]   # same ordering as ThemeObject.scenarios
    frac: float        # (X_mkt − normal_fv) / (scenario_fv − normal_fv)

class EdgeContribution(BaseModel):
    """Per-scenario edge attribution — typed, not a free-form dict (AR-ABS-003)."""
    scenario: str
    contribution: float   # (p_s - q_s) * X_s
    disagreement: float   # (p_s - q_s)

class Pricing(BaseModel):
    """Engine 2 quant output. Q4 through Q7."""
    normal_fv: float       # Q4: unconditional / regime mean of axis
    scenario_fv: float     # Q5: Σ p_s X_s
    priced_in: PricedIn    # Q6: max-entropy q_s
    residual_edge: float   # Q7: ⟨p − q, X⟩  (the edge identity)
    # optional (Step 3) — sqrt(Var[X]) under the scenario mixture (within + between).
    scenario_fv_std: Optional[float] = None
    # optional (Steps 4/6) — edge enrichment. Deterministic ones populated whenever
    # thesis_sign + sigma_axis are supplied; MC ones (edge_std..infeasible_fraction)
    # only when MC is run.
    edge_attribution: Optional[list[EdgeContribution]] = None
    edge_direction_ok: Optional[bool] = None
    vol_adjusted_edge: Optional[float] = None
    edge_basis: Optional[str] = None          # e.g. "gross_of_risk_premium"
    q_status: Optional[str] = None             # "FEASIBLE" / "INFEASIBLE"
    edge_std: Optional[float] = None
    snr: Optional[float] = None
    p_success: Optional[float] = None
    infeasible_fraction: Optional[float] = None
