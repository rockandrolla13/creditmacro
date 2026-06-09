"""Wiki + agent scaling layer — PART 1 (registry) + PART 2 (SourceIntakeAgent).

The agents are role-specific, contract-bound workflows — NOT unconstrained autonomous agents.
PART 2 implements SourceIntakeAgent (deterministic classification); the other five are declared
with full contracts but their run() is a later part.
"""
from __future__ import annotations

import pytest

from engine.wiki_agents import (
    REGISTRY,
    AgentRegistry,
    SourceIntakeAgent,
    SourceIntakeInput,
    SourcePage,
)

EXPECTED_AGENTS = {
    "SourceIntakeAgent", "EvidenceExtractionAgent", "TemporalContextAgent",
    "SkillCompilerAgent", "WikiIntegratorAgent", "WikiLintAgent", "DiscoveryRunnerAgent",
}
_ALL_CONTRACT_FIELDS = (
    "agent_name", "purpose", "input_objects", "output_objects",
    "allowed_paths_to_read", "allowed_paths_to_write", "access_class_rules",
    "provider_seams_used", "non_goals", "tests_required",
)
# These may legitimately be empty: a classification-only agent writes nothing; a deterministic
# agent uses no provider seams. The rest must be meaningfully populated.
_MAY_BE_EMPTY = ("allowed_paths_to_write", "provider_seams_used")


# ── PART 1: registry ────────────────────────────────────────────────────────────

def test_registry_lists_all_agents():
    assert set(REGISTRY.list_agents()) == EXPECTED_AGENTS


def test_get_agent_returns_contract_bound_agent():
    a = REGISTRY.get_agent("SourceIntakeAgent")
    assert a.contract.agent_name == "SourceIntakeAgent"


def test_get_unknown_agent_raises():
    with pytest.raises(KeyError):
        REGISTRY.get_agent("NopeAgent")


def test_all_contracts_validate():
    assert REGISTRY.validate_agent_contracts() == []


def test_every_contract_declares_required_fields():
    for name in REGISTRY.list_agents():
        c = REGISTRY.get_agent(name).contract
        for f in _ALL_CONTRACT_FIELDS:
            assert hasattr(c, f), f"{name}.{f} must be declared"          # field present
            if f not in _MAY_BE_EMPTY:
                assert getattr(c, f) not in (None, "", []), f"{name}.{f} must be populated"


def test_unimplemented_agent_run_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        REGISTRY.run_agent("SkillCompilerAgent", {})


# ── PART 2: SourceIntakeAgent ────────────────────────────────────────────────────

def _intake(**kw):
    base = dict(source_slug="s", source_type="other", pages=[])
    base.update(kw)
    return SourceIntakeAgent().run(SourceIntakeInput(**base))


def test_book_classifies_as_method():
    c = _intake(source_slug="book-of-why", source_type="book")
    assert c.access_class == "method"
    assert "paraphrase" in c.copyright_status.lower() or "copyright" in c.copyright_status.lower()


def test_report_classifies_as_case():
    c = _intake(source_slug="jpm-ai-capex-funding-2026-05-11", source_type="report")
    assert c.access_class == "case"


def test_alaph_deck_is_mixed_with_per_page_classes():
    pages = [
        SourcePage(page_number=3, text="Our four-step investment process: theme, valuation, "
                   "trade selection, portfolio construction — the methodology we use to reason."),
        SourcePage(page_number=4, text="Liquidity scoring and the risk framework across the macro cycle."),
        SourcePage(page_number=9, text="Past performance: net returns since inception and AUM growth."),
        SourcePage(page_number=12, text="Worked trade example: the French bank basis — we recommend "
                   "the senior-vs-sovereign relative value position."),
    ]
    c = _intake(source_slug="alaph-long-presentation-2014", source_type="deck", pages=pages)
    by = {p.page_number: p.access_class for p in c.page_classifications}
    assert by[3] == "method"
    assert by[4] == "method"
    assert by[9] == "ignore"          # performance page is not a method rule
    assert by[12] == "case"           # specific trade example
    assert c.access_class == "mixed"  # method + case present


def test_alaph_performance_page_is_not_method():
    pages = [SourcePage(page_number=9, text="Past performance and track record: returns since inception.")]
    c = _intake(source_slug="alaph", source_type="deck", pages=pages)
    assert c.page_classifications[0].access_class in ("ignore", "case")
    assert c.page_classifications[0].access_class != "method"


def test_alaph_french_bank_example_is_case():
    pages = [SourcePage(page_number=12, text="French bank trade example: we recommend the senior basis position.")]
    c = _intake(source_slug="alaph", source_type="deck", pages=pages)
    assert c.page_classifications[0].access_class == "case"


def test_xantium_process_pages_are_method():
    pages = [
        SourcePage(page_number=2, text="Investment process and risk framework: how we decompose risk "
                   "and score liquidity across sub-strategies."),
        SourcePage(page_number=5, text="The valuation framework and decision methodology."),
    ]
    c = _intake(source_slug="xantium-business-plan", source_type="other", pages=pages)
    assert all(p.access_class == "method" for p in c.page_classifications)
    assert c.access_class == "method"


def test_jpm_source_is_case():
    c = _intake(source_slug="jpm-ai-capex-funding-2026-05-11", source_type="report")
    assert c.access_class == "case"
    assert "evidence" in " ".join(c.recommended_compilers).lower()


def test_deck_without_pages_warns():
    c = _intake(source_slug="some-deck", source_type="deck", pages=[])
    assert any("page" in w.lower() for w in c.warnings)


def test_method_recommends_skill_compiler():
    c = _intake(source_slug="meadows-thinking-in-systems", source_type="book")
    assert any("skill" in r.lower() for r in c.recommended_compilers)


# ── PART 7: method source regression (Pearl / Meadows / Alaph / Xantium) ──────────
#
# SourceIntakeAgent-level assertions (access_class / per-page method|case|mixed).
# Exercises the deterministic keyword classifier against the four canonical research-corpus
# authors. Temporal-role / claim-kind / allowed-Phase-A-use assertions for the same authors
# live in tests/integration/test_temporal_agent.py (PART 7).
#
# Grounding: text snippets are representative paraphrases of the real markdowns
#   (markdowns/The Book of Why ..., Thinking in Systems A Primer ..., Alaph Long
#    Presentation Version July 2014.md, XantimumBizPlan.md). The classifier reads keywords
#   off `text`, not wiki frontmatter, so the snippets carry the method/case signals.


def _pages(*texts):
    return [SourcePage(page_number=i + 1, text=t) for i, t in enumerate(texts)]


# Pearl / Causal Compiler — a method book teaching causal reasoning.
def test_pearl_causal_book_is_method():
    c = _intake(
        source_slug="pearl-book-of-why",
        source_type="book",
        pages=_pages(
            "The do-calculus is a causal reasoning framework that separates correlation "
            "from causation using the ladder of causation.",
        ),
    )
    assert c.access_class == "method"
    assert c.page_classifications[0].access_class == "method"
    # a copyrighted book is paraphrase-only and routes to the skill compiler
    assert "paraphrase" in c.copyright_status.lower()
    assert any("skill" in r.lower() for r in c.recommended_compilers)


# Meadows / System Mapper — a method book of system concepts (stocks/flows/feedback).
def test_meadows_system_book_is_method():
    c = _intake(
        source_slug="meadows-thinking-in-systems",
        source_type="book",
        pages=_pages(
            "Stocks and flows are the core system concepts; balancing and reinforcing "
            "feedback loops drive behaviour, and leverage points are where to intervene.",
        ),
    )
    assert c.access_class == "method"
    assert all(p.access_class == "method" for p in c.page_classifications)


# Alaph — process pages are method; past-performance page is NOT method; the French-bank
# worked example is case, not method.
def test_alaph_process_french_and_performance_split_by_page():
    c = _intake(
        source_slug="alaph-long-presentation-2014",
        source_type="deck",
        pages=_pages(
            "Our four-step investment process — theme, valuation, trade selection, "
            "portfolio construction — is the methodology we use to reason.",                 # 1 method
            "Past performance: net returns since inception and AUM growth across the fund.",  # 2 ignore
            "Worked trade example: the French bank basis — we recommend the "
            "senior-vs-sovereign relative value position.",                                  # 3 case
        ),
    )
    by = {p.page_number: p.access_class for p in c.page_classifications}
    assert by[1] == "method"        # process page teaches reasoning
    assert by[2] != "method"        # past-performance page is NOT a method rule
    assert by[2] == "ignore"
    assert by[3] == "case"          # French-bank worked example is case, not method
    assert c.access_class == "mixed"


def test_alaph_past_performance_page_is_not_method():
    c = _intake(
        source_slug="alaph-long-presentation-2014",
        source_type="deck",
        pages=_pages("Past performance and track record: returns since inception, net of fees."),
    )
    assert c.page_classifications[0].access_class != "method"


def test_alaph_french_bank_worked_example_is_case_not_method():
    c = _intake(
        source_slug="alaph-long-presentation-2014",
        source_type="deck",
        pages=_pages(
            "French bank trade example: we recommend the senior basis position vs the sovereign.",
        ),
    )
    assert c.page_classifications[0].access_class == "case"
    assert c.page_classifications[0].access_class != "method"


# Xantium — process / eligible-universe / ETF-flow-framework pages are method; a specific
# historical trade-like example is case.
def test_xantium_process_universe_and_etf_flow_pages_are_method():
    c = _intake(
        source_slug="xantium-business-plan",
        source_type="other",
        pages=_pages(
            "Investment process and risk framework: how we decompose risk and score "
            "liquidity across sub-strategies.",                                         # method
            "Eligible universe and liquidity scoring methodology used to screen "
            "instruments for each sub-strategy.",                                       # method
            "ETF-flow framework: the TAARSS positioning signal methodology that maps "
            "flows to consensus.",                                                      # method
        ),
    )
    assert all(p.access_class == "method" for p in c.page_classifications)
    assert c.access_class == "method"


def test_xantium_specific_trade_example_is_case():
    c = _intake(
        source_slug="xantium-business-plan",
        source_type="other",
        pages=_pages(
            "Specific trade: we were long the 5y CDX IG basis — a worked trade example "
            "from a prior book.",
        ),
    )
    assert c.page_classifications[0].access_class == "case"
    assert c.access_class == "case"


# ── PART 8: recent case regression (JPM AI Capex Funding) ─────────────────────────
#
# Intake-layer assertion for the real JPM source page
# (wiki/sources/jpm-ai-capex-funding-2026-05-11.md): a report must classify as CASE. The
# temporal-role / freshness assertions for the same source live in
# tests/integration/test_temporal_agent.py (PART 8).


def test_jpm_ai_capex_report_intake_is_case():
    c = _intake(source_slug="jpm-ai-capex-funding-2026-05-11", source_type="report")
    assert c.source_type == "report"
    assert c.access_class == "case"
