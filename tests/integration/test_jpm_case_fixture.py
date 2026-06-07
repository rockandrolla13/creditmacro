"""Regression tests: the on-disk JPM CASE fixture respects BOTH firewalls and produces
discovery-stage strategy-family routing WITHOUT becoming trade-ready.

Fixture assumptions:
- The on-disk CASE page is wiki/sources/jpm-ai-capex-funding-2026-05-11.md (+ 4 themes).
- The discovery "current input" is cases/discovery/jpm_ai_capex.yaml — a 5s30s curve thesis,
  so the router returns the engine's concrete curve family `steepener` (= the "curve" family in
  the plausibility check). The wiki theme priors (long_short, index_index_rv, …) are the report's
  RV framing; the fixture's current-input thesis is the steepener.
- No engine code is modified; no LLM seam, no parse_research_text, no scenario/probability
  invention, no sizing, no legs.
"""
from __future__ import annotations

import json

import pytest

from engine.case_loader import load_case
from engine.firewall import run_two_phase
from engine.memory import MemoryRetriever, load_wiki_pages, parse_wiki_page
from engine.scripted_provider import ScriptedProvider
from engine.workflow import run_workflow
from tests._helpers import (
    ABS,
    CASES_DIR,
    GOLDEN_EDGE,
    GOLDEN_OMEGA,
    GOLDEN_Q,
    GOLDEN_SCENARIO_FV,
    GOLDEN_SCORE,
    build_theme,
)

ROOT = CASES_DIR.parent
WIKI = ROOT / "wiki"
CASE_SLUG = "jpm-ai-capex-funding-2026-05-11"
JPM_FIXTURE = CASES_DIR / "discovery" / "jpm_ai_capex.yaml"
THEMES = [
    "ai-capex-funding-credit-ecosystem", "hyperscaler-project-bond-basis",
    "hy-hpc-crowding-and-supply", "data-center-index-inclusion-technicals",
]
CURVE_OR_RV = {"steepener", "flattener", "curve", "long_short",
               "index_index_rv", "etf_basket_rv", "watchlist_only"}


def _discovery_jpm(scenarios=None):
    case = load_case(JPM_FIXTURE)
    if scenarios is not None:
        case = case.model_copy(update={"scenarios": scenarios})
    theme, _ = run_workflow(ScriptedProvider(case), case.resolved_policy(), mode="discovery")
    return case, theme


def _atoms():
    lines = (WIKI / "evidence" / "evidence_atoms.jsonl").read_text().splitlines()
    return [json.loads(x) for x in lines if x.strip()]


# 1 ─ JPM source page exists and is CASE memory ──────────────────────────────
def test_jpm_source_page_is_case_memory():
    page = parse_wiki_page(WIKI / "sources" / f"{CASE_SLUG}.md")
    fm = page.frontmatter
    assert page.access_class == "case"
    assert fm.get("classification") == "source"
    assert fm.get("source_type") == "report"
    assert str(fm.get("source_date")) == "2026-05-11"


# 2 ─ Evidence atoms exist and are source-backed ─────────────────────────────
def test_evidence_atoms_present_and_source_backed():
    atoms = _atoms()
    assert atoms
    for a in atoms:
        assert a.get("source_slug")
        assert a.get("source_location") or a.get("page_number")
    blob = " ".join(a["claim"].lower() for a in atoms)
    # the full 10 required claims (incl. HPC index-weight 1.07->2.68% and the 295bp level)
    for needle in ["27 issuers", "450", "105bp", "183bp", "49bn", "4.8%", "0.5%",
                   "181bp", "101bp", "26.6", "43%", "1.07", "2.68", "9.99", "1.61", "295bp"]:
        assert needle in blob, f"missing evidence claim: {needle}"


# 3 ─ Theme cards cite evidence atoms ────────────────────────────────────────
@pytest.mark.parametrize("slug", THEMES)
def test_theme_cards_cite_evidence_atoms(slug):
    page = parse_wiki_page(WIKI / "themes" / f"{slug}.md")
    assert page.access_class == "case"
    assert "evidence:jpm-2026-05-11" in page.body          # links evidence atoms
    assert CASE_SLUG in (page.frontmatter.get("sources") or [])


# 4 ─ Current-input exception works (JPM used during discovery) ───────────────
def test_current_input_exception_runs_discovery():
    _, theme = _discovery_jpm()
    assert theme.status in ("strategy_family_routed", "discovery_complete")
    assert theme.status != "expression_complete"           # never trade-ready in discovery


# 5 ─ Archived case is blocked before FreshReasoningSnapshot (phase A) ────────
def test_archived_case_blocked_in_phase_a():
    pages = load_wiki_pages(WIKI)
    assert CASE_SLUG in pages and pages[CASE_SLUG].access_class == "case"
    r = MemoryRetriever(pages, phase="A")
    assert r.retrieve(CASE_SLUG) is None                    # fail-closed
    assert CASE_SLUG in r.refusals                          # refusal logged
    rec = next(x for x in r.reads if x["slug"] == CASE_SLUG)
    assert rec["access_class"] == "case" and rec["allowed"] is False
    # the frozen snapshot carries no JPM case content (its theme is the fresh discovery thesis)
    provider = ScriptedProvider(load_case(JPM_FIXTURE))
    result = run_two_phase(provider, load_case(JPM_FIXTURE).resolved_policy(), pages=pages)
    assert CASE_SLUG not in (result.fresh_reasoning.theme.statement or "")


# 6 ─ Archived case can be read AFTER FreshReasoningSnapshot (phase B) ────────
def test_archived_case_read_only_after_snapshot():
    retriever = MemoryRetriever(load_wiki_pages(WIKI), phase="A")
    provider = ScriptedProvider(load_case(JPM_FIXTURE))
    result = run_two_phase(provider, load_case(JPM_FIXTURE).resolved_policy(), retriever=retriever)
    case_reads = [x for x in retriever.reads if x["access_class"] == "case" and x["allowed"]]
    assert case_reads, "phase B should have read at least one case page"
    assert all(x["frozen_before_read"] for x in case_reads)   # every case read came AFTER freeze
    assert result.post_case_calibration is not None           # additive calibration only


# 7 ─ Case memory cannot mutate fresh reasoning ──────────────────────────────
def test_case_read_does_not_mutate_fresh_reasoning():
    _, fresh = _discovery_jpm()                               # phase-A reasoning, no case memory
    retriever = MemoryRetriever(load_wiki_pages(WIKI), phase="A")
    provider = ScriptedProvider(load_case(JPM_FIXTURE))
    result = run_two_phase(provider, load_case(JPM_FIXTURE).resolved_policy(), retriever=retriever)
    frozen = result.fresh_reasoning.theme
    assert frozen.causal_chain == fresh.causal_chain
    assert frozen.axis == fresh.axis
    assert [(f.family, f.confidence) for f in frozen.strategy_families] == \
           [(f.family, f.confidence) for f in fresh.strategy_families]
    assert frozen.probability_justification == fresh.probability_justification
    # calibration is additive: recorded adjustments never silently change fresh confidence
    for adj in result.post_case_calibration.confidence_adjustments:
        assert adj.adjusted_confidence == adj.fresh_confidence


# 8 ─ Discovery output is not trade-ready ────────────────────────────────────
def test_discovery_output_not_trade_ready():
    _, theme = _discovery_jpm()
    assert theme.status in ("strategy_family_routed", "discovery_complete")
    assert theme.pricing is None
    assert theme.sizing is None
    assert theme.expressions == []                           # no detailed legs / hedge ratios / curve points


# 9 ─ Strategy-family ranking looks plausible ────────────────────────────────
def test_strategy_family_ranking_plausible():
    _, theme = _discovery_jpm()
    fams = [f.family for f in theme.strategy_families]
    assert fams, "discovery should route at least one family"
    assert fams[0] in CURVE_OR_RV                            # a curve/RV family, not outright
    assert not (fams == ["outright"]), "outright must not be the only family without a caveat"
    assert theme.strategy_families[0].confidence_components is not None


# 10 ─ Q4 behavior with no scenarios (none invented) ─────────────────────────
def test_q4_no_scenarios_invents_nothing():
    _, theme = _discovery_jpm(scenarios=[])
    assert theme.probability_justification is None           # no scenarios ⇒ no p_s invented
    cc = theme.strategy_families[0].confidence_components
    assert cc.scenario_availability is False                 # capped per missing-scenario rule


# 11 ─ Existing golden master unchanged ──────────────────────────────────────
def test_golden_master_unchanged():
    case, theme, _ = build_theme("ai_issuance.yaml")         # expression mode
    assert theme.pricing.scenario_fv == pytest.approx(GOLDEN_SCENARIO_FV, abs=ABS)
    assert theme.pricing.priced_in.q_s == pytest.approx(GOLDEN_Q, abs=ABS)
    assert theme.pricing.residual_edge == pytest.approx(GOLDEN_EDGE, abs=ABS)
    best = max((e for e in theme.expressions if e.score is not None), key=lambda e: e.score)
    assert best.score == pytest.approx(GOLDEN_SCORE, abs=ABS)
