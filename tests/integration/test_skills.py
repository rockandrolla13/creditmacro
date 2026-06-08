"""Skill cards + registry + wiring + firewall integrity (Part 7).

Skill cards are METHOD memory compiled from markdowns/ sources. Tests check existence,
frontmatter, registry fail-closed behaviour, injection into LLM prompts (offline fake client),
that injection never reads CASE memory, capture logging, the discovery firewall, and that the
compiled cards encode the required process primitives. Golden master unchanged.
"""
from __future__ import annotations

import json

import pytest

from engine.cases import PolicyConfig
from engine.live_discovery import run_live_discovery
from engine.memory import MemoryRetriever, WikiPage
from engine.provider_select import run_discovery
from engine.skills import (
    SEAM_TO_SKILLS,
    MissingSkillCard,
    SKILLS_DIR,
    load_skill_card,
    load_skills_for_seam,
    validate_skill_frontmatter,
)
from engine.workflow import run_workflow
from tests._helpers import ABS, GOLDEN_EDGE, GOLDEN_Q, GOLDEN_SCENARIO_FV, build_theme
from tests.integration.test_provider_selection import _RoutingFake, _llm

SLUGS = ["iceberg-classifier", "causal-compiler", "system-mapper",
         "trap-detector", "scenario-pricing-engine", "macro-regime-classifier"]


# ── existence ────────────────────────────────────────────────────────────────
def test_all_six_skill_cards_exist():                                   # 1
    for slug in SLUGS:
        assert (SKILLS_DIR / slug / "SKILL.md").exists(), slug
    assert (SKILLS_DIR / "README.md").exists()


@pytest.mark.parametrize("slug", SLUGS)
def test_card_frontmatter(slug):                                        # 2
    card = load_skill_card(slug)
    assert validate_skill_frontmatter(card)                             # skill_name/access_class=method/...
    for key in ("skill_name", "access_class: method", "pipeline_phase",
                "provider_seam", "input_objects", "output_objects"):
        assert key in card


# ── registry ─────────────────────────────────────────────────────────────────
def test_registry_loads_all_six():                                     # 3
    for slug in SLUGS:
        assert load_skill_card(slug).startswith("---")


def test_seam_to_skill_mapping():                                      # 4
    assert SEAM_TO_SKILLS["expand_causal"] == ["causal-compiler"]
    assert SEAM_TO_SKILLS["build_system_map"] == ["system-mapper"]
    assert SEAM_TO_SKILLS["diagnose_loops"] == ["trap-detector"]
    assert SEAM_TO_SKILLS["justify_probabilities"] == ["scenario-pricing-engine"]


def test_missing_card_fails_closed():                                  # 5
    with pytest.raises(MissingSkillCard):
        load_skill_card("does-not-exist")


# ── wiring ───────────────────────────────────────────────────────────────────
class _CapFake(_RoutingFake):
    def __init__(self, axis=None):
        super().__init__() if axis is None else super().__init__(axis)
        self.user = []
    class _M:
        def __init__(self, o): self.o = o
        def create(self, *, system, messages, **kw):
            self.o.systems.append(system); self.o.user.append(messages[0]["content"])
            return _RoutingFake._M(self.o).create(system=system, messages=messages, **kw)
    @property
    def messages(self): return _CapFake._M(self)


def test_skills_injected_into_prompts():                               # 6
    fake = _CapFake()
    from engine.llm_provider import LLMProvider
    prov = LLMProvider(client=fake, research_text="x", current_input_axes=["a_minus_b"])
    run_discovery(prov, PolicyConfig())
    assert prov.skills_loaded                                          # cards recorded
    blob = "\n".join(fake.user)
    assert "METHOD SKILLS" in blob and "# skill: system-mapper" in blob  # injected into user content


def test_skill_injection_reads_no_case_memory():                      # 7
    pages = {"meadows": WikiPage(slug="meadows", access_class="method", type="concept",
                                 frontmatter={"slug": "meadows"}, body="stocks flows"),
             "jpm-case": WikiPage(slug="jpm-case", access_class="case", type="theme",
                                  frontmatter={"slug": "jpm-case"}, body="prior conclusion")}
    retr = MemoryRetriever(pages, phase="A")
    run_discovery(_llm(retriever=retr), PolicyConfig())
    assert not [r for r in retr.reads if r["access_class"] == "case" and r["allowed"]]


def test_skills_logged_in_capture(tmp_path):                          # 8
    res = run_live_discovery(research_text="AI capex RV", current_input_axes=["a_minus_b"],
                             client=_RoutingFake(), env={}, timestamp="2026-06-08T00:00:00+00:00",
                             capture_dir=str(tmp_path / "runs"), slug="s")
    assert res.record.skills_loaded
    assert res.record.skill_card_hashes
    assert set(res.record.skill_card_hashes) == set(res.record.skills_loaded)


# ── firewall integrity ───────────────────────────────────────────────────────
def test_discovery_stops_at_routing_or_blocked():                     # 9
    theme, _ = run_discovery(_llm(), PolicyConfig())
    assert theme.status in ("strategy_family_routed", "discovery_complete", "blocked")


def test_no_trade_output_in_discovery():                              # 10
    theme, _ = run_discovery(_llm(), PolicyConfig())
    assert theme.pricing is None and theme.sizing is None and theme.expressions == []


def test_expression_mode_fenced():                                   # 11
    with pytest.raises(RuntimeError, match="expression_mode_not_supported"):
        run_workflow(_llm(), PolicyConfig(), mode="expression")


# ── compiled-card process primitives (acceptance) ────────────────────────────
def test_iceberg_card_encodes_layers():                              # 12
    card = load_skill_card("iceberg-classifier").lower()
    assert "hot topic" in card and "not" in card and "investable" in card   # hot_topic ≠ investable
    assert "core theme candidate" in card and "causal" in card and "axis" in card
    assert "key event" in card and ("date" in card or "catalyst" in card)


def test_causal_card_encodes_chain():                               # 13
    card = load_skill_card("causal-compiler").lower()
    assert "hyperscaler" in card and "project" in card                  # driver→...→project bond
    assert "confounder" in card and "falsifier" in card


def test_system_mapper_card_stock_flow_loop():                      # 14
    card = load_skill_card("system-mapper").lower()
    assert "issuance" in card and "flow" in card
    assert "outstanding" in card and "stock" in card
    assert "reinforcing" in card and "performance" in card and "tightening" in card


def test_trap_card_success_to_successful():                         # 15
    card = load_skill_card("trap-detector").lower()
    assert "success-to-the-successful" in card and "crowding" in card


# ── golden master ────────────────────────────────────────────────────────────
def test_golden_master_unchanged():                                 # 16 / 17
    _, theme, _ = build_theme("ai_issuance.yaml")
    assert theme.pricing.scenario_fv == pytest.approx(GOLDEN_SCENARIO_FV, abs=ABS)
    assert theme.pricing.priced_in.q_s == pytest.approx(GOLDEN_Q, abs=ABS)
    assert theme.pricing.residual_edge == pytest.approx(GOLDEN_EDGE, abs=ABS)
