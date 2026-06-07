---
type: theme
access_class: case
title: Data-center index-inclusion technicals
slug: data-center-index-inclusion-technicals
tags: [theme, index, technical, data-center]
theme_status: core_theme_candidate
status: active
main_developments: ["new Data Center sub-sector: $49bn par, 4.8% of Tech, 0.5% of JULI", "DC 181bp vs Tech 101bp"]
key_events: ["Data Center sub-sector added to JULI"]
hot_topics: []
causal_chain: ["index inclusion → index-tracking AUM demand → technical spread pressure"]
operational_axes: ["Data-Center sub-sector OAS − Technology OAS"]
confounders: ["duration", "index-rule heterogeneity (JULI vs US Agg vs Global Agg vs ICE)", "credit quality mix"]
falsifiers: ["inclusion attracts no measurable index-tracking demand"]
strategy_families: [index_index_rv, etf_basket_rv, long_short, watchlist_only]
sources: [jpm-ai-capex-funding-2026-05-11]
created: 2026-06-07
updated: 2026-06-07
---

# Data-center index-inclusion technicals

## Current belief
The new Data-Center sub-sector creates an **index-inclusion technical**: which index a name
sits in (JULI vs Bloomberg US Agg vs Global Agg vs ICE) drives index-tracking demand, so the
tradeable "basis" is index-rule-dependent. Candidate for index_index / ETF-basket RV.

## Source facts vs agent synthesis
**Source facts:** Data Center $49bn par, 4.8% of Tech, 0.5% of JULI ([[evidence:jpm-2026-05-11-006]]);
DC 181bp vs Tech 101bp, longer duration ([[evidence:jpm-2026-05-11-007]]); inclusion differs
across JULI/US Agg/Global Agg/ICE ([[evidence:jpm-2026-05-11-008]]); Bloomberg US Agg family has
large IG ETF + mutual-fund AUM share ([[evidence:jpm-2026-05-11-009]]).
**Agent synthesis:** that inclusion-rule differences are a *tradeable technical* is the agent's
inference; JPM reports the inclusion facts and AUM share, not a trade.

## Main developments
A new index sub-sector with a material spread gap to Technology and index-rule heterogeneity.

## Key events
Data Center sub-sector index entry.

## Hot topics
*(none specific.)*

## Core causal hypothesis
Index inclusion → passive/index-tracking AUM must hold the names → technical demand → spread
compression for included names relative to excluded equivalents.

## Causal graph
`index inclusion rule` → `index-tracking AUM demand (flow)` → `included-vs-excluded spread`.
Reflexive watch: inclusion → tightening → more issuance into the index.

## Operational axes
`Data-Center sub-sector OAS − Technology OAS` (181 vs 101bp); duration-adjusted preferred. A
cross-index version: same-name spread in an index with large tracking AUM vs one without.

## Confounders
Duration (DC longer), index-rule heterogeneity (the basis depends on which index), credit-quality
mix between DC and Technology.

## Falsifiers
Inclusion attracts no measurable index-tracking demand (the 181-vs-101 gap is pure duration/quality,
not a technical).

## Scenario memory
*(empty.)*

## Strategy-family priors (source-suggested)
1. [[index_index_rv]] (same exposure across index definitions) · 2. [[etf_basket_rv]] ·
3. [[long_short]] (DC vs Tech, duration-neutral — downstream) · watchlist: [[watchlist_only]].

## What changed after latest source
The sub-sector, its weights, the DC-vs-Tech gap, and the inclusion heterogeneity are new evidence.

## Open questions
Which index's rule defines the live technical? Is the DC-vs-Tech gap duration or technical?
**Not trade-ready** — needs the index-tracking-AUM mapping and a duration-clean axis.
