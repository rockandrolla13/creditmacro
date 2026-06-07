---
type: strategy_family
access_class: method
title: index_index_rv
slug: index_index_rv
aliases: []
tags: [strategy-family]
sources: [jpm-ai-capex-funding-2026-05-11]
status: active
created: 2026-06-07
updated: 2026-06-07
family_type: index_index_rv
downstream_model: matched-exposure construction across index definitions
typical_axes: [index_basis]
typical_data_needed: [same-name spread in each index, index-tracking AUM by family, inclusion rules]
typical_failure_modes: [inclusion difference is duration/quality not technical]
---

# index_index_rv

Same economic exposure priced differently across index definitions (inclusion-rule technical).

- **Routed from axis shape(s):** index_basis
- **Not auto-routed by the engine yet** — taxonomy page; `index_index_rv` is not yet in the
  `StrategyFamilyRec.family` Literal / `engine/discovery._route_family` rules (capability not overstated).
- **Downstream model (out of discovery scope):** matched-exposure construction across index definitions
- **Data needed to advance to legs:** same-name spread in each index, index-tracking AUM by family, inclusion rules

## Sources
- [[jpm-ai-capex-funding-2026-05-11]] — AI-capex credit ecosystem (CASE)

## Case priors
- **JPM AI capex (2026-05-11) — 2nd prior.** Data-Center sub-sector inclusion differs across JULI /
  Bloomberg US Agg / Global Agg / ICE, with large IG ETF + mutual-fund AUM in the US Agg family —
  a candidate index-vs-index technical. See [[index-inclusion-technical]], theme
  [[data-center-index-inclusion-technicals]]. **No legs.**

## Notes
