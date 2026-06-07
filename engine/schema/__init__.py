"""ThemeObject schema — the append-only, observable-anchored record."""
from __future__ import annotations

from .causal import (
    Axis,
    AxisCandidate,
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
from .probability import (
    EvidenceDirection,
    ProbabilityEvidenceBundle,
    ProbabilityEvidenceRef,
    ProbabilitySetJustification,
    ProbabilitySource,
    ScenarioProbabilityJustification,
)
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
    # probability (Q4)
    "ProbabilitySource", "EvidenceDirection", "ProbabilityEvidenceRef",
    "ScenarioProbabilityJustification", "ProbabilitySetJustification",
    "ProbabilityEvidenceBundle",
    # expression
    "ScenarioPnL", "Expression",
    # strategy_family
    "ConfidenceComponents", "StrategyFamilyRec",
    # risk
    "Sizing", "StopLoss", "Falsifier", "Risk", "PMGate", "Provenance",
    # theme
    "ThemeObject",
]
