# Skill — SYSTEM STRUCTURE MAPPER

**Type:** structure-mapping skill. Runs BEFORE the Causal Theme Compiler: it maps the WHOLE
system (boundary, stocks, flows, loops, delays) so the compiler can then distil ONE depth-first
causal chain with operational axes from it. **Does NOT recommend a trade** — it builds the map
later agents price.

## Provenance (method reference, not reproduced content)
- **Meadows, *Thinking in Systems: A Primer*** — a system = elements + interconnections +
  function/purpose; stocks vs flows; reinforcing vs balancing loops; delays; "systems surprise
  us" through structure, loop dominance shifts, and policy resistance; the system's real goal
  can differ from its stated goal. Source-derived (method, not summary).
- **Engine grounding (this repo):** the map's tradeable nodes must terminate in *operational
  axes* (named computable spreads/ratios — the Causal Theme Compiler / `CausalNode` contract),
  and any reflexive link becomes a `feedback=True` edge downstream. Not a source; the consumer.

---

## Skill Card

**skill_name:** system_structure_mapper

**purpose:** Convert a market theme into an explicit system map — boundary, elements,
interconnections, function, stocks, flows, feedback loops, delays, external shocks, internal
responses, observable variables, and the data to track it over time — so downstream agents can
extract priceable causal chains and anticipate how the system will surprise.

**when_to_use:** When a theme spans MULTIPLE issuers/instruments/intermediaries and "what
connects to what" is non-obvious; before causal compilation; whenever a PM says "ecosystem,"
"complex," "new market," or "everything is connected."

**input_schema:**
```
{
  "theme_id": str,
  "statement": str,                 # the theme to map
  "named_entities": [str],          # issuers/instruments/intermediaries mentioned
  "horizon": str|null
}
```

**output_schema:**
```
{
  "theme_id": str,
  "system_boundary": {"inside": [str], "outside_drivers": [str], "rationale": str},
  "function_or_purpose": {"stated": str, "revealed": str},   # Meadows: stated vs real goal
  "elements": [ {"id": str, "name": str, "type": "issuer|instrument|index|vehicle|intermediary|real_asset"} ],
  "interconnections": [ {"from": str, "to": str, "kind": "capital_flow|spread_relation|index_rule|ownership|physical", "observable": str|null} ],
  "stocks": [ {"name": str, "unit": str, "observable": str|null} ],
  "flows": [ {"name": str, "into_out_of_stock": str, "unit_per_time": str, "observable": str|null} ],
  "feedback_loops": [ {"id": str, "type": "reinforcing|balancing", "path": [str], "delay": str, "dominant_when": str} ],
  "delays": [ {"between": str, "length": str, "why_it_matters": str} ],
  "external_shocks": [str],
  "internal_responses": [str],
  "observable_variables": [str],
  "behavior_over_time_charts": [ {"series": str, "expected_shape": str} ],
  "surprise_modes": [str]
}
```

**system_boundary_rules:**
- Draw the boundary at the point where feedback loops effectively *close* — include what the
  system controls/responds to; push purely exogenous drivers to `outside_drivers`.
- Too wide = unmodellable; too narrow = the dominant loop is cut and the map lies. Justify the cut.
- The boundary is a CHOICE, not a fact (Meadows): state the rationale and what it excludes.

**element_identification_rules:**
- List the things that *hold a stock or carry a flow* (issuers, instruments, indices, vehicles,
  intermediaries, the underlying real asset). Tag each `type`.
- An "element" is not a number; it is a node that can accumulate (a stock) or transmit (a flow).

**interconnection_rules:**
- Every interconnection is either a **flow of capital/physical thing** or an **information/price
  link** (a spread relationship, an index rule, ownership). Attach an `observable` where one exists.
- Information links (rules, narratives, prices) are the usual sites of leverage AND of surprise.

**stock_flow_template:**
```
Stock  = an accumulation (a level): outstanding debt, installed GPU base, DC capacity,
         index/ETF AUM, dealer inventory, refi wall. Changes only via flows.
Flow   = a rate (per unit time): new issuance/qtr, capex spend/qtr, depreciation/yr,
         ETF creation-redemption/day, defaults/yr.
Rule:  bullish/bearish dynamics differ by whether the DRIVER is a stock or a flow
       (a rising flow can coexist with a deteriorating stock).
```

**feedback_loop_template:**
```
Reinforcing (R): X -> ... -> more X  (growth or collapse; e.g. capex->compute->revenue->capex)
Balancing  (B): X -> ... -> less X   (stabilises/limits; e.g. wide spread->higher funding cost->less issuance)
For each: path (node sequence), the DELAY around the loop, and which loop DOMINATES when.
Reflexive market loops (price -> belief -> price) are R loops and become feedback=True edges.
```

**delay_template:**
```
For each delay: {between A and B}, {length}, {why it matters}.
Delays cause overshoot, oscillation, and late-breaking surprises; a thesis must survive the
driver->axis delay (capex now, cashflows/defaults later).
```

**behavior_over_time_variables:** the handful of series whose *shape over time* (not level)
reveals which loop is winning — plot these, not point estimates.

**market_data_requirements:** the concrete series (with source/frequency) needed to instantiate
each stock, flow, interconnection, and BOT chart; flag any that are non-identifiable today.

---

## example_output — applied theme
**Theme:** *"AI capex funding is creating a credit ecosystem across hyperscalers, data-center
project bonds, HY HPC bonds, indices, ETFs, and private/neocloud intermediaries."*
*(All quantities are PM_assumption or model_required; this map names structure, not values.)*

### 1. System boundary
- **inside:** hyperscaler IG issuers; data-center project/ABS SPVs; HY HPC/neocloud issuers;
  the IG/HY indices that include them; credit ETFs (LQD/HYG/sector); private-credit & neocloud
  intermediaries; the underlying real assets (data centers, GPUs, power contracts).
- **outside_drivers (exogenous):** AI end-demand, policy rates, GPU supply / export controls,
  power & grid availability, the equity/AI-vol regime.
- **rationale:** the boundary closes where credit *funding* feeds back on credit *spreads* via
  issuance and index/ETF flows. AI demand and power are pushed outside: they shock the system but
  the system does not control them (cutting them would hide the dominant reinforcing loop).

### 2. Elements
issuer: hyperscalers (IG), HY HPC/neocloud · instrument: data-center project bonds/ABS, senior
CDS · index: IG & HY credit indices · vehicle: credit ETFs, CLOs · intermediary: private-credit
funds, neocloud lessors · real_asset: data-center capacity, installed GPU base, power PPAs.

### 3. Interconnections
- hyperscaler capex → data-center build (capital_flow; obs: capex guidance) →
- data-center SPV issuance → project-bond market (capital_flow; obs: issuance calendar) →
- new issuers → index inclusion (index_rule; obs: index composition) →
- index → ETF holdings → ETF flows (ownership/flow; obs: ETF creation-redemption) →
- spread relations: `HY HPC OAS − hyperscaler IG OAS`, `project-bond OAS − hyperscaler IG OAS`
  (spread_relation; obs: OAS series) ·
- neocloud intermediaries ← private credit funding (capital_flow) ; GPU lease ← installed base (physical).

### 4. Stocks and flows
- **Stocks:** outstanding AI-credit debt (USD); installed GPU base (units/$); data-center
  capacity (MW); index/ETF AUM (USD); HY HPC refi wall (USD by year); dealer inventory.
- **Flows:** new issuance/qtr; capex spend/qtr; GPU depreciation/yr; ETF creation-redemption/day;
  defaults/yr; index rebalance/month. *(A rising issuance FLOW can coexist with a worsening
  credit-quality STOCK — the core stock/flow trap.)*

### 5. Reinforcing loops (R)
- **R1 capex→compute→revenue→capex** (delay 18–36m): AI revenue funds more capex → more issuance.
- **R2 narrative→inclusion→tightening→issuance→bigger index weight→more forced buying** (delay
  ≈ monthly rebalance): the reflexive index/ETF loop — *spreads tighten because they're being
  bought because they tightened.* (becomes a `feedback=True` edge downstream.)

### 6. Balancing loops (B)
- **B1 supply indigestion** (delay weeks): heavy issuance → concession → wider spreads → demand
  returns / issuance pauses.
- **B2 funding-cost brake** (delay ≈ refi wall): wider HY HPC spread → higher funding cost →
  impaired credit / less issuance (can flip to a death-spiral R loop if it overshoots).
- **B3 power/physical limit**: capex → capacity build → grid/power constraint caps utilisation.

### 7. Delays
- capex → revenue: **18–36m** (thesis must survive it).
- issuance → index inclusion → ETF buying: **~monthly** (drives R2 surprise).
- GPU purchase → obsolescence/residual fall: **~1–3y** (recovery-assumption risk).
- default → recovery realisation: **months–years** (carry looks fine until it doesn't).

### 8. Observable market variables
OAS series for each leg + the two differentials; issuance calendar; index composition & weights;
ETF AUM and creation-redemption; data-center utilisation / PPA renewals; GPU resale-price index;
HY HPC refi-wall schedule; dealer inventory / bid-offer (liquidity).

### 9. How the system might surprise investors
- **R2 reverses:** a mega-issuer becomes a huge index weight; forced ETF/index buying *masks*
  deterioration until a downgrade forces selling — a sharp, non-linear snap.
- **Shared-factor illusion:** hyperscaler IG, project bonds, and HY HPC look like independent
  bets but all load on ONE AI-funding factor → "diversification" vanishes in a drawdown.
- **Stock/flow trap:** investors cheer the rising issuance FLOW while the credit-quality STOCK
  erodes; the turn is invisible in flow data.
- **Binding constraint nobody priced:** power/grid (an external shock × B3) caps the real-asset
  cashflows the whole credit complex rests on.
- **Intermediary cascade:** a neocloud/private-credit lessor default transmits through GPU-lease
  links faster than the public-bond map suggests.

### 10. Behavior-over-time charts to plot (shape, not level)
- `HY HPC OAS − hyperscaler IG OAS` and `project-bond OAS − hyperscaler IG OAS` (dispersion: widening vs compressing).
- AI-credit issuance/qtr (the FLOW) vs outstanding AI-credit debt (the STOCK) on one panel.
- Index AI-weight % and ETF AUM over time (R2 loop strength).
- GPU resale-price index and data-center utilisation (the real-asset stocks).
- HY HPC refi-wall by year (the balancing-loop trigger).

---
**Standing reminder:** this skill builds the system map only. It names structure, loops, delays,
and observables — it does NOT price, size, or recommend a trade. The Causal Theme Compiler and
pricing agents consume this map next.
