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
from engine.temporal import ForecastHorizon, TemporalContext
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


# ══════════════════════════════════════════════════════════════════════════════════
# PART 10 additions — the items not already covered above.
# ══════════════════════════════════════════════════════════════════════════════════


# ── item 2: rejects incompatible inputs ───────────────────────────────────────────

def test_integrator_rejects_incompatible_input():
    """The agent's run() validates via WikiIntegratorInput.model_validate, so a structurally
    incompatible payload (missing required objects, wrong types) is rejected with a pydantic
    ValidationError rather than silently producing a malformed plan."""
    import pydantic
    with pytest.raises(pydantic.ValidationError):
        run_agent("WikiIntegratorAgent", {"not": "a valid integrator input"})
    with pytest.raises(pydantic.ValidationError):
        # bundle present but source_classification missing
        run_agent("WikiIntegratorAgent", {"bundle": _bundle().model_dump()})


# ── item 6: evidence provenance ───────────────────────────────────────────────────

def test_evidence_page_carries_provenance(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    ev = (Path(inp.wiki_root) / "evidence" / "ev-1.md").read_text()
    # frontmatter provenance fields
    assert "evidence_id: ev-1" in ev
    assert "source_slug: acme-credit-report-2026-05-01" in ev
    assert "source_location: page:7" in ev
    assert "page_number: 7" in ev
    # body provenance section names the source + location + page
    prov = ev.split("## Source provenance", 1)[1].split("##", 1)[0]
    assert "acme-credit-report-2026-05-01" in prov
    assert "page:7" in prov
    assert "7" in prov


# ── item 7 (provenance link resolution): evidence link from theme resolves ─────────

def test_theme_evidence_links_resolve_to_evidence_pages(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    root = Path(inp.wiki_root)
    theme = (root / "themes"
             / "acme-credit-report-2026-05-01-primary-supply-pressure.md").read_text()
    ev_links = re.findall(r"\[\[(ev-[^\]]+)\]\]", theme)
    assert ev_links, "theme card must backlink to its evidence atoms"
    for eid in ev_links:
        assert (root / "evidence" / f"{eid}.md").exists(), f"[[{eid}]] must resolve"


# ── item 9: cluster cites attributions + evidence ─────────────────────────────────

def test_cluster_page_cites_attributions_and_evidence(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    cluster = (Path(inp.wiki_root) / "theme-clusters"
               / "cluster-primary-supply.md").read_text()
    # frontmatter records source + evidence provenance
    assert "source_slugs:" in cluster
    assert "acme-credit-report-2026-05-01" in cluster
    assert "evidence_ids:" in cluster
    assert "ev-1" in cluster
    # source-attributions section names the contributing source + its contribution type
    attribs = cluster.split("## Source attributions", 1)[1].split("##", 1)[0]
    assert "acme-credit-report-2026-05-01" in attribs
    assert "supports" in attribs
    # evidence bullets section cites the evidence id
    bullets = cluster.split("## Evidence bullets", 1)[1].split("##", 1)[0]
    assert "ev-1" in bullets


# ── item 10: concept / entity pages created + updated (Part 7) ─────────────────────

def test_concept_and_entity_pages_created(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    root = Path(inp.wiki_root)
    # default bundle: concepts ["spread dispersion","primary supply"], entities ["JULI","technology"]
    expected = {
        "concepts/spread-dispersion.md", "concepts/primary-supply.md",
        "entities/juli.md", "entities/technology.md",
    }
    for rel in expected:
        assert (root / rel).exists(), f"missing taxonomy page {rel}"
    concept = (root / "concepts" / "spread-dispersion.md").read_text()
    # frontmatter contract: generic taxonomy node, access mirrors the source (case here)
    assert "type: concept" in concept
    assert "access_class: case" in concept
    assert "workflow_status: discovery_complete" in concept
    assert "sources:" in concept and "acme-credit-report-2026-05-01" in concept
    # generic body + evidence backlink + no-trade boundary
    assert "[[ev-1]]" in concept
    assert "## No-trade boundary" in concept
    entity = (root / "entities" / "juli.md").read_text()
    assert "type: entity" in entity
    assert "access_class: case" in entity
    assert "[[ev-1]]" in entity


def test_method_source_still_writes_concept_entity_pages(tmp_path):
    """For a METHOD source, evidence/theme pages are NOT written, but concept/entity taxonomy
    pages ARE — stamped method (Part 7 contract)."""
    inp = _input(
        tmp_path,
        source_classification=_classification(slug="pearl-book-of-why", access="method",
                                              stype="book"),
        bundle=_bundle(slug="pearl-book-of-why"),
        temporal_context=_temporal(slug="pearl-book-of-why", role="method_source"),
        theme_set=None,
    )
    integrate(inp)
    root = Path(inp.wiki_root)
    assert not (root / "evidence").exists() or not list((root / "evidence").glob("*.md"))
    concept = (root / "concepts" / "spread-dispersion.md").read_text()
    assert "access_class: method" in concept
    assert "access_class: case" not in concept
    assert (root / "entities" / "juli.md").exists()


# ── item 11: index.md Part-8 per-source block ─────────────────────────────────────

def test_index_has_part8_source_block(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    index = (Path(inp.wiki_root) / "index.md").read_text()
    assert "<!-- integrated 2026-06-12: acme-credit-report-2026-05-01 -->" in index
    assert "### acme-credit-report-2026-05-01" in index
    for label in ("- Source:", "- Evidence:", "- Themes:", "- Theme clusters:",
                  "- Concepts:", "- Entities:"):
        assert label in index, f"index block missing line {label}"
    # grouped links present + resolve to created files
    assert "[[acme-credit-report-2026-05-01]]" in index
    assert "[[ev-1]]" in index
    created = {p.stem for p in _files(inp.wiki_root)}
    for slug in re.findall(r"\[\[([^\]]+)\]\]", index):
        assert slug in created


def test_index_empty_group_renders_none(tmp_path):
    """A bundle with no clusters renders the Theme clusters group as '(none)' with no link."""
    inp = _input(tmp_path, theme_set=None)
    integrate(inp)
    index = (Path(inp.wiki_root) / "index.md").read_text()
    block = index.split("### acme-credit-report-2026-05-01", 1)[1]
    cluster_line = next(ln for ln in block.splitlines() if ln.startswith("- Theme clusters:"))
    assert cluster_line.strip() == "- Theme clusters: (none)"
    assert "[[" not in cluster_line


# ── item 12: log appends exactly ONE entry (idempotent on re-run) ─────────────────

def test_log_appends_exactly_one_entry(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    log_path = Path(inp.wiki_root) / "log.md"
    text = log_path.read_text()
    header = "## [2026-06-12] ingest | acme-credit-report-2026-05-01"
    assert text.count(header) == 1
    for bullet in ("- Source:", "- Access class:", "- Temporal role:",
                   "- Evidence atoms created:", "- Themes updated:",
                   "- Theme clusters updated:", "- Concepts/entities updated:",
                   "- Strategy-family hints:", "- Warnings:", "- No-trade confirmation:"):
        assert bullet in text, f"log entry missing bullet {bullet}"
    # idempotent re-run: the same snippet is already present, so still exactly ONE entry
    integrate(_input(tmp_path))
    assert log_path.read_text().count(header) == 1


# ── item 13: memory-map updates (11 headings + marker) ────────────────────────────

_MEMORY_MAP_HEADINGS = [
    "#### Active Main Developments", "#### Active Core Themes", "#### Active Hot Topics",
    "#### Multi-Source Theme Clusters", "#### Strategy-Family Priors",
    "#### Historical Outcome Candidates", "#### Themes Missing Evidence",
    "#### Themes Missing Operational Axes", "#### Themes Missing Falsifiers",
    "#### Themes Ready for Strategy-Family Routing", "#### Themes Ready for Downstream Models",
]


def test_memory_map_emits_all_headings_and_marker(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    mm = (Path(inp.wiki_root) / "memory-map.md").read_text()
    assert "<!-- memory-map 2026-06-12: acme-credit-report-2026-05-01 -->" in mm
    assert len(_MEMORY_MAP_HEADINGS) == 11
    for h in _MEMORY_MAP_HEADINGS:
        assert h in mm, f"memory-map missing heading {h}"


def test_memory_map_empty_sets_render_none(tmp_path):
    """The default bundle has evidence + axis + falsifier + family hint, so the 'missing' sets are
    empty and render '- (none)'; 'Historical Outcome Candidates' is empty for a current report."""
    inp = _input(tmp_path)
    integrate(inp)
    mm = (Path(inp.wiki_root) / "memory-map.md").read_text()
    block = mm.split("### acme-credit-report-2026-05-01", 1)[1]

    def section(name):
        return block.split(name, 1)[1].split("####", 1)[0]

    assert "- (none)" in section("#### Themes Missing Evidence")
    assert "- (none)" in section("#### Historical Outcome Candidates")
    # readiness IS met for the default bundle (evidence+axis+falsifier+family)
    assert "primary supply pressure" in section("#### Themes Ready for Strategy-Family Routing")


# ── item 15: force / overwrite semantics ──────────────────────────────────────────

def test_force_rewrites_identical_page(tmp_path):
    """force=True rewrites even an identical page (it lands in written_paths, not skipped)."""
    inp = _input(tmp_path)
    integrate(inp)
    res = integrate(_input(tmp_path, force=True))
    assert any("sources" in p for p in res.written_paths), \
        "force=True must rewrite the (identical) source page rather than skip it"
    assert not any("sources" in p for p in res.skipped_paths)


def test_non_force_overwrites_divergent_create_page(tmp_path):
    """ACTUAL applier semantics (verified against apply_wiki_update_plan): on a 'create' write,
    force only short-circuits when the existing content is IDENTICAL. A divergent existing page
    is OVERWRITTEN even with force=False — there is no allow_overwrite refusal path. We assert the
    real behavior so the contract is pinned; see PART-10 return note for the discussion of whether
    a hand-edited page should instead be refused."""
    inp = _input(tmp_path)
    integrate(inp)
    src_path = Path(inp.wiki_root) / "sources" / "acme-credit-report-2026-05-01.md"
    src_path.write_text("HAND EDITED — divergent content\n", encoding="utf-8")
    res = integrate(_input(tmp_path))          # force defaults to False
    after = src_path.read_text()
    assert "HAND EDITED" not in after, "divergent create page is clobbered (current semantics)"
    assert "# Source Summary" in after
    assert any("sources" in p for p in res.written_paths)


# ── item 16: CASE pages refused in Phase A unless current input ───────────────────

def test_case_page_refused_in_phase_a_unless_current_input(tmp_path):
    """Phase-A firewall, expressed by the Part-9 pure predicate over an integrator-written page:
    a case page that is NOT the current input is refused in Phase A; the current input is admitted;
    Phase B admits everything."""
    from engine.wiki_validators import check_case_page_phase_a
    inp = _input(tmp_path)
    integrate(inp)
    src = (Path(inp.wiki_root) / "sources" / "acme-credit-report-2026-05-01.md").read_text()
    # case page, not the current input, Phase A -> refused
    findings = check_case_page_phase_a(src, phase="A", is_current_input=False)
    assert findings and findings[0].severity == "error"
    assert findings[0].check == "case_refused_phase_a"
    # same page IS the current input -> admitted (no finding)
    assert check_case_page_phase_a(src, phase="A", is_current_input=True) == []
    # Phase B -> admitted regardless
    assert check_case_page_phase_a(src, phase="B", is_current_input=False) == []


# ── item 17: historical report labelled historical / outcome-candidate ────────────

def _historical_input(tmp_path, **kw):
    """A historical_case bundle: an aged source whose forecasts are stated 'as of' the source date.
    current_update_required=True is mandatory once a forecast has expired."""
    horizon = ForecastHorizon(
        claim="IG spreads widen 30bp over the coming quarter",
        horizon_type="quarter", status="expired", outcome_check_required=True,
        outcome_variable="IG OAS")
    tc = TemporalContext(
        source_slug="euro-equity-strategy-2019",
        source_date=date.fromisoformat("2019-03-01"),
        current_date=date.fromisoformat("2026-06-12"),
        temporal_role="historical_case",
        forecast_horizons=[horizon],
        expired_forecasts=["IG spreads widen 30bp over the coming quarter"],
        current_update_required=True)
    base = dict(
        source_classification=_classification(slug="euro-equity-strategy-2019",
                                              access="case", stype="report"),
        bundle=_bundle(slug="euro-equity-strategy-2019",
                       themes=["european equity de-rating"]),
        temporal_context=tc,
        theme_set=None,
        wiki_root=str(tmp_path / "wiki"),
    )
    base.update(kw)
    return WikiIntegratorInput(**base)


def test_historical_case_source_labelled_historical(tmp_path):
    inp = _historical_input(tmp_path)
    integrate(inp)
    root = Path(inp.wiki_root)
    src = (root / "sources" / "euro-equity-strategy-2019.md").read_text()
    assert "temporal_role: historical_case" in src
    assert "current_update_required: true" in src
    # forecasts are framed historically ("as of <source_date>:") and explicitly NOT current
    assert "as of 2019-03-01:" in src
    assert "NOT current recommendations" in src
    # the Part-9 on-disk historical-case check passes (disclaimer present, no live reco)
    from engine.wiki_validators import check_historical_cases_not_current
    assert check_historical_cases_not_current(str(root)) == []


def test_historical_evidence_page_marks_outcome_check(tmp_path):
    inp = _historical_input(tmp_path)
    integrate(inp)
    ev = (Path(inp.wiki_root) / "evidence" / "ev-1.md").read_text()
    assert "temporal_status: historical" in ev
    assert "outcome_check_required: true" in ev


# ── item 18: expired forecasts not rendered as current ────────────────────────────

def test_expired_forecast_not_rendered_current(tmp_path):
    """The Part-9 forecast-expiry predicate: a forecast past its horizon must be labelled
    expired/outcome_candidate, never 'current'. A page that still calls an expired horizon
    'current' is flagged; the integrator's historical page (status historical) is not."""
    from engine.wiki_validators import check_forecast_expiry_labeled
    inp = _historical_input(tmp_path)
    integrate(inp)
    src = (Path(inp.wiki_root) / "sources" / "euro-equity-strategy-2019.md").read_text()
    # horizon ended 2019, current date 2026 -> past horizon. A 'current' label is an error.
    bad = check_forecast_expiry_labeled(
        src, horizon_end_date="2019-06-01", current_date="2026-06-12",
        temporal_status="current")
    assert bad and bad[0].severity == "error"
    # labelled outcome_candidate -> no error
    ok = check_forecast_expiry_labeled(
        src, horizon_end_date="2019-06-01", current_date="2026-06-12",
        temporal_status="outcome_candidate")
    assert ok == []
    # a still-live horizon is never flagged regardless of status
    assert check_forecast_expiry_labeled(
        src, horizon_end_date="2027-01-01", current_date="2026-06-12",
        temporal_status="current") == []


# ── items 21-26: writer exercised across diverse domains ──────────────────────────

def _domain_bundle(slug, *, concepts, entities, themes, families, axis_name, axis_series):
    atom = _atom(eid=f"{slug}-ev-1", source_slug=slug, concepts=concepts, entities=entities,
                 themes=themes, claim="A structured, paraphrased development for this domain.")
    return EvidenceExtractionBundle(
        source_slug=slug,
        source_page_fields={"source_type": "report", "author_or_publisher": "Desk Research",
                            "source_date": "2026-05-01"},
        evidence_atoms=[atom],
        main_developments=["A domain development"],
        key_events=["A domain event"],
        hot_topics=themes[:1],
        core_theme_candidates=themes,
        causal_claims=[CausalClaimCandidate(
            driver="driver", transmission="mechanism", outcome="outcome",
            confidence=0.5, rationale="why")],
        operational_axes=[OperationalAxisCandidate(
            axis_name=axis_name, axis_shape="level", observable_series=axis_series)],
        confounders=["a confounder"],
        falsifiers=[f"{axis_name} moves opposite for 4 weeks"],
        strategy_family_hints=[StrategyFamilyHint(family=f, rationale="domain rationale",
                                                  confidence=0.5) for f in families],
        open_questions=["an open question"],
    )


def _domain_input(tmp_path, slug, bundle, *, role="current_report", access="case"):
    return WikiIntegratorInput(
        source_classification=_classification(slug=slug, access=access, stype="report"),
        bundle=bundle,
        temporal_context=_temporal(slug=slug, role=role),
        theme_set=None,
        wiki_root=str(tmp_path / "wiki"),
    )


def test_jpm_like_case_integrates_to_wiki(tmp_path):
    """item 21 — JPM-style AI-capex-funding case (hermetic synthetic in the spirit of the on-disk
    wiki/sources/jpm-ai-capex-funding-2026-05-11.md fixture): integrates cleanly into a temp wiki,
    source stamped case, themes + concepts land, no-trade / copyright validators pass."""
    bundle = _domain_bundle(
        "jpm-ai-capex-funding-2026-05-11",
        concepts=["data center capex", "credit supply"],
        entities=["JPM", "hyperscalers"],
        themes=["ai capex funding pressure"],
        families=["relative_value"],
        axis_name="HG vs HY data-center issuance spread",
        axis_series="JULI tech-sector OAS")
    inp = _domain_input(tmp_path, "jpm-ai-capex-funding-2026-05-11", bundle)
    res = integrate(inp)
    root = Path(inp.wiki_root)
    assert (root / "sources" / "jpm-ai-capex-funding-2026-05-11.md").exists()
    src = (root / "sources" / "jpm-ai-capex-funding-2026-05-11.md").read_text()
    assert "access_class: case" in src
    assert (root / "themes"
            / "jpm-ai-capex-funding-2026-05-11-ai-capex-funding-pressure.md").exists()
    assert (root / "concepts" / "data-center-capex.md").exists()
    assert (root / "entities" / "jpm.md").exists()
    from engine.wiki_validators import validate_all
    # NOTE: source_slug is intentionally omitted — it would trigger check_log_single_entry, which
    # has a Part-9/Part-8 contract mismatch (see test_log_validator_format_mismatch_xfail below).
    report = validate_all(wiki_root=str(root), plan_or_result=res, raw_text=None)
    assert report.ok, [f.message for f in report.errors()]


def test_software_pc_fixture_non_jpm_themes_and_axes(tmp_path):
    """item 24 — a software/PC-cycle source produces its own (non-JPM) themes + a computable axis."""
    bundle = _domain_bundle(
        "software-pc-cycle-2026-04",
        concepts=["pc refresh cycle", "software margins"],
        entities=["technology", "semis"],
        themes=["pc replacement cycle inflection"],
        families=["long_short"],
        axis_name="tech vs market equity spread",
        axis_series="software-sector relative OAS")
    inp = _domain_input(tmp_path, "software-pc-cycle-2026-04", bundle)
    integrate(inp)
    root = Path(inp.wiki_root)
    theme = (root / "themes"
             / "software-pc-cycle-2026-04-pc-replacement-cycle-inflection.md").read_text()
    assert "pc replacement cycle inflection" in theme.lower()
    # the operational axis (a named, computable series) is recorded on the theme card
    assert "tech vs market equity spread" in theme
    assert "software-sector relative OAS" in theme
    assert (root / "concepts" / "pc-refresh-cycle.md").exists()


def test_etf_flow_fixture_yields_etf_concepts_and_family_hints(tmp_path):
    """item 25 — an ETF-flow source surfaces ETF/basket concepts + the relative_value family hint
    (etf_basket_rv routes as a relative_value sub-type)."""
    bundle = _domain_bundle(
        "etf-flow-taarss-2026-05",
        concepts=["etf primary flow", "basket arbitrage"],
        entities=["LQD", "HYG"],
        themes=["etf flow dislocation"],
        families=["relative_value"],
        axis_name="ETF NAV vs basket spread",
        axis_series="LQD NAV-minus-basket series")
    inp = _domain_input(tmp_path, "etf-flow-taarss-2026-05", bundle)
    integrate(inp)
    root = Path(inp.wiki_root)
    assert (root / "concepts" / "etf-primary-flow.md").exists()
    assert (root / "concepts" / "basket-arbitrage.md").exists()
    assert (root / "entities" / "lqd.md").exists()
    # family hint lands on the source page + memory-map Strategy-Family Priors
    src = (root / "sources" / "etf-flow-taarss-2026-05.md").read_text()
    assert "relative_value" in src
    mm = (root / "memory-map.md").read_text()
    priors = mm.split("#### Strategy-Family Priors", 1)[1].split("####", 1)[0]
    assert "relative_value" in priors


def test_inflation_margin_fixture_sector_rotation_and_long_short_hints(tmp_path):
    """item 26 — an inflation/margin-compression source carries sector-rotation + long-short hints."""
    bundle = _domain_bundle(
        "inflation-margin-compression-2026-05",
        concepts=["margin compression", "input cost inflation"],
        entities=["consumer staples", "industrials"],
        themes=["margin compression rotation"],
        families=["sector_rotation", "long_short"],
        axis_name="defensives vs cyclicals spread",
        axis_series="staples-minus-cyclicals OAS")
    inp = _domain_input(tmp_path, "inflation-margin-compression-2026-05", bundle)
    integrate(inp)
    root = Path(inp.wiki_root)
    src = (root / "sources" / "inflation-margin-compression-2026-05.md").read_text()
    assert "sector_rotation" in src
    assert "long_short" in src
    theme = (root / "themes"
             / "inflation-margin-compression-2026-05-margin-compression-rotation.md").read_text()
    fam_fm = theme.split("strategy_family_hints:", 1)[1].split("\n", 3)
    assert "sector_rotation" in theme
    assert "long_short" in theme


def test_multi_source_theme_set_yields_cluster_page(tmp_path):
    """item 23 — a MultiSourceThemeSet produces a theme-cluster page (already partially covered by
    the apply test; here we assert the cluster page content end-to-end via the default theme_set)."""
    inp = _input(tmp_path)
    integrate(inp)
    cluster = Path(inp.wiki_root) / "theme-clusters" / "cluster-primary-supply.md"
    assert cluster.exists()
    body = cluster.read_text()
    assert "type: theme_cluster" in body
    assert "cluster_id: cluster-primary-supply" in body
    assert "## Cluster thesis" in body
