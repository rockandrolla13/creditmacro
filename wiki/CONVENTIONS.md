# Wiki Conventions

The wiki is the **persistent memory layer** for the investment-research agent. It is the
generated/maintained layer over the **immutable** raw sources in `raw/` (original PDFs in
`raw/pdfs/`, page-aware markdown in `raw/normalized-md/`, page assets/tables in
`raw/assets/` and `raw/tables/`, conversion manifests in `raw/manifests/`). Never modify
raw source files. (The legacy `markdowns/` corpus is being migrated into `raw/normalized-md/`;
`raw/` is private/gitignored — only the wiki is tracked memory.)

The source compiler (`tools/convert_pdf_to_markdown.py`, `tools/create_source_card.py`,
`tools/extract_method_skills.py`) produces normalized md → source cards → evidence atoms
→ method cards / engine specs. It reuses the firewall in `engine/memory` + `engine/firewall`
(it never forks them) and writes cards in the frontmatter convention below. Wiki pages carry
PARAPHRASE + citation only — never reproduced source text (`tools/leak_check.py` enforces a
≤25-word verbatim cap against `raw/normalized-md`).

Target workflow (discovery half only):

```
research / idea
  → wiki memory
  → main developments, key events, core themes, hot topics
  → causal object
  → ranked strategy families with confidence
  → STOP
```

No detailed trade legs, sizing, hedge ratios, stops, or exact curve points are produced in
discovery mode — those are downstream (the engine's `mode="expression"`).

This mirrors the engine: `ThemeObject.status ∈ {blocked, discovery_complete,
strategy_family_routed, expression_complete}`; the discovery half stops at
`strategy_family_routed` (ranked `StrategyFamilyRec`s with decomposed `confidence`).

---

## 1. Required frontmatter

All wiki pages carry YAML frontmatter. **Do not invent facts to fill fields — use empty
arrays / blanks if unknown.**

### Common (every page)

```yaml
---
type: source | entity | concept | theme | scenario | strategy_family | model
access_class: method | case        # REQUIRED — memory access firewall (see below)
title:
slug:
aliases: []
tags: []
sources: []
status: draft | active | stub | deprecated
created:
updated:
---
```

### `access_class` — the memory access firewall

Every knowledge page MUST carry a valid `access_class`. The distinction is about CONTENT
(how-to-reason vs market-specific conclusion), not page type — so the author sets it
explicitly; the type-based defaults below are only a fallback.

**`method` — how-to-reason content. The agent may read this anytime (phase A or B).**
Teaches HOW to think, not WHAT was concluded about a specific market. Examples:
- causal-inference principles (e.g. do-calculus, confounders, identifiability)
- systems-thinking principles (stocks/flows, feedback loops, leverage points)
- Alaph investment-process rules (theme → valuation → trade selection → portfolio)
- Xantium systematic RV process rules (risk decomposition, liquidity scoring)
- strategy-family routing rules (axis shape + direction → family)
- concept mechanics — "cash-CDS basis", "credit curve", "ETF create/redeem", "OAS"

**`case` — past market-specific conclusions. The agent may NOT read these during fresh
causal construction or initial strategy-family routing (phase A); phase B only.** They
record CONCLUSIONS about specific markets and anchor fresh reasoning on history. Examples:
- a prior AI-capex theme page
- a prior scenario tree
- a prior "best family was steepener" recommendation
- outcome records / realized trade or theme postmortems
- historical analogue pages
- old report-synthesis pages that contain conclusions

Note the content-over-type rule: a deck or business-plan source that states **process
rules** (Alaph, Xantium) is `method`; a deck or report that states **market conclusions**
(a sell-side trade call, a research synthesis) is `case`. When in doubt, mark `case` — the
retriever is fail-closed, so the cost of mislabelling is over-blocking in phase A, never
leakage of a conclusion into fresh reasoning.

**Defaults** (fallback only — see `engine/memory.derive_access_class`): concept/entity/model
→ method; theme/scenario → case; source → method if `source_type` is book/paper, else case
(report/memo/transcript/market_data → case; a process-rule **deck**/**memo** must be tagged
`method` explicitly); strategy_family → method. **Lint check:** every page has a valid
`access_class` (`engine.memory.check_access_class`); a missing/invalid one is a
**Format issue** and is treated as `case` (fail-closed) until fixed.

**Exempt — operational files, not knowledge pages:** `index.md`, `log.md`, `lint-status.md`,
`lint-scratch.md`, and this `CONVENTIONS.md` are the wiki's machinery; the retriever never
serves them as knowledge, so they carry no `access_class` (and the loader/lint skip them).
Caveat: `index.md` lists pages by section — its **Themes/Scenarios** sections point at
`case` pages, so phase-A navigation must not pull those entries into reasoning context.

The two-phase rule is enforced by CONSTRUCTION (the retriever), not instruction — see
`## Memory access firewall (two-phase)` in `CLAUDE.md`. Reason fresh → freeze → consult
history; never the reverse.

### Source pages — additionally

```yaml
---
source_type: book | paper | report | deck | memo | transcript | market_data | other
source_date:
author_or_publisher:
raw_source_path:        # path into raw/ (immutable; e.g. raw/normalized-md/<slug>.md)
ingestion_status: draft | ingested | linted
---
```

### Theme pages — additionally

```yaml
---
theme_status: hot_topic | core_theme_candidate | discovery_complete | strategy_family_routed | expression_complete
main_developments: []
key_events: []
hot_topics: []
causal_chain: []
operational_axes: []
confounders: []
falsifiers: []
strategy_families: []
---
```

`theme_status` maps to the engine's `ThemeObject.status` (plus the pre-causal lanes
`hot_topic` / `core_theme_candidate`). A theme reaches `strategy_family_routed` only with a
promoted operational axis, ≥1 falsifier, and ≥1 ranked strategy family.

### Strategy-family pages — additionally

```yaml
---
family_type: steepener | flattener | curve | long_short | outright | sector_rotation | capital_structure | cash_cds_basis | etf_basket_rv | index_index_rv | credit_vs_equity | credit_vs_rates | volatility_convexity | watchlist_only
downstream_model:
typical_axes: []
typical_data_needed: []
typical_failure_modes: []
---
```

`family_type` is exactly the engine's `StrategyFamilyRec.family` Literal (engine/schema.py).
`downstream_model` / `typical_data_needed` mirror `engine/discovery.py` `_DOWNSTREAM`.

---

## 2. Investment-specific lint checks (source pages)

When linting a source page, check it connects to the investment workflow. Each source
should ideally identify:

1. **Main developments** — persistent changes in the market system.
2. **Key events** — dated catalysts: shocks, data, issuance, policy, earnings, rating
   actions, index changes.
3. **Core theme candidates** — causal, measurable, potentially investable hypotheses.
4. **Hot topics** — high-attention narratives that may or may not be investable.
5. **Causal claims** — driver → transmission channel → outcome.
6. **Operational axes** — observable market variables that could later be priced.
7. **Confounders** — alternative explanations or shared factors (e.g. the standing credit
   risk premium: a wide spread is not by itself mispricing).
8. **Falsifiers** — observable + threshold evidence that would prove the theme wrong.
9. **Strategy-family hints** — possible expression *families*, not detailed trades.

Valid strategy-family hints (the 14 families): steepener, flattener, curve, long_short,
outright, sector_rotation, capital_structure, cash_cds_basis, etf_basket_rv, index_index_rv,
credit_vs_equity, credit_vs_rates, volatility_convexity, watchlist_only.

**Discovery mode must NOT produce:** exact bonds, exact curve points, hedge ratios, position
sizes, stop losses, or execution instructions. Those are downstream.

---

## 3. Lint behaviour (per batch)

1. Open `wiki/lint-status.md`; select the next 5 unchecked source pages.
2. Open `wiki/lint-scratch.md` (load prior unresolved findings).
3. For each selected source, read the source page then every page it links to (entities,
   concepts, themes, scenarios, strategy-families).
4. Record findings under the required headings (see below) in `wiki/lint-scratch.md`.
5. Re-read this batch's findings; identify cross-cutting issues (same broken link across
   sources = higher priority).
6. Make the fixes.
7. Update linked pages' `sources:` frontmatter where needed.
8. Create missing pages only when the link represents a recurring or important
   entity/concept/theme.
9. Mark the 5 sources `[x]` in `wiki/lint-status.md`; mark hub pages `[~]` if only partially
   linted (promote to `[x]` when all contributing sources are done).
10. Append one summary entry to `wiki/log.md`.

### Finding categories (exact headings)

- **Broken wikilinks** — link target doesn't match any slug in the index.
- **Missing pages** — entity/concept linked inline but no page exists.
- **Stale sources lists** — a page's `sources:` frontmatter missing a source that links to it.
- **Stubs** — thin pages that warrant expansion.
- **Contradictions** — claims that conflict across pages.
- **Stale claims** — things newer sources may have superseded.
- **Format issues** — frontmatter missing required fields, wrong link syntax, etc.
- **Investment-process gaps** — source/theme pages missing required investment-agent fields
  (main developments, key events, core themes, hot topics, causal chain, operational axis,
  confounders, falsifiers, or strategy-family mapping).

### Preservation rules

- **Do not delete contradictions.** Preserve them under a "Contradictions / Source
  disagreement" section with source dates.
- **Do not silently overwrite older claims.** Mark the older claim as potentially stale and
  cite the newer source.
- **Do not web search** unless explicitly asked — lint is about internal wiki consistency.
