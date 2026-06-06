# Engine 2 Hardening — Design Doc (reconstructed spec, parts A–E + generic case system)

**Status:** DESIGN ONLY — no code. Approved at ideate gate.
**Scope:** Harden Engine 2 (scenario pricing / edge) and replace per-case test
fixtures with a generic, data-driven case system.
**Audience:** implementer of `engine/engine2.py`, `engine/cases.py`, the runner, and tests.

---

## 0. Why this doc exists (provenance & honesty note)

The task prompt that triggered this work references prior artifacts as if they
exist on disk: a "runner build" (`engine/workflow.py`, `engine/fixtures.py`,
`engine/tests/test_golden_master.py` with Tests A and B) and an "approved
scenario-engine hardening spec (parts A–E)". **None of these exist in the repo.**
Verified state:

- Real files: `engine/{schema.py, engines.py, stage0.py, example.py, __init__.py}`.
- No `workflow.py`, no `fixtures.py`, no `tests/`, no `run_workflow`, no `Provider`.
- No hardening-spec markdown. `creditmacro/` is not even git-tracked.

Therefore this document **reconstructs** the spec and treats the runner/case
system as **greenfield**. "Test B" has no recoverable definition and is dropped;
the two oracles are **Test A (AI-issuance, exact)** and **Test C → renamed Test B
here (French-banks, acceptance)**. Naming below uses **AI-issuance** and
**French-banks** rather than letters to avoid resurrecting a phantom.

The one thing that *is* real and must be protected: `example.py` currently
produces, via the existing SLSQP solver,

```
scenario_fv   = 75.0
q             = [0.125512, 0.184417, 0.328452, 0.361619]   (≈ [0.126,0.184,0.328,0.362])
residual_edge = 20.0
omega         = 7.666667     (≈ 7.67)
score         = 3.91822      (≈ 3.918)
frac          = -1.0
ETF basis gated out: "λ 0.32 < 0.40"
vol_scalar    = 1.250,  net_target_pnl = 747000,  all 4 discipline gates pass
```

These are the **golden numbers**. Every step must reproduce them to 1e-6.

---

## 1. Goals / non-goals

### Goals
1. **Exact** closed-form q solver (exponential tilt) replacing SLSQP, reproducing
   the golden q to 1e-6, with a real feasibility test and a risk-premium caveat.
2. **Monte-Carlo edge** producing `edge_std`, `SNR`, `P(success)`, scenario
   **attribution**, vol-normalised edge, and a direction-check flag — while
   `edge_mean` stays the deterministic identity ⟨p−q, X⟩.
3. **Uncertainty-propagating fair value**: per-scenario residual std `σ_g_s`
   flows into `scenario_fv_std`.
4. **Generic case system**: `CaseSpec` (data) → `ScriptedProvider` (mechanism) →
   parametrized runner that dispatches on an **oracle kind**. AI-issuance and
   French-banks become `cases/*.yaml`, not classes.
5. **Backtest record contract** (`ThemeOutcomeRecord`) — schema + append only.

### Non-goals (explicitly out of scope here)
- The full `g` estimator (regression / Merton / comparables). Scenarios **supply**
  `X_s` (mean) and optional `σ_g_s` (residual std); the engine **consumes** them.
- Calibration / edge-realisation analytics on closed theses (needs real data).
- Any execution, routing, or broker contact (v1 is epistemic; CLAUDE.md gate).
- LLM wiring. The point of this work is to **freeze the Pricing/edge contract**
  so the LLM later wires once to a fixed shape.

---

## 2. Architecture & layering (DAG)

```
                 cases/*.yaml  (DATA: spec + oracle)
                      │  load_case()
                      ▼
   schema.py  ◄──  cases.py  (CaseSpec, Oracle, ScriptedProvider)
      ▲               │ implements Provider Protocol
      │               ▼
   engine2.py ◄── workflow.py  (run_workflow: Provider → ThemeObject + memo)
   (pure quant)      │
      ▲              ▼
   engines.py    tests/  (parametrized over cases, dispatch on oracle.kind)
   (existing
    quant +
    stubs)
```

Dependency rule (DIP): `workflow.py` depends on the **`Provider` protocol**, never
on a concrete case. `cases.py` depends on `schema.py` only. `engine2.py` is a pure
quant module depending on nothing but `numpy`/`scipy`/`schema`. No cycles.

**The core design principle:** *generic MECHANISM, specific DATA, specific
ASSERTIONS.* The provider, loader, and runner never know which case they hold.
The YAML file and its oracle are the only case-specific things.

---

## 3. The generic case system

### 3.1 `Provider` protocol (the seam the runner depends on)

A `typing.Protocol` with one method per pipeline seam. The runner calls these in
order; it cannot tell a scripted provider from a future LLM-backed one.

```text
class Provider(Protocol):
    def parse(self, raw: str) -> IngestionResult: ...
    def load_policy(self) -> PolicyConfig: ...
    def extract_drivers(self, statement: str) -> Thesis: ...
    def define_axis(self, thesis: Thesis) -> Axis: ...
    def normal_fair_value(self, axis: Axis) -> float: ...
    def propose_scenarios(self, thesis: Thesis, axis: Axis) -> list[Scenario]: ...
    def enumerate_expressions(self, thesis, axis, scenarios) -> list[Expression]: ...
    def size_and_risk(self, ...) -> tuple[Sizing, Risk, PMGate]: ...
    def critique(self, theme: ThemeObject) -> list[str]: ...   # open questions
```

(Method set mirrors the existing engine stubs; exact signatures finalised at
design-review of `workflow.py`. The point is the *shape*: one seam per engine
sub-step, all deterministic for a `ScriptedProvider`.)

### 3.2 `CaseSpec` (Pydantic) — the data contract

```text
CaseSpec:
  theme_sentence: str
  thesis:       Thesis            # reuse schema.py types directly
  axis:         Axis
  prior:        list[float] | Literal["uniform", "historical"]
  scenarios:    list[ScenarioSpec]     # {name, p_s, X_s, sigma_g_s=0.0, hist_freq?}
  expressions:  list[ExpressionSpec]   # {id, legs, per_scenario_pnl, liquidity, cost, ...}
  stops:        {stop: float, take_profit: float}
  policy:       Literal["default"] | PolicyOverride   # inline gate-threshold overrides
  thesis_sign:  Literal[-1, +1]        # required for edge direction-check & P(success)
  oracle:       Oracle
```

- `prior="uniform"` → `[1/n,…]`. `prior="historical"` → normalised `hist_freq`
  field across scenarios (must be present if used). A literal vector is taken as-is.
- Scenarios reuse `schema.Scenario`; `sigma_g_s` is a **new Optional field**
  (default 0.0) added there (see §7).

### 3.3 Oracle taxonomy (the only case-specific assertions)

```text
Oracle:
  kind: Literal["exact", "acceptance", "invariants_only"]
  exact:      ExactOracle | None        # required iff kind == exact
  acceptance: AcceptanceOracle | None   # required iff kind == acceptance

ExactOracle:      {scenario_fv, q: list[float], edge, omega, score, gated_out: list[str]}
AcceptanceOracle: {base_worst_ratio: {target, tol}, edge_sign: "thesis_aligned",
                   attribution_top: str}     # name of the scenario the edge comes from
```

**Invariants floor — asserted for EVERY case regardless of kind:**
1. `schema_valid` — the ThemeObject constructs (all 4 discipline gates evaluate).
2. `gates_evaluate` — each gate returns pass/fail without raising.
3. `edge_sign == thesis_sign`.
4. `q_feasible` — solver returns FEASIBLE (X_mkt interior to scenario span).
5. `no NaN/inf` where a finite value is required.

This floor is what lets PDFs enter later as `kind=invariants_only` with **no
numeric oracle** — they just have to not break and to make directional sense.

### 3.4 `load_case(path) -> CaseSpec`
Reads YAML/JSON, deserialises into the typed `schema` objects, resolves `prior`
strings to vectors, validates. Pure function, no I/O beyond the read.

### 3.5 `ScriptedProvider(Provider)`
Constructed from **one** `CaseSpec`. Each seam method returns the corresponding
slice of the case, **ignoring its inputs** (so it is deterministic and input-blind
— exactly what makes the runner case-agnostic). This single class replaces every
per-case fixture constructor and any planned per-case provider subclass.

---

## 4. Part A — uncertainty-aware `g` + uncertainty-propagating fair value

`g` is the (unmodelled here) map *state → axis value*. We do **not** estimate it;
each scenario supplies the point `X_s` and an **optional residual std `σ_g_s`**
(default 0.0 → `X_s` is a point).

- `scenario_fair_value = Σ_s p_s X_s` — **unchanged** when all `σ_g_s = 0`.
- New: `scenario_fv_std`, propagated from `{σ_g_s, p}`. Treating scenario draws as
  independent given the state mixture, the design uses the law of total variance:

  ```
  Var[X] = Σ_s p_s σ_g_s²            (within-scenario)
         + Σ_s p_s (X_s − scenario_fv)²   (between-scenario)
  scenario_fv_std = sqrt(Var[X])
  ```

  With all `σ_g_s = 0`, the within term vanishes; `scenario_fv_std` still reports
  the **between-scenario dispersion** (this is information, not a regression).
  *Decision needed at review:* whether `scenario_fv_std` should include the
  between-scenario term or only the within-scenario term. Recommendation: report
  **both** as `scenario_fv_std` (total) and document; Test A is unaffected either
  way because Test A's oracle does not assert on std (Optional field, additive).

---

## 5. Part B — closed-form exponential-tilt q solver (`solve_q_tilt`)

Replaces SLSQP. The min-KL(q‖prior) solution subject to `Σ q_s = 1` and K moment
constraints `Σ_s q_s f_k(X_s) = c_k` is the **exponential tilt**

```
q_s = prior_s · exp( Σ_k λ_k f_k(X_s) ) / Z(λ),   Z(λ) = Σ_s prior_s · exp( Σ_k λ_k f_k(X_s) )
```

with λ solving the **convex dual**  `min_λ  ln Z(λ) − Σ_k λ_k c_k`.

### 5.1 K = 1 (level constraint: `f_1(X)=X`, `c_1 = X_mkt`)
1-D root find on `E_q[X] − X_mkt = 0`. `E_q[X]` is monotone increasing in λ, so:
bisection to bracket, then Newton (`d E_q[X]/dλ = Var_q[X] > 0`) to polish. This
is the path AI-issuance and French-banks use.

### 5.2 K > 1 (add axis-struck option payoffs `f_k(X)=max(X−strike_k, 0)`)
K-dim Newton on the dual gradient / Hessian:
```
∇_k = E_q[f_k] − c_k
H_jk = Cov_q[f_j, f_k]   (positive-definite ⇒ convex ⇒ unique optimum)
```
Options constrain q's **curvature/tails**, not its mean.

### 5.3 Prior
`prior` is an **explicit argument** (no implicit default inside the solver).
- AI-issuance pins `prior="uniform"` → reproduces the golden q (the tilt is the
  *exact* dual solution of the same KL problem SLSQP solved; verified to 3dp,
  expected to 1e-6).
- **Default for new runs = unconditional historical scenario frequencies**, so q
  measures the market's **departure from history**.

### 5.4 Feasibility (this is the part SLSQP hid)
A solution exists iff `X_mkt` is strictly interior to `(min_s X_s, max_s X_s)`.
If outside, return `status = INFEASIBLE` with a reason ("scenarios do not span
X_mkt — set incomplete"). **Do not fabricate a q.** The runner/MC consume this
status; the invariants floor asserts FEASIBLE for sound cases.

### 5.5 Risk-neutral caveat (load-bearing honesty)
Prices give `q^Q`. Edge vs `q^Q` is **gross of risk premium**. Accept an optional
pricing kernel `m_s` (or single risk-aversion param) and map
`q^P_s = q^Q_s·(1/m_s) / E[1/m]`. With no kernel, the edge is **labelled "gross of
risk premium"** everywhere it surfaces (Pricing field + memo). This is the engine's
single biggest epistemic assumption; Part D is what eventually tests it.

### 5.6 Back-compat
`solve_max_entropy_q(...)` stays importable as a **thin shim** delegating to
`solve_q_tilt` with `K=1, prior=uniform`. `run_pricing` switches to `solve_q_tilt`.
Existing callers are untouched.

---

## 6. Part C — Monte-Carlo edge with SNR / attribution (`compute_edge_mc`)

- **`edge_mean` is the DETERMINISTIC identity** `⟨p − q, X⟩` evaluated at the point
  estimates — it **exactly reproduces** the existing `residual_edge` (assert this in
  a unit test). MC is used **only** for second moments. *(Rationale: q is nonlinear
  in X, so the MC sample mean ≠ edge(E[X]) by Jensen; defining edge_mean as the
  point estimate keeps the golden number frozen. The hybrid nature of
  `SNR = edge_mean / edge_std` — point-estimate numerator, MC-spread denominator —
  is documented as intentional, not a bug.)*
- **MC procedure** (fixed RNG seed, reproducible): per draw,
  `X_s ~ Normal(X_s, σ_g_s)` and `p ~ Dirichlet(α)` where `α = κ·p` (κ = PM
  confidence; high κ → p ≈ fixed). Re-solve q via `solve_q_tilt`, recompute edge.
  Return `edge_std`, `SNR = edge_mean/edge_std`, and
  `P(success) = P(edge>0 AND sign(edge)==thesis_sign)`.
- **Infeasible draws** (a draw pushes X_mkt outside the drawn span): **skip,
  count, and report `infeasible_fraction`** in the result. Do not silently drop
  (it biases `edge_std`). *(This policy is new — the prompt left it undefined.)*
- **Optional delta-method analytic** for `edge_std` for speed (linearise edge in
  the perturbations); MC remains the reference.
- **Attribution:** `contribution_s = (p_s − q_s)·X_s` sorted descending, plus raw
  disagreement `(p_s − q_s)`, so the memo can name *which scenario* the edge comes
  from (`attribution_top`).
- **Normalisation:** `vol_adjusted_edge = edge_mean / σ_axis` (realised axis vol
  over the horizon) — an expected move in vol units, for cross-theme comparison.
- **Direction check:** if `sign(edge_mean) != thesis_sign`, set a loud flag.
- **SNR gate:** add `snr_min` (default 1.0) to the **policy config**, kept
  **SEPARATE** from the 4 discipline gates so Test A's gate-pass set is unchanged.
  With `σ_g=0` and high κ, `edge_std→0`, `SNR→∞`, so AI-issuance passes cleanly.

---

## 7. Schema changes (ADD-ONLY — §regression safety)

All new fields **Optional with defaults** so existing data validates and Test A is
byte-identical. No rename, no removal.

`Scenario` (engine 2 input):
```
sigma_g_s: Optional[float] = 0.0    # residual std of X_s | state
hist_freq: Optional[float] = None   # unconditional frequency, for prior="historical"
```

`Pricing` (engine 2 output):
```
scenario_fv_std:    Optional[float] = None   # Part A
q_status:           Optional[Literal["FEASIBLE","INFEASIBLE"]] = None  # Part B
q_infeasible_reason:Optional[str]  = None
edge_std:           Optional[float] = None   # Part C
snr:                Optional[float] = None
p_success:          Optional[float] = None
vol_adjusted_edge:  Optional[float] = None
edge_attribution:   Optional[list[dict]] = None   # [{scenario, contribution, disagreement}]
edge_direction_ok:  Optional[bool] = None
edge_basis:         Optional[Literal["gross_of_risk_premium","physical"]] = "gross_of_risk_premium"
infeasible_fraction:Optional[float] = None
```

`PolicyConfig` (new, but with defaults equal to today's hard-coded constants):
`omega_min=2.0, liquidity_min=0.40, cost_fraction_max=0.33, snr_min=1.0,
a=0.10, g=0.50`. Test A uses `"default"` → identical to current behaviour.

---

## 8. Part D — process-backtest record (contract only)

```
ThemeOutcomeRecord (dataclass):
  theme_id: str
  p: list[float]; q: list[float]; X_s: list[float]; X_mkt: float
  predicted_edge: float; edge_std: float
  realized_axis_at_horizon: Optional[float] = None   # None until the thesis closes
```
Plus `append_outcome(record, path)` → JSONL store. **Calibration / edge-realisation
analyses are documented stubs** (need closed theses). This record is the *only*
mechanism that later separates true alpha from the §5.5 risk premium.

---

## 9. Part E — French-banks as an `acceptance` oracle

`cases/french_banks.yaml`, sourced from the Alaph deck (lines 581–657):
- **Axis:** French-banks-basket senior CDS − French sovereign CDS (bps); entry
  near the ~40bps historical-low differential.
- **Scenarios** (5): {Dexia/full bailout, Worst/no-support, Enhanced, Best,
  No-material-change}, each with `X_s`, `σ_g_s`, `p_s`. Scenario span must
  **bracket entry on both sides** (feasibility, §5.4).
- **thesis_sign = +1** (declining support ⇒ differential **widens**).
- **stops:** stop-loss / take-profit from the deck chart.
- **prior = "historical"** (historical scenario frequencies).
- **oracle.kind = acceptance:** `base_worst_ratio = {target: 1.9, tol: <band>}`,
  `edge_sign = "thesis_aligned"`, `attribution_top = "Worst/no-support"`.

Because the deck chart is OCR-fuzzy, French-banks is **never** an exact oracle.
The acceptance assertions (ratio ≈ 1.9, edge sign, attribution) come from the
deck's *stated* facts (line 639: "base case P&L vs worst case c. 1.9x"); `X_s`
come from the deck — **1.9 is derived and checked, not reverse-fit**.

---

## 10. Test / runner design

One parametrized test iterates over `cases/*.yaml`. For each:
1. `load_case` → `ScriptedProvider` → `run_workflow` → `ThemeObject`.
2. Assert the **invariants floor** (§3.3) — always.
3. `dispatch on oracle.kind`:
   - `exact` → assert `scenario_fv, q[], edge, omega, score, gated_out` to 1e-6.
   - `acceptance` → assert `base_worst_ratio` within tol, `edge_sign`,
     `attribution_top`.
   - `invariants_only` → floor only.

The runner and test are **case-blind**; adding a case = adding a YAML file.

---

## 11. Build order (STOP for review after the last step)

1. **Case system + retrofit AI-issuance to data.** `cases.py` (`CaseSpec`, oracle,
   `load_case`, `ScriptedProvider`) + `cases/ai_issuance.yaml` (exact golden
   numbers, `prior="uniform"`). Repoint `example.py` + AI-issuance test to load
   the YAML. **Prove `example.py` output and Test A are byte-identical BEFORE any
   engine2 math.** ← truncation point of the source prompt; steps below inferred.
2. **`solve_q_tilt`** (K=1 root find, K>1 dual, feasibility) + shim. Reproduce
   golden q to 1e-6. Unit-test.
3. **Uncertainty-aware FV** (`σ_g_s` → `scenario_fv_std`). σ=0 ⇒ unchanged.
4. **`compute_edge_mc`** (edge_mean==identity proven; SNR/attribution/P(success)/
   vol-norm/direction; infeasible-draw policy). SNR gate in policy, separate.
5. **`ThemeOutcomeRecord`** + JSONL append (analytics stubbed).
6. **French-banks** `cases/french_banks.yaml` (acceptance oracle).
7. **Parametrized runner/test** dispatching on oracle kind; invariants floor for
   all. Re-confirm AI-issuance exact + French-banks acceptance + golden numbers.

Run the AI-issuance golden check **before and after every step**.

---

## 12. Open risks (carried from ideate)

1. **Prior leakage.** If `run_pricing`'s new default prior (historical) ever
   reaches AI-issuance, q drifts and Test A breaks. → prior explicit per-case;
   default change opt-in.
2. **Hybrid SNR.** `edge_mean` (point) / `edge_std` (MC) must be documented or it
   reads as inconsistent. Decided: document as intentional.
3. **Infeasible MC draws.** Policy = skip+count+report; never silent-drop.
4. **Reverse-fit French-banks.** X_s from deck; 1.9 derived + tolerance; a miss is
   a finding, not a knob.
5. **`scenario_fv_std` definition** (within vs within+between). Resolve at step-3
   review; Test A unaffected either way.

---

## 13. Design-skill minimums (checklist)

- **File structure (≥3):** `engine/engine2.py`, `engine/cases.py`,
  `engine/workflow.py`, `engine/tests/test_cases.py`, `cases/ai_issuance.yaml`,
  `cases/french_banks.yaml`. ✔
- **Protocol (≥1):** `Provider` protocol (§3.1); `ScriptedProvider` implements it. ✔
- **Config approach:** `PolicyConfig` Pydantic with defaults == current constants;
  cases carry data as YAML; new Pricing/Scenario fields Optional. ✔
- **DAG check:** acyclic (§2). ✔
