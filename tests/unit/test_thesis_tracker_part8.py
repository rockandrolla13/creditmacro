"""PART 8 acceptance tests — one test per enumerated requirement, traceable to the
spec. No external services, no Excel. (Items 19 'existing engine tests green' and 20
'golden-master unchanged' are verified by running the full suite, not here.)"""
from __future__ import annotations

import json
import sqlite3
from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest

from engine.schema.thesis_tracker import MarketDataRecord, ThesisTrackerRecord
from engine.thesis_tracker import (
    ThesisTrackerDB,
    close_thesis,
    create_thesis_stub_from_theme,
    delete_thesis,
    export_thesis_tracker_json,
    export_thesis_tracker_markdown,
    get_thesis,
    init_thesis_db,
    upsert_market_data,
    upsert_thesis,
)


@pytest.fixture
def dbp(tmp_path) -> Path:
    p = tmp_path / "tt.sqlite"
    init_thesis_db(p)
    return p


# 1. Migration creates database.
def test_01_migration_creates_database(tmp_path):
    p = tmp_path / "tt.sqlite"
    assert not p.exists()
    init_thesis_db(p)
    assert p.exists()


# 2. Tables/views exist.
def test_02_tables_and_view_exist(dbp):
    with ThesisTrackerDB(dbp) as d:
        names = {
            r["name"] for r in d.conn.execute(
                "SELECT name FROM sqlite_master WHERE type IN ('table','view')"
            )
        }
    assert {"market_data", "thesis_tracker", "thesis_audit_log", "thesis_tracker_view"} <= names


# 3. Market data upsert works.
def test_03_market_data_upsert(dbp):
    upsert_market_data(dbp, MarketDataRecord(ticker="AAPL", current_price=200.0))
    with ThesisTrackerDB(dbp) as d:
        assert d.get_market_data("AAPL").current_price == 200.0


# 4. Thesis upsert works.
def test_04_thesis_upsert(dbp):
    tid = upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL", thesis="t"))
    assert tid and get_thesis(dbp, "AAPL").thesis == "t"


# 5. Ticker is uppercased.
def test_05_ticker_uppercased(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="aapl"))
    assert get_thesis(dbp, "aapl").ticker == "AAPL"


# 6. Probabilities stored as decimals (40% -> 0.40, not 40).
def test_06_probabilities_stored_as_decimals(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL", p_bull=0.40, p_base=0.40, p_bear=0.20))
    c = get_thesis(dbp, "AAPL")
    assert c.p_bull == 0.40 and c.p_base == 0.40 and c.p_bear == 0.20


# 7. probability_check = OK when sum == 1.0.
def test_07_check_ok(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL", p_bull=0.25, p_base=0.50, p_bear=0.25))
    assert get_thesis(dbp, "AAPL").probability_check == "OK"


# 8. probability_check = CHECK when sum != 1.0.
def test_08_check_off_sum(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL", p_bull=0.30, p_base=0.50, p_bear=0.25))
    assert get_thesis(dbp, "AAPL").probability_check == "CHECK"


# 9. probability_check = MISSING when a probability is missing.
def test_09_check_missing(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL", p_bull=0.5, p_base=0.5))
    assert get_thesis(dbp, "AAPL").probability_check == "MISSING"


# 10. probability_weighted_price computes correctly.
def test_10_weighted_price(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(
        ticker="AAPL", bull_case_price=300.0, base_case_price=250.0, bear_case_price=150.0,
        p_bull=0.25, p_base=0.50, p_bear=0.25,
    ))
    # 300*.25 + 250*.5 + 150*.25 = 237.5
    assert get_thesis(dbp, "AAPL").probability_weighted_price == pytest.approx(237.5)


# 11. upside_to_current references market_data correctly.
def test_11_upside_references_market_data(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(
        ticker="AAPL", bull_case_price=300.0, base_case_price=250.0, bear_case_price=150.0,
        p_bull=0.25, p_base=0.50, p_bear=0.25,
    ))
    upsert_market_data(dbp, MarketDataRecord(ticker="AAPL", current_price=200.0))
    # 237.5 / 200 - 1 = 0.1875
    assert get_thesis(dbp, "AAPL").upside_to_current == pytest.approx(0.1875)


# 12. Missing current price leaves upside null.
def test_12_missing_current_price_null_upside(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(
        ticker="AAPL", bull_case_price=300.0, base_case_price=250.0, bear_case_price=150.0,
        p_bull=0.25, p_base=0.50, p_bear=0.25,
    ))
    c = get_thesis(dbp, "AAPL")
    assert c.current_price is None and c.upside_to_current is None


# 13. Incomplete thesis rows persist but are flagged.
def test_13_incomplete_rows_persist_flagged(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL"))
    c = get_thesis(dbp, "AAPL")
    assert c is not None
    assert c.probability_check == "MISSING"
    assert c.probability_weighted_price is None


# 14. Audit log records create/update/close/delete.
def test_14_audit_records_all_actions(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL", thesis="a"))   # create
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL", thesis="b"))   # update
    close_thesis(dbp, "AAPL", reason="done")                             # close
    delete_thesis(dbp, "AAPL", reason="cleanup")                         # delete
    with ThesisTrackerDB(dbp) as d:
        actions = [e["action"] for e in d.read_audit("AAPL")]
    assert actions == ["create", "update", "close", "delete"]


# 15. Export JSON works.
def test_15_export_json(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL"))
    rows = export_thesis_tracker_json(dbp)
    assert json.dumps(rows)  # serialisable
    assert rows[0]["ticker"] == "AAPL"


# 16. Export markdown works.
def test_16_export_markdown(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL"))
    md = export_thesis_tracker_markdown(dbp)
    assert "| Ticker |" in md and "| AAPL |" in md


# 17. No target prices or probabilities are inferred.
def test_17_no_inference_on_blank_row(dbp):
    upsert_thesis(dbp, ThesisTrackerRecord(ticker="AAPL", thesis="just words"))
    c = get_thesis(dbp, "AAPL")
    assert c.bull_case_price is None and c.base_case_price is None and c.bear_case_price is None
    assert c.p_bull is None and c.p_base is None and c.p_bear is None
    assert c.weight_placeholder is None


# 18. create_thesis_stub_from_theme does not invent prices or probabilities.
def test_18_stub_invents_nothing_priceable():
    theme = SimpleNamespace(
        id="theme-1",
        statement="plain english thesis",
        provenance=SimpleNamespace(evidence=["e1"]),
        risk=SimpleNamespace(falsifiers=[SimpleNamespace(kill_rule="dies if X")]),
    )
    stub = create_thesis_stub_from_theme(theme, ticker="AAPL")
    assert stub.thesis == "plain english thesis"
    assert stub.source_theme_id == "theme-1"
    assert stub.kill_criteria == "dies if X"
    assert stub.bull_case_price is None and stub.base_case_price is None and stub.bear_case_price is None
    assert stub.p_bull is None and stub.p_base is None and stub.p_bear is None
    assert stub.weight_placeholder is None


# Bonus: assert no external network/service dependency is importable-required.
def test_no_external_service_dependency():
    import engine.thesis_tracker as mod
    src = Path(mod.__file__).read_text()
    for forbidden in ("requests", "httpx", "openpyxl", "xlsxwriter", "boto3"):
        assert forbidden not in src
