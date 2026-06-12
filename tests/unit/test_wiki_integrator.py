"""WikiIntegratorAgent — durable wiki-persistence layer (DELIVERABLE 3).

Covers the 7 required categories — dry-run, apply, idempotency, access_class, link resolution,
no-trade leakage, no-copyright leakage — plus required frontmatter keys + section headers per
page type. All tests write into a pytest tmp_path wiki_root; the real wiki/ is never touched.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import pytest

from engine.evidence_extraction import (
    CausalClaimCandidate,
    EvidenceExtractionBundle,
    OperationalAxisCandidate,
    StrategyFamilyHint,
)
from engine.schema import EvidenceAtom
from engine.schema.theme_aggregation import (
    EvidenceBullet,
    MultiSourceThemeSet,
    SourceAttribution,
    ThemeCluster,
)
from engine.temporal import TemporalContext
from engine.wiki_agents import REGISTRY, SourceClassification, run_agent
from engine.wiki_integration import (
    WikiIntegratorInput,
    build_wiki_update_plan,
    integrate,
)


# ── fixtures ─────────────────────────────────────────────────────────────────────

def _atom(eid="ev-1", **kw):
    base = dict(
        evidence_id=eid,
        source_slug="acme-credit-report-2026-05-01",
        source_location="page:7",
        claim="Investment-grade OAS widened as primary issuance surged into a softer demand window.",
        claim_kind="source_fact",
        claim_type="observation",
        entities=["JULI", "technology"],
        concepts=["spread dispersion", "primary supply"],
        themes=["primary supply pressure"],
        market_variables=["OAS", "issuance"],
        numbers=[12.0],
        confidence=0.7,
        freshness=0.8,
        agent_use="supports the primary-supply pressure theme",
    )
    base.update(kw)
    return EvidenceAtom(**base)


def _bundle(slug="acme-credit-report-2026-05-01", atoms=None, themes=None):
    return EvidenceExtractionBundle(
        source_slug=slug,
        source_page_fields={"source_type": "report", "author_or_publisher": "Acme Research",
                            "source_date": "2026-05-01"},
        evidence_atoms=atoms if atoms is not None else [_atom()],
        main_developments=["Primary issuance surge in May"],
        key_events=["May supply window"],
        hot_topics=["AI capex funding"],
        core_theme_candidates=themes if themes is not None else ["primary supply pressure"],
        causal_claims=[CausalClaimCandidate(
            driver="primary issuance", transmission="supply/demand imbalance",
            outcome="wider OAS", confidence=0.6, rationale="more paper than demand widens spread")],
        operational_axes=[OperationalAxisCandidate(
            axis_name="IG OAS level", axis_shape="level",
            observable_series="JULI OAS daily series")],
        confounders=["rating mix", "duration"],
        falsifiers=["OAS tightens despite rising issuance over 4 weeks"],
        strategy_family_hints=[StrategyFamilyHint(
            family="relative_value", rationale="cross-sector dispersion", confidence=0.5)],
        open_questions=["does demand recover post-window?"],
    )


def _classification(slug="acme-credit-report-2026-05-01", access="case", stype="report"):
    return SourceClassification(
        source_slug=slug, source_type=stype, access_class=access,
        copyright_status="copyrighted_paraphrase_only",
        ingestion_policy="extract_evidence_atoms_case",
        recommended_compilers=["EvidenceExtractionAgent", "WikiIntegratorAgent"],
    )


def _temporal(slug="acme-credit-report-2026-05-01", role="current_report",
              cur="2026-06-12", sd="2026-05-01"):
    return TemporalContext(
        source_slug=slug, source_date=date.fromisoformat(sd),
        current_date=date.fromisoformat(cur), temporal_role=role,
        current_update_required=False)


def _theme_set(slug="acme-credit-report-2026-05-01"):
    cluster = ThemeCluster(
        cluster_id="cluster-primary-supply",
        canonical_theme_name="Primary supply pressure",
        canonical_thesis="A heavy primary calendar into soft demand widens IG spreads.",
        theme_status="watchlist",
        source_attributions=[SourceAttribution(
            source_slug=slug, source_type="report", access_class="case",
            temporal_role="current_report", is_current_input=True,
            evidence_ids=["ev-1"], contribution_type="supports",
            rationale="primary supply evidence")],
        evidence_ids=["ev-1"],
        evidence_bullets=[EvidenceBullet(text="Issuance surged in May", evidence_ids=["ev-1"],
                                         source_slugs=[slug])],
        independent_source_count=1,
        corroboration_score=0.4, attention_score=0.2, evidence_attention_divergence=0.2,
        promotion_score=0.3,
        operational_axes=["IG OAS level"], causal_claims=["issuance -> wider OAS"],
        confounders=["rating mix"], falsifiers=["OAS tightens despite issuance"],
        strategy_family_hints=["relative_value"], missing_data=["forward calendar"])
    return MultiSourceThemeSet(
        batch_id="batch-1", source_scope="explicit_current_batch",
        source_slugs=[slug], clusters=[cluster])


def _input(tmp_path, **kw):
    base = dict(
        source_classification=_classification(),
        bundle=_bundle(),
        temporal_context=_temporal(),
        theme_set=_theme_set(),
        wiki_root=str(tmp_path / "wiki"),
    )
    base.update(kw)
    return WikiIntegratorInput(**base)


def _files(wiki_root) -> list[Path]:
    return list(Path(wiki_root).rglob("*.md"))


# ── 1. dry-run ───────────────────────────────────────────────────────────────────

def test_dry_run_writes_nothing(tmp_path):
    inp = _input(tmp_path, dry_run=True)
    res = integrate(inp)
    assert res.applied is False
    assert res.plan.writes, "plan should contain planned writes"
    assert _files(inp.wiki_root) == [], "dry-run must not create any files"


# ── 2. apply ─────────────────────────────────────────────────────────────────────

def test_apply_writes_expected_pages(tmp_path):
    inp = _input(tmp_path)
    res = integrate(inp)
    assert res.applied is True
    root = Path(inp.wiki_root)
    assert (root / "sources" / "acme-credit-report-2026-05-01.md").exists()
    assert (root / "evidence" / "ev-1.md").exists()
    assert (root / "themes" / "acme-credit-report-2026-05-01-primary-supply-pressure.md").exists()
    assert (root / "theme-clusters" / "cluster-primary-supply.md").exists()
    for f in ("index.md", "log.md", "memory-map.md"):
        assert (root / f).exists(), f"{f} must be updated"
    assert res.written_paths


# ── 3. idempotency ───────────────────────────────────────────────────────────────

def test_idempotent_second_run_skips(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    files_after_first = sorted(p.name for p in _files(inp.wiki_root))
    res2 = integrate(_input(tmp_path))
    files_after_second = sorted(p.name for p in _files(inp.wiki_root))
    assert files_after_first == files_after_second, "no new/duplicate files on second run"
    assert res2.skipped_paths, "second run should skip identical pages"
    # the create pages (source/evidence/theme/cluster) must all be skipped, not rewritten
    assert any("sources" in p for p in res2.skipped_paths)
    assert any("evidence" in p for p in res2.skipped_paths)


# ── 4. access_class ──────────────────────────────────────────────────────────────

def test_case_source_stamps_case_everywhere(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    root = Path(inp.wiki_root)
    src = (root / "sources" / "acme-credit-report-2026-05-01.md").read_text()
    assert "access_class: case" in src
    theme = (root / "themes"
             / "acme-credit-report-2026-05-01-primary-supply-pressure.md").read_text()
    assert "access_class: case" in theme
    ev = (root / "evidence" / "ev-1.md").read_text()
    assert "access_class: case" in ev


def test_method_source_yields_no_case_evidence_pages(tmp_path):
    inp = _input(
        tmp_path,
        source_classification=_classification(slug="pearl-book-of-why", access="method",
                                              stype="book"),
        bundle=_bundle(slug="pearl-book-of-why"),
        temporal_context=_temporal(slug="pearl-book-of-why", role="method_source"),
        theme_set=None,
    )
    res = integrate(inp)
    root = Path(inp.wiki_root)
    # source page exists and is stamped method (never upgraded/downgraded)
    src = (root / "sources" / "pearl-book-of-why.md").read_text()
    assert "access_class: method" in src
    # NO case-evidence pages, NO case theme cards from method content
    assert not (root / "evidence").exists() or not list((root / "evidence").glob("*.md"))
    assert not (root / "themes").exists() or not list((root / "themes").glob("*.md"))
    assert any("method source" in w for w in res.warnings)


def test_case_never_upgraded_to_method(tmp_path):
    inp = _input(tmp_path)
    plan = build_wiki_update_plan(inp)
    # the source page is stamped the source's access_class verbatim; evidence/theme are case
    src_write = next(w for w in plan.writes if w.kind == "source")
    assert src_write.access_class == "case"
    for w in plan.writes:
        if w.kind in ("evidence", "theme", "theme_cluster"):
            assert w.access_class == "case"
            assert "access_class: method" not in w.content


# ── 5. link resolution ───────────────────────────────────────────────────────────

def test_index_wikilinks_resolve(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    root = Path(inp.wiki_root)
    index = (root / "index.md").read_text()
    slugs = re.findall(r"\[\[([^\]]+)\]\]", index)
    assert slugs, "index should contain wikilinks"
    # every appended wikilink must resolve to a file that was created somewhere under the root
    created = {p.stem for p in _files(inp.wiki_root)}
    for slug in slugs:
        assert slug in created, f"wikilink [[{slug}]] does not resolve to a created file"


# ── 6. no trade leakage ──────────────────────────────────────────────────────────

_TRADE_WORDS = ("buy ", "sell ", "go long", "short ", "hedge ratio", "notional",
                "position size", "stop loss", "bps target")


def test_generated_pages_have_no_trade_language(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    for page in _files(inp.wiki_root):
        body = page.read_text().lower()
        # strip the mandatory "no trades, sizing, hedge ratios" boundary line before scanning
        body = body.replace(
            "no trades, sizing, hedge ratios, or execution.", "")
        for kw in _TRADE_WORDS:
            assert kw not in body, f"{page.name} leaked trade language '{kw}'"


def test_page_with_trade_instruction_is_blocked(tmp_path):
    atoms = [_atom(eid="ev-trade",
                   claim="We recommend buy 50mm of the 5s30s steepener as the core position size.")]
    inp = _input(
        tmp_path,
        bundle=_bundle(atoms=atoms, themes=["buy 50mm steepener now"]),
        theme_set=None,
    )
    plan = build_wiki_update_plan(inp)
    assert plan.blocked, "trade-bearing pages must be blocked"
    written_paths = {w.path for w in plan.writes}
    assert not any("ev-trade.md" in p for p in written_paths), "trade evidence page must not be planned"
    res = integrate(inp)
    assert not (Path(inp.wiki_root) / "evidence" / "ev-trade.md").exists()


# ── 7. no copyright leakage ──────────────────────────────────────────────────────

def test_long_verbatim_passage_is_not_written(tmp_path):
    verbatim = (
        "the quarterly outlook described a sustained widening of investment grade spreads "
        "driven by a heavy primary calendar colliding with a softer demand backdrop across "
        "the technology and financial sectors over the coming weeks of the period")
    assert len(verbatim.split()) >= 25
    # plant the verbatim passage as if an atom accidentally copied it
    atoms = [_atom(eid="ev-copy", claim=verbatim)]
    inp = _input(
        tmp_path,
        bundle=_bundle(atoms=atoms, themes=["primary supply pressure"]),
        theme_set=None,
        raw_text="PROLOGUE. " + verbatim + " END.",
    )
    plan = build_wiki_update_plan(inp)
    assert any("verbatim" in b for b in plan.blocked), "verbatim page must be copyright-blocked"
    integrate(inp)
    for page in _files(inp.wiki_root):
        assert verbatim not in page.read_text(), f"{page.name} leaked the verbatim passage"


# ── frontmatter keys + section headers per page type ─────────────────────────────

_SOURCE_FM_KEYS = [
    "type:", "classification:", "workflow_status:", "access_class:", "source_type:",
    "source_date:", "temporal_role:", "current_update_required:", "author_or_publisher:",
    "raw_source_path:", "normalized_markdown_path:", "ingestion_status:", "evidence_atoms:",
    "themes:", "theme_clusters:", "concepts:", "entities:", "created:", "updated:",
]
_SOURCE_SECTIONS = [
    "# Source Summary", "## What this source is", "## Temporal status", "## Why it matters",
    "## Main developments mentioned", "## Key events mentioned",
    "## Core theme candidates mentioned", "## Hot topics mentioned", "## Extracted facts",
    "## Extracted causal claims", "## Extracted operational axes", "## Extracted confounders",
    "## Extracted falsifiers", "## Forecast horizons / outcome candidates",
    "## Strategy-family hints", "## Links created or updated", "## Open questions",
    "## No-trade boundary",
]
_EVIDENCE_FM_KEYS = [
    "type:", "classification:", "workflow_status:", "access_class:", "evidence_id:",
    "source_slug:", "source_location:", "page_number:", "claim_type:", "claim_kind:",
    "temporal_status:", "temporal_role:", "outcome_check_required:", "entities:", "concepts:",
    "themes:", "market_variables:", "numbers:", "causal_edges:", "confidence:", "freshness:",
    "agent_use:", "source_date:", "created:", "updated:",
]
_EVIDENCE_SECTIONS = [
    "# Evidence:", "## Claim", "## Why it matters", "## Source provenance", "## Temporal status",
    "## Structured fields", "## No-trade boundary",
]
_THEME_FM_KEYS = [
    "type:", "classification:", "workflow_status:", "access_class:", "source_evidence:",
    "parent_developments:", "linked_events:", "linked_entities:", "linked_concepts:",
    "operational_axes:", "confounders:", "falsifiers:", "strategy_family_hints:",
    "theme_clusters:", "temporal_role:", "created:", "updated:",
]
_THEME_SECTIONS = [
    "# Theme Memory Card", "## Current belief", "## Temporal status",
    "## Why this theme was picked", "## Evidence", "## Main developments", "## Key events",
    "## Hot topics", "## Core causal hypothesis", "## Causal graph", "## Operational axes",
    "## Confounders", "## Falsifiers", "## Forecast horizons / outcome candidates",
    "## Scenario memory", "## Strategy-family priors", "## What changed after latest source",
    "## Open questions", "## No-trade boundary",
]
_CLUSTER_FM_KEYS = [
    "type:", "classification:", "workflow_status:", "access_class:", "cluster_id:",
    "canonical_theme_name:", "theme_status:", "source_slugs:", "independent_source_count:",
    "evidence_ids:", "temporal_roles:", "strategy_family_hints:", "promotion_score:",
    "corroboration_score:", "attention_score:", "evidence_attention_divergence:", "created:",
    "updated:",
]
_CLUSTER_SECTIONS = [
    "# Theme Cluster:", "## Cluster thesis", "## Source attributions", "## Evidence bullets",
    "## Why this cluster was promoted / not promoted", "## Corroboration vs attention",
    "## Temporal status", "## Operational axes", "## Causal claims", "## Confounders",
    "## Falsifiers", "## Strategy-family hints", "## Missing data", "## Rejected merges",
    "## No-trade boundary",
]


@pytest.mark.parametrize("rel,fm_keys,sections", [
    ("sources/acme-credit-report-2026-05-01.md", _SOURCE_FM_KEYS, _SOURCE_SECTIONS),
    ("evidence/ev-1.md", _EVIDENCE_FM_KEYS, _EVIDENCE_SECTIONS),
    ("themes/acme-credit-report-2026-05-01-primary-supply-pressure.md", _THEME_FM_KEYS,
     _THEME_SECTIONS),
    ("theme-clusters/cluster-primary-supply.md", _CLUSTER_FM_KEYS, _CLUSTER_SECTIONS),
])
def test_required_frontmatter_and_sections(tmp_path, rel, fm_keys, sections):
    inp = _input(tmp_path)
    integrate(inp)
    body = (Path(inp.wiki_root) / rel).read_text()
    for k in fm_keys:
        assert k in body, f"{rel} missing frontmatter key {k}"
    for s in sections:
        assert s in body, f"{rel} missing section {s}"


# ── theme card append-on-existing (versioned, not overwrite) ─────────────────────

def test_theme_card_appends_versioned_note_on_reingest(tmp_path):
    # first ingestion writes the card; a second ingestion of a NEW source touching the same theme
    # slug would append. Here we re-run with the SAME source — identical content => skip (idempotent).
    inp = _input(tmp_path)
    integrate(inp)
    theme_path = (Path(inp.wiki_root) / "themes"
                  / "acme-credit-report-2026-05-01-primary-supply-pressure.md")
    original = theme_path.read_text()
    # mutate the bundle so the theme card content differs -> append path triggers
    inp2 = _input(tmp_path, bundle=_bundle(
        atoms=[_atom(eid="ev-2", claim="Issuance accelerated further into June.")],
        themes=["primary supply pressure"]), theme_set=None)
    integrate(inp2)
    updated = theme_path.read_text()
    assert updated.startswith(original.split("\n## What changed")[0][:50])
    # prior rationale preserved; a new dated change note appended
    assert updated.count("## What changed after latest source") == 1
    assert updated.count("###") >= 2  # at least two versioned sub-notes now


# ── agent wiring ─────────────────────────────────────────────────────────────────

def test_run_agent_dispatches_to_integrator(tmp_path):
    inp = _input(tmp_path, dry_run=True)
    res = run_agent("WikiIntegratorAgent", inp)
    assert res.applied is False
    assert res.plan.writes


def test_registry_lists_integrator():
    assert "WikiIntegratorAgent" in REGISTRY.list_agents()
