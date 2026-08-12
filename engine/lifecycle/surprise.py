"""L2 — surprise-vs-level scoring. SCAFFOLD: types are real, the functions are stubs.

**The failure this prevents.** Today an evidence atom carrying a number counts the same whether
it *surprised* or merely *restated a known level*. Spreads are wide; every weekly print says
spreads are wide; eight confirming prints read as accumulating evidence when it is one fact
counted eight times. Surveillance §5.9 gate 3 separates *attention* from *evidence*; this
separates *level* from *change* inside evidence itself.

Rules, deterministic, consumed by the §5.3 transition function:

  * `kind="surprise"` with `|surprise_z|` above threshold MAY move status.
  * `kind="level"` CANNOT move status toward `confirming`. It sustains `armed`, and it still
    counts for staleness — a level print is a heartbeat: the series is alive.
  * No expectation available ⇒ `kind="level"`. Absence of an expectation is never surprise.
  * N consecutive same-signed level prints contribute the weight of ONE.

Fail-closed (D-L2-1): if `expected` cannot be tied to a grounded source span, `surprise` is not
computed. It is never estimated by the model.

**Boundary.** This module wraps numeric provenance, it does not extend it. `engine/grounding/`
is agent 2's; `NumericContext` references the expectation's span by id and never re-declares a
grounding type.

Not to be confused with `engine/ledger/lifecycle.py`.
"""
from __future__ import annotations

from datetime import date
from typing import Literal, Optional, Protocol, Sequence

from pydantic import BaseModel, ConfigDict

from .decisions import LIFECYCLE_DECISIONS_VERSION

NumericKind = Literal["level", "change", "surprise"]

#: D-L2-1's tiers, in precedence order, plus the honest third state.
ExpectationTier = Literal["grounded_consensus", "prior_print", "none"]


class ExpectationSource(Protocol):
    """Supplies the expectation a realized number is compared against (D-L2-1).

    Returns ``(expected_value, grounding_span_id)`` or ``None``. The span id is mandatory on a
    hit: an expectation that cannot be tied to a grounded source span is not an expectation,
    and the caller must fall back to ``kind="level"`` rather than let a model estimate one.
    """

    def expectation_for(self, series: str, as_of: date) -> Optional[tuple[float, str]]: ...


class NumericContext(BaseModel):
    """One number, classified. `realized` is the only required value — everything downstream
    of an expectation is `Optional` because there may be no expectation to have."""

    model_config = ConfigDict(frozen=True)

    decisions_version: str = LIFECYCLE_DECISIONS_VERSION
    series: str
    observed_at: date
    realized: float
    expected: Optional[float] = None
    #: Must itself be a grounded span (harness G1). `None` whenever `expected` is `None`.
    expected_source_span_id: Optional[str] = None
    expected_tier: ExpectationTier = "none"
    surprise: Optional[float] = None              # realized - expected, harness-computed
    surprise_z: Optional[float] = None            # scaled by trailing dispersion of the series
    #: Defaults to the weakest classification. A number is a level until something proves it
    #: is a surprise, never the other way round.
    kind: NumericKind = "level"
    #: How many identical same-signed level prints this one stands for after collapsing. One
    #: fact counted eight times must contribute the weight of one.
    collapsed_count: int = 1


def classify_number(
    realized: float,
    *,
    series: str,
    observed_at: date,
    source: Optional[ExpectationSource] = None,
    trailing_dispersion: Optional[float] = None,
) -> NumericContext:
    """Classify one realized number as level, change or surprise.

    TODO(L2): consult `source` in tier order; on a hit with a span id, compute
    `surprise = realized - expected` and, when `trailing_dispersion` is present and non-zero,
    `surprise_z`. On a miss, or on a hit without a span id, return `kind="level"` with
    `expected=None` — do not estimate.
    """
    raise NotImplementedError("L2 classify_number — scaffold only, no implementation yet")


def collapse_levels(contexts: Sequence[NumericContext]) -> tuple[NumericContext, ...]:
    """Collapse runs of identical same-signed level prints into one weighted entry.

    TODO(L2): group consecutive `kind="level"` entries on the same series with the same sign,
    emit one context per run carrying `collapsed_count`, and pass surprises through untouched.
    """
    raise NotImplementedError("L2 collapse_levels — scaffold only, no implementation yet")
