---
type: strategy_family
access_class: method
title: curve
slug: curve
aliases: []
tags: [strategy-family]
sources: [jpm-ai-capex-funding-2026-05-11]
status: active
created: 2026-06-07
updated: 2026-06-07
family_type: curve
downstream_model: curve construction (>=2 tenor points, DV01-neutral)
typical_axes: [curve_slope]
typical_data_needed: [spreads at >=2 tenors, DV01s, roll/carry]
typical_failure_modes: [slope move is duration/supply technical not a curve view]
---

# curve

Curve-shape view (slope / steepener / flattener) on a single name or sector.

- **Routed from axis shape(s):** curve_slope
- **Not auto-routed by the engine yet** — taxonomy page; the engine currently routes the explicit
  `steepener` / `flattener` families (see those pages), not a generic `curve`.
- **Downstream model (out of discovery scope):** curve construction (>=2 tenor points, DV01-neutral)
- **Data needed to advance to legs:** spreads at >=2 tenors, DV01s, roll/carry

## Sources
- [[jpm-ai-capex-funding-2026-05-11]] — AI-capex credit ecosystem (CASE)

## Case priors
- **JPM AI capex (2026-05-11) — secondary watchlist.** Data-Center / project credit is longer
  duration than Technology, so a curve/steepener angle is *secondary* — only after the primary RV
  ([[long_short]]) and the index technicals. See theme [[data-center-index-inclusion-technicals]].
  **No curve points, no legs.**

## Notes
