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
