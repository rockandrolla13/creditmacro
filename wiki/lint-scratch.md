# Lint Scratch

This file stores temporary findings across lint batches. Do not delete unresolved findings.

Each batch appends a header `## Batch N — [YYYY-MM-DD]` followed by one block per source,
with findings under the required headings:

- **Broken wikilinks**
- **Missing pages**
- **Stale sources lists**
- **Stubs**
- **Contradictions**
- **Stale claims**
- **Format issues**
- **Investment-process gaps**

After the per-source blocks, a `### Cross-cutting patterns` subsection records issues that
appear across multiple sources in the batch (higher priority to fix).

---

<!-- batches appended below -->

## Batch 1 — [2026-06-08]

### Source: [[jpm-ai-capex-funding-2026-05-11]]

**Broken wikilinks**
- `[[hyperscaler-project-bond-basis-mechanics]]` resolved to no file. The concept page declared
  `slug: hyperscaler-project-bond-basis-mechanics` but was saved as
  `concepts/hyperscaler-project-bond-basis.md` (filename ≠ declared slug). Broken inbound links
  from `index.md`, `log.md`, `concepts/data-center-credit.md`, `concepts/related-obligation-rv.md`.
  → **FIXED** by renaming the file to match its slug (`git mv` to `…-mechanics.md`).

**Missing pages**
- None. All 17 source wikilinks resolve to existing pages.

**Stale sources lists**
- None. Every linked theme/concept/strategy-family page already lists
  `jpm-ai-capex-funding-2026-05-11` in `sources:`.

**Stubs**
- None. Themes ~77–81 lines, concepts ~33–38, strategy-families ~37–40; all substantive with
  required frontmatter.

**Contradictions**
- None across the linked pages.

**Stale claims**
- None (single source; nothing superseded).

**Format issues**
- **Slug collision + filename≠slug:** `concepts/hyperscaler-project-bond-basis.md` (declared slug
  `…-mechanics`) collided in bare-slug space with `themes/hyperscaler-project-bond-basis.md`, so
  `[[hyperscaler-project-bond-basis]]` was ambiguous (theme vs concept). → **FIXED** (rename).
- Source "Concepts:" list (line 96) linked the bare theme slug `[[hyperscaler-project-bond-basis]]`
  where it meant the concept. → **FIXED** to `[[hyperscaler-project-bond-basis-mechanics]]`.
- Source frontmatter carries non-CONVENTIONS fields `classification: source` and
  `workflow_status: discovery_complete` (not in the common/source schema). Minor — **left as-is**
  (likely intentional extension; preserved, flagged for a schema decision).

**Investment-process gaps**
- None. The source supplies all required investment-agent fields (main developments, key events,
  core themes, hot topics, causal claims, operational axes, confounders, falsifiers,
  strategy-family hints, open questions).

### Cross-cutting patterns
- **`engines/` not indexed (DEFERRED):** 9 pages under `wiki/engines/` (causal_compiler,
  system_mapper, max_entropy_probability_justifier, factor_r2_router, macro_state_parser,
  option_implied_q_provider, outcome_calibration_engine, system_trap_detector,
  backdoor_identifiability_gate) are absent from `index.md` (Models section empty, no Engines
  section). Outside this source's link graph → **NOT fixed this batch**; flagged for a dedicated
  engines lint pass + an index Engines section.
