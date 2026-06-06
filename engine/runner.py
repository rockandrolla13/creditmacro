"""
Generic, parametrized oracle RUNNER with an always-on invariants floor (Step 7).

Two layers, kept strictly separate (see docs/engine2_design.md §3.3 + §10 and
reviews/2026_06_06_architecture_review.md AR-ABS-001 / AR-EXT-001):

  1. The INVARIANTS FLOOR — `invariants_floor(theme)` — is asserted for EVERY case
     regardless of oracle kind. It is a pure function over a built ThemeObject.
  2. The case ORACLE — `case.oracle.check(theme)` — adds the kind-specific
     assertions. Dispatch is POLYMORPHIC via the discriminated union: there is NO
     `if kind == ...` switch anywhere in this module (that is the whole point of
     AR-ABS-001).

`run_case` ties it together: load → ScriptedProvider → run_workflow → floor +
oracle, returning the COMBINED `list[AssertionResult]` (floor first, oracle after).
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Union

from .case_loader import load_case
from .cases import AssertionResult, CaseSpec
from .schema import ThemeObject
from .scripted_provider import ScriptedProvider
from .workflow import run_workflow


# ── the always-on invariants floor ───────────────────────────────────────────

def _finite_or_none(value: float | None) -> bool:
    """A value is acceptable if it is None (not required here) or finite."""
    return value is None or math.isfinite(value)


def invariants_floor(theme: ThemeObject) -> list[AssertionResult]:
    """Assert the floor that holds for EVERY emitted ThemeObject, irrespective of
    oracle kind. Returns one AssertionResult per check, in a stable order."""
    results: list[AssertionResult] = []

    # 1. schema_valid — the ThemeObject exists / was constructed.
    results.append(AssertionResult(
        name="schema_valid",
        passed=isinstance(theme, ThemeObject),
        detail=f"type={type(theme).__name__}",
    ))

    # 2. gates_evaluate — the 4 discipline gates evaluate.
    axis = theme.axis
    pricing = theme.pricing
    gate1 = bool(axis.definition.strip()) and bool(axis.measurement.strip())
    gate2 = pricing.residual_edge is not None
    gate3 = any(e.score is not None for e in theme.expressions)
    gate4 = len(theme.risk.falsifiers) >= 1
    results.append(AssertionResult(
        name="gates_evaluate",
        passed=gate1 and gate2 and gate3 and gate4,
        detail=f"gate1={gate1} gate2={gate2} gate3={gate3} gate4={gate4}",
    ))

    # 3. edge_sign — the edge points in the thesis direction.
    results.append(AssertionResult(
        name="edge_sign",
        passed=pricing.edge_direction_ok is True,
        detail=f"edge_direction_ok={pricing.edge_direction_ok}",
    ))

    # 4. q_feasible — the max-entropy solver returned a feasible q.
    results.append(AssertionResult(
        name="q_feasible",
        passed=pricing.q_status == "FEASIBLE",
        detail=f"q_status={pricing.q_status}",
    ))

    # 5. finite — no NaN/inf where a finite value is required (None is skipped).
    finite_checks: list[tuple[str, float | None]] = [
        ("residual_edge", pricing.residual_edge),
        ("scenario_fv", pricing.scenario_fv),
        ("scenario_fv_std", pricing.scenario_fv_std),
    ]
    finite_checks.extend((f"q_s[{i}]", q) for i, q in enumerate(pricing.priced_in.q_s))
    bad = [name for name, value in finite_checks if not _finite_or_none(value)]
    results.append(AssertionResult(
        name="finite",
        passed=not bad,
        detail=("all finite" if not bad else f"non-finite: {bad}"),
    ))

    return results


# ── case discovery + the combined runner ──────────────────────────────────────

def discover_cases(cases_dir: Union[str, Path] = "cases") -> list[Path]:
    """Glob every *.yaml / *.yml case file, sorted. Dropping a new case file here
    makes the parametrized suite pick it up automatically."""
    base = Path(cases_dir)
    paths = list(base.glob("*.yaml")) + list(base.glob("*.yml"))
    return sorted(paths)


def run_case(path: Union[str, Path]) -> tuple[CaseSpec, ThemeObject, list[AssertionResult]]:
    """Load a case, run the workflow, and assert the floor + the oracle.

    Returns the case, the built theme, and the COMBINED results (floor first,
    then the polymorphic oracle's own assertions). Dispatch to the oracle is
    polymorphic — NO kind switch (AR-ABS-001)."""
    case = load_case(path)
    theme, _memo = run_workflow(ScriptedProvider(case), case.resolved_policy())

    results = invariants_floor(theme)
    results.extend(case.oracle.check(theme))  # polymorphic dispatch — no kind switch
    return case, theme, results
