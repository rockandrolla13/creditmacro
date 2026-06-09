"""Temporal PART 4 — deterministic forecast-horizon extraction.

Forward markers ('by Q3', 'over the coming months', 'by mid-year', 'going forward') resolve an
approximate forecast_end_date and mark a claim a forecast. Backward windows ('YTD', 'since the
start of the year', 'since December') resolve forecast_start_date and DO NOT make a realized fact
a forecast. Resolution is generic by year/quarter; no outcomes are scored.
"""
from __future__ import annotations

from datetime import date

import pytest

from engine.temporal import (
    classify_temporal_context,
    _resolve_backward_start,
    _resolve_forward_end,
)

SRC = date(2019, 3, 15)
CUR = date(2026, 6, 9)


@pytest.mark.parametrize("text,expected", [
    ("yields by early Q2", date(2019, 4, 30)),
    ("yields by mid-Q2", date(2019, 5, 15)),
    ("yields by late Q2", date(2019, 6, 30)),
    ("yields by Q3", date(2019, 9, 30)),
    ("yields by mid-Q3", date(2019, 8, 15)),
    ("yields by late Q3", date(2019, 9, 30)),
    ("yields by July", date(2019, 7, 31)),
    ("yields by year-end", date(2019, 12, 31)),
    ("yields over the coming months", date(2019, 6, 15)),       # source + 3 months
    ("yields over the coming six months", date(2019, 9, 15)),   # source + 6 months
    ("yields by mid-year", date(2019, 6, 30)),
])
def test_forward_end_resolution(text, expected):
    assert _resolve_forward_end(text, SRC) == expected


def test_forward_resolution_is_generic_by_year():
    assert _resolve_forward_end("by Q3", date(2022, 1, 10)) == date(2022, 9, 30)
    assert _resolve_forward_end("by mid-Q2", date(2024, 2, 1)) == date(2024, 5, 15)


@pytest.mark.parametrize("text,expected", [
    ("up 6% since the start of the year", date(2019, 1, 1)),
    ("HPC +9.99% YTD", date(2019, 1, 1)),
    ("rallied since December", date(2018, 12, 1)),
    ("since early December", date(2018, 12, 1)),
])
def test_backward_start_resolution(text, expected):
    assert _resolve_backward_start(text, SRC) == expected


def test_forward_claim_becomes_expired_forecast_with_start_and_end():
    ctx, statuses, horizons, _ = classify_temporal_context(
        source_slug="eq", access_class="case", source_date=SRC, current_date=CUR,
        claims=[("e1", 3, "US 10Y yields rise to 3.2% by mid-Q2")], mechanisms=[])
    h = horizons[0]
    assert h.forecast_start_date == SRC and h.forecast_end_date == date(2019, 5, 15)
    assert h.status == "expired" and h.outcome_check_required is True
    assert h.outcome_variable
    assert statuses[0].claim_kind == "historical_forecast"


def test_backward_only_claim_is_a_fact_not_a_forecast():
    ctx, statuses, horizons, _ = classify_temporal_context(
        source_slug="eq", access_class="case", source_date=SRC, current_date=CUR,
        claims=[("e2", 3, "cyclicals outperformed defensives by 6% since the start of the year")],
        mechanisms=[])
    # a realized 'since the start of the year' window is NOT a forward forecast
    assert horizons == []
    assert statuses[0].claim_kind == "historical_fact"
    # …but it is time-sensitive (the backward window is detected)
    assert ctx.time_sensitive_claims


def test_going_forward_is_a_forward_horizon():
    _, _, horizons, _ = classify_temporal_context(
        source_slug="eq", access_class="case", source_date=SRC, current_date=CUR,
        claims=[("e3", 1, "we stay overweight going forward")], mechanisms=[])
    assert horizons and horizons[0].forecast_end_date == date(2019, 6, 15)  # +3 months default
