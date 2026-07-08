"""Phase-4 GATES: test_seam_extract_to_map, test_axis_flip_remap
(ONTOLOGY §EvidenceLink, §Identity, §Event link-policy).

Polarity is COMPUTED (claim.direction × d(θ) × sign(X)), never LLM-emitted (I3).
The sign(X) factor is what the axis-flip-remap gate proves is necessary — see
SIGN_AUDIT.md (the ONTOLOGY §EvidenceLink formula omitted it).
"""
from __future__ import annotations

from engine.ledger.substrate.hypothesis import (
    Mechanism, TransmissionEdge, ThemeDefinitionView,
)
from engine.ledger.ingest.claim import AtomicClaim
from engine.ledger.ingest.link import EvidenceLink, JsonlEvidenceLinkStore
from engine.ledger.ingest.pass_b import (
    StructuralSemanticMapper, MapResult, polarity, structural_prematch, match_confidence, remap,
)


def _mech(*edges):
    return Mechanism(edges=tuple(TransmissionEdge(v_from=a, v_to=b, sign=s) for (a, b, s) in edges))


def _def(theme_id="t1", axis="C0A0_OAS"):
    return ThemeDefinitionView(
        theme_id=theme_id,
        mechanism=_mech(("funding_stress", "liquidity_premium", 1),
                        ("liquidity_premium", "credit_spread", 1)),
        shock_direction=1, operational_axis=axis, horizon_days=90,
    )


def _claim(cid, mv, direction, tags, inst="JPMorgan"):
    return AtomicClaim(
        claim_id=cid, doc_id="d1", source_institution=inst, doc_date="2026-03-01",
        text="…", market_variable=mv, direction=direction, horizon_days=90,
        stated_conviction=2, mechanism_tags=tuple(tags),
    )


# Claims are about the vk (credit_spread) so they map regardless of which axis the
# theme is measured on — and their polarity, expressed on the operational axis, flips
# with sign(X) when the axis convention flips (the axis-flip-remap gate).
SUPPORT = _claim("c-sup", "credit_spread", 1, ["funding_stress", "liquidity_premium"])
CONTRADICT = _claim("c-con", "credit_spread", -1, ["funding_stress", "liquidity_premium"])
ORPHAN = _claim("c-orph", "H0A0_OAS", 1, ["earnings_trajectory"])


# ── the seam gate ────────────────────────────────────────────────────────────
def test_seam_extract_to_map():
    d = _def()
    res = StructuralSemanticMapper().map([SUPPORT, CONTRADICT, ORPHAN], [d], {"t1": 1})
    assert isinstance(res, MapResult)
    by_claim = {l.claim_id: l for l in res.links}
    assert set(by_claim) == {"c-sup", "c-con"}                 # orphan not linked
    assert by_claim["c-sup"].polarity == 1                     # d(θ)=+1, sign(X)=+1
    assert by_claim["c-con"].polarity == -1                    # contra-evidence for free
    assert by_claim["c-sup"].theme_revision == 1
    assert [c.claim_id for c in res.orphans] == ["c-orph"]     # routed to orphan pool


def test_axis_sign_unknown_raises_descriptive_error():
    # CR-BUG-002: an untracked axis must fail with a clear contract error, not KeyError.
    import pytest
    from engine.ledger import vocab
    with pytest.raises(ValueError):
        vocab.axis_sign("NOT_IN_REGISTRY")


def test_polarity_verified_against_d_theta():
    d = _def()
    # polarity == claim.direction × d(θ) × sign(X); here d(θ)=+1, sign(C0A0_OAS)=+1
    assert polarity(SUPPORT, d) == SUPPORT.direction * 1 * 1
    assert polarity(CONTRADICT, d) == CONTRADICT.direction * 1 * 1


# ── the axis-flip remap gate ─────────────────────────────────────────────────
def test_axis_flip_remap():
    d1 = _def(axis="C0A0_OAS")            # sign +1
    first = StructuralSemanticMapper().map([SUPPORT], [d1], {"t1": 1}).links
    assert first[0].polarity == 1

    d2 = _def(axis="IG_EXCESS_RETURN")    # sign −1 (convention flip)
    relinked = remap(first, [SUPPORT], d2, theme_revision=2)

    assert len(relinked) == 1
    assert relinked[0].polarity == -first[0].polarity          # sign-flipped
    assert relinked[0].supersedes == first[0].link_id          # prior link superseded
    assert relinked[0].theme_revision == 2


# ── structural pre-match + τ_ORPHAN routing ──────────────────────────────────
def test_structural_prematch_needs_tag_and_variable():
    d = _def()
    assert structural_prematch(SUPPORT, d) is True
    assert structural_prematch(ORPHAN, d) is False            # tags disjoint from M


def test_weak_overlap_routes_to_orphan_below_tau():
    d = _def()
    weak = _claim("c-weak", "C0A0_OAS", 1, ["funding_stress", "earnings_trajectory", "spread_momentum"])
    assert structural_prematch(weak, d) is True               # 1 tag overlaps
    assert match_confidence(weak, d) < 0.6                    # but Jaccard < τ_ORPHAN
    res = StructuralSemanticMapper().map([weak], [d], {"t1": 1})
    assert res.links == []
    assert [c.claim_id for c in res.orphans] == ["c-weak"]


# ── evidence-link store is append-only ───────────────────────────────────────
def test_evidence_link_store_append_stamps_and_is_append_only(tmp_path):
    store = JsonlEvidenceLinkStore(str(tmp_path / "links.jsonl"),
                                   clock=lambda: "2026-03-02T00:00:00+00:00")
    link = EvidenceLink(link_id="L1", theme_id="t1", theme_revision=1, claim_id="c-sup",
                        polarity=1, match_confidence=0.9)
    assert link.recorded_at is None
    stored = store.append(link)
    assert stored.recorded_at == "2026-03-02T00:00:00+00:00"
    assert [l.link_id for l in store.links_for("t1")] == ["L1"]
    for banned in ("update", "delete", "remove", "overwrite"):
        assert not hasattr(JsonlEvidenceLinkStore, banned)
