"""run_workflow — drive a Provider through the engine seams over a shared ThemeObject."""
from __future__ import annotations

from types import SimpleNamespace
from typing import Literal, Optional

from .cases import PolicyConfig
from .discovery import select_strategy_families
from .engine2 import run_pricing
from .probability import justify_probabilities
from .scoring import compute_omega, score_expression
from .protocols import Provider, RunContext
from .schema import (
    Axis, Expression, ProbabilitySetJustification, Scenario, StrategyFamilyRec, ThemeObject,
)

def _prior_vector(ctx: RunContext, n: int) -> list[float]:
    """The resolved prior, or uniform when the context carries none."""
    return ctx.prior if ctx.prior else [1.0 / n] * n


def _justify(scenarios: list[Scenario], ctx: RunContext, *, gate_case_evidence: bool = False
             ) -> Optional[ProbabilitySetJustification]:
    """Q4 — label the scenario p_s (audit-only). In discovery (gate_case_evidence=True) the
    firewall drops case-class evidence before justifying so phase-A can't cite history."""
    if not scenarios:
        return None
    evidence = ctx.probability_evidence
    if gate_case_evidence:
        evidence = {k: [r for r in refs if not _is_case_evidence(r)] for k, refs in evidence.items()}
    return justify_probabilities(scenarios, evidence, ctx.prior_sources)


_CASE_SLUG_MARKERS = ("case", "outcome", "historical", "postmortem", "analogue", "theme-", "scenario-")

def _is_case_evidence(ref) -> bool:
    """Case-class evidence (past outcomes / case-page citations) is blocked in phase-A
    discovery. MVP heuristic on the source_slug; a later step can resolve access_class via
    the wiki memory layer instead."""
    slug = (ref.source_slug or "").lower()
    return any(m in slug for m in _CASE_SLUG_MARKERS)

def _strategy_families(
    axis: Axis,
    scenarios: list[Scenario],
    ctx: RunContext,
    *,
    has_operational_axis: bool = True,
    causal_confidence: float = 1.0,
    probability_quality: float = 1.0,
) -> list[StrategyFamilyRec]:
    """Route the promoted theme's axis to a strategy family (shape+direction), with"""
    prior = _prior_vector(ctx, len(scenarios)) if scenarios else []
    return select_strategy_families(
        axis=axis,
        scenarios=scenarios,
        prior=prior,
        thesis_sign=ctx.thesis_sign,
        x_mkt=ctx.x_mkt,
        has_operational_axis=has_operational_axis,
        has_market_value=ctx.x_mkt is not None,
        causal_confidence=causal_confidence,
        probability_quality=probability_quality,
    )

def _score_expressions(
    expressions: list[Expression],
    scenario_probs: list[float],
    capital: float,
    policy: PolicyConfig,
) -> list[Expression]:
    """Score each expression — gates FIRST, rank SECOND — returning scored copies."""
    scored: list[Expression] = []
    for expr in expressions:
        pnls = [p.pnl for p in expr.scenario_pnl]
        omega = compute_omega(pnls, weights=scenario_probs)
        expected_pnl = float(sum(p * x for p, x in zip(scenario_probs, pnls)))
        score, fail = score_expression(
            rho2=expr.purity,
            omega=omega,
            convexity=expr.convexity,
            liquidity=expr.liquidity,
            crowding=expr.crowding,
            capital=capital,
            round_trip_cost_bps=expr.round_trip_cost_bps,
            expected_pnl_bps=expected_pnl,
            a=policy.convexity_weight_a,
            g=policy.crowding_decay_g,
            omega_min=policy.omega_min,
            liquidity_min=policy.liquidity_min,
            cost_fraction_max=policy.cost_fraction_max,
        )
        scored.append(expr.model_copy(update={"score": score, "gate_fail_reason": fail}))
    return scored

def run_workflow(
    provider: Provider,
    policy: PolicyConfig,
    mode: Literal["discovery", "expression"] = "discovery",
) -> tuple[ThemeObject, str]:
    """Run the pipeline in the requested mode and return (ThemeObject, memo)."""
    if mode == "expression":
        return _run_expression(provider, policy)
    return _run_discovery(provider, policy)

def _causal_stage(provider, ctx, thesis, *, fallback_axis: bool):
    """EXPAND_CAUSAL + the system-map / critique / loop-diagnosis block shared by both"""
    main_theme, causal_chain, shared_factor = provider.expand_causal(ctx.statement, ctx.statement)
    if main_theme is None and not fallback_axis:
        return SimpleNamespace(main_theme=None, causal_chain=causal_chain,
                               shared_factor=shared_factor, axis=None, system_map=None,
                               bias_critique=None, loop_diagnosis=None)
    if main_theme is not None:
        _validate_causal_chain(main_theme, causal_chain)
        axis = main_theme.axis
    else:
        axis = provider.define_axis(thesis)
    system_map = provider.build_system_map(thesis, causal_chain)
    return SimpleNamespace(
        main_theme=main_theme, causal_chain=causal_chain, shared_factor=shared_factor,
        axis=axis, system_map=system_map,
        bias_critique=provider.critique_mental_model(ctx.statement, causal_chain),
        loop_diagnosis=provider.diagnose_loops(system_map),
    )

# ── DISCOVERY mode — idea → causal object → ranked families → STOP ────────────

def _run_discovery(provider: Provider, policy: PolicyConfig) -> tuple[ThemeObject, str]:
    ctx = provider.context()

    # Iceberg classification (Stage 0). Scripted cases carry empty streams; this is the
    # routing step a generative provider would populate. It never gates discovery.
    _ingestion = provider.parse(ctx.statement)

    thesis = provider.extract_drivers(ctx.statement)

    # A causal object is MANDATORY — no fallback to define_axis. main_theme=None ⇒ emit a
    # blocked record (an inspectable HALT, not a throw).
    cs = _causal_stage(provider, ctx, thesis, fallback_axis=False)
    if cs.main_theme is None:
        blocked = ThemeObject(
            status="blocked", block_reason="needs_causal_object",
            statement=ctx.statement, horizon=ctx.horizon, author=ctx.author,
            thesis=thesis, axis=None, provenance=ctx.provenance,
        )
        return blocked, _render_blocked_memo(blocked)

    # Scenarios the causal object already carries (we do NOT generate them); used only
    # for the LIGHT priced-in confidence, never for detailed pricing.
    scenarios = provider.propose_scenarios(thesis, cs.axis, cs.loop_diagnosis)
    # Q4 (firewall-gated): justify p_s, then let its quality floor the family confidence.
    prob_just = _justify(scenarios, ctx, gate_case_evidence=True)
    pq = prob_just.probability_quality if prob_just else 1.0

    # Promotion requires a falsifier: no falsifier ⇒ block promotion (stay at
    # discovery_complete, the causal object built but not routed to a family).
    has_falsifier = bool(cs.loop_diagnosis and cs.loop_diagnosis.invalidation_evidence)
    if has_falsifier:
        families = _strategy_families(
            cs.axis, scenarios, ctx, has_operational_axis=cs.main_theme.axis_operational,
            probability_quality=pq,
        )
        status = "strategy_family_routed" if families else "discovery_complete"
    else:
        families = []
        status = "discovery_complete"

    theme = ThemeObject(
        status=status, statement=ctx.statement, horizon=ctx.horizon, author=ctx.author,
        thesis=thesis, axis=cs.axis, strategy_families=families, provenance=ctx.provenance,
        probability_justification=prob_just,
        main_theme=cs.main_theme, causal_chain=cs.causal_chain, shared_factor=cs.shared_factor,
        system_map=cs.system_map, bias_critique=cs.bias_critique, loop_diagnosis=cs.loop_diagnosis,
        # detailed-expression half intentionally left absent (None / empty)
    )
    return theme, _render_discovery_memo(theme)

# ── EXPRESSION mode — the full legacy pipeline (+ families, + status) ─────────

def _run_expression(provider: Provider, policy: PolicyConfig) -> tuple[ThemeObject, str]:
    ctx = provider.context()

    # Expression mode prices scenarios against the live mark — it cannot run without one.
    if ctx.x_mkt is None:
        raise ValueError(
            "expression mode requires a market value (x_mkt) to price scenarios; got None. "
            "Run mode='discovery' for a theme with no live mark."
        )

    thesis = provider.extract_drivers(ctx.statement)

    # EXPAND_CAUSAL + system block. Falls back to the axis-definer for causal-less scripted
    # cases (retained in expression mode only).
    cs = _causal_stage(provider, ctx, thesis, fallback_axis=True)
    axis = cs.axis
    main_theme, causal_chain, shared_factor = cs.main_theme, cs.causal_chain, cs.shared_factor
    system_map, bias_critique, loop_diagnosis = cs.system_map, cs.bias_critique, cs.loop_diagnosis

    normal_fv = provider.normal_fair_value(axis)
    scenarios = provider.propose_scenarios(thesis, axis, loop_diagnosis)

    # Engine 2 — pricing (q via max-entropy/tilt, residual edge).
    q0 = ctx.prior or None
    pricing = run_pricing(
        scenarios, ctx.x_mkt, normal_fv, q0=q0,
        thesis_sign=ctx.thesis_sign,
        sigma_axis=axis.history.vol,
        run_mc=ctx.run_edge_mc,
    )

    # Engine 3 — score the enumerated expressions.
    raw_expressions = provider.enumerate_expressions(thesis, axis, scenarios)
    scenario_probs = [s.p_s for s in scenarios]
    expressions = _score_expressions(raw_expressions, scenario_probs, ctx.capital, policy)

    scored = [e for e in expressions if e.score is not None]
    if not scored:
        raise ValueError("no expression survived the gates — cannot assemble a ThemeObject")
    best = max(scored, key=lambda e: e.score)

    trap_implications = provider.assess_trap_implications(scenarios, pricing, expressions)

    # Engine 4 — sizing + risk + PM gate.
    bundle = provider.size_and_risk(thesis, axis, best, ctx.conviction)

    # Q4 + discovery deliverable also attach to an expression_complete object.
    prob_just = _justify(scenarios, ctx)
    pq = prob_just.probability_quality if prob_just else 1.0
    has_op_axis = bool(axis.definition.strip() and axis.measurement.strip())
    families = _strategy_families(axis, scenarios, ctx, has_operational_axis=has_op_axis,
                                  probability_quality=pq)

    theme = ThemeObject(
        status="expression_complete",
        statement=ctx.statement,
        horizon=ctx.horizon,
        author=ctx.author,
        thesis=thesis,
        axis=axis,
        strategy_families=families,
        scenarios=scenarios,
        pricing=pricing,
        probability_justification=prob_just,
        expressions=expressions,
        sizing=bundle.sizing,
        risk=bundle.risk,
        pm_gate=bundle.pm_gate,
        provenance=ctx.provenance,
        main_theme=main_theme,
        causal_chain=causal_chain,
        shared_factor=shared_factor,
        system_map=system_map,
        bias_critique=bias_critique,
        loop_diagnosis=loop_diagnosis,
        trap_implications=trap_implications,
    )
    return theme, _render_memo(theme, best, pricing)

def _validate_causal_chain(main_theme, causal_chain) -> None:
    """Boundary-validate the EXPAND_CAUSAL output (node-level rules are enforced by the"""
    if causal_chain is None:
        raise ValueError("EXPAND_CAUSAL: main_theme present but causal_chain is None")
    if not main_theme.is_routable():
        raise ValueError("EXPAND_CAUSAL: main_theme must be a kind='theme' node with an operational axis")
    if main_theme.id not in {n.id for n in causal_chain.nodes}:
        raise ValueError("EXPAND_CAUSAL: main_theme must be one of the chain's nodes")

def _render_blocked_memo(theme: ThemeObject) -> str:
    return (
        f"# Discovery BLOCKED — {theme.statement}\n\n"
        f"**Status:** blocked · **Reason:** {theme.block_reason}\n\n"
        "Discovery halted before a valid causal object was built. No axis was "
        "manufactured from the thesis sentence and no pricing was run. Supply a causal "
        "object (expand_causal) and re-run discovery.\n"
    )

def _render_discovery_memo(theme: ThemeObject) -> str:
    fam_rows = "\n".join(
        f"- **{f.family}** (confidence {f.confidence:.3f}) — {f.rationale}"
        for f in theme.strategy_families
    )
    return (
        f"# Discovery Memo — {theme.statement}\n\n"
        f"**Status:** {theme.status} (ranked strategy families; detailed legs are downstream)\n\n"
        f"**Axis:** {theme.axis.definition}\n\n"
        f"**Shared factor:** {theme.shared_factor}\n\n"
        f"**Ranked strategy families:**\n{fam_rows}\n\n"
        f"_Discovery stops here. Detailed legs (curve points, names, hedge ratios, sizing) "
        f"require a separate expression-mode run on this discovery_complete object._\n"
    )

def _render_memo(theme: ThemeObject, best: Expression, pricing) -> str:
    q_fmt = ", ".join(f"{q:.3f}" for q in pricing.priced_in.q_s)
    top_family = theme.strategy_families[0].family if theme.strategy_families else "—"
    return (
        f"# Decision Memo — {theme.statement}\n\n"
        f"**Axis:** {theme.axis.definition}\n\n"
        f"**Top strategy family:** {top_family}\n\n"
        f"**Scenario FV (Q5):** {pricing.scenario_fv}bps · "
        f"**Market q (Q6):** [{q_fmt}] · "
        f"**Residual edge (Q7):** {pricing.residual_edge:+.1f}bps\n\n"
        f"**Best expression (Q8/Q9):** {best.strategy_family} "
        f"(score {best.score:.3f})\n\n"
        f"**Size (Q10):** {theme.sizing.position}\n\n"
        f"**Stop (Q11):** axis < {theme.risk.stop_loss.level}bps · "
        f"**Falsifiers (Q12):** {len(theme.risk.falsifiers)}\n\n"
        f"**PM open questions (Q13):** {len(theme.pm_gate.open_questions)}\n"
    )
