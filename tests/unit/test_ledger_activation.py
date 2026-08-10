from __future__ import annotations

from types import SimpleNamespace

from engine.ledger.ingest.admission import AdmissionOutcome, OrphanCluster
from engine.ledger.ingest.claim import AtomicClaim
from engine.ledger.ingest.link import EvidenceLink
from engine.ledger.ingest.scoring_view import ScoreView
from engine.ledger.runner import forward_ingest
from engine.ledger.substrate.hypothesis import Mechanism, ThemeDefinitionView, TransmissionEdge


def _write_doc(corpus_dir, doc_id: str, source_institution: str = "JPM", doc_date: str = "2026-04-01") -> None:
    corpus_dir.mkdir(parents=True, exist_ok=True)
    (corpus_dir / f"{doc_id}.md").write_text(
        "---\n"
        f"source_institution: {source_institution}\n"
        f"doc_date: {doc_date}\n"
        "---\n"
        "stub\n"
    )


def _claim(
    claim_id: str,
    source_institution: str,
    *,
    doc_date: str = "2026-04-01",
    direction: int = 1,
    horizon_days: int = 90,
    conviction: int = 2,
) -> AtomicClaim:
    return AtomicClaim(
        claim_id=claim_id,
        doc_id="doc-1",
        source_institution=source_institution,
        doc_date=doc_date,
        text=claim_id,
        market_variable="credit_spread",
        direction=direction,
        horizon_days=horizon_days,
        stated_conviction=conviction,
        mechanism_tags=("funding_stress",),
    )


def _admitted_outcome(*claims: AtomicClaim, horizon_days: int) -> AdmissionOutcome:
    theme_id = "admitted:test-theme"
    definition = ThemeDefinitionView(
        theme_id=theme_id,
        mechanism=Mechanism(edges=(TransmissionEdge(v_from="funding_stress", v_to="credit_spread", sign=1),)),
        shock_direction=1,
        operational_axis="credit_spread",
        horizon_days=horizon_days,
    )
    founding_links = tuple(
        EvidenceLink(
            link_id=f"L-{claim.claim_id}",
            theme_id=theme_id,
            theme_revision=1,
            claim_id=claim.claim_id,
            polarity=1,
            match_confidence=1.0,
        )
        for claim in claims
    )
    return AdmissionOutcome(
        status="admitted",
        theme_id=theme_id,
        definition=definition,
        founding_links=founding_links,
    )


def _stub_pipeline(monkeypatch, *, claims: tuple[AtomicClaim, ...], outcome: AdmissionOutcome) -> None:
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


def test_negative_score_with_required_breadth_does_not_activate(tmp_path, monkeypatch):
    _write_doc(tmp_path, "doc-1")
    claims = (_claim("c1", "JPM"), _claim("c2", "GS"))
    _stub_pipeline(monkeypatch, claims=claims, outcome=_admitted_outcome(*claims, horizon_days=90))
    monkeypatch.setattr(
        "engine.ledger.runner.score",
        lambda *args, **kwargs: ScoreView(theme_id="admitted:test-theme", as_of="2026-04-01", S=-4.0, B=2),
    )

    state = forward_ingest(["doc-1"], tmp_path)

    assert [(a.theme_id, a.status) for a in state.admitted] == [("admitted:test-theme", "CANDIDATE")]


def test_positive_score_with_required_breadth_activates(tmp_path, monkeypatch):
    _write_doc(tmp_path, "doc-1")
    claims = (_claim("c1", "JPM"), _claim("c2", "GS"))
    _stub_pipeline(monkeypatch, claims=claims, outcome=_admitted_outcome(*claims, horizon_days=90))
    monkeypatch.setattr(
        "engine.ledger.runner.score",
        lambda *args, **kwargs: ScoreView(theme_id="admitted:test-theme", as_of="2026-04-01", S=4.0, B=2),
    )

    state = forward_ingest(["doc-1"], tmp_path)

    assert [(a.theme_id, a.status) for a in state.admitted] == [("admitted:test-theme", "ACTIVE")]


def test_zero_horizon_does_not_raise_zero_division_error(tmp_path, monkeypatch):
    _write_doc(tmp_path, "doc-1")
    claims = (
        _claim("c1", "JPM", horizon_days=0),
        _claim("c2", "GS", horizon_days=0),
    )
    _stub_pipeline(monkeypatch, claims=claims, outcome=_admitted_outcome(*claims, horizon_days=0))

    state = forward_ingest(["doc-1"], tmp_path)

    assert [(a.theme_id, a.status) for a in state.admitted] == [("admitted:test-theme", "CANDIDATE")]
