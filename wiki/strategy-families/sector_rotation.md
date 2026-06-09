---
type: strategy_family
access_class: method
title: sector_rotation
slug: sector_rotation
aliases: []
tags: [strategy-family]
sources: []
status: active
created: 2026-06-08
updated: 2026-06-08
family_type: sector_rotation
downstream_model: sector-basket construction (overweight/underweight, beta- or DV01-neutral)
typical_axes: [cross_sector_spread_differential]
typical_data_needed: [per-sector OAS baskets, sector betas, constituent liquidity]
typical_failure_modes: [rotation driven by index/duration technical or a single name, not a sector view; sector definitions unstable across index rebalances]
---

# sector_rotation

Relative-value view across credit sectors — overweight one sector basket versus another (or
versus the broad index) on a cross-sector spread differential.

- **Routed from axis shape(s):** cross_sector_spread_differential (a relative-value axis between
  two sector baskets)
- **Not auto-routed by the engine yet** — taxonomy page. `_route_family` collapses generic
  relative-value axes to [[long_short]]; there is no dedicated sector_rotation routing rule, so
  this family is a discovery *hint*, not an engine output.
- **Downstream model (out of discovery scope):** sector-basket construction
  (overweight/underweight, beta- or DV01-neutral)
- **Data needed to advance to legs:** per-sector OAS baskets, sector betas, constituent liquidity

## Sources
- Taxonomy page; no contributing source has been linted into it yet.

## Notes
- Distinguish a genuine sector view from a duration/supply technical or a single-name move
  dominating the basket — see the failure modes above and [[curve]] for the analogous
  technical-vs-view caution.
