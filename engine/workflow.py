"""
run_workflow — drive a Provider through the engine seams over a shared ThemeObject.

The runner is case-blind: it talks only to the Provider protocol and the quant layer.
It computes the two things the engine OWNS — pricing (Engine 2) and expression scores
(Engine 3) — and assembles everything else from provider seams.

PolicyConfig is threaded as the single source of gate thresholds (AR-DRY-001): the
workflow passes its fields into score_expression rather than relying on that function's
keyword defaults.
"""
from __future__ import annotations

from .cases import PolicyConfig
from .engines import compute_omega, run_pricing, score_expression
from .protocols import Provider
from .schema import Expression, ThemeObject


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


def run_workflow(provider: Provider, policy: PolicyConfig) -> tuple[ThemeObject, str]:
    """Run the pipeline and return (ThemeObject, decision memo)."""
    ctx = provider.context()

    thesis = provider.extract_drivers(ctx.statement)

    # EXPAND_CAUSAL stage (after parse/extract, before axis). When the provider yields a
    # causal chain, its main theme's operational axis feeds the pricing path; otherwise
    # fall back to the axis-definer. A malformed chain MUST fail here.
    main_theme, causal_chain, shared_factor = provider.expand_causal(ctx.statement, ctx.statement)
    if main_theme is not None:
        _validate_causal_chain(main_theme, causal_chain)
        axis = main_theme.axis
    else:
        axis = provider.define_axis(thesis)

    # SYSTEM_MAP stage (embeds the causal chain) and CRITIQUE stage (adversarial review).
    # Both optional; they record structure/judgment on the ThemeObject and do not gate it.
    system_map = provider.build_system_map(thesis, causal_chain)
    bias_critique = provider.critique_mental_model(ctx.statement, causal_chain)

    normal_fv = provider.normal_fair_value(axis)
    scenarios = provider.propose_scenarios(thesis, axis)

    # Engine 2 — pricing (q via max-entropy/tilt, residual edge). prior == [] means
    # "use the solver default" (uniform); a resolved vector is passed through.
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

    # Engine 4 — sizing + risk + PM gate (provider-supplied for a scripted case).
    bundle = provider.size_and_risk(thesis, axis, best, ctx.conviction)

    theme = ThemeObject(
        statement=ctx.statement,
        horizon=ctx.horizon,
        author=ctx.author,
        thesis=thesis,
        axis=axis,
        scenarios=scenarios,
        pricing=pricing,
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
    )
    return theme, _render_memo(theme, best, pricing)


def _validate_causal_chain(main_theme, causal_chain) -> None:
    """Boundary-validate the EXPAND_CAUSAL output (node-level rules are enforced by the
    schema; this asserts the cross-object invariants the stage depends on)."""
    if causal_chain is None:
        raise ValueError("EXPAND_CAUSAL: main_theme present but causal_chain is None")
    if not (main_theme.kind == "theme" and main_theme.axis_operational and main_theme.axis is not None):
        raise ValueError("EXPAND_CAUSAL: main_theme must be a kind='theme' node with an operational axis")
    if main_theme.id not in {n.id for n in causal_chain.nodes}:
        raise ValueError("EXPAND_CAUSAL: main_theme must be one of the chain's nodes")


def _render_memo(theme: ThemeObject, best: Expression, pricing) -> str:
    q_fmt = ", ".join(f"{q:.3f}" for q in pricing.priced_in.q_s)
    return (
        f"# Decision Memo — {theme.statement}\n\n"
        f"**Axis:** {theme.axis.definition}\n\n"
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
