"""Thesis Tracker SQLite store — migration, upsert (one row per ticker), and the
computed view. The view's math MUST agree with ComputedThesisTrackerRecord.from_record
(one definition, two surfaces)."""
from __future__ import annotations

from datetime import date

import pytest

from engine.schema.thesis_tracker import (
    ComputedThesisTrackerRecord,
    MarketDataRecord,
    ThesisTrackerRecord,
)
from engine.thesis_tracker import ThesisTrackerDB


@pytest.fixture
def db(tmp_path):
    with ThesisTrackerDB(tmp_path / "tt.sqlite") as d:
        d.migrate()
        yield d


def _rec(**over):
    base = dict(
        ticker="aapl",
        thesis="AI capex cycle.",
        bull_case_price=300.0,
        base_case_price=250.0,
        bear_case_price=150.0,
        p_bull=0.25,
        p_base=0.50,
        p_bear=0.25,
        next_catalyst="Q3 earnings",
        catalyst_date=date(2026, 7, 1),
        source_evidence_ids=["ev-1", "ev-2"],
    )
    base.update(over)
    return ThesisTrackerRecord(**base)


# ── migration ────────────────────────────────────────────────────────────────

def test_migrate_is_idempotent(tmp_path):
    with ThesisTrackerDB(tmp_path / "tt.sqlite") as d:
        d.migrate()
        d.migrate()  # second run must not raise
        assert d.applied_migrations()  # at least one recorded


# ── upsert / round-trip ──────────────────────────────────────────────────────

def test_upsert_assigns_thesis_id_when_missing(db):
    tid = db.upsert_thesis(_rec())
    assert tid
    got = db.get_thesis("AAPL")
    assert got is not None
    assert got.thesis_id == tid


def test_upsert_round_trips_all_fields(db):
    db.upsert_thesis(_rec())
    got = db.get_thesis("aapl")  # lookup normalises ticker
    assert got.ticker == "AAPL"
    assert got.catalyst_date == date(2026, 7, 1)
    assert got.source_evidence_ids == ["ev-1", "ev-2"]


def test_one_row_per_ticker_upsert_updates(db):
    db.upsert_thesis(_rec(thesis="first"))
    db.upsert_thesis(_rec(thesis="second"))
    rows = db.list_thesis()
    assert len(rows) == 1
    assert rows[0].thesis == "second"


# ── computed view ────────────────────────────────────────────────────────────

def test_computed_view_ok_with_market_data(db):
    db.upsert_thesis(_rec())
    db.upsert_market_data(MarketDataRecord(ticker="AAPL", current_price=200.0))
    c = db.get_computed("AAPL")
    assert c.probability_check == "OK"
    assert c.probability_weighted_price == pytest.approx(237.5)
    assert c.upside_to_current == pytest.approx(0.1875)
    assert c.current_price == pytest.approx(200.0)


def test_computed_view_missing_without_market_data(db):
    db.upsert_thesis(_rec(p_bear=None))
    c = db.get_computed("AAPL")
    assert c.probability_check == "MISSING"
    assert c.probability_weighted_price is None
    assert c.current_price is None
    assert c.upside_to_current is None


def test_computed_view_flags_off_sum(db):
    db.upsert_thesis(_rec(p_bull=0.30))
    db.upsert_market_data(MarketDataRecord(ticker="AAPL", current_price=200.0))
    c = db.get_computed("AAPL")
    assert c.probability_check == "CHECK"
    assert c.probability_weighted_price is None


def test_view_matches_python_definition(db):
    """The SQL view and ComputedThesisTrackerRecord.from_record must agree."""
    rec = _rec()
    db.upsert_thesis(rec)
    db.upsert_market_data(MarketDataRecord(ticker="AAPL", current_price=211.3))
    from_db = db.get_computed("AAPL")
    from_py = ComputedThesisTrackerRecord.from_record(rec, current_price=211.3)
    assert from_db.probability_check == from_py.probability_check
    assert from_db.probability_sum == pytest.approx(from_py.probability_sum)
    assert from_db.probability_weighted_price == pytest.approx(
        from_py.probability_weighted_price
    )
    assert from_db.upside_to_current == pytest.approx(from_py.upside_to_current)


def test_list_computed_returns_all(db):
    db.upsert_thesis(_rec(ticker="AAPL"))
    db.upsert_thesis(_rec(ticker="MSFT"))
    rows = db.list_computed()
    assert {r.ticker for r in rows} == {"AAPL", "MSFT"}


def test_get_missing_ticker_returns_none(db):
    assert db.get_thesis("NOPE") is None
    assert db.get_computed("NOPE") is None
