"""Q4 PART-2c — deterministic posterior update engine (PARTS 1+2).

update_probabilities_from_evidence(scenarios, evidence_maps, policy=None) -> ProbabilityUpdateAudit
compute_probability_quality(scenarios, evidence_maps, policy=None) -> float

Posterior is an AUDIT artifact; pricing keeps reading Scenario.p_s, so the golden master is
untouched. Updates are conservative: clustered / single-source / single-cluster / contradictory
evidence move the posterior less and cap probability_quality.
"""
from __future__ import annotations

from engine.probability_evidence import (
    ProbabilityUpdatePolicy,
    compute_probability_quality,
    update_probabilities_from_evidence,
)
from engine.schema import Scenario, ScenarioEvidenceImpact, ScenarioEvidenceMap

POL = ProbabilityUpdatePolicy()


def _scn(name, p):
    return Scenario(name=name, p_s=p, driver_path="", implied_axis_value=0.0, pnl_per_unit=0.0)


def _imp(scn, direction="increase", rel=0.9, fresh=1.0, indep=1.0, strength=0.8,
         cluster="c", source="src", kind="source_fact"):
    return ScenarioEvidenceImpact(
        scenario_name=scn, claim="x", claim_kind=kind, direction=direction, strength=strength,
        reliability=rel, freshness=fresh, independence_weight=indep, evidence_cluster_id=cluster,
        source_slug=source, rationale="r")


def _map(scn, impacts):
    return ScenarioEvidenceMap(
        scenario_name=scn, impacts=impacts,
        evidence_for_count=sum(1 for i in impacts if i.direction == "increase"),
        evidence_against_count=sum(1 for i in impacts if i.direction == "decrease"),
        contradiction_count=sum(1 for i in impacts if i.direction == "contradictory"),
        cluster_count=len({i.evidence_cluster_id for i in impacts if i.evidence_cluster_id}),
        mapping_confidence=0.6, warnings=[])


# 1
def test_no_scenarios_skips_update():
    a = update_probabilities_from_evidence([], [])
    assert a.update_method == "none"
    assert a.posterior_vector == [] and a.scenario_names == []
    assert any("no supplied scenarios" in w.lower() for w in a.warnings)


# 2
def test_no_evidence_posterior_equals_prior():
    scns = [_scn("A", 0.6), _scn("B", 0.4)]
    a = update_probabilities_from_evidence(scns, [_map("A", []), _map("B", [])])
    assert a.update_method == "posterior_equals_prior"
    assert a.posterior_vector == a.prior_vector == [0.6, 0.4]
    assert any("not evidence-weighted" in w.lower() for w in a.warnings)
    assert a.probability_quality <= POL.no_evidence_quality_cap + 1e-9


def test_empty_evidence_list_normalizes_to_prior():
    scns = [_scn("A", 0.6), _scn("B", 0.4)]
    a = update_probabilities_from_evidence(scns, [])
    assert a.update_method == "posterior_equals_prior"
    assert a.posterior_vector == [0.6, 0.4]


# 3
def test_evidence_weighted_moves_posterior():
    scns = [_scn("A", 0.5), _scn("B", 0.5)]
    maps = [_map("A", [_imp("A", cluster="c1", source="s1"), _imp("A", cluster="c2", source="s2")]),
            _map("B", [])]
    a = update_probabilities_from_evidence(scns, maps)
    assert a.update_method == "softmax_evidence_tilt"
    assert a.posterior_vector[0] > a.prior_vector[0]


# 4
def test_posterior_sums_to_one():
    scns = [_scn("A", 0.5), _scn("B", 0.3), _scn("C", 0.2)]
    maps = [_map("A", [_imp("A", cluster="c1", source="s1")]),
            _map("B", [_imp("B", cluster="c2", source="s2")]), _map("C", [])]
    a = update_probabilities_from_evidence(scns, maps)
    assert abs(sum(a.posterior_vector) - 1.0) < 1e-9
    assert all(p >= 0.0 for p in a.posterior_vector)


# 5
def test_posterior_move_is_bounded():
    scns = [_scn("A", 0.5), _scn("B", 0.5)]
    maps = [_map("A", [_imp("A", cluster=f"c{i}", source=f"s{i}", strength=1.0) for i in range(8)]),
            _map("B", [])]
    pol = ProbabilityUpdatePolicy(max_posterior_move=0.2)
    a = update_probabilities_from_evidence(scns, maps, pol)
    assert a.posterior_vector[0] - a.prior_vector[0] <= 0.2 + 1e-9


# 6
def test_same_cluster_evidence_is_downweighted():
    scns = [_scn("A", 0.5), _scn("B", 0.5)]
    clustered = [_imp("A", cluster="c", source="s", indep=0.25) for _ in range(4)]
    independent = [_imp("A", cluster=f"c{i}", source=f"s{i}", indep=1.0) for i in range(4)]
    a_c = update_probabilities_from_evidence(scns, [_map("A", clustered), _map("B", [])])
    a_i = update_probabilities_from_evidence(scns, [_map("A", independent), _map("B", [])])
    assert (a_c.posterior_vector[0] - 0.5) < (a_i.posterior_vector[0] - 0.5)


# 7
def test_single_source_caps_quality():
    scns = [_scn("A", 0.5), _scn("B", 0.5)]
    maps = [_map("A", [_imp("A", cluster=f"c{i}", source="onlysrc") for i in range(3)]), _map("B", [])]
    a = update_probabilities_from_evidence(scns, maps)
    assert a.probability_quality <= POL.single_source_quality_cap + 1e-9


# 8
def test_single_cluster_caps_quality():
    scns = [_scn("A", 0.5), _scn("B", 0.5)]
    maps = [_map("A", [_imp("A", cluster="c", source=f"s{i}") for i in range(3)]), _map("B", [])]
    a = update_probabilities_from_evidence(scns, maps)
    assert a.probability_quality <= POL.single_cluster_quality_cap + 1e-9


# 9
def test_contradiction_lowers_quality():
    scns = [_scn("A", 0.5), _scn("B", 0.5)]
    base = [_imp("A", cluster=f"c{i}", source=f"s{i}") for i in range(3)]
    contra = base + [_imp("A", direction="contradictory", cluster="c0", source="s0")]
    q_base = compute_probability_quality(scns, [_map("A", base), _map("B", [])])
    q_con = compute_probability_quality(scns, [_map("A", contra), _map("B", [])])
    assert q_con < q_base


# 10
def test_source_fact_quality_exceeds_opinion():
    scns = [_scn("A", 0.5), _scn("B", 0.5)]
    def q(kind, rel):
        maps = [_map("A", [_imp("A", cluster=f"c{i}", source=f"s{i}", kind=kind, rel=rel) for i in range(3)]),
                _map("B", [])]
        return compute_probability_quality(scns, maps)
    assert q("source_fact", 0.9) > q("source_opinion", 0.4)


# 11
def test_zero_impact_maps_are_posterior_equals_prior():
    scns = [_scn("A", 0.6), _scn("B", 0.4)]
    a = update_probabilities_from_evidence(scns, [_map("A", []), _map("B", [])])
    assert a.update_method == "posterior_equals_prior"
    assert a.posterior_vector == [0.6, 0.4]


def test_multiple_clusters_raise_quality_above_single_cluster():
    scns = [_scn("A", 0.5), _scn("B", 0.5)]
    one = [_map("A", [_imp("A", cluster="c", source=f"s{i}") for i in range(3)]), _map("B", [])]
    many = [_map("A", [_imp("A", cluster=f"c{i}", source=f"s{i}") for i in range(3)]), _map("B", [])]
    assert compute_probability_quality(scns, many) > compute_probability_quality(scns, one)


def test_audit_is_valid_and_one_map_per_scenario():
    scns = [_scn("A", 0.5), _scn("B", 0.5)]
    a = update_probabilities_from_evidence(scns, [_map("A", [_imp("A", cluster="c1", source="s1")]), _map("B", [])])
    assert len(a.evidence_maps) == 2
    assert [m.scenario_name for m in a.evidence_maps] == ["A", "B"]
