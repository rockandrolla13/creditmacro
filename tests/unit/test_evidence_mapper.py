"""Q4 PART-2b — deterministic evidence-to-scenario mapper.

map_evidence_to_scenarios(scenarios, evidence_atoms, causal_object=None, policy=None)
  -> list[ScenarioEvidenceMap]   (exactly one map per supplied scenario)

It never generates scenarios and never touches p_s; it only routes supplied evidence atoms to
the supplied scenarios, classifies/weights them, clusters to avoid double-counting, and records
warnings for atoms it cannot map.
"""
from __future__ import annotations

import pytest

from engine.probability_evidence import classify_claim_kind, map_evidence_to_scenarios
from engine.schema import EvidenceAtom, Scenario, ScenarioEvidenceMap


def _scn(name, driver_path, p_s=0.5):
    return Scenario(name=name, p_s=p_s, driver_path=driver_path,
                    implied_axis_value=0.0, pnl_per_unit=0.0)


def _atom(claim="x", themes=None, mvars=None, numbers=None, kind=None, **kw):
    return EvidenceAtom(
        claim=claim, claim_kind=kind, themes=themes or [], market_variables=mvars or [],
        numbers=numbers or [], **kw,
    )


# ── shape: one map per scenario, no generation, no p_s ──────────────────────────

def test_returns_one_map_per_scenario_in_order():
    scns = [_scn("Wider", "HPC OAS widens"), _scn("Tighter", "HPC OAS tightens")]
    maps = map_evidence_to_scenarios(scns, [])
    assert [m.scenario_name for m in maps] == ["Wider", "Tighter"]
    assert all(isinstance(m, ScenarioEvidenceMap) for m in maps)


def test_no_evidence_yields_empty_maps():
    maps = map_evidence_to_scenarios([_scn("Wider", "spreads widen")], [])
    assert maps[0].impacts == [] and maps[0].cluster_count == 0


# ── mapping: atoms route to overlapping scenarios only ──────────────────────────

def test_atom_maps_to_overlapping_scenario():
    scns = [_scn("HPCcrowds", "HY HPC index weight rises and HPC OAS tightens"),
            _scn("Unrelated", "sovereign curve bear steepens")]
    atom = _atom(claim="HPC index weight rose", themes=["hy-hpc-crowding-and-supply"],
                 mvars=["HPC HY index weight"])
    maps = {m.scenario_name: m for m in map_evidence_to_scenarios(scns, [atom])}
    assert len(maps["HPCcrowds"].impacts) == 1
    assert maps["HPCcrowds"].impacts[0].direction == "increase"   # default: corroborates the state
    assert maps["Unrelated"].impacts == []


def test_unmapped_atom_is_unused_and_warns():
    scns = [_scn("Wider", "IG cash-CDS basis widens")]
    atom = _atom(claim="unrelated macro note", themes=["fx-carry"], mvars=["USDJPY"])
    maps = map_evidence_to_scenarios(scns, [atom])
    assert maps[0].impacts == []
    assert any("could not be mapped" in w.lower() or "unused" in w.lower()
               for m in maps for w in m.warnings)


# ── classification (rule 5) ─────────────────────────────────────────────────────

def test_classify_hard_number_is_source_fact():
    assert classify_claim_kind(_atom(claim="HPC issuance was $26.6bn YTD", numbers=[26.6])) == "source_fact"


def test_classify_forecast_words():
    assert classify_claim_kind(_atom(claim="JPM expects HPC supply to keep rising into 2027")) == "source_forecast"


def test_classify_opinion_words():
    assert classify_claim_kind(_atom(claim="We think HPC looks crowded and unattractive here")) == "source_opinion"


def test_classify_respects_explicit_kind_and_synthesis():
    assert classify_claim_kind(_atom(claim="anything", kind="model_output")) == "model_output"
    assert classify_claim_kind(_atom(claim="agent inference", is_synthesis=True)) == "agent_synthesis"


# ── reliability defaults (rule 6) ───────────────────────────────────────────────

def test_reliability_ordering_by_kind():
    scn = _scn("S", "hpc oas tightens index weight rises issuance")
    def rel(kind):
        a = _atom(claim="hpc index weight oas issuance", themes=["t"], mvars=["HPC OAS"],
                  kind=kind)
        m = map_evidence_to_scenarios([scn], [a])[0]
        return m.impacts[0].reliability
    assert rel("source_fact") > rel("source_forecast") > rel("source_opinion")


def test_pm_assumption_not_used_as_evidence_support():
    scn = _scn("S", "hpc oas tightens")
    a = _atom(claim="assume hpc oas tightens", mvars=["HPC OAS"], kind="PM_assumption")
    m = map_evidence_to_scenarios([scn], [a])[0]
    assert m.impacts == []                                   # prior, not evidence support
    assert any("pm_assumption" in w.lower() or "prior" in w.lower() for w in m.warnings)


# ── clustering (rule 7) — deflate double-counting ───────────────────────────────

def test_cluster_deflates_independence_weight():
    scn = _scn("HPCcrowds", "hy hpc crowding index weight oas issuance return")
    atoms = [
        _atom(claim="hpc issuance 26.6", themes=["hy-hpc-crowding-and-supply"], mvars=["HPC issuance"]),
        _atom(claim="hpc 43% of non-refi", themes=["hy-hpc-crowding-and-supply"], mvars=["HPC issuance"]),
        _atom(claim="hpc index weight 2.68", themes=["hy-hpc-crowding-and-supply"], mvars=["HPC HY index weight"]),
        _atom(claim="hpc +9.99 return", themes=["hy-hpc-crowding-and-supply"], mvars=["HPC return"]),
        _atom(claim="hpc oas 295", themes=["hy-hpc-crowding-and-supply"], mvars=["HY HPC OAS"]),
    ]
    m = map_evidence_to_scenarios([scn], atoms)[0]
    assert len(m.impacts) == 5
    assert m.cluster_count == 1                              # one crowding cluster
    assert all(abs(i.independence_weight - 0.2) < 1e-9 for i in m.impacts)  # 1/5 each


def test_explicit_contradictory_direction_is_counted():
    scn = _scn("Tighten", "hpc oas tightens index weight")
    a = _atom(claim="hpc oas widened sharply", mvars=["HY HPC OAS"], themes=["t"],
              direction="contradictory")
    m = map_evidence_to_scenarios([scn], [a])[0]
    assert m.contradiction_count == 1
    assert m.impacts[0].direction == "contradictory"


# ── integration: real materialized JPM atoms ────────────────────────────────────

def test_jpm_hpc_crowding_cluster_maps_and_deflates():
    import json
    from pathlib import Path
    jsonl = Path(__file__).resolve().parents[2] / "wiki" / "evidence" / "evidence_atoms.jsonl"
    recs = [json.loads(l) for l in jsonl.read_text().splitlines() if l.strip()]
    atoms = [EvidenceAtom.from_record(r) for r in recs]
    # a scenario whose driver path is the HPC-crowding story
    scn = _scn("HPCcrowdingPersists",
               "HY HPC crowding persists: heavy HPC issuance, rising HY index weight, "
               "HPC OAS tightens, HPC total return outperforms")
    m = map_evidence_to_scenarios([scn], atoms)[0]
    assert len(m.impacts) >= 4                               # the crowding atoms route here
    assert m.cluster_count >= 1
    # the HY-HPC crowding atoms share ONE cluster and are deflated to 1/size (not double-counted);
    # a lone atom in its own cluster correctly keeps weight 1.0 — clustering only deflates groups.
    crowding = [i for i in m.impacts if i.evidence_cluster_id == "hy-hpc-crowding-and-supply"]
    assert len(crowding) >= 4
    assert all(abs(i.independence_weight - 1.0 / len(crowding)) < 1e-9 for i in crowding)
