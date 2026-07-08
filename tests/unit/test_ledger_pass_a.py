"""Phase-3 GATE: test_golden_claims_exact (+ I2 import firewall).

ONTOLOGY §AtomicClaim. Pass A is BLIND — it never imports the theme registry
(I2). The scripted provider reads the golden corpus's `claims:` block so the
exact-match gate is deterministic; an LLM provider for prose is a seam.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from engine.ledger.ingest.claim import AtomicClaim
from engine.ledger.ingest.pass_a import (
    PassAExtractor, ScriptedClaimProvider, PassAResult,
)

CORPUS = Path(__file__).parent.parent / "golden" / "corpus"
EXPECTED = json.loads((CORPUS / "expected_claims.json").read_text())


def _meta(doc_id: str) -> dict:
    fm = yaml.safe_load((CORPUS / f"{doc_id}.md").read_text().split("---", 2)[1])
    return {"source_institution": fm["source_institution"], "doc_date": str(fm["doc_date"])}


def _extract(doc_id: str) -> PassAResult:
    ex = PassAExtractor(ScriptedClaimProvider(CORPUS))
    m = _meta(doc_id)
    return ex.extract(doc_id, text="", source_institution=m["source_institution"],
                      doc_date=m["doc_date"])


class _FixedProvider:
    """Test double returning canned raw proposals (a valid ClaimProvider)."""
    def __init__(self, raws):
        self._raws = raws

    def propose(self, doc_id, text, source_institution, doc_date):
        return list(self._raws)


# ── the named gate ───────────────────────────────────────────────────────────
def test_golden_claims_exact():
    for doc_id, expected in EXPECTED.items():
        claims = _extract(doc_id).claims
        got = [
            {"claim_id": c.claim_id, "market_variable": c.market_variable,
             "direction": c.direction, "mechanism_tags": list(c.mechanism_tags)}
            for c in claims
        ]
        assert got == expected, f"{doc_id} mismatch"


def test_extracted_are_atomic_claims():
    claims = _extract("gc-001-funding").claims
    assert all(isinstance(c, AtomicClaim) for c in claims)
    assert claims[0].source_institution == "JPMorgan"
    assert claims[0].doc_date == "2026-03-01"


# ── granularity + vocab tagging ──────────────────────────────────────────────
def test_granularity_merges_same_variable_direction_horizon():
    # gc-002: two (C0A0_OAS,+1,90d) entries → one claim, union tags, max conviction
    claims = _extract("gc-002-mixed").claims
    merged = [c for c in claims if c.market_variable == "C0A0_OAS"]
    assert len(merged) == 1
    assert set(merged[0].mechanism_tags) == {"funding_stress", "dealer_balance_sheet_capacity"}
    assert merged[0].stated_conviction == 3          # max of {1, 3}


def test_out_of_vocab_tag_routed_not_kept():
    res = _extract("gc-002-mixed")
    assert "some_made_up_node" in res.out_of_vocab_tags
    curve = [c for c in res.claims if c.market_variable == "3M10Y"][0]
    assert curve.mechanism_tags == ("term_premium",)   # unknown tag dropped


# ── schema-domain validation (drop + record, never fabricate) ────────────────
def test_invalid_direction_rejected():
    ex = PassAExtractor(_FixedProvider([
        {"text": "bad dir", "market_variable": "C0A0_OAS", "direction": 2,
         "horizon_days": 90, "stated_conviction": 2, "mechanism_tags": ["funding_stress"]},
    ]))
    res = ex.extract("d", text="", source_institution="X", doc_date="2026-03-01")
    assert res.claims == []
    assert len(res.rejected) == 1


def test_invalid_conviction_rejected():
    ex = PassAExtractor(_FixedProvider([
        {"text": "bad conv", "market_variable": "C0A0_OAS", "direction": 1,
         "horizon_days": 90, "stated_conviction": 5, "mechanism_tags": ["funding_stress"]},
    ]))
    res = ex.extract("d", text="", source_institution="X", doc_date="2026-03-01")
    assert res.claims == []
    assert len(res.rejected) == 1


# ── I2 firewall wired into pytest ────────────────────────────────────────────
def test_i2_import_firewall_green():
    from tools.ledger_invariants import check_i2
    assert check_i2() == []
