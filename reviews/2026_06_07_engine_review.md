# Code Review Report

**Files reviewed:** `engine/discovery.py`, `engine/workflow.py`, `engine/firewall.py`, `engine/memory.py`, `engine/case_loader.py`, `engine/stage0.py`, `engine/engine2.py`, `engine/schema.py`, `engine/cases.py`
**Date:** 2026-06-07
**Overall health:** 🟡 Needs attention

## Executive Summary

The engine is correctness-disciplined where it matters most — the golden-mastered quant core
(`engine2`, scoring) and the two firewalls are sound. The dominant correctness issue is in the
new discovery layer: one of the six advertised confidence factors (`purity`) is **structurally
constant at 1.0**, so the decomposed-confidence model is effectively five factors, not six.
A second cluster is *reachability* — a documented cap and five declared strategy families can
never fire/route through the real pipeline. Top priority: fix or remove the tautological
`purity` factor so confidence means what the schema says it means.

## Findings

### CR-BUG-001: `purity` confidence factor is tautologically 1.0 (dead multiplicand)
- **Severity:** 🟠 Major
- **Pillar:** Correctness
- **Location:** `engine/discovery.py:207-211`

BEFORE:
```python
family_pnl = [m for m in axis_moves]   # the routed family tracks the axis directly
purity = compute_purity(family_pnl, axis_moves)
...
purity = 1.0                            # no scenarios to assess tracking against
```

AFTER:
```python
# purity must reflect the family's IMPERFECT tracking of the axis, not a copy of it.
# e.g. project the family's monetisation through its hedge/leg structure, or drop the
# factor from the product and from ConfidenceComponents until it can vary.
purity = compute_purity(family_monetisation(family, axis_moves), axis_moves)
```

WHY: `family_pnl` is an exact copy of `axis_moves`, so `compute_purity` returns 1.0 every
time (verified). The `confidence = causal × axis_fit × edge × purity × data` product therefore
has a factor that can never discriminate between a clean and a noisy expression — the schema
advertises a six-component breakdown but `purity` carries no information. Either feed it a
realistic (imperfect) family P&L series, or remove it and document a five-factor product.

### CR-BUG-002: `pre_screen_score` subtracts a mean from a count (scale mismatch)
- **Severity:** 🟡 Minor
- **Pillar:** Correctness
- **Location:** `engine/stage0.py:45-99` (`_evidence_score` returns a count; `_attention_score` returns a mean; `rank_candidates` computes `ev - att`)

BEFORE:
```python
return float(len(linked))                      # evidence: an unbounded COUNT
...
return sum(abs(s.attention_strength) for s in linked) / len(linked)   # attention: a MEAN
...
"pre_screen_score": round(ev - att, 4),        # count − mean
```

AFTER:
```python
# put both on the same scale before differencing, e.g. normalise evidence to a
# recency-weighted intensity in [0, ~1] so (evidence − attention) is dimensionally sound
```

WHY: subtracting a bounded mean (`att`) from an unbounded count (`ev`) makes the ranking
dominated by how many observations a theme links, not by the evidence-vs-attention divergence
the docstring promises. This is an acknowledged proxy stub, but the scale mismatch will bias
any real use. `[SUGGEST: add a test pinning the intended ordering on a count-vs-strength case]`

### CR-TYPE-001: `Optional` used in annotation but never imported in `case_loader.py`
- **Severity:** 🟡 Minor
- **Pillar:** Types
- **Location:** `engine/case_loader.py:12,22`

BEFORE:
```python
from typing import Union          # line 12 — Optional NOT imported
...
hist_freq: Optional[list[Optional[float]]] = None   # line 22
```

AFTER:
```python
from typing import Optional, Union
```

WHY: it only works because `from __future__ import annotations` turns the hint into a string,
so it's never evaluated. Any `typing.get_type_hints(resolve_prior)` (introspection, doc tools,
a future validator) raises `NameError`. One-line, zero-risk fix.

### CR-BUG-003: the "no current market value" cap is unreachable through `run_workflow`
- **Severity:** 🟡 Minor
- **Pillar:** Correctness
- **Location:** `engine/workflow.py` (`_strategy_families` passes `has_market_value=ctx.x_mkt is not None`); `engine/protocols.py` (`RunContext.x_mkt: float`); `engine/discovery.py:223-228`

BEFORE:
```python
has_market_value=ctx.x_mkt is not None,   # ctx.x_mkt is a required float ⇒ always True
```

AFTER:
```python
# either make x_mkt Optional[float] so a missing market value is representable,
# or drop the edge_survival="unknown"/0.60 cap as dead in the real pipeline
```

WHY: `RunContext.x_mkt` is a non-optional `float`, so `has_market_value` is always `True` from
the workflow. The documented `edge_survival="unknown"` / 0.60-ceiling behaviour can only be
exercised by calling `select_strategy_families` directly (as the unit tests do) — it can never
fire in production. The behaviour and the reachable state space disagree.

### CR-SOLID-001: 5 of the 14 declared strategy families are unreachable by routing
- **Severity:** 🟡 Minor
- **Pillar:** SOLID (dead surface)
- **Location:** `engine/discovery.py:_route_family` (returns 9 families) vs `engine/schema.py` `StrategyFamilyRec.family` (declares 14)

BEFORE:
```python
# routable: steepener, flattener, long_short, cash_cds_basis, credit_vs_equity,
#           credit_vs_rates, volatility_convexity, outright, watchlist_only  (9)
# never routed: curve, sector_rotation, capital_structure, etf_basket_rv, index_index_rv (5)
```

AFTER:
```python
# add routing rules (shape/direction or sub-shape signatures) for the 5 missing families,
# OR narrow the Literal to what routing can actually produce until the rules exist
```

WHY: the Literal advertises 14 families and the wiki seeds 14 pages, but `_route_family` can
only ever emit 9. A reader/operator will reasonably expect a `capital_structure` or
`etf_basket_rv` route to exist. Not a crash (watchlist fallback covers gaps), but the declared
taxonomy overstates capability.

### CR-DRY-001: the routable-theme axis invariant is restated in ~4 places
- **Severity:** 🔵 Suggestion
- **Pillar:** DRY
- **Location:** `engine/schema.py:190`, `engine/schema.py:699`, `engine/workflow.py:264`, `engine/llm_provider.py:97-103`

WHY: "a promoted/routed `kind=='theme'` node must have `axis is not None and axis_operational`"
is hand-written at four sites with different predicate ordering. (Cross-references
AR-DRY-001 in the architecture review.) Centralise as one predicate the four sites call.

### CR-TYPE-002: snapshot hash includes volatile `id`/`created_at`
- **Severity:** 🔵 Suggestion
- **Pillar:** Correctness
- **Location:** `engine/firewall.py:44-46` (`_hash_theme` over `theme.model_dump_json()`)

WHY: `ThemeObject.id` (uuid4) and `created_at` (now) are part of the hashed JSON, so two
*identical* fresh reasonings produce different `content_hash` values across runs. This is fine
for the firewall's purpose (detecting post-freeze mutation of a given object) but makes the
hash unusable for "are these two reasonings the same?" Consider hashing a canonical subset
(the causal object + routed families) if cross-run comparison is ever wanted, and document the
choice either way.

### CR-PERF-001: `compute_omega` divides by `len` without guarding empty input
- **Severity:** 🔵 Suggestion
- **Pillar:** Correctness
- **Location:** `engine/engines.py` `compute_omega` (`w = np.ones(len(arr)) / len(arr)`)

WHY: an empty `pnl_series` yields a divide-by-zero / NaN weight vector rather than a clear
error. No current caller passes empty, but a one-line guard (`if not pnl_series: raise/return`)
makes the failure explicit. `[SUGGEST: add a test for the empty-series boundary]`

## Summary Table

| Finding ID | Severity | Pillar | Location | Finding |
|------------|----------|--------|----------|---------|
| CR-BUG-001 | 🟠 Major | Correctness | discovery.py:207-211 | `purity` factor is tautologically 1.0 — a dead multiplicand in the confidence product |
| CR-BUG-002 | 🟡 Minor | Correctness | stage0.py:45-99 | `pre_screen_score` subtracts an attention MEAN from an evidence COUNT (scale mismatch) |
| CR-TYPE-001 | 🟡 Minor | Types | case_loader.py:12,22 | `Optional` used in annotation but not imported (works only via future-annotations) |
| CR-BUG-003 | 🟡 Minor | Correctness | workflow.py / protocols.py | "no market value" cap unreachable — `RunContext.x_mkt` is a required float |
| CR-SOLID-001 | 🟡 Minor | SOLID | discovery.py vs schema.py | 5 of 14 declared families (curve, sector_rotation, capital_structure, etf_basket_rv, index_index_rv) are never routed |
| CR-DRY-001 | 🔵 Suggestion | DRY | schema.py:190,699 / workflow.py:264 / llm_provider.py:97 | Routable-theme axis invariant duplicated across ~4 sites |
| CR-TYPE-002 | 🔵 Suggestion | Correctness | firewall.py:44 | Snapshot hash includes volatile `id`/`created_at`; identical reasonings hash differently across runs |
| CR-PERF-001 | 🔵 Suggestion | Correctness | engines.py `compute_omega` | No empty-input guard before dividing by `len` |

## Positive Highlights

1. **The quant core is genuinely careful** — `solve_q_tilt` checks strict-interior feasibility
   before solving and returns `INFEASIBLE` rather than fabricating `q`; `compute_edge_mc` uses
   `SeedSequence.spawn` for order-independent reproducibility. These are the right instincts
   for numerical code.
2. **The firewall is fail-closed and auditable** — `MemoryRetriever` refuses non-method pages
   in phase A and logs `frozen_before_read` per access, so the freeze-before-history ordering
   is verifiable from the audit log, not just asserted.
3. **Error paths raise with context** — `LLMProvider.expand_causal` and the discipline gates
   raise `ValueError` with the offending content/reason rather than failing silently, which is
   exactly the bias an epistemic engine should have.

## Handoff

| Severity | Pillar | Location | Finding | Finding ID |
|----------|--------|----------|---------|------------|
| 🟠 Major | Correctness | discovery.py:207-211 | `purity` factor is tautologically 1.0 (family_pnl == axis_moves), a dead multiplicand in the six-factor confidence product | CR-BUG-001 |
| 🟡 Minor | Correctness | stage0.py:45-99 | `pre_screen_score` = evidence COUNT − attention MEAN; dimensionally inconsistent ranking | CR-BUG-002 |
| 🟡 Minor | Types | case_loader.py:12,22 | `Optional` referenced in `resolve_prior` annotation but not imported; breaks `get_type_hints` | CR-TYPE-001 |
| 🟡 Minor | Correctness | workflow.py / protocols.py `RunContext.x_mkt` | "no current market value" cap / `edge_survival="unknown"` unreachable because x_mkt is a required float | CR-BUG-003 |
| 🟡 Minor | SOLID | discovery.py `_route_family` vs schema.py family Literal | curve, sector_rotation, capital_structure, etf_basket_rv, index_index_rv are declared but never routable | CR-SOLID-001 |
| 🔵 Suggestion | DRY | schema.py:190,699 / workflow.py:264 / llm_provider.py:97 | Routable-theme operational-axis invariant restated in ~4 places | CR-DRY-001 |
| 🔵 Suggestion | Correctness | firewall.py:44 | `_hash_theme` includes volatile `id`/`created_at`; identical reasonings hash differently across runs | CR-TYPE-002 |
| 🔵 Suggestion | Correctness | engines.py `compute_omega` | No empty-`pnl_series` guard before dividing by `len` | CR-PERF-001 |
