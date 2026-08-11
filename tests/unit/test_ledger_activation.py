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
    market_variable: str = "credit_spread",
    mechanism_tags: tuple[str, ...] = ("funding_stress",),
) -> AtomicClaim:
    return AtomicClaim(
        claim_id=claim_id,
        doc_id="doc-1",
        source_institution=source_institution,
        doc_date=doc_date,
        text=claim_id,
        market_variable=market_variable,
        direction=direction,
        horizon_days=horizon_days,
        stated_conviction=conviction,
        mechanism_tags=mechanism_tags,
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


def _stub_pipeline(
    monkeypatch,
    *,
    claims: tuple[AtomicClaim, ...],
    outcome: AdmissionOutcome | None = None,
) -> None:
    """Stub Pass A / Pass B / clustering. `outcome=None` keeps the REAL `admit`
    (and therefore the real WF gate) in the path."""
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
    if outcome is not None:
        monkeypatch.setattr("engine.ledger.runner.admit", lambda cluster: outcome)


def test_negative_score_with_required_breadth_activates_as_contested(tmp_path, monkeypatch):
    """ONTOLOGY §Lifecycle: CANDIDATE → ACTIVE iff B_θ ≥ 2 ∧ |S_θ| ≥ 2 — the gate is
    on the MAGNITUDE of S. §Theme "Interpretation" and §Lifecycle both say a theme
    with S < 0 and no breach is CONTESTED, a reportable sub-state of ACTIVE, not
    dead: unanimous disagreement is still tracked conviction. See D-09."""
    _write_doc(tmp_path, "doc-1")
    claims = (_claim("c1", "JPM"), _claim("c2", "GS"))
    _stub_pipeline(monkeypatch, claims=claims, outcome=_admitted_outcome(*claims, horizon_days=90))
    monkeypatch.setattr(
        "engine.ledger.runner.score",
        lambda *args, **kwargs: ScoreView(theme_id="admitted:test-theme", as_of="2026-04-01", S=-4.0, B=2),
    )

    state = forward_ingest(["doc-1"], tmp_path)

    assert [(a.theme_id, a.status) for a in state.admitted] == [("admitted:test-theme", "ACTIVE")]


def test_small_negative_score_stays_candidate(tmp_path, monkeypatch):
    """The mirror of the gate: |S| below the threshold does not activate, on either
    side of zero (ONTOLOGY §Lifecycle, ACTIVATION_ABS_SCORE_MIN)."""
    _write_doc(tmp_path, "doc-1")
    claims = (_claim("c1", "JPM"), _claim("c2", "GS"))
    _stub_pipeline(monkeypatch, claims=claims, outcome=_admitted_outcome(*claims, horizon_days=90))
    monkeypatch.setattr(
        "engine.ledger.runner.score",
        lambda *args, **kwargs: ScoreView(theme_id="admitted:test-theme", as_of="2026-04-01", S=-1.5, B=2),
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


def _wf_cluster_claims(horizon_days: int) -> tuple[AtomicClaim, ...]:
    """A cluster that clears the §Admission gate (3 claims, 2 institutions, same day)
    and synthesizes a k=2 chain on a tracked axis — so WF is the only thing left to
    decide. `admit` takes H = min(claim horizons)."""
    tags = ("funding_stress", "liquidity_premium")
    return tuple(
        _claim(cid, inst, horizon_days=horizon_days,
               market_variable="C0A0_OAS", mechanism_tags=tags)
        for cid, inst in (("c1", "JPM"), ("c2", "JPM"), ("c3", "GS"))
    )


def test_zero_horizon_is_rejected_by_wf_not_admitted(tmp_path, monkeypatch):
    """ONTOLOGY §WF clause (d): 0 < H ≤ H_MAX. H = 0 gives an empty valid-time window
    (§Bitemporal) and a degenerate half-life h = H/2 (§Scoring), so such a theme would
    score a permanent S = 0 / B = 0 and could never activate — admitted but invisible.
    It must fail the gate and route to NEEDS_STRUCTURING instead. See D-10."""
    _write_doc(tmp_path, "doc-1")
    _stub_pipeline(monkeypatch, claims=_wf_cluster_claims(0))

    state = forward_ingest(["doc-1"], tmp_path)

    assert state.admitted == []
    assert state.needs_structuring == ["c1", "c2", "c3"]


def test_negative_horizon_is_rejected_by_wf(tmp_path, monkeypatch):
    """Same clause (d) lower bound: a backwards horizon is not a hypothesis."""
    _write_doc(tmp_path, "doc-1")
    _stub_pipeline(monkeypatch, claims=_wf_cluster_claims(-30))

    state = forward_ingest(["doc-1"], tmp_path)

    assert state.admitted == []
    assert state.needs_structuring == ["c1", "c2", "c3"]


def test_one_day_horizon_is_admitted(tmp_path, monkeypatch):
    """The other side of the clause-(d) boundary. H = 1 is the interim floor the
    ONTOLOGY determines (strict positivity at day granularity); whether an
    economically meaningful H_MIN should sit above it is open — BLOCKED B-04."""
    _write_doc(tmp_path, "doc-1")
    _stub_pipeline(monkeypatch, claims=_wf_cluster_claims(1))

    state = forward_ingest(["doc-1"], tmp_path)

    assert state.needs_structuring == []
    assert [(a.theme_id, a.status) for a in state.admitted] == [
        ("admitted:funding_stress-liquidity_premium", "ACTIVE")
    ]
