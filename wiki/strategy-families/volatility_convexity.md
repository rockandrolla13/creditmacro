---
type: strategy_family
access_class: method
title: volatility_convexity
slug: volatility_convexity
aliases: []
tags: [strategy-family]
sources: []
status: active
created: 2026-06-06
updated: 2026-06-06
family_type: volatility_convexity
downstream_model: option structure + greeks
typical_axes: [volatility]
typical_data_needed: [implied vol surface, option chain, skew]
typical_failure_modes: []
---

# volatility_convexity

Option / convexity expression of the view.

- **Routed from axis shape(s):** volatility
- **Downstream model (out of discovery scope):** option structure + greeks
- **Data needed to advance to legs:** implied vol surface, option chain, skew

This page mirrors the engine taxonomy: `StrategyFamilyRec.family` (engine/schema.py) and the
`_DOWNSTREAM` routing templates (engine/discovery.py). Discovery stops at routing this
family with a decomposed confidence; detailed legs/sizing/hedges are downstream.

## Sources
_None yet._

## Notes
