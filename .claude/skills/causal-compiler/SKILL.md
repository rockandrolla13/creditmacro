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
tests: [test_causal_chain_hyperscaler_neocloud_project, test_causal_missing_chain_blocks, test_causal_missing_axis_watchlist, test_causal_asymmetry_counterfactual]
---

# Causal Compiler

> **Compiled from** *Thinking in Systems and Mental Models* (Dawson) — iceberg structure layer
> and behaviour-over-time — *Thinking in Systems* (Meadows) — mediators / feedback — and
> *Time, Tense, and Causation* (Tooley) — causal asymmetry and the direction of counterfactual
> dependence; with the engine's own causal method. METHOD card: no case conclusions, no trades.

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

## Causal asymmetry — what makes a causal object VALID
A causal claim is more than co-movement. Three checks sharpen validity (compiled from Tooley):
- **Direction / temporal priority.** A cause does not follow its effect: the driver must lead, or
  at least not lag, the outcome. The cause *brings the effect into being*, not the reverse. A
  series that only co-moves with the axis — or that trails it — is not a driver; flag it and
  re-orient the arrow.
- **Counterfactual dependence, not constant conjunction.** The weakest rung is *constant
  conjunction* (driver and outcome are merely regularly observed together) — this is exactly what
  spurious correlation looks like. Demand the **counterfactual**: *had the driver not moved, the
  axis would differ.* If you cannot articulate that counterfactual, you have association, not a
  causal theme.
- **Asymmetry of dependence.** Counterfactual dependence runs forward: the effect depends on the
  driver, not vice versa. If reversing the arrow reads equally well (the outcome could just as
  plausibly be driving the "driver"), the direction is unidentified — mark `direction_unidentified`
  rather than asserting causation.
- **Causal, not temporal, backtracking.** When you reason "what if the driver were different",
  hold fixed what is *causally prior* to the driver — not merely everything earlier in time — and
  do not let the driver's own downstream consequences leak back into the counterfactual world.

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

## Additional rules from Causality and Explanation (Salmon)
(Causal-mechanical view; from the "Causal Processes and Pseudo-Processes" essays.)
- Separate a **causal process** (one that can carry a *mark* — a local modification that
  propagates onward under its own steam) from a **pseudo-process** (one that exhibits perfect
  regularity / co-movement but cannot transmit a mark; its features are inherited from an outside
  common source). Salmon's spotlight-spot sweeping a wall co-moves flawlessly yet transmits
  nothing. Two pseudo-processes driven by a shared source is exactly what **spurious correlation**
  looks like.
- **Mark-transmission test for a candidate channel.** Imagine perturbing the driver at one point
  and ask whether that perturbation would travel *along the channel* through identifiable
  intervening structure. If the modification does not propagate on its own — only the endpoints
  happen to co-move — the link is a pseudo-process, not a causal channel: flag it, do not promote.
- **Mark counterfactual condition** (Salmon's amendment after Cartwright's objection): the
  downstream change must be one that would *not* have occurred had the mark not been introduced.
  If the outcome would have moved anyway (a redundant or over-determined common cause), the
  apparent transmission is spurious — mark it, not a driver.
- Demand the **intervening mechanism/structure**, not bare endpoint co-movement: a genuine channel
  localizes and carries a perturbation; this is the physical content behind requiring ≥1 mediator.
- Axis use: an axis whose moves are inherited from a common factor (rating/duration/liquidity) is a
  pseudo-process *relative to the thesis driver* until that factor is netted out — keeps
  `identification_status: associational-until-netted`.

## Additional rules from Counterfactuals and Probability (Schulz)
(What a well-posed counterfactual query requires; from the intro and Adams's-thesis sections.)
- A counterfactual's credence ≈ the **conditional probability of the consequent given the
  antecedent scenario** (Ramsey/Adams test). "Had the driver not moved, the axis would differ" is
  evaluated by asking how likely the axis-change is across the scenarios where the antecedent
  holds — express it as a likelihood, not a bare yes/no.
- Two sources of uncertainty unique to counterfactuals: (i) the **antecedent can be realized many
  ways** — if different realizations give conflicting verdicts on the outcome, the query is
  under-specified; pin down *how* the driver is moved. (ii) even with the antecedent fixed, the
  world can **unfold many ways** (residual chance) — a single point answer overstates certainty.
- **Positivity requirement:** the conditional probability is only defined when the antecedent has
  positive probability. A counterfactual built on a zero / negligible-probability antecedent is
  ill-posed — flag it rather than assert a verdict.
- **Forward projection:** hold the antecedent fixed and project the world forward from that point;
  do not backtrack into causally prior facts (consistent with the asymmetry rules above).
