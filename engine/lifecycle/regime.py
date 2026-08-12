"""A1 — regime discovery. SCAFFOLD: types are real, `discover_regimes` is not implemented.

Read the pool of grounded atoms and infer the small vocabulary (3–7) of market *postures* the
corpus is implicitly using. A regime is the market's posture, not its measurement (D-A1-3):
clustering runs on opinion-bearing atoms only, and numeric-only atoms belong to theme evidence
(L2), not to regime identity.

**Blocked on one human sentence.** `decisions.OPINION_CLAIM_KINDS` is empty because D-A1-3
names claim kinds no extractor in this repo emits. Until that mapping is ratified, A1 cannot
say which atoms are opinion-bearing, and guessing would silently redefine what a regime is.

**Overlaps something the plan did not know about.** `engine/schema/macro.py::MacroContext` and
the WIRED `macro-regime-classifier` skill already produce a qualitative macro framing per
theme. That is a *fixed taxonomy applied to one theme*; A1 is *a vocabulary inferred from the
whole corpus*. They are different jobs, but whoever builds A1 should reconcile the two rather
than emit two competing regime labels for the same week.

Fail-closed: A1 that cannot ground its output does not emit. Last week's vocabulary stays
authoritative and the L4 book renders with a stale banner. A stale but honest book beats a
fresh but fabricated one.

Not to be confused with `engine/ledger/lifecycle.py`.
"""
from __future__ import annotations

from typing import Optional, Sequence

from pydantic import BaseModel, ConfigDict, Field

from .decisions import LIFECYCLE_DECISIONS_VERSION, REGIME_COUNT_CAP, REGIME_COUNT_FLOOR

REGIME_CONTRACT: str = "regime/1"


class RegimeDiscoveryRefused(RuntimeError):
    """A1 could not ground its output, or the opinion filter is unratified. Nothing is emitted."""


class RegimeType(BaseModel):
    """One named posture cluster. Every defining feature is backed by >=1 grounded atom."""

    model_config = ConfigDict(frozen=True)

    regime_id: str
    name: str                                     # e.g. "growth_slowdown_tight_credit"
    defining_features: tuple[str, ...] = ()
    supporting_atom_ids: tuple[str, ...] = ()     # all must be harness-verified
    #: Share of the OPINION subset consistent with this regime. Harness-computed from the atom
    #: set, never model-asserted (G4). `None` when it could not be computed — a prevalence of
    #: 0.0 is a finding, not a gap.
    prevalence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None


class RegimeVocabulary(BaseModel):
    """The weekly emit. Capped at `REGIME_COUNT_FLOOR..REGIME_COUNT_CAP` (D-A1-1)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    contract_version: str = REGIME_CONTRACT
    decisions_version: str = LIFECYCLE_DECISIONS_VERSION
    as_of: str                                    # supplied, never the clock (I8)
    regimes: tuple[RegimeType, ...] = ()
    dominant_regime_id: Optional[str] = None      # highest prevalence; None if none computed
    #: True when this vocabulary is last week's, carried forward because A1 abstained. The L4
    #: book must render a banner rather than present it as this week's reading.
    stale_regime: bool = False
    ledger_root: Optional[str] = None
    count_floor: int = REGIME_COUNT_FLOOR
    count_cap: int = REGIME_COUNT_CAP


def discover_regimes(
    atoms: Sequence[object],
    *,
    as_of: str,
    previous: Optional[RegimeVocabulary] = None,
) -> RegimeVocabulary:
    """Infer this week's regime vocabulary from the grounded atom pool.

    TODO(A1): refuse with `RegimeDiscoveryRefused` while `OPINION_CLAIM_KINDS` is empty; filter
    to opinion-bearing atoms; cluster; merge above the dedup threshold down to the cap; compute
    `prevalence` deterministically from the atom set. Below the floor of three, abstain — carry
    `previous` forward with `stale_regime=True` rather than fabricating change.
    """
    raise NotImplementedError("A1 discover_regimes — scaffold only, no implementation yet")
