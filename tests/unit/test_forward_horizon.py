"""S7 (Phase 1, §3.2) — ForwardHorizon on ThemeObject.

The field is Optional with a safe default (None) and is EXCLUDED from the frozen content hash, so
FrozenSnapshot identity and the golden master are provably untouched by its presence or value.
"""
from __future__ import annotations

from datetime import date

from engine.firewall import freeze
from engine.schema import ForwardHorizon
from engine.schema.theme import ThemeObject
from engine.surveillance import ForwardHorizon as SurvForwardHorizon
from tests._helpers import CASES_DIR, build_theme

JPM_DISCOVERY = CASES_DIR / "discovery" / "jpm_ai_capex.yaml"


def _hz():
    return ForwardHorizon(opened=date(2026, 1, 1), expected_close=date(2026, 4, 2),
                          window_label="3m", window_days=91)


def test_field_present_and_defaults_none():
    assert "forward_horizon" in ThemeObject.model_fields
    _, theme, _ = build_theme(JPM_DISCOVERY, mode="discovery")
    assert theme.forward_horizon is None


def test_canonical_class_is_reexported_from_surveillance():
    assert ForwardHorizon is SurvForwardHorizon


def test_horizon_does_not_change_content_hash():
    _, theme, _ = build_theme(JPM_DISCOVERY, mode="discovery")
    stamped = theme.model_copy(update={"forward_horizon": _hz()})
    # the additive field is excluded from the hash → identity is unchanged
    assert freeze(theme).content_hash == freeze(stamped).content_hash


def test_two_horizons_same_hash():
    _, theme, _ = build_theme(JPM_DISCOVERY, mode="discovery")
    a = theme.model_copy(update={"forward_horizon": _hz()})
    b = theme.model_copy(update={"forward_horizon": ForwardHorizon(
        opened=date(2026, 2, 1), expected_close=date(2026, 8, 1),
        window_label="6m", window_days=181)})
    assert freeze(a).content_hash == freeze(b).content_hash   # horizon never alters identity
