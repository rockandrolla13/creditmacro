"""Shared test helpers — DRY: one place for case-loading, the workflow run, golden
constants, and the oracle-pass assertion. Import directly: `from tests._helpers import ...`."""
from __future__ import annotations

from pathlib import Path

from engine.case_loader import load_case
from engine.scripted_provider import ScriptedProvider
from engine.workflow import run_workflow

CASES_DIR = Path(__file__).resolve().parent.parent / "cases"

# Golden-master constants (AI-issuance), centralized so they live in exactly one file.
GOLDEN_Q = [0.125512, 0.184417, 0.328452, 0.361619]
GOLDEN_SCENARIO_FV = 75.0
GOLDEN_EDGE = 20.0
GOLDEN_OMEGA = 7.666666666666667
GOLDEN_SCORE = 3.918220233274124
ABS = 1e-6


def build_theme(case_ref, mode: str = "expression"):
    """load_case → ScriptedProvider → run_workflow. `case_ref` is a Path or a name relative
    to cases/ (may include a subdir, e.g. 'discovery/jpm_ai_capex.yaml'). Returns
    (case, theme, memo)."""
    path = case_ref if isinstance(case_ref, Path) else CASES_DIR / case_ref
    case = load_case(path)
    theme, memo = run_workflow(ScriptedProvider(case), case.resolved_policy(), mode=mode)
    return case, theme, memo


def assert_oracle_passes(case, theme) -> None:
    """Assert the case oracle reports no failures against the built theme."""
    failed = [r for r in case.oracle.check(theme) if not r.passed]
    assert not failed, f"oracle failures: {failed}"
