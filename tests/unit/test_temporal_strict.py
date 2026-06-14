"""L5 — fail-closed temporal grounding for strict/discovery extraction runs.

Acceptance (plan §2 L5): with require_current_date=True, a missing or unparseable current_date
RAISES MissingCurrentDateError instead of silently degrading (the 'old report reads as current'
path). Default (False) keeps the back-compatible warn-and-skip behavior.
"""
from __future__ import annotations

import pytest

from engine.evidence_extraction import EvidenceExtractionInput
from engine.temporal import MissingCurrentDateError
from engine.wiki_agents import EvidenceExtractionAgent, _TEMPORAL_MISSING_DATE_WARNING

AGENT = EvidenceExtractionAgent()

_MD = "Spreads widened on heavy primary supply. PPI minus CPI compressed."


def _inp(**kw):
    base = dict(source_slug="acme-report", source_type="report", access_class="case",
                normalized_markdown=_MD)
    base.update(kw)
    return EvidenceExtractionInput(**base)


# ── default (back-compatible): warn-and-skip ──────────────────────────────────────────

def test_default_missing_date_warns_and_does_not_raise():
    bundle = AGENT.run(_inp())                      # no source_date / current_date
    assert _TEMPORAL_MISSING_DATE_WARNING in bundle.extraction_warnings
    assert bundle.temporal_context is None


# ── strict: fail-closed ───────────────────────────────────────────────────────────────

def test_strict_missing_current_date_raises():
    with pytest.raises(MissingCurrentDateError):
        AGENT.run(_inp(source_date="2019-03-15", require_current_date=True))  # no current_date


def test_strict_missing_source_date_raises():
    with pytest.raises(MissingCurrentDateError):
        AGENT.run(_inp(current_date="2026-06-12", require_current_date=True))  # no source_date


def test_strict_unparseable_current_date_raises():
    with pytest.raises(MissingCurrentDateError):
        AGENT.run(_inp(source_date="2019-03-15", current_date="not-a-date",
                       require_current_date=True))


def test_strict_with_valid_dates_succeeds_and_grounds():
    bundle = AGENT.run(_inp(source_date="2019-03-15", current_date="2026-06-12",
                            require_current_date=True))
    assert bundle.temporal_context is not None
    assert _TEMPORAL_MISSING_DATE_WARNING not in bundle.extraction_warnings
