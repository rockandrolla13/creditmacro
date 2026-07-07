"""Pass B — mapping claims to themes (ONTOLOGY §EvidenceLink, invariant I3).

Receives claims + ThemeDefinitionView(M, σ, X, H) ONLY — no ledger, no scores,
no status. Two-stage match: (1) structural pre-match on vocab node overlap,
(2) semantic match → match_confidence. `polarity` is COMPUTED here as
claim.direction × d(θ) — never emitted by the LLM, never present in prompts
(ingest/prompts/). Remap policy on AXIS_REVISED / MECHANISM_REVISED.

Phase-4 deliverable — gates: test_seam_extract_to_map, test_axis_flip_remap.
"""
from __future__ import annotations

from typing import Protocol, Sequence

from .. import vocab
from ..substrate.hypothesis import ThemeDefinitionView, derived_direction  # definitions only
from .claim import AtomicClaim
from .link import EvidenceLink


class ThemeMapper(Protocol):
    def map(
        self, claims: Sequence[AtomicClaim], definitions: Sequence[ThemeDefinitionView]
    ) -> Sequence[EvidenceLink]: ...


class StructuralSemanticMapper:
    """Structural pre-match (vocab overlap) then semantic match. Polarity computed."""

    def __init__(self, provider, embedder) -> None:
        self._provider = provider
        self._embedder = embedder

    def map(
        self, claims: Sequence[AtomicClaim], definitions: Sequence[ThemeDefinitionView]
    ) -> Sequence[EvidenceLink]:
        # polarity = claim.direction * derived_direction(theme)  — computed, not LLM.
        raise NotImplementedError("Phase 4 — structural+semantic match; τ_ORPHAN routing")
