---
type: concept
access_class: method
title: Index-inclusion technical
slug: index-inclusion-technical
tags: [concept, index, technical, flows]
status: active
sources: [jpm-ai-capex-funding-2026-05-11]
created: 2026-06-07
updated: 2026-06-07
---

# Index-inclusion technical

## What it is
The demand pressure created when a bond/sub-sector enters (or is excluded from) a benchmark
index that has index-tracking AUM behind it (ETFs, index funds, mandates).

## Mechanics (how to reason)
Inclusion → passive/index-tracking holders must buy → technical spread compression for included
names vs otherwise-equivalent excluded names. Strength scales with the **index's tracking-AUM
share**; it differs across index families (JULI vs Bloomberg US Agg vs Global Agg vs ICE), so the
"basis" is **index-rule-dependent**. A reflexive loop: inclusion → tightening → more issuance.

## Operational-axis form
`included-name OAS − matched-excluded-name OAS`; cross-index: same exposure priced in a
large-tracking-AUM index vs a small one. A candidate [[index_index_rv]] / [[etf_basket_rv]] axis.

## Confounders
Duration and quality differences that masquerade as a technical; which index actually has the
tracking AUM; rebalance-timing lags (delays cause overshoot).

## Linked
[[data-center-credit]] · families [[index_index_rv]] / [[etf_basket_rv]] · theme
[[data-center-index-inclusion-technicals]].
