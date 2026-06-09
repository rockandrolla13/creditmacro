---
type: strategy_family
access_class: method
title: cash_cds_basis
slug: cash_cds_basis
aliases: []
tags: [strategy-family]
sources: [jpm-ai-capex-funding-2026-05-11]
status: active
created: 2026-06-06
updated: 2026-06-06
family_type: cash_cds_basis
downstream_model: cash-CDS basis construction
typical_axes: [basis]
typical_data_needed: [bond asset-swap spread, matched-tenor CDS, repo/financing]
typical_failure_modes: []
---

# cash_cds_basis

Cash bond vs CDS basis (cash vs derivative).

- **Routed from axis shape(s):** basis
- **Downstream model (out of discovery scope):** cash-CDS basis construction
- **Data needed to advance to legs:** bond asset-swap spread, matched-tenor CDS, repo/financing

This page mirrors the engine taxonomy: `StrategyFamilyRec.family` (engine/schema/strategy_family.py) and the
`_DOWNSTREAM` routing templates (engine/discovery.py). Discovery stops at routing this
family with a decomposed confidence; detailed legs/sizing/hedges are downstream.

## Sources
- [[jpm-ai-capex-funding-2026-05-11]] — AI-capex credit ecosystem (CASE)

## Case priors
- **JPM AI capex (2026-05-11) — secondary/conditional.** JPM is cash-only data; this family
  applies only where liquid single-name CDS exists on the legs. Likely [[watchlist_only]] until
  CDS liquidity is confirmed. Not a primary prior for this source.

## Notes
