"""Live discovery LLM seams on LLMProvider (define_axis, build_system_map, diagnose_loops,
critique_mental_model). Tests inject a FAKE Anthropic client (no network) returning canned
JSON, so the production parse+validate path runs offline. No expression seams, no scenario
probabilities, no sizing/legs.
"""
from __future__ import annotations

import json

import pytest

from engine.llm_provider import LLMProvider, NoCleanAxisError
from engine.memory import MemoryRetriever, WikiPage
from engine.schema import (
    Axis,
    AxisHistory,
    BiasCritique,
    CausalChain,
    CausalEdge,
    CausalNode,
    Delay,
    Driver,
    FeedbackLoop,
    Flow,
    LoopDiagnosis,
    Stock,
    SystemMap,
    Thesis,
)
from engine.schema.causal import CausalChainStep
from tests._helpers import ABS, GOLDEN_EDGE, GOLDEN_Q, GOLDEN_SCENARIO_FV, build_theme


# ── fake Anthropic client ─────────────────────────────────────────────────────
class _Block:
    def __init__(self, text): self.type = "text"; self.text = text
class _Resp:
    def __init__(self, text): self.content = [_Block(text)]
class _FakeClient:
    def __init__(self, text): self.text = text; self.calls = []
    class _M:
        def __init__(self, outer): self.outer = outer
        def create(self, **kw): self.outer.calls.append(kw); return _Resp(self.outer.text)
    @property
    def messages(self): return _FakeClient._M(self)


def _axis_json(definition="IG 5s30s OAS slope = OAS(30Y) − OAS(5Y), bps", source_derived=True):
    return json.dumps({
        "axis": {"definition": definition, "measurement": "Bloomberg BVAL OAS, daily close, bps",
                 "current_value": 58.0,
                 "history": {"mean": 80.0, "vol": 15.0, "percentile": 20.0, "regime_tags": ["x"]},
                 "axis_shape": "curve", "axis_direction": "steeper"},
        "confidence": 0.7, "reason": "source-derived 5s30s slope is a clean named series",
        "data_needed_next": "live 5Y/30Y OAS history", "recommend_watchlist": False,
        "source_derived": source_derived})


def _thesis():
    return Thesis(
        drivers=[Driver(name="AI capex funding surge", sign="+",
                        proxy_observable="IG 5s30s OAS slope = OAS(30Y) − OAS(5Y), bps",
                        mechanism="long-end supply steepens 5s30s")],
        causal_chain=[CausalChainStep(from_node="AI capex funding surge", to_node="IG 5s30s OAS slope")],
        direction_of_view="IG 5s30s OAS slope steepens")


def _chain():
    ax = Axis(definition="IG 5s30s OAS slope, bps", measurement="bps", current_value=58.0,
              history=AxisHistory(mean=80.0, vol=15.0, percentile=20.0, regime_tags=["x"]))
    n = CausalNode(id="n_diff", statement="5s30s steepens", kind="theme", axis=ax, axis_operational=True)
    return CausalChain(nodes=[CausalNode(id="n0", statement="supply", kind="cause"), n],
                       edges=[CausalEdge(from_id="n0", to_id="n_diff", mechanism="m", inferred=True)])


# 1 ─ define_axis uses source-derived axes when available ─────────────────────
def test_define_axis_uses_source_derived_axis():
    prov = LLMProvider(client=_FakeClient(_axis_json()))
    axis = prov.define_axis(_thesis())
    assert isinstance(axis, Axis)
    assert "5s30s" in axis.definition                       # the source-derived candidate
    assert prov.last_axis_selection.source_derived is True
    # the user content carried the source-derived candidate to the model
    assert "5s30s" in prov._client.calls[0]["messages"][0]["content"]


# 2 ─ define_axis does not invent exact trades; no-clean-axis → watchlist signal ─
def test_define_axis_no_exact_trades_and_watchlist_path():
    axis = LLMProvider(client=_FakeClient(_axis_json())).define_axis(_thesis())
    low = axis.definition.lower()
    for tok in ["buy ", "sell ", "hedge ratio", "dv01", "notional", "$mm", "stop loss"]:
        assert tok not in low                               # a named series, not a trade
    watch = json.dumps({"axis": None, "confidence": 0.2, "reason": "no clean differential",
                        "data_needed_next": "build & net the series", "recommend_watchlist": True})
    prov = LLMProvider(client=_FakeClient(watch))
    with pytest.raises(NoCleanAxisError) as e:
        prov.define_axis(_thesis())
    assert e.value.data_needed_next and prov.last_axis_selection.recommend_watchlist is True


# 3 ─ build_system_map returns stocks, flows, loops, delays ───────────────────
def test_build_system_map_has_stocks_flows_loops_delays():
    sm_json = json.dumps({
        "boundary_inside": ["hyperscalers", "data centers", "HY HPC"],
        "boundary_outside": ["policy rates"], "function_purpose": "fund AI capex",
        "stocks": [{"name": "outstanding AI/DC/HPC credit", "unit": "USD"},
                   {"name": "benchmark/index ownership", "unit": "USD AUM"}],
        "flows": [{"name": "new issuance", "changes_stock": "outstanding AI/DC/HPC credit", "unit_per_time": "USD/qtr"},
                  {"name": "ETF + mutual fund demand", "changes_stock": "benchmark/index ownership", "unit_per_time": "USD/day"}],
        "feedback_loops": [{"id": "R1", "type": "reinforcing", "path": ["perf", "inflows", "perf"],
                            "closes_via": "performance → inflows/attention → tightening → performance"},
                           {"id": "B1", "type": "balancing", "path": ["issuance", "demand"],
                            "closes_via": "issuance growth → cheapening → reduced demand"}],
        "delays": [{"between": "index inclusion", "length": "monthly rebalance", "why_it_matters": "benchmark adoption lag"}]})
    sm = LLMProvider(client=_FakeClient(sm_json)).build_system_map(_thesis(), _chain())
    assert isinstance(sm, SystemMap)
    assert sm.stocks and sm.flows and sm.feedback_loops and sm.delays
    types = {fl.type for fl in sm.feedback_loops}
    assert "reinforcing" in types and "balancing" in types


# 4 ─ diagnose_loops flags crowding/momentum for HY HPC ──────────────────────
def test_diagnose_loops_flags_crowding_momentum():
    ld_json = json.dumps({
        "dominant_loop_now": "R1 reinforcing — HY HPC performance→inflows→tightening",
        "dominant_loop_evidence": "HPC +9.99% vs HY +1.61%; weight 1.07→2.68%",
        "possible_loop_shift": "flows turn → momentum/crowding reversal (R→B)",
        "system_traps": ["success-to-the-successful crowding", "momentum chasing in HY HPC"],
        "early_warning_indicators": ["net fund flows turning"], "decision": "watchlist"})
    sm = LLMProvider(client=_FakeClient(json.dumps({"boundary_inside": [], "boundary_outside": [],
        "function_purpose": "x", "feedback_loops": [{"id": "R1", "type": "reinforcing", "path": ["a"], "closes_via": "c"}]}))
        ).build_system_map(_thesis(), _chain())
    ld = LLMProvider(client=_FakeClient(ld_json)).diagnose_loops(sm)
    assert isinstance(ld, LoopDiagnosis)
    blob = (ld.possible_loop_shift + " " + " ".join(ld.system_traps)).lower()
    assert "crowd" in blob or "momentum" in blob


# 5 ─ critique_mental_model lists confounders and falsifiers ──────────────────
def test_critique_lists_confounders_and_disconfirming():
    bc_json = json.dumps({
        "dominant_mental_model": "AI-credit RV is mispricing",
        "alternative_models": ["basis explained by rating/duration/liquidity",
                               "HPC outperformance is momentum/crowding"],
        "assumptions_treated_as_facts": ["the project/hyperscaler relationship is stationary"],
        "disconfirming_evidence": ["index inclusion does not translate into tradeable liquidity",
                                   "differential is non-stationary over the sample"],
        "lenses_examined": ["fundamental", "technical", "liquidity", "positioning", "time-horizon"],
        "decision": "challenge_model"})
    bc = LLMProvider(client=_FakeClient(bc_json)).critique_mental_model("AI capex theme", _chain())
    assert isinstance(bc, BiasCritique)
    assert bc.alternative_models and bc.disconfirming_evidence
    assert bc.decision in ("accept_model", "challenge_model", "reject_model")


# 6 ─ no CASE memory read before FreshReasoningSnapshot (METHOD only) ─────────
def test_seams_read_method_memory_only():
    pages = {
        "meadows": WikiPage(slug="meadows", access_class="method", type="concept",
                            frontmatter={"slug": "meadows"}, body="stocks and flows and loops"),
        "jpm-case": WikiPage(slug="jpm-case", access_class="case", type="theme",
                             frontmatter={"slug": "jpm-case"}, body="a prior conclusion"),
    }
    retr = MemoryRetriever(pages, phase="A")
    sm_json = json.dumps({"boundary_inside": [], "boundary_outside": [], "function_purpose": "x"})
    LLMProvider(client=_FakeClient(sm_json), retriever=retr).build_system_map(_thesis(), _chain())
    case_reads = [r for r in retr.reads if r["access_class"] == "case" and r["allowed"]]
    assert not case_reads                                   # no case page served in phase A
    assert "jpm-case" not in retr.reads or all(not r["allowed"] for r in retr.reads if r["slug"] == "jpm-case")


# 7/10 ─ no expression output; expression seams remain scripted ──────────────
def test_no_expression_seams_on_llm_provider():
    assert not hasattr(LLMProvider, "enumerate_expressions")
    assert not hasattr(LLMProvider, "size_and_risk")
    # propose_scenarios exists but invents nothing (no scenarios / probabilities)
    assert LLMProvider(research_text="x").propose_scenarios(None, None) == []
    # the discovery seams' outputs carry no pricing/sizing/expression fields
    for cls in (Axis, SystemMap, LoopDiagnosis, BiasCritique):
        fields = set(cls.model_fields)
        assert not (fields & {"pricing", "sizing", "expressions", "hedge_ratio", "scenario_pnl"})


# 8 ─ golden master unchanged ────────────────────────────────────────────────
def test_golden_master_unchanged():
    _, theme, _ = build_theme("ai_issuance.yaml")
    assert theme.pricing.scenario_fv == pytest.approx(GOLDEN_SCENARIO_FV, abs=ABS)
    assert theme.pricing.priced_in.q_s == pytest.approx(GOLDEN_Q, abs=ABS)
    assert theme.pricing.residual_edge == pytest.approx(GOLDEN_EDGE, abs=ABS)


# 9 ─ discovery still stops at strategy_family_routed (scripted path) ─────────
def test_discovery_still_stops_at_routing():
    from pathlib import Path
    from tests._helpers import CASES_DIR
    _, theme, _ = build_theme(CASES_DIR / "discovery" / "jpm_ai_capex.yaml", mode="discovery")
    assert theme.status in ("strategy_family_routed", "discovery_complete")
    assert theme.pricing is None and theme.sizing is None and theme.expressions == []
