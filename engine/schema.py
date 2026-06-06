"""
ThemeObject schema — the append-only, observable-anchored record.

Every field maps to one of Q1–Q13. Every claim carries an observable.
The four discipline gates are enforced by model_validator: no incomplete
object is ever emitted.

Stage 0 typed streams (Observation, CandidateTheme, ConsensusSignal)
are also defined here — they are the input to the pipeline, not the output.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator


# ── Stage 0 typed streams ─────────────────────────────────────────────────────

class Observation(BaseModel):
    """
    Dated, sourced fact.
    Type: developments / events from research notes.
    Downstream: updates Driver.current_level; triggers rescoring.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    date: str                    # ISO date of the observation
    source: str                  # e.g. "Citi credit weekly 2024-11-08"
    text: str                    # verbatim or paraphrased fact
    driver_tags: list[str] = []  # which Driver.name fields this updates


class CandidateTheme(BaseModel):
    """
    Durable narrative: the secular / cyclical story.
    Type: core themes from research notes.
    Downstream: becomes a ThemeObject after passing through all four engines.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    statement: str
    horizon: str
    evidence_ids: list[str] = []   # Observation ids that support this theme
    consensus_ids: list[str] = []  # ConsensusSignal ids that measure attention

    # Stage 0 scoring — cheap p−q pre-screen
    evidence_score: float = 0.0    # recency-weighted count of supporting Observations
    attention_score: float = 0.0   # strength-weighted ConsensusSignal support
    pre_screen_score: float = 0.0  # evidence_score − attention_score ≈ p−q proxy


class ConsensusSignal(BaseModel):
    """
    Market attention / positioning.
    Type: hot topics from research notes; ETF flow z-scores (TAARSS); surveys.
    Downstream: prior for market-implied q_s; input to crowding penalty c.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    source: str                    # e.g. "TAARSS", "DB_flow_report", "GS_survey"
    topic: str
    attention_strength: float      # z-score or normalised [0, 1]
    direction: Literal["positive", "negative", "neutral"]
    date: str


# ── Engine 1 output: thesis + axis (Q1, Q2, Q3) ──────────────────────────────

class Driver(BaseModel):
    """One causal factor acting on the axis. Q1 / Driver Extractor."""
    name: str
    sign: Literal["+", "-"]       # direction of effect on axis
    proxy_observable: str         # the computable series proxying this driver
    current_level: Optional[float] = None
    mechanism: str                # one sentence: driver → axis
    # optional — requires historical signal regression
    edge_elasticity: Optional[float] = None  # ∂(edge)/∂(driver_level) / edge: % edge change per 1% driver change


class CausalChainStep(BaseModel):
    from_node: str
    to_node: str


class Thesis(BaseModel):
    """Engine 1 output. Answers Q1 (theme) and Q2 (universe, via drivers)."""
    drivers: list[Driver]
    causal_chain: list[CausalChainStep]  # DAG: driver → intermediate → axis
    direction_of_view: str               # signed claim, e.g. "axis steepens (+)"
    # optional — requires historical driver signal correlation matrix
    driver_diversification_multiplier: Optional[float] = None  # 1/sqrt(avg pairwise ρ); >1 when drivers are uncorrelated


class AxisHistory(BaseModel):
    mean: float          # long-run unconditional mean
    vol: float           # σ (same units as axis)
    percentile: float    # current value percentile in history
    regime_tags: list[str]


class Axis(BaseModel):
    """
    Engine 1 output. Answers Q2 (universe scoping) and Q3 (the hard gate).
    Gate: definition must name a real, computable time series.
    Reject any axis that is a label ("credit risk") not a series
    ("CDX.IG 5Y OAS" or "IG AI-issuer 5s30s OAS slope").
    Universe scoping: L_i >= tau_L (min liquidity), o_i <= o* (max OAS).
    """
    definition: str    # full operational description + universe
    measurement: str   # exactly how it is computed; data source
    current_value: float
    history: AxisHistory
    # optional — macro regime detected from central bank signals / HMM
    regime: Optional[Literal["easing", "neutral", "tightening", "crisis"]] = None


# ── Causal Theme Compiler — ONE causal chain whose theme nodes carry axes ─────

class CausalNode(BaseModel):
    """One node in the single depth-first causal chain.

    kind=="theme" is a TRADEABLE node and MUST terminate in an operational axis
    (a named, computable spread/ratio). A node with no axis is a mechanism link
    (a valid dead end) — never invent an axis to extend the chain.
    """
    id: str
    statement: str
    kind: Literal["cause", "theme", "consequence"]
    axis: Optional[Axis] = None
    axis_operational: bool = False

    @model_validator(mode="after")
    def _axis_rules(self) -> "CausalNode":
        if self.axis_operational and self.axis is None:
            raise ValueError(
                f"CausalNode '{self.id}': axis_operational=True requires an axis."
            )
        if self.kind == "theme" and not (self.axis is not None and self.axis_operational):
            raise ValueError(
                f"CausalNode '{self.id}': a kind='theme' node must carry an OPERATIONAL "
                "axis (axis set and axis_operational=True). A dead end must be kind "
                "'cause'/'consequence' with axis=None — do not invent an axis."
            )
        return self


class CausalEdge(BaseModel):
    """A single hop. inferred=True if the agent derived it; False if stated in a
    source. feedback=True marks a reflexive link (outcome feeds back on the driver)."""
    from_id: str
    to_id: str
    mechanism: str
    inferred: bool
    feedback: bool = False


class CausalChain(BaseModel):
    """One main theme, one chain, depth-first (no tree). Edges must reference nodes."""
    nodes: list[CausalNode]
    edges: list[CausalEdge]

    @model_validator(mode="after")
    def _edges_reference_nodes(self) -> "CausalChain":
        ids = {n.id for n in self.nodes}
        if len(ids) != len(self.nodes):
            raise ValueError("CausalChain node ids must be unique.")
        for e in self.edges:
            if e.from_id not in ids or e.to_id not in ids:
                raise ValueError(
                    f"CausalChain edge {e.from_id}->{e.to_id} references a missing node."
                )
        return self


# ── System Structure Mapper (Meadows) — embeds the causal chain in a system ───

class Stock(BaseModel):
    """A LEVEL measurable at an instant (outstanding debt, index weight, AUM)."""
    name: str
    unit: str
    observable: Optional[str] = None


class Flow(BaseModel):
    """A RATE over time that changes a stock (issuance, fund flows, defaults).
    Distinct type from Stock — misclassifying level vs rate is the common error."""
    name: str
    changes_stock: str          # which Stock.name this flow moves
    unit_per_time: str
    observable: Optional[str] = None


class FeedbackLoop(BaseModel):
    """Reinforcing (amplifies) or balancing (stabilises). Reflexive links are marked
    feedback on the underlying CausalEdge."""
    id: str
    type: Literal["reinforcing", "balancing"]
    path: list[str]             # node-id sequence the loop traverses
    delay: Optional[str] = None
    closes_via: str = ""        # what closes the loop back on itself


class Delay(BaseModel):
    """A lag between a flow and its stock, or a driver and its price response — where
    the system surprises investors."""
    between: str
    length: str
    why_it_matters: str = ""


class SystemMap(BaseModel):
    """Theme embedded in a system (Meadows). Reuses the causal chain's nodes/edges as
    elements/interconnections; adds stocks, flows, loops, delays, shocks, observables."""
    boundary_inside: list[str]
    boundary_outside: list[str]
    boundary_rationale: str = ""
    function_purpose: str
    elements: list[CausalNode] = []            # reuse the chain's nodes
    interconnections: list[CausalEdge] = []     # reuse the chain's edges (+ ones a chain misses)
    stocks: list[Stock] = []
    flows: list[Flow] = []
    feedback_loops: list[FeedbackLoop] = []
    delays: list[Delay] = []
    external_shocks: list[str] = []
    internal_responses: list[str] = []
    observable_variables: list[str] = []
    surprise_modes: list[str] = []


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


# ── Engine 2 output: scenarios + pricing (Q4–Q7) ─────────────────────────────

class Scenario(BaseModel):
    """One state of the world. Engine 2 / Scenario Proposer."""
    name: str
    p_s: float = Field(ge=0.0, le=1.0)   # our probability
    driver_path: str                       # which drivers realise in this state
    implied_axis_value: float              # X_s: fair value of axis | state
    pnl_per_unit: float                    # $ P&L per unit notional if state realises
    # optional — residual std of X_s | state (Step 3). 0.0 → X_s is a point estimate.
    sigma_g_s: float = 0.0
    # optional — unconditional frequency of this state, for prior="historical"
    hist_freq: Optional[float] = None
    # optional — requires macro regime classification (Lancaster / HMM)
    regime_conditional_p_s: Optional[float] = None  # p_s given axis.regime; re-run solver on this when set


class PricedIn(BaseModel):
    """Max-entropy market-implied scenario probabilities. Q6."""
    q_s: list[float]   # same ordering as ThemeObject.scenarios
    frac: float        # (X_mkt − normal_fv) / (scenario_fv − normal_fv)


class EdgeContribution(BaseModel):
    """Per-scenario edge attribution — typed, not a free-form dict (AR-ABS-003)."""
    scenario: str
    contribution: float   # (p_s - q_s) * X_s
    disagreement: float   # (p_s - q_s)


class Pricing(BaseModel):
    """Engine 2 quant output. Q4 through Q7."""
    normal_fv: float       # Q4: unconditional / regime mean of axis
    scenario_fv: float     # Q5: Σ p_s X_s
    priced_in: PricedIn    # Q6: max-entropy q_s
    residual_edge: float   # Q7: ⟨p − q, X⟩  (the edge identity)
    # optional (Step 3) — sqrt(Var[X]) under the scenario mixture (within + between).
    scenario_fv_std: Optional[float] = None
    # optional (Steps 4/6) — edge enrichment. Deterministic ones populated whenever
    # thesis_sign + sigma_axis are supplied; MC ones (edge_std..infeasible_fraction)
    # only when MC is run.
    edge_attribution: Optional[list[EdgeContribution]] = None
    edge_direction_ok: Optional[bool] = None
    vol_adjusted_edge: Optional[float] = None
    edge_basis: Optional[str] = None          # e.g. "gross_of_risk_premium"
    q_status: Optional[str] = None             # "FEASIBLE" / "INFEASIBLE"
    edge_std: Optional[float] = None
    snr: Optional[float] = None
    p_success: Optional[float] = None
    infeasible_fraction: Optional[float] = None


# ── Engine 3 output: expressions (Q8, Q9) ────────────────────────────────────

class ScenarioPnL(BaseModel):
    scenario_name: str
    pnl: float


class Expression(BaseModel):
    """
    One trade expression. Engine 3 / Enumerator + Scorer.
    score is None if any gate failed; computed if all gates passed.
    "Best" is never max E[P&L] — it is the highest multiplicative score
    among expressions that pass Omega >= 2, liquidity >= min, cost <= max,
    finite worst-case.
    """
    id: str
    strategy_family: str   # e.g. "5s30s CDS curve", "cash bond L/S", "ETF basis"
    long_leg: str
    short_leg: str
    hedge_ratio: float
    scenario_pnl: list[ScenarioPnL]  # Π_s for every scenario
    purity: float     # ρ²: R² of expression P&L on axis moves
    convexity: float  # κ
    carry: float      # θ (bps p.a.)
    liquidity: float  # λ: composite Xantimum liquidity score [0, 1]
    crowding: float   # c: [0, 1]
    round_trip_cost_bps: float = 0.0      # cost gate input: full round-trip cost in bps
    score: Optional[float] = None         # None = gated out
    gate_fail_reason: Optional[str] = None
    # optional enrichment — require historical data to compute
    oos_stability: Optional[float] = None        # OOS/IS Sharpe ratio across walk-forward windows (Pardo)
    factor_betas: Optional[dict[str, float]] = None  # single-factor betas post-neutralisation (Tulchinsky)


# ── Engine 4 output: sizing + risk (Q10–Q12) ─────────────────────────────────

class Sizing(BaseModel):
    """Alaph Step-4 grid. Q10."""
    conviction: int = Field(ge=1, le=4)  # 1 lowest, 4 highest
    sizing_factor: float
    target_pnl: float    # $ gross target P&L for this position
    position: str        # human-readable, e.g. "20mm 5s30s CDS steepener"
    # Proposal 8 — dynamic vol targeting (Carver, Systematic Trading)
    vol_target_bps: Optional[float] = None    # target annualised axis vol in bps
    realized_vol_bps: Optional[float] = None  # rolling realized vol (same units)
    vol_scalar: Optional[float] = None        # vol_target / realized_vol, capped at 2.0; scale position by this
    # Proposal 2 — net-of-cost P&L transparency (Carver, Advanced Futures)
    round_trip_cost_bps: Optional[float] = None   # estimated round-trip cost for this expression
    expected_roundtrips: Optional[float] = None   # round trips per year at expected holding period
    net_target_pnl: Optional[float] = None        # target_pnl minus estimated annual cost


class StopLoss(BaseModel):
    """Q11. Level is on the axis, not on P&L — structural exit."""
    level: float
    rationale: str


class Falsifier(BaseModel):
    """Q12. First-class field, not a footnote."""
    observable: str      # computable series to monitor
    threshold: float     # τ: the crossing level
    kill_rule: str       # "if {observable} crosses {threshold}, thesis is dead"


class Risk(BaseModel):
    stop_loss: StopLoss
    falsifiers: list[Falsifier]
    invalidation_horizon: str
    max_loss: float      # $ worst-case across all expressions × scenarios


# ── PM gate (Q13) ─────────────────────────────────────────────────────────────

class PMGate(BaseModel):
    """
    The agent's hard boundary. Q13.
    Lists what the agent could not resolve. Hands control to the PM.
    The agent is an epistemic engine: it converts and surfaces.
    It does NOT decide, execute, route orders, or touch a broker.
    """
    open_questions: list[str]


# ── Provenance ────────────────────────────────────────────────────────────────

class Provenance(BaseModel):
    evidence: list[str]                          # source document list
    confidence: float = Field(ge=0.0, le=1.0)
    last_updated: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


# ── ThemeObject ───────────────────────────────────────────────────────────────

class ThemeObject(BaseModel):
    """
    The output of the pipeline. Append-only, observable-anchored.
    Cannot be marked complete unless all four discipline gates pass.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    statement: str     # Q1: one-sentence thesis
    horizon: str
    author: str
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    version: int = 1

    thesis: Thesis             # Engine 1
    axis: Axis                 # Engine 1
    scenarios: list[Scenario]  # Engine 2
    pricing: Pricing           # Engine 2
    expressions: list[Expression]  # Engine 3
    sizing: Sizing             # Engine 4
    risk: Risk                 # Engine 4
    pm_gate: PMGate            # Q13 — agent boundary
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

    @model_validator(mode="after")
    def discipline_gates(self) -> "ThemeObject":
        """
        Four hard gates. Failure raises ValueError — the object is not emitted.
        These are type constraints, not quality checks.
        """
        # Gate 1: axis must be operational (named computable series)
        if not self.axis.definition.strip() or not self.axis.measurement.strip():
            raise ValueError(
                "Gate 1 FAIL: axis.definition and axis.measurement must both be "
                "populated with a named, computable time series — not a label."
            )

        # Gate 2: residual_edge must be computed
        # (pricing object exists by type, but edge=0.0 from an uninitialised stub
        # is not the same as a computed zero — caller must set it explicitly)
        if self.pricing.residual_edge is None:
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
        if not self.risk.falsifiers:
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
