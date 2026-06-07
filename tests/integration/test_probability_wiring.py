"""Q4 wiring — the justification attaches to the ThemeObject, audit-only, and the golden
master is byte-for-byte unchanged (the effective vector never feeds run_pricing)."""
from __future__ import annotations

import pytest

from tests._helpers import build_theme


def test_expression_attaches_justification_and_stays_golden():
    _, theme, _ = build_theme("ai_issuance.yaml", "expression")
    j = theme.probability_justification
    assert j is not None
    # no supplied evidence ⇒ PM_assumption, capped quality, and the effective vector is the
    # supplied p_s exactly.
    assert all(r.posterior_source == "PM_assumption" for r in j.scenario_probabilities)
    assert j.probability_quality <= 0.50 + 1e-9
    assert j.effective_probability_vector == [s.p_s for s in theme.scenarios]
    # GOLDEN MASTER — unchanged by Q4.
    assert theme.pricing.scenario_fv == pytest.approx(75.0, abs=1e-6)
    assert theme.pricing.residual_edge == pytest.approx(20.0, abs=1e-6)


def test_discovery_attaches_justification():
    _, theme, _ = build_theme("discovery/jpm_ai_capex.yaml", "discovery")
    assert theme.status == "strategy_family_routed"
    assert theme.probability_justification is not None
    assert theme.probability_justification.sums_to_one is True
