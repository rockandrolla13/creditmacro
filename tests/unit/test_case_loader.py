"""Tests for engine.case_loader — loading cases/*.yaml into a typed CaseSpec and"""
from __future__ import annotations

from pathlib import Path

import pytest

from engine.case_loader import load_case, resolve_prior
from engine.cases import CaseSpec, ExactOracle

CASE_DIR = Path(__file__).resolve().parents[2] / "cases"

def test_resolve_prior_uniform():
    assert resolve_prior("uniform", n=4) == pytest.approx([0.25, 0.25, 0.25, 0.25])

def test_resolve_prior_explicit_vector_passthrough():
    assert resolve_prior([0.1, 0.2, 0.7], n=3) == pytest.approx([0.1, 0.2, 0.7])

def test_resolve_prior_historical_from_hist_freq():
    out = resolve_prior("historical", n=3, hist_freq=[0.2, 0.3, 0.5])
    assert out == pytest.approx([0.2, 0.3, 0.5])

def test_resolve_prior_historical_normalises():
    out = resolve_prior("historical", n=2, hist_freq=[1.0, 3.0])
    assert out == pytest.approx([0.25, 0.75])

def test_resolve_prior_historical_requires_hist_freq():
    with pytest.raises(ValueError):
        resolve_prior("historical", n=3, hist_freq=[0.2, None, 0.5])

def test_resolve_prior_rejects_wrong_length():
    with pytest.raises(ValueError):
        resolve_prior([0.5, 0.5], n=4)

def test_load_ai_issuance_case():
    cs = load_case(CASE_DIR / "ai_issuance.yaml")
    assert isinstance(cs, CaseSpec)
    assert cs.theme_sentence == "AI issuance will steepen IG credit curves"
    assert len(cs.scenarios) == 4
    assert cs.thesis_sign == 1
    # prior resolved from "uniform" to a concrete vector
    assert cs.prior == pytest.approx([0.25, 0.25, 0.25, 0.25])
    # exact oracle carrying the golden numbers
    assert isinstance(cs.oracle, ExactOracle)
    assert cs.oracle.scenario_fv == pytest.approx(75.0)
    assert cs.oracle.edge == pytest.approx(20.0)

def test_loaded_expressions_are_pre_scoring():
    cs = load_case(CASE_DIR / "ai_issuance.yaml")
    # the workflow computes scores; the case carries un-scored expressions
    assert all(e.score is None for e in cs.expressions)
    assert len(cs.expressions) == 2
