---
skill_name: macro-regime-classifier
access_class: method
pipeline_phase: discovery_macro_context
provider_seam: [macro_context]
input_objects: [macro_indicators, regime_signals, CausalChain, theme_candidates]
output_objects: [MacroRegimeClassification, regime_state, cross_asset_propagation_map, affected_asset_classes, regime_conditional_strategy_families, regime_risks, regime_opportunities]
gates_created: [regime_from_observable_data_not_narrative, propagation_through_mechanism_not_correlation, flag_regime_transition_risk]
allowed_to_influence: [regime state, cross-asset propagation, regime-conditional family viability, regime risks/opportunities]
not_allowed_to_influence: [macro forecasts, GDP/policy predictions, pricing, sizing, trades]
failure_modes: [narrative-driven regime call, correlation mistaken for propagation, assuming one regime persists, over-confidence on thin data]
tests: [test_macro_regime_card_exists, test_macro_seam_pending_method_context]
---

# Macro Regime Classifier

> **Compiled from** *Citi Views Macro Book* (`markdowns/CITI VIEWS MACRO BOOK.md`):
> cross-asset regimes, scenario (bear/base/bull) framing, and macro→asset-class propagation.
> METHOD card: no forecasts, no trades. **Seam status: pending** — until a macro-context seam is
> added, this card is available as method context for any discovery seam.

## Purpose
Classify the **macro regime state** and determine how macro themes **propagate across asset
classes** — i.e. "high inflation + AI capex → which sectors, which curve shape, which assets."

## Process primitives (paraphrased from the macro book)
- Macro variables — **growth, inflation, policy, liquidity** — interact as a *system*; a
  **regime** is a joint state of these (e.g. reflation, stagflation, goldilocks, late-cycle).
- The regime changes **which strategy families are viable and which are dangerous** (a basis/RV
  regime vs a directional one).
- **Cross-asset linkage**: trace a theme through mechanisms — e.g. issuance pressure → rates
  (curve shape), demand-for-yield → credit spreads, capex beneficiaries → equity sector rotation,
  capital flows → FX. Offsetting mechanisms can turn a directional view into a *dispersion/basis*
  opportunity.
- Frame outcomes as **scenarios (bear / base / bull)** with the macro mechanism behind each;
  watch for **regime-transition** risk (don't assume one regime persists).

## When to use
As macro context for any discovery seam, when a theme has cross-asset reach (rates/credit/equity/FX).

## Inputs
Macro indicators, current regime signals, causal chain, theme candidates.

## Outputs
`MacroRegimeClassification`, `regime_state`, `cross_asset_propagation_map`,
`affected_asset_classes[]`, `regime_conditional_strategy_families[]`, `regime_risks[]`,
`regime_opportunities[]`.

## Validation rules
- Regime classification must be based on **observable macro data**, not narrative.
- Cross-asset propagation must trace **causal mechanisms**, not correlation.
- Do not assume one regime persists — flag regime-transition risks.
- If macro data is insufficient, say so and cap confidence.

## Failure / blocked states
- Thin/insufficient macro data → low-confidence classification + `regime_risks: data_insufficient`.
- Propagation that is only correlational → drop the link or mark it `mechanism_unverified`.

## Example
- Regime: late-cycle expansion with rising inflation expectations.
- Propagation: AI capex → issuance pressure → steeper curves (supply) **but** → tighter credit
  spreads (demand for yield) — offsetting, creating a **basis/dispersion** opportunity rather than
  a directional one.
- Affected: credit (compute/DC), rates (curve shape), equities (capex beneficiaries).
- Regime risk: if inflation forces aggressive tightening, the whole AI-capex credit ecosystem
  faces refinancing risk simultaneously (shared factor).

## Non-goals
No specific macro forecasts, no GDP predictions, no policy predictions, no trades, no sizing.
