"""Semantic contract for discovery outputs.

Schema validity is not enough: a JSON-valid Axis that says "5s30s curve steepener" for a
relative-value report is economically WRONG. These checks encode acceptable axis / family
shapes per input kind and return human-readable violations (empty list = passes).

Family expectations are SOURCE-SUGGESTED PRIORS (long_short, index_index_rv, etf_basket_rv,
sector_rotation, …), not the engine's hard router output — the engine only routes
steepener/flattener/long_short/outright/watchlist_only today.
"""
from __future__ import annotations

from typing import Literal

InputKind = Literal["jpm_report", "curve_steepener", "etf_flow", "margin_compression"]


def _norm(s: str) -> str:
    return s.lower().replace("_", " ").replace("-", " ")


def _hit(hints: list[str], items: list[str]) -> bool:
    blob = " | ".join(_norm(i) for i in items)
    return any(h in blob for h in hints)


# Source-derived axis hints per input kind.
JPM_SOURCE_HINTS = ["project", "hyperscaler", "data center", "technology",
                    "index includ", "hpc", "basis", "weight", "stw"]
CURVE_HINTS = ["5s30s", "5s10s", "curve", "steepen", "flatten", "slope"]
ETF_AXIS_HINTS = ["etf premium", "etf discount", "premium discount", "create", "redeem",
                  "basket oas", "basket residual", "nav", "etf vs basket", "etf basket"]
MARGIN_AXIS_HINTS = ["margin", "pricing power", "input cost", "sector spread", "dispersion"]

# Curve-required follow-up questions (test 2): a curve thesis must still ask for these.
CURVE_REQUIRED_QUESTIONS = ["issuer universe", "maturity", "curve", "fair"]


def _is_curve_axis(axis: str) -> bool:
    return _hit(CURVE_HINTS, [axis])


def _ranks_above(families: list[str], a: str, bs: list[str]) -> bool:
    """True if family `a` is present and ranked strictly above every present family in `bs`."""
    fn = [_norm(f) for f in families]
    a = _norm(a)
    if a not in fn:
        return False
    ai = fn.index(a)
    return all(_norm(b) not in fn or ai < fn.index(_norm(b)) for b in bs)


def check_axis_contract(
    kind: InputKind,
    axes: list[str],
    families: list[str],
    missing_data: list[str] | None = None,
) -> list[str]:
    """Return a list of semantic violations (empty ⇒ output is economically sensible)."""
    axes = list(axes or [])
    families = list(families or [])
    missing_data = list(missing_data or [])
    v: list[str] = []

    if kind == "jpm_report":
        if not _hit(JPM_SOURCE_HINTS, axes):
            v.append("jpm_report: no source-derived axis (project/hyperscaler basis, "
                     "Data Centers vs Technology, index-inclusion basis, or HPC vs HY).")
        # generic curve must not be the SOLE top axis
        non_curve = [a for a in axes if not _is_curve_axis(a)]
        if axes and _is_curve_axis(axes[0]) and not non_curve:
            v.append("jpm_report: generic curve steepener is the only axis — expected "
                     "source-derived RV/basis axes for this report.")
        if families[:1] and _norm(families[0]) == "outright" and not _hit(
            ["downstream beta", "beta model", "requires downstream"], families):
            v.append("jpm_report: outright is the top family without a "
                     "'requires downstream beta model' caveat.")

    elif kind == "curve_steepener":
        if not _hit(CURVE_HINTS, axes):
            v.append("curve_steepener: expected a curve/slope axis (5s30s, 5s10s, …).")
        # must still demand the trade-readiness inputs before any legs
        if not all(_hit([q], missing_data) for q in CURVE_REQUIRED_QUESTIONS):
            v.append("curve_steepener: must still ask for issuer universe, maturity bucket, "
                     "current curve, and a fair-value model before trade readiness.")

    elif kind == "etf_flow":
        if not _hit(ETF_AXIS_HINTS, axes):
            v.append("etf_flow: expected an ETF premium/discount, create/redeem, basket-OAS "
                     "residual, or ETF-vs-basket basis axis.")
        if not _ranks_above(families, "etf_basket_rv", ["curve", "outright"]):
            v.append("etf_flow: etf_basket_rv must rank above curve and outright.")

    elif kind == "margin_compression":
        if not _hit(MARGIN_AXIS_HINTS, axes):
            v.append("margin_compression: expected a margin-sensitivity, pricing-power, "
                     "input-cost-beta, or sector-spread-dispersion axis.")
        if not (_ranks_above(families, "long_short", ["cash_cds_basis"])
                or _ranks_above(families, "sector_rotation", ["cash_cds_basis"])):
            v.append("margin_compression: long_short or sector_rotation must rank above cash_cds_basis.")
    else:
        v.append(f"unknown input kind {kind!r}")
    return v


def validate_discovery_output(theme, input_kind: InputKind | None = None) -> list[str]:
    """The AUTOMATIC gate run on every live discovery output BEFORE a FreshReasoningSnapshot.

    Always fails closed on trade-leg / sizing / expression leakage; additionally checks the
    axis/family contract when the input kind is known (skipped for a blocked HALT, which
    deliberately carries no axis). Returns violations (empty ⇒ safe to freeze).
    """
    v: list[str] = []
    # trade-leakage gates — discovery must NEVER carry pricing / sizing / detailed expressions
    if getattr(theme, "pricing", None) is not None:
        v.append("trade_leakage: pricing present in a discovery output")
    if getattr(theme, "sizing", None) is not None:
        v.append("trade_leakage: sizing present in a discovery output")
    if getattr(theme, "expressions", None):
        v.append("trade_leakage: detailed expressions present in a discovery output")
    if getattr(theme, "status", None) == "expression_complete":
        v.append("expression_leakage: discovery produced an expression_complete object")

    # axis/family contract — only when the axis exists and the input kind is known
    if getattr(theme, "status", None) != "blocked" and input_kind is not None \
            and getattr(theme, "axis", None) is not None:
        axes = [theme.axis.definition]
        families = [f.family for f in theme.strategy_families]
        missing = [getattr(f, "data_needed_next", "") or "" for f in theme.strategy_families]
        if getattr(theme, "loop_diagnosis", None) is not None:
            missing += list(theme.loop_diagnosis.pm_questions)
        v += check_axis_contract(input_kind, axes, families, missing_data=missing)
    return v
