"""Tests for engine.outcomes — the process-backtest record (contract only)."""
from __future__ import annotations

import pytest

from engine.outcomes import (
    ThemeOutcomeRecord,
    append_outcome,
    read_outcomes,
)

def _rec(theme_id="t1", realized=None):
    return ThemeOutcomeRecord(
        theme_id=theme_id,
        p=[0.4, 0.35, 0.15, 0.1],
        q=[0.13, 0.18, 0.33, 0.36],
        X_s=[95.0, 75.0, 45.0, 40.0],
        X_mkt=55.0,
        predicted_edge=20.0,
        edge_std=1.5,
        realized_axis_at_horizon=realized,
    )

def test_record_defaults_realized_to_none():
    assert _rec().realized_axis_at_horizon is None

def test_append_then_read_roundtrips(tmp_path):
    path = tmp_path / "outcomes.jsonl"
    append_outcome(_rec("alpha"), path)
    records = read_outcomes(path)
    assert len(records) == 1
    r = records[0]
    assert r.theme_id == "alpha"
    assert r.predicted_edge == 20.0
    assert r.p == [0.4, 0.35, 0.15, 0.1]
    assert r.realized_axis_at_horizon is None

def test_append_is_additive(tmp_path):
    path = tmp_path / "outcomes.jsonl"
    append_outcome(_rec("a"), path)
    append_outcome(_rec("b", realized=72.0), path)
    records = read_outcomes(path)
    assert [r.theme_id for r in records] == ["a", "b"]
    assert records[1].realized_axis_at_horizon == 72.0

def test_each_record_is_one_json_line(tmp_path):
    path = tmp_path / "outcomes.jsonl"
    append_outcome(_rec("a"), path)
    append_outcome(_rec("b"), path)
    lines = path.read_text().strip().splitlines()
    assert len(lines) == 2

def test_calibration_analyses_are_documented_stubs():
    from engine.outcomes import calibration_report, edge_realization

    with pytest.raises(NotImplementedError):
        calibration_report([_rec()])
    with pytest.raises(NotImplementedError):
        edge_realization([_rec()])
