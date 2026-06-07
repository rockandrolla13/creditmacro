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
