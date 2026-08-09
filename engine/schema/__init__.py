"""ThemeObject schema — the append-only, observable-anchored record."""
from __future__ import annotations

from .source_classification import (
    AccessClassT,
    PageAccessT,
    PageClassification,
    SourceClassification,
    SourceTypeT,
)
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
from .horizon import ForwardHorizon
from .macro import MacroContext, MacroRegimeTag
from .pricing import EdgeContribution, PricedIn, Pricing, Scenario
from .probability import (
    EvidenceAtom,
    EvidenceClaimKind,
    EvidenceDirection,
    EvidenceImpactDirection,
    ProbabilityEvidenceBundle,
    ProbabilityEvidenceRef,
    ProbabilitySetJustification,
    ProbabilitySource,
    ProbabilityUpdateAudit,
    ProbabilityUpdateMethod,
    ScenarioEvidenceImpact,
    ScenarioEvidenceMap,
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
from .theme_aggregation import (
    EvidenceBullet,
    MultiSourceThemeSet,
    SourceAttribution,
    ThemeCluster,
    ThemeClusterMember,
)
from .thesis_tracker import (
    ComputedThesisTrackerRecord,
    MarketDataRecord,
    ThesisTrackerRecord,
)
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
    # Q4 evidence-to-posterior bridge (PART 1 schema + PART 2 mapper input)
    "EvidenceImpactDirection", "EvidenceClaimKind", "ProbabilityUpdateMethod",
    "EvidenceAtom", "ScenarioEvidenceImpact", "ScenarioEvidenceMap", "ProbabilityUpdateAudit",
    # expression
    "ScenarioPnL", "Expression",
    # strategy_family
    "ConfidenceComponents", "StrategyFamilyRec",
    # risk
    "Sizing", "StopLoss", "Falsifier", "Risk", "PMGate", "Provenance",
    # macro context (discovery context classifier)
    "MacroContext", "MacroRegimeTag",
    # theme
    "ThemeObject", "ForwardHorizon",
    # thesis tracker (standalone persistence sidecar — not wired into discovery/firewall)
    "MarketDataRecord", "ThesisTrackerRecord", "ComputedThesisTrackerRecord",
    # Stage-0 multi-source theme aggregator
    "SourceAttribution", "EvidenceBullet", "ThemeClusterMember", "ThemeCluster",
    "MultiSourceThemeSet",
]
