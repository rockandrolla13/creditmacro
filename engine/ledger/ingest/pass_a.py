"""Pass A — BLIND claim extraction (ONTOLOGY §AtomicClaim, invariant I2).

The extractor sees ONLY the document. The theme registry is unreachable BY
CONSTRUCTION: this module MUST NOT import `engine.ledger.substrate` (enforced by
tools/ledger_invariants.py). It may import vocab (METHOD memory) + claim only.

Phase-3 deliverable — gate: test_golden_claims_exact (+ I2 import check green).
"""
from __future__ import annotations

from datetime import datetime
from typing import Protocol, Sequence

from .. import vocab  # METHOD memory — allowed
from .claim import AtomicClaim


class ClaimExtractor(Protocol):
    """Anything that turns a document into atomic, vocabulary-tagged claims."""
    def extract(
        self, doc_id: str, text: str, *, source_institution: str, doc_date: datetime
    ) -> Sequence[AtomicClaim]: ...


class LLMClaimExtractor:
    """Provider-backed blind extractor. Gates use scripted_provider (deterministic)."""

    def __init__(self, provider) -> None:      # engine.llm_provider seam
        self._provider = provider

    def extract(
        self, doc_id: str, text: str, *, source_institution: str, doc_date: datetime
    ) -> Sequence[AtomicClaim]:
        # tags MUST be drawn from vocab.NODES; out-of-vocab tags route to review.
        raise NotImplementedError("Phase 3 — blind extraction; tag against vocab.NODES")
