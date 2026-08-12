"""L5 — factor projection and the expression gate. SCAFFOLD: types are real, logic is stubbed.

The `factor-r2-router` skill card exists but is *"readable in discovery but not auto-wired"*,
so the question it is built to answer — *is this expression harvesting a known risk premium, or
is it actually our thesis?* — is currently answered by nobody.

**The two-part gate**, deterministic, before any expression is proposed:

    Alive           surveillance_status in {armed, confirming}. Not weakening, stalled,
                    falsified_pending, and obviously not terminal.
    Tractable       residual_alpha_share >= RESIDUAL_ALPHA_THRESHOLD (0.40, D-L5-1) AND no
                    unresolved premium-overlap flag. A theme A2 already marked
                    rv_layer_status="disabled" short-circuits without recomputing.

Both true ⇒ strategy families may be proposed and ranked. Either false ⇒ no expression, with
the reason recorded (`not_alive:<status>` / `not_tractable:<flag>`). **A theme can be perfectly
true and still fail this gate** — that is the point. The output is "real but not expressible
right now."

Fail-closed: missing factor data returns *not tractable*. Absence of evidence about factor
overlap is never read as absence of overlap.

**Why the gate takes primitives, not a `ThemeView`.** `ThemeView` would otherwise need to embed
`FactorDecomposition` while this module reads a `ThemeView` — a cycle. Taking the status string
and the decomposition directly breaks it and makes the gate testable without building a view.

**Boundary, unchanged.** This stops at ranked strategy families. Legs, sizes and hedge ratios
stay fenced in expression mode. The card's `not_allowed_to_influence` list is binding: factor
projection must not touch scenario probabilities `p_s`, golden-master numbers, the rho-squared
cap math, the `q`-tilt, or `residual_edge`.

Not to be confused with `engine/ledger/lifecycle.py`.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from .decisions import (
    ALIVE_STATUSES,
    LIFECYCLE_DECISIONS_VERSION,
    RESIDUAL_ALPHA_THRESHOLD,
)

FACTOR_CONTRACT: str = "factordecomp/1"


class PremiumOverlapFlag(BaseModel):
    """A named risk premium this expression may simply be harvesting. `resolved=False` closes
    the gate on its own, regardless of the residual-alpha share."""

    model_config = ConfigDict(frozen=True)

    premium: str                                  # e.g. "carry_roll_down", "broad_credit_beta"
    loading: Optional[float] = None
    resolved: bool = False
    note: str = ""


class FactorDecomposition(BaseModel):
    """The skill card's declared output objects, typed. Every share is `Optional`: a
    `residual_alpha_share` of 0.0 asserts the expression is pure premium harvest, which is a
    finding — not the same as having no factor data at all."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    contract_version: str = FACTOR_CONTRACT
    decisions_version: str = LIFECYCLE_DECISIONS_VERSION
    theme_id: str
    as_of: str                                    # supplied, never the clock (I8)
    factor_loadings: dict[str, float] = Field(default_factory=dict)
    harvested_premium_share: Optional[float] = None
    residual_alpha_share: Optional[float] = None
    purity_estimate: Optional[float] = None
    premium_overlap_flags: tuple[PremiumOverlapFlag, ...] = ()
    #: True when this refined an A2 `FactorMap` rather than recomputing from scratch — inputs
    #: already reviewed at inference time are not re-graded per PR.
    refined_from_factor_map: bool = False
    #: Named when the decomposition could not be computed, so the gate can close for a stated
    #: reason instead of on a silent `None`.
    insufficient_data_reason: Optional[str] = None


class GateDecision(BaseModel):
    """The gate's verdict. `allowed=False` always carries a `reason`; a closed gate with no
    stated reason is the failure this whole layer exists to prevent."""

    model_config = ConfigDict(frozen=True)

    theme_id: str
    allowed: bool
    #: e.g. "not_alive:weakening", "not_tractable:no_factor_data",
    #: "not_tractable:premium_overlap:carry_roll_down"
    reason: Optional[str] = None
    alive: Optional[bool] = None
    tractable: Optional[bool] = None
    residual_alpha_share: Optional[float] = None
    threshold: float = RESIDUAL_ALPHA_THRESHOLD


def decompose(
    *,
    theme_id: str,
    as_of: str,
    factor_loadings: Optional[dict[str, float]] = None,
    thesis_axis: Optional[str] = None,
    factor_premia: Optional[dict[str, float]] = None,
    prior_factor_map: Optional[object] = None,
) -> FactorDecomposition:
    """Split an expression's exposure into harvested premium versus residual alpha.

    TODO(L5): where `prior_factor_map` (an A2 `FactorMap`) is supplied, REFINE it and set
    `refined_from_factor_map`; otherwise decompose from `factor_loadings` and `factor_premia`.
    With insufficient data, return every share `None` and set `insufficient_data_reason` — do
    not return zeros.
    """
    raise NotImplementedError("L5 decompose — scaffold only, no implementation yet")


def expression_gate(
    *,
    theme_id: str,
    surveillance_status: Optional[str],
    decomposition: Optional[FactorDecomposition] = None,
    rv_layer_status: Literal["enabled", "disabled", "undetermined"] = "undetermined",
    threshold: float = RESIDUAL_ALPHA_THRESHOLD,
) -> GateDecision:
    """The two-part alive-and-tractable gate. Deterministic; runs before any expression exists.

    TODO(L5): close on `surveillance_status not in ALIVE_STATUSES` — including `None`, since a
    theme with no watch is not known to be alive. Short-circuit to not-tractable when
    `rv_layer_status == "disabled"`. Otherwise require a `residual_alpha_share` at or above
    `threshold` and no unresolved `premium_overlap_flags`. Always state the reason.
    """
    raise NotImplementedError("L5 expression_gate — scaffold only, no implementation yet")
