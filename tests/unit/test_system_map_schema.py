"""SystemMap + BiasCritique schema (Meadows mapper + adversarial critic stages).

Stock (a level) and Flow (a rate) are distinct types — misclassifying them is the most
common error. A FeedbackLoop is reinforcing or balancing (enforced by Literal). Both
ThemeObject fields are Optional (golden master unaffected).
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from engine.schema import (
    Axis,
    AxisHistory,
    BiasCritique,
    CausalEdge,
    CausalNode,
    Delay,
    FeedbackLoop,
    Flow,
    Stock,
    SystemMap,
)


def _axis():
    return Axis(definition="A OAS − B OAS, bps", measurement="daily, bps", current_value=40.0,
               history=AxisHistory(mean=70.0, vol=30.0, percentile=10.0, regime_tags=["x"]))


def _system_map():
    return SystemMap(
        boundary_inside=["issuerA", "indexX"],
        boundary_outside=["policy rates"],
        boundary_rationale="loops close at funding->spread",
        function_purpose="fund AI capex",
        elements=[CausalNode(id="issuerA", statement="issuer", kind="theme",
                             axis=_axis(), axis_operational=True)],
        interconnections=[CausalEdge(from_id="issuerA", to_id="issuerA",
                                     mechanism="self", inferred=True, feedback=True)],
        stocks=[Stock(name="outstanding debt", unit="USD")],
        flows=[Flow(name="issuance", changes_stock="outstanding debt", unit_per_time="USD/qtr")],
        feedback_loops=[FeedbackLoop(id="R1", type="reinforcing",
                                     path=["capex", "revenue", "capex"], delay="18-36m",
                                     closes_via="revenue funds more capex")],
        delays=[Delay(between="capex and revenue", length="18-36m", why_it_matters="overshoot")],
        external_shocks=["AI demand miss"],
        internal_responses=["spreads widen"],
        observable_variables=["OAS series"],
        surprise_modes=["reflexive index loop reverses"],
    )


def test_stock_and_flow_are_distinct_types():
    s = Stock(name="debt", unit="USD")
    f = Flow(name="issuance", changes_stock="debt", unit_per_time="USD/qtr")
    assert s.unit == "USD" and f.unit_per_time == "USD/qtr"
    assert type(s) is not type(f)


def test_feedback_loop_must_be_reinforcing_or_balancing():
    FeedbackLoop(id="B1", type="balancing", path=["a", "b"], closes_via="brake")
    with pytest.raises(ValidationError):
        FeedbackLoop(id="X", type="oscillating", path=["a"], closes_via="?")


def test_system_map_constructs_and_reuses_chain_types():
    sm = _system_map()
    assert sm.function_purpose == "fund AI capex"
    assert isinstance(sm.elements[0], CausalNode)
    assert isinstance(sm.interconnections[0], CausalEdge)
    assert sm.interconnections[0].feedback is True
    assert sm.feedback_loops[0].type == "reinforcing"


def test_bias_critique_decision_is_constrained():
    bc = BiasCritique(dominant_mental_model="new asset class = opportunity",
                      decision="challenge_model")
    assert bc.decision == "challenge_model"
    with pytest.raises(ValidationError):
        BiasCritique(dominant_mental_model="m", decision="maybe")


def test_theme_object_new_fields_optional_default_none():
    from engine.example import theme
    assert theme.system_map is None
    assert theme.bias_critique is None
    assert theme.loop_diagnosis is None
    assert theme.trap_implications is None
    assert theme.iceberg_classification is None  # the theme's own Stage-0 classification
