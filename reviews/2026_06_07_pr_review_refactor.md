# PR Review — Refactor & SHRINK (read-only)

**Date:** 2026-06-07
**Scope:** `engine/` (incl. `engine/schema/`), `tests/`, `cases/`, `wiki/`
**Baseline:** engine 4,096 LOC + tests 2,403 LOC = 6,499 LOC. Downstream cut target ≥ 20 % (~1,300 LOC).
**Constraint:** behaviour-preserving; 186 tests stay green; golden master pinned (`scenario_fv=75.0`, `residual_edge=20.0`, best score `3.918220233274124`).

## Sizing reality (verified, tokenised line classification)

Of the 6,499 LOC, only **4,089 are executable code**; **1,088 are comments/docstrings** and **1,322 are blank lines** (PEP-8 spacing). This matters: the 20 % target is roughly the *entire* prose budget. Dead-code + dedup wins alone (PR-001…006 below ≈ 300 LOC) cannot reach 1,300 — the bulk **must** come from disciplined docstring/comment tightening (PR-007) and shared fixtures. I do **not** recommend compressing blank lines (hurts readability, not real code).

Top prose-heavy files (comment+docstring lines): `stage0.py` 100, `engine2.py` 64, `prompts.py` 62, `schema/theme.py` 51, `discovery.py` 48, `workflow.py` 48, `firewall.py` 46, `cases.py` 41.

---

## Findings

### PR-001 🟠 Dead back-compat shim `solve_max_entropy_q`
**Location:** `engine/engine2.py:157-167` (+ module-docstring mention `:21-23`)
**Issue:** `solve_max_entropy_q` is a thin shim over `solve_q_tilt`. Grep across `engine/` and `tests/` finds **zero call sites** — `run_pricing`, `compute_edge_mc`, discovery, and every test call `solve_q_tilt`/`level_constraint` directly. It is pure vestigial back-compat for a caller that no longer exists.
**Fix:** Delete the function and trim the `solve_max_entropy_q` sentence from the module docstring.
**Est. LOC saved:** ~12

### PR-002 🟠 SLSQP "cross-validation reference" `_solve_max_entropy_slsqp` + its sole test
**Location:** `engine/engine2.py:170-197` (28 LOC) and `tests/unit/test_solve_q_tilt.py:68-74`
**Issue:** Self-documented as "RETAINED ONLY as a cross-validation reference… Not used in the pipeline." Its **only** consumer is `test_matches_slsqp_solver`, which cross-checks the closed-form tilt against SLSQP. The closed-form `solve_q_tilt` is already pinned by the golden master and by `test_k1_reproduces_golden_q`, so the SLSQP path is redundant validation. Removing both also drops the now-unused `minimize` import (`engine2.py:32`).
**Fix:** Delete `_solve_max_entropy_slsqp`, delete `test_matches_slsqp_solver`, and change `from scipy.optimize import brentq, minimize` → `import brentq`.
**Est. LOC saved:** ~28 engine + ~7 test = **~35**

### PR-003 🔴 Externalize the 168-line MEMO f-string in `example.py`
**Location:** `engine/example.py:166-333` (the `MEMO = f"""…"""` block); file is 382 LOC total.
**Issue:** The worked-example decision memo is a single ~168-line f-string — a static documentation artifact. Verified that **no test asserts on its text**: `test_golden_master` imports structured objects (`pricing`, `theme`, `score_val`, …); `test_iceberg_wiring` imports `CANDIDATE/observations/signals`; `test_workflow`/`test_french_banks` only assert `isinstance(memo, str) and memo.strip()` on the *workflow* memo, not this one. The engine already has a compact production memo renderer (`workflow._render_memo`), so this elaborate Q1–Q13 narration is demo-only.
**Fix:** Move the template to `engine/templates/ai_issuance_memo.md` and render via `str.format(**ns)`; precompute the few inline-expression locals (`COST_STEEPENER/EXPECTED_PNL_STEEPENER`, the `chr(10).join(...)` open-questions list, the scenario/falsifier row joins). The template file is not counted against the engine LOC baseline.
**Est. LOC saved:** ~150 (engine)

### PR-004 🟠 Test DRY — a `conftest.py` build-theme helper + `cases_dir` fixture
**Location:** 8 test files. The exact pattern
`case = load_case(p); theme, _ = run_workflow(ScriptedProvider(case), case.resolved_policy(), mode="expression")`
appears **24×** (verified count); the cases-dir literal `Path(__file__).resolve().parents[2] / "cases"` is redefined **9×** (as `CASE_DIR`/`CASES_DIR`/`CASES`/`ROOT`/`CASE`); `ALL_CASES = sorted(CASES.glob("*.yaml"))` is duplicated in `test_causal_stage.py:19` and `test_system_stages.py:102`.
**Fix:** Add `tests/conftest.py` exposing a `cases_dir` fixture and `build_theme(name, mode="expression") -> ThemeObject` (and reuse `runner.discover_cases`). Each call-site collapses from 2–3 lines to 1; path literals and glob duplicates vanish.
**Est. LOC saved:** ~45 (test)

### PR-005 🟡 Redundant full-workflow re-runs in the parametrized oracle suite
**Location:** `tests/integration/test_cases.py:47-81`
**Issue:** `test_case_builds_theme`, `test_case_invariants_floor_all_pass`, `test_case_oracle_all_pass`, and `test_run_case_combines_floor_and_oracle` each independently re-run `run_workflow` per case (4 full pipeline builds per case). The first three are subsumed by `runner.run_case`, which already returns `(case, theme, floor+oracle results)`.
**Fix:** Collapse to a single parametrized test that calls `run_case(path)` once and asserts `isinstance(theme, ThemeObject)`, `FLOOR_NAMES <= names`, and no failures. Keep the focused negative tests (`test_floor_catches_*`) as-is.
**Est. LOC saved:** ~20 (test) — plus a ~4× speedup on the parametrized suite.

### PR-006 🟡 Consolidate the re-declared canonical AI-issuance fixture data
**Location:** `tests/unit/test_solve_q_tilt.py:20-24`, `test_edge_mc.py:22-29`, `test_pricing_wiring.py:10-19`, `test_fair_value.py:22-30`, `test_strategy_families.py:18-51`
**Issue:** The same canonical vectors are hand-rebuilt in ≥5 files: probabilities `[0.40,0.35,0.15,0.10]`, axis values `[95,75,45,40]`, `x_mkt=55`, names `["AI Surge","Base","Risk-Off","Capex Pause"]`, golden q `[0.125512,0.184417,0.328452,0.361619]`, plus near-identical `_scenarios()`/`_axis()`/`_curve_axis()` builders.
**Fix:** Put the constants + an `ai_scenarios()` / `curve_axis()` builder in `tests/conftest.py` (alongside PR-004) and import. Note `test_system_map_schema._axis` and `test_causal_schema._axis` are also duplicates that fold in here.
**Est. LOC saved:** ~40 (test)

### PR-007 🟠 Tighten duplicated design-narrative docstrings/comments (the largest bucket)
**Location:** module + class docstrings across `engine/` — notably `engine2.py:1-24` (the MATHEMATICS block partly restated at `solve_q_tilt`, `compute_edge_mc`, `run_pricing`), `cases.py:1-16` + per-class DESIGN NOTES, `schema/theme.py:24-42`/`87-104` status-enum prose, `stage0.py` (100 prose lines), `workflow.py`, `firewall.py`, `runner.py:1-16`. Much of this restates `docs/engine2_design.md` and `reviews/2026_06_06_architecture_review.md` (the `AR-xxx` tags are pointers back to those docs) and is duplicated between a module header and the functions it documents.
**Issue:** 1,088 of 6,499 LOC are comments/docstrings. A large fraction is multi-paragraph rationale that belongs in (and already exists in) the design docs, not inline. This is the only lever large enough to approach the 20 % target.
**Fix:** Keep one-line "what + contract" docstrings; move multi-paragraph "why/derivation/AR-rationale" to the design docs they already cite. Conservatively tighten the prose budget by ~40 %.
**Est. LOC saved:** ~400 (engine) — *lower-confidence / subjective; behaviour-neutral but reviewer-judgment-bound.*

### PR-008 🔵 Generate the hand-maintained wiki strategy-family pages
**Location:** `wiki/strategy-families/*.md` (9 files)
**Issue:** Each page restates data fully derivable from the engine: `StrategyFamilyRec.family` Literal (`schema/strategy_family.py:47-50`) + the `_DOWNSTREAM`/routing templates in `discovery.py`. The pages even say "This page mirrors the engine taxonomy." Hand-maintaining them risks drift from the single source of truth.
**Fix:** Emit them from a small generator over the engine taxonomy. **Counts 0 toward the 6,499 baseline** (wiki is outside engine+tests LOC) — this is a maintenance/drift win, not a LOC cut against target.
**Est. LOC saved:** 0 (toward target); removes 9 hand-maintained files.

---

## Notes on things that are NOT dead (verified, do not cut)
- `engine/prompts.py`, `engine/llm_provider.py` — the live `CausalExpander` seam; exercised by `test_expand_causal.py`. Real, not vestigial.
- `engine/outcomes.py` — contract module with its own tests (`test_outcomes.py`).
- `option_constraint` / K>1 Newton branch in `engine2.py` — exercised by `test_k2_*` in `test_solve_q_tilt.py`. Keep.
- `scenario_fair_value` — used by `run_pricing` and pinned by the golden master. Keep.
- `scripted_provider.py` pass-through seams — each returns a distinct CaseSpec slice; not collapsible without breaking the `Provider` protocol contract.

---

## Handoff

| Finding | Severity | Location | Est. LOC saved | Summary |
|---|---|---|---:|---|
| PR-001 | 🟠 | `engine/engine2.py:157-167` | 12 | Delete unused `solve_max_entropy_q` back-compat shim (zero callers). |
| PR-002 | 🟠 | `engine/engine2.py:170-197` + `tests/unit/test_solve_q_tilt.py:68-74` | 35 | Drop SLSQP cross-check fn + its only test + the `minimize` import. |
| PR-003 | 🔴 | `engine/example.py:166-333` | 150 | Externalize the 168-line worked-example MEMO f-string to a template; not test-asserted. |
| PR-004 | 🟠 | 8 test files (24 call-sites, 9 path defs) | 45 | Add `conftest.py` `build_theme()` helper + `cases_dir` fixture to kill repeated load/run boilerplate. |
| PR-005 | 🟡 | `tests/integration/test_cases.py:47-81` | 20 | Collapse 4 per-case parametrized tests that each re-run the workflow into one `run_case` call. |
| PR-006 | 🟡 | 5 unit test files | 40 | Hoist re-declared AI-issuance vectors + `_scenarios`/`_axis` builders into shared fixtures. |
| PR-007 | 🟠 | docstrings across `engine/` (engine2, cases, stage0, theme, workflow, firewall, runner) | 400 | Tighten duplicated design-narrative prose (~1,088 prose LOC); push rationale to design docs. |
| PR-008 | 🔵 | `wiki/strategy-families/*.md` (9 files) | 0 | Generate from engine taxonomy instead of hand-maintaining (drift risk; outside LOC baseline). |

**Sum of estimated LOC saved (toward the 6,499 baseline): ~702 LOC (~10.8 %).**

**Reaching the full 20 % (~1,300):** PR-001…006 are high-confidence and total ~302 LOC. The gap is closable **only** through PR-007-style prose tightening — the 400-LOC estimate is deliberately conservative (~37 % of the 1,088 comment/docstring lines); an aggressive pass nearer ~60 % would add ~250 more and bring the total to ~950–1,000. A clean 1,300 is not achievable behaviour-neutrally without either compressing PEP-8 blank lines (not recommended) or merging modules (structural change, out of "shrink-without-behaviour-change" scope). Recommend the downstream plan treat ~1,000 LOC (~15 %) as the realistic behaviour-preserving ceiling and renegotiate the 20 % target.
