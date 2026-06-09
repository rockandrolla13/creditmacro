"""PART 1 — schema for the Q4 evidence-to-posterior bridge.

These tests pin the SHAPE and the schema-enforceable invariants only. The posterior-update
MATH (likelihood-ratio combination, softmax tilt, quality capping) is PART 2 and is not
exercised here. Rules covered:
  R1  an evidence-weighted method (log_likelihood_ratio / softmax_evidence_tilt) cannot be
      claimed without >= 1 ScenarioEvidenceImpact.
  R2  no scenarios supplied  ->  update_method == "none" and empty vectors.
  R3  scenarios supplied but no impacts  ->  update_method == "posterior_equals_prior" and
      posterior == prior.
Structural: vector / scenario_name / evidence_map lengths agree; counts are consistent with
the impacts they summarise.
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from engine.schema import (
    ProbabilityUpdateAudit,
    ScenarioEvidenceImpact,
    ScenarioEvidenceMap,
)


# ── builders ──────────────────────────────────────────────────────────────────

def _impact(scenario="Wider", direction="increase", cluster=None, lr=None, **kw):
    base = dict(
        scenario_name=scenario,
        claim="IG net issuance surged in Q2",
        claim_kind="source_fact",
        direction=direction,
        likelihood_ratio=lr,
        strength=0.8,
        reliability=0.7,
        freshness=0.9,
        independence_weight=1.0,
        evidence_cluster_id=cluster,
        rationale="net supply pressure widens spreads",
    )
    base.update(kw)
    return ScenarioEvidenceImpact(**base)


def _map(scenario="Wider", impacts=None, **kw):
    impacts = impacts if impacts is not None else []
    base = dict(
        scenario_name=scenario,
        impacts=impacts,
        evidence_for_count=sum(1 for i in impacts if i.direction == "increase"),
        evidence_against_count=sum(1 for i in impacts if i.direction == "decrease"),
        contradiction_count=sum(1 for i in impacts if i.direction == "contradictory"),
        cluster_count=len({i.evidence_cluster_id for i in impacts if i.evidence_cluster_id}),
        mapping_confidence=0.6,
        warnings=[],
    )
    base.update(kw)
    return ScenarioEvidenceMap(**base)


# ── ScenarioEvidenceImpact ──────────────────────────────────────────────────────

def test_impact_constructs_with_required_fields():
    imp = _impact()
    assert imp.scenario_name == "Wider"
    assert imp.claim_kind == "source_fact"
    assert imp.direction == "increase"
    assert imp.likelihood_ratio is None  # optional


def test_impact_rejects_strength_out_of_range():
    with pytest.raises(ValidationError):
        _impact(strength=1.5)


def test_impact_rejects_independence_weight_out_of_range():
    with pytest.raises(ValidationError):
        _impact(independence_weight=-0.1)


def test_impact_rejects_nonpositive_likelihood_ratio():
    # a likelihood ratio is by definition > 0; 0 or negative is meaningless
    with pytest.raises(ValidationError):
        _impact(lr=0.0)
    with pytest.raises(ValidationError):
        _impact(lr=-2.0)


def test_impact_accepts_positive_likelihood_ratio():
    assert _impact(lr=3.5).likelihood_ratio == 3.5


def test_impact_rejects_unknown_claim_kind():
    with pytest.raises(ValidationError):
        _impact(claim_kind="rumour")


def test_impact_rejects_unknown_direction():
    with pytest.raises(ValidationError):
        _impact(direction="up")


# ── ScenarioEvidenceMap ──────────────────────────────────────────────────────────

def test_map_constructs_empty():
    m = _map()
    assert m.impacts == []
    assert m.contradiction_count == 0
    assert m.cluster_count == 0


def test_map_contradiction_count_must_match_impacts():
    impacts = [_impact(direction="contradictory")]
    with pytest.raises(ValidationError):
        _map(impacts=impacts, contradiction_count=0)  # lies about the data


def test_map_cluster_count_must_match_distinct_clusters():
    impacts = [_impact(cluster="src-A"), _impact(cluster="src-A"), _impact(cluster="src-B")]
    _map(impacts=impacts, cluster_count=2)  # ok: 2 distinct clusters
    with pytest.raises(ValidationError):
        _map(impacts=impacts, cluster_count=3)  # only 2 distinct


def test_map_counts_cannot_exceed_impacts():
    with pytest.raises(ValidationError):
        _map(impacts=[_impact()], evidence_for_count=5)


# ── ProbabilityUpdateAudit ───────────────────────────────────────────────────────

def test_audit_no_scenarios_is_none_method():
    a = ProbabilityUpdateAudit(
        prior_vector=[], posterior_vector=[], scenario_names=[], evidence_maps=[],
        update_method="none", probability_quality=0.0, warnings=[],
    )
    assert a.update_method == "none"


def test_audit_no_scenarios_rejects_non_none_method():
    with pytest.raises(ValidationError):
        ProbabilityUpdateAudit(
            prior_vector=[], posterior_vector=[], scenario_names=[], evidence_maps=[],
            update_method="softmax_evidence_tilt", probability_quality=0.0, warnings=[],
        )


def test_audit_scenarios_no_impacts_is_posterior_equals_prior():
    a = ProbabilityUpdateAudit(
        prior_vector=[0.6, 0.4], posterior_vector=[0.6, 0.4],
        scenario_names=["Wider", "Tighter"],
        evidence_maps=[_map("Wider"), _map("Tighter")],
        update_method="posterior_equals_prior", probability_quality=0.5, warnings=[],
    )
    assert a.posterior_vector == a.prior_vector


def test_audit_scenarios_no_impacts_rejects_moved_posterior():
    with pytest.raises(ValidationError):
        ProbabilityUpdateAudit(
            prior_vector=[0.6, 0.4], posterior_vector=[0.7, 0.3],
            scenario_names=["Wider", "Tighter"],
            evidence_maps=[_map("Wider"), _map("Tighter")],
            update_method="posterior_equals_prior", probability_quality=0.5, warnings=[],
        )


def test_audit_scenarios_no_impacts_rejects_evidence_method():
    # R1 + R3: no impacts, so an evidence-weighted method is not permitted
    with pytest.raises(ValidationError):
        ProbabilityUpdateAudit(
            prior_vector=[0.6, 0.4], posterior_vector=[0.6, 0.4],
            scenario_names=["Wider", "Tighter"],
            evidence_maps=[_map("Wider"), _map("Tighter")],
            update_method="softmax_evidence_tilt", probability_quality=0.5, warnings=[],
        )


def test_audit_evidence_method_with_impact_is_valid():
    m_wider = _map("Wider", impacts=[_impact("Wider", "increase")])
    a = ProbabilityUpdateAudit(
        prior_vector=[0.6, 0.4], posterior_vector=[0.65, 0.35],
        scenario_names=["Wider", "Tighter"],
        evidence_maps=[m_wider, _map("Tighter")],
        update_method="softmax_evidence_tilt", probability_quality=0.55, warnings=[],
    )
    assert a.update_method == "softmax_evidence_tilt"


def test_audit_log_likelihood_ratio_requires_impact():
    with pytest.raises(ValidationError):
        ProbabilityUpdateAudit(
            prior_vector=[0.6, 0.4], posterior_vector=[0.6, 0.4],
            scenario_names=["Wider", "Tighter"],
            evidence_maps=[_map("Wider"), _map("Tighter")],
            update_method="log_likelihood_ratio", probability_quality=0.5, warnings=[],
        )


def test_audit_rejects_vector_length_mismatch():
    with pytest.raises(ValidationError):
        ProbabilityUpdateAudit(
            prior_vector=[0.6, 0.4], posterior_vector=[0.6],  # wrong length
            scenario_names=["Wider", "Tighter"],
            evidence_maps=[_map("Wider"), _map("Tighter")],
            update_method="posterior_equals_prior", probability_quality=0.5, warnings=[],
        )


def test_audit_rejects_evidence_map_for_unknown_scenario():
    with pytest.raises(ValidationError):
        ProbabilityUpdateAudit(
            prior_vector=[0.6, 0.4], posterior_vector=[0.6, 0.4],
            scenario_names=["Wider", "Tighter"],
            evidence_maps=[_map("Wider"), _map("Ghost")],  # "Ghost" not a scenario
            update_method="posterior_equals_prior", probability_quality=0.5, warnings=[],
        )
