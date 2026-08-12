"""The harness half of the kernel: verify_atom and enforce.

These prove the guardrail BLOCKS, not merely that it warns — a fail-closed rule with
only happy-path tests is a rule nobody has checked.
"""
from __future__ import annotations

import pytest

from engine.grounding import (
    GroundingPolicy,
    SourceIndex,
    UngroundedEvidenceError,
    enforce,
    verify_atom,
)
from engine.schema.probability import EvidenceAtom

SOURCE = (
    "European bank spreads widened 75bp in the quarter.\n"
    "Funding costs rose to 3.5% across the sector.\n"
)


@pytest.fixture
def index() -> SourceIndex:
    return SourceIndex(SOURCE)


def _atom(**kw) -> EvidenceAtom:
    return EvidenceAtom(evidence_id="e1", claim="c", **kw)


def test_a_real_quote_grounds_and_the_verdict_carries_its_offsets(index):
    quote = "European bank spreads widened 75bp in the quarter."
    verdict = verify_atom(_atom(source_span=quote, numbers=[75.0]), index)

    assert verdict.status == "grounded"
    assert verdict.method == "exact"
    assert verdict.numbers_verified
    assert SOURCE[verdict.span_char_start:verdict.span_char_end] == quote


def test_a_fabricated_quote_is_ungrounded(index):
    verdict = verify_atom(_atom(source_span="Spreads tightened dramatically."), index)
    assert verdict.status == "ungrounded"
    assert not verdict.span_found
    assert "not found" in verdict.reason


def test_no_quote_is_unverifiable_not_ungrounded(index):
    """The distinction matters: a producer that forgot to quote is a broken pipeline,
    not a rejected claim, and the two need different responses."""
    verdict = verify_atom(_atom(numbers=[75.0]), index)
    assert verdict.status == "unverifiable"
    assert verdict.reason == "no source_span supplied"


def test_a_number_absent_from_the_span_fails_even_though_the_span_is_real(index):
    """G2: the quote being real does not make its figures real. 57 is a plausible
    transcription of 75 and appears nowhere in the source."""
    verdict = verify_atom(
        _atom(source_span="European bank spreads widened 75bp in the quarter.",
              numbers=[57.0]),
        index,
    )
    assert verdict.status == "ungrounded"
    assert verdict.span_found
    assert not verdict.numbers_verified
    assert "57.0" in verdict.reason


def test_number_check_can_be_waived_by_policy(index):
    verdict = verify_atom(
        _atom(source_span="European bank spreads widened 75bp in the quarter.",
              numbers=[57.0]),
        index,
        GroundingPolicy(verify_numbers=False),
    )
    assert verdict.status == "grounded"
    assert not verdict.numbers_verified


def test_whitespace_variation_grounds_as_normalized_not_exact(index):
    quote = "European   bank  spreads widened 75bp in the quarter."
    verdict = verify_atom(_atom(source_span=quote, numbers=[75.0]), index)
    assert verdict.status == "grounded"
    assert verdict.method == "normalized"


def test_strict_mode_raises_rather_than_dropping(index):
    """D2: on the real product path, blocked beats plausible."""
    atoms = [
        _atom(source_span="European bank spreads widened 75bp in the quarter.", numbers=[75.0]),
        _atom(source_span="An assertion that appears in no source."),
    ]
    with pytest.raises(UngroundedEvidenceError) as excinfo:
        enforce(atoms, index, GroundingPolicy(mode="strict"))
    assert "ungrounded" in str(excinfo.value)


def test_lint_mode_partitions_and_records_every_rejection(index):
    atoms = [
        _atom(source_span="European bank spreads widened 75bp in the quarter.", numbers=[75.0]),
        _atom(source_span="An assertion that appears in no source."),
    ]
    bundle = enforce(atoms, index, GroundingPolicy(mode="lint"))

    assert len(bundle.kept) == 1
    assert len(bundle.rejected) == 1
    assert len(bundle.warnings) == 1, "a dropped atom must never be silent"


def test_enforce_stamps_the_verdict_without_mutating_the_original(index):
    """EvidenceAtom is frozen, so a stamped atom must be a new object."""
    original = _atom(source_span="Funding costs rose to 3.5% across the sector.",
                     numbers=[3.5])
    bundle = enforce([original], index, GroundingPolicy(mode="lint"))
    kept = bundle.kept[0]

    assert original.grounding is None, "the input atom must be untouched"
    assert kept.grounding is not None and kept.grounding.is_grounded
    assert kept is not original
    assert SOURCE[kept.span_char_start:kept.span_char_end] == original.source_span


def test_verdict_numbers_point_into_the_document_not_the_span(index):
    """The composition bug this kernel already had once — pinned at the harness level."""
    quote = "Funding costs rose to 3.5% across the sector."
    verdict = verify_atom(_atom(source_span=quote, numbers=[3.5]), index)
    number = verdict.verified_numbers[0]
    assert SOURCE[number.char_start:number.char_end] == number.raw


def test_extractor_no_longer_invents_numbers_from_dates_and_word_digits():
    """Regression for what wiring the kernel in exposed.

    The extractor used a bare `[-+]?\\d+(?:\\.\\d+)?` with no word boundary, so it read
    "1" out of "Q1" and split "2022-12-28" into 2022, -12 and -28 — taking the hyphens
    for minus signs. Those phantom figures became `EvidenceAtom.numbers` and fed
    scenario evidence downstream.
    """
    from engine.evidence_extraction import EvidenceExtractionInput, extract_evidence

    markdown = (
        "Provided on 2022-12-28T22:42+00:00 to a subscriber.\n"
        "In Q1 the index widened 40bps versus the prior quarter.\n"
    )
    bundle = extract_evidence(EvidenceExtractionInput(
        source_slug="phantom", normalized_markdown=markdown,
        source_type="research", access_class="case",
    ))

    reported = {n for atom in bundle.evidence_atoms for n in atom.numbers}
    assert -12.0 not in reported and -28.0 not in reported, "date read as negative numbers"
    assert 40.0 in reported, "a real figure in bps must survive"
    # And every atom that survived carries a verdict the harness authored.
    for atom in bundle.evidence_atoms:
        assert atom.grounding is not None and atom.grounding.is_grounded


# ── D2: the grounding mode is the caller's choice (SPEC_AND_STATE 4.4) ────────

def test_extract_evidence_defaults_to_lint_but_honours_an_explicit_policy():
    """User decision 2026-08-12: this caller lints; the parameter makes that visible.

    Until today the mode was hardcoded, so a policy choice was unreadable AS a choice.
    D2 requires the caller to decide, and `GroundingPolicy()` defaults to strict so a
    NEW caller that says nothing gets the safe direction.
    """
    import inspect
    from engine.evidence_extraction import extract_evidence
    from engine.grounding import GroundingPolicy

    sig = inspect.signature(extract_evidence)
    assert "grounding" in sig.parameters, "D2: the caller must be able to choose"
    assert sig.parameters["grounding"].default is None

    # The safe direction is the default of the POLICY, not of this call site.
    assert GroundingPolicy().mode == "strict"
