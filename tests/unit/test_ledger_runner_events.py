"""Unit tests for foldable events from runner.forward_ingest (ONTOLOGY §Bitemporal, §Lifecycle).

Proves that forward_ingest populates created_event and STATUS_CHANGED events on AdmittedTheme,
and that folding those events via substrate/fold.py reconstructs a ThemeHypothesis with the
correct properties and status (ACTIVE or CANDIDATE).
"""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from engine.ledger.ingest.admission import AdmissionOutcome, OrphanCluster
from engine.ledger.ingest.claim import AtomicClaim
from engine.ledger.ingest.link import EvidenceLink
from engine.ledger.ingest.scoring_view import ScoreView
from engine.ledger.runner import forward_ingest
from engine.ledger.substrate.events import EventType
from engine.ledger.substrate.fold import fold
from engine.ledger.substrate.hypothesis import LifecycleStatus, Mechanism, ThemeDefinitionView, TransmissionEdge

CORPUS = Path(__file__).parent.parent / "golden" / "corpus"
EXPECTED_REGISTRY = json.loads((CORPUS / "expected_registry.json").read_text())


def test_forward_ingest_golden_corpus_events_fold_to_active():
    """Golden corpus test: forward_ingest over gc-003-jpm, gc-004-gs, gc-005-solo returns
    foldable events that fold via substrate.fold into a ThemeHypothesis matching expected_registry.json.
    """
    state = forward_ingest(["gc-003-jpm", "gc-004-gs", "gc-005-solo"], CORPUS)
    assert len(state.admitted) == 1

    admitted_theme = state.admitted[0]
    assert admitted_theme.theme_id == "admitted:funding_stress-dealer_balance_sheet_capacity"
    assert admitted_theme.status == "ACTIVE"

    # Verify created_event and status_changed_event presence
    assert admitted_theme.created_event is not None
    assert admitted_theme.created_event.event_type == EventType.CREATED
    assert admitted_theme.status_changed_event is not None
    assert admitted_theme.status_changed_event.event_type == EventType.STATUS_CHANGED
    assert admitted_theme.status_changed_event.payload == {"status": "ACTIVE"}

    # Event helpers
    events = admitted_theme.events()
    assert len(events) == 2
    assert state.events_for_theme(admitted_theme.theme_id) == events
    assert state.events_by_theme()[admitted_theme.theme_id] == events

    # Fold events via engine.ledger.substrate.fold.fold
    hypothesis = fold(events)
    assert hypothesis is not None
    assert hypothesis.theme_id == admitted_theme.theme_id
    assert hypothesis.operational_axis == "C0A0_OAS"
    assert hypothesis.falsifier == admitted_theme.created_event.payload["falsifier"]
    assert hypothesis.status == LifecycleStatus.ACTIVE
    assert hypothesis.status.value == EXPECTED_REGISTRY["admitted"][0]["status"]


def _write_doc(corpus_dir: Path, doc_id: str, source_institution: str = "JPM", doc_date: str = "2026-04-01") -> None:
    corpus_dir.mkdir(parents=True, exist_ok=True)
    (corpus_dir / f"{doc_id}.md").write_text(
        "---\n"
        f"source_institution: {source_institution}\n"
        f"doc_date: {doc_date}\n"
        "---\n"
        "stub\n"
    )


def _claim(claim_id: str, source_institution: str = "JPM") -> AtomicClaim:
    return AtomicClaim(
        claim_id=claim_id,
        doc_id="doc-1",
        source_institution=source_institution,
        doc_date="2026-04-01",
        text=claim_id,
        market_variable="credit_spread",
        direction=1,
        horizon_days=90,
        stated_conviction=2,
        mechanism_tags=("funding_stress",),
    )


def _stub_pipeline(monkeypatch, claims: tuple[AtomicClaim, ...], outcome: AdmissionOutcome) -> None:
    class DummyExtractor:
        def __init__(self, _provider) -> None:
            pass

        def extract(self, doc_id: str, text: str, source_institution: str, doc_date: str):
            return SimpleNamespace(claims=list(claims), out_of_vocab_tags=[])

    class DummyMapper:
        def map(self, mapped_claims, existing_definitions, theme_revisions):
            return SimpleNamespace(orphans=list(mapped_claims))

    monkeypatch.setattr("engine.ledger.runner.PassAExtractor", DummyExtractor)
    monkeypatch.setattr("engine.ledger.runner.StructuralSemanticMapper", DummyMapper)
    monkeypatch.setattr(
        "engine.ledger.runner.cluster_orphans",
        lambda orphans: [OrphanCluster(claims=tuple(orphans))],
    )
    monkeypatch.setattr("engine.ledger.runner.admit", lambda cluster: outcome)


def test_forward_ingest_candidate_theme_folds_to_candidate(tmp_path, monkeypatch):
    """Proves that a theme whose activation gate is not met emits no STATUS_CHANGED event,
    carries created_event, and folds to LifecycleStatus.CANDIDATE.
    """
    _write_doc(tmp_path, "doc-1")
    claims = (_claim("c1", "JPM"), _claim("c2", "GS"))

    theme_id = "admitted:test-candidate"
    definition = ThemeDefinitionView(
        theme_id=theme_id,
        mechanism=Mechanism(edges=(TransmissionEdge(v_from="funding_stress", v_to="credit_spread", sign=1),)),
        shock_direction=1,
        operational_axis="credit_spread",
        horizon_days=90,
    )
    from engine.ledger.substrate.events import ThemeEvent, Provenance
    created_event = ThemeEvent(
        event_id=f"{theme_id}:created",
        theme_id=theme_id,
        event_type=EventType.CREATED,
        payload={
            "mechanism": definition.mechanism.model_dump(),
            "shock_direction": 1,
            "operational_axis": "credit_spread",
            "horizon_days": 90,
            "falsifier": "test falsifier",
        },
        effective_at="2026-04-01",
        provenance=Provenance.ORPHAN_PROMOTION,
    )
    outcome = AdmissionOutcome(
        status="admitted",
        theme_id=theme_id,
        definition=definition,
        created_event=created_event,
        founding_links=(
            EvidenceLink(
                link_id="L-c1", theme_id=theme_id, theme_revision=1,
                claim_id="c1", polarity=1, match_confidence=1.0,
            ),
        ),
    )

    _stub_pipeline(monkeypatch, claims, outcome)
    monkeypatch.setattr(
        "engine.ledger.runner.score",
        lambda *args, **kwargs: ScoreView(theme_id=theme_id, as_of="2026-04-01", S=1.0, B=1),
    )

    state = forward_ingest(["doc-1"], tmp_path)
    assert len(state.admitted) == 1

    admitted_theme = state.admitted[0]
    assert admitted_theme.theme_id == theme_id
    assert admitted_theme.status == "CANDIDATE"
    assert admitted_theme.created_event == created_event
    assert admitted_theme.status_changed_event is None

    events = admitted_theme.events()
    assert len(events) == 1

    hypothesis = fold(events)
    assert hypothesis is not None
    assert hypothesis.theme_id == theme_id
    assert hypothesis.status == LifecycleStatus.CANDIDATE
    assert hypothesis.status.value == "CANDIDATE"


def test_contested_negative_score_theme_folds_to_active(tmp_path, monkeypatch):
    """Proves that a theme with negative score but |S| >= 2 and B >= 2 activates with STATUS_CHANGED(ACTIVE)
    and folds to LifecycleStatus.ACTIVE (ONTOLOGY §Lifecycle, D-09).
    """
    _write_doc(tmp_path, "doc-1")
    claims = (_claim("c1", "JPM"), _claim("c2", "GS"))

    theme_id = "admitted:test-contested"
    definition = ThemeDefinitionView(
        theme_id=theme_id,
        mechanism=Mechanism(edges=(TransmissionEdge(v_from="funding_stress", v_to="credit_spread", sign=1),)),
        shock_direction=1,
        operational_axis="credit_spread",
        horizon_days=90,
    )
    from engine.ledger.substrate.events import ThemeEvent, Provenance
    created_event = ThemeEvent(
        event_id=f"{theme_id}:created",
        theme_id=theme_id,
        event_type=EventType.CREATED,
        payload={
            "mechanism": definition.mechanism.model_dump(),
            "shock_direction": 1,
            "operational_axis": "credit_spread",
            "horizon_days": 90,
            "falsifier": "test falsifier",
        },
        effective_at="2026-04-01",
        provenance=Provenance.ORPHAN_PROMOTION,
    )
    outcome = AdmissionOutcome(
        status="admitted",
        theme_id=theme_id,
        definition=definition,
        created_event=created_event,
        founding_links=(
            EvidenceLink(
                link_id="L-c1", theme_id=theme_id, theme_revision=1,
                claim_id="c1", polarity=-1, match_confidence=1.0,
            ),
        ),
    )

    _stub_pipeline(monkeypatch, claims, outcome)
    monkeypatch.setattr(
        "engine.ledger.runner.score",
        lambda *args, **kwargs: ScoreView(theme_id=theme_id, as_of="2026-04-01", S=-3.0, B=2),
    )

    state = forward_ingest(["doc-1"], tmp_path)
    assert len(state.admitted) == 1

    admitted_theme = state.admitted[0]
    assert admitted_theme.theme_id == theme_id
    assert admitted_theme.status == "ACTIVE"
    assert admitted_theme.status_changed_event is not None
    assert admitted_theme.status_changed_event.payload == {"status": "ACTIVE"}

    hypothesis = fold(admitted_theme.events())
    assert hypothesis is not None
    assert hypothesis.status == LifecycleStatus.ACTIVE
