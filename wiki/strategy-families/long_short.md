---
type: strategy_family
access_class: method
title: long_short
slug: long_short
aliases: []
tags: [strategy-family]
sources: [jpm-ai-capex-funding-2026-05-11]
status: active
created: 2026-06-06
updated: 2026-06-07
family_type: long_short
downstream_model: pair construction + beta/notional neutralisation
typical_axes: [relative_value]
typical_data_needed: [live spreads on both legs, beta, borrow/financing]
typical_failure_modes: []
---

# long_short

Relative-value pair: exposed leg underperforms a control leg.

- **Routed from axis shape(s):** relative_value
- **Downstream model (out of discovery scope):** pair construction + beta/notional neutralisation
- **Data needed to advance to legs:** live spreads on both legs, beta, borrow/financing

This page mirrors the engine taxonomy: `StrategyFamilyRec.family` (engine/schema/strategy_family.py) and the
`_DOWNSTREAM` routing templates (engine/discovery.py). Discovery stops at routing this
family with a decomposed confidence; detailed legs/sizing/hedges are downstream.

## Sources
- [[jpm-ai-capex-funding-2026-05-11]] — AI-capex credit ecosystem (CASE)

## Case priors
- **JPM AI capex (2026-05-11) — TOP prior for this source.** Related-obligation RV across the
  legs: hyperscaler vs project (≈105bp IG / 183bp HY), DC sub-sector vs Technology (181 vs 101bp),
  HY HPC vs HY index. See [[related-obligation-rv]], theme [[ai-capex-funding-credit-ecosystem]].
  Confidence capped by: clean-differential check, duration/rating netting, leg liquidity. **No legs.**

## Notes
