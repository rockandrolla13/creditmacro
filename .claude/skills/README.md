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

### Source gaps (noted per the read-before-write rule)
- `markdowns/citi global theme book.md` is **image-only** — its text extracts as omitted
  pictures, so the theme-taxonomy supplement in `iceberg-classifier` is compiled from the
  Super-Thinker iceberg model + the engine's `stage0` taxonomy instead. Re-OCR the deck to
  enrich the taxonomy later.

## Pending skills (later PRs)
- Carry Estimator (from *Riding Carry* — source PDF not present in repo; DEFERRED).
- Rates Fair-Value / Cycle Estimator (from *Rates Puzzle Game / Quant Guide to Duration* —
  source PDF not present in repo; DEFERRED).

These two are intentionally **not** built in this PR (no source available, and they touch
the rates/fair-value layer). Do not synthesise them from general knowledge.
