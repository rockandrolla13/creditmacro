# Wiki Index

The persistent memory layer for the investment-research agent. Pages are the
generated/maintained layer over the **immutable** raw sources in `markdowns/` (raw
sources are never modified). See `wiki/CONVENTIONS.md` for required frontmatter and the
investment-process lint checks.

Each entry should eventually carry: a wikilink, a one-line description, a source count
(where applicable), and a status.

## Sources
<!-- [[slug]] — one-line — N sources — status -->

## Entities
<!-- [[slug]] — one-line — status -->

## Concepts
<!-- [[slug]] — one-line — status -->

## Themes
<!-- [[slug]] — one-line — theme_status -->

## Scenarios
<!-- [[slug]] — one-line — status -->

## Strategy Families
The 9 families the discovery router can currently produce (mirrors `StrategyFamilyRec.family`).
Additional families (curve, sector_rotation, capital_structure, etf_basket_rv, index_index_rv)
will be added back as their routing rules are implemented.
- [[steepener]] — long the curve slope (curve, steeper) — active
- [[flattener]] — short the curve slope (curve, flatter) — active
- [[long_short]] — relative-value pair (exposed vs control) — active
- [[outright]] — directional level view — active
- [[cash_cds_basis]] — cash bond vs CDS basis — active
- [[credit_vs_equity]] — cross-asset credit vs equity — active
- [[credit_vs_rates]] — cross-asset credit vs rates — active
- [[volatility_convexity]] — option / convexity expression — active
- [[watchlist_only]] — no tradeable family yet (route, don't fail) — active

## Models
<!-- [[slug]] — one-line — status -->
