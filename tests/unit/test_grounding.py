from __future__ import annotations

from engine.grounding import SourceIndex


def test_find_span_returns_exact_hit_offsets():
    source = "Alpha beta gamma."

    span = SourceIndex(source).find_span("beta")

    assert span == (6, 10)
    assert source[span[0]:span[1]] == "beta"


def test_find_span_normalizes_curly_quotes():
    source = 'The memo says “margin expansion” is the driver.'

    span = SourceIndex(source).find_span('"margin expansion"')

    assert span == (14, 32)
    assert source[span[0]:span[1]] == "“margin expansion”"


def test_find_span_collapses_whitespace_runs():
    source = "Alpha\t\tbeta\n\n gamma"

    span = SourceIndex(source).find_span("Alpha beta gamma")

    assert span == (0, len(source))
    assert source[span[0]:span[1]] == source


def test_find_span_normalizes_en_dash_to_ascii_dash():
    source = "Risk–on moves can reverse quickly."

    span = SourceIndex(source).find_span("Risk-on")

    assert span == (0, 7)
    assert source[span[0]:span[1]] == "Risk–on"


def test_find_span_returns_none_when_quote_is_absent():
    source = "Only exact or normalization-preserving matches count."

    assert SourceIndex(source).find_span("approximate match") is None
