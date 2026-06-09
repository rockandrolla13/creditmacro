"""Current-input evidence loader.

Loads the materialized evidence atoms for the ONE source currently under analysis
(the "current input") and hands them to the deterministic evidence→scenario mapper.

Memory-firewall note: materialized evidence pages carry ``access_class: case``. That
classification is about ARCHIVED prior cases. The atoms loaded here are CASE material
*only because* they describe the current input document; they are legitimately loaded
because they ARE the fresh input, not because we are mining history. To keep that
guarantee, this loader is deliberately narrow: it loads atoms for exactly ONE
``source_slug`` and never sweeps the whole ``wiki/evidence/`` directory for other
sources' atoms.

Data source: the committed JSONL ``wiki/evidence/evidence_atoms.jsonl`` is the source of
truth (one record per atom). If it is absent we fall back to the per-atom evidence pages
(frontmatter), filtered to the same ``source_slug``. Either way we adapt records via
``EvidenceAtom.from_record`` and follow the lenient "warn, skip; don't crash" style of
``engine/memory.py``.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional, Union

from .memory import parse_wiki_page
from .probability_evidence import map_evidence_to_scenarios
from .schema import EvidenceAtom, Scenario, ScenarioEvidenceMap

logger = logging.getLogger(__name__)

_EVIDENCE_SUBDIR = "evidence"
_ATOMS_JSONL = "evidence_atoms.jsonl"

# Fields that live on the per-atom evidence PAGE frontmatter but not necessarily on the
# JSONL record. We backfill them onto JSONL records (keyed by evidence_id) so that
# claim_kind / page provenance / agent_use are preserved regardless of which source we read.
_PAGE_ENRICH_FIELDS = ("claim_kind", "agent_use", "page_number")


def _wiki_evidence_dir(wiki_root: Union[str, Path]) -> Path:
    return Path(wiki_root) / _EVIDENCE_SUBDIR


def _page_frontmatter_by_evidence_id(evidence_dir: Path, source_slug: str) -> dict[str, dict]:
    """Index evidence-page frontmatter by evidence_id for the given source (lenient)."""
    index: dict[str, dict] = {}
    if not evidence_dir.is_dir():
        return index
    for path in sorted(evidence_dir.glob("*.md")):
        try:
            page = parse_wiki_page(path)
        except Exception as exc:  # noqa: BLE001 — lenient, never crash on one bad page
            logger.warning("evidence_loader: skipping unreadable evidence page %s: %s", path, exc)
            continue
        fm = page.frontmatter or {}
        if fm.get("type") != "evidence" or fm.get("source_slug") != source_slug:
            continue
        eid = fm.get("evidence_id")
        if eid:
            index[str(eid)] = fm
    return index


def _atoms_from_jsonl(jsonl_path: Path, source_slug: str) -> Optional[list[EvidenceAtom]]:
    """Load atoms for ``source_slug`` from the JSONL source of truth.

    Returns None if the JSONL file does not exist (so the caller can fall back to pages).
    Malformed lines / records are warned about and skipped (lenient).
    """
    if not jsonl_path.is_file():
        return None
    # Backfill page-only fields (claim_kind, provenance) onto JSONL records when absent.
    page_index = _page_frontmatter_by_evidence_id(jsonl_path.parent, source_slug)
    atoms: list[EvidenceAtom] = []
    for lineno, line in enumerate(jsonl_path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as exc:
            logger.warning("evidence_loader: skipping malformed JSONL line %d in %s: %s",
                           lineno, jsonl_path, exc)
            continue
        if not isinstance(rec, dict):
            logger.warning("evidence_loader: skipping non-object JSONL record on line %d in %s",
                           lineno, jsonl_path)
            continue
        if rec.get("source_slug") != source_slug:
            continue
        page_fm = page_index.get(str(rec.get("evidence_id"))) if rec.get("evidence_id") else None
        if page_fm:
            for field in _PAGE_ENRICH_FIELDS:
                if not rec.get(field) and page_fm.get(field) is not None:
                    rec[field] = page_fm[field]
        atom = _adapt_record(rec, f"{jsonl_path}:{lineno}")
        if atom is not None:
            atoms.append(atom)
    return atoms


def _atoms_from_pages(evidence_dir: Path, source_slug: str) -> list[EvidenceAtom]:
    """Fallback: load atoms for ``source_slug`` from per-atom evidence page frontmatter.

    Only ``type: evidence`` pages are considered; malformed/dangling pages are warned and
    skipped (lenient, mirroring engine/memory.py).
    """
    atoms: list[EvidenceAtom] = []
    if not evidence_dir.is_dir():
        logger.warning("evidence_loader: evidence directory not found: %s", evidence_dir)
        return atoms
    for path in sorted(evidence_dir.glob("*.md")):
        try:
            page = parse_wiki_page(path)
        except Exception as exc:  # noqa: BLE001 — lenient, never crash on one bad page
            logger.warning("evidence_loader: skipping unreadable evidence page %s: %s", path, exc)
            continue
        fm = page.frontmatter or {}
        if fm.get("type") != "evidence":
            continue
        if fm.get("source_slug") != source_slug:
            continue
        atom = _adapt_record(fm, str(path))
        if atom is not None:
            atoms.append(atom)
    return atoms


def _adapt_record(rec: dict, provenance: str) -> Optional[EvidenceAtom]:
    """Adapt one materialized record into an EvidenceAtom; warn+skip if malformed."""
    try:
        return EvidenceAtom.from_record(rec)
    except Exception as exc:  # noqa: BLE001 — lenient, skip the bad atom
        logger.warning("evidence_loader: skipping malformed evidence record (%s): %s",
                       provenance, exc)
        return None


def load_evidence_atoms_for_current_source(
    source_slug: Optional[str],
    wiki_root: Union[str, Path],
) -> list[EvidenceAtom]:
    """Load the materialized evidence atoms for the CURRENT input ``source_slug``.

    Loads ONLY atoms whose ``source_slug`` matches the request — unrelated archived CASE
    evidence (other sources) is never loaded. Prefers the committed JSONL source of truth
    (``wiki/evidence/evidence_atoms.jsonl``) and falls back to per-atom evidence pages.

    Returns ``[]`` (and logs a warning) when ``source_slug`` is missing/empty or no atom
    matches; never raises for the missing-source case.
    """
    if not source_slug or not source_slug.strip():
        logger.warning("evidence_loader: no source_slug supplied — returning no evidence atoms")
        return []
    source_slug = source_slug.strip()

    evidence_dir = _wiki_evidence_dir(wiki_root)
    atoms = _atoms_from_jsonl(evidence_dir / _ATOMS_JSONL, source_slug)
    if atoms is None:  # JSONL absent → fall back to pages
        atoms = _atoms_from_pages(evidence_dir, source_slug)

    if not atoms:
        logger.warning("evidence_loader: no evidence atoms found for source_slug=%r under %s",
                       source_slug, evidence_dir)
    return atoms


def load_evidence_maps_for_current_source(
    source_slug: Optional[str],
    scenarios: list[Scenario],
    wiki_root: Union[str, Path],
    causal_object=None,
) -> list[ScenarioEvidenceMap]:
    """Load the current-input atoms and map them onto the SUPPLIED scenarios.

    Thin composition: ``load_evidence_atoms_for_current_source`` then the read-only
    deterministic mapper ``map_evidence_to_scenarios``. Never generates scenarios, never
    invents probabilities. With no matching atoms the mapper still returns one (empty) map
    per scenario.
    """
    atoms = load_evidence_atoms_for_current_source(source_slug, wiki_root)
    return map_evidence_to_scenarios(scenarios, atoms, causal_object=causal_object)
