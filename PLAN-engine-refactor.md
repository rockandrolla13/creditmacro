# PLAN: Engine Refactor (post-review)

**Source roadmap:** `reviews/2026_06_07_refactoring_plan.md`
**Forks:** CR-BUG-001→A · CR-BUG-003→A · CR-SOLID-001→B · AR-ABS-002→B

## Pre-execution snapshot
- Engine modules: 18 · Engine LOC: 4059
- Tests: **178 passed** (~6s)
- Baseline scores: Boundaries 🟠 · Dependencies 🟢 · Abstraction 🟡 · DRY 🟡 · Extensibility 🟡 · Testability 🟡 · Parallelisation 🟡

## Status

| Step | Description | Finding IDs | Status | Notes |
|---|---|---|---|---|
| 1.1 | purity varies (family-monetisation) | CR-BUG-001 | DONE | _family_monetisation + _TRACKING_FIDELITY; 179 green |
| 1.2 | centralise routable-theme invariant | AR-DRY-001, CR-DRY-001 | DONE | CausalNode.is_routable(); 1 def, 4 callers |
| 1.3 | hash subset + micro-fixes | CR-TYPE-001/002, CR-PERF-001, AR-ABS-002 | DONE | hash excludes id/created_at/last_updated; omega guard; Optional import; 182 green |
| 2.1 | x_mkt Optional | CR-BUG-003 | DONE | RunContext/CaseSpec Optional; expression guards; 184 |
| 2.2 | narrow family Literal | CR-SOLID-001 | DONE | 14→9 families; 5 wiki pages removed; 185 |
| 2.3 | LLMProvider → CausalExpander | AR-ABS-001 | DONE | new CausalExpander protocol; 186 |
| 3.1 | split engines + drop stubs | AR-BND-002, AR-EXT-001 | DONE | engines.py→scoring.py; 5 stubs deleted; facade dropped; 186 |
| 3.2 | build_example() | AR-TST-001 | DONE | lazy cached build + PEP562 __getattr__; import side-effect-free; 186 |
| 4.1 | schema → package | AR-BND-001 | DONE | schema.py(732)→schema/ pkg of 9 submodules; __init__ re-exports; all 28 importers unchanged; 186 |

## Outcome (all 9 steps DONE)
- Tests: 178 → **186 passed**; golden master 75.0/20.0/3.918… unchanged throughout.
- Scores: Boundaries 🟠→🟢 · Dependencies 🟢→🟢 · Abstraction 🟡→🟢 · DRY 🟡→🟢 · Extensibility 🟡→🟢 · Testability 🟡→🟢 · Parallelisation 🟡 (deferred, AR-PAR-001).
- Deferred (stated in roadmap): AR-PAR-001, CR-BUG-002, AR-DEP-002.
