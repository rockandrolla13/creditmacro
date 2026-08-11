from engine.grounding.numbers import numbers_in


def test_numbers_in_recognizes_each_supported_unit() -> None:
    text = "Spread +25bp, margin 3.5%, price $125, leverage 12x."

    numbers = numbers_in(text)

    assert [n.raw for n in numbers] == ["+25bp", "3.5%", "$125", "12x"]
    assert [n.value for n in numbers] == [25.0, 3.5, 125.0, 12.0]
    assert [n.unit for n in numbers] == ["bp", "%", "usd", "x"]


def test_numbers_in_recognizes_ranges_with_en_dash() -> None:
    text = "Guidance moved to 120–140bp on the quarter."

    numbers = numbers_in(text)

    assert len(numbers) == 1
    token = numbers[0]
    assert token.raw == "120–140bp"
    assert token.value == 120.0
    assert token.value_upper == 140.0
    assert token.unit == "bp"
    assert token.is_range is True


def test_numbers_in_recognizes_thousands_separator() -> None:
    text = "Revenue reached 1,250 units."

    numbers = numbers_in(text)

    assert len(numbers) == 1
    assert numbers[0].raw == "1,250"
    assert numbers[0].value == 1250.0
    assert numbers[0].unit is None


def test_numbers_in_recognizes_negative_value() -> None:
    text = "The shock was -7.25% versus plan."

    numbers = numbers_in(text)

    assert len(numbers) == 1
    assert numbers[0].raw == "-7.25%"
    assert numbers[0].value == -7.25
    assert numbers[0].unit == "%"


def test_numbers_in_recognizes_bare_decimal() -> None:
    text = "Conviction improved to .75 after revisions."

    numbers = numbers_in(text)

    assert len(numbers) == 1
    assert numbers[0].raw == ".75"
    assert numbers[0].value == 0.75
    assert numbers[0].unit is None


def test_numbers_in_returns_empty_when_text_has_no_numbers() -> None:
    assert numbers_in("No numeric token is present here.") == []


# ── right-edge boundary guard (the magnitude / tenor allow-list) ──────────────
#
# The guard deletes a token whose end abuts a word character, because "Q1" and
# "Basel3" must not yield phantom figures. That also deleted every real figure
# carrying a magnitude or tenor suffix: "$440bn" and "3-5y" returned NOTHING.
# The fix is an allow-list, NOT a relaxed guard -- these two test groups are a
# pair, and loosening the guard to pass the first would break the second.

def test_magnitude_and_tenor_suffixes_are_recovered() -> None:
    """Figures the guard used to delete outright. Each returned [] before the fix."""
    cases = {
        "$1.2bn issuance":      ("$1.2bn", 1.2, "usd_bn"),
        "$440bn of supply":     ("$440bn", 440.0, "usd_bn"),
        "€270bn placed":        ("€270bn", 270.0, "eur_bn"),
        "a 500mn deal":         ("500mn", 500.0, "mn"),
        "a 250k position":      ("250k", 250.0, "k"),
        "the 10y point":        ("10y", 10.0, "y"),
        "rolling 3m returns":   ("3m", 3.0, "m"),
        "12M default rate":     ("12M", 12.0, "m"),
        "a 10year bond":        ("10year", 10.0, "year"),
    }
    for text, (raw, value, unit) in cases.items():
        found = numbers_in(text)
        assert len(found) == 1, f"{text!r} -> {[n.raw for n in found]}"
        assert (found[0].raw, found[0].value, found[0].unit) == (raw, value, unit), text


def test_tenor_ranges_stay_one_token() -> None:
    """'3-5y' is one range, not 3 and 5 -- the upper bound must survive."""
    (found,) = numbers_in("barbell 3-5y")
    assert (found.raw, found.value, found.value_upper, found.unit) == ("3-5y", 3.0, 5.0, "y")
    assert found.is_range

    (found,) = numbers_in("a 1-3Q horizon")
    assert (found.value, found.value_upper, found.unit) == (1.0, 3.0, "q")


def test_ordinals_decades_and_labels_are_still_dropped() -> None:
    """The other half of the pair. These are NOT quantities and must stay dropped.

    Measured over markdowns/, ordinals and decades are the COMMONEST cause of a
    right-edge drop -- far commoner than the magnitudes above. Admitting them to
    recover "$440bn" would trade one real bug for a larger one.
    """
    for text in ("the 13th Conference", "August 19th", "2nd February", "3rd party",
                 "1st place", "the early 1990s", "the 1980s", "Q1 growth",
                 "COVID-19 era", "Basel3 rules", "the 1970Q1 period"):
        assert numbers_in(text) == [], f"{text!r} produced a phantom figure"


def test_ambiguous_m_keeps_its_source_form_rather_than_guessing() -> None:
    """'$500m' is millions and '12m' is months; nothing in the token settles it.

    Both keep unit 'm' rather than inventing a meaning. This costs nothing for
    grounding, which matches on `value` (D6), and `raw` still shows what was written.
    """
    (millions,) = numbers_in("$500m raised")
    (months,) = numbers_in("over 12m")
    assert millions.value == 500.0 and months.value == 12.0
    assert millions.unit == "usd_m" and months.unit == "m"
