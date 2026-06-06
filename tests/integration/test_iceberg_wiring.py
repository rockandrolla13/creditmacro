"""
Stage-0 wiring: the iceberg classifier is attached to IngestionResult by ingest(),
and the additive Optional field does not break existing IngestionResult construction
(example.py / scripted_provider.py).
"""
from __future__ import annotations

from engine.schema import IcebergClassification
from engine.stage0 import IngestionResult, ingest


def test_ingest_attaches_iceberg_classifications():
    # Use the worked-example streams (LLM stub bypassed) so we exercise the real path.
    from engine.example import CANDIDATE, observations, signals

    result = ingest(
        text="",
        observations=observations,
        signals=signals,
    )
    # ingest() with injected streams produces no candidates → empty classifications,
    # but the field must exist and be a list.
    assert isinstance(result.iceberg_classifications, list)


def test_ingest_classifies_ranked_candidates(monkeypatch):
    from engine.example import CANDIDATE, observations, signals
    import engine.stage0 as stage0

    # Make parse_research_text return our hand-built candidate so ingest ranks + classifies it.
    monkeypatch.setattr(
        stage0,
        "parse_research_text",
        lambda text: (observations, [CANDIDATE], signals),
    )
    result = stage0.ingest(text="anything")

    assert len(result.iceberg_classifications) == 1
    c = result.iceberg_classifications[0]
    assert isinstance(c, IcebergClassification)
    assert c.item_id == CANDIDATE.id
    # A CandidateTheme with no operational axis at Stage 0 → watchlist (CORE THEMES).
    assert c.decision == "watchlist"
    assert c.dashboard_lane == "CORE_THEMES"
    assert c.typed_stream == "CandidateTheme"


def test_ingestion_result_constructible_without_classifications():
    # The golden-master / example.py construction path: no iceberg field passed.
    r = IngestionResult(
        observations=[],
        candidate_themes=[],
        consensus_signals=[],
        ranked_candidates=[],
    )
    assert r.iceberg_classifications == []
