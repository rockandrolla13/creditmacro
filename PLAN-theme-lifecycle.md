# PLAN — Theme Lifecycle Layer (workflow + upstream assessment + the real gaps)

> **Design doc only. No code in this PR.**
>
> **Purpose.** Specify the **top-level workflow** the system must produce, place every proposed
> addition against it, and detail the pieces that genuinely do not exist yet. The workflow is:
> sources → harness (verified atoms) → **upstream corpus assessment (regime + theme discovery)** →
> condensed view objects → temporal tracking → RV expressions behind an aliveness + factor gate.
>
> This doc has four parts:
>
> 1. **§1 — the corrected top-level workflow**, so nothing is out of order.
> 2. **§2 — where each of the twelve proposed additions already lives**, so no one rebuilds a
>    solved problem.
> 3. **§3 — the upstream assessment layer** (A1 regime discovery + A2 theme discovery / factor
>    mapping). This is a stage the two existing plans did not cover.
> 4. **§4 — the five downstream lifecycle gaps** (L1 ThemeView contract, L2 surprise-vs-level,
>    L3 evidence packs, L4 weekly book, L5 factor projection + expression gate).
>
> **It deliberately does not restate the surveillance state machine.** `SURVEILLANCE_BUILD_PLAN.md`
> §5 is the single source of truth for states, transitions, the breach buffer, staleness, and the
> blind adversarial scorer. If this doc ever appears to disagree with it, that plan wins.

**Companion docs.** `PLAN-authoritative-harness.md` (groundedness: nothing is invented) ·
`SURVEILLANCE_BUILD_PLAN.md` (is the thesis still true) · this doc (the assessment layer, the
artifacts a human reads, and the contract between stages).

---

## 1. The corrected top-level workflow

Reading top to bottom. Every stage consumes only outputs of the stage above it. Nothing skips
levels; nothing loops backward silently (the only loop is surveillance's mark-to-market feedback,
governed by `SURVEILLANCE_BUILD_PLAN.md` §5.3).

```
                    SOURCE MATERIAL
                    markdowns from PDFs, Substack, sites,
                    newsletters, reports
                              │
                              ▼
              ┌──────────────────────────────┐
              │ HARNESS  (per source, per    │
              │ atom)  — G1..G8              │  ← PLAN-authoritative-harness.md
              │  grounded atoms, verified    │
              │  numbers, briefs, ledger     │
              └───────────────┬──────────────┘
                              │  (atom pool: only grounded atoms
                              │   ever cross this line)
                              ▼
              ┌──────────────────────────────┐
              │ UPSTREAM CORPUS ASSESSMENT   │  ← §3 of THIS doc  (NEW)
              │                              │
              │  A1  Regime discovery        │
              │  A2  Theme discovery +       │
              │      factor mapping          │
              └───────────────┬──────────────┘
                              │
                              ▼
              ┌──────────────────────────────┐
              │ CONDENSED VIEW OBJECTS       │
              │  · RegimeVocabulary  (3–7)   │
              │  · ThemeCandidateSet         │
              │  · ThemeFactorMap            │
              └───────────────┬──────────────┘
                              │
                              ▼
              ┌──────────────────────────────┐
              │ TEMPORAL TRACKING            │  ← §4 (L1..L4) of THIS doc
              │  emerge → strengthen →       │     + SURVEILLANCE_BUILD_PLAN.md §5
              │  mutate → fade → retire      │
              │  (surveillance state machine │
              │   with mark-to-market loop)  │
              └───────────────┬──────────────┘
                              │
                              ▼
              ┌──────────────────────────────┐
              │ CREDIT RV LAYER (gated)      │  ← §4 / L5
              │  proposed only when the      │
              │  theme is ALIVE and          │
              │  FACTOR-TRACTABLE            │
              └──────────────────────────────┘
```

**The AI's first job**, then, is not to route claims to pre-existing themes. It is to read the
corpus and infer:

1. **What regime vocabulary is being implied?** (A1)
2. **What recurring themes are present?** (A2)
3. **Which of those themes are tradeable via known credit factors?** (A2's factor map + L5's gate)

Only after that inference produces condensed, frozen view objects does the lifecycle machinery
kick in. This ordering matters: without an explicit corpus-assessment stage, themes are inferred
one-source-at-a-time and the system suffers three failures — theme proliferation, regime
blindness, and late factor mapping. §3 fixes all three.

---

## 2. Where the twelve already live

| # | Ask | Status | Where |
|---|-----|--------|-------|
| 1 | Formal ThemeView contract | **GAP** | — see §4 / **L1** |
| 2 | Separate collect / interpret / synthesize roles | **Covered** | Surveillance §5.7: the blind scorer is a *different call* from any summarizer that knows the thesis; status-update logic is deterministic code. Harness G3 splits propose/verify; G8 restricts the brief writer to verified atoms only. **A1/A2 (§3) makes this stronger**: assessment is a fourth, corpus-level role, structurally separated from per-atom extraction. |
| 3 | Consensus quarantine | **Covered** | Surveillance §5.9 gate 3 — *attention ≠ evidence*. A news flood scores on `q`, not `p`; `is_attention_only=True` events **cannot** move status to `confirming`. `ConsensusSignal` is already its own Stage-0 stream. |
| 4 | Surprise-vs-level scoring | **GAP** | — see §4 / **L2** |
| 5 | Mandatory adversarial evidence | **Covered** | Surveillance §5.7 — disconfirm steelman runs *first*, blind to status, with disconfirmation asymmetry `lambda_disconfirm ≥ 1.0`. Stronger than "carry some adversarial evidence": ties break bearish by construction. |
| 6 | Falsification triggers | **Covered** | Surveillance §5.5 breach buffer + §5.9 gate 1 (pre-registered falsifier, set before the trade, immune to reinterpretation). Falsifiers already live on `risk.falsifiers`. |
| 7 | Archived evidence packs + scorecards | **GAP** | `ThemeOutcomeRecord` exists at terminal states, but there is no frozen pack and no cross-theme scorecard — see §4 / **L3** |
| 8 | Deterministic scoring + factor projection | **Split** | Deterministic scoring: **covered** (`engine/scoring.py`; harness G4 computes confidence, the model never asserts it). Factor projection: the `factor-r2-router` skill card exists but is *"readable in discovery but not auto-wired"* — see §4 / **L5**, and note that A2 (§3) moves factor mapping upstream so tractability is known at inference time. |
| 9 | Scope guard — operational repair only, no analytical self-rewrite | **Covered** | Surveillance §5.9 gate 5 (frozen object never mutates; the watch is an additive annotation stream keyed to `snapshot_hash`) + §0.3 activity taxonomy + harness §0/§9. |
| 10 | Theme delta vs baseline | **Covered** | Harness §7 `no_view_twin` — rerun with the model's view deleted (`p := q`); report `delta_rank`, `delta_edge`. |
| 11 | Live track record, not backtested confidence | **Covered** | Surveillance §5.2 terminal states emit `ThemeOutcomeRecord`; `horizon_expired` is scored *"like a stale sell-side call."* Persistence exists in `engine/thesis_tracker.py` + `db/migrations/0001`. |
| 12 | Weekly theme book with lifecycle states | **Split** | Lifecycle states: **covered** (Surveillance §5.2). Weekly *read cadence*: covered (`breach_obs_freq="weekly"`). The **book itself** — the artifact a human opens on Monday — does not exist. See §4 / **L4**. The book's top section becomes the regime backdrop emitted by A1. |

**Score: seven fully covered, two split, three gaps** — plus **one upstream stage** (A1/A2, §3)
that neither prior plan specified. So: **two things to build upstream, five things to build
downstream. Seven items total.**

---

## 3. Upstream — the corpus assessment layer (A1, A2)

The lifecycle plan (L1–L5) assumes themes already exist as objects to track. Today they don't —
they are inferred implicitly by matching each new atom against whatever themes happen to be in the
tracker. That has three failure modes:

- **Theme proliferation.** Every analyst phrasing spawns its own theme; nothing forces a canonical
  vocabulary.
- **Regime blindness.** Themes are tracked in isolation, without a regime backdrop. A "quality
  decompression" theme reads differently in a growth-slowdown regime than in an issuance-glut
  regime; today nothing captures the backdrop.
- **Late factor mapping.** Tradeability via known credit factors is discovered per theme after the
  fact, not corpus-wide up front.

**Design.** A corpus assessment layer runs on the weekly cadence (matching L4), reads the current
pool of grounded atoms, and emits three condensed view objects. Every artifact it produces still
passes through the same eight harness guardrails — this stage does **not** invent claims; it
*summarizes* claims the harness already verified.

**Composes with the harness (invariants unchanged).** Every input is a harness-verified atom
(G1/G2). Every proposed regime name and theme name passes G3 (proposer–verifier). Every emitted
narrative passes G8's closed-vocabulary brief gate — the assessment writer sees only the atom set,
never raw markdown, so it cannot cite what it was never shown. Every emitted view object is a G6
ledger node with the underlying atoms as parents. Nothing in the assessment layer authors a
confidence, a grounding verdict, or a ledger entry (G4/G1/G6).

### A1 — Regime discovery

**Job.** Read the atom pool. Infer a small vocabulary — typically **3–7** regime types — the
corpus is implicitly using. Each regime is a named cluster with defining features drawn from
grounded atoms.

```
class RegimeType(BaseModel):        # frozen
    regime_id: str
    name: str                       # e.g. "growth_slowdown_tight_credit"
    defining_features: list[str]    # each backed by ≥1 grounded atom
    supporting_atom_ids: list[str]  # all must be harness-verified
    prevalence: float               # share of atoms consistent with this regime
    first_seen: str
    last_seen: str

class RegimeVocabulary(BaseModel):  # frozen; emitted weekly
    contract_version: str           # "regime/1"
    as_of: str                      # date, passed in — no wall clock (harness I8)
    regimes: list[RegimeType]       # 3–7; hard cap enforced
    dominant_regime_id: str         # highest prevalence
    ledger_root: str                # G6 provenance entry point
```

**Rules.**
- Prevalence is **harness-computed** from the atom set — never model-asserted (G4 discipline).
- The 3–7 cap is a hard limit. If the LLM proposes more, they are merged by dedup (embedding +
  canonical name); if fewer, the model may abstain, and the run keeps last week's vocabulary with
  a `stale_regime=True` flag rather than fabricating change.
- Regime transitions are surfaced weekly (see L4 book): "regime dominant this week vs last."

### A2 — Theme discovery + factor mapping

**Job.** Cluster grounded atoms into recurring themes. For each theme, immediately test whether it
is tradeable via the known credit factor set — that gate happens **at inference time**, not later
at expression time. A theme that is factor-untractable is still tracked, but the RV layer (L5)
never sees it.

```
class ThemeCandidate(BaseModel):    # frozen
    theme_id: str
    canonical_name: str             # deduped across the corpus
    thesis_statement: str           # one sentence, harness-verified
    supporting_atom_ids: list[str]
    contradicting_atom_ids: list[str]
    regime_ids: list[str]           # which regimes this theme lives in
    factor_map: Optional[FactorMap] = None  # A2 projection; None if untractable
    horizon: Optional[str] = None

class ThemeCandidateSet(BaseModel): # frozen; emitted weekly
    contract_version: str           # "themeset/1"
    as_of: str
    themes: list[ThemeCandidate]
    dedup_registry: dict[str, str]  # near-duplicate name → canonical
    ledger_root: str
```

**Rules.**
- **Dedup is mandatory.** Two analysts phrase one idea differently; the dedup registry matches on
  embedding similarity and canonical-name normalization, and any theme ≥0.85 similar to an
  existing canonical one is merged, not spawned. This is what stops theme proliferation.
- **Factor mapping runs at inference time.** `factor_map` uses the `factor-r2-router` skill card
  (already in the repo). A theme with `factor_map=None` is retained for tracking but flagged
  `rv_layer_status="disabled"` — L5's gate will refuse it.
- **Contradicting atoms are first-class.** Every theme carries both `supporting_atom_ids` and
  `contradicting_atom_ids`, satisfying the "mandatory adversarial evidence" spirit at inference,
  not just at monitoring.

### How the assessment feeds L1–L5

- `RegimeVocabulary.regimes` is stamped onto every downstream `ThemeView` (L1) as regime context.
  `ThemeView.regime_ids` names the regime(s) the theme lives in as of that snapshot.
- `ThemeCandidateSet.themes` are the input to L1's projection. A candidate that passes L5's
  aliveness-and-tractability gate becomes an active tracked theme in the surveillance state
  machine (`SURVEILLANCE_BUILD_PLAN` §5).
- The L4 weekly book gains a **top section: Regime backdrop** — what regime the corpus is
  currently implying, what changed from last week, and how each active theme is repositioned
  under the new backdrop.

### Fail-closed behaviour

- A1 or A2 cannot ground its outputs → the assessment run **blocks**, last week's frozen view
  objects remain authoritative, and the L4 book renders with a `stale_assessment=True` banner.
  A stale but honest book beats a fresh but fabricated one.
- Factor mapping without sufficient factor data → `factor_map=None`, theme still tracked, L5 gate
  closes. Absence of factor evidence is never read as absence of factor exposure.
- Dedup collision above threshold with a **retired** theme → the new atoms are surfaced as
  "candidate for lineage" and require the D1-style human confirmation gate before the retired
  theme is re-opened.

### Tests

- `test_regime_vocabulary.py`: cap enforced (3–7); prevalence recomputes deterministically from
  the atom set; abstention path keeps last week's vocabulary with `stale_regime=True`.
- `test_theme_candidate_set.py`: dedup collapses two paraphrases into one canonical theme;
  untractable theme retained but with `rv_layer_status="disabled"`; contradicting atoms attached
  when present in the pool.
- `test_assessment_composes_with_harness.py`: every referenced atom_id exists in the kept pool;
  every emitted narrative passes the G8 brief gate; unverified atom in a regime's
  `supporting_atom_ids` → refused.

**Effort M–L per stage · Risk medium** — the corpus-level clustering is where an LLM most wants
to invent structure; dedup + G3 verifier + G8 brief gate are what keep it honest.

---

## 4. Downstream — the five lifecycle gaps

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
    regime_ids: list[str]            # from A1 (§3); regime backdrop as of snapshot
    candidate_ref: Optional[str]     # the A2 ThemeCandidate.theme_id this view descends from
    briefs: list[SourceThemeBrief]   # harness G8
    falsifiers: list[Falsifier]      # from risk.falsifiers, with last read + breach state
    no_view_twin: Optional[NoViewTwin]
    factor_decomposition: Optional[FactorDecomposition]   # L5 (may reuse A2's factor_map)
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

**Effort M · Risk medium — the expectation source is the hard part; see §6 open question 1.**

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
  Where an A2 `factor_map` already exists on the theme, `decompose` **refines** it rather than
  recomputing from scratch — inputs already reviewed at inference time are not re-graded per PR.
- Attach to `ThemeView` (L1) as `factor_decomposition`.
- **The two-part gate** (deterministic, in the router, before any expression is proposed):

  | Condition | Requirement |
  |---|---|
  | **Alive** | `surveillance_status ∈ {armed, confirming}`. Not `weakening`, `stalled`, `falsified_pending`, and obviously not terminal. |
  | **Factor-tractable** | `residual_alpha_share ≥ threshold` **and** no unresolved `premium_overlap_flag`. A theme A2 already marked `rv_layer_status="disabled"` (untractable at inference time) short-circuits to *not tractable* without recomputing. |

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

## 5. Sequencing

Build the upstream stage before the downstream one — otherwise L1 has nothing to project and L5
has no factor map to consult.

| Step | Ships | Why here |
|------|-------|----------|
| **1** | **A1** RegimeVocabulary + weekly regime backdrop | Prerequisite for L1's `regime_ids`. Small, well-fenced by harness. |
| **2** | **A2** ThemeCandidateSet + dedup + factor mapping | Prerequisite for L1's `candidate_ref` and for L5's short-circuit. Highest-value single stage. |
| **3** | **L1** ThemeView contract | Everything downstream reads it. Now that A1+A2 exist, its schema is stable. |
| **4** | **L2** surprise-vs-level | Feeds the §5.3 transition function; wrong status data poisons packs and the book. |
| **5** | **L3** evidence pack + scorecard | Needs L1; needs L2 for the record to be honest about *why* status moved. |
| **6** | **L4** weekly theme book | Renders L1 + L3 + the A1 regime backdrop. Pure presentation — no new logic. |
| **7** | **L5** factor projection + expression gate | Highest blast radius (routing seam). Land it once the lifecycle beneath it is stable and A2's factor map is proven. |

**Prerequisite for A1/A2:** harness **Phase 3** (G6 ledger + G8 briefs). The assessment layer's
outputs are ledger nodes; its narratives are G8-gated briefs.

**Prerequisite for L1:** A1 + A2 landed and running weekly.

---

## 6. Open questions (need your call before A1, A2, L2, L5)

1. **Regime vocabulary count (A1).** The cap is stated as 3–7. Do you want a hard floor of 3, or
   is it acceptable for the model to emit fewer when the corpus is genuinely narrow?
   *Recommend: hard floor 3 — an over-narrow vocabulary is a red flag.*
2. **Assessment cadence (A1, A2).** Weekly matches the L4 book. Should the assessment also run
   on-demand when a large batch of new sources lands (e.g. >20 markdowns in a day), or is weekly
   the only cadence? *Recommend: weekly + explicit trigger, never automatic on ingest.*
3. **Dedup similarity threshold (A2).** 0.85 as a starting point — should it be tuned per
   asset class or held global?
4. **Expectation source for surprise (L2).** Where does `expected` come from — consensus forecast
   from a source markdown, the prior print, or a model path? Each has a different grounding story.
   *Recommend: consensus from a grounded span first; prior print as fallback; never a model path.*
5. **Residual-alpha threshold (L5).** What `residual_alpha_share` counts as factor-tractable? This
   is a risk-appetite call, not a technical one.
6. **Book cadence and recipient (L4).** Weekly Monday? Just you, or a PM distribution?
7. **Pack retention (L3).** Keep evidence packs indefinitely, or age out the raw atom text after N
   months and retain the scorecard inputs only?

---

## 7. What this plan does NOT change

- The surveillance state machine (`SURVEILLANCE_BUILD_PLAN.md` §5) is untouched. L2 supplies it a
  better-typed input; it does not re-specify a single transition. A1/A2 sit upstream of it
  entirely.
- The frozen `ThemeObject` never mutates. `ThemeView` is a projection; `RegimeVocabulary` and
  `ThemeCandidateSet` are new frozen objects with their own contract versions; packs are additive;
  the book is a render.
- Per-atom grounding (harness G1–G8) is unchanged. A1/A2 consume already-verified atoms and are
  themselves gated by G3/G6/G8. They do **not** loosen any harness rule.
- No trades, legs, sizing, hedge ratios or execution. L5 gates *whether* strategy families may be
  proposed — it does not propose positions.
- The golden master stays byte-identical.

---

*Design doc only. No engine code is modified by this PR.*
