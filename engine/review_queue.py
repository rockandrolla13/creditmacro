"""The human review queue — shared infrastructure, owned by neither subsystem.

**Why this is here and not inside something.** D1 routed the harness's human gate into
`engine/ledger/wiki/review_queue.py`, describing that module as *"small, finished, and
already does this"*. It is a 23-line stub whose only function raises `NotImplementedError`
and which has never had a caller. D5 says the opposite thing for a good reason — *"two
in-flight systems joined together is how both stall"* — and `engine/ledger/` today has
exactly one outward import and **nothing importing inward**. Following D1 as written would
have created that first inbound edge, into the least finished part of the tree.

Decision (user, 2026-08-12, `SPEC_AND_STATE` §4.2/§4.3): the queue lives **above both**.
The grounding harness is its only caller today, and the ledger will be its second. A queue
owned by its first caller is a queue the second caller has to depend on sideways, and that
is the coupling D5 was protecting against. Recorded as `ONTOLOGY_DELTA` D-15.

**What it is for.** Anything a human must look at before the machine proceeds: a figure the
tokenizer could not verify, a mechanism tag outside the controlled vocabulary, a Tier-C
loose grounding match. It is a queue, not a decision — nothing here resolves an item, and
resolving one is deliberately outside this module.

**Append-only, like everything else that records what happened.** There is no update and no
delete path, by construction — the same shape as `engine/ledger/substrate/store.py`, and
for the same reason: a review queue you can silently edit is a record of what someone
wanted to have flagged, not of what was flagged. Resolution is a NEW entry that supersedes.

No wall clock (invariant I8): `recorded_at` is stamped by the store from an injected clock,
never read from the caller's environment mid-computation.
"""
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Callable, Iterable, Optional, Protocol, Sequence, Union, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field


class ReviewReason(str, Enum):
    """Why a human is being asked to look. Extend deliberately: each member is a promise
    that some producer routes here, and an unused member reads as coverage that does not
    exist."""

    UNVERIFIED_NUMBER = "unverified_number"       # G2: tokenizer could not confirm a figure
    LOOSE_GROUNDING = "loose_grounding"           # D1 Tier C: matched, but not tightly
    OUT_OF_VOCABULARY = "out_of_vocabulary"       # ledger §Admission: unknown mechanism tag
    UNGROUNDED_CLAIM = "ungrounded_claim"         # G1: quote not found in the source
    CONTESTED_DIRECTION = "contested_direction"   # D-11: a cluster supporting no σ
    ADJUDICATION_SPLIT = "adjudication_split"     # G3: proposer and verifier disagree


class ReviewItem(BaseModel):
    """One thing awaiting a human. Frozen; corrections are new items (see `supersedes`)."""

    model_config = ConfigDict(frozen=True)

    item_id: str
    reason: ReviewReason
    subject: str                                  # what is being questioned, in one line
    source_ref: Optional[str] = None              # slug / doc id / node id, if there is one
    detail: str = ""                              # why the producer could not decide
    #: The producer's own name. Not decoration: when a queue fills with noise the first
    #: question is always which producer is generating it, and without this you cannot ask.
    raised_by: str = ""
    recorded_at: Optional[str] = None             # stamped by the store only (I7)
    supersedes: Optional[str] = None              # item_id of the entry this replaces


@runtime_checkable
class ReviewQueue(Protocol):
    """Append-only queue. No update, no delete, no resolve — by construction."""

    def enqueue(self, item: ReviewItem) -> ReviewItem: ...
    def pending(self) -> Sequence[ReviewItem]: ...
    def all_items(self) -> Sequence[ReviewItem]: ...


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class JsonlReviewQueue:
    """Append-only JSONL queue, mirroring `ledger/substrate/store.py`.

    `pending()` excludes anything a later entry supersedes, so a resolved item disappears
    from the working list WITHOUT the original row being altered. That is the difference
    between a record and a whiteboard.
    """

    def __init__(self, path: Union[str, Path], *, clock: Callable[[], str] = _utc_now_iso) -> None:
        self._path = Path(path)
        self._clock = clock

    def enqueue(self, item: ReviewItem) -> ReviewItem:
        stamped = item.model_copy(update={"recorded_at": self._clock()})
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a") as f:
            f.write(stamped.model_dump_json() + "\n")
        return stamped

    def _read_all(self) -> list[ReviewItem]:
        if not self._path.exists():
            return []
        return [ReviewItem.model_validate_json(ln)
                for ln in self._path.read_text().splitlines() if ln.strip()]

    def all_items(self) -> Sequence[ReviewItem]:
        return self._read_all()

    def pending(self) -> Sequence[ReviewItem]:
        items = self._read_all()
        superseded = {i.supersedes for i in items if i.supersedes}
        return [i for i in items if i.item_id not in superseded]


class InMemoryReviewQueue:
    """Deterministic queue for tests and for callers that must not touch disk."""

    def __init__(self, *, clock: Callable[[], str] = _utc_now_iso) -> None:
        self._items: list[ReviewItem] = []
        self._clock = clock

    def enqueue(self, item: ReviewItem) -> ReviewItem:
        stamped = item.model_copy(update={"recorded_at": self._clock()})
        self._items.append(stamped)
        return stamped

    def all_items(self) -> Sequence[ReviewItem]:
        return list(self._items)

    def pending(self) -> Sequence[ReviewItem]:
        superseded = {i.supersedes for i in self._items if i.supersedes}
        return [i for i in self._items if i.item_id not in superseded]


def enqueue_all(queue: ReviewQueue, items: Iterable[ReviewItem]) -> list[ReviewItem]:
    """Convenience for a producer emitting several at once. Order is preserved."""
    return [queue.enqueue(i) for i in items]
