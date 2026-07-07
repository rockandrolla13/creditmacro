"""Provenance breadcrumbs for the 82 non-WF-surviving theme cards (D-03).

These cards are NOT theme inputs. They are kept only as a card→source map so an
admitted theme can be traced back to which cards' sources fed it. The forward
re-ingest path reads the cards' `sources:` frontmatter to know which source docs
to run Pass A over. Phase-3 companion to admission.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Breadcrumb:
    card_slug: str
    source_ids: tuple[str, ...]      # the card's `sources:` frontmatter
    wf_fail_clause: str = "a"        # why it did not survive (mostly k ≤ 1)


def build_card_source_map(themes_dir: str) -> list[Breadcrumb]:
    """Scan wiki/themes/*.md → breadcrumbs. Read-only; never mutates the cards."""
    raise NotImplementedError("Phase 3 — parse sources: frontmatter into breadcrumbs")
