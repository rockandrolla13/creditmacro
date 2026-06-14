"""L4 — strategy-family hints are a typed vocabulary, not free strings.

Acceptance (plan §2 L4): ThemeCluster/ThemeClusterMember strategy_family_hints bind to the
discovery-family Literal; a hint outside the enum fails validation. curve/sector_rotation are
tagged wiki-only; ROUTABLE_FAMILIES stays in sync with what StrategyFamilyRec can emit.
"""
from __future__ import annotations

from typing import get_args

import pytest
from pydantic import ValidationError

from engine.schema.strategy_family import StrategyFamilyRec
from engine.schema.theme_aggregation import (
    ROUTABLE_FAMILIES,
    WIKI_ONLY_FAMILIES,
    StrategyFamilyName,
    ThemeClusterMember,
)


def test_valid_family_hint_accepted():
    m = ThemeClusterMember(source_slug="s", original_theme_name="t",
                           strategy_family_hints=["long_short", "etf_basket_rv", "relative_value"])
    assert m.strategy_family_hints == ["long_short", "etf_basket_rv", "relative_value"]


def test_garbage_family_hint_rejected():
    with pytest.raises(ValidationError):
        ThemeClusterMember(source_slug="s", original_theme_name="t",
                           strategy_family_hints=["made_up_family"])


def test_routable_families_match_strategy_family_rec_exactly():
    # the 12 routable hint values must equal exactly what the router can emit
    assert set(ROUTABLE_FAMILIES) == set(get_args(StrategyFamilyRec.model_fields["family"].annotation))
    assert len(ROUTABLE_FAMILIES) == 12


def test_wiki_only_families_are_not_routable():
    assert set(WIKI_ONLY_FAMILIES) == {"curve", "sector_rotation"}
    assert not (set(WIKI_ONLY_FAMILIES) & set(ROUTABLE_FAMILIES))


def test_vocabulary_is_routable_plus_wiki_only_plus_rv_parent():
    vocab = set(get_args(StrategyFamilyName))
    assert vocab == set(ROUTABLE_FAMILIES) | set(WIKI_ONLY_FAMILIES) | {"relative_value"}
    # curve/sector_rotation ARE in the discovery vocabulary (valid hints) but not routable
    assert {"curve", "sector_rotation"} <= vocab
