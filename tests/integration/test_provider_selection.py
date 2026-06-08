"""Provider selection + live guard + semantic contract + capture/replay + NoCleanAxisError.

End-to-end LLM discovery runs offline via a routing fake client (no API key). No expression
seams, no scenario probabilities, no sizing/legs. Golden master unchanged.
"""
from __future__ import annotations

import json

import pytest

from engine.capture import (
    LiveRunRecord,
    input_hash,
    replay,
    revalidate,
    write_run_record,
)
from engine.cases import PolicyConfig
from engine.case_loader import load_case
from engine.llm_provider import LLMProvider, NoCleanAxisError
from engine.memory import MemoryRetriever, WikiPage
from engine.provider_select import (
    LiveDiscoveryNotEnabled,
    run_discovery,
    select_discovery_provider,
)
from engine.scripted_provider import ScriptedProvider
from engine.semantic_contract import check_axis_contract
from engine.workflow import run_workflow
from tests._helpers import ABS, CASES_DIR, GOLDEN_EDGE, GOLDEN_Q, GOLDEN_SCENARIO_FV, build_theme

JPM_FIXTURE = CASES_DIR / "discovery" / "jpm_ai_capex.yaml"

# ── routing fake: maps a system-prompt phrase → canned per-seam JSON ──────────
_AX = {"definition": "project_bond_OAS_minus_related_hyperscaler_OAS, bps",
       "measurement": "OAS differential, bps, daily", "current_value": 105.0,
       "history": {"mean": 120.0, "vol": 20.0, "percentile": 30.0, "regime_tags": ["x"]},
       "axis_shape": "basis", "axis_direction": "tighter"}
_EXPAND = json.dumps({
    "main_theme": {"id": "n_basis", "statement": "project vs hyperscaler basis", "kind": "theme",
                   "axis": _AX, "axis_operational": True, "promoted": True},
    "causal_chain": {"nodes": [{"id": "n_capex", "statement": "AI capex funding", "kind": "cause"},
                               {"id": "n_basis", "statement": "project vs hyperscaler basis",
                                "kind": "theme", "axis": _AX, "axis_operational": True, "promoted": True}],
                     "edges": [{"from_id": "n_capex", "to_id": "n_basis",
                                "mechanism": "same capex funds both legs", "inferred": True}]},
    "shared_factor": "AI capex funding"})
_AXIS_OK = json.dumps({"axis": _AX, "confidence": 0.7, "reason": "source-derived basis",
                       "data_needed_next": "clean differential series", "recommend_watchlist": False,
                       "source_derived": True})
_AXIS_NONE = json.dumps({"axis": None, "confidence": 0.2, "reason": "no clean differential",
                         "data_needed_next": "build & net the series", "recommend_watchlist": True})
_SYSMAP = json.dumps({"boundary_inside": ["hyperscalers", "data centers"], "boundary_outside": ["rates"],
                      "function_purpose": "fund AI capex",
                      "stocks": [{"name": "outstanding credit", "unit": "USD"}],
                      "flows": [{"name": "new issuance", "changes_stock": "outstanding credit", "unit_per_time": "USD/q"}],
                      "feedback_loops": [{"id": "R1", "type": "reinforcing", "path": ["a", "b"], "closes_via": "perf→inflows→tightening"}],
                      "delays": [{"between": "index inclusion", "length": "monthly", "why_it_matters": "adoption lag"}]})
_LOOPS = json.dumps({"dominant_loop_now": "R1", "possible_loop_shift": "flows turn → crowding reversal",
                     "system_traps": ["crowding"], "invalidation_evidence": ["differential mean-reverts to zero"],
                     "decision": "watchlist"})
_CRIT = json.dumps({"dominant_mental_model": "RV is mispricing",
                    "alternative_models": ["rating/duration/liquidity"], "disconfirming_evidence": ["non-stationary"],
                    "decision": "challenge_model"})


class _Block:
    def __init__(self, t): self.type = "text"; self.text = t
class _Resp:
    def __init__(self, t): self.content = [_Block(t)]
class _RoutingFake:
    def __init__(self, axis=_AXIS_OK): self.axis = axis; self.systems = []
    class _M:
        def __init__(self, o): self.o = o
        def create(self, *, system, messages, **kw):
            self.o.systems.append(system)
            if "OPERATIONAL AXIS" in system: return _Resp(self.o.axis)
            if "SYSTEM MAP" in system: return _Resp(_SYSMAP)
            if "diagnose QUALITATIVELY" in system: return _Resp(_LOOPS)
            if "Critique the mental model" in system: return _Resp(_CRIT)
            return _Resp(_EXPAND)
    @property
    def messages(self): return _RoutingFake._M(self)


def _llm(axis=_AXIS_OK, retriever=None):
    return LLMProvider(client=_RoutingFake(axis), research_text="AI capex RV across hyperscalers and project bonds",
                       current_input_axes=["project_bond_OAS_minus_related_hyperscaler_OAS"],
                       current_sources=["jpm-ai-capex-funding-2026-05-11"], retriever=retriever)


# 1 ─ ScriptedProvider is the default ─────────────────────────────────────────
def test_scripted_is_default():
    case = load_case(JPM_FIXTURE)
    assert isinstance(select_discovery_provider(case=case), ScriptedProvider)
    assert isinstance(select_discovery_provider("scripted", case=case), ScriptedProvider)


# 2 ─ live LLM requires ALLOW_LIVE_LLM_DISCOVERY=1 ───────────────────────────
def test_live_llm_requires_optin():
    with pytest.raises(LiveDiscoveryNotEnabled, match="live_discovery_not_enabled"):
        select_discovery_provider("llm", client=None, env={})            # no flag, real client
    # opt-in present → builds (uses a fake client so no network)
    p = select_discovery_provider("llm", client=_RoutingFake(), env={"ALLOW_LIVE_LLM_DISCOVERY": "1"})
    assert isinstance(p, LLMProvider)


# 3 ─ LLMProvider runs discovery with a fake client ──────────────────────────
def test_llm_discovery_runs_with_fake_client():
    theme, _ = run_discovery(_llm(), PolicyConfig())
    assert theme.status in ("strategy_family_routed", "discovery_complete")
    assert theme.pricing is None and theme.sizing is None and theme.expressions == []
    assert theme.main_theme is not None and theme.system_map is not None


# 4 ─ LLMProvider cannot run expression mode ─────────────────────────────────
def test_llm_cannot_run_expression():
    with pytest.raises(RuntimeError, match="expression_mode_not_supported"):
        run_workflow(_llm(), PolicyConfig(), mode="expression")


# 5 ─ NoCleanAxisError → blocked, no fabricated axis ─────────────────────────
def test_no_clean_axis_blocks_not_fabricates():
    theme, _ = run_discovery(_llm(axis=_AXIS_NONE), PolicyConfig())
    assert theme.status == "blocked"
    assert theme.block_reason == "no_clean_operational_axis"
    assert theme.axis is None and theme.pricing is None and theme.expressions == []


# 6 ─ JPM semantic contract: no default to generic 5s30s ─────────────────────
def test_jpm_semantic_rejects_generic_curve():
    bad = check_axis_contract("jpm_report", axes=["IG 5s30s OAS slope"], families=["steepener"])
    assert bad and any("curve" in v for v in bad)
    good = check_axis_contract("jpm_report",
                               axes=["project_bond_OAS_minus_related_hyperscaler_OAS",
                                     "Data_Centers_OAS_minus_Technology_OAS"],
                               families=["long_short", "index_index_rv"])
    assert good == []


# 7 ─ curve-specific input can have curve/steepener top ──────────────────────
def test_curve_input_allows_steepener():
    ok = check_axis_contract("curve_steepener", axes=["IG 5s30s OAS slope"], families=["steepener"],
                             missing_data=["issuer universe", "maturity bucket", "current curve", "fair-value model"])
    assert ok == []
    # missing the trade-readiness questions → violation
    bad = check_axis_contract("curve_steepener", axes=["IG 5s30s OAS slope"], families=["steepener"], missing_data=[])
    assert bad


# 8 ─ ETF-flow input → etf_basket_rv top ─────────────────────────────────────
def test_etf_flow_ranks_etf_basket_rv():
    ok = check_axis_contract("etf_flow", axes=["ETF vs basket basis (premium/discount)"],
                             families=["etf_basket_rv", "curve", "outright"])
    assert ok == []
    bad = check_axis_contract("etf_flow", axes=["ETF vs basket basis"], families=["curve", "etf_basket_rv"])
    assert bad


# 9 ─ margin-compression → long_short / sector_rotation top ──────────────────
def test_margin_input_ranks_long_short_or_sector():
    ok = check_axis_contract("margin_compression", axes=["sector spread dispersion"],
                             families=["long_short", "cash_cds_basis"])
    assert ok == []
    bad = check_axis_contract("margin_compression", axes=["sector spread dispersion"],
                              families=["cash_cds_basis", "long_short"])
    assert bad


# 10 ─ phase-A memory reads METHOD only ──────────────────────────────────────
def test_phase_a_reads_method_only():
    pages = {"meadows": WikiPage(slug="meadows", access_class="method", type="concept",
                                 frontmatter={"slug": "meadows"}, body="stocks flows loops"),
             "jpm-case": WikiPage(slug="jpm-case", access_class="case", type="theme",
                                  frontmatter={"slug": "jpm-case"}, body="prior conclusion")}
    retr = MemoryRetriever(pages, phase="A")
    prov = _llm(retriever=retr)
    run_discovery(prov, PolicyConfig())
    log = prov.memory_log
    assert "meadows" in log["method_pages_read"]
    assert not [r for r in retr.reads if r["access_class"] == "case" and r["allowed"]]


# 11 ─ CASE refused pre-snapshot ─────────────────────────────────────────────
def test_case_refused_pre_snapshot():
    retr = MemoryRetriever({"jpm-case": WikiPage(slug="jpm-case", access_class="case", type="theme",
                                                 frontmatter={"slug": "jpm-case"}, body="x")}, phase="A")
    assert retr.retrieve("jpm-case") is None
    assert "jpm-case" in retr.refusals


# 12 ─ capture / replay works without live API (deterministic) ───────────────
def test_capture_replay_deterministic(tmp_path):
    rec = LiveRunRecord(run_id="r1", timestamp="2026-06-08T00:00:00+00:00", model_name="claude-sonnet-4-6",
                        input_hash=input_hash("idea"), source_slugs=["jpm"],
                        validated_outputs={"axis": _AX}, final_strategy_families=["long_short"])
    path = write_run_record(rec, base_dir=str(tmp_path / "runs"), slug="jpm")
    assert path.exists()
    assert replay(path) == rec                          # deterministic round-trip
    assert revalidate(rec) == []                        # captured Axis still validates, no LLM
    rec.validated_outputs["axis"] = {"definition": "x"}  # tamper → invalid
    assert revalidate(rec)                              # revalidation catches it


# 13 ─ no trade legs / sizing / hedge / curve points / execution emitted ─────
def test_no_trade_output():
    theme, _ = run_discovery(_llm(), PolicyConfig())
    assert theme.pricing is None and theme.sizing is None and theme.expressions == []
    rec = LiveRunRecord(run_id="r", timestamp="2026-06-08T00:00:00+00:00", model_name="m",
                        input_hash=input_hash("x"),
                        no_trade_confirmation=(theme.pricing is None and theme.sizing is None
                                               and not theme.expressions))
    assert rec.no_trade_confirmation is True


# 14 ─ golden master unchanged ───────────────────────────────────────────────
def test_golden_master_unchanged():
    _, theme, _ = build_theme("ai_issuance.yaml")
    assert theme.pricing.scenario_fv == pytest.approx(GOLDEN_SCENARIO_FV, abs=ABS)
    assert theme.pricing.priced_in.q_s == pytest.approx(GOLDEN_Q, abs=ABS)
    assert theme.pricing.residual_edge == pytest.approx(GOLDEN_EDGE, abs=ABS)
