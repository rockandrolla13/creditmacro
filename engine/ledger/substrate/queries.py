"""Bitemporal queries over the event log (ONTOLOGY §Bitemporal). Phase-1.

as_of     — Θ(t_x): themes recorded ≤ t_x (backtest, no lookahead)
valid_over— Θ_v(t): themes whose [effective_at, effective_at+H] contains t
revision  — number of events folded at t_x
"""
from __future__ import annotations

from collections import defaultdict
from typing import Optional

from .store import EventStore
from .fold import fold
from .hypothesis import LifecycleStatus, ThemeHypothesis

# Themes in these states have left the active registry (superseded, §Bitemporal).
_INACTIVE = (LifecycleStatus.RETIRED, LifecycleStatus.MERGED)


def as_of(store: EventStore, t_x: str) -> list[ThemeHypothesis]:
    """Θ(t_x): active themes folded from events recorded ≤ t_x (no lookahead).

    Sorted by theme_id for deterministic, byte-stable output.
    """
    by_theme: dict[str, list] = defaultdict(list)
    for e in store.events_as_of(t_x):
        by_theme[e.theme_id].append(e)
    out: list[ThemeHypothesis] = []
    for theme_id in sorted(by_theme):
        theme = fold(by_theme[theme_id])
        if theme is not None and theme.status not in _INACTIVE:
            out.append(theme)
    return out


def valid_over(store: EventStore, t: str) -> list[ThemeHypothesis]:
    raise NotImplementedError("Phase 6 — outcome-attribution query (valid-time window)")


def revision(store: EventStore, theme_id: str, *, t_x: Optional[str] = None) -> int:
    """revision(θ, t_x): number of events folded (bound by EvidenceLink at mapping)."""
    theme = fold(store.events_for(theme_id, up_to=t_x))
    return theme.revision if theme is not None else 0
