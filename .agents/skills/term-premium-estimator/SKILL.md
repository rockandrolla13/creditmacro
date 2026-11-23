---
skill_name: term-premium-estimator
access_class: method
compiled_from: [vayanos_vila_2021_preferred_habitat.md, brunner_meltzer_1976_aggregative_theory.md, 1-s2.0-S1042443102000458-main.md]
pipeline_phase: pricing_rates_term_premium
provider_seam: [Provider.define_axis, Provider.normal_fair_value]
input_objects: [bond_supply_demand_state, balance_sheet_shock, short_rate_process, curve_slope_observable, arbitrageur_risk_capacity]
output_objects: [TermPremiumReasoning, premium_shift_direction, premium_localization, premium_mean_reversion_note, expectations_hypothesis_flag, axis_candidate]
gates_created: [premium_not_level, supply_shock_via_duration_risk_mechanism, separate_stock_from_flow_channel, premium_is_gross_of_no_risk_assumption]
allowed_to_influence: [term-premium reasoning, sign/localization of a supply-driven premium shift, choice of a curve-slope operational axis, normal fair-value as a premium-aware primitive, ConfidenceComponents data half]
not_allowed_to_influence: [pricing numbers that would change golden master, sizing, trades, execution, specific bonds/curve points/hedge ratios]
failure_modes: [confusing a premium shift with a level/expectations move, treating bond supply as a clean instrument with no risk-bearing wedge, ignoring stock-vs-flow distinction, assuming the expectations hypothesis holds, treating the premium as constant]
tests: [test_term_premium_not_level, test_supply_shock_duration_mechanism, test_eh_rejection_premium_meanreverts, test_rates_seam_pending_method_context]
---

# Term Premium Estimator

> **Compiled from** Vayanos & Vila, *A Preferred-Habitat Model of the Term Structure* (`vayanos_vila_2021_preferred_habitat.md`,
> §1 intro + the demand-shock / duration-risk / premia-slope mechanisms, §2 model setup, one-factor vs
> multi-factor localization); Brunner & Meltzer, *An Aggregative Theory for a Closed Economy*
> (`brunner_meltzer_1976_aggregative_theory.md`, §1-2 the three-asset framework, finite-transaction-cost
> wedge, asset substitution across a spectrum rather than two assets); Bams & Wolff, *Risk Premia in the
> Term Structure: a Panel Data Approach* (`1-s2.0-S1042443102000458-main.md`, abstract + §1-3 separating
> the risk premium from unexpected excess return, EH rejection, premium mean-reversion). **METHOD only** —
> reason about how supply/demand and balance-sheet shocks move *premia*; never emit a priced level, a bond,
> or a hedge ratio. **Seam status: pending** — until a rates fair-value seam is wired, this card is method
> context for the axis-definition and normal-fair-value seams.

## Purpose
Reason about how bond **supply/demand and balance-sheet shocks** move the **term premium** — the
expected-excess-return component of yields — for risk-free and risky bonds. This is a pricing/rates
fair-value *primitive*: it explains the premium (the wedge over the expectations-hypothesis level), not
the level of rates per se, and it helps name a computable curve-slope axis.

## When to use
When a theme turns on bond supply, issuance, QE / central-bank balance sheet, a clientele demand shift,
or risk-bearing capacity — anything that should move the **premium** rather than the expected path of the
short rate. Use it to (a) define an operational curve-slope axis and (b) frame a normal fair value as a
premium-aware quantity.

## Process primitives (paraphrased)
- **Premium ≠ level, premium ≠ expectations.** Decompose a yield into the expectations-hypothesis part
  (average expected future short rates) and a **term premium** (compensation for bearing interest-rate
  risk). The empirical record rejects the pure expectations hypothesis: term premia are real, generally
  positive, and **time-varying** (Bams & Wolff). Reason about the premium component explicitly; do not
  attribute a supply move to changed rate expectations.
- **Supply/demand moves the premium through a risk-bearing wedge.** Maturity clienteles (preferred
  habitats) demand specific segments; risk-averse arbitrageurs absorb the residual via carry trades. A
  change in clientele demand or bond supply shifts arbitrageurs' aggregate exposure to the short rate
  ("duration risk"), and bond prices must move to compensate them — so the **premium shifts continuously**
  with supply, not as an on/off jump (Vayanos & Vila). Model the supply shock *mathematically* through the
  duration-risk channel, not as a clean observable instrument.
- **Premia relate to the slope; that suggests the axis.** Bond risk premia rise with the **slope of the
  term structure** (steep curve → higher expected excess return to arbitrageurs). This premia-slope link
  is the operational hook: a named curve slope/spread with a real historical series is a computable axis
  proxy for the premium.
- **Global vs localized effects.** With a single (short-rate) risk factor, a demand change has a **global**
  effect across maturities — its sign depends on how total duration risk changes, not on where the shock
  originates; the longest maturities react most. With multiple risk factors (e.g. stochastic demand),
  effects become **localized** to the maturities where the shock lands, and transmission can even reverse
  at the long end. State which regime you are assuming.
- **Stock vs flow channel (split the input).** A balance-sheet/monetary input acts through more than one
  channel. With finite transaction costs there is a wedge between the price of new output and the price of
  the existing capital/asset stock, so substitution runs across the **whole spectrum of assets**, not two
  (Brunner & Meltzer). Separate the **stock** effect (the outstanding aggregate of duration/asset risk to
  be held) from the **flow** effect (current issuance/purchases). Asset substitution when balance sheets
  turn is a stock-view mechanism — the same lens behind the duration-risk channel above.
- **The premium mean-reverts.** Disentangle the realized excess return into the (unobservable) risk premium
  and the unexpected excess return; the **premium itself shows mean reversion** (Bams & Wolff). So a
  premium that is currently rich/cheap relative to its own history carries a reversion prior — a method
  note, not a trade.

## Inputs
`bond_supply_demand_state` (issuance / clientele / QE posture), `balance_sheet_shock` (the input to split
into stock vs flow), `short_rate_process` (mean-reverting driver), `curve_slope_observable` (a real
spread/slope series), `arbitrageur_risk_capacity` (risk aversion / risk-bearing).

## Outputs
`TermPremiumReasoning`, `premium_shift_direction` (sign + global-vs-localized), `premium_localization`
(which maturities), `premium_mean_reversion_note`, an `expectations_hypothesis_flag` (EH rejected →
premium is live), and an `axis_candidate` (a named, computable curve-slope/spread series). Confidence
routes into the existing `ConfidenceComponents` (data half).

## Required fields
- `premium_shift_direction` with whether the assumed factor structure is one-factor (global) or
  multi-factor (localized).
- The **mechanism** linking the supply/balance-sheet shock to the premium via duration risk (no bare
  correlation).
- A `stock_vs_flow` split of any balance-sheet input.
- `axis_candidate` naming an observable curve slope/spread with a real historical series.

## Validation rules
- Output must concern the **premium**, not the rate level or the expected short-rate path; reject a "level"
  answer.
- A supply/QE/issuance shock must move the premium **through the duration-risk / risk-bearing mechanism** —
  no clean-instrument or pure-expectations story.
- Any balance-sheet input must be **split into stock vs flow** channels before reasoning about the premium.
- The premium is **time-varying and mean-reverting**; do not treat it as constant, and set
  `expectations_hypothesis_flag = rejected` as the working prior.
- Localization (global vs maturity-specific) must state the assumed number of risk factors.
- The `axis_candidate` must be a computable series (a real spread/slope), not a narrative.
- This card produces **no priced number** — nothing it emits may change a golden master.

## Failure / blocked states
- The shock is really an expectations move (changed expected short-rate path) → return
  `not_a_premium_shock`; defer to the rate-path/driver side, do not fabricate a premium shift.
- Factor structure unstated → cannot determine global vs localized → flag `localization_undetermined`.
- No observable curve slope/spread available → no `axis_candidate`; report `axis_unavailable` and cap
  confidence (axis must be operational).
- Asked for a priced fair value, bond, curve point, or hedge ratio → refuse; out of scope (downstream,
  golden-master-protected).

## Example input
A theme: a large-scale central-bank bond-purchase program concentrated at long maturities, against a
mean-reverting short rate and an observable 2s30s slope; arbitrageur risk capacity assumed binding.

## Example output
`premium_shift_direction = compression, global-leaning under a one-factor read (largest effect at the long
end)`; `premium_localization = concentrated at long maturities if demand is treated as a second factor`;
`stock_vs_flow = the outstanding stock of duration risk removed drives the premium (stock), the purchase
pace is the flow`; `expectations_hypothesis_flag = rejected`; `premium_mean_reversion_note = current
premium rich vs own history → reversion prior`; `axis_candidate = a named long-end curve slope series`.
No basis-point fair value, no bond, no hedge ratio.

## Non-goals
No priced fair-value numbers, no specific bonds, no curve points, no hedge ratios, no DV01s. Nothing that
would change a golden master. No sizing, no legs, no stops, no execution. The card reasons about premium
mechanics and names an axis, then stops.
