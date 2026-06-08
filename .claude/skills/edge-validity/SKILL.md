---
skill_name: edge-validity
access_class: method
pipeline_phase: discovery_edge_validity
provider_seam: ["READABLE in discovery as method context (define_axis / diagnose_loops); informs the edge_survival cap qualitatively; NOT auto-wired; must not alter the cap math"]
input_objects: [candidate_signal, in_sample_stats, out_of_sample_status, robustness_checks, crowding_evidence]
output_objects: [validity_checklist, overfit_flags, oos_status, robustness_verdict]
gates_created: [require_out_of_sample, flag_overfitting_and_data_snooping, momentum_may_be_crowding]
allowed_to_influence: [qualitative edge-validity checklist, overfit/crowding flags feeding edge_survival reasoning]
not_allowed_to_influence: [the edge_survival cap math, pricing, sizing, confidence numbers, golden-master output]
failure_modes: [accepting an in-sample-only signal, data-snooping, mistaking a regime artifact for skill, ignoring transaction cost, survivorship]
tests: [test_edge_validity_card_exists, test_edge_validity_flags_momentum_crowding]
---

# Edge Validity

> **Compiled from** *Finding Alphas* (Igor Tulchinsky / WorldQuant). METHOD card: the PROCESS
> that **informs** the `edge_survival` confidence cap. Outputs a checklist primitive; **does NOT
> alter the cap math** and is not auto-wired. No case conclusions, no trades.

## Purpose
Stress-test a candidate signal/edge for **validity** — is it a true signal or overfit noise? —
producing a checklist and overfit/crowding flags (not a number).

## Process primitives (paraphrased)
- A signal's quality shows in its **information ratio** (return/volatility — strength *and*
  steadiness); a good **in-sample Sharpe** is necessary but not sufficient.
- "Until an alpha is extensively tested, put into production, and **observed out of sample**, it's
  hard to know how good it is." Require OOS evidence before trusting it.
- **Estimation error, overfitting, incomplete information, and regime shifts can make a
  relationship vanish.** Distinguish relationships that are *valid and deserve capital* from ones
  that are *bogus*.
- Guard against **data-snooping** (searching until something fits) and parameter over-tuning.
- Account for **turnover / transaction cost** — paper edge ≠ net edge.
- Robustness: stable across datasets, sub-periods, parameters; not a single lucky window.

## When to use
On a promoted theme's edge claim, in discovery — to qualitatively gauge edge survival (a crowded
momentum run is a prime overfit/crowding suspect).

## Inputs
Candidate signal, in-sample stats, OOS status, robustness checks, crowding evidence.

## Outputs
`validity_checklist`, `overfit_flags`, `oos_status` (none / partial / confirmed),
`robustness_verdict`.

## Validation rules
- Require out-of-sample evidence before treating an edge as real.
- Flag overfitting / data-snooping explicitly.
- A strong recent run with no mechanism is a **crowding / momentum** suspect, not confirmed alpha.
- Net of cost — flag high-turnover signals.
- Qualitative only — never set or alter the `edge_survival` cap number.

## Failure / blocked states
- In-sample only, no OOS → `oos_status = none`, validity unconfirmed → caps confidence (engine math unchanged).
- Edge is a single lucky window / survivorship artifact → `overfit_flags` set.

## Example
A high-flying cohort returning far above its index with rising index weight and no mechanism →
`overfit_flags: [momentum/crowding]`, `oos_status: none`, `robustness_verdict: unconfirmed` —
treat as crowding risk, not a validated edge.

## Non-goals
No alteration of the edge_survival cap math, no pricing, no sizing, no trades.

## Additional rules from Pardo & Carver (backtest robustness)
(Method/validation context only — introduces NO sizing, position, or trade numbers. Pardo:
Walk-Forward Analysis & Degrees-of-Freedom chapters; Carver: "Fitting" and "Speed of trading".)
- **Walk-forward analysis (Pardo).** Optimize on one window, test on the *next, unseen* window,
  then roll forward. Trust an edge only if it survives out-of-sample windows it was never fitted
  on. Track **walk-forward efficiency** (out-of-sample vs in-sample performance ratio); a large
  drop-off is the signature of overfitting.
- **Degrees of freedom (Pardo).** More tunable parameters / fewer observations per parameter = less
  reliable fit. Optimization done correctly is fine; optimization that fits noise is overfitting —
  require enough independent observations per parameter before trusting the result.
- **In-sample fitting trap (Carver).** Any choice made with hindsight (picking the winning rule or
  instrument after seeing the whole sample) inflates the backtest; the honest estimate blends the
  alternatives you could not have known to drop. Hedging across rules is more robust than betting
  on the single best one.
- **Narrative fallacy (Carver).** We see patterns in noisy price history that were not there and are
  drawn to over-fitted rules; prefer simpler, fewer-parameter rules that generalize.
- **Cost-aware / speed limit (Carver).** Judge edges *net of trading costs*, not gross, and on a
  risk-adjusted (volatility-normalized) basis. High turnover imposes a cost hurdle the signal must
  clear; a fast signal that does not clear it is not a real edge.
- **Robustness verdict.** Confirmed only if stable across sub-periods, parameters, and instruments,
  net of cost, with positive out-of-sample evidence — otherwise `robustness_verdict: unconfirmed`.
  Qualitative only — never sets or alters the `edge_survival` cap number.
