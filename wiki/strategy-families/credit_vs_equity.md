---
type: strategy_family
access_class: method
title: credit_vs_equity
slug: credit_vs_equity
aliases: []
tags: [strategy-family]
sources: []
status: active
created: 2026-06-06
updated: 2026-06-06
family_type: credit_vs_equity
downstream_model: cross-asset hedge-ratio model
typical_axes: [cross_asset]
typical_data_needed: [credit-equity betas, live credit + equity/vol levels]
typical_failure_modes: []
---

# credit_vs_equity

Cross-asset: credit vs equity / equity-vol.

- **Routed from axis shape(s):** cross_asset
- **Downstream model (out of discovery scope):** cross-asset hedge-ratio model
- **Data needed to advance to legs:** credit-equity betas, live credit + equity/vol levels

This page mirrors the engine taxonomy: `StrategyFamilyRec.family` (engine/schema/strategy_family.py) and the
`_DOWNSTREAM` routing templates (engine/discovery.py). Discovery stops at routing this
family with a decomposed confidence; detailed legs/sizing/hedges are downstream.

## Sources
_None yet._

## Notes
