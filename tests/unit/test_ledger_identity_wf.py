"""Phase-1 gates: event-type classifier (§Event semantics, F2) and WF direction
consistency (§WF clause e / invariant I8e).

ThemeHypothesis is constructed directly here — permitted in tests (I5 excludes tests/).
"""
from __future__ import annotations

from engine.ledger.substrate.events import EventType
from engine.ledger.substrate.hypothesis import (
    Mechanism, TransmissionEdge, ThemeHypothesis,
)
from engine.ledger.substrate.identity import classify_event, wf_predicate


def _m(*edges):
    return Mechanism(edges=tuple(TransmissionEdge(v_from=a, v_to=b, sign=s) for (a, b, s) in edges))


def _theme(mech=None, sigma=1, axis="C0A0_OAS", horizon=90, falsifier="F", theme_id="t1"):
    mech = mech or _m(("funding_stress", "liquidity_premium", 1),
                      ("liquidity_premium", "credit_spread", 1))
    return ThemeHypothesis(theme_id=theme_id, mechanism=mech, shock_direction=sigma,
                           operational_axis=axis, horizon_days=horizon, falsifier=falsifier)


# ── classify_event (§Event semantics) ────────────────────────────────────────
def test_classify_refinement_is_mechanism_revised():
    cur = _theme()
    # same endpoints + sign product, extra intermediate node → ≅ (refinement)
    refined = _theme(mech=_m(("funding_stress", "dealer_balance_sheet_capacity", 1),
                             ("dealer_balance_sheet_capacity", "liquidity_premium", 1),
                             ("liquidity_premium", "credit_spread", 1)))
    assert classify_event(cur, refined) == (EventType.MECHANISM_REVISED,)


def test_classify_disjoint_mechanism_is_retire_create():
    cur = _theme()
    disjoint = _theme(mech=_m(("issuance_supply", "risk_appetite", 1),
                              ("risk_appetite", "credit_spread", 1)))
    assert classify_event(cur, disjoint) == (EventType.RETIRED, EventType.CREATED)


def test_classify_shock_reversal_is_retire_create():
    cur = _theme(sigma=1)
    flipped = _theme(sigma=-1)
    assert classify_event(cur, flipped) == (EventType.RETIRED, EventType.CREATED)


def test_classify_axis_only_is_axis_revised():
    assert classify_event(_theme(axis="C0A0_OAS"), _theme(axis="H0A0_OAS")) == (EventType.AXIS_REVISED,)


def test_classify_horizon_only_is_horizon_extended():
    assert classify_event(_theme(horizon=90), _theme(horizon=110)) == (EventType.HORIZON_EXTENDED,)


def test_classify_falsifier_only_is_falsifier_revised():
    assert classify_event(_theme(falsifier="F1"), _theme(falsifier="F2")) == (EventType.FALSIFIER_REVISED,)


def test_classify_no_change_is_empty():
    assert classify_event(_theme(), _theme()) == ()


# ── WF direction consistency — the named gate ────────────────────────────────
def test_direction_consistency():
    # σ=+1, sign product = +1 → d(θ)=+1. A stated direction of -1 is malformed (I8e).
    theme = _theme(sigma=1)
    bad = wf_predicate(theme, stated_direction=-1)
    assert bad.ok is False
    assert bad.failing_clause == "e"

    good = wf_predicate(theme, stated_direction=1)
    assert good.ok is True


def test_wf_rejects_k1_chain():
    theme = _theme(mech=_m(("funding_stress", "credit_spread", 1)))  # k=1
    assert wf_predicate(theme).failing_clause == "a"


def test_wf_rejects_untracked_axis():
    assert wf_predicate(_theme(axis="NOT_A_REAL_AXIS")).failing_clause == "c"


def test_wf_rejects_over_horizon():
    assert wf_predicate(_theme(horizon=200)).failing_clause == "d"


def test_wf_wellformed_passes():
    assert wf_predicate(_theme(), stated_direction=1).ok is True
