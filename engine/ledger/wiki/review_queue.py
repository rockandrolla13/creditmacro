"""MOVED — the review queue now lives at `engine.review_queue`, above both subsystems.

This module was a Phase-0/7 stub: one function raising `NotImplementedError`, zero
callers, ever. D1 nonetheless routed the grounding harness's human gate here, describing
it as *"small, finished, and already does this"*. It was none of those things, and a
builder following D1 as written would have added an enum member to a function that cannot
run (`SPEC_AND_STATE` §4.2).

The deeper problem was structural, not clerical (§4.3). D5 keeps the provenance ledger out
of the hypothesis ledger because *"two in-flight systems joined together is how both
stall"*, and `engine/ledger/` has exactly one outward import with **nothing importing
inward**. Putting the shared queue here would have created that first inbound edge, into
the least finished subsystem, on behalf of a caller that lives elsewhere.

Decision (user, 2026-08-12; `ONTOLOGY_DELTA` D-15): the queue is shared infrastructure and
belongs above both. Import `engine.review_queue` instead. Nothing is re-exported from here
deliberately — a shim would let the wrong dependency direction survive as a habit, and the
whole point was to not create that edge.
"""
from __future__ import annotations


def enqueue(*_args, **_kwargs):
    """Removed. Use `engine.review_queue.ReviewQueue.enqueue` (D-15)."""
    raise NotImplementedError(
        "engine.ledger.wiki.review_queue has MOVED to engine.review_queue (ONTOLOGY_DELTA "
        "D-15). The queue is shared infrastructure owned by neither the hypothesis ledger "
        "nor the grounding harness; importing it from inside engine/ledger/ would create "
        "the ledger's first inbound dependency, which D5 exists to prevent. "
        "Use: from engine.review_queue import ReviewItem, ReviewReason, JsonlReviewQueue"
    )
