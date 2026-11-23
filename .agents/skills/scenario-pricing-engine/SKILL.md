---
skill_name: scenario-pricing-engine
access_class: method
pipeline_phase: discovery_probability_and_pricing
provider_seam: [probability.justify_probabilities, engine2.run_pricing, engine2.solve_q_tilt, engine2.compute_edge]
input_objects: [ThemeObject, axis, supplied_scenarios, X_mkt, supplied_p_s, evidence_refs, pricing_constraints]
output_objects: [ProbabilitySetJustification, probability_quality, q_s, residual_edge, confidence_caps, missing_data]
gates_created: [no_invented_scenarios, no_invented_probabilities, missing_scenario_cap_0_45, infeasible_tilt_not_fabricated]
allowed_to_influence: [probability provenance/quality, q_s and residual_edge when inputs exist, ConfidenceComponents data half]
not_allowed_to_influence: [trade construction, legs, sizing, portfolio optimization, propose_scenarios]
failure_modes: [inventing scenarios, inventing p_s, fabricating an infeasible tilt, creating a parallel confidence number]
tests: [test_no_scenarios_caps_confidence, test_p_s_without_evidence_is_pm_assumption]
---

# Scenario Pricing Engine

> **Compiled from** the engine's own max-entropy math (`engine/engine2.py`,
> `engine/probability.py`) + Cover–Thomas KL concepts. `propose_scenarios` remains
> **NOT IMPLEMENTED** — this skill never invents scenarios or probabilities. METHOD card, no trades.

## Purpose
Evaluate **supplied** scenarios, market-implied pricing, probability provenance, and residual
edge. In discovery mode, only the light priced-in / probability-quality checks run — never
detailed pricing.

## Reference formulas (the engine computes these; the skill describes them)
- `X_FV = Σ p_s · X_s`  (scenario fair value).
- `q = argmin KL(q‖prior)  s.t.  Σ q_s · X_s = X_mkt`  (exponential tilt; feasible **only** if
  `X_mkt` is interior to the scenario span — **INFEASIBLE otherwise; do not fabricate** a q).
- `edge = X_FV − X_mkt = Σ (p_s − q_s) · X_s`.
- `q` is **risk-neutral** → `edge` is **gross of risk premium** unless a pricing kernel is supplied.

## When to use
On a promoted theme that carries supplied scenarios; to attach probability provenance/quality and
(if `X_mkt` exists) a priced-in q and residual edge.

## Inputs
`ThemeObject`, axis, supplied `Scenario[]`, current market value (if available), supplied `p_s`
(if available), evidence refs, pricing constraints.

## Outputs
`ProbabilitySetJustification`, `probability_quality`, `q_s` (if inputs exist),
`residual_edge` (if inputs exist), confidence caps, `missing_data`.

## Validation rules
- Do not invent scenarios. Do not invent probabilities.
- If scenarios absent: emit "no scenarios supplied", cap confidence at **0.45** (missing_scenario_cap).
- If `p_s` supplied but not evidence-backed: label `PM_assumption` / `unknown`, cap accordingly.
- `posterior = prior` in this PR (labeling only — derivation is a later PR).
- `evidence_weighted` requires ≥1 evidence ref.
- Confidence routes into the existing `ConfidenceComponents` (data half), **not** a parallel number.

## Failure / blocked states
- `X_mkt` outside the scenario span → tilt INFEASIBLE → report it; do not fabricate q/edge.
- No scenarios → `probability_justification = none`, `confidence_cap = 0.45`.

## Example (no scenarios supplied)
`probability_justification = none`; warning = "No scenario set supplied; no p_s invented.";
`confidence_cap = 0.45` (missing_scenario_cap).

## Example (p_s supplied, no evidence)
`posterior_p = prior_p`; source = `PM_assumption`; `probability_quality = low`;
warning = "Probabilities supplied but not evidence-justified."

## Non-goals
No trade construction, no legs, no sizing, no portfolio optimization, no scenario generation.
