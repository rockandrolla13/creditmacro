"""French-banks reconstruction (Alaph deck) as a second golden master — an
`acceptance` oracle run through the generic runner."""
from __future__ import annotations

from pathlib import Path

import pytest

from engine.case_loader import load_case
from engine.scripted_provider import ScriptedProvider
from engine.schema import ThemeObject
from engine.workflow import run_workflow

CASE = Path(__file__).resolve().parents[2] / "cases" / "french_banks.yaml"


def _run():
    case = load_case(CASE)
    theme, memo = run_workflow(ScriptedProvider(case), case.resolved_policy())
    return case, theme, memo


def test_builds_a_theme_object():
    _, theme, _ = _run()
    assert isinstance(theme, ThemeObject)


def test_prior_is_historical_and_q_is_feasible():
    case, theme, _ = _run()
    # prior resolved from historical frequencies, summing to 1
    assert sum(case.prior) == pytest.approx(1.0, abs=1e-9)
    assert theme.pricing.q_status == "FEASIBLE"
    assert sum(theme.pricing.priced_in.q_s) == pytest.approx(1.0, abs=1e-6)


def test_edge_is_thesis_aligned_widening():
    _, theme, _ = _run()
    assert theme.pricing.residual_edge > 0          # widening direction
    assert theme.pricing.edge_direction_ok is True


def test_edge_comes_from_underweighted_no_support_state():
    _, theme, _ = _run()
    assert theme.pricing.edge_attribution[0].scenario == "Worst / no support"


def test_base_worst_ratio_matches_deck_1p9():
    _, theme, _ = _run()
    best = max((e for e in theme.expressions if e.score is not None), key=lambda e: e.score)
    pnls = [p.pnl for p in best.scenario_pnl]
    base_idx = max(range(len(theme.scenarios)), key=lambda i: theme.scenarios[i].p_s)
    ratio = pnls[base_idx] / abs(min(pnls))
    assert ratio == pytest.approx(1.9, abs=0.25)


def test_acceptance_oracle_passes():
    case, theme, _ = _run()
    results = case.oracle.check(theme)
    failed = [r for r in results if not r.passed]
    assert not failed, f"oracle failures: {failed}"


def test_all_four_discipline_gates_evaluate():
    _, theme, _ = _run()
    assert theme.axis.definition.strip() and theme.axis.measurement.strip()  # gate 1
    assert theme.pricing.residual_edge is not None                            # gate 2
    assert any(e.score is not None for e in theme.expressions)                # gate 3
    assert len(theme.risk.falsifiers) >= 1                                    # gate 4
