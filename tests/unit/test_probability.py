"""Q4 — justify_probabilities rule coverage. Pure, audit-only: it labels supplied p_s, caps
quality by the weakest source, and NEVER invents, mutates, or raises."""
from __future__ import annotations

from engine.probability import justify_probabilities
from engine.schema import ProbabilityEvidenceRef, Scenario


def _scen(name, p):
    return Scenario(name=name, p_s=p, driver_path="", implied_axis_value=50.0, pnl_per_unit=0.0)


def _ref(scenario, direction="increase", s=0.8, r=0.8, f=0.8):
    return ProbabilityEvidenceRef(
        claim="evidence", direction=direction, scenario_impacted=scenario,
        strength=s, reliability=r, freshness=f, rationale="why",
    )


def _two():
    return [_scen("A", 0.6), _scen("B", 0.4)]


# ── provenance + caps ─────────────────────────────────────────────────────────

def test_naked_probabilities_are_pm_assumption_and_capped():
    j = justify_probabilities(_two())
    assert all(r.posterior_source == "PM_assumption" for r in j.scenario_probabilities)
    assert j.probability_quality <= 0.50 + 1e-9                # PM_assumption ceiling
    assert all(r.unresolved_questions for r in j.scenario_probabilities)


def test_evidence_weighted_claimed_without_refs_downgrades_to_unknown():
    j = justify_probabilities(_two(), prior_sources={"A": "evidence_weighted"})
    a = next(r for r in j.scenario_probabilities if r.scenario_name == "A")
    assert a.posterior_source == "unknown"
    assert any("evidence_weighted" in w and "unknown" in w for w in j.warnings)
    assert j.probability_quality <= 0.25 + 1e-9                # unknown caps the set


def test_refs_make_it_evidence_weighted_and_confidence_below_inputs():
    j = justify_probabilities(_two(), evidence={"A": [_ref("A")], "B": [_ref("B")]})
    rows = {r.scenario_name: r for r in j.scenario_probabilities}
    assert rows["A"].posterior_source == "evidence_weighted"
    assert rows["A"].evidence_for and not rows["A"].evidence_against
    assert rows["A"].confidence <= 0.8 * 0.8 * 0.8 + 1e-9      # mean(s*r*f)


def test_evidence_against_is_separated():
    j = justify_probabilities(_two(), evidence={"A": [_ref("A", direction="contradictory")]})
    a = next(r for r in j.scenario_probabilities if r.scenario_name == "A")
    assert a.evidence_against and not a.evidence_for


# ── audit-only invariants ─────────────────────────────────────────────────────

def test_effective_vector_equals_supplied_and_posterior_equals_prior():
    scen = _two()
    j = justify_probabilities(scen, evidence={"A": [_ref("A")]})
    assert j.effective_probability_vector == [s.p_s for s in scen]
    for r in j.scenario_probabilities:
        assert r.posterior_probability == r.prior_probability


def test_phase_a_gate_drops_case_evidence(monkeypatch):
    # The workflow's phase-A gate strips case-class refs (slug markers) before justifying,
    # so a discovery theme can't be evidence_weighted off historical/case pages.
    from engine.workflow import _is_case_evidence
    assert _is_case_evidence(_ref_with_slug("historical-base-rates-2024"))
    assert _is_case_evidence(_ref_with_slug("theme-2024-ai-steepener"))
    assert not _is_case_evidence(_ref_with_slug("concept-credit-curve"))


def _ref_with_slug(slug):
    return ProbabilityEvidenceRef(
        source_slug=slug, claim="x", direction="increase", scenario_impacted="A",
        strength=0.9, reliability=0.9, freshness=0.9, rationale="y",
    )


def test_unnormalised_set_warns_and_caps_quality_without_raising():
    j = justify_probabilities([_scen("A", 0.6), _scen("B", 0.6)])   # sums to 1.2
    assert j.sums_to_one is False
    assert any("sum" in w for w in j.warnings)
    assert j.probability_quality <= 0.25 + 1e-9
    # and the supplied probabilities are preserved, not normalised
    assert j.effective_probability_vector == [0.6, 0.6]
