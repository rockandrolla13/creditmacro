"""L1 — the `ThemeView` contract. SCAFFOLD: types are real, `project` is not implemented.

**The problem.** Four consumers read a theme today — surveillance, the PM memo, the tracker,
and (soon) the weekly book. Each reaches directly into `ThemeObject` fields plus, separately,
into the surveillance annotation stream and the ledger. Nothing names *what a downstream
reader is allowed to see*, so every new consumer widens the coupling and every rename is a
four-place change.

**What this is NOT.** It is not a projection of `AnalystThemeMap`. Compression sits UPSTREAM
of `ThemeObject` — it decides which themes exist. `ThemeView` sits DOWNSTREAM — it presents a
theme that already exists. They are at different points in the pipe and must not be merged.
The overlap with compression is real but lands on A2 (see `theme_enrichment`), not here.

**Assembled, never authored.** `assembled_from` is required and non-empty: every view names
the objects it was built from by id or hash. A hand-constructed view cannot name a real
snapshot hash, so "one-way projection" is checkable rather than aspirational.

**Absence is a first-class outcome.** Seven fields are `Optional` and default to `None`.
`unavailable` names the ones that are `None` *because their producer does not exist yet*,
which is a different fact from "measured and absent". `engine/ledger/projection.py` refuses
to write `0.0` for an unobserved axis level for exactly this reason; a required
`confidence: float` here would reintroduce that bug at the contract layer.

**Deferred to `themeview/2`.** `briefs` (harness G8), `no_view_twin` (harness §7) and
`factor_decomposition` (L5) are absent from v1 because their producers were unbuilt when this
contract was drawn. Declaring local copies of types another module will own is the worse
failure; the version bumps when they land.

`engine/schema/source_brief.py::SourceThemeBrief` landed DURING this scaffold, so `briefs` is
the first and cheapest v2 field — one import, one tuple field, one version bump. It is left out
here only because pinning a contract to a type that is minutes old and still uncommitted is how
two modules drift apart. `ledger_root` needs no change: it is already a reference by id, which
is the right coupling to `provenance.LedgerNode` regardless of that type's shape.

Not to be confused with `engine/ledger/lifecycle.py`, which is the ledger's own
activation/falsification transitions.
"""
from __future__ import annotations

from datetime import date
from typing import Literal, Optional, Sequence

from pydantic import BaseModel, ConfigDict, Field

from ..schema.horizon import ForwardHorizon
from ..schema.theme import ThemeObject
from ..surveillance import ThemeWatch
from .decisions import LIFECYCLE_DECISIONS_VERSION

#: Bumped on any field removal or semantic change. A consumer asserts the version it was
#: built against via `require_contract` and fails closed on mismatch.
THEME_VIEW_CONTRACT: str = "themeview/1"

#: Fields whose producer does not exist yet, so a view can never populate them in v1. Kept as
#: a constant so `unavailable` is a checkable claim rather than free text.
DEFERRED_TO_V2: tuple[str, ...] = ("briefs", "no_view_twin", "factor_decomposition")

SourceKind = Literal[
    "theme_object", "theme_watch", "regime_vocabulary", "analyst_theme_map", "ledger"
]


class ContractMismatch(RuntimeError):
    """Raised when a consumer is handed a `ThemeView` of a version it was not built against."""


class ViewSource(BaseModel):
    """One object this view was assembled from, named by id or content hash."""

    model_config = ConfigDict(frozen=True)

    kind: SourceKind
    ref: str


class FalsifierView(BaseModel):
    """A falsifier as a reader sees it: the pre-registered terms plus its current read state.

    `last_read_value` is `None` when the series has never been read — which is not the same
    as a read of zero, and the two must never render alike.
    """

    model_config = ConfigDict(frozen=True)

    observable: str
    threshold: Optional[float] = None
    direction: Optional[Literal["below", "above"]] = None
    last_read_value: Optional[float] = None
    last_read_at: Optional[date] = None
    consecutive_breach_count: int = Field(default=0, ge=0)
    breached: bool = False


class StrategyFamilyView(BaseModel):
    """A ranked family, narrowed. Deliberately NOT `StrategyFamilyRec`: embedding the engine
    type would mean a rename there breaks every consumer, which is the coupling L1 exists to
    remove."""

    model_config = ConfigDict(frozen=True)

    family: str
    rank: int = Field(ge=1)
    confidence: Optional[float] = None


class ThemeView(BaseModel):
    """The one shape a downstream reader is allowed to see. Frozen; assembled, never authored.

    Keyed on `(theme_id, snapshot_hash, as_of)`. `extra="forbid"` so a field cannot be
    smuggled in without a contract bump.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    contract_version: Literal["themeview/1"] = "themeview/1"
    decisions_version: str = LIFECYCLE_DECISIONS_VERSION
    as_of: str                                    # supplied, never read from the clock (I8)

    theme_id: str
    statement: str

    #: Ties the view to the frozen object it projects. `None` when the theme was never frozen
    #: — a projected ledger theme that has not been through `firewall.freeze` has no hash, and
    #: inventing one would forge provenance.
    snapshot_hash: Optional[str] = None

    horizon: Optional[str] = None
    forward_horizon: Optional[ForwardHorizon] = None

    #: The PIPELINE axis (`ThemeObject.status`) — always present, since a ThemeObject always
    #: has one.
    status: str
    block_reason: Optional[str] = None

    #: The MARKET-TRUTH axis, owned by the surveillance state machine. `None` means no watch
    #: exists — never a guessed "armed". Keeping the two axes as separate fields is deliberate:
    #: conflating them is how a theme that was never monitored reads as monitored-and-fine.
    surveillance_status: Optional[str] = None
    surveillance_status_at: Optional[date] = None

    regime_ids: tuple[str, ...] = ()              # from A1, as of this snapshot
    candidate_ref: Optional[str] = None           # the ParentTheme / A2 candidate it descends from

    strategy_families: tuple[StrategyFamilyView, ...] = ()
    falsifiers: tuple[FalsifierView, ...] = ()

    #: Harness G4 — computed, never model-asserted. `None` when no confidence was computed.
    confidence: Optional[float] = None
    #: Harness G6 provenance entry point. `None` until the ledger emit gate lands.
    ledger_root: Optional[str] = None

    #: Non-empty by construction: every view names what it was built from.
    assembled_from: tuple[ViewSource, ...]
    #: Field names that are `None` because their producer does not exist, distinguishing
    #: "not built" from "measured absent".
    unavailable: tuple[str, ...] = ()


def project(
    theme: ThemeObject,
    *,
    as_of: str,
    watch: Optional[ThemeWatch] = None,
    regime_ids: Sequence[str] = (),
    candidate_ref: Optional[str] = None,
    ledger_root: Optional[str] = None,
    confidence: Optional[float] = None,
) -> ThemeView:
    """Assemble the read-only view. Pure: no I/O, no clock, no mutation of `theme`.

    One-way by construction — nothing consumes a `ThemeView` and writes back, so
    `SURVEILLANCE_BUILD_PLAN` §5.9 gate 5 (the frozen object never mutates) holds without a
    runtime check.

    TODO(L1): populate from `theme` + `watch`; record every source in `assembled_from`; add
    each of `DEFERRED_TO_V2` to `unavailable`, plus `surveillance_status` when `watch is None`
    and `confidence` when none was supplied. Never substitute a default for an absent value.
    """
    raise NotImplementedError("L1 ThemeView.project — scaffold only, no implementation yet")


def require_contract(view: ThemeView, expected: str = THEME_VIEW_CONTRACT) -> ThemeView:
    """Fail closed on a version a consumer was not built against.

    TODO(L1): compare `view.contract_version` to `expected` and raise `ContractMismatch`
    naming both versions. Return the view unchanged on a match.
    """
    raise NotImplementedError("L1 require_contract — scaffold only, no implementation yet")
