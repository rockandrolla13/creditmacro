"""Temporal context + historical-case discipline — PART 1: schemas.

Pins the SHAPE and the firewall-critical invariants only. The classifier that POPULATES these
(detecting horizons, dating claims, routing to outcome evaluation) is a later part.
"""
from __future__ import annotations

from datetime import date

import pytest
from pydantic import ValidationError

from engine.temporal import ForecastHorizon, TemporalClaimStatus, TemporalContext


# ── ForecastHorizon ──────────────────────────────────────────────────────────

def _horizon(**kw):
    base = dict(claim="US 10Y rises to 3.2% by mid-Q2", horizon_text="by mid-Q2",
                horizon_type="quarter", status="active", outcome_check_required=False)
    base.update(kw)
    return ForecastHorizon(**base)


def test_horizon_constructs():
    h = _horizon()
    assert h.status == "active" and h.outcome_check_required is False


def test_expired_horizon_requires_outcome_check():
    with pytest.raises(ValidationError):
        _horizon(status="expired", outcome_check_required=False)
    assert _horizon(status="expired", outcome_check_required=True).outcome_check_required is True


def test_horizon_rejects_end_before_start():
    with pytest.raises(ValidationError):
        _horizon(forecast_start_date=date(2019, 6, 1), forecast_end_date=date(2019, 3, 1))


def test_horizon_rejects_bad_type():
    with pytest.raises(ValidationError):
        _horizon(horizon_type="fortnight")


# ── TemporalClaimStatus (firewall-critical) ──────────────────────────────────

def _claim(**kw):
    base = dict(claim_id="c1", claim_text="x", claim_kind="historical_fact",
                temporal_status="stale", allowed_use_in_phase_a="historical_context_only",
                rationale="r")
    base.update(kw)
    return TemporalClaimStatus(**base)


def test_method_rule_must_be_timeless_and_method_context():
    ok = _claim(claim_kind="method_rule", temporal_status="timeless_method",
                allowed_use_in_phase_a="method_context")
    assert ok.allowed_use_in_phase_a == "method_context"
    with pytest.raises(ValidationError):
        _claim(claim_kind="method_rule", temporal_status="stale",
               allowed_use_in_phase_a="method_context")


def test_non_method_claim_cannot_be_method_context():
    # a historical forecast can NEVER be loaded as method context in Phase A
    with pytest.raises(ValidationError):
        _claim(claim_kind="historical_forecast", temporal_status="expired",
               allowed_use_in_phase_a="method_context")
    with pytest.raises(ValidationError):
        _claim(claim_kind="current_fact", temporal_status="current",
               allowed_use_in_phase_a="method_context")


def test_timeless_status_requires_method_rule():
    with pytest.raises(ValidationError):
        _claim(claim_kind="historical_fact", temporal_status="timeless_method",
               allowed_use_in_phase_a="historical_context_only")


def test_historical_forecast_as_current_input_for_case_analysis_is_allowed():
    # allowed as current-input evidence ONLY because the document itself is the current input
    c = _claim(claim_kind="historical_forecast", temporal_status="expired",
               allowed_use_in_phase_a="current_input_evidence")
    assert c.allowed_use_in_phase_a == "current_input_evidence"


# ── TemporalContext ──────────────────────────────────────────────────────────

def _ctx(**kw):
    base = dict(source_slug="european-equity-strategy-2019-03-15",
                current_date=date(2026, 6, 9), temporal_role="historical_case",
                current_update_required=False)
    base.update(kw)
    return TemporalContext(**base)


def test_source_age_days_auto_computed():
    c = _ctx(source_date=date(2019, 3, 15))
    assert c.source_age_days == (date(2026, 6, 9) - date(2019, 3, 15)).days


def test_current_date_required():
    with pytest.raises(ValidationError):
        TemporalContext(source_slug="x", temporal_role="unknown", current_update_required=False)


def test_expired_forecasts_force_current_update_required():
    with pytest.raises(ValidationError):
        _ctx(expired_forecasts=["US 10Y to 3.2% by mid-Q2"], current_update_required=False)
    ok = _ctx(expired_forecasts=["US 10Y to 3.2% by mid-Q2"], current_update_required=True)
    assert ok.current_update_required is True


def test_expired_horizon_forces_current_update_required():
    h = ForecastHorizon(claim="…", horizon_type="quarter", status="expired",
                        outcome_check_required=True)
    with pytest.raises(ValidationError):
        _ctx(forecast_horizons=[h], current_update_required=False)
    assert _ctx(forecast_horizons=[h], current_update_required=True).current_update_required is True


def test_mechanisms_survive_even_when_forecasts_expired():
    h = ForecastHorizon(claim="…", horizon_type="quarter", status="expired",
                        outcome_check_required=True)
    c = _ctx(forecast_horizons=[h], current_update_required=True,
             still_relevant_mechanisms=["China credit impulse → China PMI"])
    assert c.still_relevant_mechanisms  # mechanisms can remain relevant despite expired forecasts
