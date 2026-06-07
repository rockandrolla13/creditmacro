"""SYSTEM_MAP + CRITIQUE stages wired into run_workflow (after EXPAND_CAUSAL).

A case carrying system_map / bias_critique payloads gets them attached to the
ThemeObject; a case without them runs the existing path unchanged (golden master).
"""
from __future__ import annotations

from pathlib import Path

import pytest

from engine.case_loader import load_case
from engine.schema import (
    BiasCritique,
    Delay,
    FeedbackLoop,
    Flow,
    Stock,
    SystemMap,
)
from engine.scripted_provider import ScriptedProvider
from engine.workflow import run_workflow

CASES = Path(__file__).resolve().parents[2] / "cases"


def _payloads_for(case):
    chain = case.causal.causal_chain  # reuse the case's own chain nodes/edges
    sm = SystemMap(
        boundary_inside=[n.id for n in chain.nodes],
        boundary_outside=["policy / sovereign-crisis backdrop"],
        boundary_rationale="loops close where support policy feeds the differential",
        function_purpose="price declining sovereign support for banks",
        elements=list(chain.nodes),
        interconnections=list(chain.edges),
        stocks=[Stock(name="sovereign support capacity", unit="EUR bn")],
        flows=[Flow(name="state-aid commitments", changes_stock="sovereign support capacity",
                    unit_per_time="EUR bn/qtr")],
        feedback_loops=[FeedbackLoop(id="B1", type="balancing",
                                     path=["n_diff", "n_support"],
                                     closes_via="a wide differential pressures intervention")],
        delays=[Delay(between="support withdrawal and spread response", length="quarters",
                      why_it_matters="price lags the policy shift")],
        external_shocks=["EU bank state-aid surprise"],
        internal_responses=["differential re-prices"],
        observable_variables=["FR-banks − France senior CDS differential (bps)"],
        surprise_modes=["a sudden bailout snaps the differential tighter"],
    )
    bc = BiasCritique(
        dominant_mental_model="sovereign always backstops systemic banks",
        alternative_models=["support is being withdrawn (the thesis)", "risk premium already fair"],
        assumptions_treated_as_facts=["the differential mean-reverts to its historical low"],
        lenses_examined=["fundamental", "positioning", "cross-asset", "time-horizon", "failure-mode"],
        disconfirming_evidence=["differential compresses below 20bps", "fresh state-aid > EUR 50bn"],
        decision="accept_model",
        rationale="declining support is structurally supported; edge net of risk premium",
    )
    return sm, bc


def _run(path, attach=False):
    case = load_case(path)
    if attach and case.causal is not None:
        sm, bc = _payloads_for(case)
        case = case.model_copy(update={"system_map": sm, "bias_critique": bc})
    theme, _ = run_workflow(ScriptedProvider(case), case.resolved_policy(), mode="expression")
    return case, theme


def test_scripted_provider_returns_none_without_payloads():
    case = load_case(CASES / "ai_issuance.yaml")
    prov = ScriptedProvider(case)
    assert prov.build_system_map(None, None) is None
    assert prov.critique_mental_model("s", None) is None


def test_workflow_attaches_system_map_and_critique_when_present():
    _, theme = _run(CASES / "french_banks.yaml", attach=True)
    assert isinstance(theme.system_map, SystemMap)
    assert theme.system_map.function_purpose
    assert theme.system_map.elements  # reused chain nodes
    assert isinstance(theme.bias_critique, BiasCritique)
    assert theme.bias_critique.decision in ("accept_model", "challenge_model", "reject_model")


def test_system_map_distinguishes_stock_from_flow():
    _, theme = _run(CASES / "french_banks.yaml", attach=True)
    assert theme.system_map.stocks and theme.system_map.flows
    assert any(fl.type == "balancing" for fl in theme.system_map.feedback_loops)


def test_ai_issuance_has_no_system_stages_and_stays_golden():
    _, theme = _run(CASES / "ai_issuance.yaml")
    assert theme.system_map is None
    assert theme.bias_critique is None
    assert theme.pricing.residual_edge == pytest.approx(20.0, abs=1e-6)


# ── generic over any case that carries the payloads as DATA (e.g. french_banks.yaml) ──

ALL_CASES = sorted(CASES.glob("*.yaml"))
MAP_CASES = [p for p in ALL_CASES if load_case(p).system_map is not None]


def test_at_least_one_case_carries_a_system_map_payload():
    assert MAP_CASES, "expected >=1 case carrying a system_map (e.g. french_banks)"


@pytest.mark.parametrize("path", MAP_CASES, ids=lambda p: p.stem)
def test_loaded_system_map_attaches_and_is_well_formed(path):
    case = load_case(path)
    theme, _ = run_workflow(ScriptedProvider(case), case.resolved_policy(), mode="expression")
    sm = theme.system_map
    assert isinstance(sm, SystemMap) and sm.function_purpose
    assert sm.stocks and sm.flows                       # stock vs flow both present, distinct
    assert all(fl.type in ("reinforcing", "balancing") for fl in sm.feedback_loops)
    assert any(fl.type == "balancing" for fl in sm.feedback_loops)
    # elements reuse the causal chain's nodes (embedded, not re-derived)
    chain_ids = {n.id for n in theme.causal_chain.nodes}
    assert {e.id for e in sm.elements} & chain_ids
    if theme.bias_critique is not None:
        assert theme.bias_critique.decision in ("accept_model", "challenge_model", "reject_model")
        assert len(theme.bias_critique.lenses_examined) >= 5
