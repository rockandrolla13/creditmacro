# Skill: CAUSAL THEME COMPILER

> A process skill for an investment-research agent. It converts ONE raw
> investment sentence into ONE causal **Theme Object** whose terminal nodes carry
> **operational axes** (named, computable spreads/ratios) so a downstream pricing
> engine (Engine 2) can consume it directly. It fuses Pearl's causal ladder with
> Meadows' systems structure. It builds a falsifiable causal map — it does **not**
> select, size, or recommend a trade.

---

## Source provenance (what is source-derived vs. standard-framework)

| Concept used in this skill | Where it comes from |
|---|---|
| Causal ladder: association → intervention (do-operator) → counterfactual; "seeing ≠ doing"; confounders | **Source-derived.** Pearl, *The Book of Why* (`markdowns/The Book of Why ....md`) — present in repo. (The brief named "Super Thinker / causal ladder" primer is in the repo as `markdowns/Thinking in Systems and Mental Models ... (Marcus P. Dawson).md` but its text is a generic mental-models primer; the *ladder* content is Pearl's, so Pearl is cited.) |
| Stock vs flow; reinforcing vs balancing loops; delays; shifting dominance; leverage points | **Source-derived.** Meadows, *Thinking in Systems: A Primer* (`markdowns/Thinking in Systems A Primer (Meadows...).md`). |
| Operational axis = a *named spread/slope with a real historical time series*; theme → valuation → expression discipline | **Source-derived.** `markdowns/Alaph Long Presentation Version July 2014.md` (the French-banks worked trade: axis = "senior CDS spread of French banks − French sovereign"). |
| Liquidity scoring of an axis (bid/offer, volume, trade frequency, clearing breadth, vol) | **Source-derived.** `markdowns/XantimumBizPlan.md`. |
| Theme → instrument taxonomy ("Theme-Ometer / Theme Machine") | **Source-derived in concept, not in text.** `markdowns/citi global theme book.md` is **image-only** in the converted markdown (no extractable prose); the taxonomy is used as described in the project CLAUDE.md. |
| The credit risk premium as a STANDING confounder (spread ≠ mispricing) | **Standard-framework knowledge**, anchored to the Alaph "current market pricing (risk premium)" step. |

---

## SKILL CARD

### skill_name
`causal_theme_compiler`

### purpose
Force the agent, in a fixed 11-step order, to turn one research sentence into one
*depth-first* causal chain (NOT a tree) terminating in operational axes, plus the
assumptions, confounders, feedback loops, the shared latent factor, testable
implications, and the residual non-identifiability that must be handed to the PM.
The output is a typed Theme Object, not a trade.

### when_to_use
- A raw thesis sentence has arrived (Stage-0 `CandidateTheme`) and must become a
  `ThemeObject` axis before Engine 2 can price it.
- You need to check whether a narrative actually *terminates in a computable
  series* (the Engine-1 discipline gate: "axis is OPERATIONAL").
- You need to know whether several themes are secretly one bet (shared factor).
- **Do not use** to choose/size/route a trade — this skill stops at the Theme Object.

### input_schema
```json
{
  "sentence": "string  // the raw investment thesis, one sentence",
  "horizon": "string   // e.g. '1-3m', '3-12m' — sets which loops/delays matter",
  "universe_hint": "string|null  // optional asset-class hint",
  "sources": ["string  // optional citations the agent may tag inferred=False against"]
}
```

### output_schema
```json
{
  "main_theme": {"statement": "string", "axis": "string  // named computable spread/ratio"},
  "causal_chain": [
    {
      "node": "string",
      "kind": "driver|mechanism|theme",
      "axis": "string|null  // operational axis ONLY for tradeable theme nodes; null otherwise",
      "edge_mechanism": "string  // the incoming edge: how the predecessor causes this node",
      "inferred": "bool  // true = agent-derived edge; false = stated in a source"
    }
  ],
  "shared_factor": "string",
  "assumptions": ["string"],
  "confounders": ["string"],
  "non_identifiability": ["string"],
  "data_requirements": ["string"]
}
```

### causal_graph_template
A single spine (depth-first), drawn as `node --[edge, inferred?]--> node`, with
feedback links drawn as back-edges and tagged `(reflexive/reinforcing/balancing,
lag=…)`:
```
ROOT_DRIVER
  --[transmission edge]--> MECHANISM(axis=None)
  --[transmission edge]--> THEME_1(axis="… spread, bps")
  --[transmission edge]--> THEME_2(axis="… spread, bps")
  --[transmission edge]--> THEME_N(axis="… spread, bps")   # terminal
  --[transmission edge]--> MECHANISM_DEADEND(axis=None)     # dead end is VALID
FEEDBACK: THEME_k --[reflexive, lag=…]--> earlier_node
```

### required_variables
For every `theme` node: (1) a named numerator leg and denominator/benchmark leg;
(2) the unit (bps or ratio); (3) the matching control that nets the standing
confounder (duration-/rating-/sector-matched). For the chain: the FLOW variable,
the STOCK variable, and the shared-factor proxy.

### assumptions_required (Step 4)
At minimum, state and flag each: (a) the transmission edge is causal at `horizon`,
not just correlational; (b) the standing credit-risk-premium confounder is netted
by the axis construction; (c) the buckets load on a common factor (so RV is
meaningful); (d) the axis legs are *live* (priced often enough to form a series).

### confounders_to_check (Step 5)
**STANDING confounder, always present: the credit risk premium — a wider spread is
not by itself a mispricing.** Then: aggregate market beta; rates/duration; rating
migration & index up/down-grade flows; sector beta; liquidity premium differences
(Xantimum); equity/vol regime; issuer-specific structure.

### mediators_to_check (Step 6)
List the transmission chain links between driver and the priced node. Each link is
either promoted to a `theme` (it has an axis) or stays a `mechanism` (axis=None).

### feedback_loops_to_check (Step 7)
- **Reflexive index-inclusion loop** (the canonical one): heavy issuance → bond
  becomes large index constituent → forced index buying → spread tightens,
  *reversing* the initial supply-cheapening. Mark `reflexive`, note the rebalance lag.
- **Reinforcing (Meadows capital loop):** capex → output → revenue → capex.
- **Balancing / refinancing death-spiral:** wider spread → higher funding cost →
  impaired credit → wider spread. Always tag the **delay**.

### stock_flow_classification (Step 8)
Separate the **FLOW** (a *rate*: new issuance per quarter) from the **STOCK** (a
*level*: outstanding debt). Meadows' warning: a spread move driven by a flow shock
(new-issue concession) mean-reverts; do not mistake it for a permanent stock repricing.

### shared_factor (Step 9)
Name the single latent factor the whole chain loads on, and give a computable
proxy (e.g. first PC of OAS changes across the complex, or an AI-capex equity
basket). Purpose: prevent correlated nodes being booked as independent bets.

### testable_implications (Step 10)
Produce event-study, cross-sectional-beta, lead-lag (Granger), do-style
intervention, and counterfactual predictions — each refutable on the axis series.

### data_requirements
Every axis leg's OAS/CDS history; the issuance calendar (FLOW); index membership +
rebalance schedule (for the reflexive loop); rating histories; Xantimum liquidity
metrics per leg; maturity/refi walls; the shared-factor proxy series.

### non_identifiability (Step 11 → hand to PM)
What observational data cannot resolve: confounders with no instrument; loops whose
sign flips at an unknown lag; small-N / short-history legs; stale-mark (liveness) legs.

### failure_modes
- **Inventing an axis to extend the chain.** A node with no real series stays
  `mechanism, axis=None`; **a dead end is a valid result.** Never fabricate a series.
- Building a tree instead of one depth-first spine.
- Quoting a spread *level* as the axis without the netting leg → standing confounder leaks in.
- Treating an issuance-flow spike as a permanent stock repricing.
- Tagging a derived edge `inferred=False` (provenance inflation).
- Emitting a chain with no testable implication / no falsifier.

### questions_for_PM
The `non_identifiability` items, phrased as decisions: which leg's liveness to
accept, whether to trade through the reflexive lag, whether small-N is acceptable.

### example_output
See the applied example below (sentence: AI capex funding & relative value).

---

## Method (the 11 forced steps)

1. **Association** — state the bare correlation the sentence asserts (rung 1, "seeing").
2. **Intervention** — restate as `do(X)`: if we *forced* the driver, what moves? (rung 2).
3. **Counterfactual** — absent the driver, what would the axis do? (rung 3).
4. **Causal assumptions** — write the edges you are *assuming* are causal.
5. **Confounders** — list them; the credit risk premium is STANDING (spread ≠ mispricing);
   build each axis as a *differential* that nets it.
6. **Mediators / transmission chain** — lay the depth-first spine; promote a link to a
   `theme` only if it has an operational axis, else leave it `mechanism, axis=None`.
7. **Feedback & delays** — mark reflexive / reinforcing / balancing back-edges + lags.
8. **Stock vs flow** — tag the FLOW and the STOCK; flag flow-shock mean reversion.
9. **Shared factor** — name the latent factor + proxy; check the nodes aren't one bet.
10. **Testable implications** — refutable predictions on the axis series.
11. **Non-identifiability** — what data cannot settle → hand to PM. Then emit the JSON.

---

# APPLIED EXAMPLE

**Input sentence:** *"AI capex funding will change relative value across hyperscaler
bonds, data-center project bonds, and HY HPC issuers."*
**Horizon:** 3–12m.

### Walkthrough (steps 1–3, condensed)
- **Association:** as AI capex is increasingly debt-funded, OAS *differentials*
  across the three buckets co-move with the pace and mix of that funding.
- **Intervention `do(·)`:** if we forced the marginal AI-capex dollar to be funded
  by debt (vs equity/internal cash), new-issue supply rises and the
  cheapest-to-fund bucket's OAS differential widens *first*. Forcing an equity raise
  instead would compress it. (Seeing the differential widen ≠ AI-supply causing it;
  it could be market beta — hence the netting legs below.)
- **Counterfactual:** absent AI capex, cross-sectional OAS dispersion across these
  names would track the TMT-sector baseline, not blow out.

## 1. Causal graph (TEXT)

```
N1  AI compute-demand growth  [driver, axis=None]
      --[root driver (exogenous secular demand); inferred=False (consensus/JPM)]-->
N2  AI capex funding-mix shift: marginal dollar moves from internal cash/equity
    to DEBT; new-issue FLOW rises  [mechanism, axis=None]
      --[debt substitution raises bond supply across the complex; inferred=False
         (JPM AI Capex Funding note)]-->
N3  Hyperscaler IG "AI supply premium": new-issue concession cheapens
    hyperscaler curves vs the broad IG index  [theme,
    axis="hyperscaler IG OAS − duration-matched IG index OAS, bps"]
      --[supply/new-issue-concession channel; inferred=True]-->
N4  Data-center project/SPV "structure premium": single-asset, secured,
    less-liquid project bonds must pay up vs hyperscaler senior unsecured  [theme,
    axis="data-center project/ABS bond OAS − hyperscaler senior IG OAS, bps"]
      --[funding substitution + structural subordination/illiquidity; inferred=True]-->
N5  HY HPC / neocloud "AI-beta": GPU-backed HY issuers' spread vs the HY index is
    the most sensitive to the marginal AI funding cost  [theme,  TERMINAL
    axis="HY HPC issuer OAS − BB/B HY index OAS, bps"]
      --[down-the-quality-ladder funding transmission; inferred=True]-->
N6  GPU residual-value / depreciation-schedule uncertainty  [mechanism, axis=None]
      --[affects all three buckets but has NO liquid traded spread → axis=None;
         DEAD END is a valid result, no axis invented; inferred=True]

FEEDBACK LINKS:
F1 (reflexive, lag≈monthly rebalance):
   N3 --> N2 : hyperscaler mega-issuance → bonds become large IG-index constituents
   → forced index buying → OAS tightens, REVERSING the initial N3 widening.
F2 (reinforcing, lag≈18–36m build-out):
   N1 <-- (capex→compute→AI revenue→capex) Meadows capital-accumulation loop.
F3 (balancing / death-spiral, lag≈refi-wall timing):
   N5 --> N5 : wider HY HPC spread → higher funding cost → impaired capex/credit
   → wider spread.
```

## 2. JSON Theme Object

```json
{
  "main_theme": {
    "statement": "Debt-funding of AI capex re-prices relative value across the AI-credit complex; the marginal funding mix and issuance flow drive OAS differentials between hyperscaler IG, data-center project bonds, and HY HPC issuers.",
    "axis": "AI-credit dispersion = HY HPC issuer OAS - hyperscaler IG OAS, duration- and rating-adjusted, bps"
  },
  "causal_chain": [
    {
      "node": "AI compute-demand growth",
      "kind": "driver",
      "axis": null,
      "edge_mechanism": "Root exogenous driver: secular demand for AI compute.",
      "inferred": false
    },
    {
      "node": "AI capex funding-mix shift to debt (new-issue FLOW rises)",
      "kind": "mechanism",
      "axis": null,
      "edge_mechanism": "Capex outgrows internal cash/equity; marginal dollar funded with bonds, lifting issuance supply across the complex.",
      "inferred": false
    },
    {
      "node": "Hyperscaler IG AI supply premium",
      "kind": "theme",
      "axis": "hyperscaler IG OAS - duration-matched IG index OAS, bps",
      "edge_mechanism": "Heavy primary supply forces new-issue concession, cheapening hyperscaler curves vs the broad IG index.",
      "inferred": true
    },
    {
      "node": "Data-center project/SPV structure premium",
      "kind": "theme",
      "axis": "data-center project/ABS bond OAS - hyperscaler senior unsecured IG OAS, bps",
      "edge_mechanism": "Funding substitution plus single-asset secured structure and weaker secondary liquidity force project bonds to pay up vs hyperscaler senior unsecured.",
      "inferred": true
    },
    {
      "node": "HY HPC / neocloud AI-beta",
      "kind": "theme",
      "axis": "HY HPC issuer OAS - BB/B HY index OAS, bps",
      "edge_mechanism": "Down-the-quality-ladder transmission: GPU-backed HY issuers' funding cost is the most sensitive to the marginal AI funding dollar.",
      "inferred": true
    },
    {
      "node": "GPU residual-value / depreciation-schedule uncertainty",
      "kind": "mechanism",
      "axis": null,
      "edge_mechanism": "Affects all three buckets' credit quality but has no liquid traded spread; no axis invented - valid dead end.",
      "inferred": true
    }
  ],
  "shared_factor": "AI-capex funding-cost / risk-appetite factor ('AI credit beta'): one latent factor on which all three buckets load with differing sensitivities (hyperscaler lowest, HY HPC highest). Proxy: first principal component of OAS changes across the AI-credit complex, or an AI-capex equity basket (semis + data-center REITs). Because all nodes load on it, a long-hyperscaler / short-HY-HPC RV position is a bet on the factor's loading slope (dispersion), NOT three independent bets.",
  "assumptions": [
    "The issuance-supply channel is causal at 3-12m, not fully arbitraged away.",
    "Each axis differential nets the standing credit-risk-premium confounder via duration/rating/sector matching (spread != mispricing).",
    "The three buckets share one AI-funding factor, so cross-sectional relative value is well defined.",
    "Index-inclusion rules are stable over the horizon (else the reflexive loop F1 changes sign/strength).",
    "Data-center project bonds and HY HPC names are priced frequently enough to form a usable time series (liveness).",
    "The reinforcing capex->revenue->capex loop (F2) is not yet saturated over the horizon."
  ],
  "confounders": [
    "STANDING: the credit risk premium - a wider differential may be fair compensation, not AI mispricing.",
    "Aggregate market/credit beta: all AI-credit spreads co-move with broad IG/HY; net out via duration-matched index legs.",
    "Rates / duration: heavy long-end IG supply interacts with rate moves even after OAS adjustment.",
    "Rating migration and index up/down-grade (fallen-angel / rising-star) flows unrelated to AI.",
    "TMT sector beta vs AI-specific repricing.",
    "Liquidity premium differences across buckets (Xantimum scoring) masquerading as AI alpha.",
    "Equity/vol regime jointly driving both funding behaviour and spreads."
  ],
  "non_identifiability": [
    "Cannot separate the AI-supply premium from general TMT-sector repricing with observational data alone (no clean instrument).",
    "The reflexive index-inclusion loop (F1) can flip the sign of the supply effect at an unknown lag - direction not point-identified.",
    "HY HPC issuers are few, short-history, and structurally idiosyncratic (GPU-backed SPVs) - factor cannot be cleanly separated from name-specific risk (small-N).",
    "Data-center project bonds have thin secondary liquidity, so the axis may be a stale mark rather than a live tradeable series (liveness risk)."
  ],
  "data_requirements": [
    "OAS history: hyperscaler IG names, duration-matched IG index, data-center project/ABS bonds, HY HPC issuers, BB/B HY index.",
    "Primary issuance calendar / flow by issuer (the FLOW variable).",
    "Index membership and rebalance schedule (for reflexive loop F1).",
    "Rating histories for all legs.",
    "Xantimum liquidity metrics per leg (bid/offer, volume, trade frequency, clearing breadth).",
    "Maturity / refinancing walls for HY HPC issuers (for death-spiral loop F3).",
    "Shared-factor proxy series (first PC of complex OAS changes, or AI-capex equity basket)."
  ]
}
```

## 3. Assumptions
See `assumptions[]` above. The load-bearing ones: the **supply channel is causal**
at 3–12m; each axis **nets the standing credit-risk-premium confounder** by
construction (differentials, duration/rating-matched); and the three buckets
**share one AI-funding factor** so RV is meaningful rather than three separate bets.

## 4. Confounders
The **standing confounder is the credit risk premium**: a wider differential can be
fair compensation, not AI mispricing — which is *why every axis is a netted
differential, never a raw level*. Other confounders to strip: aggregate market/credit
beta, rates/duration, rating-migration & index flows, TMT sector beta, cross-bucket
liquidity premia (Xantimum), and the equity/vol regime.

## 5. Data needed before pricing
See `data_requirements[]`. Critically, before Engine 2 can price this: build the
**OAS differential series** for all five legs, the **issuance-flow** series (the
Meadows FLOW), the **index-rebalance schedule** (to model the reflexive loop), and a
**shared-factor proxy**. Two legs (data-center project bonds, HY HPC) require a
**liveness check** — confirm they are quoted often enough to form a real series, not
stale marks.

## 6. Decision
**`research_more`** — The chain is coherent, depth-first, and every tradeable node
terminates in a named computable axis (so it is structurally promotable). But the
**standing credit-risk-premium confounder is not yet empirically netted** (the OAS
differentials and shared factor must be built and estimated first), and **two
terminal legs have liveness / small-N doubts**. Resolve data liveness and confirm
spread ≠ AI-mispricing on real series before promoting to a `ThemeObject`.

---

*File written by the Causal Theme Compiler skill. It builds the causal Theme Object
only; it does not select, size, or recommend a trade.*
