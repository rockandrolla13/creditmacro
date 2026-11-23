---
skill_name: system-mapper
access_class: method
pipeline_phase: discovery_system_map
provider_seam: [LLMProvider.build_system_map, Provider.build_system_map]
input_objects: [CausalChain, operational_axes, source_evidence, method_context]
output_objects: [SystemMap, Stock, Flow, FeedbackLoop, Delay, behavior_over_time_variables, observable_variables]
gates_created: [stock_vs_flow_distinction, not_everything_is_a_loop, name_the_system_boundary]
allowed_to_influence: [system structure, stock/flow identification, loop taxonomy, delay identification, observable variables]
not_allowed_to_influence: [pricing, sizing, expressions, numerical simulation, scenario probabilities]
failure_modes: [stock/flow confusion, loop-everything, missing the system boundary, inventing variables not in evidence]
tests: [test_system_map_issuance_is_flow_debt_is_stock, test_system_map_reinforcing_loop_present]
---

# System Mapper

> **Compiled from** *Thinking in Systems* (Meadows): stocks, flows, balancing (B) and
> reinforcing (R) feedback, delays, and system boundary — **supplemented** with the
> rate→economy→asset *transmission mechanism* as a stock/flow system from *Monetary Policy after
> the Great Recession* (Sieroń, channel taxonomy) and *Monetary Policy in Times of Crisis*
> (Rostagno/Altavilla, the duration / portfolio-rebalancing *mechanism* only — NOT its dated
> decision log). METHOD card: no case conclusions, no trades, no dated policy calls.

## Purpose
Convert a causal object into a **system map**: elements, interconnections, function/purpose,
stocks, flows, feedback loops, delays, and observable behaviour-over-time.

## Process primitives (paraphrased from Meadows)
- A **stock** is a level — an accumulation measurable at an instant (the memory of the system).
- A **flow** is a rate — a change-over-time that fills or drains a stock. *Misclassifying these
  is the central error.*
- **Balancing (B)** loops are goal-seeking / stabilising; they oppose imposed change and produce
  "homing" behaviour. **Reinforcing (R)** loops are self-enhancing; they produce exponential
  growth or runaway collapse. "System structure is the source of system behaviour."
- **Delays** in a balancing loop make a system oscillate / overshoot — flag them.
- Name the **system boundary** (what's inside vs outside); boundaries are problem-dependent.

## When to use
After a causal chain is built, in Phase A — to expose accumulation dynamics and loops the linear
chain hides.

## Inputs
Causal chain, operational axes, source evidence, method memory.

## Outputs
`SystemMap`, `Stock[]`, `Flow[]`, `FeedbackLoop[]`, `Delay[]`, behavior-over-time variables,
observable variables.

## Required fields
System boundary; elements; interconnections; purpose/function; ≥1 stock if accumulation exists;
≥1 flow if change-over-time exists; feedback loops where applicable; delays where applicable.

## Validation rules
- Distinguish stocks (levels, measurable at an instant) from flows (rates over time).
- Do not describe everything as a feedback loop.
- If there are no meaningful stocks/flows, say so explicitly.
- Use source-derived variables where available.

## Failure / blocked states
- No accumulation and no rate → report "no meaningful stock/flow structure" (still a valid map).
- A claimed loop with no closing path → drop it (not every arrow is a loop).

## Example output (AI-credit illustration)
- Stocks: outstanding DC/compute debt, index ownership, investor positioning, DC capacity.
- Flows: new issuance, ETF/fund inflows, index-inclusion changes, secondary liquidity.
- Loop R: performance → attention/inflows → spread tightening → more performance.
- Loop B: issuance growth → cheapening → reduced demand / higher concession.
- Delays: index-inclusion lag, construction/completion lag, secondary-liquidity lag.

## Supplement — rate→economy→asset transmission as a stock/flow system
Monetary transmission is itself a stocks/flows/feedback system; map it the same way (mechanism
only, no dated policy calls):
- **The chain.** policy rate (a set *level*) → market / long-term rates (the link is *loose*, not
  rigid — term premium, inflation expectations and risk premia sit in between) → **asset prices**
  (Tobin's-q, wealth effect, portfolio-balance) → **bank credit** (bank-lending and balance-sheet
  channels) → spending / investment / output. Named **channels**: interest-rate, credit
  (bank-lending + balance-sheet), asset-price (exchange-rate / Tobin's-q / wealth effect),
  risk-taking (search-for-yield), and portfolio-balance / **duration** channel.
- **Stocks vs flows.** Outstanding credit/loans, bank reserves, and the **aggregate stock of
  duration (interest-rate) risk** held by the market are *stocks* (levels). New **issuance**,
  lending, deposit creation, fund inflows, and central-bank purchases are *flows* that fill or
  drain them. Beware reverse causation vs the textbook: credit demand and deposit creation can
  drive reserves, not the other way round (banks create deposits in the act of lending) — so a
  reserves *flow* need not move the credit *stock*.
- **Duration / portfolio-rebalancing mechanism (stock view).** Purchases that extract duration
  risk shrink the *stock* of interest-rate risk the market must bear, compressing the term premium
  and propagating across maturities and risky assets as freed risk-bearing capacity is redeployed.
  It is the held stock relative to outstanding — not the act of buying — that sets the premium.
- **Feedback loops & delays.** R: lower rates → reach-for-yield → higher asset prices / risk
  tolerance → more risk-taking (self-reinforcing). B with **delay**: easy policy → credit growth
  → later fragility / overshoot (a delayed, oscillation-prone balancing loop). A
  sovereign↔bank↔firm "doom loop" is a vicious-circle (reinforcing-toward-collapse) structure.

## Non-goals
No ODE simulation, no numerical solver, no trades, no sizing.
