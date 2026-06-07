---
type: model
access_class: method
title: Memory map
slug: memory-map
tags: [operational, map]
status: active
sources: []
created: 2026-06-07
updated: 2026-06-07
---

# Memory map

> Operational navigation map (like `index.md`). It lists **theme names and status only** — never
> case content. The names of CASE themes appearing below must NOT be pulled into fresh causal
> reasoning in phase A; the retriever still refuses the underlying case pages until phase B.
> NOTE: this file is not yet in `engine.memory.load_wiki_pages`' skip-set — see Open items.

## Active Main Developments
- AI-credit complex: 27 issuers / >$450bn related obligations (JPM 2026-05-11).
- New Data-Center index sub-sector ($49bn par; 181bp vs Tech 101bp).
- HY HPC supply surge (43% of non-refi HY YTD; index weight 1.07%→2.68%).
- Funding channel extending bonds → leveraged loans (CRWV).

## Active Core Themes
- [[ai-capex-funding-credit-ecosystem]] (case) — core_theme_candidate
- [[hyperscaler-project-bond-basis]] (case) — core_theme_candidate
- [[hy-hpc-crowding-and-supply]] (case) — core_theme_candidate
- [[data-center-index-inclusion-technicals]] (case) — core_theme_candidate

## Active Hot Topics
- AI capex as a credit story; HY HPC outperformance (+9.99% vs +1.61%) — standing crowding confounder.

## Strategy-Family Priors (this source)
1. [[long_short]] (related-obligation RV) · 2. [[index_index_rv]] · 3. [[etf_basket_rv]] ·
4. [[curve]] (secondary watchlist) · 5. [[outright]] (only if downstream beta confirms) · [[watchlist_only]].

## Themes Missing Evidence
- _(none — all four link evidence atoms `jpm-2026-05-11-*`.)_

## Themes Missing Operational Axes
- _(none — all four carry at least one named differential axis.)_

## Themes Missing Falsifiers
- _(none — all four carry ≥1 falsifier.)_

## Themes Ready for Strategy-Family Routing
- All four have axis + falsifier + family priors, BUT they are **source-suggested, not engine-routed**
  (no fresh discovery run). Re-route through `run_workflow(mode="discovery")` to promote to
  `strategy_family_routed`.

## Themes Ready for Downstream Models
- _(none — all are pre-downstream: differentials unverified-clean, no scenarios, no liveness check.)_

## Open items
- Add `memory-map` to `engine.memory` skip-set (or keep method-with-caveat).
- Build the clean-differential series + duration/rating netting before any RV promotion.
