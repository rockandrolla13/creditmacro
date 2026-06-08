# Claude Skills

METHOD skills for the investment-research agent. Read by Provider seams to guide
structured reasoning. Not case memory. Not old conclusions. Not trade recommendations.

## Access rule
- Skills are method memory, readable during Phase A fresh reasoning.
- Case pages may NOT be read during Phase A.
- Past cases allowed only after FreshReasoningSnapshot.

## Product boundary
idea / report → causal object → ranked strategy families with confidence → STOP.
No trades. No sizing. No hedge ratios. No execution.

## Skill-to-provider mapping
- Iceberg Classifier → stage0.classify_iceberg / parse_research_text
- Causal Compiler → Provider.expand_causal
- System Mapper → Provider.build_system_map
- Trap Detector → Provider.diagnose_loops / critique_mental_model
- Scenario Pricing Engine → probability.justify_probabilities / engine2.run_pricing
- Macro Regime Classifier → pending macro-context seam (available as method context)

## Compiled-from provenance
Each card was COMPILED (paraphrased process primitives, not verbatim text) from a source in
`markdowns/`:
- `system-mapper`, `trap-detector` ← *Thinking in Systems* (Meadows) — stocks/flows, R/B
  feedback taxonomy, delays, archetype traps, leverage-point hierarchy.
- `iceberg-classifier`, `causal-compiler` ← *Thinking in Systems and Mental Models*
  (Dawson, "Super Thinker") — iceberg layers (event/pattern/structure/mental-model),
  behaviour-over-time.
- `macro-regime-classifier` ← *Citi Views Macro Book* — cross-asset regimes
  (reflation/stagflation/goldilocks), scenario (bear/base/bull) framing, macro→asset-class
  propagation.
- `scenario-pricing-engine` ← the engine's own max-entropy math (`engine/engine2.py`,
  `engine/probability.py`) + Cover–Thomas KL concepts.
- `evidence-weighting` ← *Bayes and Base Rates* (Mauboussin & Callahan, MS Counterpoint Global)
  — base-rate anchoring + likelihood-ratio updating.
- `priced-in-estimator` ← *Investing Amid Low Expected Returns* (Ilmanen) — return building
  blocks; separating valuation level from risk premium.
- `edge-validity` ← *Finding Alphas* (Tulchinsky) — in/out-of-sample, overfitting, robustness checklist.
- `trap-detector` **supplement** ← *How Not to Be Wrong* (Ellenberg) — regression to the mean,
  survivorship/selection bias, false linearity, false patterns (added as a section to the existing card).

### Registration vs wiring (this PR)
The three new cards are **registered** (discoverable via `list_available_skills`, loadable via the
registry) but deliberately **not auto-wired** into any live seam — `SEAM_TO_SKILLS` is unchanged:
- `evidence-weighting` — **PENDING** the Q4 posterior≠prior derivation (separate PR). It must NOT
  feed `ConfidenceComponents` yet (`engine.skills.PENDING_WIRING_SKILLS`).
- `priced-in-estimator`, `edge-validity` — **readable** in discovery as method context, but not
  injected, and must not change any golden-master numerical output
  (`engine.skills.READABLE_DISCOVERY_SKILLS`).

### Reviewed but intentionally NOT compiled
- *Fed Up* (Lancaster) — **reviewed**; it is a trading memoir (narrative/case material, not
  method). Compiling it would risk leaking case content across the method/case firewall, so no
  card was produced. Skipped by design.

### Source gaps (noted per the read-before-write rule)
- `markdowns/citi global theme book.md` is **image-only** — its text extracts as omitted
  pictures, so the theme-taxonomy supplement in `iceberg-classifier` is compiled from the
  Super-Thinker iceberg model + the engine's `stage0` taxonomy instead. Re-OCR the deck to
  enrich the taxonomy later.

## Method-cards batch 3 (Tooley / monetary transmission)

### Triage of the named sources
All sources live in `markdowns/` (the task's `/mnt/project/` paths do not exist here; mapped below).

| Source file (in `markdowns/`) | Bucket | Reason / disposition |
|---|---|---|
| `Time, Tense, and Causation (Michael Tooley) …md` | **METHOD** | Timeless philosophy of causation — causal asymmetry, direction of counterfactual dependence, counterfactual vs constant conjunction. Compiled into `causal-compiler` (upgrade). |
| `Monetary Policy after the Great Recession  the role of interest rates (Arkadiusz Sieroń) …md` | **MIXED → METHOD extract** | Transmission *channel taxonomy* (interest-rate / credit / asset-price / risk-taking) is timeless mechanism → supplemented into `system-mapper` + `macro-regime-classifier` as a stock/flow system. Post-2008 narrative & dated calls EXCLUDED. |
| `Monetary Policy in Times of Crisis … (Rostagno, Altavilla …) …md` | **MIXED → thin METHOD extract** | Adds the **duration / portfolio-rebalancing channel** (a *stock view*: extracted duration risk → term-premium compression) beyond Sieroń → thin-extracted into the same two cards. The two-decade ECB decision LOG is **CASE** and was NOT compiled. |
| `Avramov-UnderstandingChangesCorporate-2007.md` | **SKIP (OCR gap)** | JSTOR cover-page stub only (title/authors/"content downloaded from…" repeated); body did not OCR. No method body present → not compiled. Logged as OCR gap; source PDF re-OCR unavailable. |
| `Alaph Long Presentation Version July 2014.md` | **SPEC** | The fund's own four-step process (theme→valuation→trade selection→portfolio construction) that defines the discovery/expression split. Canonical **workflow reference**; compiled nothing. |
| `XantimumBizPlan.md` | **SPEC** | Business plan (risk decomposition, liquidity scoring). Compiled nothing. |
| `Taars.md` | **CASE / ingestion** | Dated DB TAARSS tactical/positioning note. No skill card — ingestion-fixture / case candidate only. |

### Cards updated this batch
- **`causal-compiler` (UPGRADE)** ← *Time, Tense, and Causation* (Tooley). New section
  *"Causal asymmetry — what makes a causal object VALID"*: cause precedes / brings the effect into
  being; **counterfactual dependence ≠ constant conjunction**; asymmetry of dependence
  (`direction_unidentified` if the arrow reverses cleanly); causal (not temporal) backtracking.
  Added `test_causal_asymmetry_counterfactual` to frontmatter; existing substrings
  (hyperscaler/project/confounder/falsifier) and tests preserved.
- **`system-mapper` (SUPPLEMENT)** ← Sieroń + ECB (Rostagno/Altavilla, mechanism only). New
  section mapping rate→economy→asset **transmission as a stock/flow + feedback system**
  (channels; stocks = outstanding credit/reserves/aggregate duration risk; flows = issuance /
  lending / purchases; reach-for-yield R-loop; delayed credit-boom→fragility B-loop).
- **`macro-regime-classifier` (SUPPLEMENT)** ← Sieroń + ECB. New *transmission primitive* section
  (same chain + stock/flow + loops) framing regime-conditional cross-asset propagation.

These edits are **method-text only** — no new registry wiring. `SEAM_TO_SKILLS` is unchanged; the
golden-master numerical output is unchanged. No new card was created: per the "prefer supplementing"
rule the monetary-transmission mechanism was folded into the existing macro/system cards.

### OCR gaps (read-before-write rule)
- `markdowns/Avramov-UnderstandingChangesCorporate-2007.md` — **JSTOR cover-page stub**, body not
  OCR'd. Skipped (no method body); priced-in-estimator's credit-spread-attribution enrichment is
  therefore deferred until the source PDF is re-OCR'd.

### SPEC / CASE references (not skill cards)
- **Alaph Long Presentation (July 2014)** — canonical four-step **workflow reference**.
- **XantimumBizPlan** — business plan (SPEC).
- **Taars** — dated TAARSS tactical note → **CASE / ingestion fixture** candidate.

## Pending skills (later PRs)
- Carry Estimator (from *Riding Carry* — source PDF not present in repo; DEFERRED).
- Rates Fair-Value / Cycle Estimator (from *Rates Puzzle Game / Quant Guide to Duration* —
  source PDF not present in repo; DEFERRED).

These two are intentionally **not** built in this PR (no source available, and they touch
the rates/fair-value layer). Do not synthesise them from general knowledge.
