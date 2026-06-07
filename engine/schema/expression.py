"""Engine-3 output: trade expressions (Q8, Q9)."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

class ScenarioPnL(BaseModel):
    scenario_name: str
    pnl: float

class Expression(BaseModel):
    """One trade expression. Engine 3 / Enumerator + Scorer."""
    id: str
    strategy_family: str   # e.g. "5s30s CDS curve", "cash bond L/S", "ETF basis"
    long_leg: str
    short_leg: str
    hedge_ratio: float
    scenario_pnl: list[ScenarioPnL]  # Π_s for every scenario
    purity: float     # ρ²: R² of expression P&L on axis moves
    convexity: float  # κ
    carry: float      # θ (bps p.a.)
    liquidity: float  # λ: composite Xantimum liquidity score [0, 1]
    crowding: float   # c: [0, 1]
    round_trip_cost_bps: float = 0.0      # cost gate input: full round-trip cost in bps
    score: Optional[float] = None         # None = gated out
    gate_fail_reason: Optional[str] = None
    # optional enrichment — require historical data to compute
    oos_stability: Optional[float] = None        # OOS/IS Sharpe ratio across walk-forward windows (Pardo)
    factor_betas: Optional[dict[str, float]] = None  # single-factor betas post-neutralisation (Tulchinsky)
