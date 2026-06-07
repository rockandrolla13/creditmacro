---
type: strategy_family
access_class: method
title: steepener
slug: steepener
aliases: []
tags: [strategy-family]
sources: []
status: active
created: 2026-06-06
updated: 2026-06-06
family_type: steepener
downstream_model: curve construction + DV01-neutral leg ratios
typical_axes: [curve]
typical_data_needed: [live per-tenor OAS, basket constituents, per-tenor DV01]
typical_failure_modes: []
---

# steepener

Long the curve slope — routed from (curve, steeper).

- **Routed from axis shape(s):** curve
- **Downstream model (out of discovery scope):** curve construction + DV01-neutral leg ratios
- **Data needed to advance to legs:** live per-tenor OAS, basket constituents, per-tenor DV01

This page mirrors the engine taxonomy: `StrategyFamilyRec.family` (engine/schema.py) and the
`_DOWNSTREAM` routing templates (engine/discovery.py). Discovery stops at routing this
family with a decomposed confidence; detailed legs/sizing/hedges are downstream.

## Sources
_None yet._

## Notes
