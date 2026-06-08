# Lint Status

Tracks lint progress over source pages. Lint runs in **batches of 5 sources per session**.

The order is **randomised once with seed 42** to break topic clustering, then **stored
permanently** — never reshuffled between sessions. Checkboxes:

- `[ ]` not yet linted
- `[x]` linted (for a source: done; for a hub page: all contributing sources done)
- `[~]` hub page partially linted (some contributing sources still `[ ]`)

## How this list is built (run once, when source pages first exist)

Deterministic so it reproduces exactly:

```python
import random
from pathlib import Path
slugs = sorted(p.stem for p in Path("wiki/sources").glob("*.md"))  # stable input order
random.Random(42).shuffle(slugs)                                   # randomise ONCE, seed 42
# write slugs in this order as "- [ ] [[slug]]" under "## Source order (seed 42, frozen)"
```

## Source order (seed 42, frozen)

_Built 2026-06-08 (1 source page existed). The seed-42 shuffle of a single slug is itself.
When more sources are added, extend this frozen list — do not reshuffle existing entries._

- [x] [[jpm-ai-capex-funding-2026-05-11]]  — Batch 1, 2026-06-08

## Hub pages (entities / concepts / themes touched during lint)

All 17 pages linked by the batch-1 source have exactly one contributing source (now linted) →
`[x]`. Notable fix: the concept below was renamed to match its declared slug.

- [x] [[hyperscaler-project-bond-basis-mechanics]] — concept; renamed from `…-bond-basis.md`
  (filename ≠ slug, collided with the theme); all inbound `…-mechanics` links now resolve.
- [x] themes: [[ai-capex-funding-credit-ecosystem]], [[hyperscaler-project-bond-basis]],
  [[hy-hpc-crowding-and-supply]], [[data-center-index-inclusion-technicals]]
- [x] concepts: [[data-center-credit]], [[high-performance-computing-credit]],
  [[index-inclusion-technical]], [[limited-syndication]], [[144a-for-life]], [[related-obligation-rv]]
- [x] strategy-families: [[long_short]], [[index_index_rv]], [[etf_basket_rv]], [[curve]],
  [[cash_cds_basis]], [[outright]], [[watchlist_only]]

## Deferred (not yet contributed by any linted source)

- [ ] `engines/` (9 pages) — absent from `index.md`; needs a dedicated pass + an index Engines
  section. See lint-scratch Batch 1 → Cross-cutting.
