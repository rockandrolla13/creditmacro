"""L3a — the evidence pack. SCAFFOLD: types are real, `pack_terminal` is a stub.

**What this records.** Not *what happened* — *what we knew when we said it*. Six months after
a loss the only question worth asking is whether the call was wrong because the evidence was
thin, because the reasoning was bad, or because the world changed. Nothing today can answer it.

A pack is frozen at every terminal transition (`falsified`, `horizon_expired`, `played_out`),
written once, never updated. A correction is a NEW pack naming its predecessor via
`supersedes` — that is what makes the store append-only in practice and not just in intent.

**Fail-closed.** A terminal transition that cannot write a complete pack BLOCKS the transition
and raises to the PM. Losing the record of a loss is worse than a delayed status change.

**The plan's L3 leans on the wrong object, and this module does not follow it.**
`PLAN-theme-lifecycle.md` types `EvidencePack.outcome` as `ThemeOutcomeRecord`. The real
`engine/outcomes.py::ThemeOutcomeRecord` is a plain dataclass of PRICING calibration inputs —
`p`, `q`, `X_s`, `X_mkt`, `predicted_edge`, `edge_std`. A discovery-only theme never has any of
them, so making it a required field would force six fabricated numbers into the one record that
exists to be honest. `TerminalOutcome` below carries what a discovery theme actually knows, and
`outcome_ref` points at the pricing record when one exists.

Persistence is the CALLER's job — this module builds the object and does no I/O, so it stays
pure and testable. The plan's `db/migrations/0004_evidence_packs.sql` is still owed; the
existing migrations stop at `0002`.

Not to be confused with `engine/ledger/lifecycle.py`.
"""
from __future__ import annotations

from typing import Optional, Sequence

from pydantic import BaseModel, ConfigDict, Field

from ..surveillance import ThemeWatch, WatchStatus
from .decisions import LIFECYCLE_DECISIONS_VERSION, PACK_FULL_RETENTION_MONTHS
from .theme_view import ThemeView

PACK_CONTRACT: str = "evidencepack/1"


class IncompletePack(RuntimeError):
    """A complete pack could not be built, so the terminal transition must not proceed."""


class FalsifierRead(BaseModel):
    """One scheduled read of a falsifier series. The pack keeps the FULL series, not just the
    breach — the reads before a breach are what tell you whether the falsifier was well chosen."""

    model_config = ConfigDict(frozen=True)

    observable: str
    read_at: str
    value: Optional[float] = None                 # None = the read was scheduled but missed
    breaching: bool = False
    consecutive_breach_count: int = Field(default=0, ge=0)


class TerminalOutcome(BaseModel):
    """What a DISCOVERY theme knows at its terminal state. Deliberately not
    `engine.outcomes.ThemeOutcomeRecord`, which demands pricing a discovery theme never has."""

    model_config = ConfigDict(frozen=True)

    theme_id: str
    terminal_status: WatchStatus
    terminal_at: str
    reason: str = ""
    #: Whether the pre-registered falsifier fired BEFORE the P&L did. `None` when unknown; this
    #: is the input to the scorecard's falsifier-quality metric and must not default to False.
    falsifier_fired_first: Optional[bool] = None
    realized_axis_at_horizon: Optional[float] = None
    #: Points at an `engine.outcomes.ThemeOutcomeRecord` when the theme reached pricing.
    outcome_ref: Optional[str] = None


class EvidencePack(BaseModel):
    """Immutable. Written once at a terminal transition; a correction is a new pack."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    contract_version: str = PACK_CONTRACT
    decisions_version: str = LIFECYCLE_DECISIONS_VERSION
    pack_id: str
    theme_id: str
    snapshot_hash: Optional[str] = None
    terminal_status: WatchStatus
    packed_at: str                                # supplied, never the clock (I8)

    theme_view: ThemeView                         # the L1 projection as of terminal
    atom_ids: tuple[str, ...] = ()                # every kept atom, by id
    #: Surveillance §5.7 disconfirm + confirm + adjudication passes, by id. The scoring calls
    #: themselves live in the watch; the pack records that they happened and which they were.
    blind_scoring_pass_ids: tuple[str, ...] = ()
    falsifier_reads: tuple[FalsifierRead, ...] = ()
    outcome: TerminalOutcome
    #: Set on a correction — the pack this one replaces. Nothing is ever overwritten.
    supersedes: Optional[str] = None
    retention_months: int = PACK_FULL_RETENTION_MONTHS
    #: Field names that could not be populated because their producer does not exist yet
    #: (G8 briefs, the no-view twin). Named rather than silently empty.
    unavailable: tuple[str, ...] = ()


def pack_terminal(
    view: ThemeView,
    watch: ThemeWatch,
    *,
    packed_at: str,
    pack_id: str,
    atom_ids: Sequence[str] = (),
    supersedes: Optional[str] = None,
) -> EvidencePack:
    """Freeze the complete record at a terminal transition. Pure; the caller persists.

    TODO(L3): refuse with `IncompletePack` when `watch.status` is not terminal, or when the
    falsifier read series or the view is incomplete — the caller must then block the
    transition rather than write a partial pack.
    """
    raise NotImplementedError("L3 pack_terminal — scaffold only, no implementation yet")
