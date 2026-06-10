"""Thesis Tracker service layer (PART 4) + theme stub (PART 7): merge-on-upsert,
audit logging, close/delete discipline, exports, and the discovery link helper."""
from __future__ import annotations

from datetime import date
from types import SimpleNamespace

import pytest

from engine.schema.thesis_tracker import MarketDataRecord, ThesisTrackerRecord
from engine.thesis_tracker import (
    close_thesis,
    create_thesis_stub_from_theme,
    delete_thesis,
    export_thesis_tracker_json,
    export_thesis_tracker_markdown,
    get_thesis,
    init_thesis_db,
    list_theses,
    upsert_market_data,
    upsert_thesis,
)


@pytest.fixture
def dbp(tmp_path):
    p = tmp_path / "tt.sqlite"
    init_thesis_db(p)
    return p


# ── upsert: create + merge ───────────────────────────────────────────────────

def test_upsert_creates_then_get_returns_computed(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="aapl", thesis="AI cycle"))
    c = get_thesis(dbp, "AAPL")
    assert c is not None and c.thesis == "AI cycle"
    assert c.probability_check == "MISSING"  # computed view field present


def test_upsert_merges_only_explicit_fields(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(
        ticker="AAPL", thesis="orig", bull_case_price=300.0, weight_placeholder=0.05,
    ))
    # second upsert sets ONLY thesis — price + weight must be preserved
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL", thesis="revised"))
    c = get_thesis(dbp, "AAPL")
    assert c.thesis == "revised"
    assert c.bull_case_price == 300.0       # preserved, not wiped
    assert c.weight_placeholder == 0.05     # preserved


def test_upsert_keeps_stable_thesis_id_across_updates(dbp):
    tid1 = upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL", thesis="a"))
    tid2 = upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL", thesis="b"))
    assert tid1 == tid2


# ── audit log ────────────────────────────────────────────────────────────────

def test_create_and_update_are_audited(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL", thesis="a"), reason="seed")
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL", thesis="b"), reason="revise")
    from engine.thesis_tracker import ThesisTrackerDB
    with ThesisTrackerDB(dbp) as d:
        log = d.read_audit("AAPL")
    actions = [e["action"] for e in log]
    assert actions == ["create", "update"]
    assert log[0]["reason"] == "seed" and log[1]["reason"] == "revise"


# ── close (never deletes) ────────────────────────────────────────────────────

def test_close_sets_status_and_audits(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL", thesis="a"))
    close_thesis(dbp, "AAPL", reason="thesis played out")
    c = get_thesis(dbp, "AAPL")
    assert c.status == "closed"  # row still present
    from engine.thesis_tracker import ThesisTrackerDB
    with ThesisTrackerDB(dbp) as d:
        assert d.read_audit("AAPL")[-1]["action"] == "close"


def test_close_missing_raises(dbp):
    with pytest.raises(KeyError):
        close_thesis(dbp, "NOPE", reason="x")


# ── delete (never silent) ────────────────────────────────────────────────────

def test_delete_snapshots_before_removing(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL", thesis="a", bull_case_price=10.0))
    delete_thesis(dbp, "AAPL", reason="entered by mistake")
    assert get_thesis(dbp, "AAPL") is None  # row gone
    from engine.thesis_tracker import ThesisTrackerDB
    with ThesisTrackerDB(dbp) as d:
        last = d.read_audit("AAPL")[-1]
    assert last["action"] == "delete"
    assert last["reason"] == "entered by mistake"
    assert last["snapshot"] is not None  # recoverable from the log


# ── list with status filter ──────────────────────────────────────────────────

def test_list_filters_by_status(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL", status="active"))
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="MSFT", status="watchlist"))
    actives = list_theses(dbp, status="active")
    assert {r.ticker for r in actives} == {"AAPL"}
    assert len(list_theses(dbp)) == 2


# ── exports ──────────────────────────────────────────────────────────────────

def test_export_json_is_serialisable(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(
        ticker="AAPL", bull_case_price=300.0, base_case_price=250.0, bear_case_price=150.0,
        p_bull=0.25, p_base=0.5, p_bear=0.25, catalyst_date=date(2026, 7, 1),
    ))
    upsert_market_data(dbp, MarketDataRecord(ticker="AAPL", current_price=200.0))
    import json
    rows = export_thesis_tracker_json(dbp)
    assert json.dumps(rows)  # must be JSON-serialisable
    assert rows[0]["probability_check"] == "OK"
    assert rows[0]["probability_weighted_price"] == pytest.approx(237.5)


def test_export_markdown_has_header_and_row(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL"))
    md = export_thesis_tracker_markdown(dbp)
    assert "| Ticker |" in md
    assert "| AAPL |" in md


# ── PART 7: theme stub ───────────────────────────────────────────────────────

def _fake_theme():
    falsifier = SimpleNamespace(kill_rule="if spread < 50bps, dead", observable="x", threshold=50.0)
    return SimpleNamespace(
        id="theme-123",
        statement="AI capex outpaces revenue, funding gap widens.",
        provenance=SimpleNamespace(evidence=["src-a", "src-b"]),
        risk=SimpleNamespace(falsifiers=[falsifier]),
    )


def test_stub_copies_plain_english_and_links_no_invention(dbp):
    stub = create_thesis_stub_from_theme(_fake_theme(), ticker="nvda", weight_placeholder=0.03)
    assert stub.ticker == "NVDA"
    assert stub.thesis == "AI capex outpaces revenue, funding gap widens."
    assert stub.source_theme_id == "theme-123"
    assert stub.source_evidence_ids == ["src-a", "src-b"]
    assert stub.kill_criteria == "if spread < 50bps, dead"
    assert stub.weight_placeholder == 0.03  # only because passed explicitly
    # invents nothing priceable
    assert stub.bull_case_price is None and stub.base_case_price is None
    assert stub.p_bull is None and stub.p_base is None and stub.p_bear is None
    assert stub.status == "watchlist"


def test_stub_without_falsifiers_has_no_kill_criteria(dbp):
    theme = _fake_theme()
    theme.risk = SimpleNamespace(falsifiers=[])
    stub = create_thesis_stub_from_theme(theme, ticker="NVDA")
    assert stub.kill_criteria is None
    assert stub.weight_placeholder is None  # not passed -> not invented
