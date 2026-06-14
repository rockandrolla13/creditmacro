"""S10 — closing a terminal watch: ThemeOutcomeRecord + CASE outcome page write-back.

Acceptance (plan §5.8 / §10 Q6): a terminal watch emits a ThemeOutcomeRecord (feeds the Phase-6
calibration corpus) and writes back as its own CASE outcome page; a non-terminal watch raises.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

from engine.outcomes import ThemeOutcomeRecord, append_outcome, read_outcomes
from engine.surveillance import (
    AxisState,
    FalsifierState,
    ForwardHorizon,
    ThemeWatch,
)
from engine.surveillance_agent import ThemeMonitorAgent, outcome_record_from_watch
from engine.wiki_integration import ClosedWatchPersistInput, persist_closed_watch

OPENED = date(2026, 1, 1)


def _on(d):
    return date.fromordinal(OPENED.toordinal() + d)


def _watch():
    return ThemeWatch(
        theme_id="ppi-cpi-producer-consumer", snapshot_hash="sha256:abc",
        forward_horizon=ForwardHorizon(opened=OPENED, expected_close=_on(91),
                                       window_label="3m", window_days=91),
        falsifier=FalsifierState(observable="ppi_minus_cpi", threshold=20.0, direction="below"),
        axis_state=AxisState(series="diff", current=80.0, entry_level=0.0, modeled_target=100.0),
        last_evidence_date=OPENED)


def _played_out_watch():
    w = _watch()
    ThemeMonitorAgent().read_falsifier(w, metric_value=25.0, now=_on(10))  # 80% => played_out
    assert w.status == "played_out"
    return w


def _outcome(w):
    return outcome_record_from_watch(w, p=[0.5, 0.5], q=[0.4, 0.6], X_s=[0.0, 100.0],
                                     X_mkt=80.0, predicted_edge=20.0, edge_std=5.0)


# ── outcome record ───────────────────────────────────────────────────────────────────

def test_non_terminal_watch_has_no_outcome():
    import pytest
    with pytest.raises(ValueError):
        _outcome(_watch())                       # status armed => raises


def test_terminal_watch_builds_outcome_record_with_realized_axis():
    rec = _outcome(_played_out_watch())
    assert isinstance(rec, ThemeOutcomeRecord)
    assert rec.theme_id == "ppi-cpi-producer-consumer"
    assert rec.realized_axis_at_horizon == 80.0   # current - entry


def test_outcome_record_round_trips_jsonl(tmp_path):
    rec = _outcome(_played_out_watch())
    path = tmp_path / "outcomes.jsonl"
    append_outcome(rec, path)
    back = read_outcomes(path)
    assert len(back) == 1 and back[0].realized_axis_at_horizon == 80.0


# ── CASE write-back ──────────────────────────────────────────────────────────────────

def test_closed_watch_writes_case_outcome_page(tmp_path):
    w = _played_out_watch()
    inp = ClosedWatchPersistInput(watch=w, terminal_reason="axis_target_reached",
                                  outcome=_outcome(w), wiki_root=str(tmp_path / "wiki"))
    res = persist_closed_watch(inp)
    assert res.applied
    page = list(Path(inp.wiki_root).glob("outcomes/closed-*.md"))
    assert len(page) == 1
    body = page[0].read_text()
    assert "access_class: case" in body
    assert "terminal_status: played_out" in body
    assert "outcome_check_required: true" in body
    assert "sha256:abc" in body                  # snapshot binding
    assert "## No-trade boundary" in body
    assert "NOT a current recommendation" in body


def test_closed_watch_idempotent(tmp_path):
    w = _played_out_watch()
    inp = ClosedWatchPersistInput(watch=w, terminal_reason="axis_target_reached",
                                  wiki_root=str(tmp_path / "wiki"))
    persist_closed_watch(inp)
    res2 = persist_closed_watch(inp)
    assert res2.skipped_paths and not res2.written_paths


def test_persist_non_terminal_watch_raises(tmp_path):
    import pytest
    with pytest.raises(ValueError):
        persist_closed_watch(ClosedWatchPersistInput(watch=_watch(),
                                                     wiki_root=str(tmp_path / "wiki")))
