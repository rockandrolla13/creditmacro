"""Case-system models: PolicyConfig, the Oracle discriminated union, and the small"""
from __future__ import annotations

from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field

from .scoring import compute_omega
from .schema import (
    Axis,
    BiasCritique,
    CausalChain,
    CausalNode,
    EdgeContribution,  # noqa: F401  (re-exported for back-compat)
    Expression,
    PMGate,
    Provenance,
    Risk,
    Scenario,
    LoopDiagnosis,
    ProbabilityEvidenceRef,
    ProbabilitySource,
    Sizing,
    SystemMap,
    ThemeObject,
    Thesis,
    TrapImplications,
)

# ── Policy: single source of truth for gate thresholds (AR-DRY-001) ──────────

class PolicyConfig(BaseModel):
    """Gate thresholds + scoring constants. Defaults reproduce the values currently"""
    omega_min: float = 2.0
    liquidity_min: float = 0.40
    cost_fraction_max: float = 0.33
    convexity_weight_a: float = 0.10   # `a` in score_expression
    crowding_decay_g: float = 0.50     # `g` in score_expression
    snr_min: float = 1.0               # SNR gate — SEPARATE from the 4 discipline gates

# ── Typed contracts (AR-ABS-003) — EdgeContribution now lives in schema.py ────

class AssertionResult(BaseModel):
    name: str
    passed: bool
    detail: str = ""

# ── Oracle discriminated union (AR-ABS-001 / AR-EXT-001) ─────────────────────

class _OracleBase(BaseModel):
    def check(self, theme: ThemeObject) -> list[AssertionResult]:
        """Kind-specific assertions. The invariants floor is run separately by the"""
        raise NotImplementedError(
            f"{type(self).__name__}.check is implemented in its own build step."
        )

class ExactOracle(_OracleBase):
    """Pins exact quant outputs to a tolerance. Used by self-authored cases where we"""
    kind: Literal["exact"] = "exact"
    scenario_fv: float
    q: list[float]
    edge: float
    omega: float
    score: float
    gated_out: list[str]
    tol: float = 1e-6

    def check(self, theme: ThemeObject) -> list[AssertionResult]:
        def near(a: float, b: float) -> bool:
            return abs(a - b) <= self.tol

        results: list[AssertionResult] = []
        pr = theme.pricing

        results.append(AssertionResult(
            name="scenario_fv", passed=near(pr.scenario_fv, self.scenario_fv),
            detail=f"{pr.scenario_fv} vs {self.scenario_fv}",
        ))

        q_ok = (len(pr.priced_in.q_s) == len(self.q)
                and all(near(a, b) for a, b in zip(pr.priced_in.q_s, self.q)))
        results.append(AssertionResult(
            name="q", passed=q_ok, detail=f"{pr.priced_in.q_s} vs {self.q}",
        ))

        results.append(AssertionResult(
            name="edge", passed=near(pr.residual_edge, self.edge),
            detail=f"{pr.residual_edge} vs {self.edge}",
        ))

        best = theme.best_expression()
        best_score = best.score if best is not None else float("nan")
        results.append(AssertionResult(
            name="score", passed=best is not None and near(best_score, self.score),
            detail=f"{best_score} vs {self.score}",
        ))

        if best is not None:
            weights = [s.p_s for s in theme.scenarios]
            omega = compute_omega([p.pnl for p in best.scenario_pnl], weights=weights)
            omega_ok = near(omega, self.omega)
        else:
            omega, omega_ok = float("nan"), False
        results.append(AssertionResult(
            name="omega", passed=omega_ok, detail=f"{omega} vs {self.omega}",
        ))

        gated = sorted(e.id for e in theme.expressions if e.score is None)
        results.append(AssertionResult(
            name="gated_out", passed=gated == sorted(self.gated_out),
            detail=f"{gated} vs {sorted(self.gated_out)}",
        ))

        return results

class RatioTarget(BaseModel):
    target: float
    tol: float

class AcceptanceOracle(_OracleBase):
    """Asserts structural relationships (a P&L ratio, attribution, edge direction)"""
    kind: Literal["acceptance"] = "acceptance"
    base_worst_ratio: RatioTarget
    edge_sign: Literal["thesis_aligned"] = "thesis_aligned"
    attribution_top: str

    def check(self, theme: ThemeObject) -> list[AssertionResult]:
        results: list[AssertionResult] = []

        best = theme.best_expression()

        if best is None:
            results.append(AssertionResult(
                name="base_worst_ratio", passed=False, detail="no scored expression",
            ))
        else:
            base_idx = max(range(len(theme.scenarios)), key=lambda i: theme.scenarios[i].p_s)
            pnls = [p.pnl for p in best.scenario_pnl]
            base_pnl = pnls[base_idx]
            worst_pnl = min(pnls)
            if abs(worst_pnl) < 1e-12:
                ratio_ok, ratio = False, float("inf")
            else:
                ratio = base_pnl / abs(worst_pnl)
                ratio_ok = abs(ratio - self.base_worst_ratio.target) <= self.base_worst_ratio.tol
            results.append(AssertionResult(
                name="base_worst_ratio", passed=ratio_ok,
                detail=f"base/|worst| = {ratio:.3f} vs {self.base_worst_ratio.target}±{self.base_worst_ratio.tol}",
            ))

        attribution = theme.pricing.edge_attribution
        top = attribution[0].scenario if attribution else None
        results.append(AssertionResult(
            name="attribution_top", passed=(top == self.attribution_top),
            detail=f"{top} vs {self.attribution_top}",
        ))

        results.append(AssertionResult(
            name="edge_sign", passed=(theme.pricing.edge_direction_ok is True),
            detail=f"edge_direction_ok={theme.pricing.edge_direction_ok}",
        ))

        return results

class InvariantsOnlyOracle(_OracleBase):
    """No numeric oracle — only the always-on invariants floor applies. The path for"""
    kind: Literal["invariants_only"] = "invariants_only"

    def check(self, theme: ThemeObject) -> list[AssertionResult]:
        return []  # the invariants floor (run by the runner) is the whole oracle

Oracle = Annotated[
    Union[ExactOracle, AcceptanceOracle, InvariantsOnlyOracle],
    Field(discriminator="kind"),
]

# ── CaseSpec — all the data to build a ThemeObject except the COMPUTED parts ──
# (pricing q/edge and expression scores are computed by the workflow, not stored).

class CausalPayload(BaseModel):
    """Hand-built EXPAND_CAUSAL output a case can carry, returned verbatim by the"""
    main_theme: CausalNode
    causal_chain: CausalChain
    shared_factor: str

class CaseSpec(BaseModel):
    """One self-contained case. The ScriptedProvider returns slices of this; the"""
    theme_sentence: str
    horizon: str
    author: str

    thesis: Thesis
    axis: Axis

    # prior is a vector OR a string the loader resolves to a vector
    prior: Union[list[float], Literal["uniform", "historical"]]

    scenarios: list[Scenario]
    x_mkt: Optional[float] = None   # live market price of the axis (None ⇒ discovery-only, no live mark)
    normal_fv: float      # unconditional / regime mean

    # Detailed-expression half — required for expression cases, OMITTED for discovery-only
    # cases (the discovery firewall stops before pricing/sizing). Defaults keep existing
    # full cases valid while allowing a discovery fixture to carry none of them.
    expressions: list[Expression] = []   # pre-scoring (score is None); workflow scores them
    capital: float = 0.0            # scoring input (existing book exposure)

    sizing: Optional[Sizing] = None
    risk: Optional[Risk] = None
    pm_gate: Optional[PMGate] = None
    provenance: Provenance

    thesis_sign: Literal[-1, 1]
    edge_mc: bool = False     # run Monte-Carlo edge (SNR/std) in run_pricing
    # Q4 — supplied probability evidence (per scenario name) + prior source labels.
    probability_evidence: dict[str, list[ProbabilityEvidenceRef]] = {}
    prior_sources: dict[str, ProbabilitySource] = {}
    causal: Optional[CausalPayload] = None   # EXPAND_CAUSAL payload (optional)
    system_map: Optional[SystemMap] = None        # SYSTEM_MAP stage payload (optional)
    bias_critique: Optional[BiasCritique] = None  # CRITIQUE stage payload (optional)
    loop_diagnosis: Optional[LoopDiagnosis] = None      # TRAP pre-pricing payload (optional)
    trap_implications: Optional[TrapImplications] = None  # TRAP post-pricing payload (optional)
    policy: Union[Literal["default"], PolicyConfig] = "default"
    oracle: Oracle

    def resolved_policy(self) -> PolicyConfig:
        return PolicyConfig() if self.policy == "default" else self.policy
