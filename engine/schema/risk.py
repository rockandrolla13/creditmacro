"""Engine-4 output (sizing + risk), the PM gate (Q13), and provenance."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


# ── Engine 4 output: sizing + risk (Q10–Q12) ─────────────────────────────────

class Sizing(BaseModel):
    """Alaph Step-4 grid. Q10."""
    conviction: int = Field(ge=1, le=4)  # 1 lowest, 4 highest
    sizing_factor: float
    target_pnl: float    # $ gross target P&L for this position
    position: str        # human-readable, e.g. "20mm 5s30s CDS steepener"
    # Proposal 8 — dynamic vol targeting (Carver, Systematic Trading)
    vol_target_bps: Optional[float] = None    # target annualised axis vol in bps
    realized_vol_bps: Optional[float] = None  # rolling realized vol (same units)
    vol_scalar: Optional[float] = None        # vol_target / realized_vol, capped at 2.0; scale position by this
    # Proposal 2 — net-of-cost P&L transparency (Carver, Advanced Futures)
    round_trip_cost_bps: Optional[float] = None   # estimated round-trip cost for this expression
    expected_roundtrips: Optional[float] = None   # round trips per year at expected holding period
    net_target_pnl: Optional[float] = None        # target_pnl minus estimated annual cost


class StopLoss(BaseModel):
    """Q11. Level is on the axis, not on P&L — structural exit."""
    level: float
    rationale: str


class Falsifier(BaseModel):
    """Q12. First-class field, not a footnote."""
    observable: str      # computable series to monitor
    threshold: float     # τ: the crossing level
    kill_rule: str       # "if {observable} crosses {threshold}, thesis is dead"


class Risk(BaseModel):
    stop_loss: StopLoss
    falsifiers: list[Falsifier]
    invalidation_horizon: str
    max_loss: float      # $ worst-case across all expressions × scenarios


# ── PM gate (Q13) ─────────────────────────────────────────────────────────────

class PMGate(BaseModel):
    """
    The agent's hard boundary. Q13.
    Lists what the agent could not resolve. Hands control to the PM.
    The agent is an epistemic engine: it converts and surfaces.
    It does NOT decide, execute, route orders, or touch a broker.
    """
    open_questions: list[str]


# ── Provenance ────────────────────────────────────────────────────────────────

class Provenance(BaseModel):
    evidence: list[str]                          # source document list
    confidence: float = Field(ge=0.0, le=1.0)
    last_updated: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
