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

**Opinion-driven, not number-driven (D-A1-1, decided 2026-08-09).** A1 clusters on
**opinion-bearing atoms only** — analyst posture, narrative frame, qualitative view (e.g. *"we
think the cycle is late,"* *"quality is under-priced,"* *"lending standards are tightening"*).
Numeric-only atoms (a default-rate table, a spread level) are **excluded from regime clustering**
— they belong to theme evidence (§4 L2), not to regime identity. A regime is the market's
*posture*, not its measurement. Concretely: an atom qualifies for A1 clustering iff its
`claim_kind ∈ {view, forecast, framing, mechanism}` — never `{measurement, level, tabular}`.
`RegimeType.defining_features` and `prevalence` are computed from the opinion subset only.

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

**Job.** Cluster grounded atoms into recurring themes. This is the **many-to-few** funnel — every
stage down is stricter than the one above:

```
150 markdowns
     ↓ harness (G1–G8)
~900 grounded claims / atoms
     ↓ A2 clustering + dedup + factor tractability
~12 candidate themes
     ↓ surveillance §5.3 state machine + L2 surprise
~4 active themes
     ↓ L5 aliveness + factor-tractability gate
~2 RV-ready themes
```

A theme's job in A2 is to survive clustering and pass tractability. Its job in surveillance is to
survive the state machine. Its job at L5 is to be both alive and cleanly expressible. Numbers are
illustrative — the funnel counts are recorded on every emit so drift is visible.

Factor tractability is decided **at inference time**, not at expression time. A theme that is
factor-untractable is still tracked, but the RV layer (L5) never sees it.

```
class SourceCoverage(BaseModel):
    markdowns_reviewed: int
    supporting_markdowns: int
    contradicting_markdowns: int
    background_markdowns: int
    unique_publishers_supporting: int
    first_seen: str
    last_reinforced: str

class InitialLifecycle(BaseModel):      # A2 sets DEFAULTS; surveillance owns runtime state
    created_at: str
    expected_review_at: str
    expected_retirement_at: str
    half_life_days: int                 # default 21
    max_life_days: int                  # default 90

class EvidenceScores(BaseModel):        # every score harness-computed (G4 / D4)
    support_score: float
    contradiction_score: float
    freshness_score: float
    novelty_score: float
    consensus_score: float
    crowding_score: float

class MappedRegimes(BaseModel):         # links to A1's RegimeVocabulary
    primary: list[str]                  # regime_ids
    secondary: list[str]

class FactorMap(BaseModel):
    macro: dict[str, float]             # growth, inflation, policy_rates, financial_conditions
    credit: dict[str, float]            # decompression, rating_quality, default_risk,
                                        # liquidity_quality, broad_credit_beta,
                                        # carry_roll_down, cash_cds_basis, …

class FactorTractability(BaseModel):
    decision: Literal["pass", "fail"]
    score: float                        # residual-alpha share; ≥ 0.40 → pass (D-L5-1)
    reason: str                         # harness-written; not model narrative

class ConsensusEffect(BaseModel):       # the split-effect rule (D-A2-3, "quarantine")
    # When N sell-side sources agree on a theme, the effect is SPLIT rather than compounded.
    support_delta: float                # small; consensus supports EXISTENCE, weakly
    consensus_delta: float              # larger; agreement is agreement
    crowding_delta: float               # larger still; agreement raises priced-in risk
    confidence_gamma_capped: bool       # confidence cannot exceed a ceiling on high crowding
    reason: str                         # harness-written

class SurpriseMetrics(BaseModel):       # narrative-level surprise (D-A2-6)
    # L2 handles NUMERIC surprise for state transitions. This block handles THEME-level
    # narrative surprise, which is what makes a transient theme valuable.
    narrative_surprise: float           # is the theme new vs recent research consensus?
    market_surprise: float              # is the theme not yet in spreads / basis / flows?
    revision_surprise: float            # are analysts changing view? (Δ position, not level)
    contradiction_surprise: float       # is strong evidence appearing against consensus?

class AdversarialCase(BaseModel):       # mandatory bear case (D-A2-4)
    # Every active theme MUST ship with the strongest case against itself, drawn from grounded
    # evidence — not an optional red-team step.
    against_theme: str                  # G8 closed-vocabulary; uses only kept atoms
    supporting_evidence: list[dict]     # [{atom_id, source, role: "contradiction"|"technical"}]
    system_response: str                # rebut, or move the numbers — one of the two
    conviction_cap: Optional[float]     # applied if the bear case remains material

class FalsifierTrigger(BaseModel):      # typed, not a free string (D-A2-5)
    series: str                         # e.g. "CCC/BB OAS ratio"
    condition: str                      # e.g. "compresses below 3-month median"
    deadline: Optional[str]             # e.g. "within 3 weeks"; None = open-ended
    implication: str                    # what its firing means for the theme
    retirement_state: Literal[          # explicit surveillance mapping when it fires
        "weakening", "contradicted", "invalidated", "played_out"
    ]

class ThemeCandidate(BaseModel):        # frozen
    theme_id: str
    canonical_name: str                 # deduped across the corpus
    thesis_statement: str               # one sentence, harness-verified (G8)
    aliases_seen: list[str]             # every paraphrase the dedup registry collapsed here
    supporting_atom_ids: list[str]
    contradicting_atom_ids: list[str]
    source_coverage: SourceCoverage
    initial_lifecycle: InitialLifecycle # DEFAULTS ONLY; surveillance takes over at first tick
    evidence_scores: EvidenceScores
    consensus_effect: ConsensusEffect   # required — the quarantine rule
    surprise_metrics: SurpriseMetrics   # required — narrative surprise
    adversarial_case: AdversarialCase   # required — bear case is mandatory
    mapped_regimes: MappedRegimes
    factor_map: FactorMap
    factor_tractability: FactorTractability
    falsification_triggers: list[FalsifierTrigger]   # typed, ≥1 required
    horizon: Optional[str] = None

class ThemeCandidateSet(BaseModel):     # frozen; emitted weekly
    contract_version: str               # "themeset/3"  ← bumped for consensus / surprise / adversarial / typed triggers
    as_of: str
    themes: list[ThemeCandidate]
    dedup_registry: dict[str, str]      # every alias → its canonical theme_id
    funnel: dict[str, int]              # markdowns / atoms / candidates / active / rv_ready
    ledger_root: str
```

**Rules.**
- **Aliases are first-class.** Every candidate carries every paraphrase the dedup registry
  collapsed under it. What you read in the book is exactly what the machine saw and merged —
  no hidden mergers.
- **Dedup thresholds (D-A2-1, Q3):** **IG 0.85**, **HY 0.75**, **cross-asset 0.85** (the
  stricter of the two so cross-class merging is deliberate), **other classes 0.80** as a
  placeholder pending data.
- **A2 sets initial lifecycle only.** `initial_lifecycle` is a set of **defaults**
  (half-life 21, max 90). Surveillance's state machine takes over from first tick and owns
  `lifecycle_state` thereafter (`SURVEILLANCE_BUILD_PLAN` §5.2, gate 5). A2 never authors
  runtime state.
- **All evidence scores are harness-computed** (G4). D4 applies: `CONFIDENCE_VERSION`
  stamps the formula, weights are constants in code, model never asserts them. `consensus_score`
  and `crowding_score` in particular consume the `ConsensusSignal` stream — attention data, not
  document counts.
- **Consensus quarantine (D-A2-3).** Sell-side consensus is **not** evidence a theme is true;
  it is evidence the theme is **crowded**. When N ≥ 2 additional sell-side sources agree, the
  effect is **split** — a small bump to `support_score` for theme existence, a larger bump to
  `consensus_score`, a larger bump still to `crowding_score`, and `confidence_gamma` is
  **capped** on high crowding. Reference numbers from the paper import: `+0.10 support`,
  `+0.20 consensus`, `+0.25 crowding` per additional independent publisher, cap at
  configurable ceiling. Otherwise the mesh becomes a sell-side echo machine. Composes with
  `SURVEILLANCE_BUILD_PLAN` §5.9 gate 3 ("attention ≠ evidence") — this is that gate's
  scoring implementation at inference time.
- **Contradiction increases informational value.** A credible contradicting source **lowers**
  `crowding_score` and **raises** `contradiction_surprise` (see `SurpriseMetrics`) — the
  opposite direction from a confirming one. Disagreement is signal.
- **Narrative surprise is scored, not just level (D-A2-6).** `SurpriseMetrics` asks four
  questions the paper insists on: is the theme new vs recent research consensus
  (`narrative_surprise`); is it not yet in spreads / basis / flows (`market_surprise`); are
  analysts changing view rather than restating (`revision_surprise`); is strong evidence
  appearing against consensus (`contradiction_surprise`). A theme that scores high on all four
  is **emerging**; one that scores low on all four is **already-priced consensus**. This is
  distinct from L2's numeric surprise, which lives per-atom and drives the surveillance state
  machine. Both exist; they operate at different layers.
- **Mandatory adversarial case (D-A2-4).** Every theme ships with an `AdversarialCase` — the
  strongest bear case, built only from grounded atoms (G8 closed-vocabulary), with a
  `system_response` that either rebuts it or moves numbers. Missing bear case → theme is
  **rejected** at A2 emit; a theme without a challenger is a theme without a fair test.
  Surveillance §5.7 blind disconfirm passes still run at monitoring time — this is the
  inference-time equivalent so the theme cannot be born unchallenged.
- **Typed falsification triggers (D-A2-5).** Each `FalsifierTrigger` carries
  `(series, condition, deadline, implication, retirement_state)` — not a free string. The
  `retirement_state` is the **explicit** surveillance transition that fires when the trigger
  breaches (weakening / contradicted / invalidated / played_out), so the state machine has no
  interpretive freedom. Minimum **one** trigger per theme; theme without a trigger is rejected
  (§5.9 gate 1 — "pre-registered falsifier is the primary trigger, not the narrative").
- **Retirement mechanics — the explicit mapping.** Trigger fires → transition to
  `retirement_state`. No fresh reinforcement past `half_life_days` → `fading`. Past
  `max_life_days` with no resolution → reviewed for retirement (surveillance owns the actual
  transition; A2 supplies the deadlines).
- **Macro and credit factor maps are kept separate.** `factor_map.macro` (growth, inflation,
  policy, financial conditions) is context for the book and for cross-theme portfolio inspection.
  `factor_map.credit` is what L5's tractability gate reads. Conflating them is how "the trade is
  actually a rates duration bet" hides.
- **Tractability is decided here, once.** `factor_tractability.decision` follows D-L5-1:
  residual-alpha share ≥ **0.40** → pass. Fail is retained but flagged `rv_layer_status="disabled"`;
  L5's gate short-circuits without recomputing.
- **Contradicting atoms are first-class.** Every theme carries both `supporting_atom_ids` and
  `contradicting_atom_ids`, and every contradicting atom that survived G1/G2 is available to
  the `AdversarialCase` writer — satisfying "mandatory adversarial evidence" at inference,
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

**Effort M · Risk medium — the expectation source is the hard part; see §6 D-L2-1.**

**Companion at the theme layer.** L2 handles numeric surprise per-atom (drives the surveillance
state machine). `SurpriseMetrics` on `ThemeCandidate` (A2, D-A2-6) handles **narrative**
surprise per-theme (is the theme new vs research consensus, not yet in prices, driven by
revisions, contradicting consensus). Both are needed. Never conflated: an atom that is
numerically surprising can still land inside a narratively-stale theme, and a narratively
fresh theme can be filled with numerically level prints. Score both, read both.

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

## 6. Decisions — resolved (2026-08-09)

All seven questions are answered. Binding on the build.

| # | Ref | Decision |
|---|-----|----------|
| 1 | **D-A1-1** | **Regime vocabulary — hard floor of 3.** Fewer than three → A1 halts and keeps last week's vocabulary (`stale_regime=True`). No false-narrow. |
| 2 | **D-A1-2 / D-A2-2** | **Assessment cadence — weekly + explicit trigger.** Weekly by default; manual re-fire on large ingests or on user request. Never automatic on ingest. |
| 3 | **D-A2-1** | **Dedup thresholds — per asset class.** IG 0.85 · HY 0.75 · cross-asset 0.85 (stricter of the two) · other classes 0.80 placeholder. |
| 4 | **D-A1-3** | **A1 regime clustering — opinion-only.** Clusters on `claim_kind ∈ {view, forecast, framing, mechanism}`; numeric-only atoms are excluded. A regime is the market's posture, not its measurement. |
| 5 | **D-L2-1** | **Expectation source for surprise (L2) — tiered.** Consensus forecast from a grounded source span first; prior print as fallback; **never** a model-generated expectation. None available → `kind="level"`; cannot move status toward `confirming`. |
| 6 | **D-L5-1** | **Residual-alpha threshold — 0.40.** Below → tractability=fail, RV layer disabled. Revisit after a quarter of data. |
| 7 | **D-L4-1** | **Book cadence & recipients — Monday morning, private.** Just the PM. Distribution decided later once the format has earned trust. |
| 8 | **D-L3-1** | **Pack retention — 24 months full; then age out raw atom text.** Metadata, outcomes, and scorecard inputs kept forever. |
| 9 | **D-A2-3** | **Consensus quarantine.** Extra sell-side agreement splits into `+support`, `+consensus`, `+crowding` (small / larger / larger still) with `confidence_gamma` capped on high crowding. Consensus is evidence of *crowding*, not truth. |
| 10 | **D-A2-4** | **Mandatory adversarial case.** Every theme ships with an `AdversarialCase` at inference time (against_theme, supporting_evidence, system_response). Missing bear case → theme rejected at A2 emit. |
| 11 | **D-A2-5** | **Typed falsification triggers.** Each trigger is `(series, condition, deadline, implication, retirement_state)`. Minimum one per theme; explicit `retirement_state` mapping so surveillance has no interpretive freedom when a trigger fires. |
| 12 | **D-A2-6** | **Narrative surprise scored alongside numeric surprise.** Four axes on every theme (narrative / market / revision / contradiction). Distinct from L2's numeric surprise (which drives the state machine per-atom). |

Decisions are recorded in code as constants under a `LIFECYCLE_DECISIONS_VERSION` stamp
(mirroring harness D4). Changing one is a reviewed code change plus a version bump; every past
pack and book stays interpretable against the version it was built under.

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

## 8. Scaffold landed — and what this plan got wrong (2026-08-12)

`engine/lifecycle/` now exists as **typed stubs only**: every model is real and frozen, every
function raises `NotImplementedError` naming its phase. Nothing is wired into the engine, so no
existing module gained a dependency and the golden master is untouched.
`tests/unit/test_lifecycle_scaffold.py` adds 36 tests.

### File layout

| Module | Responsibility |
|---|---|
| `lifecycle/decisions.py` | The twelve §6 decisions as constants under `LIFECYCLE_DECISIONS_VERSION` |
| `lifecycle/theme_view.py` | **L1** — the read-only join contract, `project`, `require_contract` |
| `lifecycle/regime.py` | **A1** — `RegimeVocabulary` and `discover_regimes` |
| `lifecycle/theme_enrichment.py` | **A2** — the blocks compression does not produce, keyed to `parent_id` |
| `lifecycle/surprise.py` | **L2** — `NumericContext`, `classify_number`, `collapse_levels` |
| `lifecycle/evidence_pack.py` | **L3a** — `EvidencePack` frozen at a terminal transition |
| `lifecycle/scorecard.py` | **L3b** — the cross-theme roll-up, recomputed from packs alone |
| `lifecycle/theme_book.py` | **L4** — the Monday artifact, a render of stored state only |
| `lifecycle/factor_projection.py` | **L5** — decomposition and the alive-and-tractable gate |

`engine/lifecycle/` is a different concept from the existing `engine/ledger/lifecycle.py`
(the ledger's own activation/falsification transitions). Every docstring says so.

### Four corrections to this document

**1. §3's `ThemeCandidateSet` is obsolete — `engine/compression.py` already does most of A2.**
`AnalystThemeMap` / `ParentTheme` already carry the canonical name, the causal mechanism, the
falsifier, the axis-or-watchlist, evidence-by-source, `why_it_might_be_wrong`, merged-cluster
accounting and the 3–7 cap; `CompressionStats` *is* the `funnel`, and `SourceCoverageMatrix`
*is* `SourceCoverage`. Building `ThemeCandidate` beside `ParentTheme` would give the repo two
theme types with two promotion gates. A2 is therefore scaffolded as **enrichment**:
`EnrichedThemeMap` holds a *reference* to the `AnalystThemeMap` and adds only the genuine gaps
(consensus effect, narrative surprise, mapped regimes, factor map, tractability, initial
lifecycle defaults, contradicting atom ids) plus structured upgrades of two partials — the
adversarial case (a sentence today) and the falsifier triggers (untyped today).

**2. §4/L1's `ThemeView` schema breaks the repo's own governing rule.** Four fields are typed
non-`Optional` — `surveillance_status: str`, `confidence: float`, `horizon: str`,
`ledger_root: str` — while L1's own test requires *"a blocked theme projects with
`surveillance_status` absent rather than guessed."* A required `float` forces `0.0`, which is
the "no data rendering as measured zero" that `engine/ledger/projection.py` explicitly refuses.
All four are `Optional` in the scaffold, and a test pins that decision. `ThemeView` also gains
`assembled_from` (required, non-empty — a hand-built view cannot name real source hashes) and
`unavailable` (which fields are `None` because their *producer* does not exist, as distinct
from measured-absent).

**3. §4/L3's `EvidencePack` leans on the wrong object.** It types `outcome` as
`ThemeOutcomeRecord`, but `engine/outcomes.py::ThemeOutcomeRecord` is a plain dataclass of
*pricing* calibration inputs (`p`, `q`, `X_s`, `X_mkt`, `predicted_edge`, `edge_std`) that a
discovery-only theme never has. Requiring it would force six fabricated numbers into the one
record that exists to be honest. The scaffold uses a local `TerminalOutcome` and points at the
pricing record via `outcome_ref` when one exists. The plan's `db/migrations/0004` is still
owed — existing migrations stop at `0002`.

**4. §5's ordering no longer holds.** L1 does not need A1 and A2 first: its existing-source
fields (`ThemeObject` + `ThemeWatch`) are available today, and `regime_ids` / `candidate_ref`
are `Optional`. L1 can be implemented immediately.

### What actually blocks implementation

§6 is **resolved**, so none of its questions block. But one resolved decision is stated in
vocabulary the codebase does not have, and that does block:

> **D-A1-3 is unbuildable as written.** It filters on
> `claim_kind ∈ {view, forecast, framing, mechanism}`, excluding `{measurement, level, tabular}`.
> **None of those seven strings exist in this repo.** The real vocabularies are
> `engine/temporal.py::ClaimKind` (`historical_fact, historical_forecast, source_opinion,
> current_fact, current_forecast, method_rule, unknown`) and
> `engine/evidence_extraction.py::_claim_kind` (`source_opinion, source_forecast, source_fact`).
> `view` and `forecast` map over cleanly; **`framing` and `mechanism` have no counterpart** — a
> mechanism is a *causal claim*, a separate extraction stream, not a claim kind at all.
> `decisions.OPINION_CLAIM_KINDS` is therefore an **empty frozenset** carrying the reason, and
> `discover_regimes` refuses while it is empty. This needs one human sentence.

Routed around rather than blocked: **G8 briefs and the G6 ledger** — `ThemeView` v1 omits
`briefs` and references the ledger by id, so L1 needs neither. **L5's factor data** — every
share is `Optional` and the gate closes on absence. **`no_view_twin`** — named in `unavailable`
rather than defaulted.

Also worth reconciling before A1 is implemented: `engine/schema/macro.py::MacroContext` and the
already-wired `macro-regime-classifier` skill produce a qualitative macro framing per theme.
That is a fixed taxonomy applied to one theme; A1 is a vocabulary inferred from the whole
corpus. Different jobs, but they must not emit two competing regime labels for the same week.

---

*Sections 1–7 are design only. Section 8 records the scaffold.*
