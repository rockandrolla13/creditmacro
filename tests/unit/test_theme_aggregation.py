"""Multi-Source Theme Aggregator (Stage 0) — dedup/merge, no-overmerge, source attribution,
publisher-independence downweighting, the case-can't-confirm-current firewall gate, the
promote path, and the evidence−attention divergence. No trades anywhere."""
from __future__ import annotations

from datetime import date

import pytest

from engine.evidence_extraction import (
    EvidenceExtractionBundle,
    OperationalAxisCandidate,
    StrategyFamilyHint,
)
from engine.schema.probability import EvidenceAtom
from engine.temporal import TemporalContext
from engine.theme_aggregation import ThemeAggregationPolicy, aggregate_theme_candidates
from engine.wiki_agents import SourceClassification


# ── builders ─────────────────────────────────────────────────────────────────
def _atom(eid, slug, themes, concepts=(), market_vars=()):
    return EvidenceAtom(evidence_id=eid, source_slug=slug, claim=f"claim {eid}",
                        themes=list(themes), concepts=list(concepts),
                        market_variables=list(market_vars))


def _bundle(slug, *, themes=(), hot=(), atoms=(), axes=(), fams=()):
    return EvidenceExtractionBundle(
        source_slug=slug,
        core_theme_candidates=list(themes),
        hot_topics=list(hot),
        evidence_atoms=list(atoms),
        operational_axes=list(axes),
        strategy_family_hints=list(fams),
    )


def _sc(slug, access="method", stype="report"):
    return SourceClassification(source_slug=slug, source_type=stype, access_class=access,
                                copyright_status="copyright", ingestion_policy="summarize")


def _tc(slug, role="current_report"):
    return TemporalContext(source_slug=slug, current_date=date(2026, 6, 12),
                           temporal_role=role, current_update_required=False)


def _axis(name):
    return OperationalAxisCandidate(axis_name=name, axis_shape="basis",
                                    observable_series=f"{name}_series")


def _run(bundles, classes, temporals=None, policy=None):
    return aggregate_theme_candidates(bundles, classes, temporals, policy)


# ── dedup / merge ────────────────────────────────────────────────────────────
def test_merges_aliased_themes_into_one_cluster():
    b1 = _bundle("src-a", themes=["Private credit risk is mispriced"])
    b2 = _bundle("src-b", themes=["Direct lending spreads too tight"])
    res = _run([b1, b2], [_sc("src-a"), _sc("src-b")])
    # direct lending ≈ private credit (alias) + shared spread/credit-risk structure → ONE cluster
    assert len(res.clusters) == 1
    c = res.clusters[0]
    assert c.source_count == 2
    assert {a.source_slug for a in c.source_attributions} == {"src-a", "src-b"}


def test_does_not_overmerge_distinct_themes_and_records_rejection():
    b1 = _bundle("src-a", themes=["AI capex project-bond basis"])
    b2 = _bundle("src-b", themes=["HY HPC crowding"])
    res = _run([b1, b2], [_sc("src-a"), _sc("src-b")])
    assert len(res.clusters) == 2          # related but distinct — not merged
    assert res.rejected_merges             # the near-miss is recorded with a reason


def test_custom_alias_map_merges():
    b1 = _bundle("src-a", themes=["Widget glut"])
    b2 = _bundle("src-b", themes=["Gadget oversupply"])
    pol = ThemeAggregationPolicy(alias_map={"gadget": "widget", "oversupply": "glut"})
    res = _run([b1, b2], [_sc("src-a"), _sc("src-b")], policy=pol)
    assert len(res.clusters) == 1


# ── attribution + independence ───────────────────────────────────────────────
def test_every_cluster_has_source_attribution():
    res = _run([_bundle("src-a", themes=["rates not priced"])], [_sc("src-a")])
    assert res.clusters and all(c.source_attributions for c in res.clusters)


def test_same_publisher_downweights_independence():
    b1 = _bundle("jpm-1", themes=["Private credit risk is mispriced"])
    b2 = _bundle("jpm-2", themes=["Private credit risk is mispriced"])
    pol = ThemeAggregationPolicy(publisher_groups={"jpm-1": "jpm", "jpm-2": "jpm"})
    res = _run([b1, b2], [_sc("jpm-1"), _sc("jpm-2")],
               [_tc("jpm-1"), _tc("jpm-2")], policy=pol)   # current reports
    c = res.clusters[0]
    assert c.source_count == 2
    assert c.independent_source_count == 1   # two reports from one publisher ≠ independent


# ── PART 4: corroboration / attention ranking ────────────────────────────────
def test_more_independent_sources_rank_higher():
    bA1 = _bundle("s1", themes=["Theme alpha"], atoms=[_atom("e1", "s1", themes=["theme alpha"])])
    bA2 = _bundle("s2", themes=["Theme alpha"], atoms=[_atom("e2", "s2", themes=["theme alpha"])])
    bB = _bundle("s3", themes=["Beta solo"], atoms=[_atom("e3", "s3", themes=["beta solo"])])
    res = _run([bA1, bA2, bB], [_sc("s1"), _sc("s2"), _sc("s3")],
               [_tc("s1"), _tc("s2"), _tc("s3")])
    alpha = next(c for c in res.clusters if "alpha" in c.canonical_theme_name.lower())
    beta = next(c for c in res.clusters if "beta" in c.canonical_theme_name.lower())
    assert alpha.corroboration_score > beta.corroboration_score


def test_attention_rich_theme_has_lower_divergence_than_evidence_rich():
    hot = _bundle("buzz-1", hot=["everyone loves the bubble"])
    ev = _bundle("ev-1", themes=["solid credit thesis"],
                 atoms=[_atom("e1", "ev-1", themes=["solid credit thesis"])])
    res = _run([hot, ev], [_sc("buzz-1"), _sc("ev-1")], [_tc("buzz-1"), _tc("ev-1")])
    buzzc = next(c for c in res.clusters if "bubble" in c.canonical_theme_name.lower())
    evc = next(c for c in res.clusters if "credit" in c.canonical_theme_name.lower())
    assert buzzc.attention_score > evc.attention_score
    assert buzzc.evidence_attention_divergence < evc.evidence_attention_divergence


def test_single_source_strong_evidence_promotes_but_flagged():
    b = _bundle("solo", themes=["Unique credit dislocation"], axes=[_axis("idx_basis")],
                atoms=[_atom("e1", "solo", themes=["unique credit dislocation"])])
    res = _run([b], [_sc("solo")], [_tc("solo")])
    c = res.clusters[0]
    assert c.theme_status == "promote_to_discovery"
    assert any("single-source" in w for w in c.warnings)


# ── PART 5: access / temporal firewall ───────────────────────────────────────
def test_archived_case_excluded_from_phase_a():
    jpm = _bundle("jpm-archived", themes=["AI capex funding gap"])     # archived CASE
    fresh = _bundle("fresh-1", themes=["European credit cheapening"])
    res = _run([jpm, fresh], [_sc("jpm-archived", access="case"), _sc("fresh-1", access="case")],
               [_tc("fresh-1", role="current_report")])   # only fresh-1 is current
    names = " ".join(c.canonical_theme_name.lower() for c in res.clusters)
    assert "ai capex funding gap" not in names          # archived JPM dropped from Phase A
    assert "european" in names
    assert any("jpm-archived" in w for w in res.warnings)


def test_european_2019_report_is_historical_not_current_corroboration():
    b = _bundle("eu-2019", themes=["European banks stress"], axes=[_axis("eu_sov_spread")],
                atoms=[_atom("e1", "eu-2019", themes=["european banks stress"])])
    res = _run([b], [_sc("eu-2019", access="case")], [_tc("eu-2019", role="historical_case")])
    c = res.clusters[0]
    assert c.theme_status in ("historical_case", "outcome_candidate")   # never promoted
    assert all(a.contribution_type == "historical_analogue" for a in c.source_attributions)


def test_explicit_current_batch_two_case_reports_aggregate():
    b1 = _bundle("case-a", themes=["Private credit risk is mispriced"],
                 atoms=[_atom("e1", "case-a", themes=["private credit risk is mispriced"])])
    b2 = _bundle("case-b", themes=["Direct lending spreads too tight"],
                 atoms=[_atom("e2", "case-b", themes=["direct lending spreads too tight"])])
    pol = ThemeAggregationPolicy(current_input_slugs=frozenset({"case-a", "case-b"}))
    res = _run([b1, b2], [_sc("case-a", access="case"), _sc("case-b", access="case")], policy=pol)
    assert len(res.clusters) == 1                       # two CASE reports aggregate as current input
    c = res.clusters[0]
    assert c.source_count == 2 and c.independent_source_count == 2
    assert c.evidence_count == 2


def test_method_source_is_taxonomy_only_not_market_evidence():
    b = _bundle("method-1", themes=["Cycles and risk"], axes=[_axis("vix")],
                atoms=[_atom("e1", "method-1", themes=["cycles and risk"])])
    res = _run([b], [_sc("method-1", access="method")], [_tc("method-1", role="method_source")])
    c = res.clusters[0]
    assert c.theme_status == "needs_more_evidence"     # method != market evidence → no promote
    assert c.evidence_count == 0                        # current-evidence count excludes method
    assert all(a.contribution_type == "method_context" for a in c.source_attributions)


# ── firewall: historical case cannot confirm a current theme ─────────────────
def test_historical_case_only_theme_is_not_promoted():
    atom = _atom("ev1", "old-case", themes=["gfc credit blowup"])
    b = _bundle("old-case", themes=["GFC credit blowup"], atoms=[atom], axes=[_axis("hy_oas")])
    res = _run([b], [_sc("old-case", access="case")],
               [_tc("old-case", role="historical_case")])
    c = res.clusters[0]
    assert c.theme_status != "promote_to_discovery"
    assert c.theme_status in ("historical_case", "outcome_candidate", "reject", "needs_more_evidence")


def test_current_theme_with_axis_and_evidence_promotes():
    atom = _atom("ev1", "src-a", themes=["private credit risk is mispriced"])
    b = _bundle("src-a", themes=["Private credit risk is mispriced"], atoms=[atom],
                axes=[_axis("bdc_nav_discount")])
    res = _run([b], [_sc("src-a")], [_tc("src-a", role="current_report")])
    c = res.clusters[0]
    assert c.theme_status == "promote_to_discovery"
    assert c.operational_axes  # axis carried through


# ── divergence identity + no-trade ───────────────────────────────────────────
def test_divergence_is_corroboration_minus_attention():
    b = _bundle("src-a", themes=["rates not priced"], hot=["rates not priced"])
    res = _run([b], [_sc("src-a")])
    c = res.clusters[0]
    assert c.attention_score > 0  # it came from a hot_topics list
    assert c.evidence_attention_divergence == pytest.approx(
        c.corroboration_score - c.attention_score
    )


def test_strategy_family_hint_tied_to_evidence_becomes_candidate():
    from engine.evidence_extraction import StrategyFamilyHint
    atom = _atom("e1", "src-a", themes=["credit vs equity dislocation"])
    fh = StrategyFamilyHint(family="credit_vs_equity", rationale="credit vs equity dislocation",
                            source_evidence_ids=["e1"], confidence=0.6)
    b = _bundle("src-a", atoms=[atom], fams=[fh])   # NO core_theme_candidates
    res = _run([b], [_sc("src-a")], [_tc("src-a")])
    assert res.clusters                                            # a candidate formed from it
    assert any("credit_vs_equity" in c.strategy_family_hints for c in res.clusters)


def test_family_hint_without_evidence_is_not_a_candidate():
    from engine.evidence_extraction import StrategyFamilyHint
    fh = StrategyFamilyHint(family="outright", rationale="x y z", source_evidence_ids=[], confidence=0.5)
    res = _run([_bundle("src-a", fams=[fh])], [_sc("src-a")], [_tc("src-a")])
    assert res.clusters == []   # not tied to evidence → not a theme candidate


def test_similarity_uses_shared_market_variables():
    # DISJOINT names, but both atoms cite the same market_variable → must cluster (step 3)
    a1 = _atom("e1", "src-a", themes=["widget supply"], market_vars=["bdc_nav_discount"])
    a2 = _atom("e2", "src-b", themes=["gizmo demand"], market_vars=["bdc_nav_discount"])
    b1 = _bundle("src-a", themes=["Widget supply"], atoms=[a1])
    b2 = _bundle("src-b", themes=["Gizmo demand"], atoms=[a2])
    res = _run([b1, b2], [_sc("src-a"), _sc("src-b")])
    assert len(res.clusters) == 1


def test_evidence_bullets_are_formatted_with_kind_location_id():
    atom = EvidenceAtom(evidence_id="ev-001", source_slug="src-a", source_location="page:3",
                        claim="direct-lending default rate rose to X",
                        claim_kind="source_fact", themes=["private credit risk is mispriced"])
    b = _bundle("src-a", themes=["Private credit risk is mispriced"], atoms=[atom])
    res = _run([b], [_sc("src-a")], [_tc("src-a")])
    bullets = res.clusters[0].evidence_bullets
    assert any(bl.text.startswith("[source_fact | page:3 | ev-001]") for bl in bullets)
    assert any("direct-lending default rate rose" in bl.text for bl in bullets)


def test_source_attribution_rationale_describes_contribution():
    res = _run([_bundle("src-a", themes=["X theme"], atoms=[_atom("e1", "src-a", themes=["x theme"])]),
                _bundle("buzz", hot=["x theme"])],
               [_sc("src-a"), _sc("buzz")], [_tc("src-a"), _tc("buzz")])
    rats = {a.source_slug: a.rationale.lower() for a in res.clusters[0].source_attributions}
    assert "support" in rats["src-a"]
    assert "attention" in rats["buzz"] or "mention" in rats["buzz"]


# ── the merge metric: the five measured cases ────────────────────────────────
# The aggregator used to score similarity with the OVERLAP COEFFICIENT
# (|a∩b| / min(|a|,|b|)), which returns 1.0 for ANY token set that is a subset of the other.
# 'growth' therefore scored 1.00 against every theme containing the word "growth" and merged at
# every threshold <= 1.0, so `min_similarity_to_merge` was not doing the work it appeared to.
# The replacement is an alias-anchored WEIGHTED JACCARD (`_weighted_jaccard`): symmetric, so
# containment no longer saturates, with tokens introduced by an alias substitution weighted
# `alias_anchor_weight` because a curated alias is evidence about MEANING.
#
# Each case below carries its OLD overlap-coefficient score in a comment.
MEASURED_CASES = [
    # (a, b, should_merge, new_score, old_overlap_score)
    ("growth", "rates not pricing growth", False, 0.25, 1.00),
    ("growth", "china growth slowdown", False, 0.33, 1.00),
    ("growth", "growth in ai capex funding needs", False, 0.20, 1.00),
    # blocked by the discriminator guard, not by the score: two regions, no shared region.
    ("european bank spreads", "japanese bank spreads", False, 0.50, 0.67),
    # the alias `direct lending -> private credit` anchors the shared tokens, lifting a real
    # merge from 0.33 (plain Jaccard, below the bar) to 0.60 (above it).
    ("Private credit risk is mispriced", "Direct lending spreads too tight", True, 0.60, 0.50),
]


def _score(a, b, policy=None):
    """The merge decision for two raw theme names: (score, blocked_reason, merges?)."""
    from engine.theme_aggregation import (
        _alias_anchors, _blocked, _normalize, _weighted_jaccard,
    )
    pol = policy or ThemeAggregationPolicy()
    ta, tb = _normalize(a, pol.alias_map)[1], _normalize(b, pol.alias_map)[1]
    anchors = _alias_anchors(a, pol.alias_map) | _alias_anchors(b, pol.alias_map)
    score = _weighted_jaccard(ta, tb, anchors, pol.alias_anchor_weight)
    reason = _blocked(ta, tb, pol)
    return score, reason, reason is None and score >= pol.min_similarity_to_merge


@pytest.mark.parametrize("a,b,should_merge,new_score,old_score", MEASURED_CASES)
def test_measured_case_has_its_new_score_and_merge_decision(
        a, b, should_merge, new_score, old_score):
    from engine.theme_aggregation import _containment, _normalize
    pol = ThemeAggregationPolicy()
    ta, tb = _normalize(a, pol.alias_map)[1], _normalize(b, pol.alias_map)[1]
    assert _containment(ta, tb) == pytest.approx(old_score, abs=0.005)   # what it used to be
    score, _reason, merges = _score(a, b)
    assert score == pytest.approx(new_score, abs=0.005)
    assert merges is should_merge


def test_overlap_coefficient_saturated_on_containment_but_the_new_metric_does_not():
    """The defect in one assertion: a subset scored a perfect 1.0 on being a subset."""
    from engine.theme_aggregation import _containment, _normalize
    a, b = _normalize("growth", {})[1], _normalize("china growth slowdown", {})[1]
    assert a < b                                    # 'growth' is a strict subset
    assert _containment(a, b) == 1.0                # old metric: indistinguishable from equal
    assert _score("growth", "china growth slowdown")[0] < 1.0


_LABELLED_PAIRS = [(a, b, m) for a, b, m, _n, _o in MEASURED_CASES] + [
    ("AI capex funding gap", "AI capex funding gap", True),
    ("AI capex funding gap", "AI chip demand", False),
    ("AI capex funding gap", "AI software margins", False),
    ("AI chip demand", "AI software margins", False),
    ("ETF basket basis", "Software refinancing stress", False),
    ("HY HPC crowding", "Hyperscaler project bond basis", False),
    ("Private credit risk is mispriced", "Front-end rates catch up", False),
    ("alpha credit mispriced", "bravo rates dislocation", False),
]


def test_merge_metric_separates_the_measured_cases():
    """The re-tuning measurement behind `min_similarity_to_merge = 0.55`.

    The bar must sit ABOVE every pair that must not merge and AT OR BELOW every pair that must.
    Measured over the labelled set WITHOUT help from the guards, the band is (0.500, 0.600] and
    0.55 is its max-min-margin point. The threshold is deliberately derived this way: the
    discriminator vocabulary is hand-curated and will always be incomplete, so the metric is
    required to stand on its own and the guards are defence in depth, not a crutch.

    This is NOT the old 0.5 carried over. Under the overlap coefficient the band was EMPTY at
    every threshold — that is why no dial could fix the behaviour.
    """
    pol = ThemeAggregationPolicy()
    scored = [(_score(a, b)[0], m) for a, b, m in _LABELLED_PAIRS]
    ceiling = max(s for s, m in scored if not m)     # highest must-NOT-merge
    floor = min(s for s, m in scored if m)           # lowest must-merge
    assert ceiling < floor, "no threshold separates the cases"
    assert (round(ceiling, 3), round(floor, 3)) == (0.5, 0.6)
    assert ceiling < pol.min_similarity_to_merge <= floor
    assert pol.min_similarity_to_merge == pytest.approx((ceiling + floor) / 2, abs=0.005)


def test_old_overlap_coefficient_had_no_separating_threshold():
    """The finding that made this a metric change rather than a tuning change: on the same
    labelled set the old metric scored must-merge and must-NOT-merge pairs into the same range,
    so raising the bar worsened fragmentation and lowering it worsened over-merging."""
    from engine.theme_aggregation import _containment, _normalize
    al = ThemeAggregationPolicy().alias_map
    old = [(_containment(_normalize(a, al)[1], _normalize(b, al)[1]), m)
           for a, b, m in _LABELLED_PAIRS]
    assert max(s for s, m in old if not m) >= min(s for s, m in old if m)


def test_guards_are_defence_in_depth_not_load_bearing():
    """Every labelled pair is classified correctly by the threshold ALONE, guards switched
    off — so an incomplete discriminator vocabulary degrades the result, it does not break it."""
    naked = ThemeAggregationPolicy(discriminator_groups=[], distinct_pairs=[])
    for a, b, should_merge in _LABELLED_PAIRS:
        assert _score(a, b, naked)[2] is should_merge, f"{a!r} vs {b!r}"


def test_plain_jaccard_would_not_have_worked():
    """Why the metric is weighted, not the 'obvious' plain Jaccard.

    Plain Jaccard scores a must-NOT-merge pair and a must-merge pair identically at 0.333, so
    it has no separating threshold either. The alias anchoring is what breaks the tie.
    """
    from engine.theme_aggregation import _normalize, _weighted_jaccard
    pol = ThemeAggregationPolicy()
    plain = lambda a, b: _weighted_jaccard(          # noqa: E731 — weight 1.0 == plain Jaccard
        _normalize(a, pol.alias_map)[1], _normalize(b, pol.alias_map)[1], frozenset(), 1.0)
    assert plain("growth", "china growth slowdown") == pytest.approx(0.333, abs=0.005)
    assert plain("Private credit risk is mispriced",
                 "Direct lending spreads too tight") == pytest.approx(0.333, abs=0.005)


def test_containment_is_still_used_to_link_atoms_to_a_theme():
    """The overlap coefficient is CORRECT for atom linking and is retained there: it asks
    whether a short theme name is covered by a much longer atom, where Jaccard is always tiny.
    A theme with no `themes` on its atoms still picks the atom up by content."""
    atom = EvidenceAtom(evidence_id="e1", source_slug="src-a",
                        claim="bdc nav discount widened sharply on private credit stress",
                        entities=["private credit"], market_variables=["bdc_nav_discount"])
    b = _bundle("src-a", themes=["Private credit"], atoms=[atom])
    res = _run([b], [_sc("src-a")], [_tc("src-a")])
    assert res.clusters[0].evidence_ids == ["e1"]


# ── the discriminator guard ──────────────────────────────────────────────────
def test_two_regions_with_the_same_mechanism_do_not_merge():
    b1 = _bundle("src-a", themes=["European bank spreads"])
    b2 = _bundle("src-b", themes=["Japanese bank spreads"])
    res = _run([b1, b2], [_sc("src-a"), _sc("src-b")])
    assert len(res.clusters) == 2                       # old overlap coefficient: 0.67 → MERGED
    assert any("discriminator_guard[region]" in r["reason"] for r in res.rejected_merges)


def test_one_sided_region_is_not_a_conflict():
    """'european bank spreads' vs 'bank spreads' is a candidate subtheme, not a contradiction —
    the guard needs a region on BOTH sides, and leaves this to the metric."""
    from engine.theme_aggregation import _discriminator_conflict, _normalize
    pol = ThemeAggregationPolicy()
    ta = _normalize("european bank spreads", {})[1]
    tb = _normalize("bank spreads", {})[1]
    assert _discriminator_conflict(ta, tb, pol.discriminator_groups) is None


# ── pass 2: the mechanism merge ──────────────────────────────────────────────
def _mech_bundle(slug, theme, eid, *, driver, outcome, axis, mvars):
    """A source whose theme carries a full causal story: driver→outcome, an axis, variables."""
    from engine.evidence_extraction import CausalClaimCandidate
    return EvidenceExtractionBundle(
        source_slug=slug, core_theme_candidates=[theme],
        evidence_atoms=[EvidenceAtom(evidence_id=eid, source_slug=slug, claim=f"claim {eid}",
                                     themes=[theme.lower()], market_variables=list(mvars))],
        causal_claims=[CausalClaimCandidate(
            driver=driver, transmission="funding channel", outcome=outcome,
            source_evidence_ids=[eid], confidence=0.7, rationale="r")],
        operational_axes=[OperationalAxisCandidate(
            axis_name=axis, axis_shape="basis", observable_series=f"{axis}_s",
            source_evidence_ids=[eid])],
    )


# Two sources describing ONE theme in completely different words. Every individual dimension
# sits BELOW the pass-1 bar of 0.55 (names 0.00, market_vars 0.40, axes 0.50, causal 0.43), so
# no single signal is strong enough for pass 1. All three structural dimensions clear the pass-2
# bar of 0.34 at once, which is what makes them the same theme.
_MECH_A = dict(theme="Sponsor-backed borrowers face a refinancing wall", eid="e1",
               driver="policy rate path", outcome="funding cost",
               axis="hy_oas_basis", mvars=["hy_oas", "ig_oas"])
_MECH_B = dict(theme="Leveraged issuers cannot roll their maturities", eid="e2",
               driver="policy rate path", outcome="issuance volume",
               axis="hy_oas_curve", mvars=["hy_oas", "bdc_nav"])


def _mech_pair(**overrides):
    b = dict(_MECH_B, **overrides)
    return [_mech_bundle("src-a", **_MECH_A), _mech_bundle("src-b", **b)]


def _mech_run(bundles, policy=None):
    return _run(bundles, [_sc("src-a"), _sc("src-b")], [_tc("src-a"), _tc("src-b")], policy)


def test_mechanism_pass_merges_themes_that_share_no_words():
    """The fragmentation half. Two differently-worded descriptions of ONE theme share no name
    tokens at all, so pass 1 will never join them. Pass 2 joins them because driver/outcome,
    the axis and the observable all agree at once."""
    assert _score(_MECH_A["theme"], _MECH_B["theme"])[0] == 0.0      # no shared word
    res = _mech_run(_mech_pair())
    assert len(res.clusters) == 1
    assert res.clusters[0].source_count == 2


def test_mechanism_pass_is_the_only_thing_that_merges_them():
    """Same fixture with pass 2 off stays split — proving the merge above is pass 2's doing and
    not pass 1 quietly clearing its bar on one dimension."""
    res = _mech_run(_mech_pair(), ThemeAggregationPolicy(mechanism_pass=False))
    assert len(res.clusters) == 2


def test_mechanism_pass_keeps_a_different_outcome_apart():
    """Same driver and axis, but a different outcome and a different observable. Keep-separate,
    not merge — the conjunction is exactly what stops this."""
    res = _mech_run(_mech_pair(outcome="equity multiple expansion",
                               axis="index_earnings_yield", mvars=["index_pe", "spx_div"]))
    assert len(res.clusters) == 2


def test_mechanism_pass_needs_all_three_not_two():
    """Driver/outcome and axis agree, but the observables do not overlap at all. Two out of
    three is not a mechanism match."""
    res = _mech_run(_mech_pair(mvars=["index_pe", "spx_div"]))
    assert len(res.clusters) == 2


def test_mechanism_pass_never_merges_on_missing_structure():
    """Two clusters with NO causal claim, axis or market variable must not merge just because
    they are equally empty — that is what makes pass 2 strictly additive."""
    res = _run([_bundle("src-a", themes=["Alpha wholly unrelated topic"]),
                _bundle("src-b", themes=["Bravo entirely different subject"])],
               [_sc("src-a"), _sc("src-b")])
    assert len(res.clusters) == 2


def test_mechanism_bar_must_sit_below_the_lexical_bar():
    """Why `min_mechanism_similarity` (0.34) is not simply the pass-1 bar.

    Pass 1 is a disjunction over six dimensions; pass 2 a conjunction over three of them. Raise
    the conjunction's bar to the disjunction's and pass 2 becomes dead code: any dimension that
    clears it has already caused pass 1 to merge.
    """
    pol = ThemeAggregationPolicy()
    assert pol.min_mechanism_similarity < pol.min_similarity_to_merge
    subsumed = ThemeAggregationPolicy(
        min_mechanism_similarity=ThemeAggregationPolicy().min_similarity_to_merge)
    assert len(_mech_run(_mech_pair(), subsumed).clusters) == 2      # pass 2 did nothing
    assert len(_mech_run(_mech_pair()).clusters) == 1               # at the tuned bar it acts


def test_mechanism_pass_respects_the_distinct_marker_guard():
    """Structure agreeing does not license merging what the guards call distinct."""
    res = _mech_run([
        _mech_bundle("src-a", **dict(_MECH_A, theme="AI capex project-bond basis")),
        _mech_bundle("src-b", **dict(_MECH_B,
                                     theme="HY HPC crowding high performance computing")),
    ])
    assert len(res.clusters) == 2
    assert res.rejected_merges


def test_mechanism_pass_respects_the_discriminator_guard():
    res = _mech_run([
        _mech_bundle("src-a", **dict(_MECH_A, theme="European bank funding stress")),
        _mech_bundle("src-b", **dict(_MECH_B, theme="Japanese bank funding stress")),
    ])
    assert len(res.clusters) == 2
    assert any("discriminator_guard[region]" in r["reason"] for r in res.rejected_merges)


# ── determinism / order-independence ─────────────────────────────────────────
def _fingerprint(res):
    """Everything about the clustering that a caller can observe, order-insensitively."""
    return sorted(
        (c.cluster_id, c.canonical_theme_name,
         tuple(sorted((m.source_slug, m.original_theme_name) for m in c.members)),
         c.promotion_score)
        for c in res.clusters
    )


def test_clustering_is_independent_of_input_order():
    """`_cluster_items` was a greedy pass over the caller's list, so the same themes in a
    different order produced different clusters. Items are now sorted into a canonical,
    content-derived order first, so the result is a function of the input SET."""
    import itertools
    specs = [("src-a", "Private credit risk is mispriced"),
             ("src-b", "Direct lending spreads too tight"),
             ("src-c", "European bank spreads"),
             ("src-d", "Japanese bank spreads"),
             ("src-e", "AI capex funding gap")]
    runs = []
    for order in itertools.permutations(range(len(specs))):
        picked = [specs[i] for i in order]
        res = _run([_bundle(s, themes=[t]) for s, t in picked],
                   [_sc(s) for s, _ in picked], [_tc(s) for s, _ in picked])
        runs.append(_fingerprint(res))
    assert all(r == runs[0] for r in runs), "clustering still depends on input order"


def test_repeated_runs_are_byte_identical():
    b = [_bundle("src-a", themes=["Private credit risk is mispriced"]),
         _bundle("src-b", themes=["Direct lending spreads too tight"])]
    c = [_sc("src-a"), _sc("src-b")]
    first = _run(b, c).model_dump_json()
    assert all(_run(b, c).model_dump_json() == first for _ in range(3))


def test_no_trade_confirmation_and_no_trade_fields():
    res = _run([_bundle("src-a", themes=["x theme"])], [_sc("src-a")])
    assert res.no_trade_confirmation
    dumped = res.model_dump()
    for forbidden in ("sizing", "hedge_ratio", "scenario_probabilities", "trade", "q_s"):
        assert forbidden not in dumped
