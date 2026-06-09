"""Temporal PART 5 — claim-level temporal status.

Firewall-critical: allowed_use_in_phase_a depends on whether the source is the CURRENT INPUT.
An archived historical forecast is phase_b_only / historical_context_only; only an explicitly
current-input source's claims are current_input_evidence. A non-method claim is NEVER method_context.
"""
from __future__ import annotations

from datetime import date

from engine.evidence_extraction import CausalClaimCandidate, EvidenceExtractionBundle, StrategyFamilyHint
from engine.schema import EvidenceAtom
from engine.temporal import classify_temporal_context
from engine.wiki_agents import SourceClassification, TemporalContextAgent, TemporalContextInput

OLD = date(2019, 3, 15)
CUR = date(2026, 6, 9)


def _status(text, access="case", is_current_input=False, src=OLD):
    ctx, st, hz, _ = classify_temporal_context(
        source_slug="s", access_class=access, source_date=src, current_date=CUR,
        claims=[("c1", 1, text)], mechanisms=[], is_current_input=is_current_input)
    return st[0], hz


def test_archived_historical_fact_is_historical_context_only():
    s, _ = _status("Stoxx 600 is 8% above model fair value")
    assert s.claim_kind == "historical_fact"
    assert s.allowed_use_in_phase_a == "historical_context_only"


def test_archived_historical_forecast_is_phase_b_only():
    s, _ = _status("US 10Y yields rise to 3.2% by mid-Q2")
    assert s.claim_kind == "historical_forecast"
    assert s.allowed_use_in_phase_a == "phase_b_only"


def test_archived_opinion_is_phase_b_only():
    s, _ = _status("we remain neutral on the market")
    assert s.claim_kind == "source_opinion"
    assert s.allowed_use_in_phase_a == "phase_b_only"


def test_current_input_historical_forecast_is_current_input_evidence():
    s, _ = _status("US 10Y yields rise to 3.2% by mid-Q2", is_current_input=True)
    assert s.claim_kind == "historical_forecast"      # source is still old (2019)
    assert s.allowed_use_in_phase_a == "current_input_evidence"


def test_forecast_verb_without_horizon_is_forecast_with_no_horizon():
    s, hz = _status("we expect European cyclicals to keep outperforming")
    assert s.claim_kind == "historical_forecast"
    assert hz == []                                   # no datable horizon ⇒ no ForecastHorizon
    assert s.temporal_status in ("expired", "stale")


def test_opinion_with_horizon_is_a_forecast():
    s, _ = _status("we remain overweight banks, with 15% upside by Q3")
    assert s.claim_kind == "historical_forecast"      # opinion + horizon ⇒ positioned forecast


def test_method_claim_is_method_context():
    s, _ = _status("do-calculus separates correlation from causation", access="method", src=None)
    assert s.claim_kind == "method_rule"
    assert s.temporal_status == "timeless_method"
    assert s.allowed_use_in_phase_a == "method_context"


def test_non_method_never_method_context():
    for icur in (True, False):
        s, _ = _status("US 10Y yields rise to 3.2% by mid-Q2", is_current_input=icur)
        assert s.allowed_use_in_phase_a != "method_context"


def test_agent_classifies_atoms_causal_claims_and_family_hints():
    bundle = EvidenceExtractionBundle(
        source_slug="eq",
        evidence_atoms=[EvidenceAtom(evidence_id="e1", source_slug="eq", source_location="page:2",
                                     claim="Stoxx 600 is 8% above fair value", claim_kind="source_fact")],
        source_page_fields={"source_date": "2019-03-15"},
        causal_claims=[CausalClaimCandidate(driver="China credit impulse", transmission="drives",
                                            outcome="China PMI improvement", confidence=0.5, rationale="r")],
        strategy_family_hints=[StrategyFamilyHint(family="long_short", rationale="relative-value spread",
                                                  confidence=0.5)])
    cls = SourceClassification(source_slug="eq", source_type="report", access_class="case",
                               copyright_status="x", ingestion_policy="extract_evidence_atoms_case",
                               recommended_compilers=["EvidenceExtractionAgent"])
    out = TemporalContextAgent().run(TemporalContextInput(
        source_classification=cls, extraction_bundle=bundle, current_date=CUR))
    ids = {c.claim_id for c in out.claim_statuses}
    assert any(i.startswith("causal-") for i in ids)
    assert any(i.startswith("family-") for i in ids)
    assert all(c.allowed_use_in_phase_a != "method_context" for c in out.claim_statuses)
