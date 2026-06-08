---
skill_name: trap-detector
access_class: method
pipeline_phase: discovery_loop_diagnosis
provider_seam: [LLMProvider.diagnose_loops, Provider.diagnose_loops, assess_trap_implications, critique_mental_model]
input_objects: [SystemMap, CausalChain, operational_axes, evidence, strategy_family_candidates]
output_objects: [LoopDiagnosis, dominant_loop_now, possible_loop_shift, system_traps, early_warning_indicators, expression_risk_implications, invalidation_evidence, decision]
gates_created: [name_the_balancing_limit, crowding_requires_evidence, qualitative_only_no_ode]
allowed_to_influence: [loop dominance, trap flags, reversal conditions, early-warning indicators, invalidation evidence, decision]
not_allowed_to_influence: [pricing, sizing, exact shorts/longs, hedge ratios, execution, scenario probabilities]
failure_modes: [trap-as-trade, ignoring delays/overshoot, asserting crowding without evidence, no named limit on an R loop, extrapolating a hot streak (regression to the mean), survivorship/selection bias, false linearity, texas-sharpshooter false patterns]
tests: [test_trap_flags_success_to_successful_crowding, test_trap_qualitative_no_pricing, test_trap_card_has_ellenberg_supplement]
---

# Trap Detector

> **Compiled from** *Thinking in Systems* (Meadows): system archetypes/traps, loop dominance,
> leverage points; **supplemented from** *How Not to Be Wrong* (Ellenberg): statistical traps
> (see the supplement section). METHOD card: no case conclusions, no trades.

## Purpose
Diagnose **system traps, loop dominance, crowding, reversals, and failure modes** —
qualitatively. Output the dominant loop, the reversal condition, and early-warning indicators.

## Process primitives (paraphrased archetypes)
Common trap structures ("archetypes") that produce problematic behaviour from *structure*, not
actors:
- **Policy resistance / fixes-that-fail** — subsystems pull a stock to different goals; nothing
  moves despite effort.
- **Drift to low performance / eroding goals** — the goal slides toward actual performance.
- **Escalation** — each side reinforces the other (an R loop between competitors).
- **Success-to-the-successful** — winners get the means to win more (the crowding/momentum trap).
- **Tragedy of the commons** — shared resource over-used because cost is externalised.
- **Shifting the burden / addiction** — a quick fix atrophies the system's own capacity.
Two laws to apply: **a reinforcing loop always eventually meets a balancing loop — name the
limit**; and **delays in balancing loops cause overshoot — flag them**. Loop *dominance* can shift
over time (R dominant now → B dominant later = the reversal).

## When to use
After the system map, in Phase A — before any strategy-family promotion.

## Inputs
`SystemMap`, causal chain, operational axes, evidence, strategy-family candidates.

## Outputs
`LoopDiagnosis`, `dominant_loop_now`, `possible_loop_shift`, `system_traps`,
`early_warning_indicators`, `expression_risk_implications`, `invalidation_evidence`,
`decision` (promote / watchlist / research_more / challenge_model).

## Trap patterns to detect
momentum/crowding · success-to-the-successful · limits-to-growth · shifting dominance ·
liquidity trap · policy resistance · delayed feedback · wrong-goal optimisation ·
crowded trade / limits to arbitrage.

## Validation rules
- Qualitative only, no ODE simulation.
- If crowding is suspected, list the evidence required to confirm it.
- Do not turn a trap diagnosis into a trade.
- A reinforcing loop always eventually meets a balancing loop — name the limit.
- Delays in balancing loops cause overshoot — flag this explicitly.

## Failure / blocked states
- Crowding asserted with no confirming evidence → `decision = watchlist` + list evidence needed.
- R loop with no named limit → incomplete diagnosis; add the balancing limit before promoting.

## Example output (compute-credit illustration)
- Dominant loop: performance → inflows/attention → tightening → more performance (R).
- Trap: success-to-the-successful / crowding.
- Early warnings: issuance rising while spreads stop tightening; flow reversal; secondary
  liquidity deteriorating; new-issue concessions widening; index weight rising while excess
  return fades.
- possible_loop_shift: flows turn → B loop dominates → reversal.
- Decision: watchlist / challenge_model until evidence confirms.

## Statistical traps (supplement — compiled from *How Not to Be Wrong*, Ellenberg)
Beyond the system archetypes, screen for the statistical errors that masquerade as signal:
- **Regression to the mean** — an extreme reading (a hot streak / record outperformance) tends to
  revert. Do not extrapolate the recent best performers; the "success" may be luck about to mean-revert.
- **Survivorship / selection bias** — you only see the survivors (the planes that returned, the
  funds still open). Returns measured on survivors overstate the truth; ask "what's missing from
  the sample?" (Wald's armour, dead funds).
- **Linearity vs nonlinearity** — beware *false linearity* ("more is always better"). Many
  relationships are curved with an optimum in the middle: **which way you should go depends on
  where you already are**. A directional call that ignores the curvature is a trap.
- **False patterns (Texas sharpshooter / multiple comparisons)** — pattern found after the fact, or
  after many tries, is often noise; require a pre-stated mechanism.
- **Expected-value reasoning** — weigh outcomes by probability and magnitude, not by vividness.

## Non-goals
No exact shorts/longs, no hedge ratios, no sizing, no execution.

## Additional rules from w8282.md
(Chan–Karceski–Lakonishok, growth-rate persistence; method only, no trades.)
- **Past growth does not persist.** Across the cross-section there is essentially no persistence in
  earnings / bottom-line profit growth beyond what chance predicts; only sales growth shows mild
  persistence. Competitive pressure dissipates abnormal profitability, so growth **mean-reverts**
  to a normal rate.
- **Extrapolation-of-past-trend trap.** Analysts and investors over-extrapolate a streak of strong
  past growth and put too little weight on the base case (base-rate neglect). Rich valuations bake
  in sustained-growth assumptions that history rarely delivers — flag any thesis that leans on "it
  grew fast, so it will keep growing fast."
- **False-persistence trap.** A multi-year run of above-median growth predicts future runs no
  better than a coin-flip; do not treat a track record as a causal driver. Demand a mechanism, not
  a streak (mirrors the "require a pre-stated mechanism" rule in the statistical-traps supplement).
- **Base-rate / mean-reversion check.** Anchor on the unconditional distribution — median growth is
  modest (GDP-like) and very high sustained growth sits in the far tail (rare) — before crediting
  any extrapolated high-growth path.
- **Survivorship caveat** (reinforces the existing supplement): persistence and growth stats
  measured only on survivors overstate the truth; non-survivors are missing from the sample.
