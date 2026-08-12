"""L4 — the weekly theme book. SCAFFOLD: types are real, the renderers are stubs.

The read cadence already exists (`breach_obs_freq="weekly"`). The ARTIFACT does not — so
lifecycle states live in a database and the human never sees a theme quietly go stale. This is
the thing a PM opens on Monday (D-L4-1: Monday morning, private, just the PM).

**No new inference, ever.** The book renders stored state. It never calls an LLM and never
recomputes a status. If the book and the state machine disagree, the book is wrong. No provider
is constructed anywhere in this call path, and the test asserts it.

Deterministic: same inputs and same `as_of` give a byte-identical render, so it is testable by
golden file. `as_of` is passed in; the renderer never reads the clock (I8). Ordering is by
explicit sort key, never by set or dict iteration order.

Sections, most decision-relevant first:

  0. **Regime backdrop** — A1's reading, what changed from last week, and a stale banner when
     A1 abstained.
  1. **Needs a decision** — `falsified_pending` with days left, and horizons expiring inside
     30 days. The only section meant to prompt action.
  2. **Changed since last week** — transitions with the triggering evidence and its L2
     `surprise_z`.
  3. **Live book** — armed / confirming / weakening / stalled, one line each.
  4. **Closed this week** — terminal transitions, one-line outcome, link to the pack.
  5. **Scorecard** — the L3 roll-up, trailing twelve months.

Discovery discipline: no legs, no sizing, no hedge ratios, no execution — strategy families
only, exactly as everywhere else in the engine.

Not to be confused with `engine/ledger/lifecycle.py`.
"""
from __future__ import annotations

from typing import Optional, Sequence

from pydantic import BaseModel, ConfigDict

from .decisions import BOOK_RECIPIENTS, BOOK_RENDER_WEEKDAY, LIFECYCLE_DECISIONS_VERSION
from .evidence_pack import EvidencePack
from .regime import RegimeVocabulary
from .scorecard import Scorecard
from .theme_view import ThemeView

BOOK_CONTRACT: str = "themebook/1"


class BookSection(BaseModel):
    """One rendered section. `lines` are pre-sorted so the render is byte-stable."""

    model_config = ConfigDict(frozen=True)

    key: str
    title: str
    lines: tuple[str, ...] = ()
    #: True when the section is empty on purpose. An empty week renders without error, and an
    #: empty "Needs a decision" is good news that should still be shown.
    empty: bool = False


class ThemeBook(BaseModel):
    """The Monday artifact. A render of stored state and nothing else."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    contract_version: str = BOOK_CONTRACT
    decisions_version: str = LIFECYCLE_DECISIONS_VERSION
    as_of: str                                    # supplied, never the clock (I8)
    weekday: str = BOOK_RENDER_WEEKDAY
    recipients: tuple[str, ...] = BOOK_RECIPIENTS
    sections: tuple[BookSection, ...] = ()
    #: A1 blocked, so the regime backdrop is last week's. Rendered as a banner — a stale but
    #: honest book beats a fresh but fabricated one.
    stale_assessment: bool = False
    no_trade_confirmation: str = (
        "Weekly theme book: lifecycle states, transitions and the scorecard. No trades, legs, "
        "sizing, hedge ratios, or execution."
    )


def render_week(
    *,
    as_of: str,
    views: Sequence[ThemeView],
    previous_views: Sequence[ThemeView] = (),
    closed_packs: Sequence[EvidencePack] = (),
    scorecard: Optional[Scorecard] = None,
    regimes: Optional[RegimeVocabulary] = None,
    previous_regimes: Optional[RegimeVocabulary] = None,
) -> ThemeBook:
    """Build the week's book from stored state. Pure, deterministic, no provider, no clock.

    TODO(L4): build the six sections in order; diff `views` against `previous_views` for the
    changed section; set `stale_assessment` from `regimes.stale_regime`; sort every section's
    lines by an explicit key so the golden file is stable.
    """
    raise NotImplementedError("L4 render_week — scaffold only, no implementation yet")


def to_markdown(book: ThemeBook) -> str:
    """Render the book as markdown, mirroring `thesis_tracker.export_thesis_tracker_markdown`.

    TODO(L4): emit one heading per section and the pre-sorted lines beneath it. Same book in,
    byte-identical string out.
    """
    raise NotImplementedError("L4 to_markdown — scaffold only, no implementation yet")
