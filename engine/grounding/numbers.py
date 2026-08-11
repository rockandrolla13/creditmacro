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
# `bps` must precede `bp`: the alternation is first-match, so the shorter form would
# otherwise win and leave a trailing "s" that the embedded-token guard reads as a word
# character, silently discarding the whole number. "40bps" is at least as common as
# "40bp" in credit research, so that failure hides a lot of real figures.
_SUFFIX_UNIT = r"(?:bps|bp|%|x)"

# Magnitude and tenor suffixes. These exist because of the RIGHT-edge guard below:
# an unconsumed trailing letter reads as "embedded" and silently deletes the whole
# token, so "$440bn" and "3-5y" returned nothing at all. Consuming the suffix as a
# unit is what makes the figure survive.
#
# This is deliberately an ALLOW-LIST and not a relaxation of the guard. Measured over
# markdowns/, the commonest trailing letters are `th`, `nd`, `rd`, `st` and `s` --
# "the 13th Conference", "August 19th", "2nd February", "the early 1990s". Those are
# ordinals and decades, not quantities, and dropping them is correct. Admitting them
# would reintroduce exactly the phantom figures the guard was added to stop.
#
# Longest-first: the alternation is first-match, so `bn` must precede `b` and
# `year`/`yr` must precede `y`, or the shorter form wins and leaves a trailing letter
# that the guard reads as a word character -- the original failure, moved one letter to
# the right.
_MAGNITUDE_TENOR = (
    r"(?i:months?|years?|qtrs?|yrs?|trn|tn|bn|mn|mm|[bmkt]|[ywdq])"
)
_SUFFIX_UNIT_EXT = rf"(?:{_SUFFIX_UNIT}|{_MAGNITUDE_TENOR})"

_TOKEN_RE = re.compile(
    rf"""
    (?P<range>
        (?P<range_lower>{_SIGNED_NUMBER})
        \s*{_RANGE_DASH}\s*
        (?P<range_upper>{_SIGNED_NUMBER})
        (?P<range_unit>{_SUFFIX_UNIT_EXT})
    )
    |
    (?P<prefix>
        (?P<prefix_unit>[$€£])
        (?P<prefix_value>{_SIGNED_NUMBER})
        (?P<prefix_scale>{_MAGNITUDE_TENOR})?
    )
    |
    (?P<suffix>
        (?P<suffix_value>{_SIGNED_NUMBER})
        (?P<suffix_unit>{_SUFFIX_UNIT_EXT})
    )
    |
    (?P<bare>
        (?P<bare_value>{_SIGNED_NUMBER})
    )
    """,
    re.VERBOSE,
)

_BOUNDARY_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_")
_UNIT_NORMALIZATION = {"$": "usd", "€": "eur", "£": "gbp",
                       "bps": "bp", "bp": "bp", "%": "%", "x": "x"}


def _normalize_unit(raw_unit: str) -> str:
    """Canonical unit label. Unknown suffixes keep their lowercased source form.

    `m` is genuinely ambiguous -- "$500m" is millions, "12m" is months -- and nothing
    in the token can settle it. Guessing would put a fabricated meaning on a verified
    figure, so it is left as written. This costs nothing for grounding: D6 matches on
    `value`, which is 500 or 12 either way, and `raw` still shows the human exactly
    what the page said.
    """
    return _UNIT_NORMALIZATION.get(raw_unit, raw_unit.lower())


def _to_float(raw_number: str) -> float:
    return float(raw_number.replace(",", ""))


def _unit_or_none(raw_unit: str | None) -> str | None:
    if raw_unit is None:
        return None
    return _normalize_unit(raw_unit)


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
            # "$440bn" carries two unit facts: the currency and the scale. Joining them
            # ("usd_bn") keeps both without scaling `value`, which D6 requires to stay
            # the mantissa as written ("75bp" -> 75.0, not 0.0075).
            currency = _unit_or_none(match.group("prefix_unit"))
            scale = match.group("prefix_scale")
            unit = f"{currency}_{_normalize_unit(scale)}" if scale else currency
            numbers.append(
                Number(
                    raw=raw,
                    value=value,
                    unit=unit,
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
