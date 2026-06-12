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


def test_no_trade_confirmation_and_no_trade_fields():
    res = _run([_bundle("src-a", themes=["x theme"])], [_sc("src-a")])
    assert res.no_trade_confirmation
    dumped = res.model_dump()
    for forbidden in ("sizing", "hedge_ratio", "scenario_probabilities", "trade", "q_s"):
        assert forbidden not in dumped
