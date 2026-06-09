"""Q4 PART-2c — PART 3 (justify bridge) + PART 6/7 deterministic JPM scenario fixtures.

No LLM. Fixtures supply explicit prior p_s and route the materialized JPM evidence atoms through
the mapper + posterior update. Posterior is an audit artifact; no trade legs / sizing / hedge
ratios / execution are produced anywhere.
"""
from __future__ import annotations

import json
from pathlib import Path

from engine.probability import justify_probabilities
from engine.probability_evidence import (
    ProbabilityUpdatePolicy,
    map_evidence_to_scenarios,
    update_probabilities_from_evidence,
)
from engine.schema import EvidenceAtom, Scenario

_JSONL = Path(__file__).resolve().parents[2] / "wiki" / "evidence" / "evidence_atoms.jsonl"


def _atoms():
    return [EvidenceAtom.from_record(json.loads(l))
            for l in _JSONL.read_text().splitlines() if l.strip()]


def _S(name, p, dp):
    return Scenario(name=name, p_s=p, driver_path=dp, implied_axis_value=0.0, pnl_per_unit=0.0)


def hpc_fixture():
    """Theme: HY HPC crowding and supply. Explicit priors; evidence = the materialized JPM atoms."""
    scns = [
        _S("momentum_continues", 0.35,
           "HY HPC crowding persists: heavy HPC issuance continues, HPC HY index weight keeps "
           "rising, HPC OAS tightens further, HPC total return outperforms HY"),
        _S("supply_absorbed", 0.30,
           "HPC issuance is absorbed; HPC HY index weight stabilises; HPC OAS holds steady"),
        _S("crowding_reversal", 0.20,
           "HPC crowding reverses: HPC OAS widens, HPC HY index weight falls on redemptions, "
           "HPC total return lags HY"),
        _S("risk_off_liquidity_gap", 0.15,
           "broad risk-off liquidity gap; HY spreads gap wider across the board"),
    ]
    return scns, _atoms()


def index_fixture():
    """Theme: Data-center index inclusion technicals."""
    scns = [
        _S("index_inclusion_premium_persists", 0.40,
           "Data Center sub-sector inclusion in JULI drives index-tracking demand; the inclusion "
           "premium persists; Data Center OAS stays rich versus Technology"),
        _S("index_rule_convergence", 0.25,
           "index rules converge across JULI, Bloomberg US Agg, Bloomberg Global Agg and ICE; "
           "inclusion differences shrink"),
        _S("liquidity_premium_widens", 0.20,
           "limited syndication widens the liquidity premium on data-center project bonds"),
        _S("no_tradeable_technical", 0.15, "no tradeable technical emerges; flows are noise"),
    ]
    return scns, _atoms()


# ── PART 3: justify_probabilities bridge ────────────────────────────────────────

def test_justify_bridge_attaches_audit_and_moves_posterior():
    scns, atoms = hpc_fixture()
    js = justify_probabilities(None, scns, evidence_atoms=atoms)
    assert js.update_audit is not None
    assert js.update_audit.update_method == "softmax_evidence_tilt"
    assert js.effective_probability_vector == js.update_audit.posterior_vector
    assert js.probability_quality == js.update_audit.probability_quality
    assert js.effective_probability_vector != js.update_audit.prior_vector


def test_justify_bridge_no_evidence_posterior_equals_prior():
    scns = [_S("A", 0.6, "x"), _S("B", 0.4, "y")]
    js = justify_probabilities(None, scns, evidence_maps=[])
    assert js.update_audit.update_method == "posterior_equals_prior"
    assert js.effective_probability_vector == [0.6, 0.4]
    assert any("not evidence-weighted" in w.lower() for w in js.warnings)


def test_justify_bridge_no_scenarios_skips():
    js = justify_probabilities(None, [], evidence_maps=[])
    assert js.update_audit.update_method == "none"
    assert js.effective_probability_vector == []
    assert any("no supplied scenarios" in w.lower() for w in js.warnings)


# ── PART 7 test 14 — HY HPC fixture moves posterior in expected direction ───────

def test_jpm_hpc_posterior_moves_expected_direction():
    scns, atoms = hpc_fixture()
    maps = map_evidence_to_scenarios(scns, atoms)
    a = update_probabilities_from_evidence(scns, maps)
    post = dict(zip(a.scenario_names, a.posterior_vector))
    prior = dict(zip(a.scenario_names, a.prior_vector))
    assert a.update_method == "softmax_evidence_tilt"
    assert post != prior
    # the crowding-described momentum scenario gains; the no-evidence risk-off scenario loses
    assert post["momentum_continues"] > prior["momentum_continues"]
    assert post["risk_off_liquidity_gap"] < prior["risk_off_liquidity_gap"]
    assert abs(sum(a.posterior_vector) - 1.0) < 1e-9
    # single source ⇒ probability_quality capped; clustered evidence does not over-update
    assert a.probability_quality <= ProbabilityUpdatePolicy().single_source_quality_cap + 1e-9
    assert any("single-source" in w.lower() for w in a.warnings)
    move = max(abs(po - prior[n]) for n, po in post.items())
    assert move <= ProbabilityUpdatePolicy().max_posterior_move + 1e-9


# ── PART 7 test 15 — index-inclusion moves only where evidence maps ─────────────

def test_jpm_index_inclusion_moves_only_where_mapped():
    scns, atoms = index_fixture()
    maps = map_evidence_to_scenarios(scns, atoms)
    a = update_probabilities_from_evidence(scns, maps)
    by = {m.scenario_name: m for m in a.evidence_maps}
    post = dict(zip(a.scenario_names, a.posterior_vector))
    prior = dict(zip(a.scenario_names, a.prior_vector))
    # the "no tradeable technical" scenario attracts no evidence and does not gain
    assert by["no_tradeable_technical"].impacts == []
    assert post["no_tradeable_technical"] < prior["no_tradeable_technical"]
    # a cleanly-mapped scenario gains
    assert post["index_inclusion_premium_persists"] > prior["index_inclusion_premium_persists"]
    assert abs(sum(a.posterior_vector) - 1.0) < 1e-9


# ── PART 7 test 18 — no trade legs / sizing / hedge / execution emitted ─────────

def test_no_trade_output_in_probability_objects():
    scns, atoms = hpc_fixture()
    js = justify_probabilities(None, scns, evidence_atoms=atoms)
    blob = json.dumps(js.model_dump()).lower()
    for forbidden in ("hedge_ratio", "leg_", "position_size", "stop_loss", "execution", "dv01"):
        assert forbidden not in blob
    assert js.effective_probability_vector  # but it DOES carry the posterior audit
