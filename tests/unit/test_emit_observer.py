"""The emit gate in observe mode, at both publish boundaries.

The user's decision (2026-08-12) was "plug it in, but only warn at first". These tests pin
the three properties that makes that mean something: it runs, it does NOT halt, and the
warning lands somewhere a human looks rather than in a log.
"""
from __future__ import annotations

import pytest

from engine.emit_observer import observe_emit
from engine.grounding import GroundingPolicy, SourceIndex, enforce
from engine.grounding.emit_gate import EmitBlockedError
from engine.grounding.provenance_ledger import InMemoryProvenanceLedger
from engine.grounding.record import record_enforced
from engine.review_queue import InMemoryReviewQueue, ReviewReason
from engine.schema import EvidenceAtom

MD = "Gross supply reached $440bn in May, a record for the sector."
STAMP = "2026-08-12T00:00:00+00:00"


def _atom(eid: str, span: str) -> EvidenceAtom:
    return EvidenceAtom(evidence_id=eid, source_slug="s", source_location="page:1",
                        claim="c", claim_kind="source_fact", numbers=[], confidence=0.6,
                        agent_use="case evidence", source_span=span)


def _ledger_with(good: bool):
    atoms = [_atom("e1", MD)] if good else [_atom("e1", MD), _atom("e2", "Not in the doc.")]
    b = enforce(atoms, SourceIndex(MD), GroundingPolicy(mode="lint"))
    led = InMemoryProvenanceLedger()
    ids = record_enforced(b.kept, b.rejected, led, source_slug="s", created_at=STAMP)
    return led, ids


def test_an_unsupported_claim_is_filed_for_review_and_does_not_halt():
    """The whole point of observe mode. It records; it does not stop the run."""
    led, ids = _ledger_with(good=False)
    queue = InMemoryReviewQueue(clock=lambda: STAMP)

    decision = observe_emit(ids, led, stage="strategy_family_routed", queue=queue)

    assert decision is not None and decision.allowed is False    # it ran and it refused
    (item,) = queue.pending()                                    # and a human will see it
    assert item.reason is ReviewReason.UNGROUNDED_CLAIM
    assert "e2" in item.source_ref
    assert item.raised_by == "emit_gate/observe:strategy_family_routed"


def test_a_clean_run_files_nothing():
    """A queue that fills on every run is a queue nobody reads."""
    led, ids = _ledger_with(good=True)
    queue = InMemoryReviewQueue(clock=lambda: STAMP)
    assert observe_emit(ids, led, stage="pre_freeze", queue=queue).allowed is True
    assert list(queue.pending()) == []


def test_not_run_is_distinguishable_from_ran_and_approved():
    """The load-bearing distinction. `None` means the gate did not run.

    If an unwired gate returned an ALLOWED decision, it would read as a passing check —
    which is precisely how invariant I8 sat vacuous for three days, reporting clean while
    grepping three files that did not exist.
    """
    led, ids = _ledger_with(good=True)
    assert observe_emit(ids, None, stage="s") is None            # no ledger -> did not run
    assert observe_emit([], led, stage="s") is None              # nothing to check
    assert observe_emit(ids, led, stage="s") is not None         # ran


def test_enforce_restores_halting_in_one_flag():
    """When the measurement in SPEC_AND_STATE 4.4 justifies it, this is the switch."""
    led, ids = _ledger_with(good=False)
    with pytest.raises(EmitBlockedError):
        observe_emit(ids, led, stage="s", enforce=True)


def test_the_workflow_and_firewall_accept_the_seam_without_it_changing_anything():
    """Both boundaries take the parameters and default to off, so existing callers are
    untouched — the property that let this be wired at all."""
    import inspect
    from engine.firewall import run_two_phase
    from engine.workflow import run_workflow

    for fn in (run_workflow, run_two_phase):
        params = inspect.signature(fn).parameters
        for name in ("provenance", "review_queue", "enforce_emit"):
            assert name in params, f"{fn.__name__} is missing {name}"
        assert params["provenance"].default is None
        assert params["enforce_emit"].default is False
