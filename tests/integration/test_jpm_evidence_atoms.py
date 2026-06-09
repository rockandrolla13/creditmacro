"""Q4 PART 2a — materialized JPM evidence atoms + firewall coverage on real on-disk pages.

These tests read the real wiki/ tree (and the gitignored JPM raw markdown for the leak check).
They pin: link resolution, provenance, claim_kind, paraphrase-only, and the Phase-A memory
firewall refusing archived evidence — closing the audit gaps 'evidence atoms dangling' and
'firewall realism untested on disk'.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from engine.memory import (
    MemoryRetriever,
    derive_access_class,
    load_wiki_pages,
    parse_wiki_page,
)
from tools.leak_check import longest_verbatim_run

_ROOT = Path(__file__).resolve().parents[2]
WIKI = _ROOT / "wiki"
EVID = WIKI / "evidence"
RAW_JPM = _ROOT / "markdowns" / "JPM_AI_Capex_Funding_Dat_2026-05-11_5290840.md"
SOURCE_SLUG = "jpm-ai-capex-funding-2026-05-11"
ALLOWED_KINDS = {
    "source_fact", "source_forecast", "source_opinion",
    "agent_synthesis", "PM_assumption", "model_output",
}


def _evidence_refs() -> set[str]:
    refs: set[str] = set()
    for md in WIKI.rglob("*.md"):
        # real atom-id links only (slug ending in a 3-digit index); ignores doc placeholders
        # like [[evidence:slug]] / [[evidence:…]] that appear in comments and examples.
        refs.update(re.findall(r"\[\[evidence:([a-z0-9-]+-\d{3})\]\]", md.read_text(encoding="utf-8")))
    return refs


def _evidence_pages() -> list[Path]:
    return sorted(EVID.glob("jpm-2026-05-11-*.md"))


def test_every_evidence_link_resolves():
    refs = _evidence_refs()
    assert refs, "expected [[evidence:...]] references somewhere in the wiki"
    slugs = {parse_wiki_page(p).slug for p in _evidence_pages()}
    missing = sorted(refs - slugs)
    assert not missing, f"unresolved evidence links: {missing}"


def test_every_atom_has_source_and_page_provenance_and_claim_kind():
    pages = _evidence_pages()
    assert pages, "expected materialized JPM evidence pages"
    for p in pages:
        fm = parse_wiki_page(p).frontmatter
        assert fm.get("source_slug") == SOURCE_SLUG, f"{p.stem}: source_slug"
        loc = str(fm.get("source_location") or "")
        assert re.fullmatch(r"page:\d+", loc), f"{p.stem}: bad source_location {loc!r}"
        assert fm.get("claim_kind") in ALLOWED_KINDS, f"{p.stem}: claim_kind {fm.get('claim_kind')!r}"
        assert fm.get("source_date") == "2026-05-11", f"{p.stem}: source_date"
        assert fm.get("access_class") == "case", f"{p.stem}: access_class"


def test_facts_and_synthesis_are_separated():
    # every JPM atom is a labelled source fact; no atom silently blends agent synthesis into a
    # source_fact (the kinds set is a subset of the allowed enum and contains source_fact).
    kinds = {parse_wiki_page(p).frontmatter.get("claim_kind") for p in _evidence_pages()}
    assert "source_fact" in kinds
    assert kinds <= ALLOWED_KINDS


def test_no_long_copyright_leak():
    if not RAW_JPM.exists():
        pytest.skip("JPM raw markdown absent (gitignored) — leak check needs the raw source")
    raw = RAW_JPM.read_text(encoding="utf-8", errors="ignore")
    for p in _evidence_pages():
        run = longest_verbatim_run(p.read_text(encoding="utf-8"), raw)
        assert run < 25, f"{p.stem}: {run}-word verbatim run from JPM raw — paraphrase instead"


def test_required_headline_atoms_present():
    # the audit-named headline facts must each appear as an atom (by number in the claim)
    claims = " ".join(parse_wiki_page(p).frontmatter.get("claim", "") for p in _evidence_pages())
    for token in ("27", "450", "105", "183", "49", "181", "101", "26.6", "43",
                  "2.68", "9.99", "1.61", "295"):
        assert token in claims, f"missing headline figure {token} across evidence atoms"


def test_evidence_type_derives_case():
    # firewall hardening: an evidence page missing an explicit access_class still defaults to case
    assert derive_access_class({"type": "evidence"}) == "case"


def test_phase_a_firewall_refuses_archived_evidence():
    pages = load_wiki_pages(WIKI)
    ev_slugs = [s for s, pg in pages.items() if pg.type == "evidence"]
    assert ev_slugs, "evidence pages should load from disk"
    ra = MemoryRetriever(pages, phase="A")
    for s in ev_slugs:
        assert ra.retrieve(s) is None, f"phase A must refuse archived evidence {s}"
        assert s in ra.refusals
    # phase B (post-freeze) may read case evidence as analogue/calibration
    rb = MemoryRetriever(pages, phase="B")
    assert rb.retrieve(ev_slugs[0]) is not None
