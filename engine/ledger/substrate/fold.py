"""fold — the ONLY constructor of ThemeHypothesis (ONTOLOGY §Bitemporal, I5).

θ(t_x) = ⊕_{e : recorded_at ≤ t_x} e.payload

Requirements: deterministic; invariant under replay-order permutation among
equal-recorded_at events; total (every EventType has fold semantics).
Phase-1 deliverable — gate tests written first.
"""
from __future__ import annotations

from typing import Optional, Sequence

from .events import EventType, ThemeEvent
from .hypothesis import LifecycleStatus, Mechanism, ThemeHypothesis


def _canonical(events: Sequence[ThemeEvent]) -> list[ThemeEvent]:
    """Deterministic replay order: (recorded_at, event_id). Same-timestamp events
    fold to the same result regardless of input order (ONTOLOGY §Bitemporal)."""
    return sorted(events, key=lambda e: (e.recorded_at or "", e.event_id))


def fold(events: Sequence[ThemeEvent]) -> Optional[ThemeHypothesis]:
    """Reconstruct a theme from its event stream. None if no CREATED yet.

    Sole construction site for ThemeHypothesis (I5). All other modules obtain
    hypotheses via fold / queries, never by direct construction.
    """
    state: Optional[dict] = None
    count = 0
    for e in _canonical(events):
        p = e.payload
        if e.event_type == EventType.CREATED:
            state = {
                "theme_id": e.theme_id,
                "mechanism": Mechanism.model_validate(p["mechanism"]),
                "shock_direction": p["shock_direction"],
                "operational_axis": p["operational_axis"],
                "horizon_days": p["horizon_days"],
                "falsifier": p["falsifier"],
                "status": LifecycleStatus.CANDIDATE,
            }
        elif state is None:
            # a delta before any CREATED is not foldable into this theme
            continue
        elif e.event_type == EventType.MECHANISM_REVISED:
            state["mechanism"] = Mechanism.model_validate(p["mechanism"])
        elif e.event_type == EventType.AXIS_REVISED:
            state["operational_axis"] = p["operational_axis"]
        elif e.event_type == EventType.FALSIFIER_REVISED:
            state["falsifier"] = p["falsifier"]
        elif e.event_type == EventType.HORIZON_EXTENDED:
            state["horizon_days"] = p["horizon_days"]
        elif e.event_type == EventType.STATUS_CHANGED:
            state["status"] = LifecycleStatus(p["status"])
        elif e.event_type == EventType.MERGED_INTO:
            state["status"] = LifecycleStatus.MERGED
        elif e.event_type == EventType.RETIRED:
            state["status"] = LifecycleStatus.RETIRED
        count += 1

    if state is None:
        return None
    return ThemeHypothesis(**state, revision=count)
