"""Unit tests for hypotheses_from_registry and project_all in engine/ledger_entrance.py.

Proves:
1. forward_ingest over golden corpus tests/golden/corpus folds to exactly one ThemeHypothesis with status ACTIVE.
2. project_all turns it into a ThemeObject whose id is the ledger theme id.
3. A registry with no admitted themes yields an empty list rather than raising.
4. Un-admitted claims (needs_structuring, orphan_claim_ids) are skipped.
5. Admitted themes folding to None (no CREATED event) are dropped.
"""
from __future__ import annotations

from pathlib import Path

from engine.ledger.runner import AdmittedTheme, RegistryState, forward_ingest
from engine.ledger.substrate.events import EventType, Provenance, ThemeEvent
from engine.ledger.substrate.hypothesis import LifecycleStatus
from engine.ledger_entrance import hypotheses_from_registry, project_all
from engine.schema.theme import ThemeObject

CORPUS = Path(__file__).parent.parent / "golden" / "corpus"


def test_golden_corpus_entrance_fold_and_project():
    """Proves that a registry from forward_ingest over the golden corpus folds to
    exactly one ACTIVE ThemeHypothesis, and project_all turns it into a ThemeObject
    whose id matches the ledger theme id.
    """
    state = forward_ingest(["gc-003-jpm", "gc-004-gs", "gc-005-solo"], CORPUS)
    assert len(state.admitted) == 1

    hypotheses = hypotheses_from_registry(state, as_of="2026-05-05")
    assert len(hypotheses) == 1

    hypothesis = hypotheses[0]
    assert hypothesis.theme_id == state.admitted[0].theme_id
    assert hypothesis.status == LifecycleStatus.ACTIVE
    assert hypothesis.status.value == "ACTIVE"

    projected_objs = project_all(hypotheses, as_of="2026-05-05")
    assert len(projected_objs) == 1

    projected = projected_objs[0]
    assert isinstance(projected, ThemeObject)
    assert projected.id == hypothesis.theme_id


def test_empty_registry_yields_empty_list():
    """Proves that a registry with no admitted themes yields an empty list rather than raising."""
    state = RegistryState()
    hypotheses = hypotheses_from_registry(state, as_of="2026-05-05")
    assert hypotheses == []

    projected = project_all(hypotheses, as_of="2026-05-05")
    assert projected == []


def test_registry_with_only_unadmitted_claims_yields_empty_list():
    """Proves that orphan claims and needs_structuring claims are never folded into themes."""
    state = RegistryState(
        admitted=[],
        orphan_claim_ids=["orphan-1", "orphan-2"],
        needs_structuring=["needs-1"],
    )
    hypotheses = hypotheses_from_registry(state, as_of="2026-05-05")
    assert hypotheses == []


def test_admitted_theme_folding_to_none_is_dropped():
    """Proves that an admitted theme with no CREATED event folds to None and is dropped."""
    status_ev = ThemeEvent(
        event_id="t1:status",
        theme_id="admitted:no-created",
        event_type=EventType.STATUS_CHANGED,
        payload={"status": "ACTIVE"},
        effective_at="2026-05-05",
        provenance=Provenance.ORPHAN_PROMOTION,
    )
    admitted = AdmittedTheme(
        theme_id="admitted:no-created",
        status="ACTIVE",
        created_event=None,
        status_changed_event=status_ev,
    )
    state = RegistryState(admitted=[admitted])

    hypotheses = hypotheses_from_registry(state, as_of="2026-05-05")
    assert hypotheses == []
