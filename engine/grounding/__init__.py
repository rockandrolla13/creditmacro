"""Dependency-free grounding kernel for locating verbatim source spans.

One definition of "is this text in the source", used by every producer of claims.
Pure and deterministic: no LLM, no I/O, no wall clock.

`verify_atom` and `enforce` are the harness half. They take a claim that already
carries a quote and decide whether that quote exists — the producer never grades
its own citation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Optional, Sequence

from engine.schema.grounding import GroundingVerdict

from .numbers import numbers_in

_FOLDED_CHARS = str.maketrans(
    {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
    }
)


class SourceIndex:
    """Locate verbatim and normalization-preserving spans in source markdown."""

    def __init__(self, markdown: str) -> None:
        self.markdown = markdown
        self._normalized_text, self._normalized_spans = _normalize_with_spans(markdown)

    def find_span(self, quote: str) -> Optional[tuple[int, int]]:
        if not quote:
            return None

        exact_start = self.markdown.find(quote)
        if exact_start != -1:
            return (exact_start, exact_start + len(quote))

        normalized_quote, _ = _normalize_with_spans(quote)
        if not normalized_quote:
            return None

        normalized_start = self._normalized_text.find(normalized_quote)
        if normalized_start == -1:
            return None

        normalized_end = normalized_start + len(normalized_quote) - 1
        start = self._normalized_spans[normalized_start][0]
        end = self._normalized_spans[normalized_end][1]
        return (start, end)


def _normalize_with_spans(text: str) -> tuple[str, list[tuple[int, int]]]:
    chars: list[str] = []
    spans: list[tuple[int, int]] = []
    whitespace_start: Optional[int] = None

    for index, char in enumerate(text):
        folded = char.translate(_FOLDED_CHARS)
        if folded.isspace():
            if whitespace_start is None:
                whitespace_start = index
            continue

        if whitespace_start is not None:
            chars.append(" ")
            spans.append((whitespace_start, index))
            whitespace_start = None

        chars.append(folded)
        spans.append((index, index + 1))

    if whitespace_start is not None:
        chars.append(" ")
        spans.append((whitespace_start, len(text)))

    return ("".join(chars), spans)


#: D2 — what an ungrounded claim costs. `strict` is the real product path: an
#: ungrounded claim halts rather than vanishing, because a silent drop is how evidence
#: goes missing without anyone deciding it should. `lint` is for bulk wiki passes, where
#: a run that stops on the first bad quote never finishes. Default is strict; lint must
#: be asked for by name.
GroundingMode = Literal["strict", "lint"]


@dataclass(frozen=True)
class GroundingPolicy:
    mode: GroundingMode = "strict"
    #: When False, a claim grounds on its span alone and its numbers are not checked.
    #: Useful while a producer's number parser and `numbers_in` still disagree.
    verify_numbers: bool = True


@dataclass
class EnforcedBundle:
    """The partition. `rejected` carries every claim and the reason it failed, so a
    rejection is always explicable to the human who has to act on it."""

    kept: list[Any] = field(default_factory=list)
    rejected: list[tuple[Any, GroundingVerdict]] = field(default_factory=list)

    @property
    def warnings(self) -> list[str]:
        return [f"ungrounded_evidence:{getattr(a, 'evidence_id', None)}: {v.reason}"
                for a, v in self.rejected]


class UngroundedEvidenceError(RuntimeError):
    """Raised in strict mode. Blocked beats plausible."""


def verify_atom(atom: Any, index: SourceIndex,
                policy: GroundingPolicy = GroundingPolicy()) -> GroundingVerdict:
    """Decide whether `atom`'s quote is really in the source.

    Three outcomes, and the difference between the last two matters: `unverifiable`
    means the check could not run (no quote was offered), `ungrounded` means it ran and
    the text is not there. Collapsing them would let a producer that forgot to quote
    read as a clean rejection.
    """
    quote = getattr(atom, "source_span", None)
    if not quote:
        return GroundingVerdict(
            status="unverifiable", method="none", span_found=False,
            numbers_verified=False, reason="no source_span supplied",
        )

    span = index.find_span(quote)
    if span is None:
        return GroundingVerdict(
            status="ungrounded", method="none", span_found=False,
            numbers_verified=False,
            reason=f"quote not found in source ({len(quote)} chars)",
        )

    start, end = span
    method = "exact" if index.markdown[start:end] == quote else "normalized"
    found = numbers_in(index.markdown[start:end], base_offset=start)

    if not policy.verify_numbers:
        return GroundingVerdict(
            status="grounded", method=method, span_found=True, numbers_verified=False,
            reason="span located; numbers not checked by policy",
            span_char_start=start, span_char_end=end, verified_numbers=tuple(found),
        )

    claimed = list(getattr(atom, "numbers", []) or [])
    available = {n.value for n in found} | {n.value_upper for n in found if n.is_range}
    missing = [c for c in claimed if c not in available]
    if missing:
        return GroundingVerdict(
            status="ungrounded", method=method, span_found=True, numbers_verified=False,
            reason=f"numbers absent from span: {missing[:5]}",
            span_char_start=start, span_char_end=end, verified_numbers=tuple(found),
        )

    return GroundingVerdict(
        status="grounded", method=method, span_found=True, numbers_verified=True,
        reason="span located and every claimed number found in it",
        span_char_start=start, span_char_end=end, verified_numbers=tuple(found),
    )


def enforce(atoms: Sequence[Any], index: SourceIndex,
            policy: GroundingPolicy = GroundingPolicy()) -> EnforcedBundle:
    """Partition claims into kept and rejected, stamping each kept one with its verdict.

    Atoms are frozen, so a stamped atom is a new object — `model_copy` if the claim is a
    pydantic model, otherwise passed through unchanged.
    """
    bundle = EnforcedBundle()
    for atom in atoms:
        verdict = verify_atom(atom, index, policy)
        if not verdict.is_grounded:
            bundle.rejected.append((atom, verdict))
            continue
        copier = getattr(atom, "model_copy", None)
        bundle.kept.append(copier(update={
            "grounding": verdict,
            "span_char_start": verdict.span_char_start,
            "span_char_end": verdict.span_char_end,
        }) if copier else atom)

    if bundle.rejected and policy.mode == "strict":
        raise UngroundedEvidenceError(
            f"{len(bundle.rejected)} ungrounded claim(s); "
            f"first: {bundle.warnings[0]}"
        )
    return bundle


__all__ = [
    "EnforcedBundle", "GroundingMode", "GroundingPolicy", "GroundingVerdict",
    "SourceIndex", "UngroundedEvidenceError", "enforce", "verify_atom",
]
