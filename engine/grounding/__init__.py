"""Dependency-free grounding kernel for locating verbatim source spans."""
from __future__ import annotations

from typing import Optional

from engine.schema.grounding import GroundingVerdict

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


__all__ = ["GroundingVerdict", "SourceIndex"]
