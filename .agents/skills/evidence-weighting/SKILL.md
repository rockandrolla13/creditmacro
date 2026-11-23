---
skill_name: evidence-weighting
access_class: method
pipeline_phase: discovery_probability_provenance
provider_seam: ["PENDING — Q4 posterior derivation (probability.justify_probabilities); NOT wired this PR"]
input_objects: [prior_belief, base_rate, reference_class, evidence_items, likelihoods]
output_objects: [base_rate_anchor, likelihood_ratio, directional_posterior_move, base_rate_neglect_flags]
gates_created: [anchor_on_a_base_rate, nonzero_prior_heuristic, update_in_proportion_to_evidence_weight]
allowed_to_influence: [probability provenance/labeling, qualitative directional posterior move]
not_allowed_to_influence: [ConfidenceComponents, Q4 posterior in code (posterior==prior still), pricing, sizing, golden-master numbers]
failure_modes: [base-rate neglect, anchoring on a vivid story over the reference class, zero prior, over-updating on weak evidence, ignoring that base rates can change]
tests: [test_evidence_weighting_card_exists, test_evidence_weighting_states_prior_likelihood_posterior]
---

# Evidence Weighting

> **Compiled from** *Bayes and Base Rates* (Mauboussin & Callahan, Morgan Stanley Counterpoint
> Global, Feb 2026). METHOD card: the PROCESS basis for the **deferred** Q4 posterior≠prior
> derivation — specifies the update rule as a primitive; **does NOT wire into
> ConfidenceComponents or Q4** (separate PR). No case conclusions, no trades.

## Purpose
Specify how evidence should move a belief off a prior — base-rate anchoring + likelihood-ratio
updating — as a reusable process primitive for probability provenance.

## Process primitives (paraphrased)
- **Establish the prior from a base rate** — the outcome frequency for a relevant *reference
  class* (e.g. "what % of firms this size grew 10%/yr for 5 years"). Reference-class forecasting
  beats inside-view optimism.
- **Update in proportion to the weight of the evidence** (Tetlock's reading of Bayes' core
  insight) — superforecasters update gradually, not in one jump.
- **Posterior odds = prior odds × likelihood ratio.** The likelihood ratio is
  P(evidence | hypothesis) / P(evidence | not-hypothesis); LR>1 moves the posterior up, LR<1 down.
- **Use a non-zero prior heuristic** — Bayes breaks if the prior is exactly 0.
- **Base rates can change** — a structural shift in the reference class can justify moving off the
  historical base rate (state the mechanism).

## When to use
When attaching probability provenance to a theme; to state a prior, the evidence, and the
*direction* a posterior should move — **labeling only** in this PR.

## Inputs
Prior belief, base rate, reference class, evidence items, likelihoods.

## Outputs
`base_rate_anchor`, `likelihood_ratio` (qualitative), `directional_posterior_move`,
`base_rate_neglect_flags`.

## Required fields
A named reference class + its base rate; ≥1 evidence item with a direction (raises/lowers);
the resulting directional posterior move (up / down / unchanged) — never a fabricated number.

## Validation rules
- Always anchor on a base rate / reference class before reading the new evidence.
- Move the posterior **in proportion** to evidence weight — flag over-updating on thin evidence.
- Never use a zero prior.
- Posterior labeling only — in code, posterior == prior until the Q4 derivation PR.

## Failure / blocked states
- No reference class available → state the gap; do not invent a base rate.
- Evidence is anecdotal/vivid but not diagnostic → flag base-rate neglect; no posterior move.

## Example
- Prior: base rate of a firm this size sustaining the forecast growth is low (reference class).
- Evidence: large contracted backlog raises the likelihood (LR>1); financing/counterparty risk lowers it.
- Directional posterior move: **up modestly** from the low base rate — labeling only (code posterior==prior).

## Non-goals
No probability numbers wired into confidence, no Q4 derivation, no pricing, no trades.
