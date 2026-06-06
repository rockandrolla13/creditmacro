"""Integration test: run the AI-issuance case through the generic runner and confirm
it reproduces the golden numbers and passes its own exact oracle."""
from __future__ import annotations

from pathlib import Path

import pytest

from engine.case_loader import load_case
from engine.cases import PolicyConfig
from engine.scripted_provider import ScriptedProvider
from engine.schema import ThemeObject
from engine.workflow import run_workflow

CASE = Path(__file__).resolve().parents[2] / "cases" / "ai_issuance.yaml"
ABS = 1e-6


def _run():
    case = load_case(CASE)
    provider = ScriptedProvider(case)
    theme, memo = run_workflow(provider, case.resolved_policy())
    return case, theme, memo


def test_workflow_returns_theme_and_memo():
    _, theme, memo = _run()
    assert isinstance(theme, ThemeObject)
    assert isinstance(memo, str) and memo.strip()


def test_workflow_reproduces_golden_pricing():
    _, theme, _ = _run()
    assert theme.pricing.scenario_fv == pytest.approx(75.0, abs=ABS)
    assert theme.pricing.priced_in.q_s == pytest.approx(
        [0.125512, 0.184417, 0.328452, 0.361619], abs=ABS
    )
    assert theme.pricing.residual_edge == pytest.approx(20.0, abs=ABS)
    assert theme.pricing.priced_in.frac == pytest.approx(-1.0, abs=ABS)


def test_workflow_reproduces_golden_scoring():
    _, theme, _ = _run()
    by_id = {e.id: e for e in theme.expressions}
    assert by_id["expr_cds_5s30s"].score == pytest.approx(3.918220233274124, abs=ABS)
    assert by_id["expr_etf_basis"].score is None
    assert by_id["expr_etf_basis"].gate_fail_reason == "λ 0.32 < minimum 0.40"


def test_workflow_carries_sizing_and_risk_from_case():
    _, theme, _ = _run()
    assert theme.sizing.vol_scalar == pytest.approx(1.25, abs=ABS)
    assert theme.sizing.net_target_pnl == pytest.approx(747000.0, abs=ABS)
    assert len(theme.risk.falsifiers) == 3


def test_workflow_theme_passes_its_exact_oracle():
    case, theme, _ = _run()
    results = case.oracle.check(theme)
    failed = [r for r in results if not r.passed]
    assert not failed, f"oracle failures: {failed}"
