---
skill_name: factor-r2-router
access_class: method
compiled_from: ["Expected Returns - An Investors Guide to Harvesting Market Rewards (Antti Ilmanen) (z-library.sk, 1lib.sk, z-lib.sk).md"]
pipeline_phase: expression_family_routing
provider_seam: [discovery.select_strategy_families]
input_objects: [candidate_expression, thesis_axis, known_factor_premia, expression_pnl_drivers, premium_vs_alpha_tags]
output_objects: [factor_decomposition, purity_estimate, residual_alpha_share, harvested_premium_share, premium_overlap_flags]
gates_created: [separate_alpha_from_harvested_premium, require_thesis_axis_loading, flag_deceptively_alpha_like_carry]
allowed_to_influence: [qualitative expression-purity / rho-squared framing, alpha-vs-premium routing of strategy families]
not_allowed_to_influence: [scenario probabilities p_s, golden-master numbers, sizing, trades, execution, the rho-squared cap math, q-tilt, residual_edge numbers]
failure_modes: [crediting a harvested risk premium as thesis alpha, mislabelling a tail-insurance carry as edge, ignoring idiosyncratic vs systematic split, double-counting an exposure that is already a known factor, assuming a single market factor]
tests: [test_factor_r2_router_card_exists, test_factor_r2_router_separates_alpha_from_premium]
---

# Factor-R2 Router

> **Compiled from** *Expected Returns: An Investor's Guide to Harvesting Market Rewards*
> (Antti Ilmanen, 2011). METHOD card: the PROCESS that **informs** the expression PURITY
> (rho-squared) component of strategy-family routing. It decomposes a candidate expression's
> P&L into **known risk-premium / factor exposures** versus a **thesis-specific residual**, so
> the router can tell *harvested beta* from *thesis alpha*. Paraphrase only; **readable in
> discovery but not auto-wired** and must not change any golden-master numerical output, the
> rho-squared cap math, or scenario probabilities. No case conclusions, no trades.

## Purpose
Decompose a candidate expression's expected P&L into **two parts** — (a) exposure to *known,
already-rewarded* risk premia / factors, and (b) a *thesis-specific residual* that is the
actual edge being claimed — so the router can score expression **purity** (how much of the
P&L variance loads on the thesis axis, qualitatively rho-squared) and avoid crediting a
harvested premium as alpha. Feeds EXPRESSION-family routing.

## Process primitives (paraphrased)
Ilmanen's organising idea is a three-perspective "cube": every return source can be viewed
through **asset classes**, **strategy styles** (value, momentum/trend, carry, defensive), and
**underlying risk factors** (growth, inflation, illiquidity, tail/volatility). The card uses
this to split P&L:
- **Each position is a bundle of systematic factor exposures plus idiosyncratic risk.** Only
  *systematic, non-diversifiable* exposure is priced and earns a premium; idiosyncratic risk
  earns nothing. So first ask which *known* factors the expression loads on.
- **Alpha = the return that a common-factor model cannot explain** — the residual / intercept
  after regressing P&L on the known factors. As more factors enter the model, the scope for
  "alpha" shrinks. The thesis-specific residual is what survives that stripping.
- **Beta (harvested premium) vs alpha:** a positive expected return can come from *bearing a
  rewarded risk* (beta) or from *outsmarting others* (alpha). Routing must label which one a
  candidate expression is actually capturing.
- **Beware "deceptively alpha-like" payoffs.** Carry, volatility selling, and illiquidity
  harvesting throw off smooth positive returns that *look* like skill but are compensation for
  tail risk that shows up in bad times — classify these as harvested premium, not edge.
- **Purity = loading on the thesis axis.** The cleaner the mapping from the named thesis
  axis (a spread/slope series) to the expression's P&L, the higher the purity; P&L that is
  mostly explained by off-axis known factors is low-purity (premium contamination).
- Factor labels drift: some style alphas (value, carry) have *morphed into betas* over time.
  Treat the alpha/premium split as regime-dependent, not permanent.

## When to use
On a promoted theme with one or more candidate expressions, in discovery — to qualitatively
judge whether the expression's P&L actually tracks the thesis axis (high purity) or is mostly
a repackaged known risk premium, before routing to a strategy family.

## Inputs
- `candidate_expression` — the proposed way to express the thesis.
- `thesis_axis` — the named, operational spread/slope series the thesis is about.
- `known_factor_premia` — the catalogue of already-rewarded factors/styles to strip out.
- `expression_pnl_drivers` — what is understood to move the expression's P&L.
- `premium_vs_alpha_tags` — prior labels on whether each driver is risk-premium or edge.

## Outputs
- `factor_decomposition` — qualitative split of P&L into known-factor exposures vs residual.
- `purity_estimate` — qualitative rho-squared band (low / medium / high) of P&L on the axis.
- `residual_alpha_share` — qualitative size of the thesis-specific residual.
- `harvested_premium_share` — qualitative size of the known-premium component.
- `premium_overlap_flags` — flags where the "edge" is actually a known/crowded premium or a
  tail-insurance carry.

## Required fields
Every emission must carry: `thesis_axis` (named series), `factor_decomposition`,
`purity_estimate`, `residual_alpha_share`, `harvested_premium_share`, and any
`premium_overlap_flags`. Missing `thesis_axis` blocks the card (no axis = nothing to measure
purity against).

## Validation rules
- **Separate alpha from harvested premium** — never count exposure to a known, already-rewarded
  factor (term, credit, value, momentum, carry, illiquidity, tail) as thesis edge.
- **Require a thesis-axis loading** — purity is the share of P&L that tracks the *named* axis;
  if the expression's P&L is mostly off-axis known factors, mark it low-purity.
- **Flag deceptively alpha-like carry** — smooth carry / vol-selling / illiquidity income is
  harvested premium (tail insurance), not validated edge.
- **Systematic only** — idiosyncratic P&L is not a premium and not edge; do not bank it.
- **Qualitative only** — emit bands and flags, never set or alter the rho-squared cap number,
  q-tilt, residual_edge, scenario probabilities, or any golden-master output (the engine owns
  that math).

## Failure / blocked states
- No `thesis_axis` → cannot measure purity → block and request the operational axis.
- Expression P&L fully explained by known factors → `residual_alpha_share ≈ 0`,
  `premium_overlap_flags` set → route as premium harvest, not thesis alpha.
- Smooth positive carry with no mechanism on the axis → flag as tail-insurance premium.
- No factor catalogue available → can state the bundle qualitatively but not strip it; flag
  the gap.

## Example input
```yaml
candidate_expression: "long a high-carry credit basket vs duration-matched govvies"
thesis_axis: "issuer-specific spread vs sector index (named series)"
known_factor_premia: [credit_premium, illiquidity_premium, carry_style]
expression_pnl_drivers: [carry_income, sector_spread_beta, issuer_spread]
premium_vs_alpha_tags: {carry_income: premium, sector_spread_beta: premium, issuer_spread: candidate_alpha}
```

## Example output
```yaml
factor_decomposition:
  known_factor_share: "most P&L variance loads on credit + carry (off-axis)"
  residual_on_axis: "issuer-specific spread move vs the sector index"
purity_estimate: low_medium      # P&L mostly tracks the sector/credit premium, not the issuer axis
residual_alpha_share: small
harvested_premium_share: large
premium_overlap_flags: [carry_is_tail_insurance, credit_premium_double_count]
note: "Expression mainly harvests credit + carry premia; thesis-axis residual is thin -> low purity. Route as premium-harvest family unless the expression is re-cut to isolate the issuer axis."
```

## Non-goals
No factor *regression numbers*, no rho-squared cap math, no q-tilt, no residual-edge numbers,
no scenario probabilities, no sizing, no hedge ratios, no trades, no execution. Strategy
families only.

---

### Source-coverage note (large book — sections actually used)
Read and paraphrased: front matter / Contents (chapter map), Foreword (the alpha-vs-beta split
and the three-perspective framing), Chapter 1 introduction (the asset/style/factor "cube";
underlying-factor lens), Chapter 5 (SDF / multi-factor pricing, "only systematic risk is
priced", Jensen's alpha as the factor-model intercept, "alpha = return not explained by common
factors"), Part II preamble on *Underlying risk factors* (each asset as a bundle of factor
exposures; alphas morphing into betas; crowding as an endogenous factor). **Skipped** (market
content / empirics, not method): the twelve Part-II case-study chapters (8-19, specific
asset/strategy/factor histories), the tactical-forecasting and secular-trend chapters (21-27),
and the data appendices (A-B).
