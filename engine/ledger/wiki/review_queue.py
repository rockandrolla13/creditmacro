"""Append-only, human-gated review queues (ONTOLOGY §Admission, §Rendered view).

Three sinks, nothing auto-applied:
  - OUT_OF_VOCAB    : proposed vocabulary additions (§Admission out-of-vocab path)
  - NEEDS_STRUCTURING: objects failing WF, with the failing clause named
  - ANALYST_DRIFT   : drift-diff proposed events (provenance='analyst')

Append-only like the ledger stores. Phase-0/7 companion.
"""
from __future__ import annotations

from enum import Enum


class Queue(str, Enum):
    OUT_OF_VOCAB = "out_of_vocab"
    NEEDS_STRUCTURING = "needs_structuring"
    ANALYST_DRIFT = "analyst_drift"


def enqueue(queue: Queue, item: dict) -> None:
    """Append one review item. No dequeue-with-mutate path — resolution is a new event."""
    raise NotImplementedError("Phase 0/7 — append-only JSONL per queue")
