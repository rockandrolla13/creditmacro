# Wiki Log

Append-only, chronological. One entry per lint batch. Newest entries go at the bottom.

Entry format:

```
## [YYYY-MM-DD] lint | batch N
- Sources linted:
- Fixes made:
- Cross-cutting patterns:
- Remaining issues:
```

---

## [2026-06-06] wiki bootstrap
- Created wiki structure (sources/, entities/, concepts/, themes/, scenarios/, strategy-families/, models/).
- Seeded the 14 strategy-family pages from the engine taxonomy (engine/schema.py + engine/discovery.py).
- No source pages exist yet, so no lint batch has run. Add source summaries under `wiki/sources/` then run "lint the wiki".

## [2026-06-07] source ingested | first CASE fixture — JPM AI Capex Funding (2026-05-11)
- **Source ingested:** [[jpm-ai-capex-funding-2026-05-11]] (access_class=**case**, report). Raw PDF
  private in `raw/pdfs/`; page-aware md in `raw/normalized-md/` (14 pages); paraphrase-only card.
- **Pages created (12):** 1 source; 4 themes ([[ai-capex-funding-credit-ecosystem]],
  [[hyperscaler-project-bond-basis]], [[hy-hpc-crowding-and-supply]],
  [[data-center-index-inclusion-technicals]]); 7 concepts ([[data-center-credit]],
  [[high-performance-computing-credit]], [[hyperscaler-project-bond-basis-mechanics]],
  [[index-inclusion-technical]], [[limited-syndication]], [[144a-for-life]], [[related-obligation-rv]]);
  + [[memory-map]] + 3 new family taxonomy pages.
- **Pages updated:** [[long_short]], [[cash_cds_basis]], [[outright]], [[watchlist_only]] (case priors);
  index.md (sources/concepts/themes/families); created [[index_index_rv]] [[etf_basket_rv]] [[curve]].
- **Evidence atoms created:** 15 (`jpm-2026-05-11-001 … 015`) in `wiki/evidence/evidence_atoms.jsonl`,
  each with `page:N` provenance.
- **Strategy-family priors updated:** ranked long_short > index_index_rv > etf_basket_rv > curve(2ndary) > outright(conditional); watchlist for HPC.
- **Unresolved issues:** hyperscaler-vs-project differentials unverified-clean (duration/rating); which
  index defines the live DC technical; HPC likely crowded (watchlist); memory-map not yet in skip-set.
- **No-trade confirmation:** no exact bonds, curve points, hedge ratios, sizes, or execution emitted.
  Discovery memory only — families, not trades.

## [2026-06-08] lint | batch 1
- **Sources linted:** [[jpm-ai-capex-funding-2026-05-11]] (1; the only source page — seed-42
  frozen order built this session). Read the source + all 17 pages it links (4 themes, 7
  concepts, 7 strategy-families) + evidence atoms.
- **Fixes made:** (1) renamed `concepts/hyperscaler-project-bond-basis.md` →
  `…-mechanics.md` so the filename matches its declared `slug` — this resolved a slug collision
  with the theme `hyperscaler-project-bond-basis` and fixed 4 broken inbound `[[…-mechanics]]`
  links (index.md, log.md, data-center-credit, related-obligation-rv). (2) Source "Concepts:"
  line relinked `[[hyperscaler-project-bond-basis]]` → `[[hyperscaler-project-bond-basis-mechanics]]`
  (it meant the concept, not the theme).
- **Cross-cutting patterns:** `engines/` (9 pages) absent from `index.md` — deferred to a
  dedicated pass (outside this source's link graph).
- **Remaining issues:** source frontmatter carries non-CONVENTIONS fields (`classification`,
  `workflow_status`) — preserved, flagged for a schema decision. No broken links, missing pages,
  stale sources lists, stubs, contradictions, or investment-process gaps in the linted set.
- **Verification:** 0 real broken wikilinks and 0 slug collisions wiki-wide after fixes.

## [2026-06-08] reconciliation | strategy-family count (schema vs docs)
- **Contradiction resolved:** docs (CLAUDE.md, CONVENTIONS.md) claimed `family_type` "exactly"
  equals the engine's `StrategyFamilyRec.family` Literal, but the Literal is 9 (the auto-routable
  set, test-enforced by `test_family_literal_is_exactly_the_routable_set`) while the wiki menu is 14.
- **Decision (user):** decouple, not extend the schema. The 14-family wiki list is the human
  discovery vocabulary; the 9-member Literal is the auto-routable subset. The "must not overstate
  capability" guardrail is preserved (test untouched, still 13/13 passing).
- **Fixes made:** corrected the false "exactly mirrors" claim in CONVENTIONS.md and CLAUDE.md to
  state the superset/subset relationship; fixed stale path `engine/schema.py` → `engine/schema/strategy_family.py`
  in those docs and in the 9 routable family pages; created the 2 missing taxonomy pages
  ([[sector_rotation]], [[capital_structure]]) so all 14 menu families now have pages; added both to
  index.md taxonomy list.
- **Remaining issues:** none from this reconciliation. `engines/` still absent from index.md (pre-existing, deferred).

## [2026-06-08] feature | promoted 3 RV sub-type families to first-class routing
- **Promoted (now auto-routed, in the Literal):** [[etf_basket_rv]], [[capital_structure]],
  [[index_index_rv]] — implemented as relative_value SUB-TYPES via
  `engine/discovery._relative_value_subtype` (mirrors the existing cross_asset equity/rates split;
  no change to `AxisShape` or `_direction_from_sign`). Routable set: 9 → 12.
- **Detection vocabulary:** ETF/NAV tickers → etf_basket_rv; subordination terms (subordinated,
  AT1, tier 2, hybrid, holdco/opco) → capital_structure; CDX&iTraxx co-occurrence / series-roll /
  on-the-run-vs-off → index_index_rv. Deliberately avoids bare "senior"/"sub" so a
  senior-bank-vs-sovereign pair stays long_short (regression-tested).
- **Still wiki-only (no routing rule):** [[curve]] (parent of steepener/flattener),
  [[sector_rotation]] (detection too fragile — would misfire on ordinary pairs).
- **Guardrail preserved:** `test_family_literal_is_exactly_the_routable_set` updated to the new
  12-set; +4 routing tests added. Full suite 325 passed, 0 regressions (golden masters + JPM
  fixture intact). Updated CONVENTIONS.md, CLAUDE.md, index.md, and the 3 promoted family pages.

## [2026-06-08] materialization | Q4 PART-2a — JPM evidence atoms as CASE pages
- **Materialized** all 15 JPM evidence atoms (`jpm-2026-05-11-001 … 015`) as CASE markdown pages
  in `wiki/evidence/`, derived from the committed `evidence_atoms.jsonl` (single source of truth)
  + added `claim_kind` (from `is_synthesis`), `access_class: case`, `source_date`, `page_number`.
  Closes the dangling theme-card evidence links (a JSONL can't resolve page links) and the audit's
  "evidence atoms = 0 pages" finding.
- **Firewall hardened:** `engine/memory._CASE_TYPES` now includes `evidence` + `outcome`, so an
  evidence page defaults to CASE even without an explicit `access_class` (fail-closed).
- **Tested (TDD, +7 tests):** every theme-card evidence link resolves; every atom carries source_slug
  + `page:N` + claim_kind + source_date + access_class:case; headline figures present; no ≥25-word
  verbatim run vs the JPM raw markdown (leak guard); Phase-A `MemoryRetriever` refuses archived
  evidence on **real on-disk pages** (closes "firewall realism untested on disk"), readable in Phase B.
- **Single source of truth:** pages regenerated from the JSONL so the committed `test_jpm_case_fixture`
  assertions stay green. Full suite 352 passed, 0 regressions. No golden-master change; no scenarios/
  probabilities/fair-values/legs/sizing produced. Bridge engine (atoms→map→posterior) = PART-2b, not built.
