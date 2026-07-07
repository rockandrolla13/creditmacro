"""Bitemporal queries over the event log (ONTOLOGY §Bitemporal). Phase-1.

as_of     — Θ(t_x): themes recorded ≤ t_x (backtest, no lookahead)
valid_over— Θ_v(t): themes whose [effective_at, effective_at+H] contains t
revision  — number of events folded at t_x
"""
from __future__ import annotations

from typing import Optional

from .store import EventStore
from .hypothesis import ThemeHypothesis


def as_of(store: EventStore, t_x: str) -> list[ThemeHypothesis]:
    raise NotImplementedError("Phase 1 — gate: test_as_of_exact_states")


def valid_over(store: EventStore, t: str) -> list[ThemeHypothesis]:
    raise NotImplementedError("Phase 1 — outcome-attribution query")


def revision(store: EventStore, theme_id: str, *, t_x: Optional[str] = None) -> int:
    raise NotImplementedError("Phase 1 — fold count bound to EvidenceLink at mapping time")
