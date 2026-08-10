"""Identity, merge, and well-formedness (ONTOLOGY §Identity, §WF, §Event, F2).

Pure helpers (equiv, jaccard) are implemented — they are trivial and load-bearing
for the CI/gate tests. The composite decision functions (wf_predicate,
classify_event) are Phase-1 stubs: their gate tests are written first
(BUILD_PROMPT session rules).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .. import vocab
from ..constants import H_MAX
from .hypothesis import Mechanism, ThemeHypothesis, ThemeShape, derived_direction
from .events import EventType


def _edge_set(m: Mechanism) -> frozenset[tuple[str, str, int]]:
    return frozenset((e.v_from, e.v_to, e.sign) for e in m.edges)


def jaccard_edges(m1: Mechanism, m2: Mechanism) -> float:
    """J(E1,E2) = |E1 ∩ E2| / |E1 ∪ E2| over typed signed edges (§Identity c.1)."""
    e1, e2 = _edge_set(m1), _edge_set(m2)
    if not e1 and not e2:
        return 1.0
    union = e1 | e2
    return len(e1 & e2) / len(union) if union else 0.0


def equiv(m1: Mechanism, m2: Mechanism) -> bool:
    """M1 ≅ M2: same endpoints, same sign product, intersecting intermediates."""
    if (m1.v0, m1.vk) != (m2.v0, m2.vk):
        return False
    if m1.sign_product() != m2.sign_product():
        return False
    i1, i2 = set(m1.intermediate_nodes()), set(m2.intermediate_nodes())
    if not i1 and not i2:
        return True
    return bool(i1 & i2)


@dataclass(frozen=True)
class WFResult:
    ok: bool
    failing_clause: Optional[str] = None    # 'a'..'e' when ok is False
    detail: str = ""


def wf_predicate(theme: ThemeShape, *, stated_direction: Optional[int] = None) -> WFResult:
    """WF(θ) per ONTOLOGY §WF, returning the first failing clause.

    Clause (b) decidability is a Phase-1 proxy (non-empty falsifier); a full
    predicate-parse against the tracked-axis feeds lands with surveillance.
    """
    if theme.mechanism.k < 2:
        return WFResult(False, "a", "chain has no intermediate node (k < 2)")
    if not theme.falsifier.strip():
        return WFResult(False, "b", "falsifier empty / not decidable")
    if not vocab.is_tracked_axis(theme.operational_axis):
        return WFResult(False, "c", f"axis {theme.operational_axis!r} not in tracked-axis registry")
    if theme.horizon_days > H_MAX.days:
        return WFResult(False, "d", f"horizon {theme.horizon_days}d > H_MAX {H_MAX.days}d")
    if stated_direction is not None and stated_direction != derived_direction(theme):
        return WFResult(False, "e", "stated direction != σ·Πs")
    return WFResult(True)


def classify_event(current: ThemeHypothesis, successor: ThemeHypothesis) -> tuple[EventType, ...]:
    """Event-type decision (§Event semantics + F2 tie-break), as an ordered tuple.

    Identity change (σ flip or M' ≇ M) → (RETIRED, CREATED). Otherwise the
    successor is a revision of the SAME matched theme (F2): emit one revision
    event per changed attribute. () means no change.
    """
    if successor.shock_direction != current.shock_direction or not equiv(
        successor.mechanism, current.mechanism
    ):
        return (EventType.RETIRED, EventType.CREATED)

    events: list[EventType] = []
    if successor.mechanism != current.mechanism:          # ≅ but not identical → refinement
        events.append(EventType.MECHANISM_REVISED)
    if successor.operational_axis != current.operational_axis:
        events.append(EventType.AXIS_REVISED)
    if successor.horizon_days != current.horizon_days:
        events.append(EventType.HORIZON_EXTENDED)
    if successor.falsifier != current.falsifier:
        events.append(EventType.FALSIFIER_REVISED)
    return tuple(events)
