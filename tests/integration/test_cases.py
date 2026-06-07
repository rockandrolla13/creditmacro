"""Generic, parametrized oracle runner — Step 7."""
from __future__ import annotations

from pathlib import Path

import pytest

from engine.case_loader import load_case
from engine.runner import (
    discover_cases,
    invariants_floor,
    run_case,
)
from engine.schema import ThemeObject
from engine.scripted_provider import ScriptedProvider
from engine.workflow import run_workflow
from tests._helpers import build_theme

FLOOR_NAMES = {
    "schema_valid",
    "gates_evaluate",
    "edge_sign",
    "q_feasible",
    "finite",
}
EXACT_ORACLE_NAMES = {
    "scenario_fv",
    "q",
    "edge",
    "omega",
    "score",
    "gated_out",
}

CASES = discover_cases()

# ── parametrized over every discovered case ──────────────────────────────────

@pytest.mark.parametrize("path", CASES, ids=lambda p: p.stem)
def test_case_builds_theme(path: Path):
    case, theme, _ = build_theme(path)
    assert isinstance(theme, ThemeObject)

@pytest.mark.parametrize("path", CASES, ids=lambda p: p.stem)
def test_case_invariants_floor_all_pass(path: Path):
    case, theme, _ = build_theme(path)
    results = invariants_floor(theme)
    assert {r.name for r in results} == FLOOR_NAMES
    failed = [r for r in results if not r.passed]
    assert not failed, f"floor failures for {path.stem}: {failed}"

@pytest.mark.parametrize("path", CASES, ids=lambda p: p.stem)
def test_case_oracle_all_pass(path: Path):
    case, theme, _ = build_theme(path)
    results = case.oracle.check(theme)
    failed = [r for r in results if not r.passed]
    assert not failed, f"oracle failures for {path.stem}: {failed}"

@pytest.mark.parametrize("path", CASES, ids=lambda p: p.stem)
def test_run_case_combines_floor_and_oracle(path: Path):
    case, theme, results = run_case(path)
    assert isinstance(theme, ThemeObject)
    # the combined results contain every floor name
    names = {r.name for r in results}
    assert FLOOR_NAMES <= names
    failed = [r for r in results if not r.passed]
    assert not failed, f"combined failures for {path.stem}: {failed}"

# ── focused tests ────────────────────────────────────────────────────────────

def test_both_known_cases_are_discovered():
    stems = {p.stem for p in discover_cases()}
    assert {"ai_issuance", "french_banks"} <= stems
    assert len(discover_cases()) >= 2

def test_discover_cases_is_sorted():
    paths = discover_cases()
    assert paths == sorted(paths)

def _ai_case_path() -> Path:
    return next(p for p in discover_cases() if p.stem == "ai_issuance")

def test_floor_catches_broken_theme():
    """Prove the floor CATCHES violations — not a rubber stamp."""
    case = load_case(_ai_case_path())
    theme, _ = run_workflow(ScriptedProvider(case), case.resolved_policy(), mode="expression")

    broken_pricing = theme.pricing.model_copy(update={"edge_direction_ok": False})
    broken = theme.model_copy(update={"pricing": broken_pricing})

    results = invariants_floor(broken)
    by_name = {r.name: r for r in results}
    assert by_name["edge_sign"].passed is False
    # the rest of the floor still evaluates
    assert by_name["q_feasible"].passed is True

def test_floor_catches_non_feasible_q():
    case = load_case(_ai_case_path())
    theme, _ = run_workflow(ScriptedProvider(case), case.resolved_policy(), mode="expression")

    broken_pricing = theme.pricing.model_copy(update={"q_status": "INFEASIBLE"})
    broken = theme.model_copy(update={"pricing": broken_pricing})

    by_name = {r.name: r for r in invariants_floor(broken)}
    assert by_name["q_feasible"].passed is False

def test_floor_catches_non_finite():
    case = load_case(_ai_case_path())
    theme, _ = run_workflow(ScriptedProvider(case), case.resolved_policy(), mode="expression")

    broken_pricing = theme.pricing.model_copy(update={"residual_edge": float("nan")})
    broken = theme.model_copy(update={"pricing": broken_pricing})

    by_name = {r.name: r for r in invariants_floor(broken)}
    assert by_name["finite"].passed is False

def test_run_case_dispatches_via_polymorphic_check():
    """An exact case must yield the exact-oracle assertion names PLUS the floor"""
    case, theme, results = run_case(_ai_case_path())
    names = {r.name for r in results}
    assert FLOOR_NAMES <= names
    assert EXACT_ORACLE_NAMES <= names
