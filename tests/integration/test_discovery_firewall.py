"""Integration tests for the DISCOVERY FIREWALL."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine.case_loader import load_case
from engine.scripted_provider import ScriptedProvider
from engine.schema import StrategyFamilyRec, ThemeObject
from engine.workflow import run_workflow
from tests._helpers import CASES_DIR, build_theme

AI_ISSUANCE = CASES_DIR / "ai_issuance.yaml"
FRENCH_BANKS = CASES_DIR / "french_banks.yaml"
JPM_DISCOVERY = CASES_DIR / "discovery" / "jpm_ai_capex.yaml"
ABS = 1e-6

def _discover(path: Path):
    _, theme, memo = build_theme(path, "discovery")
    return theme, memo

def _express(path: Path):
    _, theme, memo = build_theme(path, "expression")
    return theme, memo

# ── run_workflow defaults to DISCOVERY (the firewalled path) ──────────────────

def test_run_workflow_defaults_to_discovery_mode():
    # No mode argument ⇒ discovery. A causal case routes to families and STOPS; it does
    # NOT price (no pricing leak from the default path).
    case = load_case(JPM_DISCOVERY)
    theme, _ = run_workflow(ScriptedProvider(case), case.resolved_policy())
    assert theme.status == "strategy_family_routed"
    assert theme.pricing is None
    assert theme.strategy_families

def test_default_discovery_blocks_a_causal_less_case():
    # ai_issuance carries no causal payload ⇒ the default (discovery) path HALTs blocked,
    # rather than silently pricing a trade.
    case = load_case(AI_ISSUANCE)
    theme, _ = run_workflow(ScriptedProvider(case), case.resolved_policy())
    assert theme.status == "blocked"
    assert theme.block_reason == "needs_causal_object"

# ── C1 regression: no causal object ⇒ status=blocked, no pricing leak ─────────

def test_discovery_without_causal_object_is_blocked():
    theme, _memo = _discover(AI_ISSUANCE)  # ai_issuance carries NO causal payload
    assert theme.status == "blocked"
    assert theme.block_reason == "needs_causal_object"

def test_blocked_object_leaks_no_pricing_or_families():
    theme, _ = _discover(AI_ISSUANCE)
    assert theme.pricing is None
    assert not theme.expressions
    assert not theme.strategy_families
    assert theme.sizing is None
    # no axis is manufactured from the thesis sentence (no fallback)
    assert theme.axis is None

# ── discovery_complete shape: families present, detailed legs absent ──────────

def test_jpm_discovery_emits_ranked_families_not_trade_ready():
    theme, _memo = _discover(JPM_DISCOVERY)
    assert isinstance(theme, ThemeObject)
    assert theme.status == "strategy_family_routed"
    # ranked families present, each a StrategyFamilyRec with a confidence
    assert theme.strategy_families
    assert all(isinstance(f, StrategyFamilyRec) for f in theme.strategy_families)
    confs = [f.confidence for f in theme.strategy_families]
    assert confs == sorted(confs, reverse=True)
    # NOT auto trade-ready: no sizing, no scored detailed expressions
    assert theme.sizing is None
    assert not theme.expressions

def test_jpm_curve_axis_yields_steepener_top_family():
    theme, _ = _discover(JPM_DISCOVERY)
    assert theme.strategy_families[0].family == "steepener"

def test_routed_object_serializes_with_sizing_and_expressions_null():
    theme, _ = _discover(JPM_DISCOVERY)
    blob = json.loads(theme.model_dump_json())
    assert blob["status"] == "strategy_family_routed"
    assert blob["block_reason"] is None
    assert blob["sizing"] is None
    assert blob["expressions"] == []
    assert blob["strategy_families"], "families must serialize on a routed object"

def test_french_banks_discovery_selects_long_short_top():
    theme, _ = _discover(FRENCH_BANKS)
    assert theme.status == "strategy_family_routed"
    assert theme.strategy_families[0].family == "long_short"

# ── expression mode keeps golden master AND now emits families ────────────────

def test_discovery_without_market_value_routes_unknown_edge():
    # No current market value ⇒ light priced-in can't run; the family still routes but
    # edge_survival is "unknown" and confidence is capped at 0.60 — reachable via run_workflow.
    case = load_case(JPM_DISCOVERY).model_copy(update={"x_mkt": None})
    theme, _ = run_workflow(ScriptedProvider(case), case.resolved_policy(), mode="discovery")
    assert theme.status == "strategy_family_routed"
    top = theme.strategy_families[0]
    assert top.confidence_components.edge_survival == "unknown"
    assert top.confidence <= 0.60 + 1e-9
    assert top.why_not and "market value" in top.why_not.lower()

def test_expression_mode_requires_a_market_value():
    case = load_case(AI_ISSUANCE).model_copy(update={"x_mkt": None})
    with pytest.raises(ValueError):
        run_workflow(ScriptedProvider(case), case.resolved_policy(), mode="expression")

def test_ai_issuance_expression_stays_golden_and_emits_families():
    theme, _ = _express(AI_ISSUANCE)
    assert theme.status == "expression_complete"
    # golden master intact
    assert theme.pricing.scenario_fv == pytest.approx(75.0, abs=ABS)
    assert theme.pricing.residual_edge == pytest.approx(20.0, abs=ABS)
    by_id = {e.id: e for e in theme.expressions}
    assert by_id["expr_cds_5s30s"].score == pytest.approx(3.918220233274124, abs=ABS)
    # now also emits ranked families — curve axis ⇒ steepener on top
    assert theme.strategy_families
    assert theme.strategy_families[0].family == "steepener"
