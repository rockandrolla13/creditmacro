"""ThemeObject — the append-only, observable-anchored, frozen pipeline output."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .causal import Axis, CausalChain, CausalNode, Thesis, _chain_is_connected
from .expression import Expression
from .macro import MacroContext
from .pricing import Pricing, Scenario
from .probability import ProbabilitySetJustification
from .risk import PMGate, Provenance, Risk, Sizing
from .strategy_family import StrategyFamilyRec
from .streams import IcebergClassification
from .system_map import SystemMap
from .trap import BiasCritique, LoopDiagnosis, TrapImplications

class ThemeObject(BaseModel):
    """The output of the pipeline. Append-only, observable-anchored."""
    model_config = ConfigDict(frozen=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    statement: str     # Q1: one-sentence thesis
    horizon: str
    author: str
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    version: int = 1

    # Discovery firewall: lifecycle status + the discovery deliverable.
    status: Literal[
        "blocked", "discovery_complete", "strategy_family_routed", "expression_complete"
    ] = "strategy_family_routed"
    block_reason: Optional[str] = None               # set iff status=="blocked"
    strategy_families: list[StrategyFamilyRec] = []  # ranked; the discovery output

    thesis: Thesis                  # Engine 1
    axis: Optional[Axis] = None     # Engine 1 — absent on a blocked object (no fallback)
    # Detailed-expression half — present only for expression_complete objects.
    scenarios: list[Scenario] = []            # Engine 2
    pricing: Optional[Pricing] = None         # Engine 2
    # Q4 — provenance/evidence/confidence for scenario p_s (audit-only; never feeds pricing).
    probability_justification: Optional[ProbabilitySetJustification] = None
    expressions: list[Expression] = []        # Engine 3
    sizing: Optional[Sizing] = None           # Engine 4
    risk: Optional[Risk] = None               # Engine 4
    pm_gate: Optional[PMGate] = None          # Q13 — agent boundary
    provenance: Provenance

    # Causal Theme Compiler (optional; additive). main_theme.axis is the priced axis.
    # Other skill outputs map to EXISTING fields (no new ones): the standing credit-
    # risk-premium confounder → pricing.edge_basis ("gross_of_risk_premium");
    # assumptions + testable implications → risk.falsifiers;
    # non_identifiability → pm_gate.open_questions.
    main_theme: Optional[CausalNode] = None
    causal_chain: Optional[CausalChain] = None
    shared_factor: Optional[str] = None
    system_map: Optional[SystemMap] = None       # Meadows system structure (embeds the chain)
    bias_critique: Optional[BiasCritique] = None  # adversarial pre-promotion review
    loop_diagnosis: Optional[LoopDiagnosis] = None   # TRAP pre-pricing (feeds scenarios)
    trap_implications: Optional[TrapImplications] = None  # TRAP post-pricing (reads scenarios/exprs)
    # Stage 0: the iceberg classification of the candidate this theme was promoted from.
    iceberg_classification: Optional[IcebergClassification] = None
    # Discovery context classifier (additive, advisory). Qualitative macro-regime framing;
    # NOT priced, NOT a gate input. affected_strategy_families_hint is recorded only —
    # confidence influence is pending a follow-up PR.
    macro_context: Optional[MacroContext] = None

    def best_expression(self):
        """The highest-scored surviving expression, or None if none passed the gates."""
        scored = [e for e in self.expressions if e.score is not None]
        return max(scored, key=lambda e: e.score) if scored else None

    @model_validator(mode="after")
    def discipline_gates(self) -> "ThemeObject":
        """Status-dependent hard gates. Failure raises ValueError — the object is not"""
        if self.status == "blocked":
            # The HALT record is exempt from all gates; it only needs its reason.
            if not (self.block_reason and self.block_reason.strip()):
                raise ValueError(
                    "blocked ThemeObject must carry a block_reason (e.g. 'needs_causal_object')."
                )
            return self
        if self.status == "expression_complete":
            return self._expression_gates()
        # discovery_complete AND strategy_family_routed both run the discovery gates;
        # the family gate additionally guards the routed terminal state.
        return self._discovery_gates()

    def _expression_gates(self) -> "ThemeObject":
        """The original four EXPRESSION gates — apply to expression_complete objects."""
        # Gate 1: axis must be operational (named computable series)
        if self.axis is None or not self.axis.definition.strip() or not self.axis.measurement.strip():
            raise ValueError(
                "Gate 1 FAIL: axis.definition and axis.measurement must both be "
                "populated with a named, computable time series — not a label."
            )

        # Gate 2: residual_edge must be computed (pricing present + edge set)
        if self.pricing is None or self.pricing.residual_edge is None:
            raise ValueError(
                "Gate 2 FAIL: pricing.residual_edge is not computed. "
                "Run Engine 2 (max-entropy solver) before emitting."
            )

        # Gate 3: at least one expression survived all scoring gates
        scored = [e for e in self.expressions if e.score is not None]
        if not scored:
            raise ValueError(
                "Gate 3 FAIL: no expression survived the Omega / liquidity gates. "
                "Cannot emit a ThemeObject with zero viable expressions."
            )

        # Gate 4: at least one falsifier with observable + threshold
        if self.risk is None or not self.risk.falsifiers:
            raise ValueError(
                "Gate 4 FAIL: risk.falsifiers is empty. "
                "A thesis with no falsifier is not a thesis. Do not emit it."
            )
        for f in self.risk.falsifiers:
            if not f.observable.strip() or f.threshold is None:
                raise ValueError(
                    f"Gate 4 FAIL: falsifier '{f.kill_rule}' is missing "
                    "observable or threshold."
                )

        return self

    def _discovery_gates(self) -> "ThemeObject":
        """The DISCOVERY gates — apply to discovery_complete AND strategy_family_routed."""
        # D-Gate 1: a causal chain is present and connected (one component).
        if self.causal_chain is None or not self.causal_chain.nodes:
            raise ValueError(
                "Discovery Gate 1 FAIL: causal_chain is required (present + connected)."
            )
        if not _chain_is_connected(self.causal_chain):
            raise ValueError(
                "Discovery Gate 1 FAIL: causal_chain is not connected — every node must "
                "join one component via edges."
            )

        # D-Gate 2: the PROMOTED/routed theme (main_theme) terminates in an operational
        # axis. Non-promoted theme candidates may lack one (relaxed from per-node).
        mt = self.main_theme
        if mt is None or not mt.is_routable():
            raise ValueError(
                "Discovery Gate 2 FAIL: the routed theme (main_theme) must be a kind='theme' "
                "node carrying an operational axis. Non-promoted candidates may omit it."
            )
        for n in self.causal_chain.nodes:
            if n.promoted and not n.is_routable():
                raise ValueError(
                    f"Discovery Gate 2 FAIL: promoted theme node '{n.id}' lacks an operational axis."
                )

        # ── Promotion gates: bind only on the routed terminal state ──────────
        if self.status == "strategy_family_routed":
            # Promotion requires a falsifier (no falsifier ⇒ block promotion).
            if self.loop_diagnosis is None or not self.loop_diagnosis.invalidation_evidence:
                raise ValueError(
                    "Discovery Gate FAIL: promotion to strategy_family_routed requires ≥1 "
                    "falsifier from loop_diagnosis.invalidation_evidence."
                )
            # ≥1 ranked strategy family with a confidence (route to 'watchlist_only' if
            # nothing clears).
            if not self.strategy_families:
                raise ValueError(
                    "Discovery Gate FAIL: strategy_family_routed requires ≥1 ranked strategy "
                    "family (route to 'watchlist_only' if nothing clears)."
                )

        return self
