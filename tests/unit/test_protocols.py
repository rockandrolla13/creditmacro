"""Conformance tests for the Provider seam protocol and SizingRiskBundle.

Provider is runtime_checkable, so isinstance verifies the full method set across the
composed ScenarioSource/ExpressionSource/RiskSource protocols — this catches a seam
method being dropped or renamed.
"""
from __future__ import annotations

from engine.protocols import Provider, SizingRiskBundle
from engine.schema import Falsifier, PMGate, Risk, Sizing, StopLoss


class _FullProvider:
    def context(self): ...
    def parse(self, raw): ...
    def expand_causal(self, research_text, parsed_theme): ...
    def extract_drivers(self, statement): ...
    def define_axis(self, thesis): ...
    def normal_fair_value(self, axis): ...
    def propose_scenarios(self, thesis, axis): ...
    def enumerate_expressions(self, thesis, axis, scenarios): ...
    def size_and_risk(self, thesis, axis, best, conviction): ...
    def critique(self, theme): ...


class _MissingSeam:
    def parse(self, raw): ...
    # everything else missing


def test_full_provider_satisfies_protocol():
    assert isinstance(_FullProvider(), Provider)


def test_incomplete_provider_does_not_satisfy_protocol():
    assert not isinstance(_MissingSeam(), Provider)


def test_sizing_risk_bundle_groups_the_three_outputs():
    bundle = SizingRiskBundle(
        sizing=Sizing(conviction=3, sizing_factor=0.2, target_pnl=1.0, position="x"),
        risk=Risk(
            stop_loss=StopLoss(level=45.0, rationale="r"),
            falsifiers=[Falsifier(observable="o", threshold=1.0, kill_rule="k")],
            invalidation_horizon="12m",
            max_loss=-1.0,
        ),
        pm_gate=PMGate(open_questions=["q1"]),
    )
    assert bundle.sizing.conviction == 3
    assert bundle.risk.max_loss == -1.0
    assert bundle.pm_gate.open_questions == ["q1"]
