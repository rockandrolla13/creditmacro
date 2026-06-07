# Code Review Report — Engine + Tests (v2, size-reduction lens)

**Files reviewed:** `engine/` (incl. `engine/schema/*`), `tests/unit/*`, `tests/integration/*`
**Date:** 2026-06-07
**Overall health:** 🟢 Good — correct, well-documented, 186 tests green. The findings below are **structure + size**, not correctness.

## Executive Summary

The codebase is disciplined and the quant core is clean. The size opportunity is concentrated in two places: (1) **the test suite has no `conftest.py`**, so the same `cases/` path constant, the same `load_case → ScriptedProvider → run_workflow` triple, the same AI-issuance scenario builder, and the same golden literals are re-typed across 6–9 files; and (2) **`engine/example.py` carries a 167-line untested memo f-string** that duplicates the responsibility of `workflow._render_memo` (whose output `build_example` already computes and then throws away). A handful of true dead/near-dead functions and two small in-module duplications round it out. Top priority: add a `tests/conftest.py` and trim `example.py`.

**MUST NOT TOUCH (regression firewalls):**
- The golden-master numeric path: `engine2.solve_q_tilt` / `run_pricing` / `scoring.score_expression` and the `build_example()` bundle fields that `test_golden_master` imports (`theme, pricing, expr_steepener, expr_etf_basis, omega_steepener, score_val, sizing`). The pins `scenario_fv=75.0`, `residual_edge=20.0`, `q_s=[0.125512, 0.184417, 0.328452, 0.361619]`, `best score=3.918220233274124` must hold to 1e-6.
- The memory firewall invariants: `ThemeObject`/`StrategyFamilyRec`/`FrozenSnapshot` `frozen=True`, `_hash_theme` + `_HASH_EXCLUDE`, `MemoryRetriever` fail-closed phase-A, and `freeze()`-before-`advance_to_phase_b()` ordering in `firewall.run_two_phase`. None of the findings below touch these.

All "unused/duplicated" claims below were grep-verified against `engine/` and `tests/`.

---

## Findings

### CR-SOLID-001: `example.py` ships a 167-line untested memo that duplicates `workflow._render_memo`
- **Severity:** 🟠 Major
- **Pillar:** Single Responsibility / Conciseness
- **Location:** `engine/example.py:L124-L345` (the discarded workflow memo at L124; the `MEMO` f-string L166-L333; its feeder locals L142-L164; the namespace fields L335-L345)

BEFORE:
```python
theme, _memo = run_workflow(ScriptedProvider(_case), _case.resolved_policy(), mode="expression")
...
q_s_fmt = ", ".join(f"{q:.3f}" for q in pricing.priced_in.q_s)
scenario_rows = "\n".join(...)        # only the MEMO reads these
falsifier_rows = "\n".join(...)
MEMO = f"""# Decision Memo — AI Issuance ...   # 167 lines, Q1–Q13
... {EXPECTED_PNL_STEEPENER} {RHO2} {LIQUIDITY} {COST_STEEPENER} {COST_ETF} ...
"""
_BUNDLE = SimpleNamespace(theme=..., RHO2=RHO2, COST_ETF=COST_ETF, THEME_JSON=THEME_JSON, MEMO=MEMO, ...)
```

AFTER:
```python
theme, memo = run_workflow(ScriptedProvider(_case), _case.resolved_policy(), mode="expression")
# keep ONLY the names test_golden_master imports; render via the workflow memo
_BUNDLE = SimpleNamespace(
    theme=theme, pricing=theme.pricing, sizing=theme.sizing,
    expr_steepener=_by_id["expr_cds_5s30s"], expr_etf_basis=_by_id["expr_etf_basis"],
    omega_steepener=compute_omega(...), score_val=_by_id["expr_cds_5s30s"].score,
    MEMO=memo,                       # reuse the rendered memo instead of rebuilding it
)
```

WHY: `grep "MEMO\|THEME_JSON" tests` returns nothing — the giant memo and ~10 feeder locals (`RHO2`, `LIQUIDITY`, `COST_STEEPENER`, `COST_ETF`, `EXPECTED_PNL_STEEPENER`, `q_s_fmt`, `scenario_rows`, `falsifier_rows`, `X_MKT`, `NORMAL_FV`) are demo-only output that re-derives what `workflow._render_memo` already returns and `build_example` discards at L124. The detailed Q1–Q13 template, if still wanted, belongs in one renderer (workflow), not duplicated here.
**Estimated LOC saved: ~180**

---

### CR-DRY-001: No `tests/conftest.py` — `cases/` path + `load_case→ScriptedProvider→run_workflow` helper re-defined per file
- **Severity:** 🟠 Major
- **Pillar:** DRY (shared fixtures)
- **Location:** `tests/integration/test_workflow.py:L15,L19-23`, `test_french_banks.py:L14,L17-20`, `test_causal_stage.py:L18,L23-26`, `test_discovery_firewall.py:L26-29,L33-40`, `test_system_stages.py:L25,L62-68`, `test_loop_stage.py:L20`, `test_cases.py`, `tests/unit/test_case_loader.py:L12`, `test_memory_firewall.py:L30`, `test_expand_causal.py:L22`

BEFORE (repeated ~9×):
```python
CASE = Path(__file__).resolve().parents[2] / "cases" / "ai_issuance.yaml"
def _run():
    case = load_case(CASE)
    theme, memo = run_workflow(ScriptedProvider(case), case.resolved_policy(), mode="expression")
    return case, theme, memo
```

AFTER (`tests/conftest.py`, once):
```python
@pytest.fixture(scope="session")
def cases_dir(): return Path(__file__).resolve().parent.parent / "cases"

@pytest.fixture
def run_expression():
    def _run(path):
        case = load_case(path)
        theme, memo = run_workflow(ScriptedProvider(case), case.resolved_policy(), "expression")
        return case, theme, memo
    return _run          # add a sibling run_discovery fixture; ai_case/french_case path fixtures
```

WHY: the `parents[2]/"cases"` literal and the three-call run helper are knowledge duplicated across 6–9 files; `mode="expression"` is typed inline ~18 times. One conftest centralizes them and lets a path change propagate once.
**Estimated LOC saved: ~70**

---

### CR-DRY-002: AI-issuance scenario builder (`_PX` + `_scenarios()`) duplicated across 5 test files
- **Severity:** 🟠 Major
- **Pillar:** DRY (shared fixtures)
- **Location:** `tests/unit/test_pricing_wiring.py:L10-18`, `tests/unit/test_fair_value.py:L17-29`, `tests/unit/test_strategy_families.py`, `tests/integration/test_loop_stage.py`, `tests/unit/test_protocols.py`

BEFORE (in 5 files, near-identical):
```python
_PX = [(0.40, 95.0, "AI Surge"), (0.35, 75.0, "Base"), (0.15, 45.0, "Risk-Off"), (0.10, 40.0, "Capex Pause")]
def _scenarios():
    return [Scenario(name=nm, p_s=p, driver_path="d", implied_axis_value=x, pnl_per_unit=0.0) for p, x, nm in _PX]
```

AFTER (`conftest.py`):
```python
@pytest.fixture
def ai_scenarios():
    def _make(sigma=0.0):
        return [Scenario(name=nm, p_s=p, driver_path="d", implied_axis_value=x, pnl_per_unit=0.0, sigma_g_s=sigma)
                for p, x, nm in _AI_PX]
    return _make
```

WHY: the same four (p, X) tuples and the same `Scenario(...)` construction are the same domain fact repeated five times; they drift independently today (`test_fair_value` adds a `sigma` arg, `test_pricing_wiring` adds names — a parametrizable shared factory covers both).
**Estimated LOC saved: ~30**

---

### CR-DRY-003: Golden-master literals re-typed across the suite
- **Severity:** 🟡 Minor
- **Pillar:** DRY
- **Location:** q-vector `[0.125512, 0.184417, 0.328452, 0.361619]` in `test_golden_master.py:L36`, `test_workflow.py:L36`, `test_cases.py`, `test_pricing_wiring.py:L27`, `test_solve_q_tilt.py`; score `3.918220233274124` in `test_workflow.py:L45`, `test_golden_master.py:L57-58`, `test_cases.py`, `test_discovery_firewall.py:L146`

BEFORE:
```python
assert theme.pricing.priced_in.q_s == pytest.approx([0.125512, 0.184417, 0.328452, 0.361619], abs=ABS)
assert by_id["expr_cds_5s30s"].score == pytest.approx(3.918220233274124, abs=ABS)
```

AFTER (`conftest.py`):
```python
GOLDEN = dict(scenario_fv=75.0, residual_edge=20.0,
              q=[0.125512, 0.184417, 0.328452, 0.361619], score=3.918220233274124, abs=1e-6)
```

WHY: these are one set of pinned constants; re-typing them in 4–5 files invites a transcription drift that would mask a real golden break. Centralize as the single source the pins are read from.
**Estimated LOC saved: ~12**

---

### CR-DRY-004: `_run_discovery` and `_run_expression` share an identical causal/system/critique/loop stage block
- **Severity:** 🟠 Major
- **Pillar:** DRY / Single Responsibility
- **Location:** `engine/workflow.py:L113-L147` vs `L183-L211`

BEFORE (both functions):
```python
thesis = provider.extract_drivers(ctx.statement)
main_theme, causal_chain, shared_factor = provider.expand_causal(ctx.statement, ctx.statement)
if main_theme is not None:
    _validate_causal_chain(main_theme, causal_chain); axis = main_theme.axis
# (discovery: else → blocked; expression: else → provider.define_axis(thesis))
system_map = provider.build_system_map(thesis, causal_chain)
bias_critique = provider.critique_mental_model(ctx.statement, causal_chain)
loop_diagnosis = provider.diagnose_loops(system_map)
scenarios = provider.propose_scenarios(thesis, axis, loop_diagnosis)
```

AFTER:
```python
def _causal_stage(provider, ctx):
    """thesis + expand_causal (+ validate) + system_map + critique + loop_diagnosis."""
    thesis = provider.extract_drivers(ctx.statement)
    mt, chain, shared = provider.expand_causal(ctx.statement, ctx.statement)
    if mt is not None: _validate_causal_chain(mt, chain)
    sm = provider.build_system_map(thesis, chain)
    return thesis, mt, chain, shared, sm, provider.critique_mental_model(ctx.statement, chain), provider.diagnose_loops(sm)
# discovery: mt None → blocked; expression: mt None → axis = provider.define_axis(thesis)
```

WHY: the seven provider calls run in the same order in both modes; only the `main_theme is None` branch differs (block vs `define_axis` fallback). Extracting the shared stage removes the parallel copy and makes the one real difference explicit.
**Estimated LOC saved: ~22**

---

### CR-DRY-005: Edge-attribution build duplicated in `compute_edge_mc` and `run_pricing`
- **Severity:** 🟡 Minor
- **Pillar:** DRY
- **Location:** `engine/engine2.py:L282-L293` vs `L386-L397`

BEFORE (twice, modulo a `round(...)`):
```python
attribution = sorted(
    (EdgeContribution(scenario=names[i], contribution=(p[i]-q[i])*X_s[i], disagreement=p[i]-q[i])
     for i in range(n)),
    key=lambda c: c.contribution, reverse=True,
)
```

AFTER:
```python
def _edge_attribution(p, q, X_s, names, ndigits=None):
    r = (lambda v: round(v, ndigits)) if ndigits else (lambda v: v)
    return sorted((EdgeContribution(scenario=names[i], contribution=r((p[i]-q[i])*X_s[i]),
                                    disagreement=r(p[i]-q[i])) for i in range(len(X_s))),
                  key=lambda c: c.contribution, reverse=True)
```

WHY: identical "build EdgeContribution per scenario, sort by contribution desc" logic in two places; the only difference is whether values are rounded for the persisted `Pricing`. One helper, two call sites.
**Estimated LOC saved: ~12**

---

### CR-STYLE-001: Dead back-compat shim `solve_max_entropy_q`
- **Severity:** 🟡 Minor
- **Pillar:** Conciseness (dead code)
- **Location:** `engine/engine2.py:L157-L167`

BEFORE:
```python
def solve_max_entropy_q(X_s, X_mkt, q0=None) -> list[float]:
    """Back-compat: ... Delegates to solve_q_tilt. prior defaults to uniform."""
    n = len(X_s); prior = q0 if q0 is not None else [1.0/n]*n
    sol = solve_q_tilt(X_s, [level_constraint(X_mkt)], prior)
    if sol.status != "FEASIBLE": raise RuntimeError(...)
    return sol.q
```

AFTER: *(delete — no callers)*

WHY: `grep "solve_max_entropy_q\b"` finds only the definition and its own docstring mention — zero call sites in `engine/` or `tests/`. The pipeline calls `solve_q_tilt` directly.
**Estimated LOC saved: ~11**

---

### CR-STYLE-002: SLSQP cross-validation solver + its single test are removable scaffolding
- **Severity:** 🔵 Suggestion
- **Pillar:** Conciseness (dead-ish code)
- **Location:** `engine/engine2.py:L170-L197` (`_solve_max_entropy_slsqp`) and its only consumer `tests/unit/test_solve_q_tilt.py:L70-72`

BEFORE: a 28-line SLSQP solver "RETAINED ONLY as a cross-validation reference for the closed form," exercised by one cross-check test.

AFTER: keep only if you still want the closed-form/SLSQP agreement guard; otherwise delete the function and that one test assertion.

WHY: it is not used by the pipeline (only by one cross-validation test). It is legitimate belt-and-braces, so this is a judgment call, not a defect — flagged so the roadmap can decide. If kept, leave as-is; if cut, remove both together.
**Estimated LOC saved: ~40 (only if the cross-check is retired)**

---

### CR-DRY-006: "best scored expression" selection re-implemented in 4 places
- **Severity:** 🟡 Minor
- **Pillar:** DRY
- **Location:** `engine/workflow.py:L227-L230`, `engine/cases.py:L111-L113` (ExactOracle), `engine/cases.py:L159-L160` (AcceptanceOracle), `engine/example.py:L145-L147`

BEFORE (repeated):
```python
scored = [e for e in theme.expressions if e.score is not None]
best = max(scored, key=lambda e: e.score) if scored else None
```

AFTER (method on `ThemeObject`, or a `schema` helper):
```python
def best_expression(self) -> Optional[Expression]:
    scored = [e for e in self.expressions if e.score is not None]
    return max(scored, key=lambda e: e.score) if scored else None
```

WHY: "the best expression is the max-score survivor" is one domain rule; centralizing it on the model removes three re-derivations and keeps the tie-break definition single-sourced.
**Estimated LOC saved: ~8**

---

### CR-DRY-007: `failed = [r for r in results if not r.passed]; assert not failed` repeated across oracle tests
- **Severity:** 🔵 Suggestion
- **Pillar:** DRY
- **Location:** `test_workflow.py:L59-60`, `test_french_banks.py:L58-60`, `test_causal_stage.py:L72`, `test_cases.py:L60-61,L69-70,L80-81`

BEFORE:
```python
failed = [r for r in results if not r.passed]
assert not failed, f"oracle failures: {failed}"
```

AFTER (`conftest.py`):
```python
def assert_all_passed(results):
    failed = [r for r in results if not r.passed]
    assert not failed, f"assertion failures: {failed}"
```

WHY: the same "no AssertionResult failed" check appears ~6 times; a shared helper makes the intent one line at each call site.
**Estimated LOC saved: ~7**

---

### CR-STYLE-003: Unused import alias `SystemMap as _SM`
- **Severity:** 🟡 Minor
- **Pillar:** Conciseness (dead import)
- **Location:** `tests/integration/test_system_stages.py:L20`

BEFORE:
```python
from engine.schema import (BiasCritique, Delay, FeedbackLoop, Flow, Stock, SystemMap, SystemMap as _SM)
```

AFTER:
```python
from engine.schema import (BiasCritique, Delay, FeedbackLoop, Flow, Stock, SystemMap)
```

WHY: `grep "_SM"` in that file returns only the import line — the alias is never referenced.
**Estimated LOC saved: ~1**

---

### CR-STYLE-004: Twin manual root-bracketing loops in `solve_q_tilt`
- **Severity:** 🔵 Suggestion
- **Pillar:** Conciseness
- **Location:** `engine/engine2.py:L120-L128`

BEFORE:
```python
lo, hi = -1.0, 1.0
for _ in range(200):
    if resid(lo) < 0: break
    lo *= 2.0
for _ in range(200):
    if resid(hi) > 0: break
    hi *= 2.0
```

AFTER:
```python
def _expand(start, ok):           # double until resid has the wanted sign
    x = start
    for _ in range(200):
        if ok(resid(x)): break
        x *= 2.0
    return x
lo = _expand(-1.0, lambda r: r < 0); hi = _expand(1.0, lambda r: r > 0)
```

WHY: two structurally identical expand-the-bracket loops; one helper expresses the single idea. (Numerically identical — guard against altering the brentq bracket when refactoring, given the golden q.)
**Estimated LOC saved: ~4**

---

## Positive Highlights
- The quant core (`engine2.solve_q_tilt`, `scoring`) is genuinely deep: heavy math documentation, INFEASIBLE returned rather than fabricated, reproducible MC via `SeedSequence.spawn`. Do not dilute these docstrings when shrinking elsewhere.
- The memory firewall (`memory.py` + `firewall.py`) enforces the case/method split by *construction* (fail-closed retriever, hash-before-unlock), which is exactly the right shape — leave it intact.
- The Oracle discriminated union + always-on `invariants_floor` is a clean polymorphic design with no `kind` switch; `discover_cases()` auto-parametrization keeps the case suite DRY at the data layer (the *test-harness* layer is where the duplication crept in — see CR-DRY-001/002/003).

---

## Handoff

| Finding ID | Severity | Pillar | Location | Est. LOC saved | Summary |
|------------|----------|--------|----------|----------------|---------|
| CR-SOLID-001 | 🟠 Major | SRP/Conciseness | engine/example.py:L124-L345 | ~180 | Untested 167-line memo f-string duplicates `workflow._render_memo` (whose output is discarded); keep only the tested bundle. |
| CR-DRY-001 | 🟠 Major | DRY | tests/* (9 files) | ~70 | No conftest: `cases/` path + `load_case→ScriptedProvider→run_workflow` helper re-defined per file. |
| CR-DRY-002 | 🟠 Major | DRY | tests/* (5 files) | ~30 | AI-issuance `_PX`+`_scenarios()` builder duplicated; make one parametrizable fixture. |
| CR-DRY-004 | 🟠 Major | DRY/SRP | engine/workflow.py:L113-211 | ~22 | `_run_discovery`/`_run_expression` share the causal+system+critique+loop block; extract `_causal_stage`. |
| CR-DRY-005 | 🟡 Minor | DRY | engine/engine2.py:L282-397 | ~12 | Edge-attribution build duplicated in `compute_edge_mc` and `run_pricing`. |
| CR-DRY-003 | 🟡 Minor | DRY | tests/* (5 files) | ~12 | Golden q-vector/score literals re-typed in 4–5 files; centralize in conftest. |
| CR-STYLE-001 | 🟡 Minor | Conciseness | engine/engine2.py:L157-167 | ~11 | Dead shim `solve_max_entropy_q` — zero callers. |
| CR-DRY-006 | 🟡 Minor | DRY | workflow/cases/example (4 sites) | ~8 | "best scored expression" re-implemented; add `ThemeObject.best_expression()`. |
| CR-DRY-007 | 🔵 Suggestion | DRY | tests/* (4 files) | ~7 | `assert not failed` oracle pattern repeated; conftest helper. |
| CR-STYLE-003 | 🟡 Minor | Conciseness | tests/integration/test_system_stages.py:L20 | ~1 | Unused import alias `SystemMap as _SM`. |
| CR-STYLE-004 | 🔵 Suggestion | Conciseness | engine/engine2.py:L120-128 | ~4 | Twin manual root-bracketing loops; one `_expand` helper. |
| CR-STYLE-002 | 🔵 Suggestion | Conciseness | engine/engine2.py:L170-197 + test_solve_q_tilt.py:L70 | ~40 (if retired) | SLSQP cross-check solver + its one test are removable scaffolding (judgment call). |

**Total estimated LOC saved: ~357 firm + ~40 conditional (CR-STYLE-002) ≈ 397.**

> Note: this is the high-confidence, behaviour-preserving subset (every claim grep-verified). It does not by itself reach the ~1,300-LOC roadmap target; the remaining reduction will come from structural consolidation the architecture review should size (e.g. whether the 10-file `schema/` package + 64-line re-export `__init__` and the `prompts.py`/`llm_provider.py` generative path can be thinned), which is out of scope for a behaviour-preserving file-level review.
