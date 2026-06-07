---
type: theme
access_class: case
title: Hyperscaler vs project-bond basis
slug: hyperscaler-project-bond-basis
tags: [theme, relative-value, basis, ai-capex]
theme_status: core_theme_candidate
status: active
main_developments: ["measurable hyperscaler-vs-project spread relationships (105bp IG / 183bp HY)"]
key_events: []
hot_topics: []
causal_chain: ["same AI-capex driver funds hyperscaler IG and project bonds at different risk profiles → a spread relationship"]
operational_axes: ["hyperscaler IG OAS − IG DC-project OAS (~105bp)", "hyperscaler IG OAS − HY DC-project OAS (~183bp)"]
confounders: ["duration", "rating/subordination", "liquidity premium", "standing risk premium"]
falsifiers: ["differential mean is unstable / not mean-reverting over the sample"]
strategy_families: [long_short, watchlist_only]
sources: [jpm-ai-capex-funding-2026-05-11]
created: 2026-06-07
updated: 2026-06-07
---

# Hyperscaler vs project-bond basis

## Current belief
There is a **named, computable spread relationship** between hyperscaler IG credit and the
data-center project bonds funded by the same capex — a candidate operational axis for a
related-obligation long_short, *if* the differential is clean and mean-reverting.

## Source facts vs agent synthesis
**Source facts:** average hyperscaler-to-IG-project 105bp ([[evidence:jpm-2026-05-11-003]]);
hyperscaler-to-HY-project 183bp ([[evidence:jpm-2026-05-11-004]]); the legs are "related
obligations" ([[evidence:jpm-2026-05-11-002]]). **Agent synthesis:** that this is an *axis*
(a tradeable differential) is an inference; JPM reports the *level* of the relationship, not
its tradeability or mean-reversion.

## Main developments
The relationship is now quantified at two risk profiles (IG and HY project).

## Key events
*(none dated in source.)*

## Hot topics
*(none specific.)*

## Core causal hypothesis
One capex driver funds both legs; structural differences (recourse, subordination, duration)
set a *level* for the differential; deviations from that level are the candidate RV signal.

## Causal graph
`AI capex` → `hyperscaler IG issuance` and → `DC project issuance` → `differential (105/183bp)`.
The differential is the outcome node; it is the operational axis.

## Operational axes
`hyperscaler IG OAS − IG DC-project OAS` (~105bp); `hyperscaler IG OAS − HY DC-project OAS`
(~183bp). Duration/rating-adjusted versions preferred (see confounders).

## Confounders
Duration, rating/subordination, liquidity premium, and the standing credit risk premium — any
of which can explain the level without it being a mispricing.

## Falsifiers
The differential is not stationary / not mean-reverting over the available history (no signal),
or it is fully explained by a duration/rating regression (no residual edge).

## Scenario memory
*(empty.)*

## Strategy-family priors (source-suggested)
1. [[long_short]] (hyperscaler vs project, beta/duration-neutral — downstream) · watchlist:
[[watchlist_only]] until the differential series is built and netted.

## What changed after latest source
The basis went from unmeasured to quantified (105bp IG, 183bp HY) by JPM 2026-05-11.

## Open questions
Is the differential mean-reverting? Is it clean of duration/rating? **Not trade-ready** — needs
the series, the netting, and a liveness/liquidity check on the project-bond leg.
