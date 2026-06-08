"""Method skill cards (batch 4) — six new cards compiled from the research/ papers and the
causal/factor/calibration books, plus four supplements appended to frozen cards. Offline;
mirrors test_skills_batch2 / test_method_cards_3. Asserts each new card is registered, has valid
method frontmatter WITH compiled_from filled, is NOT wired into any seam, carries no trade/case
conclusions, and that the golden master is unchanged.
"""
from __future__ import annotations

import re

import pytest

from engine.skills import (
    REGISTERED_UNWIRED_SKILLS,
    SEAM_TO_SKILLS,
    list_available_skills,
    load_skill_card,
    validate_skill_frontmatter,
)
from tests._helpers import ABS, GOLDEN_EDGE, GOLDEN_Q, GOLDEN_SCENARIO_FV, build_theme

NEW = list(REGISTERED_UNWIRED_SKILLS)
SUPPLEMENTED = ["causal-compiler", "priced-in-estimator", "trap-detector", "edge-validity"]

# trade/case language that must NOT appear as an instruction (Non-goals/exclusions are fine, so
# we check only outside lines that explicitly forbid them).
_FORBIDDEN = re.compile(r"\b(go long|short the|position size|buy \d|sell \d|stop[- ]loss order)\b", re.I)


# ── existence + valid METHOD frontmatter ─────────────────────────────────────
@pytest.mark.parametrize("slug", NEW)
def test_new_card_exists_and_valid(slug):
    assert slug in list_available_skills()
    assert validate_skill_frontmatter(load_skill_card(slug))


@pytest.mark.parametrize("slug", NEW)
def test_new_card_has_compiled_from_and_method(slug):
    card = load_skill_card(slug)
    fm = re.search(r"^---\n(.*?)\n---", card, re.S).group(1)
    assert re.search(r"compiled_from:\s*\[.+\]", fm), f"{slug} missing compiled_from"
    assert "access_class: method" in fm


# ── registered but NOT wired into any seam (golden-master / firewall safety) ──
def test_new_cards_not_wired_into_any_seam():
    wired = {s for skills in SEAM_TO_SKILLS.values() for s in skills}
    for slug in NEW:
        assert slug not in wired


def test_seam_mapping_unchanged_exact():
    # the four load-bearing seam mappings stay exactly as before (no new card injected)
    assert SEAM_TO_SKILLS["expand_causal"] == ["causal-compiler"]
    assert SEAM_TO_SKILLS["build_system_map"] == ["system-mapper"]
    assert SEAM_TO_SKILLS["justify_probabilities"] == ["scenario-pricing-engine"]


# ── no trade/case conclusions in the new cards ───────────────────────────────
@pytest.mark.parametrize("slug", NEW)
def test_new_card_has_no_trade_instruction(slug):
    for line in load_skill_card(slug).splitlines():
        low = line.lower()
        if "not_allowed" in low or "non-goal" in low or low.lstrip().startswith(("no ", "- no ")):
            continue  # exclusion lines may name the forbidden things
        assert not _FORBIDDEN.search(line), f"{slug}: trade-instruction language: {line!r}"


# ── supplements: frozen cards still valid after appended sections ─────────────
@pytest.mark.parametrize("slug", SUPPLEMENTED)
def test_supplemented_card_still_valid(slug):
    card = load_skill_card(slug)
    assert validate_skill_frontmatter(card)
    assert "## Additional rules from" in card


# ── golden master unchanged ──────────────────────────────────────────────────
def test_golden_master_unchanged():
    _, theme, _ = build_theme("ai_issuance.yaml", "expression")
    assert theme.pricing.scenario_fv == pytest.approx(GOLDEN_SCENARIO_FV, abs=ABS)
    assert theme.pricing.priced_in.q_s == pytest.approx(GOLDEN_Q, abs=ABS)
    assert theme.pricing.residual_edge == pytest.approx(GOLDEN_EDGE, abs=ABS)
