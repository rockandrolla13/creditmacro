---
skill_name: macro-state-parser
access_class: method
compiled_from: [hamilton_2005_regime_switching_models.md, stock_watson_2002_principal_components.md, feds200542_giannone_reichlin_small_us.md, imf_wp1143_matheson_2011_global.md]
pipeline_phase: context_macro_state
provider_seam: [Provider.macro_context]
input_objects: [macro_series_panel, release_calendar, series_metadata, prior_state_estimate]
output_objects: [MacroState, regime_probability_vector, latent_factor_estimates, state_uncertainty, missing_data_flags, transition_risk_flag]
gates_created: [state_from_estimated_latent_not_narrative, regime_probabilities_sum_to_one, jagged_edge_handled_not_dropped, report_state_uncertainty]
allowed_to_influence: [latent macro state, regime-probability vector, extracted factors, state uncertainty, driver/regime context fed downstream, ConfidenceComponents data half]
not_allowed_to_influence: [macro point forecasts, GDP/policy predictions, pricing numbers that would change golden master, sizing, trades, execution]
failure_modes: [forcing a deterministic regime label instead of a probability vector, dropping series with publication lags, over-fitting the factor count, ignoring estimation uncertainty, treating one regime as permanent]
tests: [test_macro_state_regime_vector, test_macro_state_factors_from_panel, test_macro_state_jagged_edge, test_macro_seam_pending_method_context]
---

# Macro State Parser

> **Compiled from** Hamilton, *Regime-Switching Models* (`hamilton_2005_regime_switching_models.md`,
> §§ on the Markov-switching setup, the Hamilton-filter inference iteration, smoothing, and the
> N-regime generalization); Stock & Watson, *Forecasting Using Principal Components* (`stock_watson_2002_principal_components.md`,
> §1 intro, §2 approximate-factor model + principal-components estimation, §6 discussion);
> Giannone, Reichlin & Small, *Nowcasting GDP and Inflation* (`feds200542_giannone_reichlin_small_us.md`,
> §2 the real-time projection problem, §3 dynamic-factor + Kalman-filter methodology, news/uncertainty
> decomposition); Matheson, *New Indicators for Tracking Growth in Real Time* (`imf_wp1143_matheson_2011_global.md`,
> §II DFM + two-step estimation, §IV factor-count selection, §V the jagged-edge real-time problem).
> **METHOD only** — the engine extracts a state, never a forecast or a market view. **Seam status:
> pending** — until a macro-context seam is wired, this card is available as method context for any
> discovery seam.

## Purpose
Turn many conflicting, asynchronous, differently-dated macro series into a single latent macro
**STATE**: either a regime-probability vector (which unobserved phase is the economy most likely in)
and/or a small set of extracted latent factors (the common signal under hundreds of indicators).
The state is CONTEXT — a driver/regime input — not a prediction of any number.

## When to use
When a theme depends on "what macro phase are we in" or "what is the common signal under all this
noisy data", and the raw inputs are a large, collinear, lag-staggered panel rather than one clean
series. Use it to compress the panel before any downstream reasoning consumes a driver.

## Process primitives (paraphrased)
- **State, not switch.** A break in a series is better modeled as an unobserved discrete state `s_t`
  that follows a Markov chain with transition probabilities `p_ij`, than as a hand-dated, deterministic
  intercept change. You never observe `s_t`; you infer a probability over it from the observed data
  (Hamilton). Permanence is the special case `p_ii = 1`; usually allow `p_ii < 1` so a regime can
  revert.
- **Filtered probability vector.** Run the forward inference iteration: at each date combine the prior
  state probabilities, the transition matrix, and the per-regime densities of the new observation to
  produce a posterior probability over regimes that **sums to one**. Optionally smooth (use the full
  sample) to refine the historical state estimate. Generalize to an N-regime, vector-observation form;
  keep N small (2-3) unless the regimes are tightly parameterized.
- **Latent factors from a wide panel.** When the input is hundreds of predictors, model them as an
  approximate factor structure (each series = factor loadings × a few common factors + an idiosyncratic
  part) and estimate the factors by **principal components**. With both the cross-section and the time
  dimension large, the first few components consistently recover the common signal even when the
  idiosyncratic errors are serially and weakly cross-sectionally correlated (Stock & Watson). Most of
  the signal lives in the first two or three factors.
- **Real-time / jagged-edge handling.** Releases arrive on a staggered calendar, so the panel is
  unbalanced at the end (some series end this month, some last month). Do **not** discard the late or
  the early series. Cast the factor model in state-space form and run the Kalman filter; impose the
  missing-value restriction so the filter puts **zero weight** on a not-yet-released series when forming
  the factor at that date (Giannone-Reichlin-Small; Matheson). The two-step recipe: principal components
  + OLS for a first parameter pass, then re-estimate with the Kalman filter.
- **Track the update, not a forecast.** As each release block arrives, the state estimate updates and its
  uncertainty shrinks. Decompose the change into the part from new information ("news") and report the
  residual uncertainty (common-factor uncertainty vs idiosyncratic). The product is a current-state
  reading with an error band, not a path projection.
- **Choose the factor count deliberately.** Pick the number of factors with an information criterion or a
  variance-explained rule; too many factors degrades the state estimate (over-fitting). Prefer the
  parsimonious count that captures the bulk of the comovement.

## Inputs
A panel of macro series (`macro_series_panel`), a release calendar / publication-lag metadata
(`release_calendar`, `series_metadata`) so the jagged edge is known, and optionally a prior state
estimate (`prior_state_estimate`) to seed the filter.

## Outputs
`MacroState`, a `regime_probability_vector` (sums to one), `latent_factor_estimates` (the first few
common factors), `state_uncertainty` (common + idiosyncratic), `missing_data_flags`, and a
`transition_risk_flag`. Confidence routes into the existing `ConfidenceComponents` (data half).

## Required fields
- `regime_probability_vector` OR `latent_factor_estimates` (at least one must be populated).
- `state_uncertainty` for whichever state representation is emitted.
- `missing_data_flags` listing series that were lagged/unobserved at the as-of date.
- `as_of_date` and the `release_vintage` the state was computed on.

## Validation rules
- The state must come from an **estimated latent object** (filtered probabilities or extracted factors),
  never from a narrative label asserted by hand.
- A `regime_probability_vector` MUST sum to one and have non-negative entries.
- Late/early-released series are handled via the missing-value restriction (zero filter weight), **not**
  dropped — the jagged edge is preserved.
- The number of factors must be selected by a stated criterion; do not silently maximize it.
- Always emit `state_uncertainty`; a point state with no error band is invalid.
- Do not assert one regime is permanent — set `transition_risk_flag` when `p_ii < 1` is plausible.
- If the panel is too thin/short to identify factors or regimes, say so and cap confidence.

## Failure / blocked states
- Panel too short or too narrow to identify the latent structure → emit `state = indeterminate`,
  low confidence, `missing_data: insufficient_panel`.
- Regime likelihood-ratio is unidentified (testing N vs N+1 regimes is non-standard) → report the state
  but do **not** claim a tested regime count; flag `regime_count_unverified`.
- All series at the as-of date are stale (nothing released) → no update; carry prior state forward and
  flag `no_new_information`.
- Factor count unstable across vintages → flag `specification_unstable`, widen the uncertainty band.

## Example input
A ~150-series monthly panel (activity surveys, hard activity, trade, financial conditions, employment,
prices), with industrial production released for last month, surveys for the current month, and GDP only
for the prior quarter; as-of a mid-month release vintage.

## Example output
`regime_probability_vector = {expansion: 0.62, slowdown: 0.31, contraction: 0.07}` (sums to 1);
`latent_factor_estimates = [f1, f2]` with f1 the broad activity signal; `state_uncertainty = {common:
moderate, idiosyncratic: low}`; `missing_data_flags = [GDP_current_quarter, some_hard_activity]`;
`transition_risk_flag = true` (expansion→slowdown probability rising). No GDP number, no path forecast.

## Non-goals
No macro point forecasts, no GDP/inflation/policy predictions, no path projections. No pricing numbers
(nothing that could change a golden master), no sizing, no trades, no legs, no execution. The card emits
a state and its uncertainty, and stops.
