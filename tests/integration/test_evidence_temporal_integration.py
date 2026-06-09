"""PART 9 — TemporalContextAgent integrated into EvidenceExtractionAgent output.

The EvidenceExtractionBundle OPTIONALLY carries temporal context (temporal_context,
temporal_claim_statuses, forecast_horizons). EvidenceExtractionAgent populates these by calling
TemporalContextAgent, but ONLY when BOTH source_date AND current_date are supplied. current_date is
NEVER implicit (no wall-clock default): if it is missing, temporal context is not computed and an
exact warning fires. Backward compatibility: runs with no temporal args behave exactly as before.
"""
from __future__ import annotations

from datetime import date

from engine.evidence_extraction import EvidenceExtractionInput, EvidenceExtractionBundle
from engine.temporal import ForecastHorizon, TemporalClaimStatus, TemporalContext
from engine.wiki_agents import EvidenceExtractionAgent

WARN_NO_DATE = "Temporal context not computed; current_date missing."

# A 2019 report with dated, now-expired forecasts → temporal context routes it as historical/expired.
OLD_MD = """
<!-- page:3 -->
US 10-year yields are expected to rise to 3.2% by mid-Q2, and Bund yields to 0.6% by Q3.
<!-- page:2 -->
Stoxx 600 trades 8% above model fair value because the China credit impulse drives PMI improvement.
"""


def _run(md, slug="src", **kw):
    return EvidenceExtractionAgent().run(EvidenceExtractionInput(
        source_slug=slug, source_type="report", access_class="case",
        normalized_markdown=md, **kw))


# ── 1. both dates supplied → temporal context populated ──────────────────────────

def test_temporal_context_populated_when_both_dates_supplied():
    b = _run(OLD_MD, slug="eu-2019", source_date="2019-03-15", current_date="2026-06-09")
    assert isinstance(b, EvidenceExtractionBundle)
    assert b.temporal_context is not None
    assert isinstance(b.temporal_context, TemporalContext)
    assert b.temporal_context.current_date == date(2026, 6, 9)
    assert b.temporal_context.source_date == date(2019, 3, 15)
    # claim statuses populated, one per classified claim
    assert b.temporal_claim_statuses
    assert all(isinstance(s, TemporalClaimStatus) for s in b.temporal_claim_statuses)
    # forecast horizons carried through (dated forecasts present)
    assert all(isinstance(h, ForecastHorizon) for h in b.forecast_horizons)
    assert b.forecast_horizons, "dated forecasts should yield forecast horizons"
    # no missing-date warning when both dates are present
    assert WARN_NO_DATE not in b.extraction_warnings


# ── 2. current_date missing → not computed + exact warning ───────────────────────

def test_no_current_date_emits_exact_warning_and_no_context():
    b = _run(OLD_MD, slug="eu-2019", source_date="2019-03-15")  # current_date omitted
    assert b.temporal_context is None
    assert b.temporal_claim_statuses == []
    assert b.forecast_horizons == []
    assert WARN_NO_DATE in b.extraction_warnings


# ── 3. current_date is never implicit (no wall-clock fallback) ───────────────────

def test_current_date_not_implicit_from_today():
    b = _run(OLD_MD, slug="eu-2019", source_date="2019-03-15")
    # the agent must NOT silently substitute today's date and compute a context
    assert b.temporal_context is None
    assert WARN_NO_DATE in b.extraction_warnings


def test_source_date_present_but_current_missing_still_warns():
    # source_date alone is not enough — current_date is the missing piece named in the warning
    b = _run(OLD_MD, slug="eu-2019", source_date="2026-01-01")
    assert b.temporal_context is None
    assert WARN_NO_DATE in b.extraction_warnings


# ── 4. backward compatibility: no temporal args → behaves as before ──────────────

def test_backward_compatible_defaults_when_no_temporal_args():
    b = _run(OLD_MD, slug="eu-2019")  # no source_date, no current_date
    assert isinstance(b, EvidenceExtractionBundle)
    assert b.temporal_context is None
    assert b.temporal_claim_statuses == []
    assert b.forecast_horizons == []
    # source_date missing → the exact current_date-missing warning fires (both must be present)
    assert WARN_NO_DATE in b.extraction_warnings
    # existing extraction output is unaffected
    assert b.evidence_atoms
    assert b.strategy_family_hints


def test_only_current_date_supplied_no_source_date_warns():
    b = _run(OLD_MD, slug="eu-2019", current_date="2026-06-09")  # source_date omitted
    assert b.temporal_context is None
    assert WARN_NO_DATE in b.extraction_warnings
