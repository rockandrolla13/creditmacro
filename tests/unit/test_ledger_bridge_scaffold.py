"""Scaffold gates for the ledger→discovery seam.

Two things are asserted while the seam is still stubs, because both are STRUCTURAL and
neither gets easier to add later:

1. The adapter exposes every discovery seam `run_workflow` calls, and NONE of the
   expression seams. The absence is the fence that makes `run_workflow(..., "expression")`
   raise `expression_mode_not_supported` on a ledger theme — a theme with no observed
   market level must never reach pricing.
2. Both new modules import cleanly and their stubs raise `NotImplementedError` rather
   than returning a plausible empty value. A stub that returns `[]` is indistinguishable
   from a working seam that found nothing.
"""
from __future__ import annotations

import pytest

from engine import ledger_bridge, ledger_entrance
from engine.ledger_bridge import (
    DISCOVERY_SEAMS,
    EXPRESSION_SEAMS,
    LedgerProjectionNotRoutable,
    LedgerProvider,
)
from engine.ledger.projection import to_theme_object
from engine.ledger.substrate.events import EventType, Provenance, ThemeEvent
from engine.ledger.substrate.fold import fold
from engine.ledger.substrate.hypothesis import Mechanism, TransmissionEdge
from engine.schema import ThemeObject

_MECHANISM = Mechanism(edges=(
    TransmissionEdge(v_from="funding_stress", v_to="liquidity_premium", sign=1),
    TransmissionEdge(v_from="liquidity_premium", v_to="credit_spread", sign=1),
))


def _event(event_id: str, event_type: EventType, payload: dict) -> ThemeEvent:
    return ThemeEvent(
        event_id=event_id, theme_id="t1", event_type=event_type, payload=payload,
        effective_at="2026-05-01T00:00:00+00:00", recorded_at="2026-05-01T00:00:00+00:00",
        provenance=Provenance.ORPHAN_PROMOTION,
    )


def _minimal_projected(*, dead: bool = False) -> ThemeObject:
    """A REAL projection output — folded from events, mapped by `projection.py`.

    Hand-building a `ThemeObject` here would be a second mapping site (AMEND A3) and
    would drift from what the bridge actually receives."""
    events = [_event("e1", EventType.CREATED, {
        "mechanism": _MECHANISM.model_dump(), "shock_direction": 1,
        "operational_axis": "C0A0_OAS", "horizon_days": 90,
        "falsifier": "IG OAS fails to widen 20bp within 60d of a funding-stress print",
    })]
    if dead:
        events.append(_event("e2", EventType.RETIRED, {}))
    return to_theme_object(fold(events), as_of="2026-05-05")


# ── seam surface ─────────────────────────────────────────────────────────────

def test_provider_exposes_every_discovery_seam():
    provider = LedgerProvider(_minimal_projected())
    missing = [s for s in DISCOVERY_SEAMS if not callable(getattr(provider, s, None))]
    assert missing == [], f"LedgerProvider is missing discovery seams: {missing}"


def test_provider_exposes_no_expression_seam():
    provider = LedgerProvider(_minimal_projected())
    present = [s for s in EXPRESSION_SEAMS if hasattr(provider, s)]
    assert present == [], (
        f"LedgerProvider must not expose expression seams {present}: their absence is what "
        "makes run_workflow reject expression mode for a theme with no observed mark."
    )


def test_blocked_projection_is_refused_at_construction():
    with pytest.raises(LedgerProjectionNotRoutable):
        LedgerProvider(_minimal_projected(dead=True))


# ── stubs are honest ─────────────────────────────────────────────────────────

def test_discovery_seams_are_unimplemented_not_silently_empty():
    provider = LedgerProvider(_minimal_projected())
    with pytest.raises(NotImplementedError):
        provider.context()
    with pytest.raises(NotImplementedError):
        provider.diagnose_loops(None)
    with pytest.raises(NotImplementedError):
        provider.propose_scenarios(None, None, None)


def test_entrance_stubs_are_unimplemented():
    with pytest.raises(NotImplementedError):
        ledger_entrance.run_ledger_discovery(None, None)


def test_modules_import_without_touching_the_ledger_at_import_time():
    """The bridge must not pull the ledger substrate in just by being imported — the
    entrance is the only module allowed to reach into `engine.ledger`."""
    assert ledger_bridge.__doc__ and ledger_entrance.__doc__
    assert not hasattr(ledger_bridge, "forward_ingest")
