# Anonymous Corporate Bond RFQ Alpha Prediction Specification

## 0. Purpose

This document defines a detailed, code-translatable specification for creating **alpha-prediction features** from anonymous corporate bond RFQ data.

The objective is **not** RFQ quote optimization, fill prediction, inventory control, or market-making policy. The objective is:

```text
Predict future bond fair-value returns or spread returns from anonymous RFQ state.
```

The core prediction object is:

```text
Alpha_{i,t,h} = E[Return_{i,t,h} | Information available at RFQ time t]
```

where:

```text
i = bond / ISIN
t = RFQ timestamp
h = prediction horizon
```

The model should answer:

```text
Given anonymous RFQ flow, public factors, and bond state at time t,
does bond i become richer or cheaper over horizon h?
```

---

## 1. Scope

## 1.1 Included

This spec includes alphas based on:

1. anonymous RFQ side imbalance,
2. Cotton-scaled flow pressure,
3. RFQ intensity,
4. signed notional pressure,
5. repeat inquiry pressure,
6. dormant-bond wake-up,
7. issuer flow,
8. neighbor flow,
9. sector/rating/maturity group flow,
10. issuer curve pressure,
11. liquidity-conditioned flow,
12. flow acceleration and exhaustion,
13. cross-asset factor residuals,
14. flow-confirmed relative value,
15. ETF / CDX / rates lead-lag pressure,
16. historical markout momentum and reversal,
17. news / event interactions.

## 1.2 Excluded

The following are not primary targets in this document:

```text
fill probability
quote width
quote skew policy
client-specific toxicity
relationship pricing
dealer franchise value
optimal inventory control
```

Some quantities from market-making theory, especially local win-curve width `w`, are still used as **feature scalers**, not as quote-policy targets.

---

## 2. Data Contract

## 2.1 Required RFQ Inputs

Each RFQ event must contain:

| Field | Symbol | Required | Notes |
|---|---:|---:|---|
| RFQ ID | `rfq_id` | yes | unique event key |
| Timestamp | `t` | yes | quote/request timestamp |
| Bond ID | `i` | yes | ISIN or internal bond key |
| RFQ side | `side_t` | yes | dealer-perspective side |
| RFQ size | `size_t` | yes | notional or quantity |
| Venue | `venue_t` | preferred | MarketAxess, Tradeweb, Trumid, etc. |
| Protocol | `protocol_t` | preferred | single-name/list/firm/indicative |
| Your quote | `Q_t` | optional for alpha, useful | only needed for markout/quote-conditioned analysis |
| Fill flag | `fill_t` | optional for alpha, useful | not required for pure return labels |
| Number of requested dealers | `n_dealers_t` | optional | competition / information leakage proxy |

## 2.2 Required Bond Inputs

| Field | Symbol | Required | Notes |
|---|---:|---:|---|
| Fair value | `FV_{i,t}` | yes | as-of mark before or at RFQ time |
| Spread | `S_{i,t}` | preferred | OAS, G-spread, z-spread, or model spread |
| Clean price | `P_{i,t}` | preferred | if FV is price-based |
| Spread duration | `D^S_i` | yes for spread returns | converts spread move to price return |
| Rate duration | `D^R_i` | preferred | rate hedge / factor residual |
| Issuer | `issuer_i` | yes | issuer spillovers |
| Sector | `sector_i` | yes | group flow |
| Rating | `rating_i` | yes | group flow |
| Maturity | `mat_i` | yes | curve pressure |
| Liquidity score | `liq_i` | preferred | stratification |
| ADV / typical RFQ size | `ADV_i` | preferred | size pressure normalization |

## 2.3 Required Public Factor Inputs

Use what is available, but the intended factor vector is:

```text
F_t =
[
  CDX_IG_t,
  CDX_HY_t,
  Treasury_2Y_t,
  Treasury_5Y_t,
  Treasury_10Y_t,
  LQD_t,
  HYG_t,
  JNK_t,
  issuer_equity_t,
  VIX_t,
  MOVE_t
]
```

If issuer equity is unavailable for some issuers, use sector ETF or equity index proxy.

---

## 3. Canonical Sign Convention

Use dealer perspective:

```text
side_t = +1  means client sells bond to dealer.
side_t = -1  means client buys bond from dealer.
```

Therefore:

```text
side_t = +1
```

is anonymous selling pressure from clients.

For alpha prediction, define the intuitive pressure sign:

```text
SellPressure_{B,t} = q_{B,t} - 0.5
```

where `q_{B,t}` is the probability that anonymous flow in bucket `B` is client-sell flow.

If seller-heavy flow is informational, expected price return should usually be negative:

```text
SellPressure_{B,t} > 0  =>  E[PriceReturn_{i,t,h}] < 0
```

So define a return-oriented flow alpha:

```text
ReturnFlowAlpha_{B,t} = -SellPressure_{B,t}
```

or, using Cotton scaling:

```text
ReturnCottonAlpha_{B,t} = -CottonFlowSkew_{B,t}
```

Positive alpha should mean expected positive future bond price return.

---

## 4. Prediction Targets

## 4.1 Price Fair-Value Return

Primary target if your fair value is in clean-price basis points:

```text
R^{P}_{i,t,h} = FV^P_{i,t+h} - FV^P_{i,t}
```

where:

```text
FV^P = fair-value clean price
```

Positive means the bond richens in price.

## 4.2 Spread Return

If the model works in spread:

```text
ΔS_{i,t,h} = S_{i,t+h} - S_{i,t}
```

Convert spread move into approximate price return:

```text
R^{S}_{i,t,h} = -D^S_i × ΔS_{i,t,h}
```

where:

```text
D^S_i = spread duration
```

Positive means spread tightening / price richening.

## 4.3 Excess Return Over Factor Model

To isolate idiosyncratic alpha:

```text
R^{XS}_{i,t,h}
= R^P_{i,t,h} - β_i' ΔF_{t,h}
```

where:

```text
ΔF_{t,h} = F_{t+h} - F_t
```

## 4.4 Recommended Horizons

Use:

```text
h ∈ {30 minutes, 2 hours, 1 day, 3 days, 5 days, 10 days}
```

For your current responder horizon, emphasize:

```text
h = 5 days
```

but discover whether the signal is actually intraday, 1-day, or multi-day.

---

## 5. As-Of And Leakage Rules

Every feature must be computable with information available at or before RFQ time `t`.

Strict rule:

```text
feature_time <= t
```

Rolling RFQ features must exclude the current RFQ unless the field is known before prediction:

```text
use u < t, not u <= t
```

Labels use future marks:

```text
label_time = t + h
```

Validation must be time-blocked:

```text
train before validation before test
```

Use an embargo:

```text
embargo >= max(h)
```

For 5-day alpha:

```text
embargo >= 5 trading days
```

---

## 6. Buckets And Clocks

## 6.1 Bucket Families

Construct alpha features at multiple aggregation levels:

```text
B ∈ {
  ISIN,
  issuer,
  sector,
  rating,
  sector × rating,
  sector × rating × maturity,
  issuer × maturity bucket,
  venue,
  venue × sector,
  liquidity bucket,
  kNN neighbor set
}
```

## 6.2 Clock Families

Use multiple clocks:

| Clock | Definition | Why |
|---|---|---|
| Calendar window | last `W` time | good for active bonds |
| RFQ event window | last `N` RFQs | robust for sparse bonds |
| EWMA time clock | exponential decay by elapsed time | smooth pressure |
| Notional clock | last `V` notional | detects large risk transfer |

Recommended calendar windows:

```text
W ∈ {30m, 2h, 1d, 5d, 20d}
```

Recommended event windows:

```text
N ∈ {5, 10, 25, 50, 100, 250}
```

Recommended EWMA half-lives:

```text
τ ∈ {30m, 2h, 1d, 5d}
```

---

## 7. Alpha 1: Anonymous Flow Imbalance

## 7.1 Idea

Measure whether recent anonymous RFQ flow in a bucket is dominated by client sellers or client buyers.

## 7.2 Inputs

For all historical RFQs `u<t`:

```text
side_u
timestamp_u
bucket membership B(u)
```

## 7.3 Formula

EWMA client-sell count:

```text
N^+_{B,t}(τ)
= Σ_{u<t,u∈B} 1{side_u=+1} exp(-(t-u)/τ)
```

EWMA client-buy count:

```text
N^-_{B,t}(τ)
= Σ_{u<t,u∈B} 1{side_u=-1} exp(-(t-u)/τ)
```

Smoothed sell-flow probability:

```text
q_{B,t}
= (N^+_{B,t}+α) / (N^+_{B,t}+N^-_{B,t}+2α)
```

Recommended:

```text
α = 1
```

Flow imbalance:

```text
FlowImbalance_{B,t} = q_{B,t} - 0.5
```

Return-oriented alpha:

```text
FlowAlpha_{B,t} = -FlowImbalance_{B,t}
```

## 7.4 Interpretation

```text
FlowImbalance > 0  means client-seller pressure.
FlowAlpha > 0      means expected positive return under the convention that seller pressure predicts price weakness.
```

Actually, if seller pressure predicts future price declines, then:

```text
FlowImbalance > 0 => future price return < 0
```

So:

```text
FlowAlpha = -FlowImbalance
```

has the natural sign:

```text
positive FlowAlpha => expected positive price return.
```

## 7.5 Experiment

For each horizon `h`:

```text
R^P_{i,t,h}
= a
  + b FlowAlpha_{B,t}
  + Γ'Controls_{i,t}
  + FE_i
  + FE_date
  + ε_{i,t,h}
```

Pass condition:

```text
b > 0 out of sample
```

---

## 8. Alpha 2: Flow Log-Odds

## 8.1 Idea

Raw imbalance is bounded and can compress extreme pressure. Log-odds expands the tails.

## 8.2 Formula

Clip:

```text
q̃_{B,t} = min(max(q_{B,t}, ε), 1-ε)
```

Recommended:

```text
ε ∈ {0.02, 0.05}
```

Log-odds:

```text
FlowLogOdds_{B,t}
= log(q̃_{B,t} / (1-q̃_{B,t}))
```

Return-oriented version:

```text
FlowLogOddsAlpha_{B,t}
= -FlowLogOdds_{B,t}
```

## 8.3 Experiment

Compare:

```text
FlowAlpha = -(q-0.5)
```

against:

```text
FlowLogOddsAlpha = -log(q/(1-q))
```

Pass condition:

```text
log-odds improves OOS rank IC or top-minus-bottom return.
```

---

## 9. Alpha 3: Cotton-Scaled Flow Alpha

## 9.1 Idea

The same imbalance should matter more in a wide, noisy RFQ market than in a tight, competitive one.

Cotton scaling converts anonymous flow imbalance into a basis-point pressure variable using local win-curve width `w`.

## 9.2 Inputs

```text
q_{B,t}
w_{B,t}
```

## 9.3 Local Win-Curve Width

For historical RFQs in bucket `B`, define quote distance:

```text
d_u = side_u × (FV_{i,u} - Q_u)
```

where larger `d` means less aggressive quote.

Estimate:

```text
logit P(fill_u=1)
= a_B + b_B d_u + γ'X_u
```

with:

```text
b_B < 0
```

Then:

```text
w_{B,t} = -1/b_B
```

For alpha-only use, `w` is a scaler of flow pressure, not a target.

## 9.4 Cotton Flow Skew

```text
CottonFlowSkew_{B,t}
= (w_{B,t}/2) log(q̃_{B,t}/(1-q̃_{B,t}))
```

Return-oriented version:

```text
CottonFlowAlpha_{B,t}
= -CottonFlowSkew_{B,t}
```

## 9.5 Small-Imbalance Approximation

```text
CottonFlowSkew_{B,t}
≈ 2w_{B,t}(q_{B,t}-0.5)
```

So:

```text
CottonFlowAlpha_{B,t}
≈ -2w_{B,t}(q_{B,t}-0.5)
```

## 9.6 Experiment

Compare three versions:

```text
M1: R ~ FlowAlpha
M2: R ~ FlowLogOddsAlpha
M3: R ~ CottonFlowAlpha
```

Pass condition:

```text
CottonFlowAlpha improves OOS prediction versus raw imbalance and raw log-odds.
```

---

## 10. Alpha 4: RFQ Intensity Alpha

## 10.1 Idea

Abnormally high RFQ activity may indicate information arrival or forced risk transfer.

## 10.2 Formula

EWMA RFQ intensity:

```text
λ_{B,t}(τ)
= Σ_{u<t,u∈B} exp(-(t-u)/τ)
```

Historical same-clock baseline:

```text
μ_{B,c} = E[λ_{B,t} | clock(t)=c]
σ_{B,c} = sd[λ_{B,t} | clock(t)=c]
```

Intensity z-score:

```text
IntensityZ_{B,t}
= (λ_{B,t} - μ_{B,c}) / σ_{B,c}
```

## 10.3 Directional Version

Signed RFQ intensity:

```text
λ^S_{B,t}(τ)
= Σ_{u<t,u∈B} side_u exp(-(t-u)/τ)
```

Signed z-score:

```text
SignedIntensityZ_{B,t}
= (λ^S_{B,t} - μ^S_{B,c}) / σ^S_{B,c}
```

Return-oriented version:

```text
SignedIntensityAlpha_{B,t}
= -SignedIntensityZ_{B,t}
```

## 10.4 Experiment

```text
R^P_{i,t,h}
= a
  + b_1 IntensityZ_{B,t}
  + b_2 SignedIntensityAlpha_{B,t}
  + Γ'Controls
  + ε
```

Interpretation:

| Result | Meaning |
|---|---|
| `b_1` significant | attention itself predicts repricing |
| `b_2` significant | directional pressure predicts repricing |

---

## 11. Alpha 5: Signed Notional Pressure

## 11.1 Idea

Large RFQs should carry more information than small RFQs. Count imbalance and notional imbalance can differ.

## 11.2 Formula

Signed notional pressure:

```text
SignedNotional_{B,t}(τ)
= Σ_{u<t,u∈B} side_u size_u exp(-(t-u)/τ)
```

Normalize:

```text
SignedNotionalZ_{B,t}
= (SignedNotional_{B,t} - μ^V_{B,c}) / σ^V_{B,c}
```

Return-oriented:

```text
SignedNotionalAlpha_{B,t}
= -SignedNotionalZ_{B,t}
```

## 11.3 Alternative Probability Version

```text
V^+_{B,t}
= Σ_{u<t,u∈B} 1{side_u=+1} size_u exp(-(t-u)/τ)
```

```text
V^-_{B,t}
= Σ_{u<t,u∈B} 1{side_u=-1} size_u exp(-(t-u)/τ)
```

```text
q^V_{B,t}
= (V^+_{B,t}+α_V)/(V^+_{B,t}+V^-_{B,t}+2α_V)
```

```text
SizeFlowAlpha_{B,t}
= -(q^V_{B,t}-0.5)
```

Count-size gap:

```text
SizeFlowGap_{B,t}
= log(q̃^V_{B,t}/(1-q̃^V_{B,t}))
 - log(q̃_{B,t}/(1-q̃_{B,t}))
```

## 11.4 Experiment

```text
R_{i,t,h}
= a
  + b_1 FlowAlpha_{B,t}
  + b_2 SignedNotionalAlpha_{B,t}
  + b_3 SizeFlowGap_{B,t}
  + Γ'Controls
  + ε
```

Pass:

```text
b_2 or b_3 adds OOS lift beyond count flow.
```

---

## 12. Alpha 6: Repeat-Inquiry Alpha

## 12.1 Idea

Repeated same-bond RFQs may indicate urgency or information. Direction matters.

## 12.2 Formula

For window `W`:

```text
RepeatCount_{i,t,W}
= #{u<t: ISIN_u=i, t-W <= u < t}
```

Signed repeat pressure:

```text
RepeatSigned_{i,t,W}
= Σ_{u<t,ISIN_u=i,t-W<=u<t} side_u
```

Same-side repeat concentration:

```text
RepeatSameSide_{i,t,W}
= max(
  #{u<t: ISIN_u=i, side_u=+1, t-W<=u<t},
  #{u<t: ISIN_u=i, side_u=-1, t-W<=u<t}
)
```

Return-oriented:

```text
RepeatAlpha_{i,t,W}
= -RepeatSigned_{i,t,W}
```

## 12.3 Experiment

```text
R_{i,t,h}
= a
  + b_1 RepeatAlpha_{i,t,W}
  + b_2 RepeatSameSide_{i,t,W}
  + b_3 RepeatCount_{i,t,W}
  + Γ'Controls
  + ε
```

Interpretation:

| Pattern | Meaning |
|---|---|
| `RepeatAlpha` predicts continuation | repeated flow is informed |
| `RepeatAlpha` predicts reversal | repeated flow is liquidity pressure |
| only `RepeatCount` matters | attention matters more than direction |

---

## 13. Alpha 7: Dormant Wake-Up Alpha

## 13.1 Idea

An RFQ in a normally inactive bond may reveal stale mark adjustment or new information.

## 13.2 Formula

Time since last RFQ:

```text
ΔLastRFQ_{i,t}
= t - max{u<t: ISIN_u=i}
```

Historical threshold:

```text
WakeThreshold_i
= Q_{0.90}(ΔLastRFQ_i)
```

Wake-up indicator:

```text
DormantWakeup_{i,t}
= 1{ΔLastRFQ_{i,t} > WakeThreshold_i}
```

Directional wake-up alpha:

```text
DormantWakeupAlpha_{i,t}
= -side_t × DormantWakeup_{i,t}
```

## 13.3 Experiment

```text
R_{i,t,h}
= a
  + b_1 DormantWakeupAlpha_{i,t}
  + b_2 DormantWakeup_{i,t}
  + Γ'Controls
  + ε
```

---

## 14. Alpha 8: Issuer Flow Alpha

## 14.1 Idea

Flow in one bond from an issuer can predict repricing in other bonds from the same issuer.

## 14.2 Formula

For issuer `a = issuer(i)`:

```text
IssuerImbalance_{a,t}
= q_{a,t} - 0.5
```

where `q_{a,t}` is computed from all bonds of issuer `a`, excluding the current RFQ and optionally excluding the current ISIN:

```text
u<t, issuer(u)=a, ISIN_u != i
```

Return-oriented:

```text
IssuerFlowAlpha_{a,t}
= -IssuerImbalance_{a,t}
```

## 14.3 Experiment

```text
R_{i,t,h}
= a
  + b_1 FlowAlpha_{i,t}
  + b_2 IssuerFlowAlpha_{a,t}
  + Γ'Controls
  + FE_i
  + ε
```

Pass:

```text
b_2 improves OOS alpha beyond own-ISIN flow.
```

---

## 15. Alpha 9: Neighbor Flow Alpha

## 15.1 Idea

For sparse bonds, economically similar bonds may carry more signal than the bond itself.

## 15.2 Neighbor Definition

Define bond descriptor:

```text
Z_i =
[
  sector_i,
  rating_i,
  maturity_i,
  spread_duration_i,
  rate_duration_i,
  liquidity_i,
  factor_beta_i
]
```

Distance:

```text
Dist(i,j)
= weighted_distance(Z_i,Z_j)
```

Neighbor set:

```text
N_K(i) = K nearest bonds to i
```

Weights:

```text
ω_{ij}
= exp(-Dist(i,j)/η)
  /
  Σ_{l∈N_K(i)} exp(-Dist(i,l)/η)
```

## 15.3 Feature

```text
NeighborImbalance_{i,t}
= Σ_{j∈N_K(i)} ω_{ij} FlowImbalance_{j,t}
```

Return-oriented:

```text
NeighborFlowAlpha_{i,t}
= -NeighborImbalance_{i,t}
```

## 15.4 Experiment

```text
R_{i,t,h}
= a
  + b_1 FlowAlpha_{i,t}
  + b_2 IssuerFlowAlpha_{a,t}
  + b_3 NeighborFlowAlpha_{i,t}
  + Γ'Controls
  + ε
```

Pass:

```text
b_3 stable and improves OOS rank IC.
```

---

## 16. Alpha 10: Sector / Rating / Maturity Group Flow

## 16.1 Idea

Portfolio-level de-risking often appears at the group level rather than individual ISIN level.

## 16.2 Bucket

```text
g(i) = sector_i × rating_bucket_i × maturity_bucket_i
```

## 16.3 Formula

```text
GroupImbalance_{g,t}
= q_{g,t} - 0.5
```

Return-oriented:

```text
GroupFlowAlpha_{g,t}
= -GroupImbalance_{g,t}
```

## 16.4 Experiment

```text
R_{i,t,h}
= a
  + b_1 FlowAlpha_{i,t}
  + b_2 IssuerFlowAlpha_{a,t}
  + b_3 GroupFlowAlpha_{g,t}
  + Γ'Controls
  + ε
```

---

## 17. Alpha 11: Issuer Curve Pressure

## 17.1 Idea

Issuer flow can be concentrated in maturity buckets. Long-end selling can predict different returns for long versus short bonds.

## 17.2 Maturity Buckets

Example:

```text
short: maturity <= 3y
belly: 3y < maturity <= 7y
long: maturity > 7y
```

## 17.3 Formula

```text
LongImb_{a,t} = FlowImbalance_{issuer=a,long,t}
```

```text
ShortImb_{a,t} = FlowImbalance_{issuer=a,short,t}
```

Curve pressure:

```text
CurvePressure_{a,t}
= LongImb_{a,t} - ShortImb_{a,t}
```

Bond alignment:

```text
maturity_sign_i =
  +1 if bond i is long
   0 if bond i is belly
  -1 if bond i is short
```

Return-oriented curve alpha:

```text
CurveFlowAlpha_{i,t}
= -maturity_sign_i × CurvePressure_{a,t}
```

## 17.4 Experiment

```text
R_{i,t,h}
= a
  + b CurveFlowAlpha_{i,t}
  + Γ'Controls
  + FE_{issuer}
  + ε
```

---

## 18. Alpha 12: Liquidity-Conditioned Flow

## 18.1 Idea

Anonymous flow should predict future returns more strongly when liquidity is poor.

## 18.2 Width Z-Score

Observed width:

```text
WidthObs_{i,t} = Ask_{i,t} - Bid_{i,t}
```

or proxy:

```text
quote dispersion
model bid-offer
TRACE liquidity proxy
RFQ-implied width
```

Normalize:

```text
WidthZ_{i,t}
= (WidthObs_{i,t} - μ_{bucket,clock}) / σ_{bucket,clock}
```

## 18.3 Feature

```text
LiquidityConditionedFlowAlpha_{i,t}
= FlowAlpha_{B,t} × WidthZ_{i,t}
```

Magnitude-only pressure:

```text
AbsLiquidityPressure_{i,t}
= |FlowImbalance_{B,t}| × WidthZ_{i,t}
```

## 18.4 Experiment

```text
R_{i,t,h}
= a
  + b_1 FlowAlpha_{B,t}
  + b_2 WidthZ_{i,t}
  + b_3 LiquidityConditionedFlowAlpha_{i,t}
  + Γ'Controls
  + ε
```

Pass:

```text
b_3 > 0
```

if flow alpha is stronger in wide markets.

---

## 19. Alpha 13: Flow Acceleration

## 19.1 Idea

The level of flow imbalance matters, but the change in pressure may matter more.

## 19.2 Formula

Short-window imbalance:

```text
ImbShort_{B,t} = FlowImbalance_{B,t}^{short}
```

Long-window imbalance:

```text
ImbLong_{B,t} = FlowImbalance_{B,t}^{long}
```

Acceleration:

```text
FlowAcceleration_{B,t}
= ImbShort_{B,t} - ImbLong_{B,t}
```

Return-oriented:

```text
FlowAccelerationAlpha_{B,t}
= -FlowAcceleration_{B,t}
```

## 19.3 Experiment

```text
R_{i,t,h}
= a
  + b_1 FlowAlpha_{B,t}
  + b_2 FlowAccelerationAlpha_{B,t}
  + Γ'Controls
  + ε
```

---

## 20. Alpha 14: Flow Exhaustion / Reversal

## 20.1 Idea

If flow has been extremely one-sided but is now decelerating, future returns may reverse.

## 20.2 Formula

Extreme long-window pressure:

```text
ExtremeFlow_{B,t}
= 1{|ImbLong_{B,t}| > c}
```

Recommended:

```text
c = historical 80th or 90th percentile of |ImbLong|
```

Exhaustion score:

```text
FlowExhaustion_{B,t}
= ExtremeFlow_{B,t}
  × [-sign(ImbLong_{B,t}) × FlowAcceleration_{B,t}]
```

Interpretation:

```text
positive FlowExhaustion means previous one-sided pressure is fading.
```

Reversal alpha:

```text
FlowReversalAlpha_{B,t}
= sign(ImbLong_{B,t}) × FlowExhaustion_{B,t}
```

This says:

- after extreme client selling that fades, expect positive reversal,
- after extreme client buying that fades, expect negative reversal.

## 20.3 Experiment

```text
R_{i,t,h}
= a
  + b_1 FlowAlpha_{B,t}
  + b_2 FlowAccelerationAlpha_{B,t}
  + b_3 FlowReversalAlpha_{B,t}
  + Γ'Controls
  + ε
```

---

## 21. Alpha 15: Factor Residual Rich/Cheap

## 21.1 Idea

Bond fair value should be explained by public credit, rates, ETF, equity, and volatility factors. Residual deviations may mean revert.

## 21.2 Factor Model

Estimate historical exposure:

```text
β_i
= argmin_β Σ_{s<t}
   (ΔFV_{i,s} - β'ΔF_s)^2
   + λ||β||_2^2
```

Use shrinkage because many bonds are sparse.

## 21.3 Factor-Implied Fair Value

```text
FVHat_{i,t} = β_i'F_t
```

Residual:

```text
RVResidual_{i,t}
= FV_{i,t} - FVHat_{i,t}
```

Normalized:

```text
RVZ_{i,t}
= (RVResidual_{i,t} - μ^{RV}_{i,t}) / σ^{RV}_{i,t}
```

Mean-reversion alpha:

```text
RVAlpha_{i,t} = -RVZ_{i,t}
```

## 21.4 Experiment

```text
R_{i,t,h}
= a
  + b RVAlpha_{i,t}
  + Γ'Controls
  + ε
```

Pass:

```text
b > 0
```

if residual rich/cheap mean-reverts.

---

## 22. Alpha 16: Flow-Confirmed Relative Value

## 22.1 Idea

Relative-value signals are more useful when anonymous flow confirms the direction.

## 22.2 Formula

Flow expected return sign:

```text
FlowSign_{B,t} = sign(FlowAlpha_{B,t})
```

RV expected return sign:

```text
RVSign_{i,t} = sign(RVAlpha_{i,t})
```

Agreement indicator:

```text
FlowRVAgree_{i,t}
= 1{FlowSign_{B,t} = RVSign_{i,t}}
```

Continuous feature:

```text
FlowConfirmedRV_{i,t}
= RVAlpha_{i,t} × FlowSign_{B,t}
```

Alternative:

```text
FlowConfirmedRV2_{i,t}
= RVAlpha_{i,t} × FlowAlpha_{B,t}
```

## 22.3 Experiment

```text
R_{i,t,h}
= a
  + b_1 RVAlpha_{i,t}
  + b_2 FlowAlpha_{B,t}
  + b_3 FlowConfirmedRV2_{i,t}
  + Γ'Controls
  + ε
```

Pass:

```text
b_3 > 0
```

if flow confirmation strengthens RV alpha.

---

## 23. Alpha 17: Cross-Asset Lead Alpha

## 23.1 Idea

Liquid markets often move before individual corporate bond marks update.

## 23.2 Factor Moves

For factor vector `F_t`, compute recent changes:

```text
ΔF_{t,L} = F_t - F_{t-L}
```

Bond-specific factor lead:

```text
CrossAssetLead_{i,t,L}
= β_i'ΔF_{t,L}
```

## 23.3 Components

Credit index lead:

```text
CDXLead_{i,t}
= β_{i,CDX} ΔCDX_t
```

Rates lead:

```text
RatesLead_{i,t}
= β_{i,rates}' ΔRates_t
```

ETF lead:

```text
ETFLead_{i,t}
= β_{i,ETF} ΔETF_t
```

Equity-credit lead:

```text
EquityLead_{i,t}
= β_{i,eq} ΔEquity_{issuer,t}
```

## 23.4 Experiment

```text
R_{i,t,h}
= a
  + b_1 CrossAssetLead_{i,t,L}
  + b_2 FlowAlpha_{B,t}
  + b_3 CrossAssetLead_{i,t,L} × FlowAlpha_{B,t}
  + Γ'Controls
  + ε
```

Interpretation:

```text
b_1 captures public-market lead-lag.
b_3 captures whether RFQ flow confirms the public factor move.
```

---

## 24. Alpha 18: ETF / Cash-Credit Pressure

## 24.1 Idea

Credit ETFs can create portfolio pressure that later appears in individual cash bonds.

## 24.2 ETF Pressure

For ETF `E`, such as LQD, HYG, JNK:

```text
ETFVolumeZ_{E,t}
= (Volume_{E,t} - μ^V_E) / σ^V_E
```

```text
ETFPressure_{E,t}
= Return_{E,t,L} × ETFVolumeZ_{E,t}
```

If premium/discount is available:

```text
ETFBasisPressure_{E,t}
= PremiumDiscount_{E,t} × ETFVolumeZ_{E,t}
```

Bond-mapped ETF pressure:

```text
ETFAlpha_{i,t}
= β_{i,E} ETFPressure_{E,t}
```

## 24.3 Experiment

```text
R_{i,t,h}
= a
  + b_1 ETFAlpha_{i,t}
  + b_2 FlowAlpha_{B,t}
  + b_3 ETFAlpha_{i,t} × FlowAlpha_{B,t}
  + Γ'Controls
  + ε
```

---

## 25. Alpha 19: Markout Momentum

## 25.1 Idea

Recent RFQ-conditioned markouts in the same bucket may persist.

## 25.2 Formula

Historical bucket markout:

```text
BucketReturn_{B,u,h}
= FV_{i,u+h} - FV_{i,u}
```

Recent average:

```text
MarkoutMomentum_{B,t,h0}
= Σ_{u<t,u∈B} BucketReturn_{B,u,h0} exp(-(t-u)/τ)
  /
  Σ_{u<t,u∈B} exp(-(t-u)/τ)
```

Use a short formation horizon `h0`, for example:

```text
h0 ∈ {30m, 2h, 1d}
```

## 25.3 Experiment

```text
R_{i,t,h}
= a
  + b MarkoutMomentum_{B,t,h0}
  + Γ'Controls
  + ε
```

Pass:

```text
b > 0
```

for continuation.

---

## 26. Alpha 20: Markout Reversal

## 26.1 Idea

Large recent moves caused by liquidity pressure may reverse.

## 26.2 Formula

Extreme recent markout:

```text
ExtremeMarkout_{B,t}
= 1{|MarkoutMomentum_{B,t,h0}| > Q_{0.90}(|MarkoutMomentum_B|)}
```

Liquidity condition:

```text
StressedLiquidity_{i,t}
= 1{WidthZ_{i,t} > Q_{0.80}(WidthZ_i)}
```

No public-factor confirmation:

```text
NoFactorConfirm_{i,t}
= 1{sign(MarkoutMomentum_{B,t,h0}) != sign(CrossAssetLead_{i,t,L})}
```

Reversal alpha:

```text
MarkoutReversalAlpha_{i,t}
= -MarkoutMomentum_{B,t,h0}
   × ExtremeMarkout_{B,t}
   × StressedLiquidity_{i,t}
   × NoFactorConfirm_{i,t}
```

## 26.3 Experiment

```text
R_{i,t,h}
= a
  + b_1 MarkoutMomentum_{B,t,h0}
  + b_2 MarkoutReversalAlpha_{i,t}
  + Γ'Controls
  + ε
```

---

## 27. Alpha 21: News / Event Flow Interaction

## 27.1 Idea

Anonymous flow may be more informative around events.

## 27.2 Event Indicators

Construct:

```text
Event_{i,t} ∈ {0,1}
```

for:

```text
issuer earnings
rating action
large issuer equity move
large CDX move
large Treasury move
macro event: CPI, payrolls, FOMC
sector news
new issue announcement
```

## 27.3 Interaction Features

```text
EventFlowAlpha_{i,t}
= FlowAlpha_{B,t} × Event_{i,t}
```

```text
EventIntensityAlpha_{i,t}
= SignedIntensityAlpha_{B,t} × Event_{i,t}
```

## 27.4 Experiment

```text
R_{i,t,h}
= a
  + b_1 FlowAlpha_{B,t}
  + b_2 Event_{i,t}
  + b_3 EventFlowAlpha_{i,t}
  + Γ'Controls
  + ε
```

Pass:

```text
b_3 > 0
```

if flow is more informative around events.

---

## 28. Controls For Alpha Prediction

Use controls to avoid confusing alpha with static risk premia or mechanical factor exposure.

Minimum controls:

```text
rating_bucket_i
sector_i
maturity_bucket_i
spread_duration_i
rate_duration_i
liquidity_bucket_i
log(issue_size_i)
bond_age_i
time_of_day_t
day_of_week_t
venue_t
market_vol_state_t
recent_CDX_move_t
recent_rates_move_t
recent_ETF_move_t
```

Optional fixed effects:

```text
ISIN fixed effects
issuer fixed effects
date fixed effects
sector × rating fixed effects
venue fixed effects
```

For sparse data, avoid overusing fixed effects that absorb the signal.

---

## 29. Model Families

## 29.1 Linear Baseline

For interpretability:

```text
R_{i,t,h}
= a
  + β'AlphaFeatures_{i,t}
  + Γ'Controls_{i,t}
  + FE
  + ε_{i,t,h}
```

## 29.2 Regularized Linear Model

Use when feature count is high:

```text
β̂
= argmin_β
Σ (R_{i,t,h} - β'X_{i,t})^2
+ λ_1 ||β||_1
+ λ_2 ||β||_2^2
```

## 29.3 Tree / Boosting Model

Use for interactions:

```text
R_{i,t,h} = f(X_{i,t}) + ε
```

Key interactions to allow:

```text
FlowAlpha × WidthZ
FlowAlpha × Event
FlowAlpha × CrossAssetLead
RVAlpha × FlowAlpha
Intensity × Liquidity
NeighborFlow × OwnFlow
```

## 29.4 Ranking Model

For cross-sectional alpha:

```text
rank(R_{i,t,h}) = f(rank(features_{i,t}))
```

Evaluate by:

```text
rank IC
top-minus-bottom decile return
hit rate
```

---

## 30. Experiment Ladder

## 30.1 Experiment A: Single-Feature IC

For each alpha feature `X`:

```text
IC_h(X) = corr_cross_sectional(X_{i,t}, R_{i,t,h})
```

Compute by date and average:

```text
MeanIC_h = mean_t IC_{t,h}
```

Pass:

```text
stable sign
positive t-stat
not concentrated in one period
```

## 30.2 Experiment B: Horizon Curve

For each feature:

```text
β(h), IC(h), DecileSpread(h)
```

for:

```text
h ∈ {30m, 2h, 1d, 3d, 5d, 10d}
```

Classification:

| Horizon Pattern | Interpretation |
|---|---|
| immediate then fades | stale mark / microstructure |
| grows to 3-5 days | information alpha |
| reverses after initial move | liquidity pressure |
| only same day | execution / marking artifact |

## 30.3 Experiment C: Nested Model Test

Models:

```text
M0: controls only
M1: M0 + own flow
M2: M1 + issuer/group/neighbor flow
M3: M2 + intensity/notional/repeat features
M4: M3 + factor residuals and cross-asset leads
M5: M4 + event interactions
```

Metrics:

```text
OOS R2
rank IC
top-minus-bottom decile return
directional hit rate
turnover-adjusted alpha
```

## 30.4 Experiment D: Raw Flow Versus Cotton Scaling

Compare:

```text
X1 = FlowAlpha
X2 = FlowLogOddsAlpha
X3 = CottonFlowAlpha
```

Pass:

```text
CottonFlowAlpha improves OOS IC or decile spread.
```

If it does not, keep raw flow and log-odds as preferred alpha features.

## 30.5 Experiment E: Flow Versus Public Factors

Test whether flow adds information beyond liquid markets:

```text
R_{i,t,h}
= a
  + β_1 FlowAlpha
  + β_2 CrossAssetLead
  + β_3 RVAlpha
  + Γ'Controls
  + ε
```

Pass:

```text
β_1 survives after CrossAssetLead and RVAlpha.
```

## 30.6 Experiment F: Continuation Versus Reversal

Estimate:

```text
R_{i,t,h}
= a
  + β_1 FlowAlpha
  + β_2 FlowReversalAlpha
  + β_3 MarkoutMomentum
  + β_4 MarkoutReversalAlpha
  + Γ'Controls
  + ε
```

Classify signal as:

```text
information continuation
liquidity reversal
stale-mark correction
noise
```

---

## 31. Feature Promotion Rules

Promote an alpha feature only if:

```text
1. It is as-of computable.
2. It improves OOS rank IC or OOS R2.
3. It has stable sign across time splits.
4. It survives major universe splits.
5. It is not explained away by public factors.
6. It has reasonable turnover / decay.
7. It improves top-minus-bottom portfolio return or RFQ decision ranking.
```

Major splits:

```text
IG vs HY
liquid vs illiquid
large vs small RFQ
single-name vs list RFQ
venue
sector
rating
maturity bucket
calm vs stressed markets
event vs non-event windows
```

---

## 32. Minimum Implementation Order

Build in this order:

```text
1. As-of RFQ panel
2. Future return labels: 30m, 2h, 1d, 3d, 5d, 10d
3. FlowImbalance by ISIN, issuer, group
4. FlowAlpha and FlowLogOddsAlpha
5. Win-curve width w for Cotton scaling
6. CottonFlowAlpha
7. IntensityZ and SignedIntensityAlpha
8. SignedNotionalAlpha
9. RepeatAlpha and DormantWakeupAlpha
10. IssuerFlowAlpha and NeighborFlowAlpha
11. GroupFlowAlpha and CurveFlowAlpha
12. WidthZ and LiquidityConditionedFlowAlpha
13. CrossAssetLead and RVAlpha
14. FlowConfirmedRV
15. MarkoutMomentum and MarkoutReversalAlpha
16. EventFlowAlpha
17. Single-feature IC tests
18. Nested model tests
19. Horizon classification
20. Promotion table
```

---

## 33. Final Alpha Inventory

| ID | Feature | Formula Sketch | Primary Hypothesis |
|---|---|---|---|
| A1 | `FlowAlpha` | `-(q-0.5)` | anonymous seller pressure predicts price weakness |
| A2 | `FlowLogOddsAlpha` | `-log(q/(1-q))` | extreme imbalance has nonlinear effect |
| A3 | `CottonFlowAlpha` | `-(w/2)log(q/(1-q))` | imbalance matters more in wide RFQ markets |
| A4 | `IntensityZ` | z-score RFQ count | attention predicts repricing |
| A5 | `SignedIntensityAlpha` | negative signed intensity z | directional RFQ intensity predicts returns |
| A6 | `SignedNotionalAlpha` | negative signed size pressure | large same-side flow is more informative |
| A7 | `SizeFlowGap` | size log-odds minus count log-odds | block flow differs from count flow |
| A8 | `RepeatAlpha` | negative repeat signed flow | repeated same-side RFQs predict continuation/reversal |
| A9 | `DormantWakeupAlpha` | `-side × dormant flag` | inactive bond RFQ reveals stale mark |
| A10 | `IssuerFlowAlpha` | negative issuer imbalance | issuer-level spillover |
| A11 | `NeighborFlowAlpha` | negative weighted neighbor imbalance | similar-bond spillover |
| A12 | `GroupFlowAlpha` | negative group imbalance | portfolio de-risking pressure |
| A13 | `CurveFlowAlpha` | negative maturity-aligned curve pressure | issuer curve repricing |
| A14 | `LiquidityConditionedFlowAlpha` | `FlowAlpha × WidthZ` | flow stronger in illiquid states |
| A15 | `FlowAccelerationAlpha` | negative short-minus-long imbalance | pressure building |
| A16 | `FlowReversalAlpha` | exhaustion of extreme flow | liquidity reversal |
| A17 | `RVAlpha` | `-RVZ` | factor residual mean reversion |
| A18 | `FlowConfirmedRV` | `RVAlpha × FlowAlpha` | RV stronger when flow agrees |
| A19 | `CrossAssetLead` | `β'ΔF` | liquid markets lead cash bond marks |
| A20 | `ETFAlpha` | `β_ETF × ETFPressure` | ETF pressure leads cash repricing |
| A21 | `MarkoutMomentum` | recent bucket return | continuation in recent markouts |
| A22 | `MarkoutReversalAlpha` | negative extreme markout under stress | liquidity-driven reversal |
| A23 | `EventFlowAlpha` | `FlowAlpha × Event` | flow more informative around events |
| A24 | `EventIntensityAlpha` | `SignedIntensityAlpha × Event` | event-period urgency predicts returns |

---

## 34. First Research Table To Produce

Produce this table for each horizon:

| Feature | Coverage | Mean | Std | IC | IC t-stat | OOS R2 contribution | Top-bottom decile | Sign stable? | Promote? |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| FlowAlpha | | | | | | | | | |
| FlowLogOddsAlpha | | | | | | | | | |
| CottonFlowAlpha | | | | | | | | | |
| SignedIntensityAlpha | | | | | | | | | |
| SignedNotionalAlpha | | | | | | | | | |
| RepeatAlpha | | | | | | | | | |
| IssuerFlowAlpha | | | | | | | | | |
| NeighborFlowAlpha | | | | | | | | | |
| GroupFlowAlpha | | | | | | | | | |
| RVAlpha | | | | | | | | | |
| FlowConfirmedRV | | | | | | | | | |
| CrossAssetLead | | | | | | | | | |

---

## 35. Decision Logic

After experiments, classify every alpha:

| Result | Classification |
|---|---|
| predicts returns and survives factors | true return alpha |
| predicts returns only intraday | stale-mark / microstructure alpha |
| predicts initial move then reversal | liquidity-pressure alpha |
| predicts only filled-trade markout | execution / selection alpha, not pure return alpha |
| no OOS lift | reject or keep only as control |

The highest-value alpha for your anonymous setup is likely:

```text
FlowConfirmedRV
```

or:

```text
NeighborFlowAlpha + CottonFlowAlpha
```

because sparse individual-bond RFQ flow usually needs both cross-sectional pooling and economic scaling.

