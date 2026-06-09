---
type: strategy_family
access_class: method
title: outright
slug: outright
aliases: []
tags: [strategy-family]
sources: [jpm-ai-capex-funding-2026-05-11]
status: active
created: 2026-06-06
updated: 2026-06-06
family_type: outright
downstream_model: instrument selection + sizing
typical_axes: [level]
typical_data_needed: [live level, instrument liquidity, carry]
typical_failure_modes: []
---

# outright

Directional level view on a single axis.

- **Routed from axis shape(s):** level
- **Downstream model (out of discovery scope):** instrument selection + sizing
- **Data needed to advance to legs:** live level, instrument liquidity, carry

This page mirrors the engine taxonomy: `StrategyFamilyRec.family` (engine/schema/strategy_family.py) and the
`_DOWNSTREAM` routing templates (engine/discovery.py). Discovery stops at routing this
family with a decomposed confidence; detailed legs/sizing/hedges are downstream.

## Sources
- [[jpm-ai-capex-funding-2026-05-11]] — AI-capex credit ecosystem (CASE)

## Case priors
- **JPM AI capex (2026-05-11) — lowest prior.** Only if a downstream beta model confirms residual
  value. AI-credit outright is crowded (HY HPC +9.99% YTD, tightened to 295bp) → prefer the RV
  families ([[long_short]], [[index_index_rv]]) over an outright level here.

## Notes
