"""Thesis Tracker — one persistent thesis row per ticker, with a computed view.

Discipline layer (mirrors engine/probability.py): incomplete or inconsistent rows
ARE allowed to persist; they are FLAGGED, never silently fixed and never inferred.
Nothing here invents a target price, a probability, or a current price.

- ThesisTrackerRecord          the stored row (may be incomplete)
- MarketDataRecord             ticker -> current price (the only external input)
- ComputedThesisTrackerRecord  row + current price -> probability check, weighted
                               price, upside (the read model / "view")
"""
from __future__ import annotations

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Matches the Excel rule ABS(SUM(p) - 100%) < 0.0001 so the SQLite view and a
# spreadsheet agree to the same digit.
PROBABILITY_SUM_TOL = 1e-4

ThesisStatus = Literal["active", "watchlist", "closed", "killed", "stale", "needs_review"]
ProbabilityCheck = Literal["OK", "CHECK", "MISSING"]


def _norm_ticker(v: str) -> str:
    return v.strip().upper()


class MarketDataRecord(BaseModel):
    """A ticker's current price — the only external number the tracker reads.
    Never inferred: a missing price simply leaves upside blank downstream."""
    ticker: str
    current_price: Optional[float] = None
    as_of_date: Optional[date] = None
    source: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("ticker")
    @classmethod
    def _ticker(cls, v: str) -> str:
        return _norm_ticker(v)


class ThesisTrackerRecord(BaseModel):
    """One stored thesis row. Probabilities, if present, are bounded to [0, 1] but
    their SUM is NOT enforced at construction — an off-sum row persists and is
    flagged probability_check='CHECK' by the computed view."""
    thesis_id: Optional[str] = None
    ticker: str
    weight_placeholder: Optional[float] = None
    thesis: Optional[str] = None
    bull_case_price: Optional[float] = None
    base_case_price: Optional[float] = None
    bear_case_price: Optional[float] = None
    p_bull: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    p_base: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    p_bear: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    next_catalyst: Optional[str] = None
    catalyst_date: Optional[date] = None
    kill_criteria: Optional[str] = None
    status: ThesisStatus = "active"
    source_theme_id: Optional[str] = None
    source_run_id: Optional[str] = None
    source_evidence_ids: list[str] = Field(default_factory=list)
    notes: Optional[str] = None

    @field_validator("ticker")
    @classmethod
    def _ticker(cls, v: str) -> str:
        return _norm_ticker(v)


class ComputedThesisTrackerRecord(ThesisTrackerRecord):
    """Read model: the stored row plus the derived fields. Built by from_record so
    the math has ONE definition; the SQL view in db/migrations mirrors it."""
    probability_sum: Optional[float] = None
    probability_check: ProbabilityCheck = "MISSING"
    probability_weighted_price: Optional[float] = None
    current_price: Optional[float] = None
    upside_to_current: Optional[float] = None

    @classmethod
    def from_record(
        cls, record: ThesisTrackerRecord, current_price: Optional[float] = None
    ) -> "ComputedThesisTrackerRecord":
        probs = (record.p_bull, record.p_base, record.p_bear)
        prices = (record.bull_case_price, record.base_case_price, record.bear_case_price)

        if any(p is None for p in probs):
            prob_sum: Optional[float] = None
            check: ProbabilityCheck = "MISSING"
        else:
            prob_sum = float(sum(probs))
            check = "OK" if abs(prob_sum - 1.0) < PROBABILITY_SUM_TOL else "CHECK"

        if check == "OK" and all(x is not None for x in prices):
            weighted: Optional[float] = sum(x * p for x, p in zip(prices, probs))
        else:
            weighted = None

        if weighted is not None and current_price not in (None, 0):
            upside: Optional[float] = weighted / current_price - 1.0
        else:
            upside = None

        return cls(
            **record.model_dump(),
            probability_sum=prob_sum,
            probability_check=check,
            probability_weighted_price=weighted,
            current_price=current_price,
            upside_to_current=upside,
        )
