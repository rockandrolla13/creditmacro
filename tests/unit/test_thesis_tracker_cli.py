"""Thesis Tracker CLI (PART 5/6) — init, upsert-market, upsert-thesis (args or
JSON/YAML), list, show, export-json, export-md. It persists only what the operator
provides; it never infers prices or probabilities, and hides notes unless --verbose."""
from __future__ import annotations

import json

from engine.thesis_tracker import get_thesis
from tools.thesis_tracker_cli import main


def _init(tmp_path):
    db = str(tmp_path / "tt.sqlite")
    assert main(["init", "--db", db]) == 0
    return db


# ── init + upsert via args ───────────────────────────────────────────────────

def test_init_then_upsert_args_persists(tmp_path):
    db = _init(tmp_path)
    rc = main(["upsert-thesis", "--db", db, "--ticker", "aapl", "--thesis", "AI cycle"])
    assert rc == 0
    assert get_thesis(db, "AAPL").thesis == "AI cycle"


def test_show_reports_ok_and_weighted_price(tmp_path, capsys):
    db = _init(tmp_path)
    main(["upsert-thesis", "--db", db, "--ticker", "AAPL",
          "--bull", "300", "--base", "250", "--bear", "150",
          "--pbull", "0.25", "--pbase", "0.5", "--pbear", "0.25"])
    main(["upsert-market", "--db", db, "--ticker", "AAPL", "--current-price", "200"])
    capsys.readouterr()
    assert main(["show", "--db", db, "--ticker", "AAPL"]) == 0
    out = capsys.readouterr().out
    assert "OK" in out and "237.5" in out


def test_invalid_probability_nonzero_exit_persists_nothing(tmp_path):
    db = _init(tmp_path)
    rc = main(["upsert-thesis", "--db", db, "--ticker", "AAPL", "--pbull", "1.5"])
    assert rc != 0
    assert get_thesis(db, "AAPL") is None


# ── PART 6: JSON / YAML ingestion ────────────────────────────────────────────

def test_upsert_from_json_single(tmp_path):
    db = _init(tmp_path)
    f = tmp_path / "one.json"
    f.write_text(json.dumps({
        "ticker": "ABC", "weight_placeholder": 0.05, "thesis": "t",
        "bull_case_price": 150, "base_case_price": 110, "bear_case_price": 70,
        "p_bull": 0.25, "p_base": 0.50, "p_bear": 0.25,
        "catalyst_date": "2026-07-30",
    }))
    assert main(["upsert-thesis", "--db", db, "--json", str(f)]) == 0
    c = get_thesis(db, "ABC")
    assert c.probability_check == "OK"
    assert str(c.catalyst_date) == "2026-07-30"


def test_upsert_from_json_bulk_rows(tmp_path):
    db = _init(tmp_path)
    f = tmp_path / "bulk.json"
    f.write_text(json.dumps({"rows": [{"ticker": "AAA"}, {"ticker": "BBB"}]}))
    assert main(["upsert-thesis", "--db", db, "--json", str(f)]) == 0
    assert get_thesis(db, "AAA") is not None and get_thesis(db, "BBB") is not None


def test_upsert_from_yaml(tmp_path):
    db = _init(tmp_path)
    f = tmp_path / "one.yaml"
    f.write_text("ticker: YML\nthesis: from yaml\n")
    assert main(["upsert-thesis", "--db", db, "--json", str(f)]) == 0
    assert get_thesis(db, "YML").thesis == "from yaml"


# ── list / export ────────────────────────────────────────────────────────────

def test_list_shows_columns(tmp_path, capsys):
    db = _init(tmp_path)
    main(["upsert-thesis", "--db", db, "--ticker", "AAPL"])
    main(["upsert-thesis", "--db", db, "--ticker", "MSFT"])
    capsys.readouterr()
    main(["list", "--db", db])
    out = capsys.readouterr().out
    assert "AAPL" in out and "MSFT" in out and "Check" in out


def test_export_json_and_md(tmp_path, capsys):
    db = _init(tmp_path)
    main(["upsert-thesis", "--db", db, "--ticker", "AAPL"])
    capsys.readouterr()
    main(["export-json", "--db", db])
    js = capsys.readouterr().out
    assert json.loads(js)[0]["ticker"] == "AAPL"
    main(["export-md", "--db", db])
    md = capsys.readouterr().out
    assert "| Ticker |" in md and "| AAPL |" in md


# ── notes privacy: hidden unless --verbose ───────────────────────────────────

def test_show_hides_notes_unless_verbose(tmp_path, capsys):
    db = _init(tmp_path)
    main(["upsert-thesis", "--db", db, "--ticker", "AAPL", "--notes", "SECRET-NOTE"])
    capsys.readouterr()
    main(["show", "--db", db, "--ticker", "AAPL"])
    assert "SECRET-NOTE" not in capsys.readouterr().out
    main(["show", "--db", db, "--ticker", "AAPL", "--verbose"])
    assert "SECRET-NOTE" in capsys.readouterr().out
