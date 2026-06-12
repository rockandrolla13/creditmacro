---
skill_name: Multi-Source Theme Aggregator
access_class: method
pipeline_phase: stage0_multi_source_discovery
provider_seam:
  - aggregate_theme_candidates
  - stage0
  - evidence_extraction
  - wiki_integration
input_objects:
  - EvidenceExtractionBundle
  - CandidateTheme
  - EvidenceAtom
  - TemporalContext
  - SourceClassification
output_objects:
  - MultiSourceThemeSet
  - ThemeCluster
  - SourceAttribution
  - ThemeCorroborationScore
gates_created:
  - no_archived_case_in_phase_a
  - no_duplicate_theme_clusters
  - theme_cluster_requires_source_attribution
  - historical_case_cannot_confirm_current_theme
  - no_trade_from_theme_aggregation
allowed_to_influence:
  - stage0 theme ranking
  - theme promotion status
  - evidence support quality
  - attention/crowding score
  - discovery input queue
not_allowed_to_influence:
  - exact trades
  - sizing
  - hedge ratios
  - execution
  - scenario probabilities
  - q/edge/Omega/scoring numerical functions
failure_modes:
  - duplicate_theme_not_merged
  - unrelated_themes_merged
  - stale_case_used_as_current_evidence
  - attention_confused_with_evidence
  - source_count_confused_with_independence
implementation_maturity: wired
---

# Multi-Source Theme Aggregator

Purpose:
Combine theme candidates from multiple current-input sources into one deduplicated,
source-attributed, ranked theme set.

Core idea:
A single source can identify themes, but only multiple sources can reveal corroboration,
consensus, attention, crowding, and contradictions.

The aggregator should answer:
1. Which themes are unique?
2. Which sources support each theme?
3. Which evidence atoms support each theme?
4. Are sources independent or clustered?
5. Is the theme evidence-rich or attention-rich?
6. Is the theme current, historical, stale, or mixed?
7. Should the theme be promoted to discovery, watchlist, historical outcome candidate, or rejected?

Non-goals:
- no trades
- no sizing
- no scenario probabilities
- no fair values
- no execution

## How to run it

Deterministic entry point (`engine/theme_aggregation.py`):

```python
from engine.theme_aggregation import aggregate_theme_candidates, ThemeAggregationPolicy

theme_set = aggregate_theme_candidates(
    bundles,                 # list[EvidenceExtractionBundle] — one per current-input source
    source_classifications,  # list[SourceClassification]
    temporal_contexts,       # list[TemporalContext] | None
    policy=ThemeAggregationPolicy(),   # alias_map, publisher_groups, weights, thresholds
)
# theme_set.clusters: unique ThemeClusters, ranked by promotion_score (discovery-ready first)
```

Pipeline position: this is the **Stage-0 multi-source** step. It runs over current-input
bundles *after* per-source evidence extraction and *before* discovery. Each cluster with
`theme_status == "promote_to_discovery"` becomes a discovery input; the aggregator then STOPS.

## Firewall

`access_class: method`. The aggregator runs in Phase A and must read only current-input /
method bundles. Archived **CASE** memory may not enter Phase A, and a historical/stale case
can never *confirm* a current theme — a cluster lacking current-input, source-backed
supporting evidence cannot be `promote_to_discovery` (enforced in `_route_status` and the
`ThemeCluster` validator). Case/historical sources contribute only as `historical_analogue`.

## Discipline

No trades, sizing, hedge ratios, execution, scenario probabilities, or fair values; the
component never touches q/edge/Omega/scoring. Every `MultiSourceThemeSet` carries an explicit
`no_trade_confirmation`. Dedup is deterministic (alias map + overlap coefficient); the
`distinct_pairs` guard keeps related-but-distinct themes apart and records each near-miss in
`rejected_merges`. Independence is counted by `independence_group`, not raw source count, so
multiple pages/reports from one publisher do not inflate corroboration.
