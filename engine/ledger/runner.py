"""Orchestration: doc → Pass A → Pass B → append → score/admit → render/project.

Reuses engine.workflow patterns. Catches per-document, logs, continues; emits a
session summary (docs, claims, links, orphans, admitted, NEEDS_STRUCTURING,
review items). Runtime settings live in a Pydantic LedgerRunConfig (D-06) —
distinct from the ONTOLOGY constants in constants.py.
"""
from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel


class LedgerRunConfig(BaseModel):
    corpus_dirs: tuple[Path, ...]                 # e.g. (markdowns/, wiki/sources/)
    events_store: Path = Path("data/ledger/events.jsonl")
    links_store: Path = Path("data/ledger/links.jsonl")
    provider: str = "scripted"                    # "scripted" (gates) | live provider id
    embedder: str = "hash_stub"                   # BLOCKED B-02


def run(config: LedgerRunConfig) -> dict:
    """Forward re-ingest over the corpus. Returns the session summary dict. Phase-6/7."""
    raise NotImplementedError("Phase 6/7 — wires the pipeline; emits session summary")
