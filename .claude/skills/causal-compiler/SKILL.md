---
skill_name: causal-compiler
access_class: method
pipeline_phase: discovery_expand_causal
provider_seam: [LLMProvider.expand_causal, Provider.expand_causal]
input_objects: [raw_thesis, report_evidence, IcebergClassification, causal_claims, method_context]
output_objects: [CausalChain, main_theme, driver, mediators, outcome_variable, confounders, falsifiers, operational_axis_candidates, identification_status]
gates_created: [no_causal_chain_blocks, no_axis_routes_to_watchlist, association_is_not_causation]
allowed_to_influence: [causal chain structure, promotion to main_theme, operational-axis candidates, identification_status]
not_allowed_to_influence: [effect-size estimation, pricing, sizing, expressions, scenario probabilities]
failure_modes: [correlation-as-causation, promoting a hot topic, claiming an effect that is only associational, missing falsifier]
tests: [test_causal_chain_hyperscaler_neocloud_project, test_causal_missing_chain_blocks, test_causal_missing_axis_watchlist]
---

# Causal Compiler

> **Compiled from** *Thinking in Systems and Mental Models* (Dawson) — iceberg structure layer
> and behaviour-over-time — and *Thinking in Systems* (Meadows) — mediators / feedback;
> with the engine's own causal method. METHOD card: no case conclusions, no trades.

## Purpose
Convert an investment narrative into a **causal object**: driver → transmission channel(s)
→ market outcome, with confounders, falsifiers and operational-axis candidates.

## Process primitives
Distinguish three rungs of causal claim — **association** (X moves with Y), **intervention**
(doing X changes Y), **counterfactual** (had X not happened, Y would differ). A narrative that
is only associational is not a causal theme. The causal method is:
`assumptions + causal model + query + data → is it answerable? → only then an estimand/estimate`.
Separate **mediators** (on the causal path, channels) from **confounders** (common causes of
both driver and outcome that create spurious association). Meadows' lens: the chain is a
structure of stocks/flows/feedback; the outcome variable is the operational axis.

## When to use
Right after iceberg classification, on any promoted `CoreThemeCandidate`, in Phase A fresh reasoning.

## Inputs
Raw thesis, report evidence, `IcebergClassification`, extracted causal claims, method memory.

## Outputs
`CausalChain`, promoted `main_theme`, driver, mediators, outcome variable, confounders,
falsifiers, `operational_axis_candidates`, `identification_status`.

## Required fields
A causal driver; ≥1 mediator/channel; a market outcome; ≥1 confounder (or explicit "none known");
≥1 falsifier; ≥1 operational axis for any promoted theme.

## Validation rules
- Do not confuse correlation with causation.
- Do not claim a causal effect if the evidence is purely associational.
- Do not treat a hot topic as a causal theme.
- Missing chain → `blocked` / `needs_causal_object`.
- Missing axis → `watchlist` / `research_more`.

## Failure / blocked states
- No connected chain from driver to outcome → `blocked: needs_causal_object`.
- Chain present but no operational axis → `watchlist_only` (research the axis).
- Only association, no mechanism → `challenge_model`.

## Example input
"AI capex funding is changing credit RV across hyperscalers, DC project bonds, and HY compute issuers."

## Example output
Chain: AI-infrastructure demand → hyperscaler capex/leasing → project-level financing → growth
in DC/compute bond universe → valuation dispersion across related obligations.
- Confounders: rating, duration, liquidity, security/guarantee, construction risk, index eligibility.
- Falsifiers: basis fully explained by rating/duration/liquidity; relationships fail out of sample;
  index inclusion has no liquidity/spread effect.
- operational_axis_candidates: `project_OAS − hyperscaler_OAS`; identification_status: associational-until-netted.

## Non-goals
No effect-size estimation, no trade construction, no scenario probabilities.
