"""Mental-model/bias critic + the feedback/leverage/system-trap detector (Meadows)."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from .system_map import FeedbackLoop


# ── Mental Model & Bias Critic — adversarial pre-promotion review ─────────────

class BiasCritique(BaseModel):
    """Records the critic's reading of the thinking behind a theme."""
    dominant_mental_model: str
    alternative_models: list[str] = []
    assumptions_treated_as_facts: list[str] = []
    lenses_examined: list[str] = []
    disconfirming_evidence: list[str] = []
    decision: Literal["accept_model", "challenge_model", "reject_model"]
    rationale: str = ""


# ── Feedback, Leverage Point & System Trap Detector (Meadows) ─────────────────

class LeveragePoint(BaseModel):
    """Where a small change most alters system behaviour. observable=True if an
    investor can watch it; False if it is structural (a deeper Meadows leverage point)."""
    description: str
    observable: bool = True


class LoopDiagnosis(BaseModel):
    """PRE-PRICING half of the trap detector. CONSUMES the SystemMap's loop map (does not
    re-derive loops) and FEEDS propose_scenarios — the balancing limit / reversal point
    becomes a reversal scenario. Carries only what is knowable BEFORE pricing.

    Meadows: a reinforcing loop always eventually meets a balancing loop (limits to
    growth); delays in a balancing loop cause overshoot (crowded trades reverse
    violently); high attention × reinforcing-loop dominance ⇒ likely already priced."""
    feedback_loop_map: list[FeedbackLoop] = []   # reused from the SystemMap
    dominant_loop_now: str
    dominant_loop_evidence: str = ""
    possible_loop_shift: str                     # the R<->B reversal condition → a reversal scenario
    system_traps: list[str] = []
    leverage_points: list[LeveragePoint] = []
    early_warning_indicators: list[str] = []
    invalidation_evidence: list[str] = []        # → risk.falsifiers
    pm_questions: list[str] = []                  # → pm_gate.open_questions
    decision: Literal[
        "promote_to_scenario_pricing", "watchlist", "reject", "needs_more_data"
    ]


class TrapImplications(BaseModel):
    """POST-PRICING half. Needs the scenarios/pricing/expressions that only exist after
    pricing — so it CANNOT live in LoopDiagnosis (that was the backward dependency)."""
    scenario_implications: list[str] = []            # how each loop state maps to scenario FVs
    expression_risk_implications: list[str] = []     # which expression families break on reversal
