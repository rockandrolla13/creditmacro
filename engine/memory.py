"""Memory access — the FIREWALL that keeps CASE memory out of FRESH reasoning."""
from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Literal, Optional, Union

import yaml
from pydantic import BaseModel, ConfigDict

VALID_ACCESS_CLASSES = ("method", "case")

# ── coverage: what phase A may know ABOUT case memory without reading it ──────
#
# The firewall exists because prior conclusions anchor fresh causal reasoning. But
# reasoning fresh is not the same as reasoning blind: not knowing that a question was
# already asked wastes work and re-derives settled ground. The rule that separates the
# two:
#
#     HISTORY MAY SET THE AGENDA. IT MAY NOT SUPPLY THE ANSWER.
#
# "A prior case exists on this topic, it is settled, and three sources fed it" is a fact
# about COVERAGE — it says where to look and cannot anchor a conclusion because it
# contains none. "It concluded spreads widen" is the ANSWER, and that is exactly what
# phase A must not see.
#
# This mirrors `substrate.hypothesis.ThemeDefinitionView`, which grants Pass B the
# theme's shape while withholding its ledger, scores and status. Same move, same reason.
#
# Case frontmatter mixes both freely, so the split is drawn explicitly:
#   COVERAGE  slug · type · status · source count · updated
#   ANSWER    causal_chain · operational_axes · falsifiers · strategy_families ·
#             main_developments · hot_topics · confounders · and the whole body


class CoverageStatus(str, Enum):
    """How far prior work got — never which way it came out."""
    OPEN = "open"              # prior work exists and is still live
    SETTLED = "settled"        # it reached a conclusion; the DIRECTION is withheld
    CONTESTED = "contested"    # prior work disagreed with itself
    BLOCKED = "blocked"        # it stopped for a stated non-epistemic reason


#: The ONLY fields a CoverageEntry may carry. Pinned by
#: `test_coverage_entry_exposes_no_conclusion_bearing_field`, so adding a field that
#: leaks a conclusion fails a test rather than quietly widening what phase A can see.
COVERAGE_FIELDS = frozenset({"slug", "page_type", "status", "evidence_breadth", "last_updated"})

#: Frontmatter keys that carry conclusions. Named here so the guard is auditable, and so
#: a new conclusion-bearing key added to the wiki has an obvious place to be declared.
CONCLUSION_KEYS = frozenset({
    "causal_chain", "operational_axes", "falsifiers", "strategy_families",
    "main_developments", "hot_topics", "confounders", "key_events", "numbers",
    "theme_status", "confidence", "outcome", "direction",
})


class CoverageEntry(BaseModel):
    """WHERE prior work exists. Never WHAT it concluded.

    Deliberately absent: body, causal chain, axes, falsifiers, routed families,
    developments — see CONCLUSION_KEYS. `evidence_breadth` is a COUNT, not the evidence:
    "three sources looked at this" is agenda, "here is what they said" is answer.
    """
    model_config = ConfigDict(frozen=True)

    slug: str
    page_type: Optional[str] = None
    status: CoverageStatus = CoverageStatus.OPEN
    evidence_breadth: int = 0          # number of contributing sources, not their content
    last_updated: Optional[str] = None


def _coverage_status(frontmatter: dict) -> CoverageStatus:
    """Derive how far prior work got, without reading which way it went.

    `status: falsified` is deliberately mapped to SETTLED rather than surfaced. That a
    question was answered is agenda; that the answer was "no" is the answer.
    """
    raw = str(frontmatter.get("status") or frontmatter.get("workflow_status") or "").lower()
    if raw in {"blocked", "needs_structuring"}:
        return CoverageStatus.BLOCKED
    if raw in {"contested", "disputed"}:
        return CoverageStatus.CONTESTED
    if raw in {"closed", "settled", "falsified", "played_out", "expired", "retired", "resolved"}:
        return CoverageStatus.SETTLED
    return CoverageStatus.OPEN

# type → default access_class for backfill/derivation. Concepts/entities and book/paper
# sources teach method; themes/scenarios and recorded analyses are case.
_METHOD_TYPES = {"concept", "entity", "model"}
_CASE_TYPES = {"theme", "scenario", "evidence", "outcome"}

class WikiPage(BaseModel):
    """One parsed wiki page. access_class may be None/invalid on a malformed page — the
    lint check (`check_access_class`) surfaces that; the retriever fails closed regardless."""
    model_config = ConfigDict(frozen=True)
    slug: str
    access_class: Optional[str] = None
    type: Optional[str] = None
    frontmatter: dict = {}
    body: str = ""

def derive_access_class(frontmatter: dict) -> Optional[str]:
    """Best-effort backfill default from a page's type/source_type. Returns None when it"""
    if frontmatter.get("access_class") in VALID_ACCESS_CLASSES:
        return frontmatter["access_class"]
    typ = frontmatter.get("type")
    if typ in _CASE_TYPES:
        return "case"
    if typ in _METHOD_TYPES:
        return "method"
    if typ == "source":
        # book/paper sources teach method; reports/memos/transcripts/market_data record
        # situational facts/conclusions → case.
        return "method" if frontmatter.get("source_type") in {"book", "paper"} else "case"
    if typ == "strategy_family":
        return "method"   # the family taxonomy is how-to-express knowledge
    return None

# ── parsing ───────────────────────────────────────────────────────────────────

def parse_wiki_page(path: Union[str, Path]) -> WikiPage:
    """Parse a markdown page with YAML frontmatter into a WikiPage."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    frontmatter: dict = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            raw = text[3:end].strip("\n")
            body = text[end + 4:].lstrip("\n")
            loaded = yaml.safe_load(raw)
            if isinstance(loaded, dict):
                frontmatter = loaded
    access_class = frontmatter.get("access_class")
    if access_class not in VALID_ACCESS_CLASSES:
        access_class = derive_access_class(frontmatter) or access_class
    return WikiPage(
        slug=str(frontmatter.get("slug") or path.stem),
        access_class=access_class,
        type=frontmatter.get("type"),
        frontmatter=frontmatter,
        body=body,
    )

def load_wiki_pages(wiki_dir: Union[str, Path]) -> dict[str, WikiPage]:
    """Load all content pages (sources/entities/concepts/themes/scenarios/strategy-families/"""
    wiki_dir = Path(wiki_dir)
    skip = {"index", "log", "lint-status", "lint-scratch", "CONVENTIONS", "README"}
    pages: dict[str, WikiPage] = {}
    for md in sorted(wiki_dir.rglob("*.md")):
        if md.stem in skip:
            continue
        page = parse_wiki_page(md)
        pages[page.slug] = page
    return pages

# ── lint check (rule 1) ───────────────────────────────────────────────────────

def check_access_class(pages: dict[str, WikiPage]) -> list[str]:
    """Lint: every page must carry a valid access_class (method | case). Returns one"""
    findings: list[str] = []
    for slug, page in pages.items():
        if page.access_class not in VALID_ACCESS_CLASSES:
            findings.append(
                f"{slug}: missing/invalid access_class={page.access_class!r} "
                f"(must be one of {VALID_ACCESS_CLASSES})"
            )
    return findings

# ── the retriever (the firewall) ──────────────────────────────────────────────

class MemoryRetriever:
    """Phase-gated, FAIL-CLOSED wiki retriever."""

    def __init__(self, pages: dict[str, WikiPage], phase: Literal["A", "B"] = "A") -> None:
        self._pages = pages
        self._phase = phase
        self.refusals: list[str] = []                    # slugs refused in phase A
        self.frozen_hash: Optional[str] = None           # set when the snapshot is frozen
        self.reads: list[dict] = []                      # audit log of every retrieve()

    @property
    def phase(self) -> str:
        return self._phase

    def mark_frozen(self, content_hash: str) -> None:
        """Record that the phase-A snapshot is frozen — must be called BEFORE phase B so
        every later case read is provably after the freeze."""
        self.frozen_hash = content_hash

    def advance_to_phase_b(self) -> None:
        if self._phase != "A":
            raise RuntimeError("MemoryRetriever already advanced past phase A")
        self._phase = "B"

    def retrieve(self, slug: str) -> Optional[WikiPage]:
        page = self._pages.get(slug)
        is_method = page is not None and page.access_class == "method"
        # Phase A is fail-closed: only method pages pass.
        allowed = page is not None and (self._phase == "B" or is_method)
        self.reads.append({
            "phase": self._phase,
            "slug": slug,
            "access_class": page.access_class if page is not None else None,
            "allowed": allowed,
            "frozen_before_read": self.frozen_hash is not None,
        })
        if page is None:
            return None
        if not allowed:
            self.refusals.append(slug)
            return None
        return page

    def retrieve_many(self, slugs: list[str]) -> list[WikiPage]:
        return [p for p in (self.retrieve(s) for s in slugs) if p is not None]

    def method_slugs(self) -> list[str]:
        return [s for s, p in self._pages.items() if p.access_class == "method"]

    def case_slugs(self) -> list[str]:
        return [s for s, p in self._pages.items() if p.access_class == "case"]

    def coverage(self) -> list[CoverageEntry]:
        """Which questions prior work already touched — readable in phase A.

        This is the ONE thing phase A may learn about case memory, and it is not an
        exception to the firewall: a CoverageEntry carries no conclusion, so there is
        nothing here to anchor on. `retrieve()` on the same slug still returns None in
        phase A, which `test_coverage_does_not_open_a_back_door_to_case_bodies` pins.

        Sorted by slug so two runs of identical reasoning see an identical agenda.
        """
        entries = [
            CoverageEntry(
                slug=slug,
                page_type=page.type,
                status=_coverage_status(page.frontmatter),
                # a COUNT of contributing sources; never the sources' content
                evidence_breadth=len(page.frontmatter.get("sources") or []),
                last_updated=(str(page.frontmatter["updated"])
                              if page.frontmatter.get("updated") is not None else None),
            )
            for slug, page in self._pages.items()
            if page.access_class == "case"
        ]
        entries.sort(key=lambda e: e.slug)
        self.reads.append({
            "phase": self._phase,
            "slug": "<coverage>",
            "access_class": "case",
            "allowed": True,              # coverage carries no conclusion; see the note above
            "frozen_before_read": self.frozen_hash is not None,
            "entries": len(entries),
        })
        return entries
