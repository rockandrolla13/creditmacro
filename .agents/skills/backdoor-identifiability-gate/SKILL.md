---
skill_name: backdoor-identifiability-gate
access_class: method
compiled_from: ["Causal Inference What If (Miguel A. Hernán, James M. Robins) (z-library.sk, 1lib.sk, z-lib.sk).md", "Mostly Harmless Econometrics An Empiricists Companion (Joshua D. Angrist, Jorn-Steffen Pischke) (z-library.sk, 1lib.sk, z-lib.sk).md", "Explanation in Causal Inference Methods for Mediation and Interaction (Tyler VanderWeele) (z-library.sk, 1lib.sk, z-lib.sk).md", "The Book of Why (Judea Pearl) (z-library.sk, 1lib.sk, z-lib.sk).md"]
pipeline_phase: discovery_causal_identification
provider_seam: [Provider.expand_causal]
input_objects: [CausalChain, driver, mediators, outcome_variable, confounders, causal_dag, method_context]
output_objects: [IdentifiabilityVerdict, estimand, adjustment_set_or_instrument, assumption_ledger, residual_backdoor_paths, identification_status, downgrade_reason]
gates_created: [association_is_not_causation, unidentified_effect_blocks_pricing, no_adjustment_set_routes_to_watchlist, positivity_violation_blocks, mediator_outcome_confounder_blocks_decomposition]
allowed_to_influence: [identification_status, promotion-vs-watchlist routing of a causal effect, the named estimand and adjustment-set/instrument, assumption ledger, falsifier list]
not_allowed_to_influence: [pricing numbers that change golden master, sizing, trades, execution]
failure_modes: [treating association as a do-effect, omitting an unblocked backdoor path, conditioning on a collider or post-treatment mediator, ignoring positivity, asserting a weak/invalid instrument, naming no estimand, skipping the mediator-outcome confounding check]
tests: [test_backdoor_gate_blocks_associational_only, test_backdoor_gate_names_estimand_and_adjustment_set, test_backdoor_gate_positivity_violation_watchlist, test_backdoor_gate_collider_not_admissible, test_backdoor_gate_instrument_path_accepts]
---

# Backdoor Identifiability Gate

> **Compiled from** Hernán & Robins, *Causal Inference: What If* (identifiability conditions §3.1–3.4;
> backdoor criterion & confounding §7.1–7.6 — read; skipped the survival/time-varying-treatment,
> g-methods and measurement-error chapters 9–17) — Angrist & Pischke, *Mostly Harmless Econometrics*
> (IV/2SLS & LATE §4.1–4.5, the conditional-independence assumption & bad-control §3.2 — read;
> skipped the panel/standard-error and quantile chapters) — VanderWeele, *Explanation in Causal
> Inference* (the four mediation confounding assumptions §2.3 and sensitivity analysis ch.3 — read;
> skipped the survival, multiple-mediator and interaction-decomposition chapters) — Pearl & Mackenzie,
> *The Book of Why* (the ladder, the do-operator, the back-door / front-door criteria and do-calculus
> ch.1, 4, 7 — read; skipped the historical and AI-ethics chapters). METHOD card: no case
> conclusions, no trades, no numbers that move pricing.

## Purpose
A **gate** that decides whether the causal effect a theme depends on is *identifiable* BEFORE it may
be priced. The compiler hands over a `CausalChain` (driver → mediators → outcome). This gate refuses
to let an effect proceed to scenario pricing unless three things are stated and survive review:
1. a **named estimand** — the specific interventional/counterfactual contrast (e.g. the average effect
   of *doing* the driver, `E[Y | do(driver=high)] − E[Y | do(driver=low)]`), not a regression slope;
2. an **adjustment (backdoor) set OR an instrument** that licenses estimating that estimand from
   observational data;
3. an **assumption ledger** (exchangeability, positivity, consistency, no unblocked backdoor) with each
   assumption marked plausible / heroic / violated.

If only an association can be defended, the effect is **blocked or downgraded to watchlist** — it never
reaches pricing. This is the construction-level version of "correlation is not causation."

## When to use
Immediately after the Causal Compiler emits a `CausalChain`, on any promoted `CoreThemeCandidate`, in
Phase A fresh reasoning, and before Engine 2 (scenario pricing) is allowed to touch the effect.

## Process primitives
- **Walk the ladder (Pearl).** Association (X moves with Y) sits on rung 1; intervention (`do(X)`) on
  rung 2; counterfactual on rung 3. Pricing needs at least a rung-2 (do-) effect. The `do`-operator
  erases the arrows *into* the driver; confounding is exactly what makes `P(Y | do(X))` differ from
  `P(Y | X)`. The gate's job is to certify that, given the stated graph, the do-effect is recoverable
  from observed data.
- **Name the estimand first (Hernán-Robins, Imbens-Rubin spirit).** State the counterfactual contrast
  precisely — which intervention, on whom, against what alternative — before asking whether data can
  estimate it. Identification = "do the stated assumptions pin the observed-data distribution to a
  *single* value of the effect?" If several effect values are compatible with the data, the effect is
  **non-identified**.
- **Run the backdoor criterion (Pearl; Hernán-Robins §7.3).** A backdoor path is any path from driver to
  outcome that begins with an arrow *into* the driver; such paths carry spurious (non-causal) flow. A
  candidate adjustment set **Z** is admissible iff (a) Z blocks every backdoor path, and (b) no member
  of Z is a descendant of the driver on a causal path (do not adjust away the very channel you want).
  Blocking rules: condition on a chain or fork middle to close it; do **not** condition on a collider
  (that *opens* a previously blocked path — collider/M-bias / selection bias). "Control for everything
  measured" is wrong: it can open colliders.
- **Check the three identifiability conditions (Hernán-Robins §3).**
  - **Exchangeability** (conditional ignorability): within levels of Z the driver is as-good-as
    randomly assigned — all *other* outcome predictors are balanced across driver levels. Unverifiable
    from data; rests on expert knowledge. Unmeasured common causes break it.
  - **Positivity**: every driver level under contrast has positive probability within every Z-stratum
    that occurs. If some regime/state always (or never) sees the driver move, the effect there is not
    estimable. Positivity is partly checkable in data.
  - **Consistency**: the driver is a well-defined intervention with versions that match the data, and
    observed outcomes equal counterfactuals under the realised driver value. A vague "driver" (no
    well-specified intervention) fails this.
- **Instrument fallback (Angrist-Pischke §4).** When no admissible backdoor set exists (unmeasured
  confounding), look for an **instrument**: a variable that (i) shifts the driver (relevance / strong
  first stage), (ii) affects the outcome *only through* the driver (exclusion), and (iii) is
  as-good-as-randomly assigned given covariates (independence). A valid instrument identifies a LATE
  (effect on the compliers) — record *whose* effect it is. Weak instruments and exclusion violations
  are blocking failures; flag "bad controls" (post-treatment conditioning) as inadmissible.
- **Mediation guard (VanderWeele §2.3).** If the chain decomposes a total effect into direct/indirect
  parts through a mediator, identifying those parts needs MORE than randomising the driver: no
  unmeasured treatment-outcome, mediator-outcome, or treatment-mediator confounding, and **no
  mediator-outcome confounder that is itself affected by the driver**. A mediator-outcome confounder
  on the path is a hard blocker for any direct/indirect split — downgrade the decomposition, not just
  the total effect.
- **Sensitivity, not silence (VanderWeele ch.3; Hernán-Robins Fine Point 7.1).** When an assumption is
  "heroic", record how strong an unmeasured confounder would have to be to overturn the sign/conclusion,
  and the *direction* of the likely bias (signed-graph reasoning). A fragile effect is downgraded, not
  asserted.

## Inputs
A `CausalChain` (driver, mediators, outcome), the proposed `causal_dag`, the candidate confounder list,
and method memory. No case pages, no historical themes.

## Outputs
`IdentifiabilityVerdict` carrying: the named `estimand`; the chosen `adjustment_set_or_instrument`; an
`assumption_ledger` (each of exchangeability / positivity / consistency / no-unblocked-backdoor marked
plausible | heroic | violated); any `residual_backdoor_paths` left open; an `identification_status`
in `{identified, identified_via_instrument, conditionally_identified, non_identified}`; and a
`downgrade_reason` when blocked.

## Required fields
A named estimand (interventional/counterfactual contrast); an admissible adjustment set OR a stated
instrument with its three conditions; the assumption ledger with all four entries filled; an explicit
list of residual open backdoor paths (or "none"); ≥1 falsifier tied to an assumption (an observable +
threshold that, if seen, would void identification).

## Validation rules
- A purely associational claim (no defensible `do`-effect) → `non_identified` → **blocked from pricing**
  (`association_is_not_causation`).
- No admissible backdoor set and no valid instrument → `non_identified` → **watchlist**, never priced
  (`unidentified_effect_blocks_pricing`).
- The adjustment set must block every backdoor path and contain no descendant of the driver; a set that
  conditions on a collider or a post-treatment mediator is rejected (re-derive Z).
- Positivity must hold for the driver levels under contrast within every occurring stratum; a stratum
  with zero driver variation cannot carry the effect → restrict scope or downgrade.
- For any direct/indirect (mediation) claim, all four VanderWeele assumptions must be addressed; a
  driver-affected mediator-outcome confounder blocks the decomposition.
- An instrument asserted without relevance + exclusion + independence (or only weakly relevant) is not
  an identification — treat as `non_identified`.

## Failure / blocked states
- Only association, no interventional contrast → `blocked: association_only`.
- Open backdoor path with no measurable blocker and no instrument → `blocked: unidentified` → watchlist.
- Positivity violated in the regime that matters → `conditionally_identified` (scope-restricted) or
  `watchlist`.
- Estimand un-nameable because the "driver" is not a well-defined intervention → `blocked: ill_posed_do`
  (consistency failure).
- Mediation split required but a driver-affected mediator-outcome confounder is present →
  `blocked: mediation_not_identified` (total effect may still pass).

## Example input
CausalChain: driver = "policy tariff step on intermediate-goods imports" → mediators = "input-cost
pass-through, supplier margin compression" → outcome = "credit quality of an exposed issuer cohort".
Proposed confounders: global demand cycle, sector beta, FX, commodity prices.

## Example output
- estimand: `E[issuer-cohort impairment | do(tariff=on)] − E[· | do(tariff=off)]`, cohort-average.
- adjustment_set: {global demand cycle, sector beta, FX, commodity prices}; checked admissible (blocks
  the demand-cycle backdoor; contains no post-tariff mediator).
- assumption_ledger: exchangeability = heroic (unobserved firm-level sourcing flexibility may remain);
  positivity = plausible (both tariff states observed across the cycle); consistency = plausible (tariff
  is a well-defined intervention); no-unblocked-backdoor = conditionally satisfied given the set.
- residual_backdoor_paths: one (firm sourcing flexibility) — unmeasured → sensitivity: a confounder
  moving impairment by >X and tariff-exposure by >Y would flip the sign.
- identification_status: `conditionally_identified`; falsifier: cohort impairment fully explained by
  demand-cycle + commodity controls (effect vanishes after adjustment) → identification void.
- Verdict: passes to pricing as *conditionally identified*, flagged heroic-exchangeability; the
  direct-vs-indirect (cost-channel vs margin-channel) split is **downgraded** — a driver-affected
  margin confounder blocks the mediation decomposition.

## Non-goals
No effect-size estimation, no scenario probabilities, no pricing numbers, no sizing, no trade
construction, no execution. The gate decides *whether* an effect may be priced — not *what* it is worth.
