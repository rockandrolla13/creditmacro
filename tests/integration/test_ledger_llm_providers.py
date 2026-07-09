"""Wiring the Anthropic LLM seams behind Pass A / Pass B (BLOCKED B-01).

Tests inject a FAKE Anthropic client (same bypass the engine's provider_select
uses for offline tests) so the deterministic gates stay LLM-free. A real client
is built only under the ALLOW_LIVE_LLM_DISCOVERY opt-in.
"""
from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from engine.ledger.substrate.hypothesis import (
    Mechanism, TransmissionEdge, ThemeDefinitionView,
)
from engine.ledger.ingest.claim import AtomicClaim
from engine.ledger.ingest.pass_a import LLMClaimProvider, PassAExtractor
from engine.ledger.ingest.pass_b import (
    LLMMatchScorer, StructuralSemanticMapper,
)


class _FakeMessages:
    def __init__(self, text, calls):
        self._text, self._calls = text, calls

    def create(self, **kwargs):
        self._calls.append(kwargs)
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=self._text)])


class _FakeClient:
    """Minimal stand-in for anthropic.Anthropic()."""
    def __init__(self, text):
        self.calls = []
        self.messages = _FakeMessages(text, self.calls)


def _def(theme_id="t1", axis="C0A0_OAS"):
    mech = Mechanism(edges=(
        TransmissionEdge(v_from="funding_stress", v_to="liquidity_premium", sign=1),
        TransmissionEdge(v_from="liquidity_premium", v_to="credit_spread", sign=1),
    ))
    return ThemeDefinitionView(theme_id=theme_id, mechanism=mech, shock_direction=1,
                               operational_axis=axis, horizon_days=90)


def _claim(cid="c1", mv="credit_spread", direction=1, tags=("funding_stress", "liquidity_premium")):
    return AtomicClaim(claim_id=cid, doc_id="d", source_institution="JPM", doc_date="2026-03-01",
                       text="funding stress widens ig spreads", market_variable=mv,
                       direction=direction, horizon_days=90, stated_conviction=2,
                       mechanism_tags=tuple(tags))


# ── Pass A: LLM claim provider ───────────────────────────────────────────────
def test_llm_claim_provider_parses_and_extracts():
    payload = json.dumps({"claims": [
        {"text": "IG wider on funding stress", "market_variable": "C0A0_OAS",
         "direction": 1, "horizon_days": 90, "stated_conviction": 2,
         "mechanism_tags": ["funding_stress", "liquidity_premium"]},
    ]})
    client = _FakeClient(payload)
    provider = LLMClaimProvider(client=client)

    raws = provider.propose("gc-x", "IG spreads look set to widen.",
                            source_institution="JPM", doc_date="2026-03-01")
    assert raws[0]["market_variable"] == "C0A0_OAS"

    # end-to-end through the (deterministic) PassAExtractor
    res = PassAExtractor(provider).extract("gc-x", text="IG spreads look set to widen.",
                                           source_institution="JPM", doc_date="2026-03-01")
    assert isinstance(res.claims[0], AtomicClaim)
    assert res.claims[0].market_variable == "C0A0_OAS"
    assert res.claims[0].direction == 1
    # the document text was actually sent to the model
    assert "IG spreads look set to widen." in client.calls[0]["messages"][0]["content"]
    assert client.calls[0]["model"] == "claude-opus-4-8"


def test_llm_claim_provider_requires_live_optin(monkeypatch):
    monkeypatch.delenv("ALLOW_LIVE_LLM_DISCOVERY", raising=False)
    provider = LLMClaimProvider(client=None)          # no injected client → must build a real one
    with pytest.raises(RuntimeError):
        provider.propose("d", "text", source_institution="X", doc_date="2026-03-01")


# ── Pass B: LLM match scorer ─────────────────────────────────────────────────
def test_llm_match_scorer_returns_confidence():
    client = _FakeClient(json.dumps({"match_confidence": 0.82}))
    scorer = LLMMatchScorer(client=client)
    assert scorer.score(_claim(), _def()) == pytest.approx(0.82)
    # I3: the scorer sees only the definition (axis/mechanism) — polarity is never asked
    sent = client.calls[0]
    assert "polarity" not in json.dumps(sent).lower()


def test_mapper_uses_injected_llm_scorer():
    client = _FakeClient(json.dumps({"match_confidence": 0.9}))
    mapper = StructuralSemanticMapper(scorer=LLMMatchScorer(client=client).score)
    res = mapper.map([_claim()], [_def()], {"t1": 1})
    assert len(res.links) == 1
    assert res.links[0].match_confidence == pytest.approx(0.9)
    assert res.links[0].polarity == 1                 # still computed, not from the LLM


def test_default_mapper_still_deterministic():
    # the default scorer is the node-Jaccard function — no client, no network
    res = StructuralSemanticMapper().map([_claim()], [_def()], {"t1": 1})
    assert len(res.links) == 1
