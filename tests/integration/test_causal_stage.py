"""EXPAND_CAUSAL stage — generic over cases/*.yaml."""
from __future__ import annotations

import pytest

from engine.case_loader import load_case
from engine.schema import CausalChain, CausalNode
from tests._helpers import CASES_DIR, build_theme

ALL_CASES = sorted(CASES_DIR.glob("*.yaml"))
CAUSAL_CASES = [p for p in ALL_CASES if load_case(p).causal is not None]

def _run(path):
    case, theme, _ = build_theme(path.name)
    return case, theme

def test_at_least_one_case_carries_a_causal_payload():
    assert CAUSAL_CASES, "expected >=1 case with a causal payload (e.g. french_banks)"

def test_ai_issuance_has_no_causal_and_stays_golden():
    _, theme = _run(CASES_DIR / "ai_issuance.yaml")
    assert theme.main_theme is None
    assert theme.causal_chain is None
    assert theme.pricing.residual_edge == pytest.approx(20.0, abs=1e-6)  # golden intact

@pytest.mark.parametrize("path", CAUSAL_CASES, ids=lambda p: p.stem)
def test_causal_case_attaches_one_main_theme_and_chain(path):
    _, theme = _run(path)
    assert isinstance(theme.main_theme, CausalNode)
    assert theme.main_theme.kind == "theme"
    assert isinstance(theme.causal_chain, CausalChain)
    assert theme.shared_factor

@pytest.mark.parametrize("path", CAUSAL_CASES, ids=lambda p: p.stem)
def test_every_theme_node_is_operational(path):
    _, theme = _run(path)
    theme_nodes = [n for n in theme.causal_chain.nodes if n.kind == "theme"]
    assert theme_nodes
    assert all(n.axis_operational and n.axis is not None for n in theme_nodes)

@pytest.mark.parametrize("path", CAUSAL_CASES, ids=lambda p: p.stem)
def test_edges_are_tagged_and_main_theme_in_chain(path):
    _, theme = _run(path)
    ids = {n.id for n in theme.causal_chain.nodes}
    assert theme.main_theme.id in ids
    for e in theme.causal_chain.edges:
        assert isinstance(e.inferred, bool) and isinstance(e.feedback, bool)
        assert e.from_id in ids and e.to_id in ids

def test_french_banks_marks_a_feedback_loop_and_stays_thesis_aligned():
    case, theme = _run(CASES_DIR / "french_banks.yaml")
    assert any(e.feedback for e in theme.causal_chain.edges)   # reflexive link marked
    assert theme.pricing.edge_direction_ok is True             # pricing unchanged
    # acceptance oracle still passes through the causal stage
    assert not [r for r in case.oracle.check(theme) if not r.passed]
