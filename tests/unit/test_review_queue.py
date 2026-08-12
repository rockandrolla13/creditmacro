"""The shared review queue (SPEC_AND_STATE §4.2/§4.3, ONTOLOGY_DELTA D-15).

The tests that matter here are structural, not behavioural: the queue's value is that it
records what was flagged and cannot be quietly edited afterwards, and that it sits ABOVE
both subsystems rather than inside one.
"""
from __future__ import annotations

import pytest

from engine.review_queue import (
    InMemoryReviewQueue, JsonlReviewQueue, ReviewItem, ReviewQueue, ReviewReason, enqueue_all,
)

FIXED_CLOCK = lambda: "2026-08-12T00:00:00+00:00"  # noqa: E731


def _item(item_id: str, **kw) -> ReviewItem:
    base = dict(reason=ReviewReason.UNVERIFIED_NUMBER, subject="$440bn of gross supply",
                raised_by="G2")
    base.update(kw)
    return ReviewItem(item_id=item_id, **base)


@pytest.mark.parametrize("make", [
    lambda tmp: InMemoryReviewQueue(clock=FIXED_CLOCK),
    lambda tmp: JsonlReviewQueue(tmp / "q.jsonl", clock=FIXED_CLOCK),
])
def test_both_implementations_satisfy_the_protocol(make, tmp_path):
    assert isinstance(make(tmp_path), ReviewQueue)


@pytest.mark.parametrize("make", [
    lambda tmp: InMemoryReviewQueue(clock=FIXED_CLOCK),
    lambda tmp: JsonlReviewQueue(tmp / "q.jsonl", clock=FIXED_CLOCK),
])
def test_resolution_supersedes_and_never_erases(make, tmp_path):
    """The load-bearing property. A resolved item leaves `pending()` but stays in the record.

    A queue you can edit records what someone wanted flagged, not what was flagged. The
    same reason `ledger/substrate/store.py` has no update path.
    """
    q = make(tmp_path)
    q.enqueue(_item("r1"))
    q.enqueue(_item("r2", subject="verified by hand", raised_by="human", supersedes="r1"))

    assert [i.item_id for i in q.pending()] == ["r2"]
    assert [i.item_id for i in q.all_items()] == ["r1", "r2"]   # the original survives


@pytest.mark.parametrize("make", [
    lambda tmp: InMemoryReviewQueue(clock=FIXED_CLOCK),
    lambda tmp: JsonlReviewQueue(tmp / "q.jsonl", clock=FIXED_CLOCK),
])
def test_no_update_or_delete_path_exists(make, tmp_path):
    """Enforced by absence, not by convention — the shape the ledger store already uses."""
    q = make(tmp_path)
    for forbidden in ("update", "delete", "remove", "resolve", "clear", "pop"):
        assert not hasattr(q, forbidden), f"{forbidden} would make the record editable"


def test_recorded_at_is_stamped_by_the_store_not_the_caller(tmp_path):
    """I7: the caller leaves it None and the store stamps it, from an injected clock (I8)."""
    q = JsonlReviewQueue(tmp_path / "q.jsonl", clock=FIXED_CLOCK)
    submitted = _item("r1")
    assert submitted.recorded_at is None
    assert q.enqueue(submitted).recorded_at == FIXED_CLOCK()


def test_jsonl_queue_survives_a_reopen(tmp_path):
    """It is a record; a record that does not outlive the process is a variable."""
    path = tmp_path / "q.jsonl"
    JsonlReviewQueue(path, clock=FIXED_CLOCK).enqueue(_item("r1"))
    assert [i.item_id for i in JsonlReviewQueue(path).pending()] == ["r1"]


def test_enqueue_all_preserves_order(tmp_path):
    q = InMemoryReviewQueue(clock=FIXED_CLOCK)
    enqueue_all(q, [_item("r1"), _item("r2"), _item("r3")])
    assert [i.item_id for i in q.all_items()] == ["r1", "r2", "r3"]


def test_the_old_ledger_stub_refuses_and_says_where_to_go():
    """D-15 deliberately leaves NO shim.

    Re-exporting from the old location would let the wrong dependency direction survive as
    a habit, and not creating that edge was the entire point of moving it.
    """
    from engine.ledger.wiki import review_queue as moved

    with pytest.raises(NotImplementedError) as excinfo:
        moved.enqueue({})
    assert "engine.review_queue" in str(excinfo.value)
    assert not hasattr(moved, "ReviewItem"), "a shim would defeat the move"


def test_the_queue_does_not_import_either_subsystem():
    """It sits ABOVE both, so it must depend on neither (§4.3).

    If this fails, the queue has been pulled inside one of the systems it exists to serve
    from outside, and D5's 'two in-flight systems joined together' problem is back.
    """
    import pathlib
    src = pathlib.Path("engine/review_queue.py").read_text()
    for forbidden in ("engine.ledger", "from .ledger", "engine.grounding", "from .grounding"):
        assert forbidden not in src, f"review_queue must not import {forbidden}"
