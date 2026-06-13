# Surveillance & Build-Completion Plan

> **What this is.** A phased, implementation-ready plan to complete the discovery engine and add
> **post-confirmation theme surveillance** — the loop that watches a theme *after* it is confirmed and
> trades are on, tracks it via new reports/news, and routes its status without ever touching execution.
> Written to be read by **Claude Code** for `/ideate`. Companion to `docs/ENGINE_MANUAL.md`,
> `docs/ENGINE_CONTEXT_PACK.md`, `docs/THEME_DISCIPLINE_AND_FAILURE_MODES.md`.
>
> **Status tags:** ✅ implemented · ⚠️ partial · 🚧 planned/contract_only · ❌ missing · 🔒 firewall/gate.
> **Do not assume planned features exist.** Trust the tags. Every "add" below is new code; every
> "refactor" is a tightening of existing behavior, never a teardown.
>
> **Prime directive:** this whole plan is **~85% add, ~15% surgical refactor.** The architecture is
> sound — the firewalls, the discovery/expression split, the locked lifecycle, and the wiki memory
> model all stay. We are filling holes in a finished frame.

---

## 0. Orientation

### 0.1 The product loop and where it is broken

```
ingest → theme → route → │ persist → watch → terminal │ → calibrate → memory
  ❌        ⚠️      ✅     │   ❌        ❌       ⚠️      │     ❌          ⚠️
 (D1)     (D2)   (works)  │  (P1)      (P3)    (P3/P6)  │    (P6)        (P6)
```

Three breaks: the **entrance** (no live ingestion), the **write-back + watch** (no persistence, no
surveillance), and the **back-end** (no calibration). Surveillance is the piece you just prioritized;
it makes **persistence a hard prerequisite** (you cannot watch a theme you never wrote down) and pushes
**calibration to last** (you cannot calibrate theses that have not closed yet).

### 0.2 Non-negotiable invariants (every PR obeys these)

1. **`tests/integration/test_golden_master.py` numerics unchanged.** Gate every merge on it.
2. **Firewalls preserved** — method/case fail-closed (`engine/memory.py`), discovery/expression fence
   (`engine/firewall.py`), temporal (`engine/temporal.py`). New evidence enters **only** through the
   current-input seam (`engine/protocols.py::RunContext.current_input_*`).
3. **No legs / sizing / hedge ratios** anywhere new. Reuse the WikiIntegrator no-trade guard.
4. **Determinism.** No wall-clock; `now` is always supplied. Same input → same output. Stable ordering.
5. **New frozen-model fields are `Optional` with safe defaults** so `FrozenSnapshot` and the golden
   master are unaffected.
6. **Surveillance is discovery-*class*, not expression.** It re-opens the *epistemic* question ("is the
   thesis still true?"), never the *execution* question ("what is my position?"). It STOPS at an alert.

### 0.3 The activity taxonomy (so surveillance does not blur into expression)

| Phase | Question it answers | Emits | Mode |
|---|---|---|---|
| Discovery | "What is changing and how would I express it?" | themes + ranked strategy families | discovery |
| Expression *(fenced)* | "What is my position?" | legs, sizes, hedge ratios | expression (scripted-only) |
| **Surveillance** | "**Is the thesis still true?**" | **status + alerts** | **discovery-class** |
| Calibration | "Did the call work?" | reliability + edge realization | post-freeze analytics |

The lifecycle becomes: **discovery → (human picks trades) → surveillance → terminal → calibration.**

---

## 1. Dependency graph & sequencing

```
Phase 0  free wiring + guardrails (L1–L5) ───> one discovery entry point + clean output
            │
Phase 1  PERSISTENCE (ThemeObject → wiki) + forward_horizon on ThemeObject   ← KEYSTONE
            ├───────────────> Phase 3  SURVEILLANCE (watch a persisted theme) ──┐
            │                                                                    │ terminal states
            └───────────────> Phase 6  CALIBRATION  <─────────────────────────────┘ feed the corpus

Phase 2  THEME COMPRESSION   ── independent; parallelizable with 1/3
Phase 4  INGESTION           ── automates the entrance to all of the above
Phase 5  NEWS CRITIC ──> feeds Phase 3;  memory categorization + sufficiency gate ── hardening
```

**The one fork you own — ingestion-first vs spine-first.** This plan sequences ingestion (Phase 4)
*after* the deterministic spine. Rationale: validate the whole loop with injected inputs first, so when
a bad theme appears you can localize the failure (parsing vs compression vs routing). Building the flaky
LLM parser first into an unfinished pipeline destroys that localization. The counter-argument is that
"consume PDFs" is the headline feature and you may want it visible early. Spine-first = lower risk;
ingestion-first = higher demo value. **Pick one — it is the only real fork in the plan.**

**Parallelization.** Phase 2 (compression) is independent of the persistence→surveillance chain and can
run on a second track.

---

## 2. Phase 0 — Free wiring + guardrails (L1–L5)

*Add (L1, L2) + surgical refactor (L3, L4, L5). Size: M total; each item individually S.*

| ID | Build | State today | Action | Files | Acceptance | GM risk |
|---|---|---|---|---|---|---|
| L1 | `DiscoveryRunnerAgent` | 🚧 contract_only | Wrap `engine.workflow.run_workflow` in the registered agent whose `run()` raises `NotImplementedError`. One-call entry: load slug → current-input seam → run. | `engine/wiki_agents.py` | Agent loads a slug, feeds the seam, returns a `strategy_family_routed` ThemeObject. | none — GM already calls `run_workflow` directly |
| L2 | `WikiLintAgent` | 🚧 contract_only (lib ✅) | Orchestrate the 14 `engine/wiki_validators.py` checks in batches (Workflow 3). | `engine/wiki_agents.py` | Runs `validate_all`; reconciles index/log/memory-map; the known xfail becomes a real check. | none |
| L3 | Aggregator cap + deterministic order | ⚠️ uncapped | After `_cluster_items`, impose a configurable parent cap; demote the tail to `watchlist`; log demotions. | `engine/theme_aggregation.py` | N>cap clusters → ≤cap emitted; nothing dropped silently (demotion count logged). | low — confirm no test asserts exact cluster **count** |
| L4 | Type the strategy-family hints | ⚠️ free strings | Bind `ThemeCluster.strategy_family_hints` to the 12-value routable `Literal`; tag `curve`/`sector_rotation` wiki-only. | `engine/schema/theme_aggregation.py` + validator | A hint outside the enum fails validation. | low |
| L5 | Require `current_date` for discovery | ⚠️ silent skip | Convert the silent skip in temporal classification to **fail-closed** for discovery runs. | `engine/temporal.py`, `engine/workflow.py` | Discovery without `current_date` raises rather than degrading; "old report reads as current" path closed. | low |

**Unlocks:** a single-entry, capped, correctly-typed discovery flow that every downstream phase rides on.

---

## 3. Phase 1 — Persistence + forward horizon (the keystone)

*Add (persistence) + add field (horizon). Size: M + S.*

### 3.1 D3a — Discovery-output persistence ❌ → ✅

Add a WikiIntegrator path that writes a routed `ThemeObject` back as a **CASE theme page** carrying:
families + `ConfidenceComponents` + operational axis + falsifier + `fresh_snapshot_hash` +
`forward_horizon`. Reuse the no-trade and ≥25-word copyright guards. Idempotent re-write.

- **Files:** `engine/wiki_integration.py`, page type in `wiki/CONVENTIONS.md`.
- **Acceptance:** a routed ThemeObject round-trips to a CASE page and reloads losslessly; no
  legs/sizing in the page; re-writing the same object is a no-op (idempotent).

### 3.2 `forward_horizon` on `ThemeObject` (closes a previously flagged gap)

The engine currently assigns **no forward horizon** to a theme. Add it at discovery, `Optional` with a
safe default so `FrozenSnapshot` and the golden master are untouched.

```python
class ForwardHorizon(BaseModel):
    opened: date                 # discovery date (caller-supplied; no wall-clock)
    expected_close: date         # opened + window
    window_label: str            # "3w" | "6w" | "3m" | "4m" | ...
    window_days: int             # derived; the single number every clock keys off
```

- **Acceptance:** discovery stamps a 3–4-month window by default; frozen-model and GM field-set tests
  still pass.

**Unlocks:** surveillance *and* calibration both become possible — neither can exist without a
persisted, horizon-stamped theme. **Build this before Phase 3.**

---

## 4. Phase 2 — Theme compression (highest-leverage quality fix, parallelizable)

*Add. Size: L. Independent of the persistence→surveillance chain.*

`ThemeCompressionAgent` + `AnalystThemeMap`: the precision layer over the lexical recall pass —
mechanism-based merge (not token Jaccard), parent/subtheme hierarchy, capped output, the full promotion
gate (evidence + mechanism + axis + falsifier + temporal + ≥1 routable family + rationale), downgrade
rules, source-coverage matrix, "why not." **The 10 acceptance tests already exist** in
`docs/THEME_DISCIPLINE_AND_FAILURE_MODES.md` — do not re-derive them.

**Golden-master placement (critical):** put compression in the **discovery flow** (`run_workflow` /
DiscoveryRunner), *not* in the scripted `runner.run_case` expression path the golden master locks. That
path is already fenced from the live provider, so GM numerics cannot move. State this in the PR.

---

## 5. Phase 3 — SURVEILLANCE ★ (the centerpiece)

> Watch a confirmed theme while trades are on. Track it via new reports/memos/news. Update its status.
> Emit alerts. **STOP.** Never size, never adjust a hedge ratio. This is the discovery STOP discipline
> pointed at a *live, frozen theme* instead of a blank page.

### 5.1 The two clocks

**Clock A — forward horizon (the 3–4-month window).** Reuse `TemporalContextAgent` *by symmetry*: the
same expiry machinery that flags a 2019 report's call as **expired** flags *your own* theme as
approaching or past its window. Point the agent at `ThemeObject.forward_horizon`.

**Clock B — evidence cadence + decay.** Event-driven (a new report/memo/news item tagged to the theme
arrives → run a monitor pass) **plus** a scheduled axis read (weekly is the BMI/eBMI reset precedent).
Confirming evidence **decays with recency** (BMI decaying-moving-average precedent). No new evidence past
a staleness threshold is itself a signal — the theme is going quiet.

### 5.2 States

**Non-terminal (active monitoring):**

| Status | Meaning |
|---|---|
| `armed` | Theme confirmed, trades on, monitoring active, nothing notable. |
| `confirming` | Recent weighted evidence supports the causal chain. |
| `weakening` | Recent weighted evidence undermines the chain, but the falsifier is **not** breached. |
| `stalled` | No new evidence for longer than the (dynamic) staleness threshold. |
| `falsified_pending` | Falsifier metric is breaching its threshold but the **breach buffer** has not yet elapsed. *(Guardrail 1.)* |

**Terminal (absorbing — emit `ThemeOutcomeRecord`, hand control to human):**

| Status | Meaning | Outcome |
|---|---|---|
| `falsified` | Falsifier breached **and persisted** through the breach buffer. | exit signal; wrong-thesis record |
| `horizon_expired` | Past `forward_horizon` with no resolution. | your own expired forecast, scored like a stale sell-side call |
| `played_out` | Axis reached target / thesis realized. | win record **+ priced-in check** (is the edge now gone?) |

### 5.3 The prioritized transition function (the core — the simulator implements this exactly)

Evaluated on every **tick** (a tick = a new evidence event OR a scheduled falsifier read). Higher rules
win. This is the single source of truth for the state machine.

```python
def transition(w: ThemeWatch, tick: Tick, pol: SurveillancePolicy) -> StatusUpdate:
    # ---- 1. ingest the tick, update raw state variables ----
    if tick.is_falsifier_read:
        breaching = is_breach(tick.metric_value, w.falsifier.threshold, w.falsifier.direction)
        if breaching:
            w.consecutive_breach_count += 1
            if w.breach_started_at is None:
                w.breach_started_at = tick.now
        else:
            if w.consecutive_breach_count > 0:
                w.log("whipsaw_averted", count=w.consecutive_breach_count)   # Guardrail 1
            w.consecutive_breach_count = 0
            w.breach_started_at = None

    if tick.is_evidence_event:
        w.events.append(tick.event)            # event valence was scored BLIND (Guardrail 3)
        w.last_evidence_date = tick.now

    # ---- 2. derive (all horizon-keyed; Guardrail 2) ----
    H        = w.forward_horizon.window_days
    elapsed  = days(tick.now - w.forward_horizon.opened)
    stale_th = clamp(pol.k_stale * H, pol.stale_floor, pol.stale_cap)         # Guardrail 2
    half_life= clamp(pol.k_decay * H, pol.decay_floor, pol.decay_cap)         # Guardrail 2
    quiet    = days(tick.now - w.last_evidence_date)
    net_val  = sum(
        e.signed_valence
        * (0.5 ** (days(tick.now - e.timestamp) / half_life))                 # recency decay
        * (pol.lambda_disconfirm if e.signed_valence < 0 else 1.0)            # disconfirm asymmetry
        for e in w.events
    )
    axis_done = realized_fraction(w.axis_state)   # |move| / |modeled target move|

    # ---- 3. prioritized routing (FIRST match wins) ----
    if axis_done >= pol.axis_target_fraction:
        return terminal(PLAYED_OUT, "axis_target_reached")
    if w.consecutive_breach_count >= w.falsifier.breach_buffer:              # Guardrail 1 (confirmed)
        return terminal(FALSIFIED, "falsifier_persisted")
    if elapsed > H:
        return terminal(HORIZON_EXPIRED, "horizon_elapsed")
    if w.consecutive_breach_count >= 1:                                       # Guardrail 1 (pending)
        return active(FALSIFIED_PENDING, "falsifier_breaching_buffering")
    if quiet > stale_th:                                                      # Guardrail 2
        return active(STALLED, "evidence_stale")
    if net_val < -pol.valence_band:
        return active(WEAKENING, "valence_negative")
    if net_val > +pol.valence_band:
        return active(CONFIRMING, "valence_positive")
    return active(ARMED, "nominal")
```

**Why this order.** Terminal *wins* (`played_out` > `falsified` > `horizon_expired`) — a realized thesis
is a win even amid a falsifier wobble; a mis-specified config where target and falsifier are
simultaneously satisfiable resolves to the win (see §5.7 sanity check). Within the active band, a
breaching falsifier *dominates* the health read (it is the pre-registered exit), then staleness, then
valence. `armed` is the quiet default.

### 5.4 Default policy parameters

```python
class SurveillancePolicy(BaseModel):
    # Guardrail 1 — breach buffer
    breach_buffer: int        = 3        # consecutive qualifying reads to confirm falsification
    breach_obs_freq: str      = "weekly" # the read cadence the buffer counts in
    # Guardrail 2 — horizon-keyed dynamics
    k_stale: float            = 0.15     # staleness threshold = k_stale * window_days
    stale_floor: int          = 2
    stale_cap: int            = 30
    k_decay: float            = 0.25     # evidence half-life = k_decay * window_days
    decay_floor: int          = 3
    decay_cap: int            = 45
    # Guardrail 3 — disconfirmation asymmetry
    lambda_disconfirm: float  = 1.5      # disconfirming evidence weighted >= confirming
    # health dead-band + win threshold
    valence_band: float       = 0.5      # |net_val| <= band stays armed (no flicker)
    axis_target_fraction: float = 0.75   # fraction of modeled target move => played_out
```

### 5.5 Guardrail 1 — The Breach Buffer (time-weighted falsification)

**Problem solved:** whipsaw exits on noisy single-day/single-print breaches. A point breach is not a
broken thesis.

**Mechanism (default — consecutive persistence).** A falsifier breach transitions the theme to
`falsified_pending`, not `falsified`. It only reaches the terminal `falsified` if the breach **persists
for `breach_buffer` consecutive qualifying reads** (cadence `breach_obs_freq`, e.g. 3 straight weekly
prints). If the metric un-breaches before the buffer elapses, `consecutive_breach_count` resets to 0,
the theme returns to its recomputed health state, and a `whipsaw_averted` event is logged.

**State variables on `ThemeWatch`:** `consecutive_breach_count: int`, `breach_started_at: date | None`.

**`FalsifierState` schema:**

```python
class FalsifierState(BaseModel):
    observable: str                 # e.g. "PPI_minus_CPI_diff_bp"  (a real series name)
    threshold: float                # X
    direction: Literal["below","above"]
    breach_buffer: int = 3
    current_value: float | None = None
    distance_to_threshold: float | None = None   # signed; for the "how close" alert
    consecutive_breach_count: int = 0
    breached: bool = False          # True only when the buffer has elapsed (terminal)
```

**Variant 🚧 (decayed breach integral — for intermittent-but-deepening breaches).** Instead of requiring
*consecutive* reads, accumulate a recency- and magnitude-weighted breach integral and fire when it
crosses a threshold:

```
breach_integral_t = decay * breach_integral_{t-1} + max(0, signed_excess_past_threshold_t)
falsify if breach_integral_t >= BREACH_INTEGRAL_THRESHOLD
```

This handles a falsifier that breaches in weeks 1, 3, 5 (never 3 in a row) but is clearly trending
through the threshold. Offer as a configurable `breach_mode: Literal["consecutive","integral"]`. Default
`consecutive` (matches "3 straight weeks"); document the integral as the noisy-series upgrade.

**Config sanity checks (lint at watch creation):** `breach_buffer >= 1`; `breach_obs_freq` divides the
horizon into ≥ `breach_buffer + 1` reads (otherwise a theme can expire before it can ever be falsified);
`threshold`/`direction` consistent with the axis's sign convention.

### 5.6 Guardrail 2 — Dynamic staleness (horizon-keyed)

**Problem solved:** a static `staleness_days` is scale-blind. *"A theme with a 3-week horizon going
quiet for 4 days is stalled; a theme with a 4-month horizon going quiet for 4 days is just noise."*

**Mechanism.** Both the staleness threshold and the evidence half-life **scale with the window**:

```
window_days  H
staleness_threshold = clamp(k_stale * H, stale_floor, stale_cap)     # default k_stale = 0.15
evidence_half_life  = clamp(k_decay * H, decay_floor, decay_cap)     # default k_decay = 0.25
recency_weight(age) = 0.5 ** (age_days / evidence_half_life)
```

**Worked numbers (matching the brief exactly):**

| Theme window | `H` (days) | staleness threshold (`0.15·H`, clamp 2–30) | half-life (`0.25·H`, clamp 3–45) | 4 days quiet ⇒ |
|---|---|---|---|---|
| **3 weeks** | 21 | `max(2, 3.15) ≈ 3.2 d` | `5.25 d` | `4 > 3.2` → **`stalled`** ✓ |
| **4 months** | 122 | `min(30, 18.3) = 18.3 d` | `30.5 d` | `4 < 18.3` → **noise** (health unchanged) ✓ |

The half-life scaling means the *meaning of "recent"* also scales: a 4-month theme treats month-old
evidence as still partly live (weight `0.5^(30/30.5) ≈ 0.49`); a 3-week theme treats week-old evidence as
mostly decayed (weight `0.5^(7/5.25) ≈ 0.40`). The decay coefficient scales with the window, as required.

**Clamps matter:** the floor stops a 1-week tactical theme from a sub-day threshold (every weekend =
stalled); the cap stops a 12-month structural theme from a 50-day blind spot.

### 5.7 Guardrail 3 — The LLM confirmation-bias guard (blind + adversarial, enforced by construction)

**Problem solved:** LLM sycophancy. Once it knows the prior thesis (and that a trade is on), an LLM will
rationalize adverse data as "confirming." Monitoring is exactly where this kills you.

**Enforced by construction, not instruction** — mirroring the `MemoryRetriever` fail-closed pattern. The
status field is **physically withheld** from the scoring call's context. The scorer literally cannot see
the conclusion it might be tempted to justify.

```python
class BlindScoringContext(BaseModel):
    """The ONLY thing the valence scorer sees. Structurally cannot carry the conclusion."""
    causal_chain: CausalChain        # driver -> transmission -> outcome  (the MECHANISM)
    operational_axis: str            # the named series
    new_source_atoms: list[EvidenceAtom]
    # DELIBERATELY ABSENT (cannot be added): current status, confirming/weakening lean,
    # P&L, whether a trade is on, the prior overall conviction, the watch history.
```

**Protocol (three passes, deterministic adjudication):**

1. **Disconfirm pass.** Prompt: *"Find the strongest reading of this evidence that BREAKS the causal
   chain. Which link (driver / transmission / outcome) does it threaten?"* Steelman the bear case.
2. **Confirm pass.** Symmetric steelman of the bull case.
3. **Adjudication (deterministic code, not the LLM).** Each atom gets a signed valence vs each causal
   link. Aggregate with the **disconfirmation asymmetry** `lambda_disconfirm >= 1.0`: ties and
   near-ties break toward disconfirming, because the operator is already long and biased the other way.

**Structural separation.** The blind scorer is a *different* call (ideally a different persona/system
prompt) from any summarizer that knows the thesis. The scorer emits signed per-atom valence + rationale;
the **status-update logic is deterministic code** (the §5.3 function), which *does* know status but does
*not* "interpret." The LLM never sees status when judging; the code never editorializes.

**Audit.** Persist the `BlindScoringContext`, both steelman passes, and the adjudication, so a reviewer
can verify the status was withheld. Acceptance test 6 asserts the context object excludes the forbidden
fields.

**Ties into existing discipline:** a news flood is *attention*, scored on the `q` side, not the `p`
side — handled by the news critic (§7) and the `attention ≠ evidence` gate (§5.9).

### 5.8 Objects & agent

```python
class ThemeWatchEvent(BaseModel):
    source_provenance: SourceRef          # temporal_role MUST be current_report
    valence: Literal["confirming","disconfirming","neutral","falsifying"]
    signed_valence: float                 # blind-scored magnitude, signed
    bears_on: Literal["driver","transmission","outcome","falsifier","axis"]
    evidence_atoms: list[EvidenceAtom]    # reuse EvidenceExtractionBundle output
    is_attention_only: bool = False       # news flood w/ no new atoms => True (cannot raise conviction)
    timestamp: date

class AxisState(BaseModel):
    series: str
    current: float
    entry_level: float
    modeled_target: float                 # from discovery scenario FV (NOT a trade level)
    realized_move: float | None = None
    direction_vs_thesis: Literal["with","against","flat"] = "flat"
    decay_flag: bool = False              # regime shift / index recomp,osition decoupled the series

class ThemeWatch(BaseModel):
    theme_id: str
    snapshot_hash: str                    # binds to the FROZEN causal object; never mutates it
    status: WatchStatus
    forward_horizon: ForwardHorizon
    falsifier: FalsifierState
    axis_state: AxisState
    events: list[ThemeWatchEvent] = []
    last_evidence_date: date
    consecutive_breach_count: int = 0
    breach_started_at: date | None = None
    alerts: list[WatchAlert] = []         # the only OUTPUT to the human; no legs/sizing
    log: list[WatchLogEntry] = []         # whipsaw_averted, transitions, decay flags
```

**`ThemeMonitorAgent` (discovery-mode):**

1. Load the **frozen** theme from its persisted CASE page (Phase 1). The causal object is read-only.
2. Classify + extract the new source — reuse `SourceIntakeAgent` / `EvidenceExtractionAgent` /
   `TemporalContextAgent`. New evidence is `current_report` case evidence entering through the existing
   **current-input seam** — *no firewall change needed*.
3. Score valence **BLIND** (§5.7) → produce `ThemeWatchEvent`s.
4. Run `transition()` (§5.3). Update `FalsifierState` + `AxisState`.
5. Emit a `ThemeWatch` update + alerts (`hold`, `falsifier_approaching`, `exit_signal`, `stalled`,
   `axis_decay`, `priced_in`). **STOP.** Re-evaluation goes to the human.

### 5.9 The discipline gates (the part that actually matters)

Post-trade monitoring is where rigor goes to die. These gates are the whole point.

1. **The pre-registered falsifier is the primary trigger, not the narrative.** Set *before* the trade,
   an observable + threshold, immune to reinterpretation. Once you are long the spread, every headline
   reads bullish — the threshold does not care how you feel.
2. **Price ≠ thesis.** Two *distinct* alerts: (a) thesis intact, mark adverse → *hold* (the eBMI "right
   trend, ugly week" case); (b) falsifier breached or causal chain severed → *exit*. Conflating them is
   how people panic out of good trades and ride broken ones down.
3. **Attention ≠ evidence.** A news flood is attention (`q`), not evidence (`p`). Rising coverage with no
   new atoms may mean the theme is getting **priced in** → push toward `played_out` and *lower* edge
   expectation, not added conviction. `is_attention_only=True` events cannot move status to `confirming`.
   This is the `corroboration − attention` divergence, run forward in time.
4. **Axis-decay alert.** A regime shift or index recomposition can decouple the series from the thesis
   (a Fed pivot breaks the PPI−CPI → credit-differential link; the basket gets re-weighted). The axis is
   "still computable but no longer faithful." Flag **instrument broke** distinct from **thesis broke**.
5. **Firewall preserved.** The frozen causal object never mutates; the watch is an **additive,
   timestamped annotation stream keyed to `snapshot_hash`** — the same shape as `PostCaseCalibration`.
   Monitoring stays in discovery mode: alerts and re-evaluation only.

### 5.10 Acceptance tests (testable "done" — mirror the 10 compression tests)

1. **Whipsaw protection.** One breaching read → `falsified_pending`, **not** `falsified`. Un-breach
   before buffer → returns to prior health state; logs `whipsaw_averted`.
2. **Persisted breach.** Breach for `breach_buffer` consecutive reads → `falsified` (terminal); writes a
   `ThemeOutcomeRecord`.
3. **Dynamic staleness — short horizon.** 3-week theme, 4 days no evidence → `stalled`.
4. **Dynamic staleness — long horizon.** 4-month theme, 4 days no evidence → **not** `stalled`.
5. **Price ≠ thesis.** Adverse axis move, thesis intact, falsifier not breaching → `weakening`/`hold`
   alert, **never** an exit.
6. **Confirmation-bias guard (construction).** The valence-scoring context object excludes
   status / lean / P&L / trade-on (assert by schema); ties break disconfirming (`lambda_disconfirm`).
7. **Attention ≠ evidence.** An `is_attention_only` flood does not move status to `confirming`; raises
   priced-in/played-out pressure instead.
8. **Horizon expiry.** `now > expected_close`, not played_out/falsified → `horizon_expired`; writes a
   `ThemeOutcomeRecord`.
9. **Played out.** `realized_fraction >= axis_target_fraction` → `played_out`; triggers a priced-in check.
10. **Firewall.** Causal object never mutated; watch is additive keyed to `snapshot_hash`; evidence
    enters only via the current-input seam; no legs/sizing in any watch output.
11. **Determinism.** Same tick sequence → same status path (no wall-clock; `now` supplied).

### 5.11 Worked example — the PPI/CPI theme through the machine

- **Theme (frozen at discovery):** *short producer-price-sensitive credits vs consumer-price-sensitive
  credits.* Driver → margin compression in producers; transmission → spread widening in producer-heavy
  baskets; outcome → producer−consumer credit differential widens.
- **Operational axis:** the producer−consumer credit differential, anchored to the **PPI−CPI** series.
- **Forward horizon:** `3m` (`window_days = 91`). ⇒ `stale_th ≈ 13.7 d`, `half_life ≈ 22.8 d`.
- **Falsifier (pre-registered):** *"PPI−CPI compresses below `X` bp for `3` straight weekly prints while
  the credit differential fails to widen."* `direction="below"`, `breach_buffer=3`.
- **Run:**
  - New CPI/PPI print arrives → falsifier read. Margin-pressure sell-side note arrives → blind-scored
    `ThemeWatchEvent`, `bears_on="driver"`.
  - One weak print pushes PPI−CPI below `X` → `consecutive_breach_count = 1` → **`falsified_pending`**
    (not an exit). Next print recovers → reset → `whipsaw_averted` logged → back to `confirming`.
  - Three straight sub-`X` prints with no differential widening → **`falsified`** (terminal, exit signal,
    outcome record).
  - Alternatively, a Fed pivot decouples PPI−CPI from credit → **`axis_decay`** alert (*instrument broke*,
    re-anchor the axis — distinct from the thesis being wrong).
  - Alternatively, the differential blows out to ≥ 75% of the modeled target → **`played_out`** + a
    priced-in check (is the remaining edge gone?).

### 5.12 Honest state

Nothing in Phase 3 exists yet. **Reusable today (✅):** `SourceIntake` / `EvidenceExtraction` /
`TemporalContext`; the freeze → additive `PostCaseCalibration` firewall pattern; the falsifier
observable+threshold requirement; the current-input seam. **Manual version buildable now:** inject a new
report through the seam, run a monitor pass, update a `ThemeWatch` by hand. **Automatic version gated** on
Phase 1 (persistence), Phase 4 (ingestion), and Phase 5 (news critic) — all already on the roadmap, now
with a second reason to exist.

---

## 6. Phase 4 — Live ingestion (the entrance)

*Add. Size: L; highest single risk.*

Implement `engine/stage0.parse_research_text` (currently a `NotImplementedError` stub). A generative LLM
seam that turns a PDF/markdown into the three Stage-0 streams (`Observation` / `CandidateTheme` /
`ConsensusSignal`), produces **case** evidence, stays inside the firewall, never leaks trades, and
generalizes evidence extraction beyond the JPM-tuned regex.

- **Touches:** stage0, both providers, the current-input seam, the semantic contract (extend beyond its
  4 input kinds), `evidence_extraction`, no-trade/copyright guards.
- **Acceptance:** a real PDF produces typed streams; expression stays scripted-only; semantic contract
  rejects unknown-kind leakage; same document → same streams (temperature-0 / cached → determinism).

**Unlocks:** *automatic* discovery-from-PDF and *automatic* surveillance-from-news. Until it lands, both
run manually through the seam — enough to demo the full loop.

---

## 7. Phase 5 — News critic + memory categorization + sufficiency gate (hardening)

*Add (news critic, sufficiency) + refactor (categorization). Size: M + S + M.*

| ID | Build | State | Action | Acceptance |
|---|---|---|---|---|
| #9 | **GDELT news critic** | ❌ missing | Feeds Phase 3; every item tagged **attention-not-evidence**; cannot raise conviction alone (the `corroboration − attention` divergence run forward). | Coverage never flips a watch to `confirming` on its own; populates `is_attention_only`. |
| D4 | **Memory categorization** | ⚠️ binary only | Extend the taxonomy *within* method (by reasoning function ≈ skill card) and *within* case (regime × axis × mechanism × outcome) **without touching the binary Phase-A gate** — that fail-closed method-only gate is load-bearing. | A case sub-tag never becomes Phase-A-readable; firewall test suite unchanged. |
| D5 | **Context-sufficiency gate** | ❌ missing | Block routing below a sufficiency floor so the engine refuses to manufacture 5–6 themes from a thin batch. | A thin batch → `blocked`; thresholds are **tested**, not hard-coded (the docs warn against this). |

**D4 detail — the two-axis memory you asked for:**

- **Method memory (textbooks) → by reasoning function**, one skill-card family each: causal
  identification (Pearl → `causal-compiler`, `backdoor-identifiability-gate`); systems/feedback (Meadows →
  `system-mapper`, `global-io-network`); regime (→ `macro-regime-classifier`, `macro-state-parser`);
  valuation/priced-in (→ `priced-in-estimator`, `term-premium-estimator`, `scenario-pricing-engine`);
  edge validity (→ `edge-validity`, `factor-r2-router`, `outcome-calibration-engine`). Lever:
  `SkillCompilerAgent` is contract_only and most cards are unwired — compile the rest, wire the
  `registered_unwired` ones **gated on the golden master**.
- **Case memory (20 yrs of reports/memos) → four tags** so Phase-B retrieval is by analogue, not
  keyword: **regime/epoch** · **axis/instrument** (makes a 2011 sovereign-bank note retrievable when
  today's theme shares the *same axis*) · **mechanism** (driver→transmission→outcome) · **outcome status**
  (requires the Phase-6 calibration loop — the missing "outcome-weighted theme memory").
- **Illustration from your own project files:** the Morgan Stanley BMI docs are method+case **hybrids**
  (the BMI *construction* — z-score, CDF→±10 mapping, factor selection — is method; the dated reading is
  case); Collin-Dufresne is **pure method** (the systematic-residual finding is a timeless mechanism).

---

## 8. Phase 6 — Outcome calibration (corpus-gated, last by necessity)

*Add. Size: M. Cannot precede Phase 3 — it consumes Phase 3's terminal records.*

Implement `calibration_report` / `edge_realization` in `engine/outcomes.py` (currently
`NotImplementedError`). Consumes the `ThemeOutcomeRecord`s that surveillance's terminal states
(`falsified` / `horizon_expired` / `played_out`) produce.

- **Acceptance:** given a closed-thesis corpus, emits a reliability diagram (q-calibration) +
  edge-realization regression; reads case memory **only post-freeze**.

**Unlocks:** the final loop closure — memory of historical scenarios *including how they resolved* (the
outcome-weighted theme memory you originally wanted).

---

## 9. Interactive state-machine simulator (spec + reference implementation)

> A working reference implementation ships alongside this plan
> (`theme_surveillance_simulator.html`). It implements the §5.3 transition function and the three
> guardrails **exactly**, so you can validate the logic before Claude Code touches it. The spec below is
> the contract; the HTML is one faithful realization of it.

**Purpose.** The surveillance system has three interlocking variables — *time passing*, *falsifier
metric*, *evidence valence*. Letting them play out interactively is the fastest way to validate that the
transition function routes status correctly and that the guardrails fire when intended.

**Controls (what the operator drives):**

- **Forward-horizon window** — select `3w | 6w | 3m | 4m` → sets `window_days`, which re-derives the
  staleness threshold and the half-life live (Guardrail 2 made visible).
- **Advance clock** — step forward one read period (`breach_obs_freq`, default weekly). Each step
  performs a falsifier read at the current metric value and ages all evidence.
- **Falsifier metric** — set the current value relative to threshold `X`; set `breach_buffer`. Drives
  `consecutive_breach_count`, `falsified_pending`, `falsified` (Guardrail 1 made visible).
- **Inject evidence** — `+ Confirming`, `+ Disconfirming`, `+ Neutral`, `+ Attention-only (news)`. Adds a
  `ThemeWatchEvent` at the current clock, resets the staleness clock, updates `net_valence`.
- **Axis realized %** — drive `played_out`.
- **Policy knobs** (advanced) — `k_stale`, `k_decay`, `lambda_disconfirm`, `valence_band`,
  `axis_target_fraction`.

**Panels:**

- **State graph (signature):** all eight states; the active one highlighted; the firing edge animated.
- **State-variable readout:** `consecutive_breach_count`, `days_since_evidence`, `staleness_threshold`
  (derived), `half_life` (derived), `net_valence` (derived), `elapsed / window_days`, `axis_realized`.
- **Transition tape:** every tick → the rule that fired + the reason string (`whipsaw_averted`,
  `falsifier_persisted`, `evidence_stale`, …). This is the audit trail.
- **Status banner:** the current status + alert type (`hold` vs `exit` vs `stalled` vs `axis_decay`).

**Simulator acceptance (it is faithful iff):**

- Holding the metric below `X` and advancing `breach_buffer` periods → `falsified_pending` for the first
  `breach_buffer−1` steps, then `falsified`. Recovering the metric before then → reset + `whipsaw_averted`.
- Switching the window from `3m` to `3w` makes a 4-day-quiet theme flip from noise to `stalled` with no
  other change.
- Injecting a disconfirming event moves `net_valence` more than a confirming event of equal magnitude
  (the `lambda_disconfirm` asymmetry is observable).
- An `Attention-only` event never moves status to `confirming`.

---

## 10. Open questions to seed `/ideate`

These are deliberately unresolved — good targets for Claude Code's ideation pass.

1. **Breach mode default.** Ship `consecutive` only, or expose `consecutive | integral` from day one?
   When is the decayed-integral variant *necessary* vs over-engineering for a daily/weekly series?
2. **Falsifier ⇄ axis-target consistency.** Should watch-creation lint **reject** a config where the
   falsifier threshold and the modeled target are simultaneously satisfiable on the same series, or just
   warn and let priority resolve it?
3. **Multi-falsifier themes.** The schema assumes one falsifier. Real theses often have 2–3. AND vs OR
   composition? Does *any* falsifier breach (with its own buffer) terminate, or a quorum?
4. **`lambda_disconfirm` calibration.** 1.5 is a guess. Should it be *learned* from the Phase-6
   outcome corpus (how often did confirming-at-the-time evidence precede a loss)? That closes a loop:
   calibration tunes the surveillance asymmetry.
5. **Scheduled-read source.** Who supplies the weekly falsifier read in production — a market-data
   adapter, or is every read an evidence event? (Affects determinism and the Phase-4 boundary.)
6. **Surveillance-output persistence.** Does a terminal `ThemeWatch` write back as its *own* CASE page
   (a closed-thesis record), feeding both Phase-6 calibration and the outcome-weighted case memory (D4)?
   Recommended: yes — fold into the Phase-1 persistence schema rather than a parallel store.
7. **Horizon-expiry grace.** Hard cutoff at `expected_close`, or a grace band keyed to volatility (a
   theme mid-resolution at expiry should perhaps get one more read, not an automatic `horizon_expired`)?
8. **Re-arming.** After `weakening` → recovery, is there hysteresis to prevent status flapping around the
   `valence_band`, beyond the dead-band? (e.g. require N confirming ticks to return from `weakening`.)

---

## 11. Sequencing summary (one line)

**L1/L2** (free wiring) → **L3** (cap, the theme-discipline down payment) → **Phase 1 persistence**
(the keystone) → **Phase 3 surveillance** (your priority; manual-capable immediately) → **Phase 2
compression** (parallel, highest quality leverage) → **Phase 4 ingestion** (automates the entrance) →
**Phase 5 hardening** → **Phase 6 calibration** (closes the loop). Build the spine, validate with
injected inputs, *then* automate the noisy entrance.

*Epistemic engine. Discovery and surveillance both STOP at alerts/strategy families. Expression remains
downstream and fenced. No trades are emitted anywhere in this plan.*
