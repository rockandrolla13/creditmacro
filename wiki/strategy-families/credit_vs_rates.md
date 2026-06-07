---
type: strategy_family
access_class: method
title: credit_vs_rates
slug: credit_vs_rates
aliases: []
tags: [strategy-family]
sources: []
status: active
created: 2026-06-06
updated: 2026-06-06
family_type: credit_vs_rates
downstream_model: cross-asset duration/hedge-ratio model
typical_axes: [cross_asset]
typical_data_needed: [asset-swap/z-spread, live rates, DV01 map]
typical_failure_modes: []
---

# credit_vs_rates

Cross-asset: credit vs rates / duration.

- **Routed from axis shape(s):** cross_asset
- **Downstream model (out of discovery scope):** cross-asset duration/hedge-ratio model
- **Data needed to advance to legs:** asset-swap/z-spread, live rates, DV01 map

This page mirrors the engine taxonomy: `StrategyFamilyRec.family` (engine/schema.py) and the
`_DOWNSTREAM` routing templates (engine/discovery.py). Discovery stops at routing this
family with a decomposed confidence; detailed legs/sizing/hedges are downstream.

## Sources
_None yet._

## Notes
