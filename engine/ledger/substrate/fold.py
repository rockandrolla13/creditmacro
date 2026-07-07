"""fold — the ONLY constructor of ThemeHypothesis (ONTOLOGY §Bitemporal, I5).

θ(t_x) = ⊕_{e : recorded_at ≤ t_x} e.payload

Requirements: deterministic; invariant under replay-order permutation among
equal-recorded_at events; total (every EventType has fold semantics).
Phase-1 deliverable — gate tests written first.
"""
from __future__ import annotations

from typing import Optional, Sequence

from .events import ThemeEvent
from .hypothesis import ThemeHypothesis


def fold(events: Sequence[ThemeEvent]) -> Optional[ThemeHypothesis]:
    """Reconstruct a theme from its ordered event stream. None if no CREATED yet.

    This is the sole construction site for ThemeHypothesis (I5). All other
    modules obtain hypotheses via fold / queries, never by direct construction.
    """
    raise NotImplementedError(
        "Phase 1 — gates: test_as_of_exact_states, test_fold_order_invariance"
    )
