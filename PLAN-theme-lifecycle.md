# PLAN — Theme Lifecycle Layer (reconciliation + the real gaps)

> **Design doc only. No code in this PR.**
>
> **Purpose.** Twelve additions were proposed for the theme lifecycle. Most of them already exist
> — specified in `SURVEILLANCE_BUILD_PLAN.md`, built in `engine/`, or added in
> `PLAN-authoritative-harness.md`. This doc does two things and nothing else:
>
> 1. **§1 — says where each of the twelve already lives**, so no one rebuilds a solved problem.
> 2. **§2 — specifies the five that genuinely do not exist yet.**
>
> **It deliberately does not restate the surveillance state machine.** `SURVEILLANCE_BUILD_PLAN.md`
> §5 is the single source of truth for states, transitions, the breach buffer, staleness, and the
> blind adversarial scorer. If this doc ever appears to disagree with it, that plan wins.

**Companion docs.** `PLAN-authoritative-harness.md` (groundedness: nothing is invented) ·
`SURVEILLANCE_BUILD_PLAN.md` (is the thesis still true) · this doc (the artifacts a human reads and
the contract between stages).

---

## 1. Where the twelve already live

| # | Ask | Status | Where |
|---|-----|--------|-------|
| 1 | Formal ThemeView contract | **GAP** | — see §2 / **L1** |
| 2 | Separate collect / interpret / synthesize roles | **Covered** | Surveillance §5.7: the blind scorer is a *different call* from any summarizer that knows the thesis; status-update logic is deterministic code. Harness G3 splits propose/verify; G8 restricts the brief writer to verified atoms only. |
| 3 | Consensus quarantine | **Covered** | Surveillance §5.9 gate 3 — *attention ≠ evidence*. A news flood scores on `q`, not `p`; `is_attention_only=True` events **cannot** move status to `confirming`. `ConsensusSignal` is already its own Stage-0 stream. |
| 4 | Surprise-vs-level scoring | **GAP** | — see §2 / **L2** |
| 5 | Mandatory adversarial evidence | **Covered** | Surveillance §5.7 — disconfirm steelman runs *first*, blind to status, with disconfirmation asymmetry `lambda_disconfirm ≥ 1.0`. Stronger than "carry some adversarial evidence": ties break bearish by construction. |
| 6 | Falsification triggers | **Covered** | Surveillance §5.5 breach buffer + §5.9 gate 1 (pre-registered falsifier, set before the trade, immune to reinterpretation). Falsifiers already live on `risk.falsifiers`. |
| 7 | Archived evidence packs + scorecards | **GAP** | `ThemeOutcomeRecord` exists at terminal states, but there is no frozen pack and no cross-theme scorecard — see §2 / **L3** |
| 8 | Deterministic scoring + factor projection | **Split** | Deterministic scoring: **covered** (`engine/scoring.py`; harness G4 computes confidence, the model never asserts it). Factor projection: the `factor-r2-router` skill card exists but is *"readable in discovery but not auto-wired"* — see §2 / **L5** |
| 9 | Scope guard — operational repair only, no analytical self-rewrite | **Covered** | Surveillance §5.9 gate 5 (frozen object never mutates; the watch is an additive annotation stream keyed to `snapshot_hash`) + §0.3 activity taxonomy + harness §0/§9. |
| 10 | Theme delta vs baseline | **Covered** | Harness §7 `no_view_twin` — rerun with the model's view deleted (`p := q`); report `delta_rank`, `delta_edge`. |
| 11 | Live track record, not backtested confidence | **Covered** | Surveillance §5.2 terminal states emit `ThemeOutcomeRecord`; `horizon_expired` is scored *"like a stale sell-side call."* Persistence exists in `engine/thesis_tracker.py` + `db/migrations/0001`. |
| 12 | Weekly theme book with lifecycle states | **Split** | Lifecycle states: **covered** (Surveillance §5.2). Weekly *read cadence*: covered (`breach_obs_freq="weekly"`). The **book itself** — the artifact a human opens on Monday — does not exist. See §2 / **L4** |

**Score: seven fully covered, two split, three gaps.** Five things to build.

---

## 2. The five gaps

Inherits every invariant in `PLAN-authoritative-harness.md` §0 — in particular: golden master
byte-identical, new frozen-model fields `Optional` with defaults, no wall clock in new modules.

### L1 — The `ThemeView` contract  ·  [DET]  ·  first

**Problem.** Four consumers now read a theme: surveillance, the PM memo, the tracker, and (soon) the
weekly book. Each reaches directly into `ThemeObject` fields plus, separately, into the surveillance
annotation stream and the ledger. There is no single named thing that says *"this is what a
downstream reader is allowed to see, and this is the version of that shape."* Every new consumer
widens the coupling, and any field rename becomes a four-place change.

**Design.** `engine/schema/theme_view.py` — a **read-only projection**, never persisted as truth:

```
class ThemeView(BaseModel):          # frozen; assembled, never authored
    contract_version: str            # e.g. "themeview/1"
    theme_id: str
    snapshot_hash: str               # ties the view to the frozen object it projects
    statement: str
    horizon: str
    forward_horizon: Optional[ForwardHorizon]
    surveillance_status: str         # from SURVEILLANCE_BUILD_PLAN §5.2 — the state machine owns this
    briefs: list[SourceThemeBrief]   # harness G8
    falsifiers: list[Falsifier]      # from risk.falsifiers, with last read + breach state
    no_view_twin: Optional[NoViewTwin]
    factor_decomposition: Optional[FactorDecomposition]   # L5
    confidence: float                # harness G4 — computed, never model-asserted
    ledger_root: str                 # harness G6 — provenance entry point
```

**Rules.**
- Assembled by `engine/theme_view.py::project(theme, watch, ledger) -> ThemeView`. Pure; no I/O
  beyond reads; `now` passed in.
- **One-way.** Nothing consumes a `ThemeView` and writes back. It cannot mutate the frozen object —
  §5.9 gate 5 holds by construction.
- **Versioned.** `contract_version` bumps on any field removal or semantic change. A consumer
  asserts the version it was built against and fails closed on mismatch.
- Every consumer in §2 (L3, L4) and the PM memo reads `ThemeView` **only**.

**Tests.** `test_theme_view.py`: projection is pure; a frozen object is unchanged after projection;
version mismatch refused; a blocked theme projects with `surveillance_status` absent rather than
guessed.

**Effort S–M · Risk low.**

---

### L2 — Surprise-vs-level scoring  ·  [DET]  ·  after L1

**Problem.** Today an evidence atom carrying a number is treated the same whether the number
*surprised* or merely *restated a known level*. That is the single most common way a monitoring loop
fools itself: spreads are wide, every weekly print says spreads are wide, and the run of confirming
prints reads as accumulating evidence when it is one fact counted eight times. Surveillance §5.9 gate
3 already separates *attention* from *evidence*; this separates **level** from **change** inside
evidence itself.

**Design.** Extend the numeric provenance already built for harness G2 (which stores raw token +
canonical value — decision D6). Add, where an expectation is available:

```
class NumericContext(BaseModel):
    realized: float
    expected: Optional[float] = None      # consensus / prior print / model path
    expected_source: Optional[str] = None # must itself be a grounded span (harness G1)
    surprise: Optional[float] = None      # realized − expected, harness-computed
    surprise_z: Optional[float] = None    # scaled by trailing dispersion of the series
    kind: Literal["level", "change", "surprise"]
```

**Scoring rule (deterministic, in the §5.3 transition function):**
- `kind="surprise"` with `|surprise_z|` above threshold → **may** move status.
- `kind="level"` → **cannot** move status toward `confirming`. It can sustain `armed`, and it still
  counts for staleness (a level print is a heartbeat: the series is alive).
- No expectation available → `kind="level"`. Absence of an expectation is never treated as surprise.
- Repeated identical levels are **collapsed**: N consecutive same-signed level prints contribute the
  weight of one, so a fact cannot be counted eight times.

**Fail-closed.** If `expected` cannot be grounded to a source span, `surprise` is not computed —
it is not estimated by the model.

**Tests.** `test_surprise_scoring.py`: eight identical level prints do not reach `confirming`; one
genuine surprise does; an ungrounded expectation yields `kind="level"`; a level print still resets the
staleness clock.

**Effort M · Risk medium — the expectation source is the hard part; see §4 open question 1.**

---

### L3 — Evidence pack + scorecard  ·  [DET]  ·  after L1

**Problem.** `ThemeOutcomeRecord` records *what happened*. Nothing records *what we knew when we
said it*. Six months later you cannot reconstruct whether a call was wrong because the evidence was
thin, because the reasoning was bad, or because the world changed — which is the only question worth
asking after a loss.

**Design — two artifacts.**

**(a) Evidence pack** — frozen at every terminal transition (`falsified`, `horizon_expired`,
`played_out`), written once, never updated:

```
class EvidencePack(BaseModel):
    theme_id: str
    snapshot_hash: str
    terminal_status: str
    packed_at: str
    theme_view: ThemeView                 # the L1 projection as of terminal
    atoms: list[EvidenceAtom]             # every kept atom, with grounding verdicts
    briefs: list[SourceThemeBrief]        # harness G8
    blind_scoring_passes: list[dict]      # surveillance §5.7 disconfirm + confirm + adjudication
    falsifier_reads: list[FalsifierRead]  # the full read series, not just the breach
    outcome: ThemeOutcomeRecord
```

Stored beside the provenance ledger (harness D5): `db/migrations/0004_evidence_packs.sql`,
append-only. A pack is immutable — a correction is a **new** pack that references its predecessor.

**(b) Scorecard** — the cross-theme roll-up, computed from packs, never hand-maintained:

| Metric | Definition |
|---|---|
| Hit rate by terminal state | count `played_out` / (`played_out` + `falsified` + `horizon_expired`) |
| Median time-to-terminal | by state, vs `forward_horizon` |
| Falsifier quality | share of `falsified` where the pre-registered falsifier fired *before* the P&L did |
| Expiry rate | share of `horizon_expired` — a high rate means themes are being written without a clock |
| **View contribution** | mean `delta_rank` / `delta_edge` from `no_view_twin` on winners vs losers |
| Evidence thinness | median grounded-atom count per terminal theme, split by outcome |

The last two are the ones that matter. *View contribution* answers "is the model adding anything?"
with realized outcomes rather than self-assessment. *Evidence thinness* tells you whether losses
correlate with thin evidence — actionable — or not — which means the process, not the sourcing, is
what needs work.

**Fail-closed.** A terminal transition that cannot write a complete pack **blocks the transition**
and raises to the PM. Losing the record of a loss is worse than a delayed status change.

**Tests.** `test_evidence_pack.py`: pack written on each terminal state; immutability enforced;
incomplete pack blocks transition; scorecard recomputes identically from packs alone.

**Effort M–L · Risk low.**

---

### L4 — Weekly theme book  ·  [DET]  ·  after L1 + L3

**Problem.** The read cadence exists (`breach_obs_freq="weekly"`). The *artifact* does not. Without
one, lifecycle states live in a database and the human never sees a theme quietly go stale.

**Design.** `engine/theme_book.py::render_week(as_of: date) -> ThemeBook` — pure, deterministic,
reads `ThemeView`s and packs only. Markdown output mirroring
`thesis_tracker.export_thesis_tracker_markdown`.

**Sections, in this order** (most decision-relevant first):

1. **Needs a decision** — `falsified_pending` (buffer running, with days left), and horizons
   expiring inside 30 days. This is the only section that is *supposed* to prompt action.
2. **Changed since last week** — state transitions, with the triggering evidence and its
   `surprise_z` (L2). Includes deltas in `no_view_twin`.
3. **Live book** — `armed` / `confirming` / `weakening` / `stalled`, one line each: statement, state,
   days since last evidence, next scheduled falsifier read.
4. **Closed this week** — terminal transitions with a one-line outcome and a link to the pack.
5. **Scorecard** — the L3 roll-up, trailing 12 months.

**Rules.**
- **No new inference.** The book renders stored state. It never calls an LLM and never recomputes
  a status — if the book and the state machine disagree, the book is wrong.
- Deterministic: same inputs and `as_of` → byte-identical output. Testable by golden file.
- `as_of` is passed in; the renderer never reads the clock (invariant I8).

**Tests.** `test_theme_book.py`: golden-file render; a theme going stale appears in *Changed*; empty
week renders without error; no provider is constructed anywhere in the call path.

**Effort M · Risk low.**

---

### L5 — Wire factor projection, and gate expression on it  ·  [DET + skill]  ·  last

**Problem.** `factor-r2-router` exists as a compiled method card and is explicitly *"readable in
discovery but not auto-wired."* So the question its card is built to answer — *is this expression
harvesting a known risk premium, or is it actually our thesis?* — is currently answered by nobody.
This is also the missing half of ask #8 and the whole of your closing requirement: propose RV
expressions **only when the theme is alive and factor-tractable**.

**Design.**
- `engine/factor_projection.py::decompose(expression, thesis_axis, factor_premia) ->
  FactorDecomposition {factor_loadings, harvested_premium_share, residual_alpha_share,
  purity_estimate, premium_overlap_flags}` — the skill card's declared `output_objects`, typed.
- Attach to `ThemeView` (L1) as `factor_decomposition`.
- **The two-part gate** (deterministic, in the router, before any expression is proposed):

  | Condition | Requirement |
  |---|---|
  | **Alive** | `surveillance_status ∈ {armed, confirming}`. Not `weakening`, `stalled`, `falsified_pending`, and obviously not terminal. |
  | **Factor-tractable** | `residual_alpha_share ≥ threshold` **and** no unresolved `premium_overlap_flag`. |

  Both true → strategy families may be proposed and ranked. Either false → no expression, with the
  reason recorded (`not_alive:<status>` / `not_tractable:<flag>`). A theme can be perfectly true and
  still fail this gate — that is the point. The output is *"real but not expressible right now."*

**Boundary — unchanged.** This stops at **ranked strategy families**, matching the activity taxonomy
(`SURVEILLANCE_BUILD_PLAN` §0.3): legs, sizes and hedge ratios remain fenced in expression mode. The
skill card's own `not_allowed_to_influence` list is binding — factor projection must not touch
scenario probabilities `p_s`, golden-master numbers, the rho-squared cap math, `q`-tilt, or
`residual_edge`.

**Fail-closed.** Missing factor data → gate returns *not tractable*. Absence of evidence about
factor overlap is never read as absence of overlap.

**Tests.** `test_factor_projection.py`: a carry trade that is mostly harvested premium fails the
gate; a live, high-residual theme passes; a `weakening` theme fails on aliveness even with perfect
purity; golden master untouched.

**Effort L · Risk medium — it touches the routing seam.**

---

## 3. Sequencing

| Step | Ships | Why here |
|------|-------|----------|
| **1** | **L1** ThemeView contract | Everything else reads it. Build it first or build the coupling twice. |
| **2** | **L2** surprise-vs-level | Feeds the §5.3 transition function; wrong status data poisons packs and the book. |
| **3** | **L3** evidence pack + scorecard | Needs L1; needs L2 for the record to be honest about *why* status moved. |
| **4** | **L4** weekly theme book | Renders L1 + L3. Pure presentation — no new logic. |
| **5** | **L5** factor projection + expression gate | Highest blast radius (routing seam). Land it once the lifecycle beneath it is stable. |

Prerequisite: harness **Phase 3** (G6 ledger, G8 briefs, `no_view_twin`) — L1 projects all three.

---

## 4. Open questions (need your call before L2 and L5)

1. **Expectation source for surprise (L2).** Where does `expected` come from — consensus forecast
   from a source markdown, the prior print, or a model path? Each has a different grounding story.
   *Recommend: consensus from a grounded span first; prior print as fallback; never a model path.*
2. **Residual-alpha threshold (L5).** What `residual_alpha_share` counts as factor-tractable? This is
   a risk-appetite call, not a technical one.
3. **Book cadence and recipient.** Weekly Monday? Just you, or a PM distribution?
4. **Pack retention.** Keep evidence packs indefinitely, or age out the raw atom text after N months
   and retain the scorecard inputs only?

---

## 5. What this plan does NOT change

- The surveillance state machine (`SURVEILLANCE_BUILD_PLAN.md` §5) is untouched. L2 supplies it a
  better-typed input; it does not re-specify a single transition.
- The frozen `ThemeObject` never mutates. `ThemeView` is a projection; packs are additive; the book
  is a render.
- No trades, legs, sizing, hedge ratios or execution. L5 gates *whether* strategy families may be
  proposed — it does not propose positions.
- The golden master stays byte-identical.

---

*Design doc only. No engine code is modified by this PR.*
