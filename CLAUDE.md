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

## Wiki — persistent memory layer
`wiki/` is the agent's persistent memory: the generated/maintained layer over the
IMMUTABLE raw sources in `markdowns/` (never modify raw sources). It stores raw source
summaries, entities, concepts, market developments, key events, core themes, hot topics,
causal chains, operational axes, falsifiers, scenarios, and ranked strategy families.
It mirrors the engine lifecycle: research → wiki memory → developments/events/themes/hot
topics → causal object → ranked strategy families with confidence → STOP (no detailed
legs/sizing/hedge ratios in discovery mode). Page frontmatter + investment-process lint
checks live in `wiki/CONVENTIONS.md`. The 14 strategy-family pages are the human discovery
vocabulary (the hint menu); they are a **superset** of the engine's auto-routable output set.
`StrategyFamilyRec.family` (`engine/schema/strategy_family.py`) declares only the families the
router can actually emit today (currently 12, test-enforced not to overstate capability), and
`_DOWNSTREAM` (`engine/discovery.py`) carries downstream models for that routable subset.
`etf_basket_rv` / `capital_structure` / `index_index_rv` route as relative_value sub-types
(`_relative_value_subtype`). The two remaining wiki-only families (`curve`, `sector_rotation`)
are taxonomy pages with no routing rule yet.

## Memory access firewall (two-phase)

The wiki is shared memory: human-curated, agent-maintained, agent-consumed. The hazard is
**CASE memory** (past themes, scenarios, closed-thesis outcomes, prior analyses) leaking into
**FRESH** causal reasoning, so the agent anchors on old conclusions. **METHOD memory**
(concepts, causal mechanisms, how-to-reason pages from books & papers) carries no such
hazard. Every page declares `access_class: method | case` (see `wiki/CONVENTIONS.md`).

**The rule: reason fresh, freeze, then consult history — never the reverse.**

This is enforced by CONSTRUCTION, not by instruction:

- **Phase A (fresh reasoning).** The agent loads ONLY method pages. `MemoryRetriever`
  (`engine/memory.py`) is **fail-closed**: in phase A it returns method pages and REFUSES
  everything else (case / missing / invalid) — returning `None` and logging the refused
  slug. There is no other path to wiki content, so phase A *cannot* retrieve case content.
  It builds the causal object and routes strategy families with confidence, ending at the
  locked lifecycle status `strategy_family_routed`.
- **FREEZE.** `freeze()` (`engine/firewall.py`) serializes the phase-A output into an
  immutable `FrozenSnapshot` with a SHA-256 `content_hash` + timestamp. The hash is marked
  on the retriever BEFORE phase B is unlocked, so any case read is provably post-freeze.
  `ThemeObject`, `StrategyFamilyRec`, and `ConfidenceComponents` are frozen pydantic models —
  the causal object physically cannot be mutated after the snapshot.
- **Phase B (analogue & calibration).** Only now may the agent read case pages, and ONLY to
  (a) find analogues and (b) calibrate confidence. Changes are written to a separate,
  additive `PostCaseCalibration` block that references the snapshot hash. The frozen causal
  object and its routed families are never mutated.

The emitted `FirewalledResult` carries `fresh_snapshot_hash`, `fresh_reasoning` (immutable),
and `post_case_calibration` (additive) — so a reader can always tell what the agent
concluded BEFORE seeing history vs the adjustment AFTER. The phases map onto the engine's
locked lifecycle (do not invent a parallel one): phase A ends at `strategy_family_routed`;
phase B annotates it; neither phase produces `expression_complete`. Iceberg classification
(hot_topic / core_theme_candidate / …) stays separate from `status`.

Run a two-phase pass: `engine.firewall.run_two_phase(provider, policy, pages)` →
`FirewalledResult`.

## Workflow 3: Lint

**Trigger:** Human says "lint the wiki", "continue lint", "health-check", or "what's missing".

### Process

Lint runs in **batches of 5 sources per session** to protect context. The order is
**randomised once with seed 42** (not alphabetical or ingestion-order) to counteract topic
clustering and reveal cross-cutting connections that order-biased passes miss. The order is
stored in `wiki/lint-status.md` and must NOT be re-shuffled between sessions. Lint is about
internal wiki consistency — do NOT web search unless explicitly asked.

### Steps

1. Read `wiki/lint-status.md` to find the next 5 unchecked sources (`[ ]`).
2. Read `wiki/lint-scratch.md` to load findings from previous batches and check for
   unresolved patterns.
3. For each source: read the source page, then read every entity, concept, theme, scenario,
   and strategy-family page it links to.
4. Append findings for each source to `wiki/lint-scratch.md` under a new batch header, using
   the exact finding-category headings below.
5. After all 5 sources, re-read the scratch entries for this batch and note any
   **cross-cutting patterns** (e.g. the same broken link in multiple sources = higher
   priority fix).
6. Execute all fixes for the batch. Create missing pages only when the link represents a
   recurring or important entity/concept/theme. Update linked pages' `sources:` frontmatter.
7. Mark the 5 sources `[x]` in `wiki/lint-status.md`. Hub concept/entity pages touched get
   `[~]` if not all contributing sources have been linted yet; promote to `[x]` only when
   all contributing sources are done.
8. Append one summary entry to `wiki/log.md`.

**Discovery discipline:** lint never produces detailed trades — no exact bonds, curve
points, hedge ratios, position sizes, stop losses, or execution instructions. Strategy
families only (the 14 in `wiki/CONVENTIONS.md`). Do NOT delete contradictions (preserve with
source dates); do NOT silently overwrite older claims (mark stale, cite the newer source).

### Finding categories (exact headings in `wiki/lint-scratch.md`)

- **Broken wikilinks** — link target doesn't match any slug in the index
- **Missing pages** — entity/concept linked inline but no page exists
- **Stale sources lists** — concept/entity page's `sources:` frontmatter missing a source
  that links to it
- **Stubs** — pages with thin content that warrant expansion
- **Contradictions** — claims that conflict across pages
- **Stale claims** — things newer sources may have superseded
- **Format issues** — frontmatter missing required fields, wrong link syntax, etc.
- **Investment-process gaps** — source/theme pages missing required investment-agent fields
  such as main developments, key events, core themes, hot topics, causal chain, operational
  axis, confounders, falsifiers, or strategy-family mapping.
