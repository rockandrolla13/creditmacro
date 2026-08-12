"""Populate the provenance ledger from a grounding pass — the step G6 was missing.

**Why this module had to exist before the emit gate could be switched on.** `emit_gate`
was built, tested and left unwired, and the reason it could not simply be wired is that
**nothing wrote to the ledger it checks against**. `ProvenanceLedger` had an `append` and
no producers. Wiring the gate in that state would have made it report every claim as
ungrounded on its first run — a false alarm on everything, which is how a gate gets
switched off permanently and stays off. A gate that cries wolf is worse than no gate,
because it teaches people to ignore it.

So this is the producer. It turns the output of a grounding pass into the citation graph
the gate walks:

    source_span   one per atom, carrying the atom's own GroundingVerdict
        ↑
    atom          parented on its span

**Ungrounded atoms are RECORDED, not skipped.** `LedgerNode`'s own docstring insists on
this: *"An UNGROUNDED verdict is recorded, not discarded — the gate refuses it, and a
refusal you can see beats a claim that vanished."* So `enforce`'s rejected half lands here
too, with its failing verdict attached. The gate then refuses those nodes by rule rather
than by their absence, and a human can ask why. An atom that never reached the ledger is
indistinguishable from an atom nobody produced.

**Ids are derived, not generated.** `evidence_id` is already unique per bundle, so the
span is `<evidence_id>:span` and the atom is `<evidence_id>`. Two runs over the same
document produce the same graph — required by I8 and by the golden master.

No wall clock (I8): `created_at` is a parameter. There is no default, deliberately; a
caller that has no defensible timestamp should not be writing provenance.
"""
from __future__ import annotations

from typing import Any, Iterable, Optional, Sequence

from engine.schema.grounding import GroundingVerdict
from engine.schema.provenance import LedgerNode

from .provenance_ledger import ProvenanceLedger


def _span_id(evidence_id: str) -> str:
    return f"{evidence_id}:span"


def _verdict_of(atom: Any, fallback: Optional[GroundingVerdict]) -> Optional[GroundingVerdict]:
    """The verdict `enforce` stamped on the atom, or the one carried alongside it.

    `enforce` stamps kept atoms with `grounding` and returns rejected ones as
    `(atom, verdict)` pairs, so the two halves arrive shaped differently. This flattens
    that difference rather than making every caller know about it.
    """
    return getattr(atom, "grounding", None) or fallback


def record_atom(
    atom: Any,
    ledger: ProvenanceLedger,
    *,
    source_slug: str,
    created_at: str,
    verdict: Optional[GroundingVerdict] = None,
) -> Optional[str]:
    """Append one atom's span + atom nodes. Returns the atom node id, or None.

    None means the atom carried no verdict at all — it never went through `enforce`, so
    there is nothing to record and inventing a verdict here would be the fabrication the
    whole harness exists to prevent.
    """
    evidence_id = getattr(atom, "evidence_id", None)
    v = _verdict_of(atom, verdict)
    if not evidence_id or v is None:
        return None

    span_id = _span_id(evidence_id)
    if ledger.get(span_id) is None:
        ledger.append(LedgerNode(
            id=span_id,
            kind="source_span",
            source_slug=source_slug,
            span_char_start=v.span_char_start,
            span_char_end=v.span_char_end,
            verdict=v,
            created_at=created_at,
            note=v.reason,
        ))
    if ledger.get(evidence_id) is None:
        ledger.append(LedgerNode(
            id=evidence_id,
            kind="atom",
            parents=(span_id,),
            source_slug=source_slug,
            created_at=created_at,
            note=getattr(atom, "claim", "")[:120],
        ))
    return evidence_id


def record_enforced(
    kept: Sequence[Any],
    rejected: Iterable[tuple[Any, GroundingVerdict]],
    ledger: ProvenanceLedger,
    *,
    source_slug: str,
    created_at: str,
) -> list[str]:
    """Record BOTH halves of an `EnforcedBundle`. Returns the recorded atom node ids.

    Both halves, because the ledger's job is to say what the run saw. Recording only the
    survivors would make the gate's later refusals unexplainable: it would report a claim
    as unsupported with no record of the attempt that failed.
    """
    ids: list[str] = []
    for atom in kept:
        node_id = record_atom(atom, ledger, source_slug=source_slug, created_at=created_at)
        if node_id:
            ids.append(node_id)
    for atom, verdict in rejected:
        node_id = record_atom(atom, ledger, source_slug=source_slug,
                              created_at=created_at, verdict=verdict)
        if node_id:
            ids.append(node_id)
    return ids


def record_derived(
    node_id: str,
    kind: str,
    parent_ids: Sequence[str],
    ledger: ProvenanceLedger,
    *,
    created_at: str,
    note: str = "",
) -> str:
    """Append a node that rests on atoms already recorded — a causal claim, an axis, a
    routed family.

    Parents are NOT checked for existence here: `ProvenanceLedger.append` already refuses
    a node whose parents are absent, and duplicating that check would give two places to
    keep in step. A caller passing an unknown parent gets an error from the store, which
    is the module that owns the rule.
    """
    ledger.append(LedgerNode(
        id=node_id, kind=kind, parents=tuple(parent_ids),
        created_at=created_at, note=note,
    ))
    return node_id
