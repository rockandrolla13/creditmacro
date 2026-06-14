"""S8 / D3a — discovery-output persistence: a routed ThemeObject → durable CASE theme page.

Acceptance (plan §3.1): a routed ThemeObject round-trips to a CASE page carrying families +
ConfidenceComponents + axis + falsifier + snapshot_hash + forward_horizon; no legs/sizing; idempotent
re-write. Writes into a tmp wiki_root only.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

from engine.firewall import freeze
from engine.schema import ForwardHorizon
from engine.wiki_integration import (
    ThemeObjectPersistInput,
    persist_theme_object,
)
from tests._helpers import CASES_DIR, build_theme

JPM_DISCOVERY = CASES_DIR / "discovery" / "jpm_ai_capex.yaml"


def _routed():
    _, theme, _ = build_theme(JPM_DISCOVERY, mode="discovery")
    theme = theme.model_copy(update={"forward_horizon": ForwardHorizon(
        opened=date(2026, 1, 1), expected_close=date(2026, 4, 2),
        window_label="3m", window_days=91)})
    return theme, freeze(theme).content_hash


def _persist(tmp_path, **kw):
    theme, h = _routed()
    inp = ThemeObjectPersistInput(theme=theme, snapshot_hash=h,
                                  wiki_root=str(tmp_path / "wiki"), **kw)
    return inp, persist_theme_object(inp)


def test_dry_run_writes_nothing(tmp_path):
    inp, res = _persist(tmp_path, dry_run=True)
    assert res.applied is False
    assert res.plan.writes
    assert not list((Path(inp.wiki_root)).rglob("*.md"))


def test_routed_theme_round_trips_to_case_page(tmp_path):
    inp, res = _persist(tmp_path)
    assert res.applied and res.written_paths
    pages = list(Path(inp.wiki_root).glob("themes/routed-*.md"))
    assert len(pages) == 1
    body = pages[0].read_text()
    assert "access_class: case" in body
    assert "theme_kind: routed_discovery_theme" in body
    assert inp.snapshot_hash in body                       # snapshot binding
    assert "forward_horizon_window_days: 91" in body       # horizon
    assert "## Ranked strategy families" in body
    assert "## Operational axis" in body
    assert "## Falsifiers" in body
    assert "## No-trade boundary" in body
    # at least one routed family is rendered
    assert any(f.family in body for f in inp.theme.strategy_families)


def test_no_legs_or_sizing_in_page(tmp_path):
    inp, _ = _persist(tmp_path)
    body = Path(inp.wiki_root).glob("themes/routed-*.md").__next__().read_text().lower()
    body = body.replace("no trades, sizing, hedge ratios, or execution.", "")
    for bad in ("hedge ratio", "position size", "stop loss", "go long", "go short"):
        assert bad not in body


def test_idempotent_rewrite_skips(tmp_path):
    inp, _ = _persist(tmp_path)
    res2 = persist_theme_object(inp)
    assert res2.skipped_paths and not res2.written_paths   # identical content => skip


def test_confidence_components_rendered(tmp_path):
    inp, _ = _persist(tmp_path)
    body = Path(inp.wiki_root).glob("themes/routed-*.md").__next__().read_text()
    # the decomposed confidence is persisted, not just the scalar
    assert "causal" in body and "axis_fit" in body and "purity" in body
