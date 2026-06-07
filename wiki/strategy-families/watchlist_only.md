---
type: strategy_family
access_class: method
title: watchlist_only
slug: watchlist_only
aliases: []
tags: [strategy-family]
sources: [jpm-ai-capex-funding-2026-05-11]
status: active
created: 2026-06-06
updated: 2026-06-06
family_type: watchlist_only
downstream_model: (none — not tradable yet)
typical_axes: []
typical_data_needed: [an operational axis, supplied scenarios, and a falsifier]
typical_failure_modes: []
---

# watchlist_only

No tradeable family yet — route here when nothing clears confidence.

- **Routed from axis shape(s):** _(not auto-routed by the engine yet)_
- **Downstream model (out of discovery scope):** (none — not tradable yet)
- **Data needed to advance to legs:** an operational axis, supplied scenarios, and a falsifier

This page mirrors the engine taxonomy: `StrategyFamilyRec.family` (engine/schema.py) and the
`_DOWNSTREAM` routing templates (engine/discovery.py). Discovery stops at routing this
family with a decomposed confidence; detailed legs/sizing/hedges are downstream.

## Sources
- [[jpm-ai-capex-funding-2026-05-11]] — AI-capex credit ecosystem (CASE)

## Case priors
- **JPM AI capex (2026-05-11).** Default for [[hy-hpc-crowding-and-supply]] (crowded; promote only
  on a named reversal condition — flows turning) and for any AI-credit axis lacking a confirmed
  clean differential, supplied scenarios, and a falsifier.

## Notes
