"""
Engine 2 — scenario pricing and edge (the SINGLE home for Engine-2 quant; AR-BND-001).

MATHEMATICS
  q (priced-in measure):  min_q KL(q ‖ prior)  s.t.  Σ q_s f_k(X_s) = c_k,  Σ q_s = 1.
  Solution is the EXPONENTIAL TILT
        q_s = prior_s · exp(Σ_k λ_k f_k(X_s)) / Z(λ),
  with λ solving the convex dual  min_λ  ln Z(λ) − Σ_k λ_k c_k.
    - K=1 (level f_1(X)=X, c_1=X_mkt): E_q[f] is monotone increasing in λ
      (dE/dλ = Var_q[f] ≥ 0) → 1-D root find.
    - K>1 (+ axis-struck option payoffs): K-dim Newton on the dual
      (gradient E_q[f]−c, Hessian Cov_q[f] ≻ 0).
  Feasibility: a solution exists iff each target c_k is strictly interior to
  (min_s f_k(X_s), max_s f_k(X_s)). Otherwise status=INFEASIBLE — q is NOT fabricated.

  edge (identity): ⟨p − q, X⟩.

RISK CAVEAT: prices give a RISK-NEUTRAL q; edge vs this q is GROSS OF RISK PREMIUM.
  (A pricing-kernel map to physical q lands with the MC-edge step.)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Literal, Optional

import numpy as np
from pydantic import BaseModel
from scipy.optimize import brentq

from .schema import EdgeContribution, PricedIn, Pricing, Scenario


# ── Moment constraints ────────────────────────────────────────────────────────

@dataclass(frozen=True)
class MomentConstraint:
    """One constraint  Σ_s q_s fn(X_s) = target  on the tilted measure."""
    fn: Callable[[float], float]
    target: float
    label: str = ""


def level_constraint(x_mkt: float) -> MomentConstraint:
    """The level constraint E_q[X] = X_mkt (f(X)=X)."""
    return MomentConstraint(fn=lambda x: x, target=float(x_mkt), label="level")


def option_constraint(strike: float, target: float) -> MomentConstraint:
    """An axis-struck call payoff f(X)=max(X−strike,0) constraining q's tail/curvature."""
    return MomentConstraint(
        fn=lambda x, k=float(strike): max(x - k, 0.0),
        target=float(target),
        label=f"call@{strike}",
    )


@dataclass
class QSolution:
    q: list[float]
    status: Literal["FEASIBLE", "INFEASIBLE"]
    reason: str = ""
    lambdas: list[float] = field(default_factory=list)


# ── Tilt internals ────────────────────────────────────────────────────────────

def _tilt_q(prior: np.ndarray, expo: np.ndarray) -> np.ndarray:
    """q_s ∝ prior_s · exp(expo_s), computed stably."""
    m = float(np.max(expo))
    w = prior * np.exp(expo - m)
    return w / w.sum()


def _expand_bracket(resid, x0: float, hit) -> float:
    """Geometrically expand x0 (×2, up to 200 steps) until resid(x) satisfies `hit`."""
    x = x0
    for _ in range(200):
        if hit(resid(x)):
            break
        x *= 2.0
    return x


def solve_q_tilt(
    X_s: list[float],
    constraints: list[MomentConstraint],
    prior: list[float],
) -> QSolution:
    """Exact min-KL(q‖prior) tilt subject to the given moment constraints.

    See module docstring. Returns INFEASIBLE (without fabricating q) when any target
    is not strictly interior to its payoff's scenario span.
    """
    n = len(X_s)
    prior_arr = np.asarray(prior, dtype=float)
    if prior_arr.shape != (n,):
        raise ValueError(f"prior length {prior_arr.shape} != number of scenarios {n}")
    if not np.all(prior_arr > 0):
        raise ValueError("prior must be strictly positive")

    K = len(constraints)
    F = np.array([[con.fn(x) for x in X_s] for con in constraints], dtype=float)  # (K, n)
    c = np.array([con.target for con in constraints], dtype=float)

    # Feasibility: each target strictly interior to its payoff range.
    EPS = 1e-12
    for k in range(K):
        fmin, fmax = float(F[k].min()), float(F[k].max())
        if (fmax - fmin) <= EPS or not (fmin + EPS < c[k] < fmax - EPS):
            return QSolution(
                q=[], status="INFEASIBLE",
                reason=(
                    f"constraint '{constraints[k].label or k}' target {c[k]} is not "
                    f"interior to the scenario span ({fmin}, {fmax}) — set incomplete"
                ),
            )

    if K == 1:
        fv = F[0]
        tgt = float(c[0])

        def resid(lam: float) -> float:
            q = _tilt_q(prior_arr, lam * fv)
            return float(q @ fv - tgt)

        lo = _expand_bracket(resid, -1.0, lambda r: r < 0)
        hi = _expand_bracket(resid, 1.0, lambda r: r > 0)
        lam = brentq(resid, lo, hi, xtol=1e-15, rtol=4 * np.finfo(float).eps, maxiter=200)
        q = _tilt_q(prior_arr, lam * fv)
        return QSolution(q=q.tolist(), status="FEASIBLE", lambdas=[float(lam)])

    # K > 1 — Newton on the dual gradient/Hessian.
    lam = np.zeros(K)
    q = _tilt_q(prior_arr, lam @ F)
    for _ in range(200):
        q = _tilt_q(prior_arr, lam @ F)
        grad = F @ q - c
        if float(np.max(np.abs(grad))) < 1e-13:
            break
        Fc = F - (F @ q)[:, None]
        H = (Fc * q) @ Fc.T  # Cov_q[F]  (PD)
        try:
            step = np.linalg.solve(H + 1e-15 * np.eye(K), -grad)
        except np.linalg.LinAlgError:
            return QSolution(q=[], status="INFEASIBLE", reason="singular dual Hessian")
        lam = lam + step

    q = _tilt_q(prior_arr, lam @ F)
    if float(np.max(np.abs(F @ q - c))) > 1e-6:
        return QSolution(q=[], status="INFEASIBLE", reason="dual Newton did not converge")
    return QSolution(q=q.tolist(), status="FEASIBLE", lambdas=lam.tolist())


# ── Edge identity ─────────────────────────────────────────────────────────────

def compute_edge(p_s: list[float], q_s: list[float], X_s: list[float]) -> float:
    """Edge = ⟨p − q, X⟩ = Σ_s (p_s − q_s) X_s. Positive → axis worth more than priced."""
    p = np.array(p_s, dtype=float)
    q = np.array(q_s, dtype=float)
    X = np.array(X_s, dtype=float)
    return float(np.dot(p - q, X))


def _edge_attribution(names, p, q, X_s, *, round_dp: Optional[int] = None) -> list[EdgeContribution]:
    """Per-scenario (p−q)·X attribution, sorted by contribution desc. round_dp rounds the
    stored values (run_pricing persists 6dp; the MC point estimate stays exact)."""
    def v(x: float) -> float:
        return round(x, round_dp) if round_dp is not None else x
    return sorted(
        (EdgeContribution(scenario=names[i], contribution=v((p[i] - q[i]) * X_s[i]),
                          disagreement=v(p[i] - q[i])) for i in range(len(X_s))),
        key=lambda c: c.contribution, reverse=True,
    )


# ── Uncertainty-propagating fair value (Step 3) ──────────────────────────────

def scenario_fair_value(scenarios: list[Scenario]) -> tuple[float, float]:
    """Return (E[X], sqrt(Var[X])) under the scenario mixture.

    Var[X] = Σ_s p_s σ_g_s²              (within-scenario: each X_s uncertain)
           + Σ_s p_s (X_s − E[X])²       (between-scenario: dispersion of fair value)

    Law of total variance. With all σ_g_s = 0 only the between term survives, so the
    std reports how dispersed the axis fair value is across states.
    """
    p = np.array([s.p_s for s in scenarios], dtype=float)
    X = np.array([s.implied_axis_value for s in scenarios], dtype=float)
    sig = np.array([(s.sigma_g_s or 0.0) for s in scenarios], dtype=float)

    fv = float(np.dot(p, X))
    within = float(np.dot(p, sig ** 2))
    between = float(np.dot(p, (X - fv) ** 2))
    return fv, float(np.sqrt(within + between))


# ── Monte-Carlo edge (Step 4) ────────────────────────────────────────────────

class EdgeMC(BaseModel):
    """Edge with second moments. edge_mean is the DETERMINISTIC identity (NOT the MC
    sample mean); MC supplies the rest. See module note on the hybrid SNR."""
    edge_mean: float
    edge_std: float
    snr: float
    p_success: float
    vol_adjusted_edge: float
    direction_ok: bool
    attribution: list[EdgeContribution]
    infeasible_fraction: float


def compute_edge_mc(
    p: list[float],
    X_s: list[float],
    sigma_g: list[float],
    X_mkt: float,
    prior: list[float],
    thesis_sign: int,
    sigma_axis: float,
    n_draws: int = 10_000,
    kappa: float = 1e6,
    seed: int = 0,
    scenario_names: Optional[list[str]] = None,
) -> EdgeMC:
    """Monte-Carlo edge.

    edge_mean = ⟨p − q, X⟩ at the POINT estimates (exactly reproduces residual_edge;
    NOT the MC mean — q is nonlinear in X so by Jensen they differ).

    MC: each draw samples X_s ~ N(X_s, σ_g_s) and p ~ Dirichlet(κ·p), re-solves q via
    the tilt, recomputes the edge. SNR = edge_mean / edge_std (a documented hybrid:
    point-estimate numerator, MC-spread denominator). Infeasible draws (X_mkt outside
    the drawn span) are SKIPPED and COUNTED — never silently dropped.

    Reproducibility: SeedSequence(seed).spawn(n_draws) gives each draw an independent
    stream, so results are identical regardless of execution order (AR-PAR-001).
    """
    n = len(X_s)
    names = scenario_names if scenario_names is not None else [f"s{i}" for i in range(n)]

    # Point-estimate q and the deterministic edge identity + attribution.
    point = solve_q_tilt(X_s, [level_constraint(X_mkt)], prior)
    if point.status != "FEASIBLE":
        raise ValueError(f"base-case pricing infeasible: {point.reason}")
    q_point = point.q
    edge_mean = compute_edge(p, q_point, X_s)

    attribution = _edge_attribution(names, p, q_point, X_s)

    # Monte-Carlo for the second moments.
    p_arr = np.asarray(p, dtype=float)
    X_arr = np.asarray(X_s, dtype=float)
    sig = np.asarray(sigma_g, dtype=float)
    alpha = kappa * p_arr

    edges: list[float] = []
    infeasible = 0
    for child in np.random.SeedSequence(seed).spawn(n_draws):
        rng = np.random.default_rng(child)
        x_draw = rng.normal(X_arr, sig)
        p_draw = rng.dirichlet(alpha)
        sol = solve_q_tilt(x_draw.tolist(), [level_constraint(X_mkt)], prior)
        if sol.status != "FEASIBLE":
            infeasible += 1
            continue
        edges.append(compute_edge(p_draw.tolist(), sol.q, x_draw.tolist()))

    edge_arr = np.asarray(edges, dtype=float)
    edge_std = float(edge_arr.std(ddof=1)) if edge_arr.size > 1 else 0.0
    snr = edge_mean / edge_std if edge_std > 0 else float("inf")
    if edge_arr.size:
        success = np.sum((edge_arr > 0) & (np.sign(edge_arr) == thesis_sign))
        p_success = float(success) / float(edge_arr.size)
    else:
        p_success = 0.0
    vol_adjusted_edge = edge_mean / sigma_axis if sigma_axis > 0 else float("nan")
    direction_ok = bool(edge_mean * thesis_sign > 0)

    return EdgeMC(
        edge_mean=edge_mean,
        edge_std=edge_std,
        snr=snr,
        p_success=p_success,
        vol_adjusted_edge=vol_adjusted_edge,
        direction_ok=direction_ok,
        attribution=attribution,
        infeasible_fraction=infeasible / n_draws,
    )


# ── Pricing assembly ──────────────────────────────────────────────────────────

def run_pricing(
    scenarios: list[Scenario],
    X_mkt: float,
    normal_fv: float,
    q0: Optional[list[float]] = None,
    thesis_sign: Optional[int] = None,
    sigma_axis: Optional[float] = None,
    run_mc: bool = False,
    n_draws: int = 10_000,
    seed: int = 0,
) -> Pricing:
    """Assemble Pricing from scenarios via the closed-form tilt q and the edge identity.

    q0 is the prior (None → uniform). When thesis_sign and sigma_axis are supplied the
    DETERMINISTIC edge enrichments (attribution, direction, vol-adjusted edge, basis,
    q_status) are populated. MC second moments (edge_std, snr, p_success,
    infeasible_fraction) are added only when run_mc=True (the edge is gross of risk
    premium regardless)."""
    p_s = [s.p_s for s in scenarios]
    X_s = [s.implied_axis_value for s in scenarios]
    names = [s.name for s in scenarios]

    if abs(sum(p_s) - 1.0) > 1e-6:
        raise ValueError(f"Scenario probabilities sum to {sum(p_s):.4f}, not 1.0")

    n = len(scenarios)
    prior = q0 if q0 is not None else [1.0 / n] * n
    sol = solve_q_tilt(X_s, [level_constraint(X_mkt)], prior)
    if sol.status != "FEASIBLE":
        raise ValueError(f"pricing infeasible: {sol.reason}")
    q_s = sol.q

    scenario_fv, scenario_fv_std = scenario_fair_value(scenarios)
    edge = compute_edge(p_s, q_s, X_s)

    denom = scenario_fv - normal_fv
    frac = (X_mkt - normal_fv) / denom if abs(denom) > 1e-6 else 0.0

    pricing = Pricing(
        normal_fv=round(normal_fv, 4),
        scenario_fv=round(scenario_fv, 4),
        priced_in=PricedIn(q_s=[round(q, 6) for q in q_s], frac=round(frac, 4)),
        residual_edge=round(edge, 4),
        scenario_fv_std=round(scenario_fv_std, 4),
    )

    # Deterministic edge enrichment (needs the trade direction + axis vol).
    if thesis_sign is not None and sigma_axis is not None:
        pricing.edge_attribution = _edge_attribution(names, p_s, q_s, X_s, round_dp=6)
        pricing.edge_direction_ok = bool(edge * thesis_sign > 0)
        pricing.vol_adjusted_edge = round(edge / sigma_axis, 6) if sigma_axis > 0 else None
        pricing.edge_basis = "gross_of_risk_premium"
        pricing.q_status = "FEASIBLE"

        if run_mc:
            mc = compute_edge_mc(
                p=p_s, X_s=X_s, sigma_g=[s.sigma_g_s or 0.0 for s in scenarios],
                X_mkt=X_mkt, prior=prior, thesis_sign=thesis_sign, sigma_axis=sigma_axis,
                n_draws=n_draws, seed=seed, scenario_names=names,
            )
            pricing.edge_std = round(mc.edge_std, 6)
            pricing.snr = mc.snr
            pricing.p_success = round(mc.p_success, 6)
            pricing.infeasible_fraction = round(mc.infeasible_fraction, 6)

    return pricing
