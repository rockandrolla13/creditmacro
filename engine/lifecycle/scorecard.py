"""L3b — the cross-theme scorecard. SCAFFOLD: types are real, `compute_scorecard` is a stub.

Computed from evidence packs, never hand-maintained. Separate from `evidence_pack` because the
two change for different reasons and at different cadences: a pack is immutable and written
once at a terminal transition, while the scorecard is a recomputed roll-up whose metric
definitions will iterate — and it is allowed to lag without the system being invalid.

The two metrics that matter:

  * **View contribution** — mean `delta_rank` / `delta_edge` from the no-view twin on winners
    versus losers. It answers "is the model adding anything?" with realized outcomes rather
    than self-assessment. It is `None` today because the no-view twin (harness §7) is unbuilt,
    and `None` is the honest answer.
  * **Evidence thinness** — median grounded-atom count per terminal theme, split by outcome.
    If losses correlate with thin evidence that is actionable; if they do not, the process
    rather than the sourcing is what needs work.

Every metric is `Optional`. A hit rate over zero closed themes is not 0.0, it is unknown, and
a scorecard that renders "0%" on an empty corpus would be read as a track record.

Not to be confused with `engine/ledger/lifecycle.py`.
"""
from __future__ import annotations

from typing import Optional, Sequence

from pydantic import BaseModel, ConfigDict, Field

from .decisions import LIFECYCLE_DECISIONS_VERSION
from .evidence_pack import EvidencePack

SCORECARD_CONTRACT: str = "scorecard/1"


class Scorecard(BaseModel):
    """The trailing roll-up. Recomputes identically from packs alone — no other input."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    contract_version: str = SCORECARD_CONTRACT
    decisions_version: str = LIFECYCLE_DECISIONS_VERSION
    as_of: str                                    # supplied, never the clock (I8)
    window_months: int = 12
    packs_considered: int = Field(default=0, ge=0)

    #: played_out / (played_out + falsified + horizon_expired). None on an empty corpus.
    hit_rate: Optional[float] = None
    #: Median days to terminal, by terminal state, versus the forward horizon.
    median_days_to_terminal: dict[str, float] = Field(default_factory=dict)
    #: Share of `falsified` where the pre-registered falsifier fired BEFORE the P&L did.
    falsifier_quality: Optional[float] = None
    #: Share of `horizon_expired` — a high rate means themes are written without a clock.
    expiry_rate: Optional[float] = None
    #: Mean no-view-twin deltas on winners vs losers. `None` until harness §7 lands.
    view_contribution_winners: Optional[float] = None
    view_contribution_losers: Optional[float] = None
    #: Median grounded-atom count per terminal theme, keyed by outcome.
    evidence_thinness: dict[str, float] = Field(default_factory=dict)
    #: Metric names that could not be computed, and why they are absent rather than zero.
    unavailable: tuple[str, ...] = ()


def compute_scorecard(
    packs: Sequence[EvidencePack],
    *,
    as_of: str,
    window_months: int = 12,
) -> Scorecard:
    """Roll packs up into the cross-theme scorecard. Pure and deterministic.

    TODO(L3): filter to the trailing window, compute each metric, and leave a metric `None`
    plus named in `unavailable` whenever its denominator is zero or its input is unbuilt.
    Same packs and same `as_of` must give an identical scorecard.
    """
    raise NotImplementedError("L3 compute_scorecard — scaffold only, no implementation yet")
