# Skill — FEEDBACK, LEVERAGE POINT, AND SYSTEM TRAP DETECTOR

**Type:** behavior-diagnosis skill. Runs AFTER the System Structure Mapper and BEFORE the
scenario / pricing engine. It **CONSUMES the mapper's loop map** (`SystemMap.feedback_loops`,
`SystemMap.delays`, stocks/flows) and diagnoses *why the theme may accelerate, reverse,
overshoot, crowd, or fail*. It does **NOT re-derive loops** (the mapper already did) and it does
**NOT price, size, or recommend a trade** — it labels loop dynamics, names the traps, locates
leverage points, and hands the scenario engine the loop-state → fair-value mapping plus
falsifiers.

## Provenance (method reference, not reproduced content)
- **Meadows, *Thinking in Systems: A Primer*** — read as METHOD, not data. The source IS present
  in this repo: `markdowns/Thinking in Systems A Primer (Meadows, Donella H.) ...md` (and the
  matching PDF at repo root). Concepts used, source-derived: reinforcing vs balancing loops;
  *limits to growth* (a reinforcing loop ALWAYS eventually meets a balancing loop, ch. on the
  systems zoo); **delays in a balancing loop cause overshoot and oscillation**; the system-trap
  archetypes — *success to the successful* (competitive exclusion / "the rich get richer"),
  *escalation* ("I'll raise you one"), *drift to low performance* (the boiled-frog erosion of
  goals), policy resistance, tragedy of the commons, seeking the wrong goal; and the **12
  leverage points in increasing order of effectiveness** (numbers → buffers → stock/flow
  structure → delays → balancing loops → reinforcing loops → information flows → rules →
  self-organization → goals → paradigms → transcending paradigms). The famous corollary: people
  intuit leverage points but "push in the wrong direction."
- **Engine grounding (this repo):** consumes `engine/schema.py:SystemMap` and its
  `FeedbackLoop` (`id`, `type ∈ {reinforcing, balancing}`, `path: list[str]`, `delay`,
  `closes_via`), `Delay` (`between`, `length`, `why_it_matters`), `Stock`/`Flow`. NOW WIRED as
  the live **TRAP stage** (`engine/workflow.py`, after `SYSTEM_MAP`/`CRITIQUE`, before pricing):
  emits `engine/schema.py:TrapDetection` via the `Provider.detect_traps(system_map)` seam
  (`ScriptedProvider` from the case; `LLMProvider` later), recorded on the `ThemeObject`.
  Its `scenario_implications` feed `Scenario.implied_axis_value`; its `invalidation_evidence`
  feed `Falsifier`; its crowding verdict is consistent with the pre-screen's
  `−attention_score` term (`schema.py:CandidateTheme.pre_screen_score = evidence − attention`)
  and with `Pricing.edge_basis = "gross_of_risk_premium"`. Not a source — the consumer.

---

## Skill Card

**skill_name:** feedback_leverage_trap_detector

**purpose:** Given a Theme Object / candidate and its already-built system map, diagnose the
loop dynamics that govern whether the theme accelerates, reverses, overshoots, crowds, or fails:
identify the dominant loop now, the condition under which R↔B dominance flips, the delays that
make investors late, the Meadows system traps the structure is prone to (especially the
crowding signature, *success to the successful*), the leverage points where a small change most
alters behavior, the early-warning series that move BEFORE the shift, and the mapping from each
loop state to upstream scenario fair values and expression-family risk. Ends with a promote /
watchlist / reject / needs-more-data decision.

**when_to_use:** Immediately AFTER the System Structure Mapper (it requires
`SystemMap.feedback_loops`) and BEFORE scenario pricing; whenever a theme is described as
"momentum," "everyone's in it," "crowded," "it keeps tightening," "parabolic," "consensus,"
"too good to be true," or has outperformed sharply; whenever a candidate carries a high
`attention_score` and you must decide whether it is already priced.

**input_schema:** (CONSUMES the mapper's `SystemMap`; shape matches `engine/schema.py`)
```
{
  "theme_id": str,
  "statement": str,
  "system_map": SystemMap,                # engine/schema.py:SystemMap — CONSUMED, not re-derived
                                          #   .feedback_loops: [FeedbackLoop{id,type,path,delay,closes_via}]
                                          #   .delays:         [Delay{between,length,why_it_matters}]
                                          #   .stocks/.flows, .surprise_modes, .observable_variables
  "axis": Axis|null,                      # operational axis if one already exists (gates "promote")
  "attention_score": float,               # from CandidateTheme — the consensus/crowding prior (q-side)
  "evidence_score": float,                # from CandidateTheme — factual support (p-side)
  "horizon": str|null
}
```

**output_schema:** (the diagnosis fields — exactly these)
```
{
  "theme_id": str,
  "feedback_loop_map": [ {"id": str, "type": "reinforcing|balancing", "path": [str],
                          "delay": str|null, "closes_via": str} ],   # FROM the mapper, not re-derived
  "dominant_loop_now": {"loop_id": str, "evidence": [str]},
  "possible_loop_shift": {"from_loop": str, "to_loop": str,
                          "reversal_condition": str, "reversal_point_observable": str|null},
  "delays": [ {"between": str, "length": str, "kind": "flow_to_stock|price_to_structure",
               "makes_investors_late_because": str} ],
  "system_traps": [ {"archetype": str, "why_this_theme": str, "signature_series": str|null,
                     "masks": str|null} ],
  "leverage_points": [ {"name": str, "meadows_rank": int, "small_change": str, "large_effect": str,
                        "tag": "observable_to_investors|structural"} ],
  "early_warning_indicators": [ {"series": str, "leads_what": str, "direction_of_warning": str} ],
  "scenario_implications": [ {"loop_state": str, "axis_direction": str,
                              "upstream_scenario_fv_effect": str} ],   # -> Scenario.implied_axis_value
  "expression_risk_implications": [ {"expression_family": str, "breaks_if": str, "order_of_death": int} ],
  "invalidation_evidence": [ {"claim": str, "observable": str, "threshold": str} ],   # -> Falsifier
  "PM_questions": [str],
  "decision": "promote_to_scenario_pricing|watchlist|reject|needs_more_data",
  "decision_reason": str
}
```
*Every numeric quantity below is tagged `PM_assumption` (a judgement the PM must supply) or
`model_required` (must be computed/estimated) — this skill names structure, not values.*

---

## trap_inventory (Meadows archetypes ⇒ market manifestation)
| Archetype | Loop structure | Market manifestation | Tell |
|---|---|---|---|
| **Success to the successful** | R: performance → inflows → more buying → performance | the crowding signature — winners attract capital that makes them keep winning, **masking rising fragility** | rising index weight + rising fund inflows + falling dispersion, while fundamentals flat/eroding |
| **Escalation** ("I'll raise you one") | R: competitor-relative goal | spread-compression / yield-reach race; capex arms race; carry pile-on | each actor's target set by the other's position, not by value |
| **Drift to low performance** | B with eroding goal | underwriting standards / covenant quality / liquidity slowly degrade; "new normal" lulls | goal references *recent* state not absolute; quality declines unnoticed |
| **Policy resistance / fixes that fail** | B vs. opposing B | spreads stuck despite issuance or intervention; CB/fiscal backstop offset by behaviour | big effort, little net change in the stock |
| **Tragedy of the commons** | R growth on shared erodable resource w/ delayed feedback | shared liquidity / dealer balance-sheet / a funding pool consumed until it snaps | individual incentive to add exposure; feedback from the commons is delayed |
| **Seeking the wrong goal** | B optimising mismeasured indicator | optimising carry / index inclusion / rating-arb instead of risk-adjusted value | "producing effort, not result"; metric ≠ welfare |
| **Limits to growth** | R that MUST meet a B | every momentum theme; name the B loop and its limit | the R loop visibly running; the B loop not yet binding |

## leverage_point_ladder (Meadows' 12, increasing effectiveness; tag for investors)
1. **(12) Numbers / parameters** — coupon, spread level, subsidy, tax — *observable, weak.*
2. **(11) Buffers** — dealer inventory, ETF cash, reserve/liquidity cushions — *observable.*
3. **(10) Stock-and-flow structure** — index-inclusion rules' plumbing, refi-wall shape — *structural.*
4. **(9) Delays** — the lag lengths themselves; shortening/lengthening one flips behaviour — *structural, high.*
5. **(8) Balancing-loop strength** — funding-cost brake, supply indigestion — *structural.*
6. **(7) Reinforcing-loop gain** — the inflow→performance gain; **weaken this to defuse a bubble** — *structural, high.*
7. **(6) Information flows** — who sees positioning / quality deterioration, and when — *partly observable.*
8. **(5) Rules** — index methodology, margin/haircut rules, rating triggers — *structural.*
9. **(4) Self-organization** — new instruments/vehicles that re-wire the system — *structural.*
10. **(3) Goals** — the system's actual purpose (max AUM? max carry?) — *structural, very high.*
11. **(2) Paradigms** — the consensus belief the whole theme rests on — *structural, highest practical.*
12. **(1) Transcending paradigms** — holding the narrative loosely.
> Meadows' warning encoded: investors fixate on the **observable, low-rank** points (numbers,
> buffers) and "push in the wrong direction"; the points that actually move behaviour
> (loop gain, delays, rules, goals, paradigm) are **structural** and usually unpriced. The
> *most investable EARLY WARNING* lives at ranks 6–9 (information flows, delays, balancing-loop
> strength) — they move before the price.

## loop_shift_rules (R ↔ B dominance — the reversal point)
- **Limits to growth (mandatory check):** for EVERY dominant reinforcing loop, NAME the
  balancing loop that must eventually meet it and NAME its limit (a stock running down, a
  constraint binding, a price reaching a level that re-activates B). A reinforcing loop with no
  named limiting B loop is an incomplete map — push back to the mapper, do not promote.
- **The shift is a dominance flip, not a new loop:** R and B coexist; behaviour changes when
  the B loop's gain overtakes the R loop's gain. State the `reversal_condition` as the inequality
  that flips (e.g. "marginal inflow < marginal supply," "funding cost > carry," "redemptions >
  creations").
- **Overshoot is structural, not bad luck (delays ⇒ violent reversal):** because the balancing
  loop acts with a DELAY, the system *overshoots* the level B would have held it at, then
  oscillates / snaps back. This is exactly why **crowded trades reverse violently, not
  smoothly** — by the time the B loop bites, the stock is far past equilibrium and the unwind is
  discontinuous. The longer the B-loop delay, the larger the overshoot and the more violent the
  reversal.
- **Success-to-the-successful masks the turn:** while R dominates, performance→inflows hides
  deteriorating fundamentals; dispersion compresses and realised vol falls *just before* peak
  fragility. Low vol + high crowding is a late-stage signal, not a safe one.
- **Already-priced rule (engine-consistent):** *high attention × reinforcing-loop dominance =
  likely ALREADY PRICED.* The consensus has paid for the R-loop continuation, so residual edge
  on "it keeps going" is small (mirrors `−attention_score` in the pre-screen and
  `edge_basis = gross_of_risk_premium`). Edge, if any, lives on the **reversal** (betting the B
  loop binds) or on a mispriced delay — not on more momentum.

## delay_rules (two delay kinds the scenario engine must respect)
- **flow_to_stock:** a flow has moved but its stock has not yet visibly changed (issuance up,
  but credit-quality stock still looks fine; inflows up, but the index hasn't rebalanced). The
  turn is **invisible in flow data** → investors extrapolate the flow and are late.
- **price_to_structure:** price/spread has moved but the structural cause (covenant erosion,
  refi wall, capacity constraint) hasn't yet transmitted. Price looks "confirmed" while the
  structure that will reverse it is already in place.
- **Rule:** for each `Delay` from the mapper, tag its kind and state *makes_investors_late_because*.
  A delay that is LONGER than the trade horizon is a hidden tail; a delay SHORTER than consensus
  expects is an early reversal risk. Delays are themselves a rank-9 leverage point.

## early_warning_template (series that move BEFORE the shift)
For each candidate shift, list a *leading* series, what it leads, and the warning direction:
```
{ "series": <observable from SystemMap.observable_variables>,
  "leads_what": <which loop-state change it precedes>,
  "direction_of_warning": <which move = the B loop starting to bind> }
```
Prefer rank 6–9 leverage-point series (information flows, buffers, delays, balancing-loop
strength) over the price itself — the price is the LAST thing to move. Canonical set for a
crowding reversal: net fund flows turning (creations→redemptions), dispersion widening off
lows, dealer inventory / buffer drawdown, new-issue concession re-appearing, the relevant
delay's stock finally moving.

## decision_rubric
- **promote_to_scenario_pricing** — ONLY IF (a) an OPERATIONAL axis exists (a named spread/slope
  with a real series) AND (b) evidence exceeds attention (`evidence_score > attention_score`,
  i.e. positive pre-screen) AND (c) the edge is on a *diagnosable, falsifiable* loop state (a
  named reversal condition or a mispriced delay), not on "more momentum."
- **watchlist** — a crowded, already-priced reinforcing loop with a real axis but
  `attention ≥ evidence`: the structure is understood but there is no residual edge yet; wait
  for the early-warning series to signal the B loop binding.
- **reject** — no named limiting balancing loop (incomplete map), OR no falsifier with an
  observable + threshold, OR the only thesis is "the R loop continues" with attention already
  high (no edge).
- **needs_more_data** — the loop dominance cannot be established because the deciding series
  (flows, dispersion, buffers) is non-identifiable today.

---

## example_output — applied (illustration, NOT baked into the engine)
**Generic input:** *a sector that has outperformed sharply and grown its index weight on a
performance → inflows → spread-tightening loop.* (No real tickers; every number is
`PM_assumption` or `model_required`. **No trade is recommended.**)

**feedback_loop_map** (FROM the mapper, consumed):
- `R1` reinforcing — `path: [outperformance → fund_inflows → forced/again buying → spread_tightening → outperformance]`, `delay: ~weekly–monthly (flow/rebalance)`, `closes_via: index-weight & ETF creation`.
- `B1` balancing — `path: [tight_spread → low_forward_return/carry → marginal_inflow_slows → buying_slows]`, `delay: months`, `closes_via: valuation/return exhaustion`.
- `B2` balancing — `path: [tight_spread → heavy_new_issuance/supply → concession → wider_spread]`, `delay: weeks`, `closes_via: supply indigestion`.
- `B3` balancing — `path: [inflows → bigger position → redemption_sensitivity → outflows_on_shock → forced_selling]`, `delay: event-driven`, `closes_via: liquidity/buffer exhaustion (can flip to a death-spiral R)`.

**dominant_loop_now:** `R1`. evidence: rising index weight, positive net inflows, compressing
dispersion, realised vol falling, fundamentals flat-to-eroding (the *success-to-the-successful*
signature). `model_required` to confirm flow and dispersion series.

**possible_loop_shift:** from `R1` to `B1`/`B3`. **reversal_condition:** *marginal inflow <
marginal supply* OR *forward carry < funding/hurdle* OR *creations turn to redemptions*.
reversal_point_observable: net fund flows crossing zero; dispersion turning up off its low.

**delays:**
- `inflows → index rebalance → forced buying` — ~monthly — **flow_to_stock** — investors
  extrapolate inflows; the weight change lags, so the loop looks self-sustaining longer than it is.
- `spread tightening → forward-return deterioration realised` — months — **price_to_structure** —
  carry looks fine after the return has already been spent; the turn is invisible in spot spread.

**system_traps:**
- *Success to the successful* — performance funds inflows that fund performance; **masks** rising
  fragility (concentration + valuation). signature_series: index weight × inflows × (−dispersion).
- *Escalation* — yield-reach / spread-compression race; each buyer's target set by others' positions.
- *Drift to low performance* — underwriting/covenant quality erodes under the "new tight normal."
- *Limits to growth* — `R1` MUST meet `B1` (return exhaustion) and `B2` (supply); named above.

**leverage_points:**
- *Reinforcing-loop gain* (rank 7, **structural**): a small drop in marginal inflow most alters
  behaviour — defuses `R1`. The point that matters; usually unpriced.
- *Delays* (rank 9, **structural**): the rebalance lag; shortening it (faster ETF flows) raises
  overshoot risk.
- *Information flows* (rank 6, partly **observable_to_investors**): positioning/flow visibility —
  watch this, it leads price.
- *Buffers* (rank 11, **observable_to_investors**): ETF cash / dealer inventory cushion.
- *Numbers* (rank 12, **observable_to_investors**): the spread level itself — what investors
  fixate on and the *weakest* lever (Meadows' "wrong direction" warning).

**early_warning_indicators:**
- net fund flows (leads spread reversal; warning = creations→redemptions).
- cross-sectional dispersion (leads; warning = widening off the low).
- dealer inventory / buffer (leads; warning = drawdown / inability to absorb).
- new-issue concession (leads; warning = concessions re-appearing → `B2` binding).

**scenario_implications** (→ upstream `Scenario.implied_axis_value`):
- loop_state `R1 dominant`: axis_direction = continued tightening → upstream "bull/momentum"
  scenario FV richer; but **already-priced**, so small (p−q).
- loop_state `B1/B2 binding`: axis_direction = widening/normalisation → "mean-reversion" FV.
- loop_state `B3 cascade`: axis_direction = violent gap-wider (overshoot, delay-driven) →
  fat-tail "crowded-unwind" scenario; the unwind is **discontinuous**, not smooth.

**expression_risk_implications** (which FAMILIES break first if `R1` reverses):
- order 1 — **long-beta / momentum / long-the-tight-sector**: dies first in a crowding reversal.
- order 2 — **short-vol / carry / curve-flatteners** funded by the compression: die as vol re-prices.
- order 3 — **relative-value longs vs. the crowded leg**: gap risk as the whole factor unwinds.
- robust(er) — **convex / long-protection / dispersion-wideners**: gain when `B3` overshoots.

**invalidation_evidence** (→ `Falsifier`):
- claim "the R loop is intact" — observable: net fund flows — threshold: *two consecutive
  periods of net redemptions* `PM_assumption`.
- claim "fundamentals support the tightening" — observable: dispersion / quality metric —
  threshold: *dispersion widens X bp off its low* `model_required`.
- claim "supply is absorbed" — observable: new-issue concession — threshold: *concession >
  Y bp returns* `PM_assumption`.

**PM_questions:**
- Is the marginal buyer price-sensitive or flow-mechanical (index/ETF)? Sets `R1` gain.
- How long is the rebalance/flow delay vs. our horizon? Sets overshoot magnitude.
- Where is the buffer (dealer inventory / ETF cash) and how thin is it?
- Are we being paid for the reversal or for more momentum? (the latter is already priced.)

---

## APPLIED ANSWERS (the 7 questions)
1. **Reinforcing?** Yes — `R1`: performance → inflows → (forced) buying → spread tightening →
   performance is a textbook reinforcing loop and the *success-to-the-successful* archetype; the
   rising index weight is its accumulating stock.
2. **Balancing loops that stop/reverse it (limits to growth):** `B1` return/carry exhaustion
   (tight spread → poor forward return → inflows slow); `B2` supply indigestion (tight spread →
   heavy issuance → concession → wider); `B3` redemption/liquidity cascade (big crowded position
   → outflows on a shock → forced selling, can flip to a death-spiral R). Every R loop must meet
   a B loop — these are its limits.
3. **Delays that make investors late:** the *flow→stock* lag (inflows move before the index
   weight / quality stock visibly changes, so the loop looks self-sustaining) and the
   *price→structure* lag (spread has tightened before the forward-return / covenant deterioration
   is realised). Investors extrapolate the flow; the turn is invisible in flow data.
4. **Signal of the shift from momentum to crowding reversal:** net fund flows turning
   (creations → redemptions), cross-sectional dispersion widening off its lows, dealer
   inventory / buffer drawdown, and new-issue concessions re-appearing — the `reversal_condition`
   is *marginal inflow < marginal supply* (or *carry < funding*).
5. **What to monitor:** flows, dispersion, buffers (dealer inventory / ETF cash), new-issue
   concession, and the rebalance-delay'd stock — i.e. rank 6–9 leverage-point series that move
   BEFORE the price, not the spread level (rank 12) that investors fixate on.
6. **Expression families that become risky if the loop reverses:** long-beta / momentum /
   long-the-tight-sector dies FIRST; then short-vol / carry / flatteners funded by the
   compression; then RV longs vs. the crowded leg (gap risk). Convex / long-protection /
   dispersion expressions are the ones that survive/benefit. Because the balancing loop acts with
   a delay, the unwind **overshoots and is violent, not smooth.**
7. **What proves it wrong:** two consecutive periods of net redemptions; dispersion widening a
   set threshold off its low; new-issue concessions exceeding a threshold — any one fires the
   falsifier that the reinforcing loop is intact.

## DECISION
**watchlist** — the loop structure is well-diagnosed and (likely) an operational axis exists, but
this is a high-attention, reinforcing-loop-dominant theme: *high attention × R-loop dominance =
already priced* (consistent with `−attention_score` and `edge_basis = gross_of_risk_premium`), so
there is no residual edge on "more momentum." Promote ONLY if `evidence_score > attention_score`
AND the edge is positioned on the named reversal condition (the B loop binding) — otherwise hold
on the watchlist until the early-warning series (flows turning, dispersion widening) signal the
shift. **No trade recommended.**

---
**Standing reminder:** this skill consumes the mapper's loop map and diagnoses behaviour only —
loop dominance, traps, leverage points, delays, early warnings, loop-state→FV and
expression-risk mappings, and falsifiers. It does NOT re-derive loops, price, size, or recommend
a trade. The scenario / pricing engine consumes this diagnosis next.
