"""Unit tests for engine.cases — PolicyConfig, the Oracle discriminated union, and"""
from __future__ import annotations

import pytest
from pydantic import TypeAdapter, ValidationError

from engine.cases import (
    AcceptanceOracle,
    AssertionResult,
    ExactOracle,
    InvariantsOnlyOracle,
    Oracle,
    PolicyConfig,
    RatioTarget,
)

_oracle_adapter = TypeAdapter(Oracle)

# ── PolicyConfig: single source of truth for gate thresholds (AR-DRY-001) ────

def test_policy_config_defaults_match_current_constants():
    p = PolicyConfig()
    assert p.omega_min == 2.0
    assert p.liquidity_min == 0.40
    assert p.cost_fraction_max == 0.33
    assert p.convexity_weight_a == 0.10
    assert p.crowding_decay_g == 0.50
    assert p.snr_min == 1.0

# ── Oracle discriminated union (AR-ABS-001) ──────────────────────────────────

def test_oracle_parses_exact_by_discriminator():
    o = _oracle_adapter.validate_python(
        {
            "kind": "exact",
            "scenario_fv": 75.0,
            "q": [0.25, 0.25, 0.25, 0.25],
            "edge": 20.0,
            "omega": 7.67,
            "score": 3.92,
            "gated_out": ["expr_etf_basis"],
        }
    )
    assert isinstance(o, ExactOracle)

def test_oracle_parses_acceptance_by_discriminator():
    o = _oracle_adapter.validate_python(
        {
            "kind": "acceptance",
            "base_worst_ratio": {"target": 1.9, "tol": 0.3},
            "attribution_top": "Worst/no-support",
        }
    )
    assert isinstance(o, AcceptanceOracle)
    assert o.edge_sign == "thesis_aligned"

def test_oracle_parses_invariants_only():
    o = _oracle_adapter.validate_python({"kind": "invariants_only"})
    assert isinstance(o, InvariantsOnlyOracle)

def test_exact_oracle_rejects_missing_required_field():
    # kind=exact MUST carry its numbers — illegal states unrepresentable
    with pytest.raises(ValidationError):
        _oracle_adapter.validate_python({"kind": "exact", "scenario_fv": 75.0})

# ── ExactOracle.check against the real golden theme ──────────────────────────

def _golden_exact_oracle() -> ExactOracle:
    return ExactOracle(
        scenario_fv=75.0,
        q=[0.125512, 0.184417, 0.328452, 0.361619],
        edge=20.0,
        omega=7.666666666666667,
        score=3.918220233274124,
        gated_out=["expr_etf_basis"],
    )

def test_exact_check_all_pass_on_golden_theme():
    from engine.example import theme

    results = _golden_exact_oracle().check(theme)
    assert all(isinstance(r, AssertionResult) for r in results)
    failed = [r for r in results if not r.passed]
    assert not failed, f"unexpected failures: {failed}"

def test_exact_check_detects_a_wrong_number():
    from engine.example import theme

    bad = _golden_exact_oracle().model_copy(update={"edge": 99.0})
    results = bad.check(theme)
    assert any(r.name == "edge" and not r.passed for r in results)

def test_ratio_target_model():
    rt = RatioTarget(target=1.9, tol=0.3)
    assert rt.target == 1.9 and rt.tol == 0.3
