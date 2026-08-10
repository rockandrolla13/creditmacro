"""Numeric grounding helpers.

This module is intentionally standalone: it tokenizes numeric spans into the
frozen grounding schema without importing the rest of `engine.grounding`.
"""
from __future__ import annotations

import re

from engine.schema.grounding import Number

_NUMBER_BODY = r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|\.\d+"
_SIGNED_NUMBER = rf"[+-]?(?:{_NUMBER_BODY})"
_RANGE_DASH = r"(?:-|–)"
_SUFFIX_UNIT = r"(?:bp|%|x)"

_TOKEN_RE = re.compile(
    rf"""
    (?P<range>
        (?P<range_lower>{_SIGNED_NUMBER})
        \s*{_RANGE_DASH}\s*
        (?P<range_upper>{_SIGNED_NUMBER})
        (?P<range_unit>{_SUFFIX_UNIT})
    )
    |
    (?P<prefix>
        (?P<prefix_unit>\$)
        (?P<prefix_value>{_SIGNED_NUMBER})
    )
    |
    (?P<suffix>
        (?P<suffix_value>{_SIGNED_NUMBER})
        (?P<suffix_unit>{_SUFFIX_UNIT})
    )
    |
    (?P<bare>
        (?P<bare_value>{_SIGNED_NUMBER})
    )
    """,
    re.VERBOSE,
)

_BOUNDARY_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_")
_UNIT_NORMALIZATION = {"$": "usd", "bp": "bp", "%": "%", "x": "x"}


def _to_float(raw_number: str) -> float:
    return float(raw_number.replace(",", ""))


def _unit_or_none(raw_unit: str | None) -> str | None:
    if raw_unit is None:
        return None
    return _UNIT_NORMALIZATION[raw_unit]


def _is_embedded(text: str, start: int, end: int) -> bool:
    left_ok = start == 0 or text[start - 1] not in _BOUNDARY_CHARS
    right_ok = end == len(text) or text[end] not in _BOUNDARY_CHARS
    return not (left_ok and right_ok)


def numbers_in(text: str, base_offset: int = 0) -> list[Number]:
    """Return numeric tokens found in `text`.

    Tokens preserve the exact raw source span while exposing canonical values for
    comparison. Ranges remain one token with `value_upper` populated.

    `base_offset` is where `text` starts inside the document the offsets should refer
    to, and it exists because the natural way to use this function is the wrong way::

        start, end = index.find_span(quote)
        numbers_in(markdown[start:end])          # offsets relative to the SLICE

    `SourceIndex.find_span` speaks in document offsets, so a caller that reads
    `Number.char_start` from that result gets a position in the document where
    different text lives — provenance that points at the wrong words while looking
    perfectly well-formed. Passing `base_offset=start` makes the two agree::

        numbers_in(markdown[start:end], base_offset=start)

    The default of 0 is correct whenever `text` IS the whole document.
    """

    numbers: list[Number] = []
    for match in _TOKEN_RE.finditer(text):
        start, end = match.span()
        if _is_embedded(text, start, end):
            continue

        raw = text[start:end]
        if match.group("range") is not None:
            numbers.append(
                Number(
                    raw=raw,
                    value=_to_float(match.group("range_lower")),
                    value_upper=_to_float(match.group("range_upper")),
                    unit=_unit_or_none(match.group("range_unit")),
                    char_start=base_offset + start,
                    char_end=base_offset + end,
                )
            )
            continue

        if match.group("prefix") is not None:
            value = _to_float(match.group("prefix_value"))
            numbers.append(
                Number(
                    raw=raw,
                    value=value,
                    unit=_unit_or_none(match.group("prefix_unit")),
                    char_start=base_offset + start,
                    char_end=base_offset + end,
                )
            )
            continue

        if match.group("suffix") is not None:
            value = _to_float(match.group("suffix_value"))
            numbers.append(
                Number(
                    raw=raw,
                    value=value,
                    unit=_unit_or_none(match.group("suffix_unit")),
                    char_start=base_offset + start,
                    char_end=base_offset + end,
                )
            )
            continue

        value = _to_float(match.group("bare_value"))
        numbers.append(
            Number(
                raw=raw,
                value=value,
                unit=None,
                char_start=base_offset + start,
                char_end=base_offset + end,
            )
        )

    return numbers
