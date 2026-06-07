"""TRAP split into two stages, fixing the backward dependency:

  LOOP_DIAGNOSIS  (pre-pricing)  — loops/dominant/shift/traps/decision; FEEDS propose_scenarios
                                   (the balancing limit becomes a reversal scenario).
  TRAP_IMPLICATIONS (post-pricing) — scenario_implications + expression_risk, which need the
                                   scenarios/pricing/expressions that only exist after pricing.
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from engine.case_loader import load_case
from engine.schema import LeveragePoint, LoopDiagnosis, TrapImplications
from engine.scripted_provider import ScriptedProvider
from engine.workflow import run_workflow
from tests._helpers import CASES_DIR as CASES, build_theme


# ── schema split ──────────────────────────────────────────────────────────────

def test_loop_diagnosis_is_pre_pricing_only():
    ld = LoopDiagnosis(dominant_loop_now="R1", possible_loop_shift="inflows turn",
                       decision="promote_to_scenario_pricing")
    # the pre-pricing object must NOT carry post-pricing fields
    assert not hasattr(ld, "scenario_implications")
    assert not hasattr(ld, "expression_risk_implications")
    with pytest.raises(ValidationError):
        LoopDiagnosis(dominant_loop_now="R1", possible_loop_shift="x", decision="buy")


def test_trap_implications_is_post_pricing_only():
    ti = TrapImplications(scenario_implications=["worst state drives edge"],
                          expression_risk_implications=["long-beta dies first"])
    assert ti.scenario_implications and ti.expression_risk_implications
    assert not hasattr(ti, "dominant_loop_now")


def test_leverage_point_observable_flag():
    assert LeveragePoint(description="flows", observable=True).observable is True


# ── ordering: loop diagnosis FEEDS propose_scenarios (no backward dependency) ──

class _SpyProvider(ScriptedProvider):
    """Records what propose_scenarios and assess_trap_implications received."""
    def __init__(self, case):
        super().__init__(case)
        self.scenarios_got_loop = None
        self.implications_got = None

    def propose_scenarios(self, thesis, axis, loop_diagnosis=None):
        self.scenarios_got_loop = loop_diagnosis
        return super().propose_scenarios(thesis, axis, loop_diagnosis)

    def assess_trap_implications(self, scenarios, pricing, expressions):
        self.implications_got = (scenarios, pricing, expressions)
        return super().assess_trap_implications(scenarios, pricing, expressions)


def test_loop_diagnosis_is_passed_into_propose_scenarios():
    case = load_case(CASES / "french_banks.yaml")
    spy = _SpyProvider(case)
    run_workflow(spy, case.resolved_policy(), mode="expression")
    # the pre-pricing loop diagnosis reached scenario construction
    assert isinstance(spy.scenarios_got_loop, LoopDiagnosis)


def test_trap_implications_run_after_pricing_with_real_scenarios():
    case = load_case(CASES / "french_banks.yaml")
    spy = _SpyProvider(case)
    run_workflow(spy, case.resolved_policy(), mode="expression")
    scenarios, pricing, expressions = spy.implications_got
    assert scenarios and pricing is not None and expressions  # post-pricing inputs exist


# ── attachment + golden ───────────────────────────────────────────────────────

def test_workflow_attaches_both_loop_and_implications():
    _, theme, _ = build_theme("french_banks.yaml")
    assert isinstance(theme.loop_diagnosis, LoopDiagnosis)
    assert theme.loop_diagnosis.decision in (
        "promote_to_scenario_pricing", "watchlist", "reject", "needs_more_data")
    assert isinstance(theme.trap_implications, TrapImplications)
    assert theme.trap_implications.scenario_implications


def test_ai_issuance_has_neither_and_stays_golden():
    _, theme, _ = build_theme("ai_issuance.yaml")
    assert theme.loop_diagnosis is None
    assert theme.trap_implications is None
    assert theme.pricing.residual_edge == pytest.approx(20.0, abs=1e-6)
