"""
ThemeObject schema — the append-only, observable-anchored record.

Split by subdomain (AR-BND-001) into a package; this `__init__` re-exports every public
name so existing `from engine.schema import X` imports are unchanged. Submodules:
  streams         — Stage-0 typed streams + Iceberg classifier
  causal          — Engine-1 thesis/axis + Causal Theme Compiler
  system_map      — Meadows system structure
  trap            — bias critic + feedback/leverage/trap detector
  pricing         — Engine-2 scenarios + max-entropy pricing
  expression      — Engine-3 trade expressions
  strategy_family — discovery deliverable (ranked families + confidence)
  risk            — Engine-4 sizing/risk, PM gate, provenance
  theme           — the assembled, frozen ThemeObject + discipline gates
"""
from __future__ import annotations

from .causal import (
    Axis,
    AxisHistory,
    CausalChain,
    CausalChainStep,
    CausalEdge,
    CausalNode,
    Driver,
    Thesis,
    _chain_is_connected,
)
from .expression import Expression, ScenarioPnL
from .pricing import EdgeContribution, PricedIn, Pricing, Scenario
from .risk import Falsifier, PMGate, Provenance, Risk, Sizing, StopLoss
from .strategy_family import ConfidenceComponents, StrategyFamilyRec
from .streams import (
    CandidateTheme,
    ConsensusSignal,
    IcebergClassification,
    IcebergScores,
    Observation,
)
from .system_map import Delay, FeedbackLoop, Flow, Stock, SystemMap
from .theme import ThemeObject
from .trap import BiasCritique, LeveragePoint, LoopDiagnosis, TrapImplications

__all__ = [
    # streams
    "Observation", "CandidateTheme", "ConsensusSignal", "IcebergScores", "IcebergClassification",
    # causal
    "Driver", "CausalChainStep", "Thesis", "AxisHistory", "Axis",
    "CausalNode", "CausalEdge", "CausalChain", "_chain_is_connected",
    # system_map
    "Stock", "Flow", "FeedbackLoop", "Delay", "SystemMap",
    # trap
    "BiasCritique", "LeveragePoint", "LoopDiagnosis", "TrapImplications",
    # pricing
    "Scenario", "PricedIn", "EdgeContribution", "Pricing",
    # expression
    "ScenarioPnL", "Expression",
    # strategy_family
    "ConfidenceComponents", "StrategyFamilyRec",
    # risk
    "Sizing", "StopLoss", "Falsifier", "Risk", "PMGate", "Provenance",
    # theme
    "ThemeObject",
]
