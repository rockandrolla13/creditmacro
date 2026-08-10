"""Do the two halves of the grounding kernel actually compose?

`engine/grounding/__init__.py` (span matching) and `engine/grounding/numbers.py`
(numeric tokenizing) were written in parallel, in separate worktrees, by agents that
never saw each other's code. They share only the frozen contract in
`engine/schema/grounding.py`. They merged without conflict — which proves they do not
collide, not that they agree.

These tests run against a REAL file from `markdowns/`, not a fixture, because the
corpus is PDF-derived and carries the whitespace, table reflow and unicode punctuation
that a hand-written fixture would quietly omit.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from engine.grounding import SourceIndex
from engine.grounding.numbers import numbers_in

_CORPUS = Path(__file__).resolve().parents[2] / "markdowns"
_SOURCE = _CORPUS / "Alaph Long Presentation Version July 2014.md"
_OTHER = _CORPUS / "XantimumBizPlan.md"

pytestmark = pytest.mark.skipif(
    not _SOURCE.exists() or not _OTHER.exists(),
    reason="research corpus not present",
)


@pytest.fixture(scope="module")
def markdown() -> str:
    return _SOURCE.read_text(errors="replace")


@pytest.fixture(scope="module")
def index(markdown: str) -> SourceIndex:
    return SourceIndex(markdown)


def _numeric_line(markdown: str) -> str:
    """A real line from the source that carries at least one number."""
    for line in markdown.splitlines():
        stripped = line.strip()
        if len(stripped) > 40 and re.search(r"\d", stripped):
            return stripped
    pytest.skip("no numeric line in source")


def test_real_quote_grounds_and_slices_back_identically(index, markdown):
    quote = _numeric_line(markdown)
    span = index.find_span(quote)
    assert span is not None, "a verbatim line from the source must ground"
    assert markdown[span[0]:span[1]] == quote


def test_numbers_recovered_from_a_grounded_span_are_really_there(index, markdown):
    quote = _numeric_line(markdown)
    start, end = index.find_span(quote)
    for number in numbers_in(markdown[start:end]):
        assert number.raw in quote, f"{number.raw!r} reported but absent from the span"


def test_number_offsets_point_at_the_document_when_given_a_base(index, markdown):
    """The two halves speak the same offset language, but only if you say so.

    `find_span` returns document offsets. `numbers_in` returns offsets into the string
    it was handed, so tokenizing a span slice and reading `Number.char_start` as a
    document position used to land on unrelated text — provenance pointing at the wrong
    words while looking perfectly well-formed. `base_offset` rebases them, and this test
    slices the document at the reported offsets to prove it.
    """
    quote = _numeric_line(markdown)
    start, end = index.find_span(quote)
    numbers = [
        n for n in numbers_in(markdown[start:end], base_offset=start)
        if n.char_start is not None
    ]
    if not numbers:
        pytest.skip("no offset-bearing numbers in the chosen span")

    for number in numbers:
        assert markdown[number.char_start:number.char_end] == number.raw


def test_every_token_kind_is_rebased_not_just_some(markdown):
    """Each branch of the tokenizer stamps offsets separately, so each is checked.

    Ranges, prefix units, suffix units and bare numbers are four distinct construction
    sites. Rebasing three of them and missing the fourth would pass any test that only
    exercised the common case.
    """
    text = "spreads 120-140bp on $1,250 of notional at 3.5x versus 75 last week"
    document = "PREAMBLE. " + text
    base = document.index(text)

    tokens = numbers_in(text, base_offset=base)
    assert {t.unit for t in tokens} >= {"bp", "usd", "x", None}, "not all kinds exercised"
    for token in tokens:
        assert document[token.char_start:token.char_end] == token.raw


def test_default_base_offset_is_unchanged_for_whole_document_callers(markdown):
    """The default must stay correct for anyone passing the entire document."""
    tokens = numbers_in(markdown)[:20]
    for token in tokens:
        assert markdown[token.char_start:token.char_end] == token.raw


def test_a_paraphrase_of_a_real_sentence_does_not_ground(index, markdown):
    quote = _numeric_line(markdown)
    paraphrase = " ".join(quote.split()[:4]) + " and then something never written here"
    assert index.find_span(paraphrase) is None, "a near-match is not grounding"


def test_a_verbatim_quote_from_a_different_source_does_not_ground(index):
    other = _OTHER.read_text(errors="replace")
    foreign = next(
        line.strip() for line in other.splitlines()
        if len(line.strip()) > 50 and line.strip().isprintable()
    )
    assert index.find_span(foreign) is None


def test_whitespace_inflated_quote_grounds_and_maps_back_to_the_original(index, markdown):
    """Tier B: the normalized match must return RAW offsets, not normalized ones."""
    quote = _numeric_line(markdown)
    span = index.find_span(quote.replace(" ", "   "))
    assert span is not None, "whitespace variation must still ground (tier B)"
    assert markdown[span[0]:span[1]] == quote


def test_a_number_absent_from_the_span_is_never_reported(index, markdown):
    quote = _numeric_line(markdown)
    start, end = index.find_span(quote)
    reported = {n.value for n in numbers_in(markdown[start:end])}
    assert 999_999_777.0 not in reported
