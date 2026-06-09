# Wiki Index

The persistent memory layer for the investment-research agent. Pages are the
generated/maintained layer over the **immutable** raw sources in `markdowns/` (raw
sources are never modified). See `wiki/CONVENTIONS.md` for required frontmatter and the
investment-process lint checks.

Each entry should eventually carry: a wikilink, a one-line description, a source count
(where applicable), and a status.

## Sources
<!-- [[slug]] — one-line — N sources — status -->
- [[jpm-ai-capex-funding-2026-05-11]] — JPM AI-capex funding credit data — **case** — ingested

## Evidence atoms
<!-- materialized source-backed atoms; CASE memory; theme-card evidence links resolve here -->
- [[evidence:jpm-2026-05-11-001]] … [[evidence:jpm-2026-05-11-015]] — 15 JPM atoms (`wiki/evidence/`, mirrored in `evidence_atoms.jsonl`) — **case**

## Entities
<!-- [[slug]] — one-line — status -->

## Concepts
<!-- [[slug]] — one-line — status -->
- [[data-center-credit]] — DC corporate/project/ABS credit — active
- [[high-performance-computing-credit]] — HY HPC/neocloud credit — active
- [[hyperscaler-project-bond-basis-mechanics]] — hyperscaler-vs-project basis (mechanic) — active
- [[index-inclusion-technical]] — index-inclusion demand technical — active
- [[limited-syndication]] — narrow placement / liquidity caveat — active
- [[144a-for-life]] — 144A index-eligibility flag — active
- [[related-obligation-rv]] — RV across common-driver obligations — active

## Themes
<!-- [[slug]] — one-line — theme_status -->
- [[ai-capex-funding-credit-ecosystem]] — AI-credit complex as related obligations — **case** — core_theme_candidate
- [[hyperscaler-project-bond-basis]] — hyperscaler-vs-project spread RV — **case** — core_theme_candidate
- [[hy-hpc-crowding-and-supply]] — HPC supply + crowding signature — **case** — core_theme_candidate
- [[data-center-index-inclusion-technicals]] — DC index-inclusion technical — **case** — core_theme_candidate

## Scenarios
<!-- [[slug]] — one-line — status -->

## Memory map
- [[memory-map]] — active developments / themes / family priors / readiness — active

## Strategy Families
The 12 families the discovery router can currently produce (mirrors `StrategyFamilyRec.family`).
Remaining wiki-only families (curve, sector_rotation) will be added back as their routing rules
are implemented.
- [[steepener]] — long the curve slope (curve, steeper) — active
- [[flattener]] — short the curve slope (curve, flatter) — active
- [[long_short]] — relative-value pair (exposed vs control) — active
- [[outright]] — directional level view — active
- [[cash_cds_basis]] — cash bond vs CDS basis — active
- [[credit_vs_equity]] — cross-asset credit vs equity — active
- [[credit_vs_rates]] — cross-asset credit vs rates — active
- [[volatility_convexity]] — option / convexity expression — active
- [[etf_basket_rv]] — ETF vs underlying basket / NAV (relative_value sub-type) — active
- [[capital_structure]] — within one issuer: senior/sub/AT1/hybrid (relative_value sub-type) — active
- [[index_index_rv]] — same exposure across index definitions (relative_value sub-type) — active
- [[watchlist_only]] — no tradeable family yet (route, don't fail) — active

Taxonomy pages (knowledge only; **not yet auto-routed** by `engine/discovery._route_family`):
- [[curve]] — generic curve slope (engine routes explicit steepener/flattener) — taxonomy
- [[sector_rotation]] — relative value across credit sectors — taxonomy

## Models
<!-- [[slug]] — one-line — status -->
