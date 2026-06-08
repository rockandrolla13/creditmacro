---
skill_name: priced-in-estimator
access_class: method
pipeline_phase: discovery_priced_in_reasoning
provider_seam: ["READABLE in discovery as method context (define_axis / justify_probabilities); NOT auto-wired; must not change golden output"]
input_objects: [axis, current_market_level, valuation_history, carry, regime]
output_objects: [priced_in_decomposition, what_is_discounted, residual_premium_estimate, valuation_state]
gates_created: [separate_valuation_from_premium, do_not_credit_getting_expensive]
allowed_to_influence: [qualitative reasoning about what is already discounted, residual-premium framing]
not_allowed_to_influence: [pricing math, q-tilt, residual_edge numbers, sizing, golden-master output]
failure_modes: [confusing a cheapening/expensive move with the premium, ignoring carry, extrapolating valuation, double-counting a discounted risk]
tests: [test_priced_in_card_exists, test_priced_in_articulates_decomposition]
---

# Priced-In Estimator

> **Compiled from** *Investing Amid Low Expected Returns* (Antti Ilmanen) — building blocks of
> long-run returns. METHOD card: the PROCESS for the back-half question *q* ("what is priced
> in"). Paraphrase only; **readable in discovery but not auto-wired** and must not change any
> golden-master numerical output. No case conclusions, no trades.

## Purpose
Reason about **what is already discounted** in a spread/price by decomposing expected return
into its building blocks, and separating the *valuation level* from the *risk premium*.

## Process primitives (paraphrased)
Decompose long-run expected return into building blocks:
- **Risk premia** — term/duration, **credit**, equity (compensation for "bad returns in bad times").
- **Valuation level** — how rich/cheap the asset is vs history (a *level*, not a premium). A move
  that comes from *getting more expensive* is **not** repeatable expected return — do not credit
  it (nor blame a cheapening). This is the core "what's priced in" adjustment.
- **Carry / income** — the return earned if nothing changes.
- **Illiquidity premium** and **style premia** (value, momentum, carry, defensive/quality).
Reason: market level = discounted base case + premium; the *residual premium* is what remains
after stripping the carry and the valuation level. Cheap valuation = more premium latent; rich
valuation = much already discounted.

## When to use
On a promoted axis with a current market level, in discovery — to articulate what the spread
already discounts before any edge claim.

## Inputs
Axis, current market level, valuation history, carry, regime.

## Outputs
`priced_in_decomposition` (premium / valuation / carry), `what_is_discounted`,
`residual_premium_estimate` (qualitative), `valuation_state` (rich / neutral / cheap).

## Validation rules
- Separate the **valuation level** from the **risk premium** — never count "getting expensive" as edge.
- Account for **carry** explicitly.
- Do not extrapolate the recent valuation change as expected return.
- Qualitative only — never emit q-tilt or residual_edge numbers (the engine owns that math).

## Failure / blocked states
- No valuation history → can state the building blocks but not the valuation state; flag the gap.
- The "edge" is entirely a recent cheapening/richening → flag it as not a repeatable premium.

## Example
For a project-bond spread: decomposition = credit risk premium + illiquidity premium + carry,
on top of a valuation level. If the spread is historically tight (rich), much of the good news is
**already discounted** → residual premium is small; if wide (cheap), more premium is latent.

## Non-goals
No pricing math, no q-tilt, no residual-edge numbers, no sizing, no trades.
