# PLAN: Engine Shrink ≥20%

**Source roadmap:** `reviews/2026_06_07_refactoring_plan_v2.md`
**Goal:** engine+tests 6,499 → ≤5,200 LOC (−20%), 186 tests + golden master green at every step.

## Pre-execution snapshot
- engine 4,096 + tests 2,403 = **6,499 LOC** · 186 tests pass · golden master 75.0/20.0/3.918…

## Status

| Step | Description | Finding IDs | Status | LOC | Notes |
|---|---|---|---|---:|---|
| 1.1 | excise dead max-entropy code+test | PR-001/002, CR-STYLE-001/002 | PENDING | 52 | |
| 1.2 | micro-dead bits | CR-STYLE-003/004 | PENDING | 5 | |
| 2.1 | delete untested worked-example memo | PR-003, CR-SOLID-001 | PENDING | 165 | |
| 3.1 | extract _causal_stage | CR-DRY-004 | PENDING | 22 | |
| 3.2 | edge-attr helper + best_expression() | CR-DRY-005/006 | PENDING | 20 | |
| 4.1 | conftest.py fixtures | PR-004, CR-DRY-001/002/003/007 | PENDING | — | |
| 4.2 | migrate + collapse tests | PR-004/005/006, CR-DRY-* | PENDING | 250 | |
| 5.1 | tighten prose + blanks (gap-closer) | PR-007 | PENDING | 785 | |

Target total ≈ 1,299 LOC (−20.0%).

## Outcome (executed)
| Step | Status | Note |
|---|---|---|
| 1.1 dead max-entropy code+test | DONE | zero-caller fns + SLSQP + test + import removed |
| 1.2 micro-dead bits | DONE | unused alias; `_expand_bracket` helper |
| 2.1 delete untested memo | DONE | example.py 382→155; reuses tested workflow memo |
| 3.1 extract _causal_stage | DONE | shared by both runners; firewall behaviour preserved |
| 3.2 edge-attr helper + best_expression() | DONE | engine2 `_edge_attribution`; `ThemeObject.best_expression()` |
| 4.1 shared test helpers | DONE | `tests/_helpers.py` (build_theme, golden consts, oracle assert) |
| 4.2 migrate tests | DONE | all clean sites migrated to _helpers (french_banks/workflow/causal_stage/discovery_firewall/cases/loop_stage); special-cased sites (custom providers, model_copy) left; structural DRY win, LOC ~neutral due to _helpers fixed cost |
| 5.1 prose tightening | STOPPED | trimmed the worst stub docstring only; declined scorched-earth |

**Result: 6,499 → 6,190 LOC = −309 (−4.8%), 185 tests green, golden master intact, zero behaviour change.**
**20% NOT reached** — by design decision: the remaining ~15% is pure docstring/comment deletion that both reviewers flagged as removing genuine design value. Awaiting user call on whether to proceed with that.
