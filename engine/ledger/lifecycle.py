"""Lifecycle transitions (ONTOLOGY §Lifecycle, AMEND A3). Phase-6 deliverable.

Governs the MARKET-TRUTH status axis only (A3). Emits STATUS_CHANGED events.
- CANDIDATE → ACTIVE   iff B_θ ≥ ACTIVATION_BREADTH_MIN ∧ |S_θ| ≥ ACTIVATION_ABS_SCORE_MIN
- ACTIVE → FALSIFIED   ONLY via surveillance Breach Buffer confirmation of F
                       (engine.surveillance_agent). Document contra-evidence
                       decrements S_θ (→ CONTESTED sub-state), never falsifies.
- ACTIVE → EXPIRED     at effective_at + H without HORIZON_EXTENDED.

Reuses engine.surveillance_agent (FalsifierState / ThemeMonitorAgent) as the
breach input — the ledger does not re-implement breach detection.
"""
from __future__ import annotations

from .ingest.scoring_view import ScoreView


def activation_transition(score: ScoreView) -> bool:
    """True iff the CANDIDATE→ACTIVE gate is met. Phase-6."""
    raise NotImplementedError("Phase 6 — B ≥ 2 ∧ |S| ≥ 2 → emit STATUS_CHANGED(ACTIVE)")


def falsified_from_breach(theme_id: str, breach) -> None:
    """Map a surveillance Breach-Buffer confirmation to a FALSIFIED STATUS_CHANGED."""
    raise NotImplementedError("Phase 6 — consumes engine.surveillance_agent breach")


def expiry_sweep(as_of: str) -> None:
    raise NotImplementedError("Phase 6 — ACTIVE→EXPIRED at effective_at+H")
