"""G6 contract — the append-only citation graph tying an emitted claim to a span.

Capture/replay records what the pipeline DID. The provenance ledger records what each
statement RESTS ON. They answer different questions, and only the second one answers
"show me every claim that depends on this source".

One node type, deliberately. A graph of one node kind with a `kind` discriminator is
navigable by code that does not know the taxonomy — the emit gate walks `parents`
without caring whether it is standing on an axis or a scenario — where seven sibling
classes would need seven cases and would grow an eighth silently.

**Append-only.** `parents` may only name nodes that already exist, which is what makes
the graph acyclic without a cycle check: you cannot cite something that has not been
recorded yet. Enforced in `engine.grounding.provenance_ledger`, and in SQL by triggers
for the persistent store.

**No wall clock (I8).** `created_at` is supplied by the caller. A ledger that stamps its
own timestamps cannot be replayed, and a provenance record that changes between runs is
not provenance.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, model_validator

from engine.schema.grounding import GroundingVerdict

#: What a node stands for. `source_span` is the only kind that can be grounded on its
#: own — everything else is grounded by descent. `synthesis` is the escape hatch that
#: makes summaries expressible, and it is a LOUD one: the emit gate applies a stricter
#: rule to it than to any other kind (every parent grounded, not merely one).
LedgerNodeKind = Literal[
    "source_span",
    "atom",
    "causal_claim",
    "axis",
    "scenario_evidence",
    "strategy_family",
    "synthesis",
]


class LedgerNode(BaseModel):
    """One node in the citation graph. Frozen — a provenance record that can be edited
    after the fact records the edit, not the provenance."""

    model_config = ConfigDict(frozen=True)

    id: str
    kind: LedgerNodeKind
    #: Ids of the nodes this one rests on. Empty is legal at construction and is what
    #: the emit gate blocks on: an unparented claim is a claim resting on nothing, and
    #: refusing it at the GATE rather than at construction keeps validation errors
    #: (a broken caller) distinct from blocks (an unsupported claim).
    parents: tuple[str, ...] = ()
    source_slug: Optional[str] = None
    span_char_start: Optional[int] = None
    span_char_end: Optional[int] = None
    #: Set on `source_span` nodes. An UNGROUNDED verdict is recorded, not discarded —
    #: the gate refuses it, and a refusal you can see beats a claim that vanished.
    verdict: Optional[GroundingVerdict] = None
    #: Caller-supplied ISO-8601 instant. See the module docstring: never the wall clock.
    created_at: str
    note: str = ""

    @model_validator(mode="after")
    def _source_spans_carry_their_evidence(self) -> "LedgerNode":
        if self.kind == "source_span":
            if self.verdict is None:
                raise ValueError("a source_span node must carry its GroundingVerdict")
            if not self.source_slug:
                raise ValueError("a source_span node must name its source")
            if self.parents:
                raise ValueError("a source_span node is a root and has no parents")
        elif self.verdict is not None:
            raise ValueError(
                f"only a source_span node carries a verdict (got kind={self.kind!r}); "
                "a derived claim is grounded by descent, not by assertion"
            )
        return self

    @property
    def is_grounded_root(self) -> bool:
        """True only for a `source_span` whose verdict is `grounded`."""
        return self.kind == "source_span" and self.verdict is not None and self.verdict.is_grounded
