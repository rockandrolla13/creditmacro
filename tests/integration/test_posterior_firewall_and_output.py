"""Q4 PART-2c — PART 5 (firewall) + PART 8 (output) integration tests.

12. Archived CASE evidence is refused in Phase A.
13. Post-snapshot CASE memory cannot mutate the initial ProbabilityUpdateAudit.
16. ConfidenceComponents receives probability_quality through the existing path.
17. Discovery output includes the probability_update_audit when scenarios are supplied.
"""
from __future__ import annotations

import json
from pathlib import Path

from engine.case_loader import load_case
from engine.memory import MemoryRetriever, load_wiki_pages
from engine.probability_evidence import (
    audit_hash,
    map_evidence_to_scenarios,
    update_probabilities_from_evidence,
)
from engine.schema import EvidenceAtom, Scenario
from engine.scripted_provider import ScriptedProvider
from engine.workflow import run_workflow
from tests._helpers import CASES_DIR

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
JPM_FIXTURE = CASES_DIR / "discovery" / "jpm_ai_capex.yaml"


def _atoms():
    jsonl = WIKI / "evidence" / "evidence_atoms.jsonl"
    return [EvidenceAtom.from_record(json.loads(l)) for l in jsonl.read_text().splitlines() if l.strip()]


def _hpc_scns():
    def S(n, p, dp):
        return Scenario(name=n, p_s=p, driver_path=dp, implied_axis_value=0.0, pnl_per_unit=0.0)
    return [
        S("momentum_continues", 0.5, "HPC issuance rises, HPC HY index weight rises, HPC OAS tightens, HPC return outperforms"),
        S("reversal", 0.5, "HPC OAS widens, index weight falls, HPC return lags"),
    ]


# 12 — archived CASE evidence pages are refused in Phase A
def test_archived_case_evidence_refused_in_phase_a():
    pages = load_wiki_pages(WIKI)
    ev_slugs = [s for s, p in pages.items() if p.type == "evidence"]
    assert ev_slugs, "evidence pages should load"
    r = MemoryRetriever(pages, phase="A")
    for s in ev_slugs:
        assert r.retrieve(s) is None
        assert s in r.refusals


# 13 — post-snapshot CASE memory cannot mutate the initial ProbabilityUpdateAudit
def test_post_snapshot_case_cannot_mutate_initial_audit():
    scns = _hpc_scns()
    # Phase A: posterior audit from CURRENT-INPUT evidence only (atoms supplied directly).
    maps_a = map_evidence_to_scenarios(scns, _atoms())
    audit_a = update_probabilities_from_evidence(scns, maps_a)
    h_a = audit_hash(audit_a)

    # The archive (wiki CASE evidence) is refused in Phase A — it never entered audit_a.
    pages = load_wiki_pages(WIKI)
    r = MemoryRetriever(pages, phase="A")
    some_evidence = next(s for s, p in pages.items() if p.type == "evidence")
    assert r.retrieve(some_evidence) is None

    # FREEZE, then Phase B: case pages become readable for calibration...
    r.mark_frozen(h_a)
    r.advance_to_phase_b()
    assert r.retrieve(some_evidence) is not None              # readable now (analogue/calibration)

    # ...but recomputing the INITIAL audit from the same phase-A inputs is byte-identical:
    # case memory did not mutate it.
    audit_recomputed = update_probabilities_from_evidence(scns, maps_a)
    assert audit_hash(audit_recomputed) == h_a
    assert audit_recomputed.posterior_vector == audit_a.posterior_vector


# 16 + 17 — discovery (ScriptedProvider) routes quality into ConfidenceComponents and surfaces the audit
def test_discovery_routes_quality_and_surfaces_audit():
    theme, _ = run_workflow(ScriptedProvider(load_case(JPM_FIXTURE)),
                            load_case(JPM_FIXTURE).resolved_policy(), mode="discovery")
    assert theme.status in ("strategy_family_routed", "discovery_complete")
    # 17: audit present on the justification when scenarios are supplied
    assert theme.probability_justification is not None
    assert theme.probability_justification.update_audit is not None
    audit = theme.probability_justification.update_audit
    assert audit.update_method in ("posterior_equals_prior", "softmax_evidence_tilt")
    if theme.strategy_families:
        f = theme.strategy_families[0]
        # 16: probability_quality reached the family AND the existing data_confidence path
        assert f.probability_quality is not None
        assert f.confidence_components.data_confidence is not None
        # one number, not a parallel score: the stamped quality is the data_confidence floor input
        assert f.probability_update_method == audit.update_method
        assert f.probability_update_audit_hash == audit_hash(audit)
