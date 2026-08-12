"""G6 population — the step that had to exist before the emit gate could be switched on.

`emit_gate` was built, tested and left unwired, and the reason was not caution: NOTHING
wrote to the ledger it checks. Wiring it against an empty ledger would have reported every
claim as ungrounded on the first run — a false alarm on everything, which is how a gate
gets switched off and stays off. These tests pin that the ledger now carries real verdicts
and that the gate decides on them.
"""
from __future__ import annotations

from engine.evidence_extraction import EvidenceExtractionInput, extract_evidence
from engine.grounding import GroundingPolicy, SourceIndex, enforce
from engine.grounding.emit_gate import check_emittable, is_grounded
from engine.grounding.provenance_ledger import InMemoryProvenanceLedger
from engine.grounding.record import record_enforced
from engine.schema import EvidenceAtom

MD = "Gross supply reached $440bn in May, a record for the sector."
STAMP = "2026-08-12T00:00:00+00:00"


def _atom(evidence_id: str, claim: str, span: str) -> EvidenceAtom:
    return EvidenceAtom(
        evidence_id=evidence_id, source_slug="s", source_location="page:1", claim=claim,
        claim_kind="source_fact", numbers=[], confidence=0.6,
        agent_use="case evidence", source_span=span,
    )


def _enforced_ledger():
    bundle = enforce(
        [_atom("e1", "real claim", MD), _atom("e2", "invented", "Not in the document at all.")],
        SourceIndex(MD), GroundingPolicy(mode="lint"),
    )
    ledger = InMemoryProvenanceLedger()
    ids = record_enforced(bundle.kept, bundle.rejected, ledger,
                          source_slug="s", created_at=STAMP)
    return bundle, ledger, ids


def test_both_halves_are_recorded_not_just_the_survivors():
    """An atom that never reached the ledger is indistinguishable from one nobody produced.

    Recording only the kept half would make the gate's refusals unexplainable — a claim
    reported unsupported with no record of the attempt that failed.
    """
    bundle, ledger, ids = _enforced_ledger()
    assert len(bundle.kept) == 1 and len(bundle.rejected) == 1
    assert ids == ["e1", "e2"]                       # the rejected atom is recorded too
    assert len(ledger.nodes()) == 4                  # a span AND an atom node for each


def test_the_gate_decides_on_real_verdicts():
    """The point of the whole exercise: grounded passes, fabricated is blocked BY ID."""
    _, ledger, ids = _enforced_ledger()
    assert is_grounded("e1", ledger) is True
    assert is_grounded("e2", ledger) is False

    decision = check_emittable(ids, ledger)
    assert decision.allowed is False
    assert decision.blocked_node_ids == ("e2",)
    assert "e2" in decision.reason


def test_a_fully_grounded_set_is_allowed():
    """The gate must be able to say yes, or it is not a gate — it is an off switch."""
    bundle, _, _ = _enforced_ledger()
    ledger = InMemoryProvenanceLedger()
    ids = record_enforced(bundle.kept, [], ledger, source_slug="s", created_at=STAMP)
    assert check_emittable(ids, ledger).allowed is True


def test_recording_is_deterministic_across_runs():
    """I8 and the golden master both require it. Ids are derived from evidence_id, not generated."""
    first = [n.id for n in _enforced_ledger()[1].nodes()]
    second = [n.id for n in _enforced_ledger()[1].nodes()]
    assert first == second
    # Insertion order, and a span always precedes the atom that cites it — the ledger
    # refuses a node whose parents are absent, so this ordering is the append rule
    # showing through, not an incidental detail.
    assert first == ["e1:span", "e1", "e2:span", "e2"]


def test_extraction_records_provenance_only_when_a_ledger_is_passed():
    """Off by default, so every existing caller and the golden master are untouched."""
    inp = EvidenceExtractionInput(
        source_slug="s", source_type="report", access_class="case",
        normalized_markdown=MD, source_date="2026-05-01", current_date="2026-05-02",
    )
    ledger = InMemoryProvenanceLedger()

    extract_evidence(inp)                                  # no ledger -> nothing written
    assert ledger.nodes() == []

    extract_evidence(inp, provenance=ledger)
    assert ledger.nodes(), "a supplied ledger must be populated"
    assert all(n.created_at == "2026-05-02" for n in ledger.nodes()), "no wall clock (I8)"


def test_extraction_does_not_gate_it_only_records():
    """Recording belongs in extraction; REFUSING belongs at the emit boundary.

    Halting here would stop a run on the harness's own coverage gaps — the same trade
    already decided against in SPEC_AND_STATE 4.4.
    """
    inp = EvidenceExtractionInput(
        source_slug="s", source_type="case", access_class="case",
        normalized_markdown=MD, source_date="2026-05-01", current_date="2026-05-02",
    )
    ledger = InMemoryProvenanceLedger()
    bundle = extract_evidence(inp, provenance=ledger)      # must not raise
    assert bundle is not None
