# Theme-to-Trade Conversion Engine

## What this is
A disciplined pipeline that converts a research document 
into a falsifiable, Thematic HYPOTHESIS.
Based on the Alaph four-step process (theme -> valuation -> trade selection
-> portfolio construction). 
It is an EPISTEMIC engine. It STOPS at a PM
decision memo. 
## Architecture
Stage 0 (ingestion) -> ThemeObject (shared typed state) populated by 4
engines -> PM gate.

Stage 0 parses research into THREE typed streams, kept separate:
  - Observation     (facts: developments, events) -> update driver levels
  - CandidateTheme  (narratives: core themes)      -> become ThemeObjects
  - ConsensusSignal (attention: hot topics)        -> prior for market-implied q
Nominate candidate themes RANKED BY divergence(evidence, attention): high
factual support + low attention = high latent edge. This is a pre-screen on (p - q).

Engine 1  Driver + axis      -> Q1 theme, Q2 universe, Q3 axis (MUST be a computable series)
Engine 2  Scenario pricing   -> Q4 normal FV, Q5 scenario FV = sum p_s X_s,
                                Q6 priced-in q via max-entropy, Q7 edge = <p - q, X>
Engine 3  Expression scoring -> Q8 candidates, Q9 best = gated multiplicative score
Engine 4  Sizer + risk       -> Q10 size (Alaph grid), Q11 stop, Q12 falsifiers
PM gate                       -> Q13 open questions; hands control to the human

## Hard discipline gates (refuse to emit a ThemeObject without these)
1. axis is OPERATIONAL: a named spread/slope with a real historical time series
2. pricing.residual_edge is computed
3. >= 1 scored expression survives the liquidity / asymmetry gates
4. >= 1 falsifier with an observable + threshold
A thesis with no falsifier is not a thesis. Do not emit it.

## Scoring rules (Engine 3) — "best" is NEVER max E[P&L]
purity  rho^2 = beta^2 Var(dX) / (beta^2 Var(dX) + Var(eps))   # R^2 of expression P&L on the thesis axis
asym    Omega(tau) = E[(Pi - tau)+] / E[(tau - Pi)-]            # generalizes E{Gain}/E{Loss}; require >= 2
score   = rho^2 * Omega * (1 + a*convexity) * liquidity * exp(-g*crowding) / (1 + capital)
Gates FIRST (Omega >= 2, liquidity >= min, finite worst case), rank SECOND.
Liquidity score per Xantimum: trade frequency, volume, clearing breadth, cost, vol.

## Research corpus (read these first)
- markdowns/Alaph Long Presentation Version July 2014.md   # the four-step process, French-banks worked trade
- markdowns/XantimumBizPlan.md                             # risk decomposition, liquidity scoring, sub-strategies
- markdowns/citi global theme book.md                      # theme taxonomy (Theme-Ometer / Theme Machine)
- markdowns/Taars.md                                       # ETF-flow signals (TAARSS) -> positioning / consensus input

### Background priors (systems thinking + causality)
- markdowns/Thinking in Systems A Primer (Meadows, Donella H.) (z-library.sk, 1lib.sk, z-lib.sk).md   # stocks/flows, feedback loops, leverage points -> driver dynamics
- markdowns/Thinking in Systems and Mental Models Think Like a Super Thinker. Primer to Learn the Art of Making a Great Decision and… (Marcus P. Dawson) (z-library.sk, 1lib.sk, z-lib.sk).md   # mental-model toolkit for decision framing
- markdowns/Systematic Trading - A unique new method for designing trading and investing systems (Robert Carver) (z-library.sk, 1lib.sk, z-lib.sk).md   # systematic rules, sizing, risk budgeting -> Engine 4 sizer/stops
- markdowns/The Book of Why (Judea Pearl) (z-library.sk, 1lib.sk, z-lib.sk).md   # causal inference, do-calculus -> separating correlation from driver causation

## Stack
Python. Pydantic for the schema. scipy.optimize for the max-entropy q solver.
LLM calls behind interfaces for the generative engines. No subagents yet —
one orchestrated workflow over the shared ThemeObject. Output per theme:
one ThemeObject JSON + a human-readable decision memo (markdown).
