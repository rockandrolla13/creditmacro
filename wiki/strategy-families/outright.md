---
type: strategy_family
access_class: method
title: outright
slug: outright
aliases: []
tags: [strategy-family]
sources: []
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

This page mirrors the engine taxonomy: `StrategyFamilyRec.family` (engine/schema.py) and the
`_DOWNSTREAM` routing templates (engine/discovery.py). Discovery stops at routing this
family with a decomposed confidence; detailed legs/sizing/hedges are downstream.

## Sources
_None yet._

## Notes
