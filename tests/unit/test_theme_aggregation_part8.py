"""PART 8 — deterministic acceptance matrix for the Multi-Source Theme Aggregator.
One test per enumerated requirement (items 1-20; 21 = full suite). No live API."""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from pydantic import ValidationError

import engine.theme_aggregation as ta
from engine.evidence_extraction import (
    EvidenceExtractionBundle,
    OperationalAxisCandidate,
    StrategyFamilyHint,
)
from engine.schema.probability import EvidenceAtom
from engine.schema.theme_aggregation import SourceAttribution, ThemeCluster
from engine.temporal import TemporalContext
from engine.theme_aggregation import ThemeAggregationPolicy, aggregate_theme_candidates
from engine.wiki_agents import REGISTRY
from engine.stage0 import rank_multi_source_theme_clusters


def _atom(eid, slug, themes=(), mvars=()):
    return EvidenceAtom(evidence_id=eid, source_slug=slug, claim=f"claim {eid}",
                        themes=list(themes), market_variables=list(mvars))


def _bundle(slug, *, themes=(), hot=(), atoms=(), axes=(), fams=()):
    return EvidenceExtractionBundle(
        source_slug=slug, core_theme_candidates=list(themes), hot_topics=list(hot),
        evidence_atoms=list(atoms), operational_axes=list(axes), strategy_family_hints=list(fams))


def _sc(slug, access="case", stype="report"):
    from engine.wiki_agents import SourceClassification
    return SourceClassification(source_slug=slug, source_type=stype, access_class=access,
                                copyright_status="c", ingestion_policy="summarize")


def _tc(slug, role="current_report"):
    return TemporalContext(source_slug=slug, current_date=date(2026, 6, 12),
                           temporal_role=role, current_update_required=False)


def _axis(n):
    return OperationalAxisCandidate(axis_name=n, axis_shape="basis", observable_series=n + "_s")


def _run(bundles, classes, temps=None, policy=None):
    return aggregate_theme_candidates(bundles, classes, temps, policy)


# 1. Agent contract exists and validates.
def test_01_agent_contract_validates():
    assert "MultiSourceThemeAggregatorAgent" in REGISTRY.list_agents()
    assert not REGISTRY.validate_agent_contracts()


# 2. Aggregator accepts multiple bundles.
def test_02_accepts_multiple_bundles():
    res = _run([_bundle("a", themes=["x"]), _bundle("b", themes=["y"])], [_sc("a"), _sc("b")])
    assert res.source_slugs == ["a", "b"]


# 3. Near-duplicate themes merge (shared spread-decompression structure).
def test_03_near_duplicates_merge():
    mv = ["credit_spread_decompression"]
    b1 = _bundle("s1", themes=["Private credit risk is mispriced"],
                 atoms=[_atom("e1", "s1", themes=["private credit risk is mispriced"], mvars=mv)])
    b2 = _bundle("s2", themes=["Direct lending spreads too tight"],
                 atoms=[_atom("e2", "s2", themes=["direct lending spreads too tight"], mvars=mv)])
    b3 = _bundle("s3", themes=["Software PC decompression"],
                 atoms=[_atom("e3", "s3", themes=["software pc decompression"], mvars=mv)])
    res = _run([b1, b2, b3], [_sc("s1"), _sc("s2"), _sc("s3")],
               [_tc("s1"), _tc("s2"), _tc("s3")])
    assert len(res.clusters) == 1
    assert res.clusters[0].source_count == 3


# 4. Unrelated themes do not merge.
def test_04_unrelated_do_not_merge():
    res = _run([_bundle("s1", themes=["ETF basket basis"]),
                _bundle("s2", themes=["Software refinancing stress"]),
                _bundle("s3", themes=["Europe vs US equity valuation"])],
               [_sc("s1"), _sc("s2"), _sc("s3")], [_tc("s1"), _tc("s2"), _tc("s3")])
    assert len(res.clusters) == 3


# 5. Same source multiple mentions ≠ independent corroboration.
def test_05_same_source_multiple_mentions_not_independent():
    b = _bundle("s1", themes=["Rates catch up"], hot=["Rates catch up"])  # mentioned twice
    res = _run([b], [_sc("s1")], [_tc("s1")])
    c = res.clusters[0]
    assert c.source_count == 1 and c.independent_source_count <= 1


# 6. Two independent sources increase corroboration.
def test_06_two_independent_sources_raise_corroboration():
    two = _run([_bundle("s1", themes=["Theme z"], atoms=[_atom("e1", "s1", themes=["theme z"])]),
                _bundle("s2", themes=["Theme z"], atoms=[_atom("e2", "s2", themes=["theme z"])])],
               [_sc("s1"), _sc("s2")], [_tc("s1"), _tc("s2")]).clusters[0]
    one = _run([_bundle("s1", themes=["Theme z"], atoms=[_atom("e1", "s1", themes=["theme z"])])],
               [_sc("s1")], [_tc("s1")]).clusters[0]
    assert two.corroboration_score > one.corroboration_score


# 7. Same publisher downweighted via independence_group.
def test_07_same_publisher_downweighted():
    pol = ThemeAggregationPolicy(publisher_groups={"jpm-1": "jpm", "jpm-2": "jpm"})
    res = _run([_bundle("jpm-1", themes=["Theme q"]), _bundle("jpm-2", themes=["Theme q"])],
               [_sc("jpm-1"), _sc("jpm-2")], [_tc("jpm-1"), _tc("jpm-2")], pol)
    assert res.clusters[0].independent_source_count == 1


# 8. High attention / weak evidence lowers divergence.
def test_08_high_attention_weak_evidence_low_divergence():
    res = _run([_bundle("s1", hot=["everyone loves the bubble narrative"])], [_sc("s1")], [_tc("s1")])
    assert res.clusters[0].evidence_attention_divergence < 0


# 9. Strong evidence / low attention raises divergence.
def test_09_strong_evidence_low_attention_high_divergence():
    res = _run([_bundle("s1", themes=["Solid credit thesis"],
                        atoms=[_atom("e1", "s1", themes=["solid credit thesis"])])],
               [_sc("s1")], [_tc("s1")])
    assert res.clusters[0].evidence_attention_divergence > 0


# 10. Archived CASE refused in Phase A unless current_input.
def test_10_archived_case_refused_unless_current():
    bundles = [_bundle("jpm", themes=["AI capex funding gap"])]
    refused = _run(bundles, [_sc("jpm", access="case")])   # no current marker
    assert refused.clusters == [] and any("jpm" in w for w in refused.warnings)
    pol = ThemeAggregationPolicy(current_input_slugs=frozenset({"jpm"}))
    allowed = _run(bundles, [_sc("jpm", access="case")], policy=pol)
    assert allowed.clusters       # included when declared current input


# 11. METHOD supplies aliases but is not market evidence.
def test_11_method_not_market_evidence():
    res = _run([_bundle("m1", themes=["Cycles"], atoms=[_atom("e1", "m1", themes=["cycles"])])],
               [_sc("m1", access="method")], [_tc("m1", role="method_source")])
    c = res.clusters[0]
    assert c.evidence_count == 0
    assert all(a.contribution_type == "method_context" for a in c.source_attributions)


# 12. European 2019 → historical_case/outcome_candidate, not current corroboration.
def test_12_european_2019_historical():
    res = _run([_bundle("eu-2019", themes=["European banks stress"],
                        atoms=[_atom("e1", "eu-2019", themes=["european banks stress"])])],
               [_sc("eu-2019", access="case")], [_tc("eu-2019", role="historical_case")])
    assert res.clusters[0].theme_status in ("historical_case", "outcome_candidate")


# 13. AI-capex themes merge across two AI reports; other AI themes stay separate.
def test_13_ai_capex_ecosystem_merges_not_all_ai():
    b1 = _bundle("jpm", themes=["AI capex funding gap", "AI chip demand"])
    b2 = _bundle("ms", themes=["AI capex funding gap", "AI software margins"])
    res = _run([b1, b2], [_sc("jpm"), _sc("ms")], [_tc("jpm"), _tc("ms")])
    by = {c.canonical_theme_name.lower(): c for c in res.clusters}
    capex = next(c for c in res.clusters if "capex" in c.canonical_theme_name.lower())
    assert capex.source_count == 2          # only the matching AI-capex theme merged
    assert len(res.clusters) == 3           # chip + software stayed separate


# 14. HY HPC crowding and hyperscaler-project basis remain separate.
def test_14_hpc_crowding_and_hyperscaler_basis_separate():
    b = _bundle("jpm", themes=["HY HPC crowding", "Hyperscaler project bond basis"])
    res = _run([b], [_sc("jpm")], [_tc("jpm")])
    assert len(res.clusters) == 2
    assert res.rejected_merges


# 15. ETF-flow fixture routes to an ETF/basket cluster.
def test_15_etf_flow_routes_to_etf_cluster():
    res = _run([_bundle("s1", themes=["ETF flow dislocation"])], [_sc("s1")], [_tc("s1")])
    assert any("etf" in c.canonical_theme_name.lower() for c in res.clusters)


# 16. Inflation/margin fixture routes to a sector/margin cluster.
def test_16_inflation_margin_routes_to_margin_cluster():
    res = _run([_bundle("s1", themes=["Inflation margin compression"])], [_sc("s1")], [_tc("s1")])
    assert any("margin" in c.canonical_theme_name.lower() for c in res.clusters)


# 17. Output contains evidence bullets + source attributions.
def test_17_output_has_bullets_and_attribution():
    res = _run([_bundle("s1", themes=["Credit thesis"],
                        atoms=[_atom("e1", "s1", themes=["credit thesis"])])],
               [_sc("s1")], [_tc("s1")])
    c = res.clusters[0]
    assert c.source_attributions and c.evidence_bullets


# 18. Promoted cluster without evidence fails validation.
def test_18_promoted_without_evidence_fails_validation():
    with pytest.raises(ValidationError):
        ThemeCluster(
            cluster_id="x", canonical_theme_name="t", canonical_thesis="t",
            theme_status="promote_to_discovery",
            source_attributions=[SourceAttribution(
                source_slug="s1", source_type="report", access_class="case",
                is_current_input=True, contribution_type="supports", evidence_ids=[])],
        )


# 19. No trades / sizing / hedge ratios / execution emitted.
def test_19_no_trade_fields():
    res = _run([_bundle("s1", themes=["x"])], [_sc("s1")])
    assert res.no_trade_confirmation
    dumped = res.model_dump()
    for k in ("sizing", "hedge_ratio", "scenario_probabilities", "trade", "execution", "q_s"):
        assert k not in dumped


# 20. Golden-master numerical functions are not imported/touched by the aggregator.
def test_20_no_pricing_or_scoring_imports():
    src = Path(ta.__file__).read_text()
    for forbidden in ("engine.scoring", "engine.engine2", "solve_q", "compute_edge",
                      "compute_omega", "run_pricing"):
        assert forbidden not in src


# bonus: the additive Stage-0 multi-source ranker orders discovery-first
def test_stage0_multi_source_ranker_is_additive():
    res = _run([_bundle("s1", themes=["Strong", "Weak buzz hot"],
                        atoms=[_atom("e1", "s1", themes=["strong"])], axes=[_axis("ax")]),
                ], [_sc("s1")], [_tc("s1")])
    ranked = rank_multi_source_theme_clusters(res)
    assert [c.cluster_id for c in ranked] == [c.cluster_id for c in
            sorted(res.clusters, key=lambda c: c.promotion_score, reverse=True)]
