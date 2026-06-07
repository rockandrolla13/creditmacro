"""Q4 probability engine (PART 2) — validate / wrap / tilt / justify / quality.
Deterministic provenance & discipline layer: never invents or generates p_s."""
from __future__ import annotations

import pytest

from engine.probability import (
    apply_evidence_tilt,
    justify_probabilities,
    probability_quality,
    validate_probability_vector,
    wrap_supplied_probabilities,
)
from engine.schema import ProbabilityEvidenceBundle, ProbabilityEvidenceRef, Scenario


def _scen(name, p):
    return Scenario(name=name, p_s=p, driver_path="", implied_axis_value=50.0, pnl_per_unit=0.0)


def _ref(scenario, direction="increase", s=0.9, r=0.9, f=0.9, slug=None):
    return ProbabilityEvidenceRef(
        source_slug=slug, claim="evidence", direction=direction, scenario_impacted=scenario,
        strength=s, reliability=r, freshness=f, rationale="why",
    )


def _two():
    return [_scen("A", 0.5), _scen("B", 0.5)]


# ── 1. validate ───────────────────────────────────────────────────────────────

def test_validate_flags_unnormalised_without_raising():
    ok, warns = validate_probability_vector([_scen("A", 0.6), _scen("B", 0.6)])
    assert ok is False and any("sum" in w for w in warns)
    ok2, _ = validate_probability_vector(_two())
    assert ok2 is True


# ── 2. wrap (no-evidence default) ─────────────────────────────────────────────

def test_wrap_labels_pm_assumption_with_warning_and_capped_quality():
    j = wrap_supplied_probabilities(_two())
    assert all(r.posterior_source == "PM_assumption" for r in j.scenario_probabilities)
    assert all(r.posterior_probability == r.prior_probability for r in j.scenario_probabilities)
    assert j.probability_quality <= 0.50 + 1e-9
    assert "Probabilities supplied but not evidence-justified." in j.warnings
    assert j.effective_probability_vector == [0.5, 0.5]


# ── 3. evidence tilt (deterministic) ──────────────────────────────────────────

def test_tilt_moves_toward_increase_evidence_and_is_haircut_and_deterministic():
    priors = {"A": 0.5, "B": 0.5}
    ev = {"A": [_ref("A", "increase")]}
    post, ec = apply_evidence_tilt(priors, ev)
    assert post["A"] > 0.5 > post["B"]                      # tilted toward A
    assert post["A"] < 0.6745                               # haircut vs full softmax (ec<1)
    assert abs(sum(post.values()) - 1.0) < 1e-9            # still a distribution
    assert 0.0 < ec < 1.0
    assert apply_evidence_tilt(priors, ev) == (post, ec)    # deterministic


def test_decrease_evidence_tilts_away():
    post, _ = apply_evidence_tilt({"A": 0.5, "B": 0.5}, {"A": [_ref("A", "decrease")]})
    assert post["A"] < 0.5 < post["B"]


# ── 4. justify (orchestrator, new signature) ──────────────────────────────────

def test_justify_no_evidence_falls_back_to_wrap():
    j = justify_probabilities(None, _two(), evidence_bundle=None)
    assert all(r.posterior_source == "PM_assumption" for r in j.scenario_probabilities)
    assert j.effective_probability_vector == [0.5, 0.5]     # posterior == prior


def test_justify_with_evidence_is_evidence_weighted_and_effective_is_posterior():
    bundle = ProbabilityEvidenceBundle(evidence_by_scenario={
        "A": [_ref("A", "increase")], "B": [_ref("B", "decrease")],
    })
    j = justify_probabilities(None, _two(), evidence_bundle=bundle)
    rows = {r.scenario_name: r for r in j.scenario_probabilities}
    assert rows["A"].posterior_source == "evidence_weighted"
    assert j.effective_probability_vector[0] > 0.5          # A tilted up; posterior, not prior
    assert j.effective_probability_vector != [0.5, 0.5]
    assert abs(sum(j.effective_probability_vector) - 1.0) < 1e-9


def test_evidence_weighted_claimed_without_refs_downgrades_to_unknown():
    bundle = ProbabilityEvidenceBundle(prior_sources={"A": "evidence_weighted"})
    j = justify_probabilities(None, _two(), evidence_bundle=bundle)
    a = next(r for r in j.scenario_probabilities if r.scenario_name == "A")
    assert a.posterior_source == "unknown"
    assert any("evidence_weighted" in w and "unknown" in w for w in j.warnings)
    assert j.probability_quality <= 0.25 + 1e-9             # unknown caps the set


# ── 5. quality (contradiction lowers it) ──────────────────────────────────────

def test_contradictory_evidence_lowers_quality():
    clean = ProbabilityEvidenceBundle(evidence_by_scenario={
        "A": [_ref("A", "increase")], "B": [_ref("B", "increase")]})
    mixed = ProbabilityEvidenceBundle(evidence_by_scenario={
        "A": [_ref("A", "increase"), _ref("A", "contradictory")],
        "B": [_ref("B", "increase")]})
    qc = probability_quality(justify_probabilities(None, _two(), evidence_bundle=clean))
    qm = probability_quality(justify_probabilities(None, _two(), evidence_bundle=mixed))
    assert qm < qc


def test_probability_quality_matches_field():
    j = justify_probabilities(None, _two(), evidence_bundle=None)
    assert probability_quality(j) == pytest.approx(j.probability_quality)


# ── firewall gate heuristic (unchanged) ───────────────────────────────────────

def test_phase_a_gate_classifies_case_slugs():
    from engine.workflow import _is_case_evidence
    assert _is_case_evidence(_ref("A", slug="historical-base-rates-2024"))
    assert _is_case_evidence(_ref("A", slug="theme-2024-ai-steepener"))
    assert not _is_case_evidence(_ref("A", slug="concept-credit-curve"))
