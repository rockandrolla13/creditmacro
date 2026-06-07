---
type: strategy_family
access_class: method
title: long_short
slug: long_short
aliases: []
tags: [strategy-family]
sources: []
status: active
created: 2026-06-06
updated: 2026-06-06
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

This page mirrors the engine taxonomy: `StrategyFamilyRec.family` (engine/schema.py) and the
`_DOWNSTREAM` routing templates (engine/discovery.py). Discovery stops at routing this
family with a decomposed confidence; detailed legs/sizing/hedges are downstream.

## Sources
_None yet._

## Notes
