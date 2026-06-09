---
type: strategy_family
access_class: method
title: capital_structure
slug: capital_structure
aliases: []
tags: [strategy-family]
sources: []
status: active
created: 2026-06-08
updated: 2026-06-08
family_type: capital_structure
downstream_model: intra-issuer pair construction (subordination-adjusted leg ratios)
typical_axes: [intra_issuer_spread_differential]
typical_data_needed: [per-tranche spreads (senior/sub/hybrid), recovery/subordination assumptions, matched-tenor financing]
typical_failure_modes: [subordination or recovery assumption mis-specified; "differential" is really a liquidity/issuance technical between tranches; tranche call/extension optionality not modelled]
---

# capital_structure

Relative-value view *within a single issuer's* capital structure — e.g. senior vs subordinated,
hybrid vs senior, or bond vs CDS of the same name — on an intra-issuer spread differential.

- **Routed from axis shape(s):** relative_value, sub-typed by subordination vocabulary
  (subordinated, AT1, tier 2, hybrid, holdco-vs-opco) in `engine/discovery._relative_value_subtype`.
- **Auto-routed by the engine** — in the `StrategyFamilyRec.family` Literal. Note the split: a
  same-issuer **bond-vs-CDS** axis still routes to [[cash_cds_basis]] (the `basis` shape wins);
  capital_structure captures the **subordination** play (senior vs sub / hybrid / AT1), not the
  cash-CDS basis. A plain name-vs-name pair stays [[long_short]].
- **Downstream model (out of discovery scope):** intra-issuer pair construction
  (subordination-adjusted leg ratios)
- **Data needed to advance to legs:** per-tranche spreads (senior/sub/hybrid),
  recovery/subordination assumptions, matched-tenor financing

## Sources
- Taxonomy page; no contributing source has been linted into it yet.

## Notes
- The differential must reflect a subordination/recovery view, not a liquidity or issuance
  technical between tranches; model call/extension optionality on hybrids before legs.
