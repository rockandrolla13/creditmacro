"""The theme lifecycle layer — `PLAN-theme-lifecycle.md` §3 (A1/A2) and §4 (L1–L5).

SCAFFOLD ONLY. Every model here is real and frozen; every function raises `NotImplementedError`
naming its phase. Nothing in this package is wired into the engine yet, so no existing module
gains a dependency and the golden master is untouched.

Where the pieces sit relative to what already exists:

    grounded atoms ──→ A1 regime.discover_regimes ──→ RegimeVocabulary
                                                            │
    MultiSourceThemeSet ─→ compression.compress_theme_set ─→ AnalystThemeMap   (ALREADY BUILT)
                                                            │
                                    A2 theme_enrichment.enrich (adds only what compression lacks)
                                                            │
    ThemeObject + ThemeWatch ──→ L1 theme_view.project ──→ ThemeView
                                                            ├─→ L3 evidence_pack ─→ scorecard
                                                            ├─→ L4 theme_book
                                                            └─→ L5 expression_gate (status only)

`engine/lifecycle/` is NOT `engine/ledger/lifecycle.py`. That module holds the ledger's own
activation and falsification transitions; this package holds the theme lifecycle — assessment,
projection, packs, the weekly book and the expression gate.

Discovery discipline throughout: no trades, no legs, no sizing, no hedge ratios. No wall clock
— `as_of` and `now` are always parameters (I8).
"""
from __future__ import annotations

from . import (
    decisions,
    evidence_pack,
    factor_projection,
    regime,
    scorecard,
    surprise,
    theme_book,
    theme_enrichment,
    theme_view,
)
from .decisions import LIFECYCLE_DECISIONS_VERSION
from .theme_view import THEME_VIEW_CONTRACT, ThemeView, project, require_contract

__all__ = [
    "LIFECYCLE_DECISIONS_VERSION",
    "THEME_VIEW_CONTRACT",
    "ThemeView",
    "decisions",
    "evidence_pack",
    "factor_projection",
    "project",
    "regime",
    "require_contract",
    "scorecard",
    "surprise",
    "theme_book",
    "theme_enrichment",
    "theme_view",
]
