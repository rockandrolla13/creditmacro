"""MacroContext discovery seam (Part: macro_context).

A METHOD-only discovery CONTEXT CLASSIFIER — qualitative regime tags, never probabilities,
scenarios, or trades. Tests run OFFLINE via a fake Anthropic client (no network), reusing the
routing-fake pattern from test_provider_selection. They assert: the schema round-trips, the
LLM seam validates with method+case memory but reads NO case page, a discovery run attaches
theme.macro_context yet still STOPS at strategy_family_routed (pricing/sizing/expressions stay
None/[]), the macro-poor "unclear" path, the golden master is unchanged, and expression mode
remains fenced off the discovery-only provider.
"""
from __future__ import annotations

import json

import pytest

from engine.cases import PolicyConfig
from engine.llm_provider import LLMProvider
from engine.memory import MemoryRetriever, WikiPage
from engine.provider_select import run_discovery
from engine.schema import MacroContext
from engine.workflow import run_workflow
from tests._helpers import ABS, GOLDEN_EDGE, GOLDEN_Q, GOLDEN_SCENARIO_FV, build_theme
from tests.integration.test_provider_selection import _MACRO, _RoutingFake, _llm


# canned MacroContext for a macro-POOR input → unclear + missing_data
_MACRO_UNCLEAR = json.dumps({
    "input_kind": "idea", "macro_regime_tags": ["unclear"],
    "growth_bias": "unclear", "inflation_bias": "unclear", "policy_bias": "unclear",
    "liquidity_bias": "unclear", "credit_cycle_bias": "unclear", "horizon": "unclear",
    "affected_asset_classes": [], "affected_strategy_families_hint": [],
    "confidence": 0.1, "evidence_refs": [],
    "missing_data": ["no growth/inflation/policy signal in the input", "no dated observations"],
    "rationale": "input is a bare idea with no macro evidence", "warnings": []})


def _macro_llm(retriever=None):
    """LLMProvider whose fake client routes the macro prompt to canned MacroContext JSON."""
    return LLMProvider(
        client=_RoutingFake(), research_text="AI capex RV across hyperscalers and project bonds",
        current_input_axes=["project_bond_OAS_minus_related_hyperscaler_OAS"],
        current_sources=["jpm-ai-capex-funding-2026-05-11"], retriever=retriever)


# 1 ─ schema validates + round-trips, incl. the unclear/missing_data shape ────
def test_macro_context_schema_round_trips():
    mc = MacroContext(
        input_kind="idea", macro_regime_tags=["unclear"],
        growth_bias="unclear", inflation_bias="unclear", policy_bias="unclear",
        liquidity_bias="unclear", credit_cycle_bias="unclear", horizon="unclear",
        missing_data=["no macro signal"])
    assert mc.macro_regime_tags == ["unclear"]
    assert mc.missing_data == ["no macro signal"]
    # tags are qualitative, not probabilities — defaults are advisory/empty
    assert mc.affected_strategy_families_hint == [] and mc.confidence == 0.0
    again = MacroContext.model_validate(json.loads(mc.model_dump_json()))
    assert again == mc


# 2 ─ LLM seam returns a valid MacroContext from a fake client ────────────────
def test_macro_context_seam_validates():
    mc = _macro_llm().macro_context("AI capex theme", None)
    assert isinstance(mc, MacroContext)
    assert "policy_tightening" in mc.macro_regime_tags
    # advisory hint recorded; never empty for this canned regime
    assert mc.affected_strategy_families_hint


# 3 ─ macro seam injects the METHOD card, reads NO case memory ────────────────
def test_macro_context_reads_method_only():
    pages = {
        "macro-method": WikiPage(slug="macro-method", access_class="method", type="concept",
                                 frontmatter={"slug": "macro-method"}, body="growth inflation policy liquidity"),
        "jpm-case": WikiPage(slug="jpm-case", access_class="case", type="theme",
                             frontmatter={"slug": "jpm-case"}, body="a prior conclusion"),
    }
    retr = MemoryRetriever(pages, phase="A")
    prov = _macro_llm(retriever=retr)
    mc = prov.macro_context("AI capex theme", None)
    assert isinstance(mc, MacroContext)
    # the macro-regime-classifier METHOD card was injected (recorded for capture)
    assert "macro-regime-classifier" in prov.skills_loaded
    assert "macro-regime-classifier" in prov.skill_card_hashes
    # NO allowed case read occurred in phase A
    case_reads = [r for r in retr.reads if r["access_class"] == "case" and r["allowed"]]
    assert not case_reads


# 4 ─ discovery run attaches theme.macro_context, still STOPS at routing ──────
def test_discovery_attaches_macro_context_and_stops():
    theme, _ = run_discovery(_llm(), PolicyConfig())
    assert theme.status in ("strategy_family_routed", "discovery_complete")
    assert isinstance(theme.macro_context, MacroContext)
    assert theme.macro_context.macro_regime_tags  # populated from the routing fake
    # discovery deliverable only — no detailed expression half
    assert theme.pricing is None and theme.sizing is None and theme.expressions == []


# 5 ─ macro-poor input → ["unclear"] + non-empty missing_data ─────────────────
def test_macro_unclear_path_populates_missing_data():
    class _UnclearFake(_RoutingFake):
        class _M(_RoutingFake._M):
            def create(self, *, system, messages, **kw):
                if "MACRO REGIME CONTEXT CLASSIFIER" in system:
                    self.o.systems.append(system)
                    from tests.integration.test_provider_selection import _Resp
                    return _Resp(_MACRO_UNCLEAR)
                return super().create(system=system, messages=messages, **kw)
        @property
        def messages(self):
            return _UnclearFake._M(self)

    prov = LLMProvider(client=_UnclearFake(),
                       research_text="a bare idea with no macro signal",
                       current_input_axes=["project_bond_OAS_minus_related_hyperscaler_OAS"],
                       current_sources=["idea-note"])
    mc = prov.macro_context("a bare idea", None)
    assert mc.macro_regime_tags == ["unclear"]
    assert mc.missing_data  # non-empty: what's absent is recorded, not fabricated


# 6 ─ golden master unchanged ─────────────────────────────────────────────────
def test_golden_master_unchanged():
    _, theme, _ = build_theme("ai_issuance.yaml")
    assert theme.pricing.scenario_fv == pytest.approx(GOLDEN_SCENARIO_FV, abs=ABS)
    assert theme.pricing.priced_in.q_s == pytest.approx(GOLDEN_Q, abs=ABS)
    assert theme.pricing.residual_edge == pytest.approx(GOLDEN_EDGE, abs=ABS)
    # scripted/golden path carries NO macro context (provider returns None)
    assert theme.macro_context is None


# 7 ─ expression mode stays fenced off the discovery-only LLM provider ────────
def test_expression_mode_still_fenced():
    with pytest.raises(RuntimeError, match="expression_mode_not_supported"):
        run_workflow(_macro_llm(), PolicyConfig(), mode="expression")


# keep the imported canned macro JSON referenced (routing-fake contract) ──────
def test_routing_fake_macro_json_is_valid_macro_context():
    MacroContext.model_validate(json.loads(_MACRO))
