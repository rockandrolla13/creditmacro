"""Phase-6 GATE: test_end_to_end_golden (+ admission unit coverage)
ONTOLOGY §Admission. Orphan clustering → gate → synthesize CandidateTheme → WF →
activation. Out-of-vocab modal tag → review queue (never auto-added).
"""
from __future__ import annotations

import json
from pathlib import Path

from engine.ledger.ingest.claim import AtomicClaim
from engine.ledger.ingest.admission import cluster_orphans, admit, OrphanCluster
from engine.ledger.runner import forward_ingest

CORPUS = Path(__file__).parent.parent / "golden" / "corpus"
EXPECTED_REGISTRY = json.loads((CORPUS / "expected_registry.json").read_text())


def _claim(cid, inst, tags, mv="C0A0_OAS", direction=1, horizon=90, date="2026-04-01", conv=3):
    return AtomicClaim(
        claim_id=cid, doc_id="d", source_institution=inst, doc_date=date, text=cid,
        market_variable=mv, direction=direction, horizon_days=horizon,
        stated_conviction=conv, mechanism_tags=tuple(tags),
    )


# ── clustering ───────────────────────────────────────────────────────────────
def test_cluster_by_shared_tag():
    claims = [
        _claim("a", "JPM", ["funding_stress", "liquidity_premium"]),
        _claim("b", "GS", ["funding_stress"]),
        _claim("c", "PIMCO", ["earnings_trajectory"]),   # disjoint
    ]
    clusters = cluster_orphans(claims)
    sizes = sorted(len(c.claims) for c in clusters)
    assert sizes == [1, 2]                               # {a,b} and {c}


# ── admission gate ───────────────────────────────────────────────────────────
def _funding_cluster(insts=("JPM", "GS")):
    return OrphanCluster(claims=(
        _claim("x0", insts[0], ["funding_stress", "liquidity_premium"], horizon=90, date="2026-04-01"),
        _claim("x1", insts[0], ["funding_stress", "dealer_balance_sheet_capacity"], horizon=60, date="2026-04-01"),
        _claim("x2", insts[-1], ["funding_stress"], horizon=90, date="2026-04-06"),
    ))


def test_admission_rejects_single_institution():
    out = admit(_funding_cluster(insts=("JPM", "JPM")))
    assert out.status == "rejected_gate"


def test_admission_rejects_below_n_min():
    small = OrphanCluster(claims=_funding_cluster().claims[:2])
    assert admit(small).status == "rejected_gate"


def test_admission_rejects_wide_window():
    wide = OrphanCluster(claims=(
        _claim("w0", "JPM", ["funding_stress", "liquidity_premium"], date="2026-04-01"),
        _claim("w1", "GS", ["funding_stress"], date="2026-04-01"),
        _claim("w2", "PIMCO", ["funding_stress"], date="2026-06-01"),   # >30d span
    ))
    assert admit(wide).status == "rejected_gate"


def test_admits_and_synthesizes_wf_theme():
    out = admit(_funding_cluster())
    assert out.status == "admitted"
    assert out.theme_id == "admitted:funding_stress-dealer_balance_sheet_capacity"
    assert out.definition.mechanism.k == 2
    assert out.definition.operational_axis == "C0A0_OAS"
    assert len(out.founding_links) == 3
    assert all(l.polarity == 1 for l in out.founding_links)   # dir+1 · d(θ)+1 · sign+1


def test_out_of_vocab_modal_tag_routes_to_review():
    cluster = OrphanCluster(claims=(
        _claim("o0", "JPM", ["made_up_node"], date="2026-04-01"),
        _claim("o1", "GS", ["made_up_node"], date="2026-04-02"),
        _claim("o2", "PIMCO", ["made_up_node"], date="2026-04-03"),
    ))
    out = admit(cluster)
    assert out.status == "out_of_vocab"
    assert "made_up_node" in out.review_tags


# ── the end-to-end gate ──────────────────────────────────────────────────────
def test_end_to_end_golden():
    state = forward_ingest(["gc-003-jpm", "gc-004-gs", "gc-005-solo"], CORPUS)
    admitted = [{"theme_id": a.theme_id, "status": a.status} for a in state.admitted]
    assert admitted == EXPECTED_REGISTRY["admitted"]
    assert sorted(state.orphan_claim_ids) == sorted(EXPECTED_REGISTRY["orphan_claim_ids"])
    assert state.needs_structuring == EXPECTED_REGISTRY["needs_structuring"]
    assert state.review_tags == EXPECTED_REGISTRY["review_tags"]
