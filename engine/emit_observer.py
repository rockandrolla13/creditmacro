"""The emit gate in OBSERVE mode — it files a review item instead of halting.

**Why observe and not enforce.** The gate is finished and correct: given a populated
provenance ledger it allows a grounded claim and blocks a fabricated one by id. Turning it
straight on would let it HALT a live run, and the honest position today is that we do not
yet know the rejection rate on real documents. The curated alias map has five entries
(`SPEC_AND_STATE` §4.8b) and the tokenizer is still incomplete, so the first thing a strict
gate would do is stop good work because of the harness's own gaps. That is the same trade
already declined in §4.4 when grounding was set to lint.

**Why the review queue and not a log.** A warning that goes to stdout is a warning nobody
reads, and a gate whose output nobody reads is off with extra steps. An unsupported claim
at the emit boundary is precisely a thing a human must look at, which is what
`engine.review_queue` exists for — so the observation lands there, with the blocking node
ids attached and the producer named.

**The measurement this exists to produce.** §4.4's flip condition is a count, not a
judgement: run this over real batches, read `queue.pending()`, and see whether refusals are
dominated by genuinely absent figures or by tokenizer misses. When it is the former,
`enforce=True` becomes defensible. Until then this records what a strict gate WOULD have
stopped, at zero risk to a live run.

No wall clock (I8): `now` is a parameter, and the queue stamps `recorded_at` itself (I7).
"""
from __future__ import annotations

from typing import Iterable, Optional

from .grounding.emit_gate import EmitDecision, EmitBlockedError, check_emittable
from .grounding.provenance_ledger import ProvenanceLedger
from .review_queue import ReviewItem, ReviewQueue, ReviewReason


def observe_emit(
    node_ids: Iterable[str],
    ledger: Optional[ProvenanceLedger],
    *,
    stage: str,
    queue: Optional[ReviewQueue] = None,
    item_id: Optional[str] = None,
    enforce: bool = False,
) -> Optional[EmitDecision]:
    """Check whether these nodes are emittable. Record a refusal; raise only if asked.

    Returns None when there is nothing to check — no ledger, or no node ids. That is a
    deliberate distinction from an ALLOWED decision: "the gate did not run" and "the gate
    ran and approved" must not look the same to a caller, or an unwired gate reads as a
    passing one. That is exactly how invariant I8 sat vacuous for three days.

    `enforce=True` restores the halting behaviour in one flag, for when the measurement
    below says the rejection rate is dominated by real absences rather than harness gaps.
    """
    ids = list(node_ids)
    if ledger is None or not ids:
        return None

    decision = check_emittable(ids, ledger)
    if decision.allowed:
        return decision

    if queue is not None:
        queue.enqueue(ReviewItem(
            item_id=item_id or f"emit:{stage}:{decision.blocked_node_ids[0]}",
            reason=ReviewReason.UNGROUNDED_CLAIM,
            subject=f"{stage}: {len(decision.blocked_node_ids)} claim(s) rest on nothing",
            source_ref=",".join(decision.blocked_node_ids),
            detail=decision.reason,
            raised_by=f"emit_gate/observe:{stage}",
        ))

    if enforce:
        raise EmitBlockedError(decision)
    return decision
