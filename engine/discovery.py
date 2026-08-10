"""Discovery half — route a causal object's promoted theme to ONE strategy FAMILY."""
from __future__ import annotations

from typing import Literal, Optional, Union

import numpy as np

from .engine2 import compute_edge, level_constraint, solve_q_tilt
from .scoring import compute_purity
from .schema import Axis, ConfidenceComponents, Scenario, StrategyFamilyRec

AxisShape = Literal["level", "curve", "basis", "relative_value", "cross_asset", "volatility"]
AxisDirection = Literal[
    "higher", "lower", "steeper", "flatter", "wider", "tighter",
    "dispersion_up", "dispersion_down",
]

# Keyword signatures for axis-shape detection, in priority order (first match wins).
_VOL_KEYS = ("vol", "convexity", "swaption", "payer", "receiver", "gamma", "vega")
_BASIS_KEYS = ("basis", "cash-cds", "cash vs cds", "bond-cds", "cds vs cash", "asset swap")
_CROSS_ASSET_KEYS = ("vs equity", "credit vs equity", "vs rates", "vs treasury",
                     "credit vs rates", "equity")
_CURVE_KEYS = ("slope", "5s30s", "2s10s", "2s5s", "10s30s", "steepen", "flatten", "curve")
_RELATIVE_KEYS = ("−", " minus ", " vs ", "differential", "spread between", "basket")

# Relative-value SUB-TYPE signatures — checked ONLY inside the relative_value branch (the axis
# SHAPE stays relative_value, direction wider/tighter; these only refine WHICH RV family it is,
# mirroring the cross_asset equity/rates split). Most-specific vocabulary wins; a plain
# name-vs-name pair falls through to long_short. Deliberately avoids bare "senior"/"sub" so a
# senior-bank-vs-sovereign pair stays long_short, not capital_structure.
_ETF_KEYS = ("etf", "nav", "net asset value", "creation/redemption", "creation unit",
             "lqd", "hyg", "jnk", "ishares")
_CAPSTRUCT_KEYS = ("subordinated", "subordination", "sub-senior", "senior-sub", "senior vs sub",
                   "sub vs senior", "at1", "additional tier 1", "tier 2", "hybrid",
                   "holdco vs opco", "opco vs holdco", "capital structure")
_INDEX_INDEX_KEYS = ("on-the-run vs off-the-run", "otr vs off-the-run", "series roll",
                     "index roll", "old series vs new", "index vs index")

# (shape, direction) → strategy family. direction enters only where it disambiguates.
_ROUTE: dict[tuple[str, str], str] = {
    ("curve", "steeper"): "steepener",
    ("curve", "flatter"): "flattener",
}

# Per-family axis_fit: how DIRECTLY the family expresses the axis shape (a blunt outright
# tracks a level less cleanly than a curve trade tracks a slope).
_AXIS_FIT: dict[str, float] = {
    "steepener": 1.0, "flattener": 1.0, "long_short": 1.0, "cash_cds_basis": 1.0,
    "etf_basket_rv": 0.95, "index_index_rv": 0.95, "capital_structure": 0.9,
    "credit_vs_equity": 0.9, "credit_vs_rates": 0.9, "volatility_convexity": 0.9,
    "outright": 0.7, "watchlist_only": 0.0,
}

# Per-family TRACKING FIDELITY: how cleanly the family's legs isolate the axis (1.0 = the
# expression IS the axis; < 1 = basis/leg residual leaks in). Used to build an imperfect
# monetisation series so `purity` (R² of that series on the axis moves) genuinely varies.
_TRACKING_FIDELITY: dict[str, float] = {
    "steepener": 0.95, "flattener": 0.95, "long_short": 0.90, "cash_cds_basis": 0.85,
    "etf_basket_rv": 0.85, "outright": 0.80, "index_index_rv": 0.80, "capital_structure": 0.80,
    "credit_vs_rates": 0.75, "credit_vs_equity": 0.70,
    "volatility_convexity": 0.65, "watchlist_only": 0.0,
}

def _family_monetisation(axis_moves: list[float], fidelity: float) -> list[float]:
    """The family's per-scenario P&L: ``fidelity·(axis move) + (1−fidelity)·residual`` where"""
    x = np.asarray(axis_moves, dtype=float)
    if x.size < 2 or float(x.std()) < 1e-12 or fidelity >= 1.0:
        return x.tolist()
    xc = x - x.mean()
    b = np.array([(-1.0) ** i for i in range(x.size)])      # base, then Gram-Schmidt ⟂ {1, x}
    b = b - b.mean()
    b = b - (b @ xc) / (xc @ xc) * xc
    if float(np.linalg.norm(b)) < 1e-12:
        return x.tolist()
    b = b / b.std() * x.std()                                # match the axis-move variance
    return (fidelity * x + (1.0 - fidelity) * b).tolist()

# What each family needs DOWNSTREAM (out of discovery scope) to become legs.
_DOWNSTREAM: dict[str, tuple[str, str]] = {
    "steepener": ("curve construction + DV01-neutral leg ratios",
                  "live per-tenor OAS, basket constituents, per-tenor DV01"),
    "flattener": ("curve construction + DV01-neutral leg ratios",
                  "live per-tenor OAS, basket constituents, per-tenor DV01"),
    "long_short": ("pair construction + beta/notional neutralisation",
                   "live spreads on both legs, beta, borrow/financing"),
    "cash_cds_basis": ("cash-CDS basis construction",
                       "bond asset-swap spread, matched-tenor CDS, repo/financing"),
    "credit_vs_equity": ("cross-asset hedge-ratio model",
                         "credit-equity betas, live credit + equity/vol levels"),
    "credit_vs_rates": ("cross-asset duration/hedge-ratio model",
                        "asset-swap/z-spread, live rates, DV01 map"),
    "volatility_convexity": ("option structure + greeks",
                             "implied vol surface, option chain, skew"),
    "etf_basket_rv": ("ETF vs underlying-basket / NAV construction",
                      "ETF price + NAV, basket constituents/weights, create/redeem mechanics"),
    "capital_structure": ("intra-issuer subordination pair construction (subordination-adjusted ratios)",
                          "per-tranche spreads (senior/sub/AT1/hybrid), recovery & subordination "
                          "assumptions, matched-tenor financing"),
    "index_index_rv": ("matched-exposure construction across index definitions",
                       "same-name spread in each index, index-tracking AUM by family, inclusion rules"),
    "outright": ("instrument selection + sizing",
                 "live level, instrument liquidity, carry"),
    "watchlist_only": ("(none — not tradable yet)",
                       "an operational axis, supplied scenarios, and a falsifier"),
}

def classify_axis(
    axis: Axis, thesis_sign: int
) -> tuple[AxisShape, AxisDirection]:
    """Resolve (shape, direction): use the axis's own typed fields when set, else derive"""
    shape: AxisShape = axis.axis_shape or _shape_from_text(axis)
    if axis.axis_direction is not None:
        return shape, axis.axis_direction
    return shape, _direction_from_sign(shape, thesis_sign)

def _shape_from_text(axis: Axis) -> AxisShape:
    text = f"{axis.definition} {axis.measurement}".lower()
    if any(k in text for k in _VOL_KEYS):
        return "volatility"
    if any(k in text for k in _BASIS_KEYS):
        return "basis"
    if any(k in text for k in _CROSS_ASSET_KEYS):
        return "cross_asset"
    if any(k in text for k in _CURVE_KEYS):
        return "curve"
    if any(k in text for k in _RELATIVE_KEYS):
        return "relative_value"
    return "level"

def _direction_from_sign(shape: AxisShape, thesis_sign: int) -> AxisDirection:
    up = thesis_sign >= 0
    return {
        "curve": "steeper" if up else "flatter",
        "level": "higher" if up else "lower",
        "relative_value": "wider" if up else "tighter",
        "basis": "wider" if up else "tighter",
        "cross_asset": "wider" if up else "tighter",
        "volatility": "dispersion_up" if up else "dispersion_down",
    }[shape]

def _route_family(shape: AxisShape, direction: AxisDirection, axis: Axis) -> str:
    """Map (shape, direction) to one strategy family."""
    if (shape, direction) in _ROUTE:
        return _ROUTE[(shape, direction)]
    if shape == "relative_value":
        return _relative_value_subtype(axis)
    if shape == "basis":
        return "cash_cds_basis"
    if shape == "volatility":
        return "volatility_convexity"
    if shape == "cross_asset":
        text = f"{axis.definition} {axis.measurement}".lower()
        return "credit_vs_equity" if "equity" in text else "credit_vs_rates"
    return "outright"  # level (and any curve direction not steeper/flatter)

def _relative_value_subtype(axis: Axis) -> str:
    """Refine a relative_value axis into a concrete RV family (mirrors the cross_asset split).

    Most-specific vocabulary wins; a plain name-vs-name pair falls through to long_short. An
    index-vs-index axis is also recognised when two index families co-occur (e.g. CDX & iTraxx).
    """
    text = f"{axis.definition} {axis.measurement}".lower()
    if any(k in text for k in _ETF_KEYS):
        return "etf_basket_rv"
    if any(k in text for k in _CAPSTRUCT_KEYS):
        return "capital_structure"
    if any(k in text for k in _INDEX_INDEX_KEYS) or ("cdx" in text and "itraxx" in text):
        return "index_index_rv"
    return "long_short"

def _light_residual_edge(
    scenarios: list[Scenario], prior: list[float], x_mkt: float
) -> tuple[Optional[float], float]:
    """Residual edge ⟨p−q, X⟩ via the max-entropy tilt, and the scenario span. Returns"""
    X_s = [s.implied_axis_value for s in scenarios]
    p = [s.p_s for s in scenarios]
    span = max(X_s) - min(X_s)
    sol = solve_q_tilt(X_s, [level_constraint(x_mkt)], prior)
    if sol.status != "FEASIBLE":
        return None, span
    return compute_edge(p, sol.q, X_s), span

def _data_confidence(scenario_availability: bool, priced_in_available: bool,
                     n_scenarios: int) -> float:
    """Data sufficiency in [0,1]. Weak (0.5) when scenarios/pricing are missing — the
    ceiling caps do the hard 'unanswerable' work; the factor only grades richness."""
    if not scenario_availability or not priced_in_available:
        return 0.5
    return min(1.0, n_scenarios / 4.0)

def select_strategy_families(
    axis: Optional[Axis],
    scenarios: list[Scenario],
    prior: list[float],
    thesis_sign: int,
    x_mkt: Optional[float],
    *,
    has_operational_axis: bool = True,
    has_market_value: bool = True,
    causal_confidence: float = 1.0,
    probability_quality: float = 1.0,
) -> list[StrategyFamilyRec]:
    """Route the promoted theme's axis to one strategy family with decomposed confidence.
    probability_quality (Q4) floors data_confidence — weak p_s provenance caps the family."""
    if axis is None or not has_operational_axis:
        return []

    shape, direction = classify_axis(axis, thesis_sign)
    family = _route_family(shape, direction, axis)

    scenario_availability = bool(scenarios)
    market_value_known = has_market_value and x_mkt is not None

    # Light priced-in edge (only when both scenarios AND a market value exist).
    priced_in_available = scenario_availability and market_value_known
    edge_value: Optional[float] = None
    span = 0.0
    if priced_in_available:
        edge_value, span = _light_residual_edge(scenarios, prior, x_mkt)
        if edge_value is None:           # infeasible tilt → priced-in unavailable
            priced_in_available = False

    # ── the six confidence components ────────────────────────────────────────
    axis_fit = _AXIS_FIT.get(family, 0.8)
    data_confidence = min(
        _data_confidence(scenario_availability, priced_in_available, len(scenarios)),
        probability_quality,   # Q4: weak probability provenance caps the data half
    )

    fidelity = _TRACKING_FIDELITY.get(family, 0.8)
    if priced_in_available:
        # directional edge survival: thesis-aligned residual edge over the scenario span.
        edge_thesis = edge_value * thesis_sign
        edge_survival: Union[float, str] = (
            0.0 if span <= 0 else max(0.0, min(1.0, edge_thesis / span))
        )
        X_s = [s.implied_axis_value for s in scenarios]
        axis_moves = [x - x_mkt for x in X_s]
        # R² of the family's IMPERFECT monetisation on the axis moves (not a copy of them).
        purity = compute_purity(_family_monetisation(axis_moves, fidelity), axis_moves)
    else:
        edge_survival = "unknown"               # cannot run solve_q_tilt/compute_edge
        purity = fidelity                       # no scenarios: fall back to structural fidelity

    # ── ceilings (lowest applicable) — encode "unanswerable" ─────────────────
    ceilings: list[tuple[float, str]] = []
    if not scenario_availability:
        ceilings.append((0.45, "no supplied scenarios (not invented): ceiling 0.45"))
    if not market_value_known or not priced_in_available:
        reason = ("no current market value: edge_survival unknown, ceiling 0.60"
                  if not market_value_known else
                  "priced-in unavailable (infeasible tilt): edge_survival unknown, ceiling 0.60")
        ceilings.append((0.60, reason))
    ceiling, why_not = min(ceilings, key=lambda c: c[0]) if ceilings else (1.0, None)

    edge_num = edge_survival if isinstance(edge_survival, (int, float)) else 1.0
    product = causal_confidence * axis_fit * edge_num * purity * data_confidence
    confidence = max(0.0, min(product, ceiling))

    components = ConfidenceComponents(
        causal_confidence=causal_confidence,
        axis_fit=axis_fit,
        edge_survival=edge_survival,
        purity=purity,
        data_confidence=data_confidence,
        scenario_availability=scenario_availability,
    )

    # Route, don't fail: nothing clears ⇒ watchlist_only with the reason named.
    if confidence <= 0.0:
        wl_reason = why_not or (
            "no surviving edge — the directional view is already priced in"
            if priced_in_available else "insufficient inputs to assess tradability"
        )
        model, data_next = _DOWNSTREAM["watchlist_only"]
        return [StrategyFamilyRec(
            family="watchlist_only",
            direction=direction,
            rationale=(
                f"axis ({shape}, {direction}) routes to {family}, but nothing cleared "
                "confidence — held on the watchlist."
            ),
            confidence=0.0,
            why_not=wl_reason,
            required_downstream_model=model,
            data_needed_next=data_next,
            confidence_components=components,
        )]

    model, data_next = _DOWNSTREAM.get(family, ("downstream model TBD", "live data TBD"))
    return [StrategyFamilyRec(
        family=family,
        direction=direction,
        rationale=(
            f"axis shape '{shape}', direction '{direction}' → {family}; "
            f"confidence = causal {causal_confidence:.2f} × axis_fit {axis_fit:.2f} × "
            f"edge {edge_num:.2f} × purity {purity:.2f} × data {data_confidence:.2f}"
        ),
        confidence=confidence,
        why_not=why_not,
        required_downstream_model=model,
        data_needed_next=data_next,
        confidence_components=components,
    )]
