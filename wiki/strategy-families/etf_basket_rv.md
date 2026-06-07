---
type: strategy_family
access_class: method
title: etf_basket_rv
slug: etf_basket_rv
aliases: []
tags: [strategy-family]
sources: [jpm-ai-capex-funding-2026-05-11]
status: active
created: 2026-06-07
updated: 2026-06-07
family_type: etf_basket_rv
downstream_model: ETF vs underlying-basket / NAV construction
typical_axes: [etf_nav_basis]
typical_data_needed: [ETF price + NAV, basket constituents/weights, create/redeem mechanics]
typical_failure_modes: [basis is liquidity premium not mispricing]
---

# etf_basket_rv

Credit ETF vs its underlying basket / NAV (create-redeem-driven basis).

- **Routed from axis shape(s):** etf_nav_basis
- **Not auto-routed by the engine yet** — taxonomy page; `etf_basket_rv` is not yet in the
  `StrategyFamilyRec.family` Literal / `engine/discovery._route_family` rules.
- **Downstream model (out of discovery scope):** ETF vs underlying-basket / NAV construction
- **Data needed to advance to legs:** ETF price + NAV, basket constituents/weights, create/redeem mechanics

## Sources
- [[jpm-ai-capex-funding-2026-05-11]] — AI-capex credit ecosystem (CASE)

## Case priors
- **JPM AI capex (2026-05-11) — 3rd prior.** The Bloomberg US Agg family's large IG ETF + mutual-
  fund AUM share makes the Data-Center inclusion technical expressible via an ETF/basket wrapper.
  See [[index-inclusion-technical]], theme [[data-center-index-inclusion-technicals]]. **No legs.**

## Notes
