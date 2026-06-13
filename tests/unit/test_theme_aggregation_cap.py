"""L3 — aggregator parent cap (the theme-discipline down payment).

Acceptance (plan §2 L3): with a configurable parent cap, N>cap promoted clusters emit at most
`cap` non-watchlist parents; the tail (lowest promotion_score) is demoted to `watchlist`, NOT
dropped; the demotion count is logged. Default (no cap) is unchanged behavior.

NOTE the fixtures use per-theme-DISTINCT concept/market-var/axis tokens on purpose: shared tokens
would lexically over-merge into one cluster (the very theme-explosion failure mode this cap exists
to mitigate downstream).
"""
from __future__ import annotations

from datetime import date

from engine.evidence_extraction import (
    EvidenceExtractionBundle,
    OperationalAxisCandidate,
    StrategyFamilyHint,
)
from engine.schema.probability import EvidenceAtom
from engine.temporal import TemporalContext
from engine.theme_aggregation import ThemeAggregationPolicy, aggregate_theme_candidates
from engine.wiki_agents import SourceClassification

THEMES = ["alpha credit mispriced", "bravo rates dislocation", "charlie capex funding",
          "delta bank stress", "echo basis widening"]


def _bundle(slug, theme, i):
    return EvidenceExtractionBundle(
        source_slug=slug, core_theme_candidates=[theme],
        operational_axes=[OperationalAxisCandidate(
            axis_name=f"ax{i}", axis_shape="basis", observable_series=f"ax{i}_s")],
        strategy_family_hints=[StrategyFamilyHint(
            family="relative_value", rationale="rv", confidence=0.5)],
        evidence_atoms=[
            EvidenceAtom(evidence_id=f"{slug}-e1", source_slug=slug, claim="c1", themes=[theme],
                         concepts=[f"concept{i}"], market_variables=[f"var{i}"]),
            EvidenceAtom(evidence_id=f"{slug}-e2", source_slug=slug, claim="c2", themes=[theme])])


def _sc(slug):
    return SourceClassification(source_slug=slug, source_type="report", access_class="case",
                                copyright_status="copyright", ingestion_policy="summarize")


def _tc(slug):
    return TemporalContext(source_slug=slug, current_date=date(2026, 6, 12),
                           temporal_role="current_report", current_update_required=False)


def _batch(n):
    slugs = [f"src-{i}" for i in range(n)]
    bundles = [_bundle(s, THEMES[i], i) for i, s in enumerate(slugs)]
    return bundles, [_sc(s) for s in slugs], [_tc(s) for s in slugs], frozenset(slugs)


def _agg(n, **pol):
    bundles, classes, temporals, slugs = _batch(n)
    return aggregate_theme_candidates(
        bundles, classes, temporals,
        ThemeAggregationPolicy(current_input_slugs=slugs, **pol))


def test_no_cap_by_default_keeps_all_promoted():
    res = _agg(5)
    assert len(res.clusters) == 5
    assert all(c.theme_status == "promote_to_discovery" for c in res.clusters)
    assert not any("parent_cap" in w for w in res.warnings)


def test_cap_demotes_tail_to_watchlist_and_logs():
    res = _agg(5, parent_cap=2)
    assert len(res.clusters) == 5                                    # nothing dropped
    non_watch = [c for c in res.clusters if c.theme_status != "watchlist"]
    assert len(non_watch) == 2                                       # exactly cap parents kept
    assert sum(1 for c in res.clusters if c.theme_status == "watchlist") == 3
    assert any("parent_cap=2" in w and "demoted 3" in w for w in res.warnings)


def test_cap_above_count_is_a_noop():
    res = _agg(3, parent_cap=7)
    assert len(res.clusters) == 3
    assert all(c.theme_status == "promote_to_discovery" for c in res.clusters)
    assert not any("parent_cap" in w for w in res.warnings)


def test_cap_keeps_highest_promotion_score_parents():
    res = _agg(5, parent_cap=2)
    kept = [c.promotion_score for c in res.clusters if c.theme_status != "watchlist"]
    demoted = [c.promotion_score for c in res.clusters if c.theme_status == "watchlist"]
    if kept and demoted:
        assert min(kept) >= max(demoted)                            # no demoted parent outranks a kept one
