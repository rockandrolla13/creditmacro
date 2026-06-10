"""Thesis Tracker schema — validators + computed view (probability check, weighted
price, upside). Discipline layer: incomplete rows persist but are FLAGGED, never
inferred. Mirrors the engine's validate-flag-don't-raise convention."""
from __future__ import annotations

from datetime import date

import pytest
from pydantic import ValidationError

from engine.schema.thesis_tracker import (
    ComputedThesisTrackerRecord,
    MarketDataRecord,
    ThesisTrackerRecord,
)


def _full_record(**over):
    base = dict(
        ticker="aapl",
        thesis="AI capex cycle.",
        bull_case_price=300.0,
        base_case_price=250.0,
        bear_case_price=150.0,
        p_bull=0.25,
        p_base=0.50,
        p_bear=0.25,
    )
    base.update(over)
    return ThesisTrackerRecord(**base)


# ── ticker normalisation ────────────────────────────────────────────────────

def test_ticker_uppercased_and_stripped():
    r = ThesisTrackerRecord(ticker="  aapl  ")
    assert r.ticker == "AAPL"


def test_market_data_ticker_uppercased_and_stripped():
    m = MarketDataRecord(ticker=" msft ", current_price=400.0)
    assert m.ticker == "MSFT"


# ── probability bounds ──────────────────────────────────────────────────────

@pytest.mark.parametrize("bad", [-0.01, 1.01, 1.5])
def test_probabilities_must_be_in_unit_interval(bad):
    with pytest.raises(ValidationError):
        ThesisTrackerRecord(ticker="X", p_bull=bad)


def test_probabilities_may_be_omitted():
    r = ThesisTrackerRecord(ticker="X")
    assert r.p_bull is None and r.p_base is None and r.p_bear is None


# ── incomplete rows persist, no inference ───────────────────────────────────

def test_incomplete_row_is_allowed():
    r = ThesisTrackerRecord(ticker="X")
    assert r.thesis is None
    assert r.bull_case_price is None
    assert r.status == "active"


def test_status_rejects_unknown_value():
    with pytest.raises(ValidationError):
        ThesisTrackerRecord(ticker="X", status="bananas")


# ── computed view: probability_check ────────────────────────────────────────

def test_probability_check_ok_when_sum_is_one():
    c = ComputedThesisTrackerRecord.from_record(_full_record(), current_price=200.0)
    assert c.probability_check == "OK"
    assert c.probability_sum == pytest.approx(1.0)


def test_probability_check_flags_when_sum_off():
    c = ComputedThesisTrackerRecord.from_record(
        _full_record(p_bull=0.30, p_base=0.50, p_bear=0.25), current_price=200.0
    )
    assert c.probability_check == "CHECK"
    assert c.probability_weighted_price is None  # blank unless probabilities sum to 1


def test_probability_check_missing_when_any_omitted():
    c = ComputedThesisTrackerRecord.from_record(
        _full_record(p_bear=None), current_price=200.0
    )
    assert c.probability_check == "MISSING"
    assert c.probability_sum is None
    assert c.probability_weighted_price is None


def test_tolerance_matches_excel_threshold():
    # |sum - 1| just under 1e-4 is OK; just over is CHECK
    ok = ComputedThesisTrackerRecord.from_record(
        _full_record(p_bull=0.25005, p_base=0.50, p_bear=0.24996), current_price=200.0
    )
    assert ok.probability_check == "OK"
    bad = ComputedThesisTrackerRecord.from_record(
        _full_record(p_bull=0.2502, p_base=0.50, p_bear=0.25), current_price=200.0
    )
    assert bad.probability_check == "CHECK"


# ── computed view: weighted price + upside ──────────────────────────────────

def test_probability_weighted_price_is_sumproduct():
    c = ComputedThesisTrackerRecord.from_record(_full_record(), current_price=200.0)
    # 300*.25 + 250*.5 + 150*.25 = 75 + 125 + 37.5 = 237.5
    assert c.probability_weighted_price == pytest.approx(237.5)


def test_upside_to_current_uses_weighted_price():
    c = ComputedThesisTrackerRecord.from_record(_full_record(), current_price=200.0)
    # 237.5 / 200 - 1 = 0.1875
    assert c.upside_to_current == pytest.approx(0.1875)


def test_upside_blank_when_current_price_missing():
    c = ComputedThesisTrackerRecord.from_record(_full_record(), current_price=None)
    assert c.current_price is None
    assert c.upside_to_current is None
    # weighted price still computes (does not depend on current price)
    assert c.probability_weighted_price == pytest.approx(237.5)


def test_weighted_price_blank_when_a_target_missing():
    c = ComputedThesisTrackerRecord.from_record(
        _full_record(bear_case_price=None), current_price=200.0
    )
    assert c.probability_weighted_price is None
    assert c.upside_to_current is None


def test_computed_carries_through_base_fields():
    c = ComputedThesisTrackerRecord.from_record(
        _full_record(catalyst_date=date(2026, 7, 1), next_catalyst="Q3 earnings"),
        current_price=200.0,
    )
    assert c.ticker == "AAPL"
    assert c.next_catalyst == "Q3 earnings"
    assert c.catalyst_date == date(2026, 7, 1)
