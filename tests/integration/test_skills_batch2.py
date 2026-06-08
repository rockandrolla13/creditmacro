"""New METHOD skill cards (batch 2) — evidence-weighting, priced-in-estimator, edge-validity,
plus the Ellenberg supplement to trap-detector. Registered but NOT auto-wired. Acceptance checks
that each compiled card encodes the right process primitive. Golden master unchanged.
"""
from __future__ import annotations

import pytest

from engine.cases import PolicyConfig
from engine.provider_select import run_discovery
from engine.skills import (
    PENDING_WIRING_SKILLS,
    READABLE_DISCOVERY_SKILLS,
    SEAM_TO_SKILLS,
    list_available_skills,
    load_skill_card,
    validate_skill_frontmatter,
)
from tests._helpers import ABS, GOLDEN_EDGE, GOLDEN_Q, GOLDEN_SCENARIO_FV, build_theme
from tests.integration.test_provider_selection import _llm

NEW = ["evidence-weighting", "priced-in-estimator", "edge-validity"]


# ── registration ─────────────────────────────────────────────────────────────
@pytest.mark.parametrize("slug", NEW)
def test_new_card_registered_and_valid(slug):
    assert slug in list_available_skills()                 # discoverable
    assert validate_skill_frontmatter(load_skill_card(slug))  # method frontmatter


def test_registry_now_has_nine_cards():
    avail = list_available_skills()
    assert len([s for s in avail]) >= 9
    for slug in NEW:
        assert slug in avail


# ── NOT auto-wired (Part 2) ──────────────────────────────────────────────────
def test_new_cards_not_wired_into_any_seam():
    wired = {s for skills in SEAM_TO_SKILLS.values() for s in skills}
    for slug in NEW:
        assert slug not in wired                           # no seam injects them
    assert "evidence-weighting" in PENDING_WIRING_SKILLS
    assert set(READABLE_DISCOVERY_SKILLS) == {"priced-in-estimator", "edge-validity"}


def test_discovery_run_does_not_inject_new_cards():
    prov = _llm()
    run_discovery(prov, PolicyConfig())
    for slug in NEW:
        assert slug not in prov.skills_loaded              # not injected during discovery


# ── acceptance: compiled cards encode the process primitive ──────────────────
def test_evidence_weighting_states_prior_likelihood_posterior():
    card = load_skill_card("evidence-weighting").lower()
    assert "base rate" in card and "prior" in card
    assert "likelihood" in card and "posterior" in card
    assert "labeling only" in card or "posterior == prior" in card   # not wired into Q4 yet


def test_priced_in_articulates_decomposition():
    card = load_skill_card("priced-in-estimator").lower()
    assert "risk premi" in card and "valuation" in card and "carry" in card
    assert "discount" in card                              # what is already priced in


def test_edge_validity_flags_momentum_crowding():
    card = load_skill_card("edge-validity").lower()
    assert "out-of-sample" in card and "overfit" in card
    assert "momentum" in card and "crowding" in card       # HPC-style hot run = crowding/overfit suspect


def test_trap_detector_has_ellenberg_supplement():
    card = load_skill_card("trap-detector").lower()
    assert "regression to the mean" in card and "survivorship" in card
    assert "linearity" in card and "ellenberg" in card


# ── golden master unchanged ──────────────────────────────────────────────────
def test_golden_master_unchanged():
    _, theme, _ = build_theme("ai_issuance.yaml")
    assert theme.pricing.scenario_fv == pytest.approx(GOLDEN_SCENARIO_FV, abs=ABS)
    assert theme.pricing.priced_in.q_s == pytest.approx(GOLDEN_Q, abs=ABS)
    assert theme.pricing.residual_edge == pytest.approx(GOLDEN_EDGE, abs=ABS)
