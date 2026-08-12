"""G6 — the final gate. Nothing is emitted that cannot be traced to a grounded span.

Pure and deterministic: it reads a ledger and decides. No LLM, no wall clock, no writes.

**The rule**, from `PLAN-authoritative-harness.md` §3 G6:

* a `source_span` node is grounded iff its verdict says so;
* a `synthesis` node needs **every** parent grounded;
* every other kind needs **at least one** parent grounded.

The asymmetry is the whole design. An ordinary claim resting on three spans, one of
which failed to verify, still rests on two that did. A synthesis — a brief, a summary,
the paragraph a PM will actually read — is a sentence that BLENDS its parents, so a
single ungrounded parent contaminates the sentence rather than being outvoted by the
others. §G8 calls the summary "the single highest-value place to fabricate"; this is
where that costs something.

**Blocked beats plausible.** `check_emittable` never repairs, never drops the offending
claim and continues, and never downgrades to a warning. It returns a decision, and
`assert_emittable` raises on a refusal. The caller's correct response is
`status="blocked"` with the reason named — `blocked_theme` builds exactly that object.

**Not yet wired.** The plan's integration points (`firewall.run_two_phase` after
`freeze()`, `workflow.run_workflow` before `strategy_family_routed`) are untouched: both
files belong to other work in flight, and wiring a gate that can HALT a live run is a
change that deserves its own review. The gate is complete and tested; turning it on is
one call at each site.
"""
from __future__ import annotations

from typing import Iterable, Optional

from pydantic import BaseModel, ConfigDict

from engine.grounding.provenance_ledger import ProvenanceLedger
from engine.schema.provenance import LedgerNode


class EmitBlockedError(RuntimeError):
    """An emit was refused. Carries the decision so the caller can name the reason on
    the blocked object instead of inventing one."""

    def __init__(self, decision: "EmitDecision") -> None:
        super().__init__(decision.reason or "emit blocked")
        self.decision = decision


class EmitDecision(BaseModel):
    """Why an emit was allowed or refused, in a form a memo can print.

    `blocked_node_ids` is every node that failed, not just the first: a run that halts,
    gets one node fixed and halts again on the next is how a fail-closed gate becomes a
    thing people switch off.
    """

    model_config = ConfigDict(frozen=True)

    allowed: bool
    blocked_node_ids: tuple[str, ...] = ()
    #: `None` when allowed. Otherwise `ungrounded_claim:<id>[,<id>...]` — the same shape
    #: as `ThemeObject.block_reason` elsewhere in the engine.
    reason: Optional[str] = None
    #: Human-readable, one line per failure. The gate must be able to explain itself or
    #: a person cannot act on it.
    detail: tuple[str, ...] = ()


def _grounded(
    node_id: str,
    ledger: ProvenanceLedger,
    memo: dict[str, bool],
    visiting: frozenset[str] = frozenset(),
) -> bool:
    """Is this node traceable to a grounded span, under the kind-specific rule?

    `visiting` guards against a cycle. The ledger's append rule makes cycles
    unconstructible, but the gate is the last thing standing between a claim and a PM,
    and it should not depend on another module's invariant to terminate.
    """
    if node_id in memo:
        return memo[node_id]
    if node_id in visiting:
        return False

    node = ledger.get(node_id)
    if node is None:
        # A dangling citation is not a weak citation. Treat it as ungrounded.
        memo[node_id] = False
        return False

    if node.kind == "source_span":
        result = node.is_grounded_root
    elif not node.parents:
        result = False
    else:
        deeper = visiting | {node_id}
        checks = (_grounded(p, ledger, memo, deeper) for p in node.parents)
        result = all(checks) if node.kind == "synthesis" else any(checks)

    memo[node_id] = result
    return result


def is_grounded(node_id: str, ledger: ProvenanceLedger) -> bool:
    """Public single-node form of the gate's rule."""
    return _grounded(node_id, ledger, {})


def _why(node: Optional[LedgerNode], node_id: str) -> str:
    if node is None:
        return f"{node_id}: cited but never recorded in the ledger"
    if node.kind == "source_span":
        status = node.verdict.status if node.verdict else "missing"
        reason = node.verdict.reason if node.verdict else "no verdict"
        return f"{node_id}: source span is {status} ({reason})"
    if not node.parents:
        return f"{node_id}: {node.kind} rests on nothing (no parents)"
    if node.kind == "synthesis":
        return (
            f"{node_id}: synthesis requires every parent grounded; "
            f"at least one of {list(node.parents)} is not"
        )
    return (
        f"{node_id}: {node.kind} has no grounded parent among {list(node.parents)}"
    )


def check_emittable(node_ids: Iterable[str], ledger: ProvenanceLedger) -> EmitDecision:
    """Decide whether every named node may be emitted. Never raises on a refusal."""
    memo: dict[str, bool] = {}
    blocked = [nid for nid in node_ids if not _grounded(nid, ledger, memo)]
    if not blocked:
        return EmitDecision(allowed=True)
    return EmitDecision(
        allowed=False,
        blocked_node_ids=tuple(blocked),
        reason="ungrounded_claim:" + ",".join(blocked),
        detail=tuple(_why(ledger.get(nid), nid) for nid in blocked),
    )


def assert_emittable(node_ids: Iterable[str], ledger: ProvenanceLedger) -> EmitDecision:
    """`check_emittable`, raising `EmitBlockedError` on a refusal.

    Two entry points on purpose: a caller that wants to record the block on a
    `ThemeObject` uses `check_emittable`; a caller that must not proceed at all uses
    this one and cannot forget to look at the result.
    """
    decision = check_emittable(node_ids, ledger)
    if not decision.allowed:
        raise EmitBlockedError(decision)
    return decision


def blocked_theme(theme, decision: EmitDecision):
    """A blocked copy of a frozen `ThemeObject`, with the gate's reason on it.

    Untyped in the signature so this module does not import the theme schema for one
    `model_copy` — the gate reasons about ledger nodes, and a dependency on the full
    `ThemeObject` graph would make it harder to reuse for the other emit sites.
    """
    if decision.allowed:
        raise ValueError("blocked_theme called on an allowed decision")
    return theme.model_copy(
        update={"status": "blocked", "block_reason": decision.reason}
    )


__all__ = [
    "EmitBlockedError",
    "EmitDecision",
    "assert_emittable",
    "blocked_theme",
    "check_emittable",
    "is_grounded",
]
