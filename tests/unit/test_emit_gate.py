"""G6 — the emit gate. Blocked beats plausible.

The load-bearing tests are the ones proving the gate BLOCKS, not the ones proving it
passes clean input (§9: "fail-closed behaviour has a test that proves it blocks, not
just that it warns").
"""
from __future__ import annotations

import pytest

from engine.grounding.emit_gate import (
    EmitBlockedError,
    assert_emittable,
    blocked_theme,
    check_emittable,
    is_grounded,
)
from engine.grounding.provenance_ledger import InMemoryProvenanceLedger
from engine.schema.grounding import GroundingVerdict
from engine.schema.provenance import LedgerNode

NOW = "2026-08-12T00:00:00+00:00"

GROUNDED = GroundingVerdict(status="grounded", method="exact", span_found=True,
                           numbers_verified=True, reason="span located")
UNGROUNDED = GroundingVerdict(status="ungrounded", method="none", span_found=False,
                              numbers_verified=False, reason="quote not found in source")
UNVERIFIABLE = GroundingVerdict(status="unverifiable", method="none", span_found=False,
                                numbers_verified=False, reason="no source_span supplied")


def _ledger(*nodes) -> InMemoryProvenanceLedger:
    store = InMemoryProvenanceLedger()
    store.extend(nodes)
    return store


def span(node_id: str, verdict: GroundingVerdict = GROUNDED) -> LedgerNode:
    return LedgerNode(id=node_id, kind="source_span", source_slug="src", verdict=verdict,
                      created_at=NOW)


def claim(node_id: str, *parents: str, kind: str = "atom") -> LedgerNode:
    return LedgerNode(id=node_id, kind=kind, parents=tuple(parents), created_at=NOW)


def _discovery_theme():
    """A real `discovery_complete` ThemeObject — the object the gate actually blocks.

    Built out rather than mocked because `blocked_theme` must produce something that
    still validates as a ThemeObject; a stand-in with two fields would pass whatever it
    was given.
    """
    from engine.schema import (
        Axis, AxisHistory, CausalChain, CausalChainStep, CausalEdge, CausalNode, Driver,
        Provenance, ThemeObject, Thesis,
    )

    axis = Axis(definition="IG 5s30s OAS slope, bps", measurement="bps",
                current_value=58.0,
                history=AxisHistory(mean=80.0, vol=15.0, percentile=20.0,
                                    regime_tags=["post-2022"]))
    theme_node = CausalNode(id="n_slope", statement="IG 5s30s steepens", kind="theme",
                            axis=axis, axis_operational=True)
    chain = CausalChain(
        nodes=[CausalNode(id="n_supply", statement="long-end supply", kind="cause"),
               theme_node],
        edges=[CausalEdge(from_id="n_supply", to_id="n_slope",
                          mechanism="issuance concentrates at the long end", inferred=True)])
    thesis = Thesis(
        drivers=[Driver(name="AI capex funding surge", sign="+",
                        proxy_observable="IG 5s30s OAS slope, bps",
                        mechanism="long-end supply steepens 5s30s")],
        causal_chain=[CausalChainStep(from_node="AI capex funding surge",
                                      to_node="IG 5s30s OAS slope")],
        direction_of_view="IG 5s30s OAS slope steepens")
    return ThemeObject(
        statement="AI capex funding steepens the IG curve", horizon="3m", author="test",
        status="discovery_complete", thesis=thesis, main_theme=theme_node,
        causal_chain=chain,
        provenance=Provenance(evidence=["src"], last_updated=NOW))


# ── the happy path, so the blocks below mean something ───────────────────────

def test_a_claim_with_a_grounded_span_ancestor_is_emittable():
    ledger = _ledger(span("s1"), claim("a1", "s1"),
                     claim("c1", "a1", kind="causal_claim"),
                     claim("f1", "c1", kind="strategy_family"))
    decision = check_emittable(["f1"], ledger)
    assert decision.allowed is True
    assert decision.blocked_node_ids == ()
    assert is_grounded("f1", ledger) is True


def test_grounding_survives_a_long_chain():
    nodes = [span("s1")] + [claim(f"n{i}", f"n{i - 1}" if i else "s1") for i in range(12)]
    assert check_emittable(["n11"], _ledger(*nodes)).allowed is True


# ── fail-closed: these must BLOCK ────────────────────────────────────────────

def test_an_ungrounded_span_blocks_everything_that_rests_on_it():
    ledger = _ledger(span("s_bad", UNGROUNDED), claim("a1", "s_bad"))
    decision = check_emittable(["a1"], ledger)
    assert decision.allowed is False
    assert decision.blocked_node_ids == ("a1",)
    assert decision.reason == "ungrounded_claim:a1"


def test_an_unverifiable_span_blocks_too():
    """`unverifiable` means the check could not run. That is not a pass."""
    ledger = _ledger(span("s_none", UNVERIFIABLE), claim("a1", "s_none"))
    assert check_emittable(["a1"], ledger).allowed is False


def test_a_claim_resting_on_nothing_is_refused():
    ledger = _ledger(claim("a1"))
    decision = check_emittable(["a1"], ledger)
    assert decision.allowed is False
    assert "rests on nothing" in decision.detail[0]


def test_a_dangling_citation_is_ungrounded_not_merely_weak():
    """A node nobody recorded is the easiest provenance to fake: cite an id and move on."""
    decision = check_emittable(["ghost"], InMemoryProvenanceLedger())
    assert decision.allowed is False
    assert "never recorded" in decision.detail[0]


def test_every_failure_is_reported_not_just_the_first():
    ledger = _ledger(span("s_bad", UNGROUNDED), claim("a1", "s_bad"), claim("a2", "s_bad"),
                     span("s_ok"), claim("a3", "s_ok"))
    decision = check_emittable(["a1", "a2", "a3"], ledger)
    assert decision.blocked_node_ids == ("a1", "a2")
    assert len(decision.detail) == 2


def test_assert_emittable_raises_and_carries_the_decision():
    ledger = _ledger(span("s_bad", UNGROUNDED), claim("a1", "s_bad"))
    with pytest.raises(EmitBlockedError) as exc:
        assert_emittable(["a1"], ledger)
    assert exc.value.decision.blocked_node_ids == ("a1",)


# ── ordinary claim: ANY grounded parent is enough ────────────────────────────

def test_one_grounded_parent_out_of_two_still_grounds_an_ordinary_claim():
    ledger = _ledger(span("s_ok"), span("s_bad", UNGROUNDED), claim("a1", "s_bad", "s_ok"))
    assert check_emittable(["a1"], ledger).allowed is True


# ── synthesis: EVERY parent must be grounded ─────────────────────────────────

def test_a_synthesis_with_grounded_parents_is_allowed():
    ledger = _ledger(span("s1"), span("s2"), claim("a1", "s1"), claim("a2", "s2"),
                     claim("brief", "a1", "a2", kind="synthesis"))
    assert check_emittable(["brief"], ledger).allowed is True


def test_one_ungrounded_parent_blocks_a_synthesis_even_though_it_would_pass_as_an_atom():
    """The asymmetry that makes G8's brief safe: a summary BLENDS its parents, so a
    single unsupported parent contaminates the sentence rather than being outvoted."""
    ledger = _ledger(span("s_ok"), span("s_bad", UNGROUNDED),
                     claim("a_ok", "s_ok"), claim("a_bad", "s_bad"),
                     claim("brief", "a_ok", "a_bad", kind="synthesis"),
                     claim("atom_same_parents", "a_ok", "a_bad"))

    assert check_emittable(["brief"], ledger).allowed is False
    assert check_emittable(["atom_same_parents"], ledger).allowed is True
    assert "every parent grounded" in check_emittable(["brief"], ledger).detail[0]


def test_a_parentless_synthesis_is_refused():
    assert check_emittable(["s"], _ledger(claim("s", kind="synthesis"))).allowed is False


# ── the caller's response to a block ─────────────────────────────────────────

def test_blocked_theme_names_the_reason_rather_than_inventing_one():
    theme = _discovery_theme()
    ledger = _ledger(span("s_bad", UNGROUNDED), claim("a1", "s_bad"))

    blocked = blocked_theme(theme, check_emittable(["a1"], ledger))
    assert blocked.status == "blocked"
    assert blocked.block_reason == "ungrounded_claim:a1"
    assert theme.status != "blocked"          # frozen: the original is untouched
    # The block must be a legal ThemeObject in its own right, not a field poke.
    type(theme).model_validate(blocked.model_dump())


def test_blocked_theme_refuses_an_allowed_decision():
    with pytest.raises(ValueError):
        blocked_theme(object(), check_emittable([], InMemoryProvenanceLedger()))
