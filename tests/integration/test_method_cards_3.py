"""Method skill cards (batch 3) — the Tooley causal-asymmetry upgrade to causal-compiler and the
monetary-transmission supplements to system-mapper / macro-regime-classifier. Offline; mirrors
test_skills_batch2.py. Asserts each card encodes the extracted process primitive, that the SPEC/CASE
sources (Alaph, Taars) are NOT compiled into skill slugs, and that the golden master is unchanged.
"""
from __future__ import annotations

from engine.skills import (
    SEAM_TO_SKILLS,
    list_available_skills,
    load_skill_card,
    validate_skill_frontmatter,
)
from tests._helpers import ABS, GOLDEN_EDGE, GOLDEN_Q, GOLDEN_SCENARIO_FV, build_theme

UPDATED = ["causal-compiler", "system-mapper", "macro-regime-classifier"]


# ── existence + valid method frontmatter ─────────────────────────────────────
def test_updated_cards_exist_and_valid():
    for slug in UPDATED:
        assert slug in list_available_skills()
        assert validate_skill_frontmatter(load_skill_card(slug))


# ── causal-compiler: Tooley causal-asymmetry primitive ───────────────────────
def test_causal_asymmetry_counterfactual():
    card = load_skill_card("causal-compiler").lower()
    # asymmetry / direction of causation
    assert "causal asymmetry" in card or "asymmetry of dependence" in card
    # counterfactual dependence vs constant conjunction
    assert "counterfactual dependence" in card and "constant conjunction" in card
    # cause precedes / brings effect into being
    assert "precede" in card or "brings the effect into being" in card
    # provenance updated
    assert "tooley" in card
    # existing substrings preserved (do not break test_skills.py)
    assert "hyperscaler" in card and "project" in card
    assert "confounder" in card and "falsifier" in card


# ── system-mapper: transmission as stock/flow + loops ────────────────────────
def test_system_mapper_has_transmission_supplement():
    card = load_skill_card("system-mapper").lower()
    assert "transmission" in card
    assert "policy rate" in card and "asset price" in card
    assert "duration" in card and "term premium" in card
    assert "stock" in card and "flow" in card
    assert "reach-for-yield" in card or "search-for-yield" in card
    # existing Meadows primitives preserved
    assert "issuance" in card and "reinforcing" in card and "outstanding" in card


# ── macro-regime-classifier: transmission propagation primitive ──────────────
def test_macro_regime_has_transmission_primitive():
    card = load_skill_card("macro-regime-classifier").lower()
    assert "transmission" in card
    assert "policy rate" in card and "asset price" in card
    assert "duration" in card and "term premium" in card
    assert "stock" in card and "flow" in card
    assert "credit" in card and "channel" in card


# ── triage outcome: SPEC/CASE sources are NOT skill cards ─────────────────────
def test_alaph_and_taars_not_compiled_into_skills():
    avail = list_available_skills()
    for slug in ("alaph", "alaph-long-presentation", "taars", "xantium",
                 "xantimum", "avramov", "monetary-transmission"):
        assert slug not in avail


def test_no_new_card_wired_into_seams():
    # supplements are method-text only; SEAM_TO_SKILLS unchanged shape for the touched cards
    assert SEAM_TO_SKILLS["expand_causal"] == ["causal-compiler"]
    assert SEAM_TO_SKILLS["build_system_map"] == ["system-mapper"]
    assert SEAM_TO_SKILLS["macro_context"] == ["macro-regime-classifier"]


# ── golden master unchanged ──────────────────────────────────────────────────
def test_golden_master_unchanged():
    _, theme, _ = build_theme("ai_issuance.yaml")
    assert theme.pricing.scenario_fv == __import__("pytest").approx(GOLDEN_SCENARIO_FV, abs=ABS)
    assert theme.pricing.priced_in.q_s == __import__("pytest").approx(GOLDEN_Q, abs=ABS)
    assert theme.pricing.residual_edge == __import__("pytest").approx(GOLDEN_EDGE, abs=ABS)
