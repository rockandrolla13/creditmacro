"""Phase-5 GATES: test_score_order_invariance, test_novelty_and_caps, test_score_is_pure
(ONTOLOGY §Scoring). S_θ and B_θ are PURE views over the link ledger (I1).
"""
from __future__ import annotations

import pytest
from hypothesis import given, strategies as st

from engine.ledger.ingest.claim import AtomicClaim
from engine.ledger.ingest.link import EvidenceLink
from engine.ledger.ingest.scoring_view import score, ScoreView


def _pair(cid, inst, polarity, conviction, text, date="2026-03-01", theme="t1", supersedes=None):
    claim = AtomicClaim(
        claim_id=cid, doc_id="d", source_institution=inst, doc_date=date, text=text,
        market_variable="credit_spread", direction=polarity, horizon_days=90,
        stated_conviction=conviction, mechanism_tags=(),
    )
    link = EvidenceLink(
        link_id=f"L-{cid}", theme_id=theme, theme_revision=1, claim_id=cid,
        polarity=polarity, match_confidence=0.9, supersedes=supersedes,
    )
    return link, claim


def _score(pairs, as_of="2026-03-01", horizon_days=90, prior_mass=None):
    links = [l for l, _ in pairs]
    claims = {c.claim_id: c for _, c in pairs}
    return score("t1", as_of, links, claims, horizon_days=horizon_days, prior_mass=prior_mass)


# ── core formula + decay ─────────────────────────────────────────────────────
def test_single_support_at_t0():
    sv = _score([_pair("a", "JPM", 1, 2, "funding stress widens ig")])
    assert isinstance(sv, ScoreView)
    assert sv.S == pytest.approx(2.0)          # p·s·λ^0·ν = 1·2·1·1
    assert sv.B == 1


def test_half_life_decay():
    # h = H/2 = 45d; at t0+45d decay = λ^1 = 0.5
    sv = _score([_pair("a", "JPM", 1, 2, "x", date="2026-01-01")], as_of="2026-02-15")
    assert sv.S == pytest.approx(1.0)          # 2 · 0.5


def test_contra_evidence_is_negative():
    sv = _score([_pair("a", "JPM", -1, 3, "spreads tighten")])
    assert sv.S == pytest.approx(-3.0)
    assert sv.B == 0                           # no institution with net-positive


# ── novelty discount + per-institution cap (the named gate) ──────────────────
def test_novelty_and_caps():
    # same institution, near-identical text, same date → later-by-id discounted (ν=0.15)
    repeat = _score([
        _pair("a", "JPM", 1, 2, "funding stress widens ig spreads", date="2026-03-01"),
        _pair("b", "JPM", 1, 2, "funding stress widens ig spreads", date="2026-03-01"),
    ])
    assert repeat.S == pytest.approx(2.0 + 2.0 * 0.15)   # second at ν=0.15
    assert repeat.B == 1

    # single-institution flood → net contribution capped at +3
    flood = _score([_pair(f"c{i}", "JPM", 1, 3, f"distinct claim number {i}") for i in range(10)])
    assert flood.S == pytest.approx(3.0)                  # CAP_INST
    assert flood.B == 1


def test_cross_institution_repeat_not_discounted():
    sv = _score([
        _pair("a", "JPM", 1, 2, "funding stress widens ig spreads"),
        _pair("b", "GS", 1, 2, "funding stress widens ig spreads"),   # same text, diff inst
    ])
    assert sv.S == pytest.approx(4.0)          # both full weight
    assert sv.B == 2


# ── purity + order invariance (named gates) ──────────────────────────────────
_PAIRS = [
    _pair("a", "JPM", 1, 2, "alpha claim", date="2026-03-01"),
    _pair("b", "JPM", 1, 2, "alpha claim", date="2026-03-02"),   # same-inst repeat
    _pair("c", "GS", 1, 3, "beta claim", date="2026-03-01"),
    _pair("d", "PIMCO", -1, 1, "gamma claim", date="2026-03-03"),
]
_REF = _score(_PAIRS, as_of="2026-03-05")


@given(st.permutations(_PAIRS))
def test_score_order_invariance(perm):
    got = _score(list(perm), as_of="2026-03-05")
    assert got.S == pytest.approx(_REF.S)
    assert got.B == _REF.B


def test_score_is_pure():
    links = [l for l, _ in _PAIRS]
    claims = {c.claim_id: c for _, c in _PAIRS}
    before_ids = [l.link_id for l in links]
    sv1 = score("t1", "2026-03-05", links, claims, horizon_days=90)
    sv2 = score("t1", "2026-03-05", links, claims, horizon_days=90)
    assert sv1 == sv2                           # identical
    assert [l.link_id for l in links] == before_ids   # ledger unmutated


# ── superseded links + prior mass ────────────────────────────────────────────
def test_superseded_link_excluded():
    old = _pair("a", "JPM", 1, 3, "old")
    new = _pair("b", "JPM", -1, 3, "new", supersedes="L-a")   # supersedes L-a
    sv = _score([old, new])
    assert sv.S == pytest.approx(-3.0)          # only the superseding link counts


def test_prior_mass_only():
    sv = _score([], prior_mass=(2, "2026-03-01"), as_of="2026-03-01")
    assert sv.S == pytest.approx(2.0)           # s_prior · λ^0
    assert sv.B == 0                            # wiki testimony is not an institution
