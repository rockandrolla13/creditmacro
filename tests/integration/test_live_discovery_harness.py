"""Live discovery harness + AUTOMATIC semantic-contract validation (before FreshReasoningSnapshot).

The harness runs discovery via the LLM provider (offline fake client), validates the output
against the semantic contract, and FAILS CLOSED — never freezing a snapshot — on economically
wrong axes, accidental trade legs, sizing, or expression leakage. Golden master unchanged.
"""
from __future__ import annotations

import pytest

from engine.live_discovery import (
    SemanticContractViolation,
    run_live_discovery,
)
from engine.provider_select import LiveDiscoveryNotEnabled, run_discovery
from engine.semantic_contract import validate_discovery_output
from tests._helpers import ABS, GOLDEN_EDGE, GOLDEN_Q, GOLDEN_SCENARIO_FV, build_theme
from tests.integration.test_provider_selection import _RoutingFake, _llm

TS = "2026-06-08T00:00:00+00:00"


def _kw(**over):
    base = dict(research_text="AI capex RV across hyperscalers and project bonds",
                current_input_axes=["project_bond_OAS_minus_related_hyperscaler_OAS"],
                current_sources=["jpm-ai-capex-funding-2026-05-11"],
                client=_RoutingFake(), timestamp=TS)
    base.update(over)
    return base


# 1 ─ validator passes a clean discovery output ──────────────────────────────
def test_validate_passes_clean_discovery():
    theme, _ = run_discovery(_llm(), __import__("engine.cases", fromlist=["PolicyConfig"]).PolicyConfig())
    assert validate_discovery_output(theme, input_kind="jpm_report") == []


# 2 ─ validator flags trade-leg / sizing / expression leakage ────────────────
def test_validate_flags_trade_leakage():
    _, expr_theme, _ = build_theme("ai_issuance.yaml")     # expression_complete: pricing/sizing/exprs
    v = validate_discovery_output(expr_theme)
    assert any("leakage" in x for x in v)
    assert any("expression_leakage" in x for x in v)       # status == expression_complete


# 3 ─ validator flags an economically wrong axis for the input kind ──────────
def test_validate_flags_wrong_axis_for_kind():
    theme, _ = run_discovery(_llm(), __import__("engine.cases", fromlist=["PolicyConfig"]).PolicyConfig())
    v = validate_discovery_output(theme, input_kind="curve_steepener")   # basis axis ≠ curve
    assert v and any("curve" in x for x in v)


# 4 ─ harness: clean run validates, freezes snapshot, captures ───────────────
def test_harness_clean_freezes_and_captures(tmp_path):
    res = run_live_discovery(input_kind="jpm_report", capture_dir=str(tmp_path / "runs"),
                             slug="jpm", env={}, **_kw())
    assert res.violations == []
    assert res.snapshot is not None and res.snapshot.content_hash
    assert res.record.snapshot_hash == res.snapshot.content_hash
    assert res.theme.pricing is None and res.theme.sizing is None and res.theme.expressions == []
    assert res.record.no_trade_confirmation is True
    assert list((tmp_path / "runs").glob("*.json"))        # capture written (gitignored dir)


# 5 ─ harness: FAILS CLOSED on contract violation (no snapshot) ──────────────
def test_harness_fails_closed_on_violation(tmp_path):
    with pytest.raises(SemanticContractViolation) as e:
        run_live_discovery(input_kind="curve_steepener", capture_dir=str(tmp_path / "runs"),
                           slug="bad", env={}, **_kw())
    assert e.value.violations
    assert e.value.record.snapshot_hash is None            # snapshot NOT frozen on violation
    assert e.value.record.validation_errors                # violation captured for audit
    assert list((tmp_path / "runs").glob("*.json"))        # captured even on failure


# 6 ─ harness respects the live opt-in guard ────────────────────────────────
def test_harness_respects_live_guard():
    with pytest.raises(LiveDiscoveryNotEnabled, match="live_discovery_not_enabled"):
        run_live_discovery(research_text="x", client=None, env={}, timestamp=TS, capture=False)


# 7 ─ golden master unchanged ────────────────────────────────────────────────
def test_golden_master_unchanged():
    _, theme, _ = build_theme("ai_issuance.yaml")
    assert theme.pricing.scenario_fv == pytest.approx(GOLDEN_SCENARIO_FV, abs=ABS)
    assert theme.pricing.priced_in.q_s == pytest.approx(GOLDEN_Q, abs=ABS)
    assert theme.pricing.residual_edge == pytest.approx(GOLDEN_EDGE, abs=ABS)
