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
    res = _run([b1, b2], [_sc("jpm-1"), _sc("jpm-2")], policy=pol)
    c = res.clusters[0]
    assert c.source_count == 2
    assert c.independent_source_count == 1   # two pages/reports from one publisher ≠ independent


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


def test_no_trade_confirmation_and_no_trade_fields():
    res = _run([_bundle("src-a", themes=["x theme"])], [_sc("src-a")])
    assert res.no_trade_confirmation
    dumped = res.model_dump()
    for forbidden in ("sizing", "hedge_ratio", "scenario_probabilities", "trade", "q_s"):
        assert forbidden not in dumped
