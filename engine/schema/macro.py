"""MacroContext — a METHOD-only discovery CONTEXT CLASSIFIER.

This is NOT a macro regime model, scenario generator, probability engine, or trade
generator. It carries QUALITATIVE regime/bias tags that frame a discovery input — never
state probabilities, fair values, sizing, or legs. When the input lacks macro information
the classifier MUST set macro_regime_tags=["unclear"] and populate missing_data rather than
fabricate a regime.

affected_strategy_families_hint is ADVISORY ONLY: it may influence family confidence in a
LATER PR (the confidence-influence wiring is deliberately deferred), but it cannot create a
trade.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

# Qualitative regime tags (a joint state of growth / inflation / policy / liquidity / credit).
MacroRegimeTag = Literal[
    "recovery", "expansion", "contraction", "recession",
    "inflationary_growth", "stagflation", "disinflationary_slowdown",
    "liquidity_stress", "policy_easing", "policy_tightening", "fiscal_expansion",
    "credit_cycle_early", "credit_cycle_late",
    "risk_on", "risk_off", "unclear",
]


class MacroContext(BaseModel):
    """Qualitative macro-regime framing for a discovery input. Tags, NOT probabilities."""

    input_kind: Literal[
        "idea", "current_report", "macro_note", "theme_taxonomy", "case_replay"
    ]
    # Qualitative regime tags — never state probabilities. Missing info -> ["unclear"].
    macro_regime_tags: list[MacroRegimeTag]
    growth_bias: Literal["positive", "negative", "mixed", "unclear"]
    inflation_bias: Literal["higher", "lower", "mixed", "unclear"]
    policy_bias: Literal["easing", "tightening", "mixed", "unclear"]
    liquidity_bias: Literal["improving", "deteriorating", "mixed", "unclear"]
    credit_cycle_bias: Literal[
        "repair", "recovery", "expansion", "contraction", "stress", "unclear"
    ]
    horizon: Literal["intraday", "1-5d", "1w-3m", "3-12m", "secular", "unclear"]
    affected_asset_classes: list[str] = []
    # ADVISORY ONLY — recorded, never auto-routed to a trade (confidence wiring pending).
    affected_strategy_families_hint: list[str] = []
    confidence: float = 0.0
    evidence_refs: list[str] = []
    missing_data: list[str] = []
    rationale: str = ""
    warnings: list[str] = []
