"""TRAP stage — Feedback/Leverage/System-Trap detector wired after SYSTEM_MAP, before
pricing. Consumes the system map's loop map; records its diagnosis on the ThemeObject."""
from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from engine.case_loader import load_case
from engine.schema import LeveragePoint, TrapDetection
from engine.scripted_provider import ScriptedProvider
from engine.workflow import run_workflow

CASES = Path(__file__).resolve().parents[2] / "cases"


# ── schema ───────────────────────────────────────────────────────────────────

def test_trap_detection_decision_is_constrained():
    td = TrapDetection(dominant_loop_now="R1", possible_loop_shift="inflows turn",
                       decision="watchlist")
    assert td.decision == "watchlist"
    with pytest.raises(ValidationError):
        TrapDetection(dominant_loop_now="R1", possible_loop_shift="x", decision="buy")


def test_leverage_point_tags_observable_vs_structural():
    lp = LeveragePoint(description="net fund flows", observable=True)
    assert lp.observable is True


# ── stage wiring ─────────────────────────────────────────────────────────────

def _trap():
    return TrapDetection(
        dominant_loop_now="B1 (balancing) — support-withdrawal currently widening",
        dominant_loop_evidence="differential off its historical low",
        possible_loop_shift="a bailout flips B1->R1, snapping the differential tighter",
        system_traps=["success-to-the-successful if the trade crowds"],
        leverage_points=[LeveragePoint(description="state-aid commitments", observable=True)],
        early_warning_indicators=["state-aid announcements", "differential compressing off lows"],
        scenario_implications=["worst/no-support state drives the widening edge"],
        expression_risk_implications=["long-the-differential dies first on a bailout"],
        invalidation_evidence=["differential < 20bps for two months"],
        pm_questions=["is the edge net of risk premium?"],
        decision="promote_to_scenario_pricing",
    )


def _run(path, attach_trap=False):
    case = load_case(path)
    if attach_trap:
        case = case.model_copy(update={"trap_detection": _trap()})
    theme, _ = run_workflow(ScriptedProvider(case), case.resolved_policy())
    return case, theme


def test_scripted_provider_returns_none_without_payload():
    case = load_case(CASES / "ai_issuance.yaml")
    assert ScriptedProvider(case).detect_traps(None) is None


def test_workflow_attaches_trap_detection_when_present():
    _, theme = _run(CASES / "french_banks.yaml", attach_trap=True)
    assert isinstance(theme.trap_detection, TrapDetection)
    assert theme.trap_detection.decision in (
        "promote_to_scenario_pricing", "watchlist", "reject", "needs_more_data")
    assert theme.trap_detection.possible_loop_shift


def test_ai_issuance_has_no_trap_stage_and_stays_golden():
    _, theme = _run(CASES / "ai_issuance.yaml")
    assert theme.trap_detection is None
    assert theme.pricing.residual_edge == pytest.approx(20.0, abs=1e-6)


# ── generic over cases that carry a trap_detection payload as DATA ───────────

ALL = sorted(CASES.glob("*.yaml"))
TRAP_CASES = [p for p in ALL if load_case(p).trap_detection is not None]


def test_at_least_one_case_carries_a_trap_payload():
    assert TRAP_CASES, "expected >=1 case carrying a trap_detection (e.g. french_banks)"


@pytest.mark.parametrize("path", TRAP_CASES, ids=lambda p: p.stem)
def test_loaded_trap_detection_attaches_and_consumes_loop_map(path):
    case = load_case(path)
    theme, _ = run_workflow(ScriptedProvider(case), case.resolved_policy())
    td = theme.trap_detection
    assert isinstance(td, TrapDetection)
    assert td.dominant_loop_now and td.possible_loop_shift
    # consumes the system map's loops (does not re-derive): references a mapped loop id
    if theme.system_map is not None:
        loop_ids = {fl.id for fl in theme.system_map.feedback_loops}
        assert any(lid in td.dominant_loop_now for lid in loop_ids)
