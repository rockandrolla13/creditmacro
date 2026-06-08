---
skill_name: outcome-calibration-engine
access_class: method
compiled_from: ["Gneiting2007jasa.md", "1910.07325v1.md"]
pipeline_phase: q4_probability_calibration
provider_seam: [Provider.justify_probabilities]
input_objects: [scenario_probabilities, scenario_outcomes, realized_outcome, reference_forecast, competing_forecast_set]
output_objects: [proper_score, calibration_assessment, sharpness_assessment, skill_score, dm_comparison, probability_justification]
gates_created: [use_strictly_proper_score, sharpness_subject_to_calibration, require_reference_for_skill, multivariate_needs_dependency_aware_score]
allowed_to_influence: [qualitative justification/evaluation of supplied probabilities, calibration + sharpness verdict, relative ranking of competing forecasts]
not_allowed_to_influence: [the supplied scenario probabilities p_s, golden-master numbers, sizing, trades, execution, q-tilt, residual_edge numbers]
failure_modes: [using an improper score that rewards hedging away from belief, ranking on sharpness alone with no calibration, comparing scores across non-identical forecast sets, scoring a multivariate forecast with a dependency-blind rule, treating a score difference as significant without a Diebold-Mariano test]
tests: [test_outcome_calibration_card_exists, test_outcome_calibration_uses_strictly_proper_score]
---

# Outcome-Calibration Engine

> **Compiled from** *Strictly Proper Scoring Rules, Prediction, and Estimation* (Gneiting &
> Raftery, JASA 2007) and *Multivariate Forecasting Evaluation: On Sensitive and Strictly
> Proper Scoring Rules* (Ziel & Berk, 2019, arXiv:1910.07325). METHOD card: the PROCESS for
> **scoring and calibrating** probabilistic forecasts — the Q4 scenario probabilities and their
> later realised outcomes — with strictly proper scoring rules. It is a probability-*evaluation*
> primitive (calibration + sharpness), **not a probability generator**. Paraphrase only;
> **readable in discovery but not auto-wired**, it must NOT mutate the supplied `p_s` or change
> any golden-master numerical output. No case conclusions, no trades.

## Purpose
Provide a defensible way to **evaluate and justify** probabilistic forecasts: given the Q4
scenario probabilities (and, when available, the realised outcome), assign a *strictly proper*
score and report whether the forecast is **calibrated** and **sharp**. The guiding principle is
**maximise sharpness subject to calibration** — concentration is only a virtue once the
forecast is statistically consistent with what materialises. The card evaluates and ranks; it
never writes the probabilities.

## Process primitives (paraphrased)
- **Strictly proper scoring rules.** A scoring rule rewards a forecaster *most* for quoting
  their true belief: the expected score is maximised (or, in loss orientation, minimised) only
  by the true distribution. *Proper* means truth-telling is optimal; *strictly proper* means it
  is uniquely optimal, so the true model is identifiable. Improper rules (intuitive but
  hedge-rewarding) can be gamed and must be refused.
- **Calibration vs sharpness.** *Calibration* is statistical consistency between the forecast
  distribution and the observations (a joint property of forecasts and outcomes); *sharpness*
  is concentration of the predictive distribution (a property of the forecast alone). The goal
  is sharpness **subject to** calibration — never sharpness for its own sake.
- **Concrete proper scores (univariate).** Logarithmic score (links to Shannon entropy / KL
  divergence), quadratic / Brier score (categorical calibration primitive), spherical and
  pseudospherical scores, and the **Continuous Ranked Probability Score (CRPS)** for forecasts
  given as a CDF (it generalises absolute error and is strictly proper).
- **Proper scores derive from convexity.** Every proper score corresponds to a convex
  generalized-entropy / information measure, with the divergence between forecasts a Bregman
  divergence — which is why honesty is rewarded.
- **Skill scores need a reference.** To compare across heterogeneous forecast situations,
  standardise against a reference (e.g. a climatological / base-rate forecast): skill = 1 for
  an ideal forecast, 0 for the reference, negative for worse-than-reference. Raw scores are only
  comparable across *identical* forecast sets.
- **Multivariate / dependency-aware scoring (Ziel & Berk).** When the forecast object is
  joint (several scenario dimensions / horizons), marginal scores miss the dependency
  structure. Use the **energy score** (strictly proper, the standard multivariate CRPS
  generalisation) or a **marginal-copula score** (Sklar's theorem: score the marginals and the
  copula separately, then combine while preserving strict propriety) to capture dependency.
  Note the **variogram score** and **Dawid-Sebastiani score** are only *proper*, not strictly
  proper (they match correlation / first-two-moments), so they cannot uniquely identify the
  true model.
- **Significance of a score gap.** A difference in average score between two forecast
  procedures is not self-evidently meaningful; test it with a **Diebold-Mariano** test before
  declaring one forecaster better.

## When to use
At Q4 to *justify* a set of scenario probabilities (is the assignment defensible / honest under
a proper rule?), and post-resolution to *evaluate* a closed thesis's predicted-vs-realised
outcome (was it calibrated; how sharp; did it beat the reference; is the edge over a rival
forecast statistically real).

## Inputs
- `scenario_probabilities` — the supplied Q4 `p_s` (read-only).
- `scenario_outcomes` — the payoff/state space the probabilities are over.
- `realized_outcome` — what materialised (only available post-resolution).
- `reference_forecast` — base-rate / climatological benchmark for skill scoring.
- `competing_forecast_set` — rival forecasts to rank (for the DM comparison).

## Outputs
- `proper_score` — the strictly-proper score value(s) (log / Brier / CRPS / energy as fits).
- `calibration_assessment` — consistency of forecast with outcomes (qualitative + diagnostic).
- `sharpness_assessment` — concentration of the predictive distribution.
- `skill_score` — score standardised against the reference.
- `dm_comparison` — Diebold-Mariano verdict when ranking competing forecasts.
- `probability_justification` — the written defence of (or caveat on) the supplied `p_s`.

## Required fields
Every emission must name: the **scoring rule used** and that it is **strictly proper**, a
**calibration** verdict, a **sharpness** verdict (explicitly ranked *subject to* calibration),
and — for any cross-situation or cross-forecaster claim — the **reference** used and/or the
**DM test** result. A bare score with no calibration verdict is incomplete.

## Validation rules
- **Use a strictly proper score** — refuse improper rules that reward hedging away from belief;
  prefer log / Brier / CRPS (univariate) and energy / marginal-copula (multivariate).
- **Sharpness only subject to calibration** — never rank a forecast as better because it is
  sharper if it is not calibrated.
- **Require a reference for any skill / cross-situation claim** — raw scores compare only on
  *identical* forecast sets; otherwise standardise against a benchmark.
- **Dependency-aware in the multivariate case** — score joint forecasts with a dependency-
  sensitive *strictly* proper rule (energy / copula); do not certify the true model with a
  merely-proper rule (variogram, Dawid-Sebastiani).
- **Test before declaring superiority** — a score gap needs a Diebold-Mariano test.
- **Evaluation only** — never mutate the supplied `p_s`, emit q-tilt / residual_edge, or change
  any golden-master number (the card scores and justifies; it does not generate probabilities).

## Failure / blocked states
- Improper rule requested → block; substitute a strictly proper rule and state why.
- Sharp-but-uncalibrated forecast → flag; do not credit the sharpness.
- Cross-situation comparison with no reference → block the skill claim; ask for a benchmark.
- Multivariate forecast scored with a marginal-only / merely-proper rule → flag dependency
  blindness; recommend energy or copula score.
- Score difference asserted as "better" with no DM test → block the superiority claim.
- No `realized_outcome` yet → can assess propriety/sharpness of the *forecast* and justify
  `p_s`, but cannot give a calibration verdict; flag as pre-resolution.

## Example input
```yaml
scenario_probabilities: {base: 0.55, bull: 0.25, bear: 0.20}   # supplied p_s (read-only)
scenario_outcomes: [base, bull, bear]
realized_outcome: bear
reference_forecast: {base: 0.50, bull: 0.25, bear: 0.25}       # base-rate climatology
competing_forecast_set: [forecaster_A, forecaster_B]
```

## Example output
```yaml
scoring_rule: brier            # strictly proper, categorical
proper_score: "reported per forecaster (read-only over supplied p_s)"
calibration_assessment: "single draw insufficient; over the closed-thesis sample, bear states are under-weighted -> mild mis-calibration"
sharpness_assessment: "moderately concentrated; only credited because calibration holds in-sample"
skill_score: "positive vs the base-rate reference (beats climatology)"
dm_comparison: "A vs B score gap NOT significant at the chosen level -> do not declare a winner"
probability_justification: "p_s is defensible under a strictly proper rule; flag the bear-tail under-weighting for the next assignment. p_s unchanged."
```

## Non-goals
No generation or mutation of scenario probabilities `p_s`, no q-tilt, no residual-edge numbers,
no golden-master numbers, no sizing, no trades, no execution. The card evaluates, calibrates,
and justifies probabilities — it does not produce them.
