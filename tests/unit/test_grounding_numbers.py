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
