"""Orphan clustering + admission (ONTOLOGY §Admission). Phase-6 deliverable.

Cluster orphan claims by mechanism_tags overlap + embedding proximity; promote
iff |claims| ≥ N_MIN ∧ |institutions| ≥ I_MIN ∧ span ≤ W_ADMIT. Synthesize a
CandidateTheme over the vocab from modal tags; it must pass WF or route to
NEEDS_STRUCTURING. Out-of-vocab modal tag → review queue (never auto-added).

This is the load-bearing population path (D-03 forward re-ingest): the registry
is rebuilt here from claims, not imported from theme pages.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .claim import AtomicClaim


@dataclass(frozen=True)
class OrphanCluster:
    claim_ids: tuple[str, ...]
    modal_tags: tuple[str, ...]
    institutions: tuple[str, ...]


def cluster_orphans(orphans: Sequence[AtomicClaim], embedder) -> list[OrphanCluster]:
    raise NotImplementedError("Phase 6 — mechanism-tag + embedding clustering")


def admit(cluster: OrphanCluster) -> None:
    """Promote a cluster to a CandidateTheme (CREATED via fold) or NEEDS_STRUCTURING.

    Gate: N_MIN / I_MIN / W_ADMIT, then WF. Out-of-vocab → review queue.
    """
    raise NotImplementedError("Phase 6 — gate: test_end_to_end_golden")
