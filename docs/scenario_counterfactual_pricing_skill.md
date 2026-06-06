# Skill: SCENARIO AND COUNTERFACTUAL PRICING ENGINE

> A process skill for an investment-research agent. For ONE causal **Theme Object**
> it answers a single question: **"how much of this theme is already priced, and
> what edge remains?"** It runs **AFTER** the causal compiler (which produced the
> operational axis) and **BEFORE** expression selection. It computes a scenario
> fair value, recovers the market-implied (risk-neutral) scenario measure by
> minimum-relative-entropy tilting, and reports the residual edge and a priced-in
> percentage. **It does NOT pick a trade, size it, or recommend it.**

---

## Source provenance (source-derived vs. standard-framework)

| Concept used in this skill | Where it comes from |
|---|---|
| Causal ladder: association → intervention (`do`) → counterfactual; "seeing ≠ doing" | **Source-derived.** Pearl, *The Book of Why* (`markdowns/The Book of Why ... .md`, repo PDF present). The "Super Thinker" primer (`markdowns/Thinking in Systems and Mental Models ... (Marcus P. Dawson).md`) is a generic mental-models text; the *ladder* itself is Pearl's. |
| Stock vs flow; reinforcing/balancing loops; delays; reflexivity of a signal on its own driver | **Source-derived.** Meadows, *Thinking in Systems: A Primer* (`markdowns/Thinking in Systems A Primer (Meadows...).md`, repo file present). |
| Scenario fair value `Σ p_s X_s`; "current market pricing (risk premium)" as an explicit valuation step; edge as model-FV vs market | **Source-derived.** `markdowns/Alaph Long Presentation Version July 2014.md` (the four-step process; French-banks worked trade). |
| The credit/risk premium as a STANDING confounder (a price level is not by itself a mispricing); liquidity scoring | **Standard-framework knowledge**, anchored to the Alaph "current market pricing (risk premium)" step and `markdowns/XantimumBizPlan.md`. |
| Minimum-KL exponential tilt to recover the implied measure; risk-neutral vs physical pricing-kernel map | **Standard-framework knowledge** (max-entropy / Kullback information projection; Girsanov / change-of-measure). Stated as such here. |
| **Reference implementation** of every formula below | **In-repo code.** `engine/engine2.py` — `solve_q_tilt`, `compute_edge`, `scenario_fair_value`, `run_pricing`. This skill card *points to that code*; it does not re-derive it. The applied example below **imports and calls** it. |

---

## The causal ladder mapped onto the three values

This is the conceptual core. The engine's three numeric objects are exactly Pearl's
three rungs of the ladder, applied to the axis:

| Rung | Pearl question | Engine object | Meaning on the axis |
|---|---|---|---|
| **Association** (rung 1, *seeing*) | `P(axis)` — what is the axis normally? | `normal_fv` | The **no-theme baseline**: where the axis sits absent any intervention by the driver. The unconditional / long-run level. |
| **Intervention** (rung 2, *doing*, `do(driver)`) | `P(axis \| do(driver=s))` — if we force the driver into state *s*, where does the axis go? | `X_s` and `X_FV = Σ p_s X_s` | Each scenario `X_s` is the axis fair value **under a forced driver path** (`do(·)`). `X_FV` is the probability-weighted interventional fair value. |
| **Counterfactual** (rung 3, *imagining*) | "had the theme not fired, vs it firing — what is the **marginal** axis effect?" | `X_s − normal_fv`, and in aggregate `X_FV − normal_fv` | The theme's **marginal effect**: the difference between the interventional fair value and the baseline that *would have held* otherwise. This is what the theme is *worth* if you are right, net of the world that would have happened anyway. |

The **edge** (`X_FV − X_mkt`) is then the gap between the interventional fair value
(rung 2) and what the market has *already* priced (recovered as `q`). The
counterfactual decomposition (rung 3) tells you whether that edge is the *theme's*
doing or just the baseline — i.e. it separates "the axis is here" from "the theme
moved the axis here".

---

## SKILL CARD

### skill_name
`scenario_counterfactual_pricing`

### purpose
Given a Theme Object carrying an **operational axis** and a set of probability-
weighted scenarios for that axis, quantify (a) the scenario fair value `X_FV`,
(b) the market-implied scenario measure `q` recovered by minimum-relative-entropy
tilting toward `X_mkt`, (c) the residual edge `⟨p − q, X⟩`, and (d) a `PricedIn%`.
It exposes — never hides — the feasibility of the implied-measure problem, the fact
that `q` is **risk-neutral** (edge is gross of premium unless a kernel is supplied),
the standing risk-premium confounder, and any reflexive scenarios / driver→axis
delays. Output is a `Pricing` object plus a PM-facing read on how much edge is left.

### when_to_use
- A `ThemeObject` has a **promoted, operational axis** (real historical series) and
  scenarios for it; you need to know if there is edge *before* spending effort on
  expression selection.
- You need to falsify "the market already knows this" — i.e. recover the implied
  scenario probabilities `q` and compare to your `p`.
- You need to report **how much of the move is priced in** to a PM.
- **Do not use** to choose / size / route a trade (that is Engine 3 / Engine 4); to
  build the axis or causal map (that is the Causal Theme Compiler); or when the axis
  is not yet operational (no series → no `X_mkt`, nothing to price).

### input_schema
```json
{
  "axis": "string  // named computable spread/slope/ratio with a real series",
  "X_mkt": "float  // current market-implied axis level (same unit as axis)",
  "normal_fv": "float  // rung-1 baseline: no-theme/unconditional axis level",
  "scenarios": [
    {
      "name": "string",
      "p_s": "float    // OUR (physical) probability of this state; Σ p_s = 1",
      "X_s": "float    // rung-2 interventional axis fair value | do(driver=state)",
      "sigma_s": "float  // optional within-scenario residual std of X_s (0 = point)"
    }
  ],
  "assumptions": ["string  // each scenario's driver path; horizon; channel"],
  "data_confidence": "string|float  // confidence in p_s and X_s (PM_assumption vs model_required)",
  "confounders": ["string  // incl. the STANDING risk-premium confounder, always"],
  "prior": "list[float]|'historical'|null  // default: historical freq if given, else uniform",
  "option_constraints": [
    {"strike": "float", "target": "float  // E_q[max(X-strike,0)] from a traded option"}
  ],
  "pricing_kernel": "list[float]|null  // m_s; maps risk-neutral q^Q to physical q^P. null → edge is GROSS of premium"
}
```

### output_schema
```json
{
  "normal_fv": "float",
  "scenario_fv": "float    // X_FV = Σ p_s X_s",
  "scenario_fv_std": "float  // law-of-total-variance std across + within scenarios",
  "priced_in": {
    "q_s": "list[float]   // recovered implied measure (risk-neutral)",
    "frac": "float        // (X_mkt - normal_fv)/(scenario_fv - normal_fv)"
  },
  "residual_edge": "float  // ⟨p - q, X⟩ = X_FV - X_mkt",
  "edge_attribution": [{"scenario": "string", "contribution": "float", "disagreement": "p_s - q_s"}],
  "PricedIn_pct": "float   // q_{s*}/p_{s*} clamped to [0,1], with raw (p_{s*}-q_{s*})",
  "q_status": "FEASIBLE|INFEASIBLE",
  "edge_basis": "gross_of_risk_premium | net_of_premium(kernel supplied)",
  "feasibility_reason": "string  // populated when INFEASIBLE"
}
```

### formulas (stated exactly; implemented in `engine/engine2.py`)
```
Scenario fair value (rung 2, interventional):
    X_FV = Σ_s p_s · X_s                                    # scenario_fair_value()

Implied measure q (min relative entropy to prior, matched to the market):
    q = argmin_q  KL(q ‖ prior)   s.t.  Σ_s q_s f_k(X_s) = c_k ,  Σ_s q_s = 1
    Solution is the EXPONENTIAL TILT:
        q_s ∝ prior_s · exp( Σ_k λ_k f_k(X_s) ),  λ solving the convex dual.   # solve_q_tilt()
    Base level constraint:  f_1(X)=X,  c_1 = X_mkt   (E_q[X] = X_mkt).
    Optional option constraints add f_k(X)=max(X-strike,0), c_k from traded prices.

Edge (identity):
    edge = X_FV - X_mkt = Σ_s (p_s - q_s) X_s = ⟨p - q, X⟩          # compute_edge()

Priced-in percentage (report for the chosen pivotal scenario s*):
    PricedIn% = clamp( q_{s*} / p_{s*} , 0, 1 )    reported WITH the raw (p_{s*} - q_{s*}).
    (Portfolio-level alt: frac = (X_mkt - normal_fv)/(scenario_fv - normal_fv).)
```

### feasibility_conditions
- `q` exists **iff** every target `c_k` is **strictly interior** to its payoff span
  across scenarios. For the level constraint this means
  **`min_s X_s < X_mkt < max_s X_s`**. If `X_mkt` sits at or beyond the extreme
  scenario, **no tilt of a finite set can match it** — the engine returns
  `status=INFEASIBLE` and **does not fabricate `q`**. (`solve_q_tilt` checks this
  before solving; see `engine/engine2.py` lines ~99–110.)
- Also requires `Σ p_s = 1`, `prior_s > 0` for all `s`, and at least 2 distinct `X_s`.
- INFEASIBLE is **information, not an error**: it means the market is pricing a level
  no modeled scenario reaches → the scenario set is incomplete. Add the missing
  tail state; do not clamp `X_mkt` into the span.

### risk_premium_handling
- The recovered `q` is the **risk-NEUTRAL** implied measure (it is what reproduces
  market prices, which embed compensation for risk). Therefore the edge
  `⟨p − q, X⟩` is **GROSS OF RISK PREMIUM**: part of the `p − q` gap can be a
  fair risk premium rather than a mispricing. The engine tags
  `edge_basis = "gross_of_risk_premium"` whenever no kernel is supplied.
- This is the **STANDING confounder** of pricing (the Alaph "current market pricing
  = risk premium" step, and Engine-2's own caveat): a wide axis level is not by
  itself an edge.
- To convert to a physical edge, supply a **pricing kernel** `m_s` and map
  `q^P_s = q^Q_s · (1/m_s) / E_q[1/m]`, then recompute the edge with `q^P`. Absent a
  kernel, the skill must **flag the edge as gross** and hand the premium question to
  the PM rather than silently treating `q` as physical.

### feedback_and_delays (Meadows)
- **Reflexive scenarios** — a state whose realisation feeds back on **its own
  probability** (e.g. heavy issuance → bond enters the index → forced buying →
  spread tightens, *reversing* the move that defined the scenario). Mark these:
  their `p_s` is endogenous and may flip sign at an unknown lag, so the tilt's `q`
  is only valid before the feedback dominates. Tag with the rebalance/feedback lag.
- **Driver→axis delays** — the `do(driver)` effect on `X_s` arrives with a lag
  (refi-wall timing, build-out cycle, rebalance schedule). The pricing snapshot is
  valid for the horizon over which the delay has *not yet* resolved; record the lag
  next to each scenario so the PM knows the edge's shelf-life.
- Both are **annotations on scenarios**, not new math: they tell the PM when `q`
  (and hence the edge) decays.

### data_requirements
- A real historical series for the axis (to anchor `X_mkt` and `normal_fv`).
- `X_mkt` from live quotes; `normal_fv` from the unconditional/long-run axis level.
- `p_s` (our view) and `X_s` (model fair value per state) — **each tagged
  `PM_assumption` or `model_required`**.
- `prior`: historical scenario frequencies if available (`hist_freq`); else uniform
  (maximum ignorance) is the documented default.
- Optional: traded option prices struck on the axis (for `option_constraints`); a
  pricing kernel `m_s` (to net the premium).

### non_identifiability
- `p` (physical) vs `q` (risk-neutral) are **not separable from prices alone**: the
  `p − q` gap conflates true edge with the risk premium. No amount of price data
  fixes this without an external kernel or a physical-probability estimate.
- With `K` constraints and `n > K+1` scenarios, `q` is **identified only up to the
  max-entropy choice** — it is the least-committed measure consistent with the
  market, not "the" market belief.
- A reflexive scenario's `p_s` is endogenous → not point-identified from a snapshot.

### failure_modes
- **Fabricating `q` when `X_mkt` is outside the scenario span.** The honest result
  is INFEASIBLE → enrich the scenario set; never clamp `X_mkt`.
- **Reporting the edge as if it were physical** when no kernel was supplied (premium
  leaks in as fake alpha). Always carry the `gross_of_premium` flag.
- **Using a raw level as the axis** (standing confounder leaks in) — the axis must
  be the netted differential the compiler produced.
- **Treating a flow-shock scenario as a permanent stock repricing** (Meadows): a
  new-issue concession mean-reverts; do not price it as a level shift.
- **Ignoring a reflexive scenario / delay** → edge with no shelf-life.
- **Mis-anchoring `normal_fv`** (using a theme-contaminated period as the baseline)
  → the counterfactual marginal effect is wrong.
- **Probabilities not summing to 1**, or a zero-mass prior bucket (tilt undefined).

### questions_for_PM
1. Is the `p − q` gap an edge or a **risk premium**? (Supply a kernel, or accept the
   edge as gross.)
2. Are the `p_s` / `X_s` your numbers (`PM_assumption`) or to be modeled
   (`model_required`)? Confidence on each?
3. Is the scenario set **complete** — especially if INFEASIBLE, what tail state is
   missing?
4. Which scenario is **pivotal** for `PricedIn%` (modal? the thesis state?)?
5. Do you trade **through** any reflexive loop / driver→axis delay, or before it?
6. Is `normal_fv` a clean, theme-free baseline?

### next_agent
`expression_scorer` (Engine 3). It consumes `residual_edge`, the per-scenario
`edge_attribution`, and `scenario_fv_std` to score candidate expressions
(purity ρ², asymmetry Ω, liquidity, crowding) and pick the best vehicle — a step
this skill deliberately does **not** perform.

### example_output
See the applied example below (generic cash-CDS basis compression, 4 scenarios,
numbers produced by importing and calling `engine/engine2.py`).

---

# APPLIED EXAMPLE — IG cash-CDS basis compression

**Theme (generic, post-compiler):** a wide-negative **IG cash-CDS basis**
dislocation will **compress** toward its long-run level as dealer balance-sheet /
funding pressure normalises.

**Axis (operational, netted differential):**
`IG cash-CDS basis = 5y CDS spread − duration-matched cash OAS, bps`.
A *more negative* basis = cash trades cheap to CDS. Compression = basis moves up
toward zero. (This is a real, quoted series; it nets the standing credit-risk-
premium confounder because it is a *same-issuer* differential, not a level.)

**Causal-ladder reading of the three values:**
- *Association (`normal_fv`)*: absent the theme the basis sits near its long-run
  mean ≈ **−12 bps**.
- *Intervention (`X_s`, `do(funding state)`)*: forcing each funding state gives the
  per-scenario fair basis below.
- *Counterfactual (`X_s − normal_fv`)*: the marginal compression the theme buys
  over the baseline.

### Inputs — every number tagged

| Field | Value | Tag |
|---|---|---|
| axis | IG cash-CDS basis, bps | — |
| `X_mkt` (market-implied basis now) | **−22.0 bps** | **PM_assumption** (live quote) |
| `normal_fv` (no-theme baseline) | **−12.0 bps** | **PM_assumption** (long-run mean) |
| prior | uniform `[0.25]×4` (max ignorance; no hist_freq given) | model default |
| pricing_kernel | **none supplied** | → edge **gross of premium** |

| Scenario | `p_s` (ours) | `X_s` (bps) | `σ_s` | tags |
|---|---|---|---|---|
| full_compression | 0.40 | −5.0 | 3.0 | p: PM_assumption · X: model_required |
| partial_compression | 0.35 | −15.0 | 4.0 | p: PM_assumption · X: model_required |
| status_quo | 0.15 | −25.0 | 5.0 | p: PM_assumption · X: model_required |
| dislocation_deepens (tail) | 0.10 | −40.0 | 6.0 | p: PM_assumption · X: model_required |

`Σ p_s = 1.0`. Confounders: **STANDING credit/funding risk premium** (the basis can
be wide as fair compensation for balance-sheet cost, not a mispricing); repo/funding
regime; rates/duration mismatch in the netting leg; CDS-index roll technicals.

### Computation (REAL — via `from engine.engine2 import run_pricing, solve_q_tilt, ...`)

**Feasibility check first:** scenario span = `(−40.0, −5.0)`; `X_mkt = −22.0` is
**strictly interior** ⇒ `q_status = FEASIBLE`. (Had `X_mkt` been, say, −45, the
engine would return INFEASIBLE and refuse to fabricate `q`.)

```
X_FV  = Σ p_s X_s = 0.40(−5) + 0.35(−15) + 0.15(−25) + 0.10(−40) = −15.0 bps
scenario_fv_std (law of total variance)                          =  11.578 bps

q (min-KL tilt, prior uniform, level constraint E_q[X] = −22.0):
    q = [0.232143, 0.242726, 0.253791, 0.271341]      λ = −0.0044578
    check: E_q[X] = −22.0  ✓ (matches X_mkt exactly)

edge = X_FV − X_mkt = ⟨p − q, X⟩ = −15.0 − (−22.0)        =  +7.0 bps
    cross-check ⟨p−q,X⟩ via compute_edge()                =  +7.0 bps  ✓

frac = (X_mkt − normal_fv)/(scenario_fv − normal_fv)
     = (−22 − (−12))/(−15 − (−12)) = −10/−3                =  3.333
```

**Edge attribution** (`(p_s − q_s)·X_s`, from `run_pricing`):

| scenario | contribution (bps) | disagreement `p−q` |
|---|---|---|
| dislocation_deepens | +6.854 | −0.1713 |
| status_quo | +2.595 | −0.1038 |
| full_compression | −0.839 | +0.1679 |
| partial_compression | −1.609 | +0.1073 |

**PricedIn%** — pivotal scenario `s* = full_compression` (our modal state, p=0.40):
```
q_{s*} = 0.232143,  p_{s*} = 0.40
PricedIn% = clamp(q_{s*}/p_{s*}, 0, 1) = clamp(0.5804, 0,1) = 58.04 %
raw (p_{s*} − q_{s*}) = +0.167857
```

### Interpretation (what the engine is and is NOT saying)
- **Edge = +7.0 bps, gross of premium.** Our interventional fair value (−15) is 7 bps
  tighter than the market-implied level (−22): the market has priced the basis
  *wider* (more dislocated) than our scenario-weighted view — `frac = 3.33` (>1)
  confirms the market has priced *beyond* the full theme move relative to baseline.
- The implied measure `q` puts only **23.2%** on full compression vs our **40%**, and
  *over*-weights the deepening tail (27.1% vs our 10%). The edge is the market over-
  pricing the wide-basis tail. **58% of our modal compression view is priced in;**
  ~42% (the `p−q` gap) is the latent edge — **but** this gap is gross of the
  funding/risk premium: with no kernel supplied we **cannot** assert it is all
  mispricing. A kernel `m_s` mapping `q^P_s = q^Q_s·(1/m_s)/E[1/m]` is required to net it.
- **Feedback/delay flags:** `full_compression` is mildly **reflexive** — if the
  basis compresses, basis-trade unwinds free up dealer balance sheet, which *further*
  compresses (reinforcing, lag ≈ days–weeks). `dislocation_deepens` is **balancing**
  (a repo squeeze self-corrects as funding clears, lag ≈ quarter-end timing). The
  edge's shelf-life is the funding-normalisation horizon.

---

## CLOSING ITEMS

- **trade_ready (t/f):** **f** — this skill quantifies edge only; it does not select,
  size, or route a trade. There IS positive computed edge (+7.0 bps), feasible `q`,
  and a clean attribution, so the theme is **promotable to Engine 3** — but it is not
  itself a trade decision, and the edge is gross of premium.
- **missing_data:**
  1. A **pricing kernel `m_s`** (or a physical-probability estimate) to convert the
     gross +7 bps edge into a premium-net edge — without it the edge is risk-neutral.
  2. Empirical **historical scenario frequencies** to replace the uniform prior.
  3. Validation that `X_mkt = −22` and `normal_fv = −12` are from a clean, theme-free
     basis series (both currently PM_assumption).
  4. Traded **option/skew prices** on the basis to add curvature constraints to `q`.
- **PM_questions:**
  1. Is the +7 bps `p−q` gap an edge or fair **funding/risk premium**? Supply a kernel
     or accept it as gross.
  2. Are `p_s` your numbers, and which scenario is **pivotal** for PricedIn% (modal
     vs thesis state)?
  3. Do you trade **through** the reflexive compression / balancing repo loop, or
     before quarter-end funding normalises?
  4. Is `normal_fv = −12 bps` a genuinely theme-free baseline?
- **next_agent_to_call:** `expression_scorer` (Engine 3) — consume `residual_edge`,
  `edge_attribution`, and `scenario_fv_std` to score and pick the best expression.

---

*File written by the Scenario and Counterfactual Pricing Engine skill. It quantifies
how much is priced and what edge remains; it does not select, size, or recommend a
trade. Formulas and the applied numbers are produced by `engine/engine2.py`
(`solve_q_tilt`, `compute_edge`, `scenario_fair_value`, `run_pricing`), called
read-only.*
