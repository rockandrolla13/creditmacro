# creditmacro — Specification and State of the Project

**Written 2026-08-10** from the plan documents and the code, both read directly.
**Open items re-verified against the code 2026-08-12** — every entry in Part 4 was checked
by running the command it now cites. Two were fixed and are moved to Part 4C. One (§4.4)
is waiting on a human decision, not on work.

> **This document is a map, not a territory.** Where it summarises a rule, the linked
> document is canonical and wins on any conflict. Its job is to let you see the whole
> system at once and know which document to open next. It restates no rule it does not
> attribute.
>
> **Canonical sources, in precedence order for their own domain:**
> 1. `docs/ledger/ONTOLOGY.md` — normative for the Theme Hypothesis Ledger. Its own
>    preamble: *"Where this document and any other document conflict, this document
>    wins and the conflict is a bug."*
> 2. `SURVEILLANCE_BUILD_PLAN.md` §5 — the single source of truth for the surveillance
>    state machine.
> 3. `PLAN-authoritative-harness.md` — the grounding / anti-hallucination contract.
> 4. `docs/theme_object_contract.md` — the shared typed state and pipeline order.
> 5. `CLAUDE.md` — the product boundary and the four discipline gates.
>
> **Status tags** (the repo's own convention): ✅ implemented · ⚠️ partial ·
> 🚧 contract-only / scaffolded · ❌ missing · 🔒 firewall or gate.
>
> **Supersedes `docs/ENGINE_MANUAL.md` and `docs/ENGINE_CONTEXT_PACK.md`** (both
> 2026-06-13, both deleted 2026-08-10). Their component inventory, source lifecycle,
> skills registry and failure-mode catalogue are folded into Part 2 and re-checked
> against the current tree; the context pack was a condensed copy of the manual, so
> keeping either meant keeping a fact in three places. **There is now one state document.
> If you find yourself writing a second, update this one instead** — a fact recorded
> twice and updated once is the failure this repo has already had (Part 4.1).

---

# Part 1 — The specification

## 1.1 What the system is

An **epistemic engine**. It converts a research document into a falsifiable thematic
hypothesis and a ranked set of strategy families, and then it **stops at a PM decision
memo**. It does not emit trades, legs, sizes, hedge ratios, or execution.

The product boundary, as `README.md` states it:

```
idea / report / batch of sources
  → source classification        (method | case | mixed | ignore)
  → evidence extraction          (typed atoms + axes + falsifiers)
  → temporal classification      (current vs historical vs expired)
  → theme aggregation            (dedup into source-attributed clusters)
  → causal object / axes / strategy families + confidence
  → STOP   (status = strategy_family_routed, or a blocked HALT)
```

There are two modes. **Discovery** is the default and stops as above. **Expression**
(scenario pricing → fair value → scored expressions → sizing) is a separate, fenced,
downstream path that runs only on the deterministic scripted provider for golden cases.
The live LLM provider is structurally rejected in expression mode — it does not
implement the seams that mode requires.

## 1.2 The shared typed state

Two objects span the pipeline (`docs/theme_object_contract.md`):

- **`IngestionResult`** — Stage 0's three separate streams: `Observation` (facts),
  `CandidateTheme` (narratives), `ConsensusSignal` (attention), plus a ranked candidate
  list pre-screened by `divergence(evidence, attention)`. High factual support with low
  attention is the latent-edge signal; it is a proxy for `p − q` computed before any
  pricing.
- **`ThemeObject`** — the frozen, append-only record every later stage reads and writes.
  Identity, thesis, axis, scenarios, pricing, expressions, sizing, risk, PM gate,
  provenance, plus five optional skill-owned slices (iceberg classification, causal
  chain, system map, bias critique, loop diagnosis / trap implications).

The pipeline order is fixed in `engine/workflow.py` and documented as a ten-row table in
`docs/theme_object_contract.md` §2. The one structural subtlety: the trap detector runs
**twice** — `diagnose_loops` before pricing (its output feeds scenario construction) and
`assess_trap_implications` after (it reads scenarios, pricing and expressions). The
reversal point flows forward only, never backward.

**Adding a stage** is an optional field plus a provider seam plus a workflow line.
**Adding a case** is a YAML file. The schema is the interface; nothing is passed as prose.

## 1.3 The four discipline gates

A `ThemeObject` **cannot be constructed** unless all four hold (`CLAUDE.md`,
`docs/theme_object_contract.md` §3):

1. **The axis is operational** — a named spread or slope with a real, computable
   historical series. Not a concept, a series.
2. **`pricing.residual_edge` is computed.**
3. **At least one expression survived** the asymmetry / liquidity / cost gates.
4. **At least one falsifier** with an observable and a threshold.

These are type constraints, not quality scores. `CLAUDE.md` states the rule behind them:
*a thesis with no falsifier is not a thesis; do not emit it.*

## 1.4 The firewalls

Four gates, enforced by construction rather than by instruction.

**🔒 Memory access firewall — two-phase** (`engine/memory.py`, `engine/firewall.py`).
The hazard is old conclusions contaminating fresh reasoning. Every wiki page declares
`access_class: method | case`. **Method** memory teaches how to reason and is timeless.
**Case** memory records what a source or a past theme said and is time-bound.

- *Phase A* loads method pages only. `MemoryRetriever` is **fail-closed**: it returns
  method pages and refuses everything else — case, missing, invalid — returning `None`
  and logging the refused slug. There is no other path to wiki content, so phase A
  cannot retrieve case content.
- *Freeze.* `freeze()` serialises phase A into an immutable `FrozenSnapshot` with a
  SHA-256 content hash. The hash is marked on the retriever **before** phase B unlocks,
  so any case read is provably post-freeze.
- *Phase B* may read case pages, and only to find analogues and calibrate confidence.
  Changes go into a separate additive `PostCaseCalibration` block referencing the hash.
  The frozen object is never mutated.

The rule in one line: **reason fresh, freeze, then consult history — never the reverse.**

**🔒 Discovery / expression firewall.** A causal object is mandatory. With none,
discovery emits a `blocked` record rather than fabricating a path toward a trade.

**🔒 Temporal firewall** (`engine/temporal.py`). Only a `method_rule` claim may serve as
method context. An expired forecast forces `current_update_required`. A historical
source cannot be rendered as a current view — a 2019 call reads *"as of 15 March 2019
the source argued…"*, never *"the market is…"*.

**🔒 Semantic contract** (`engine/semantic_contract.py`). Before any snapshot, checks
the discovery output for economically wrong axes and for trade/sizing/expression
leakage. Fails closed. Currently narrow — four enumerated input kinds.

**❌ Context-sufficiency gate.** Specified in several documents, does not exist. The only
brakes on thin context today are a data-confidence floor of 0.5 and two confidence
ceilings (no scenarios → ≤0.45, no market value → ≤0.60).

## 1.5 The ledger ontology

`docs/ledger/ONTOLOGY.md` is normative and self-contained. The essentials:

**A theme is a tuple** `θ = (M, σ, X, H, F)`:

| Symbol | Meaning |
|---|---|
| `M` | transmission chain — a signed path `v0 --s1--> … --sk--> vk` over a controlled vocabulary |
| `σ ∈ {+1,−1}` | shock direction — the assertion that the channel is being driven *now*, in this direction |
| `X` | operational axis — the observable proxy for `vk`, carrying a sign convention `sign(X)` |
| `H` | forward horizon, `H ≤ 120 days` |
| `F` | falsifier — a decidable predicate over market data, no human judgment required |

**Direction is derived, never stored.** `d(θ) = σ · Π sj`, and on the axis
`d_X(θ) = d(θ)·sign(X)`. Any externally supplied direction that disagrees makes the
theme malformed.

**Identity is `(M, σ)` alone.** Everything else is attribute. Same prediction is not the
same theme — two themes agreeing on the axis and direction but with different
transmission stories are distinct, because they have different falsifiers and different
survival behaviour. Swapping the axis preserves identity. Reversing the shock creates a
new theme.

**Well-formedness gate `WF(θ)`** — five clauses, of which the first is the theme/forecast
boundary: `k ≥ 2` (at least one intermediate node). A `k = 1` claim — "spreads widen
because risk-off" — has no transmission to surveil and is rejected as a directional call.
A survival spike over the 86 existing theme pages found **82 of 86 fail this clause**;
that is why the population path is forward re-ingest rather than import.

**Bitemporal, event-sourced.** Every fact carries valid time (when the hypothesis claims
to hold) and transaction time (when the system recorded it). Themes are never mutable
rows; a theme is a fold over its event stream. No event may retroactively alter an
earlier as-of query.

**Scoring is a derived view, never stored.** `S_θ(t)` is a decayed, novelty-discounted,
per-institution-capped sum over the evidence links; `B_θ(t)` is the count of
institutions with positive net contribution. Both are pure functions of (ledger, t) and
invariant under append-order permutation.

**Lifecycle.** `CANDIDATE → ACTIVE` iff `B_θ ≥ 2 ∧ |S_θ| ≥ 2`. The absolute value is
deliberate: §Theme states that a theme with `S < 0` is **contested, not reversed**, and
§Lifecycle calls a contested theme *"a reportable sub-state of ACTIVE, not dead."*
`ACTIVE → FALSIFIED` happens only through breach-buffer confirmation of `F` — document
contra-evidence never falsifies, it decrements the score. The stated rationale: *analyst
disagreement is opinion flow; market breach is realized state.*

> ✅ **The code implements this rule.** It briefly did not; the divergence was closed on
> 2026-08-12 by restoring `abs()` in `engine/ledger/runner.py`. See Part 4C, item 4.1.

**Three status axes, orthogonal, never to be conflated** (amendment A3): pipeline
progress (`ThemeObject.status`), surveillance observation (`WatchStatus`), and market
truth (the lifecycle status above). `engine/ledger/projection.py` is the only site
permitted to map between them.

## 1.6 The surveillance state machine

`SURVEILLANCE_BUILD_PLAN.md` §5 owns this and no other document may re-specify it.

Surveillance answers one question — **is the thesis still true?** — and stops at an
alert. It never answers "what is my position?"

**States.** Non-terminal: `armed`, `confirming`, `weakening`, `stalled`,
`falsified_pending`. Terminal and absorbing: `falsified`, `horizon_expired`,
`played_out`. Each terminal state emits a `ThemeOutcomeRecord` and hands control to the
human.

**The transition function is prioritised, first match wins** (§5.3). Terminal states win
first, in the order played-out, falsified, horizon-expired — a realised thesis is a win
even amid a falsifier wobble. Within the active band a breaching falsifier dominates the
health read, then staleness, then valence. `armed` is the quiet default.

**Three guardrails, each solving a named failure:**

1. **Breach buffer.** A single breaching read moves the theme to `falsified_pending`,
   not `falsified`. It becomes terminal only if the breach persists for
   `breach_buffer` consecutive qualifying reads. An un-breach resets the counter and
   logs `whipsaw_averted`. *A point breach is not a broken thesis.*
2. **Horizon-keyed dynamics.** Both the staleness threshold and the evidence half-life
   scale with the window. A three-week theme quiet for four days is stalled; a
   four-month theme quiet for four days is noise. Clamps at both ends stop a tactical
   theme going stale over a weekend and a structural theme having a fifty-day blind spot.
3. **Blind adversarial scoring.** The valence scorer is **physically denied** the
   theme's current status, its lean, the P&L, and whether a trade is on — the context
   object structurally cannot carry them. It runs a disconfirm steelman first, then a
   confirm steelman, and the adjudication is deterministic code with a disconfirmation
   asymmetry `λ ≥ 1.0`, so ties break bearish. *The scorer cannot rationalise a
   conclusion it was never shown.*

**And five discipline gates** (§5.9), of which the third is the one most easily lost:
**attention is not evidence.** A news flood with no new atoms scores on the `q` side and
may mean the theme is getting priced in — pushing toward played-out and *lower* edge
expectation, not higher conviction. An attention-only event can never move status to
`confirming`.

## 1.7 The grounding harness

`PLAN-authoritative-harness.md`. Governing principle: **the LLM proposes, the harness
disposes.** The model emits typed, span-cited proposals and may always abstain. The
deterministic harness verifies grounding, computes every number and confidence itself,
and fails closed on anything it cannot trace to a verbatim source span.

Its non-negotiable, to be handed to any builder verbatim: *a missing output is always
preferable to an unsourced one. Blocked beats plausible.*

**Eight guardrails:**

| ID | Guards against | Phase |
|---|---|---|
| G1 | a claim citing a page that does not contain it | 1 |
| G2 | an invented or mis-transcribed number | 1 |
| G3 | a single generative pass fabricating a mechanism or a series | 5 |
| G4 | author-set confidence — false precision, and no first-class "I don't know" | 2 |
| G5 | prompt injection from third-party source documents | 4 |
| G6 | no single append-only graph tying an emitted claim to a span | 3 |
| G7 | silent model and prompt drift across versions | 6 |
| G8 | an unsourced sentence smuggled into the human-readable summary | 3 |

**Six binding decisions:**

- **D1 — tiered matching.** Tier A (exact) and Tier B (whitespace/quote-normalised) auto-
  accept. Tier C (bounded loose match) is **never** auto-accepted and queues to a human
  gate asking three questions. No fuzzy match ever becomes evidence without a person.
- **D2 — mode-dependent failure.** Discovery and theme-building **HALT** on an ungrounded
  atom. Wiki lint and bulk ingest skip-and-warn. The mode is an explicit parameter,
  never inferred; the default is HALT and lint must be asked for by name.
- **D3 — verifier independence.** The G3 verifier runs on a *different model id*, plus a
  deep-confirm rescan over the whole corpus before a theme is finalised.
- **D4 — confidence weights are constants in code** with a version string. Not tunable
  per run, not read from config, not settable by the model.
- **D5 — the provenance ledger is a separate SQLite store** from the hypothesis ledger.
  The document is explicit that this is *accepted* duplication, not *resolved*
  duplication, and says why: the hypothesis ledger is mid-build and joining two in-flight
  systems is how both stall.
- **D6 — numbers store both forms.** The raw source token *and* the canonical value plus
  unit. Match on canonical; display raw.

**Eight invariants**, gated after every step. The load-bearing ones: the golden master
stays byte-identical (I1); any new field on a frozen model is `Optional` with a default
and excluded from the content hash if it can vary (I6); no wall clock in new
deterministic modules (I8).

## 1.8 The governance protocol

The ledger build established a protocol that is the most valuable process artifact in the
repo, and it is worth stating plainly because it is what makes the rest trustworthy.

1. **The specification is normative.** A conflict between spec and code is a bug, and
   which one is wrong is a question to be *investigated*, not assumed.
2. **Every decision not derivable from the spec is recorded** in `ONTOLOGY_DELTA.md` at
   the moment it is made — decision, rationale, alternatives rejected, files affected.
3. **Every question the spec does not determine** goes in `BLOCKED.md` with a proposed
   resolution implemented behind a named constant. Nothing is silently chosen.
4. **Changing a constant is a specification change**, requiring an edit to the ontology
   plus a delta entry — *"never a local override."*
5. **Scheduled adversarial audits.** `SIGN_AUDIT.md` enumerated all eight sites in the
   ledger that compute a sign and checked each against the spec.

The sign audit is the worked example of the protocol functioning. It found the code and
the spec disagreeing about a polarity formula, established that **the code was right and
the spec was wrong**, amended the spec, and recorded delta D-07. No behaviour changed;
the contradiction was closed.

---

# Part 2 — State of the project

Test baseline **1065 passing** (`python -m pytest -q`, verified 2026-08-12 on branch
`harness-and-lifecycle`; was 898 on 2026-08-10). Engine: 99 modules, 18,132 lines.

## 2.1 Built and working ✅

The limitation column matters as much as the status column. Everything here works; each
row also says how far you can trust it.

| Subsystem | Module | What works | Known limitation |
|---|---|---|---|
| **Source intake** | `wiki_agents.py` | Deterministic keyword classifier → `access_class`, per-page classes, ingestion policy | Pure keyword signatures, no semantic understanding; a deck without a page manifest only warns |
| **Evidence extraction** | `evidence_extraction.py` | CASE markdown → atoms, causal claims, axes, confounders, falsifiers, family hints; refuses non-case sources | Regex and lexicon, visibly tuned to AI-credit / JPM. **Falsifiers are templated synthesis, not source-derived.** Family hints bypass the typed vocabulary |
| **Temporal classification** | `temporal.py` | Source role, expired/active horizons, per-claim phase-A admissibility, no wall clock | Forecast detection is regex; `current_date` must be supplied or context is skipped with a warning |
| **Theme aggregation** | `theme_aggregation.py` | Lexical clustering → clusters with corroboration / attention / divergence; parent cap and demotion logging | **This is where theme explosion lives** — see Part 3.2 |
| **Wiki persistence** | `wiki_integration.py` | Plan→apply, idempotent; no-trade and ≤25-word copyright guards | Deterministic dates are hardcoded constants; the copyright guard is per-line |
| **Engine 2 pricing** | `engine2.py` | Exact exponential-tilt `q`, Monte-Carlo edge with SNR and attribution, uncertainty-propagating fair value, feasibility status | `edge_mean` is the deterministic point identity while `edge_std` is Monte-Carlo — a documented hybrid, not a bug. Edge is **gross of risk premium** unless a pricing kernel is supplied |
| **Q4 probability** | `probability*.py` | Validates and tilts *supplied* `p_s`; maps supplied evidence to scenarios; audited posterior | Posterior is **audit-only** — pricing still reads `Scenario.p_s`. The tilt is a heuristic softmax, not calibrated likelihood ratios |
| **Strategy routing** | `discovery.py` | Twelve routable families, decomposed confidence, falsifier-gated promotion | `direction` is a free string; four hardcoded dispatch branches beside the route table |
| **Four firewalls** 🔒 | `memory.py`, `firewall.py`, `temporal.py`, `semantic_contract.py` | As specified in §1.4 | The semantic contract is narrow — four enumerated input kinds, no dedicated test file. `default_calibrator` is a reference implementation that makes **no** actual confidence change |
| **Theme Hypothesis Ledger** | `engine/ledger/` | All 7 phases: event log, fold, as-of queries, wiki import, blind Pass A, Pass B mapper, scoring view, orphan clustering, admission, renderer, drift diff, projection | `lifecycle.py` is a stub; `queries.valid_over` deferred; match-confidence calibration is open (BLOCKED B-01) |
| **Surveillance** | `surveillance.py`, `surveillance_agent.py` | State machine, three guardrails, monitor agent, terminal write-back, discovery→CASE persistence, forward horizon | Single falsifier per theme; the scheduled-read source in production is undecided |
| **Thesis tracker** | `thesis_tracker.py` | SQLite sidecar, computed view, audit log, CLI | Deliberately isolated — does not touch discovery, the firewall, or sizing, and infers nothing priceable |
| **Grounding kernel** | `engine/grounding/` | Span matching (exact + normalised, **no fuzzy**), unit-aware tokenizer incl. magnitudes and tenors (Part 4C/4.5, fixed 2026-08-12), `verify_atom`, `enforce`, wired into extraction | Mode hardcoded to lint (Part 4.4, awaiting your decision); Tier C not built; a bare year is still extracted from inside a date |
| **Provider seam** | `provider_select.py`, `llm_provider.py` | Scripted default; live LLM discovery-only, fails closed without explicit opt-in; capture/replay | The live provider supplies no scenarios and no evidence maps, so the live Q4 posterior always equals the prior |

**Agent registry** (`engine/wiki_agents.py`). Eight agents registered. Five implement
`run()`: source intake, evidence extraction, temporal context, multi-source aggregation,
wiki integration — plus the discovery runner and wiki lint, wired during the surveillance
build. `SkillCompilerAgent` still raises.

## 2.1b Source lifecycle and temporal roles

How a source is meant to move through the system:

```
PDF / markdown (immutable in raw/, markdowns/)
  → source classification  → access_class
  → temporal role          → TemporalContext.temporal_role
  → evidence atoms         → EvidenceExtractionBundle
  → per-source themes      → core_theme_candidates
  → cross-source clusters  → ThemeCluster[]
  → wiki persistence       → wiki/ pages
  → discovery              → ranked strategy families
```

**Access classes:** `method` (readable in phase A), `case` (gated — readable in phase A
*only* as explicitly supplied current input), `mixed` (treated conservatively as case),
`ignore`.

**Temporal roles:** `current_report`, `historical_case`, `stale_case`,
`outcome_candidate` (an expired forecast that should be *scored*, not acted on),
`method_source`, `unknown`.

**The current-input exception is the one to understand.** A case source can inform phase A
**only** when supplied as this run's current input through the seam in
`engine/protocols.py`. Archived case pages stay firewall-refused. That is what lets a
fresh report inform reasoning without re-opening the whole case archive.

## 2.2 Partial ⚠️

- **Grounding harness** — Phase 1 only. G1 and G2 are built and wired. G3–G8 are not.
- **Outcome memory** — the JSONL store works; `calibration_report` and `edge_realization`
  raise. Blocked on a closed-thesis corpus, which the surveillance close-out loop has
  only just begun to produce.
- **Q4 on live runs** — the machinery is complete and tested, but the live LLM provider
  supplies no scenarios and no evidence maps, so the live posterior always equals the
  prior. There is no live producer feeding it.
- **Semantic contract** — narrow, four input kinds, no dedicated test file.

## 2.3 Missing ❌

Thirteen `raise NotImplementedError` stubs remain (counted 2026-08-12:
`grep -rn "raise NotImplementedError" --include=*.py engine | wc -l`). The ones that matter:

| Stub | What it blocks |
|---|---|
| `stage0.parse_research_text` | **All live ingestion.** Every run starts from hand-prepared input |
| `ledger/lifecycle.py` (×3) | Surveillance → ledger FALSIFIED wiring; the ledger's own activation transition |
| `ledger/wiki/review_queue.enqueue` | D1's human confirmation gate — zero callers, raises |
| `outcomes.calibration_report` / `edge_realization` | The calibration loop |
| `ledger/substrate/queries.valid_over` | Outcome attribution over valid time |
| `ledger/wiki/breadcrumbs` | Card→source provenance map |

And these modules do not exist at all (re-checked 2026-08-12):

- ~~`engine/compression.py`~~ — **now built** (commit 88b700b, 1,084 lines): the
  ThemeCompressionAgent, screen → group → merge → cap → synthesis → gate, with the
  synthesis step behind a `ThemeSynthesizer` seam. See §4.8b for what the shipped merge
  metric does and does not fix.
- `engine/news_critic.py` — external corroboration tagged attention-not-evidence.
- `engine/theme_view.py`, `engine/factor_projection.py`, `engine/theme_book.py` — the
  whole of `PLAN-theme-lifecycle.md` (L1, L5, L4).
- `engine/grounding/emit_gate.py` — harness G6. (`engine/grounding/confidence.py`, harness
  G4, landed 2026-08-12 while this pass was running — see §4.6.)

## 2.4 The skill surface overstates capability

Seventeen skill cards exist; **six are wired**. A card existing under `.claude/skills/`
does not mean it runs. Only membership in `SEAM_TO_SKILLS` (`engine/skills.py`) does, and
that is the source of truth.

**Wired (6):**

| Card | Seams it feeds |
|---|---|
| `iceberg-classifier` | `classify_iceberg`, `parse_research_text` |
| `causal-compiler` | `parse_research_text`, `expand_causal`, `define_axis`, `critique_mental_model` |
| `scenario-pricing-engine` | `define_axis`, `justify_probabilities`, `run_pricing` |
| `system-mapper` | `build_system_map` |
| `trap-detector` | `diagnose_loops`, `critique_mental_model` |
| `macro-regime-classifier` | `macro_context` |

**Not wired (9+):** `evidence-weighting` is pending the Q4 posterior≠prior derivation.
`priced-in-estimator` and `edge-validity` are readable-only. Six are
registered-but-unwired: `macro-state-parser`, `term-premium-estimator`,
`backdoor-identifiability-gate`, `global-io-network`, `factor-r2-router`,
`outcome-calibration-engine`. `multi-source-theme-aggregator` and
`fetch-investor-memos` are card-only — the logic lives elsewhere.

Two of the unwired ones are load-bearing for planned work: `factor-r2-router` is the
whole of lifecycle gap L5, and `outcome-calibration-engine` is the calibration loop.

The staging is deliberate — the constants exist precisely to prevent silent wiring — but
it means the skill directory reads as more capable than the engine is.

**Long-form source specs** for six of these cards live in `docs/*_skill.md`. They are the
derivation, two to five times longer than the compiled card. Nothing imports them; treat
them as reference for *why* a card says what it says.

## 2.5 Known failure modes

Carried forward and re-checked against the current tree. These are the ways this system
goes wrong, ranked by how exposed it is today.

| # | Failure mode | State |
|---|---|---|
| 1 | **Theme explosion** — near-duplicates, no hierarchy, hot topics promoted as core themes | ⚠️ **open, and the largest.** Structural, not a tuning bug. See Part 3.2 |
| 2 | Old reports read as current views | ✅ mitigated by the temporal layer — *provided* `current_date` is supplied |
| 3 | Evidence without reasoning — bullets with no stated mechanism | ⚠️ open. No selection-rationale object binds chosen evidence to a mechanism |
| 4 | Reasoning without evidence — a theme that merely sounds plausible | ⚠️ partly guarded: a theme with no atoms is flagged unpromotable, but nothing enforces "every claim cites evidence" at extraction time |
| 5 | External context missing — confident opinion with no current data | ❌ **unmitigated.** No news critic, no sufficiency gate |
| 6 | Case-memory contamination | 🔒 **best-defended failure mode.** This is what the two-phase firewall exists for |
| 7 | Skill bloat — many cards, few wired | ⚠️ intentional staging, but see 2.4 |
| 8 | No persistence — good output that is never written down | ✅ largely closed. Extraction, aggregation *and* discovery output now round-trip to the wiki |

Failure modes 1, 3, 4 and 5 all point at the same missing stage. A compression pass that
enforces the promotion gate would close 1, 3 and most of 4. A sufficiency gate closes 5.

---

# Part 3 — The two gaps that stand between the engine and its purpose

The stated goal is: a research document goes in, a small number of good, falsifiable
themes come out. Two specified-but-unbuilt pieces stand in the way, and neither is in the
three most recent plans.

## 3.1 There is no entrance

`stage0.parse_research_text` raises `NotImplementedError`, and both providers bypass it.
Real runs begin from a scripted case specification or from injected evidence atoms. This
is the single most important caveat about the whole system: **there is no automatic path
from a document to a theme.**

This is why hardening work on the extraction path has limited reach today: the current
extractor is a regex over markdown and cannot invent much. The exposure arrives with the
parser.

**Specified in** `SURVEILLANCE_BUILD_PLAN.md` §6 (Phase 4). Size: large. Named as the
highest single risk in that plan.

## 3.2 The engine produces too many themes

`docs/THEME_DISCIPLINE_AND_FAILURE_MODES.md` is a whole memo about this, and it is
explicit that the problem is **structural, not a tuning bug**:

- Clustering is a greedy, order-dependent single pass; an item merges only if a *max*
  over six Jaccard overlaps clears 0.5. That bar is high, so near-duplicates survive as
  separate themes.
- The canonical name is the longest existing member. Nothing synthesises a parent.
- There is no parent/subtheme structure and no cap.

You cannot fix it by lowering the threshold — that over-merges unrelated themes. The
missing piece reasons about **mechanism**, not token overlap.

A human analyst wants three to seven parent themes, each carrying subthemes, evidence by
source, a causal mechanism, an observable axis, why it matters, why it might be wrong, a
falsifier, one or two strategy families, and what data is missing.

**Specified in** `THEME_DISCIPLINE_AND_FAILURE_MODES.md` — including ten acceptance tests
that already define "done", and a promotion gate, merge rules, keep-separate rules and
downgrade rules. `SURVEILLANCE_BUILD_PLAN.md` §4 places it in the discovery flow, never
in the scripted expression path the golden master locks.

> **Update 2026-08-12 — the missing piece now exists, but this gap is not closed.**
> `engine/compression.py` shipped (commit 88b700b) and does group by driver rather than by
> tokens. What it has NOT had is a run against a real multi-source batch. §4.8b measured
> the shipped merge metric on labelled *name* pairs only: it fixes every over-merge and
> **none of the four under-merges**, and two true-duplicate pairs still score 0.00 because
> they share no vocabulary. So the fragmentation half of the problem is unfixed and the
> alias vocabulary that would reach it has 5 entries. Read this section as *specified and
> built, not yet demonstrated*.

---

# Part 4 — Open contradictions and pending decisions

These are live. Each needs a decision, not more analysis.

**Live:** 4.2, 4.3, 4.4, 4.6, 4.7, 4.8b.
**Closed since this document was written:** 4.1 and 4.5, moved to **Part 4C** below. Their
original numbers are kept there so existing references still resolve, and the original
reasoning is kept underneath each resolution — you need it to judge whether the resolution
still applies.

## 4.2 🟠 D1's human gate rests on a stub

D1 was corrected on 2026-08-09 to reuse `engine/ledger/wiki/review_queue.py`, described
as *"small, finished, and already does this."* Its only function raises
`NotImplementedError` and has zero callers. A builder following D1 as written would add
an enum member to a function that cannot run.

**Decide:** re-scope D1 to acknowledge that Tier C pulls forward Phase-0/7 work, and
where the queue should live — see 4.3.

**Still open, re-verified 2026-08-12.** `enqueue` still raises and still has no callers:
`grep -rn "review_queue\|enqueue" --include=*.py engine tests` returns exactly one hit,
the definition itself.

## 4.3 🟠 D1 and D5 pull in opposite directions

D5 keeps the provenance ledger separate from the hypothesis ledger, on the stated grounds
that *"two in-flight systems joined together is how both stall."* D1 then routes the
harness's human gate into a module inside that same in-flight substrate. Today
`engine/ledger/` has exactly one outward import and nothing imports inward; D1 would
create the first inbound edge.

**Decide:** together, not separately. If the queue is shared infrastructure it belongs
above both subsystems, not inside one.

**Still open, re-verified 2026-08-12.** Unresolved architectural question; nothing in the
code has moved either way.

## 4.4 ✅ RESOLVED 2026-08-12 — grounding LINTS for now; the caller can choose

**Decision (user, 2026-08-12): lint, not halt — for now.**

D2's *structure* is implemented: `extract_evidence(inp, grounding=None)` takes a policy,
and `GroundingPolicy()` defaults to **strict**, so any NEW caller that says nothing gets
the safe direction. This caller passes `lint` deliberately, and the call site says why.

**Why lint today.** Under strict, a single figure the tokenizer cannot verify aborts the
whole extraction. The tokenizer is demonstrably incomplete — the magnitude/tenor
allow-list fixed `$1.2bn` and `3-5y`, but §4.8b shows the curated alias map has **five**
entries, so coverage of real corpus vocabulary is thin. Halting today would block good
runs on the harness's own gaps rather than on bad evidence, which inverts what the gate
is for.

**Rejected:** leaving it hardcoded (what it was until today). That made a policy choice
unreadable *as* a choice — nobody could see a decision had been taken, which is how it
sat inverted against D2 without anyone noticing.

**The condition for flipping to strict**, and it is a measurement rather than a
judgement: count `EnforcedBundle.warnings` over a real `markdowns/` batch and read a
sample. Flip when rejections are dominated by genuinely absent figures rather than by
tokenizer misses.


**This one is blocked on you, not on more work.** It is the only entry in Part 4 that a
builder should not touch until you say which way it goes.

`extract_evidence` hardcodes lint mode with no caller override. D2 requires the mode be
an explicit caller-supplied parameter defaulting to HALT. Note the ordering constraint:
flipping to strict is unsafe until the number tokenizer stops dropping real figures
(4.5), because strict mode turns a dropped figure into a halt on correct work.

**Still open, re-verified 2026-08-12.** `engine/evidence_extraction.py:270` still reads
`enforce(atoms, index, GroundingPolicy(mode="lint"))`, with no `mode` parameter on
`extract_evidence`. Verify with
`grep -n "GroundingPolicy" engine/evidence_extraction.py`.

**What changed under it:** the ordering constraint that made this unsafe to flip has been
lifted — 4.5 is fixed (Part 4C). So the blocker is now only the decision, not the
tokenizer.

## 4.6 🟡 Invariant I8 cannot fail

Its gate command in `PLAN-authoritative-harness.md:31` greps `engine/grounding.py`,
`engine/confidence.py`, `engine/emit_gate.py` — three paths that do not exist, because the
layout moved to the `engine/grounding/` package. The grep errors, produces no output, and
reads as green. The code is in fact clean; the gate is vacuous. One-line fix.

**Still open, re-verified 2026-08-12 (state at time of writing — this one is moving).** All
three named paths are still absent, so the gate is still vacuous. The package layout is:

- `engine/grounding/__init__.py` — holds `GroundingPolicy`, `SourceIndex`, `enforce`. The
  gate's `engine/grounding.py` was never renamed to this, so the grep misses it.
- `engine/grounding/numbers.py` — the tokenizer. Not named by the gate at all.
- `engine/grounding/confidence.py` — **just landed** (G4). The gate names
  `engine/confidence.py`, which does not exist, so it misses this too.
- `engine/grounding/emit_gate.py` — still not written (G6).

So fixing the gate is **not** a path rename: one of its three targets does not exist yet in
any location, and two exist at different paths than it names. **Point the grep at
`engine/grounding/` as a directory** — it becomes non-vacuous today and stays correct as
G6 lands, with no further edit. Verify the current state with `ls engine/grounding/`; if
that listing has grown since this was written, the directory form is the reason to prefer
it.

## 4.7 Decisions the plans defer to you

Reviewed against the code 2026-08-12. All six are still yours to make — none has been
quietly settled. One has changed shape and is now more urgent than it reads above.

- **Expectation source for surprise scoring** (L2) — consensus from a grounded span,
  the prior print, or a model path. Plan recommends the first, never the last.
  *Still open; nothing built. `engine/theme_view.py` does not exist.*
- **Residual-alpha threshold** (L5) — a risk-appetite call, not a technical one.
  *Still open; `engine/factor_projection.py` does not exist.*
- **Book cadence and recipient** (L4). *Still open; `engine/theme_book.py` does not exist.*
- **Evidence-pack retention** (L3). *Still open; no `EvidencePack` anywhere in `engine/`.*
- **Breach mode** — ship consecutive-only, or expose the decayed-integral variant.
  🔴 **Now a live trap, not just a deferred choice.** `engine/surveillance.py:55` declares
  `breach_mode: Literal["consecutive", "integral"] = "consecutive"`, and that line is the
  **only** occurrence of `breach_mode` in the repo — nothing reads it, and no test covers
  it. So the integral variant is *selectable but inert*: setting `breach_mode="integral"`
  is accepted by the type and silently gives consecutive behaviour. Verify with
  `grep -rn "breach_mode" --include=*.py .` — one hit. Either implement the branch or drop
  the field; a knob that does nothing is worse than an absent one, because it reads as a
  capability. This is exactly the "surface overstates capability" pattern of Part 2.4.
- **Multi-falsifier themes** — the schema assumes one; real theses often have two or
  three. AND or OR, and does any breach terminate or does it take a quorum?
  *Still open, and the two halves of the codebase disagree with each other:*
  `engine/schema/risk.py:39` carries `falsifiers: list[Falsifier]` (plural) while
  `engine/surveillance.py:166` watches a single `falsifier: FalsifierState`. A theme may
  therefore be *authored* with three falsifiers and *surveilled* on one, with no error
  raised and no record of which one was picked.

## 4.8 🟠 REVISIT: the theme distance metric — swapping it trades errors, it does not fix them

**Raised 2026-08-11, with measurements. Needs a decision after the compression work lands.**

`_overlap` in `engine/theme_aggregation.py` is the **overlap coefficient**
(`|A∩B| / min(|A|,|B|)`), not Jaccard — `THEME_DISCIPLINE_AND_FAILURE_MODES.md` said
Jaccard and was wrong. The obvious fix is to swap in Jaccard. **Measured, that is not a
clean win.** Both metrics on the same eight pairs, threshold 0.5:

| A | B | coef | jac | should |
|---|---|---|---|---|
| growth | rates not pricing growth | **1.00** merge | 0.33 sep | **separate** |
| growth | china growth slowdown | **1.00** merge | 0.33 sep | **separate** |
| funding stress | funding | **1.00** merge | **0.50** merge | **separate** |
| european bank spreads | japanese bank spreads | **0.67** merge | **0.50** merge | **separate** |
| hyperscaler bond basis | hyperscaler project bond basis risk premium | 1.00 merge | 0.50 merge | merge ✓ |
| ai capex funding | ai capex credit supply | 0.67 merge ✓ | **0.40 sep** | **merge** |
| ai capex debt funded buildout | hyperscaler issuance surge | **0.00 sep** | **0.00 sep** | **merge** |
| rates not pricing growth | market underpricing recovery | **0.00 sep** | **0.00 sep** | **merge** |

**What this shows.**

1. Jaccard fixes the two `growth` containment blowups and breaks a correct merge
   (`ai capex funding` / `ai capex credit supply` drops to 0.40 and separates). It trades
   one error class for another.
2. **Both metrics fail identically on the last two rows — score 0.00.** Two descriptions
   of the same theme sharing no vocabulary are invisible to any token-counting function.
   That is the fragmentation half of the problem, and **no threshold and no choice of
   set-similarity metric reaches it.**
3. Rows 3 and 4 are wrong under *both*. `funding stress`/`funding` is a parent/child
   relation being scored as equality — the hierarchy the engine lacks. `european`/
   `japanese` differ by exactly the token the metric discards.

**So the real question to revisit is not which metric.** It is whether merge should be a
lexical decision at all, or a *mechanism* decision — same driver, same transmission, same
outcome — with tokens demoted to a cheap pre-filter for recall. Rows 6–8 are only
separable that way. Rows 3–4 need a parent/subtheme relation, which `ThemeCluster` does
not model.

**Do not re-tune the threshold and call it fixed.** Re-run the table above against
whatever is in place after the compression work; if rows 7 and 8 still score 0.00, the
metric change was cosmetic.

### 4.8b — VERIFIED 2026-08-12, after the weighted-Jaccard change. Half fixed.

Re-ran the table against the shipped metric (weighted Jaccard, threshold 0.55,
alias anchors ×3), scoring **names only**:

| pair | old coef | new score | want | result |
|---|---|---|---|---|
| growth / rates not pricing growth | 1.00 | **0.25** | separate | **fixed** |
| growth / china growth slowdown | 1.00 | **0.33** | separate | **fixed** |
| funding stress / funding | 1.00 | **0.50** | separate | **fixed** |
| european / japanese bank spreads | 0.67 | **0.50** | separate | **fixed** (+ guard) |
| hyperscaler bond basis / …risk premium | 1.00 | 0.50 | merge | still separates |
| ai capex funding / ai capex credit supply | 0.67 | 0.40 | merge | still separates |
| ai capex debt funded buildout / hyperscaler issuance surge | 0.00 | **0.00** | merge | still separates |
| rates not pricing growth / market underpricing recovery | 0.00 | **0.00** | merge | still separates |

**All four over-merges are fixed. None of the four under-merges are fixed by the metric.**
That is the expected result, not a regression — a symmetric set function cannot see that
two disjoint vocabularies mean the same thing. Rows 5–8 are now handled by three other
mechanisms instead, and the caveat has moved with them:

1. **Curated aliases** (`alias_map`, anchors weighted ×3). This works — it lifts the one
   labelled merge pair from 0.33 to 0.60. But **there are 5 aliases**, 1 discriminator
   group and 3 distinct pairs. Coverage of the synonym space is therefore ~nil today, and
   the metric's own test docstring concedes the vocabulary "is hand-curated and will
   always be incomplete".
2. **The other five dimensions.** `_similarity` takes the max over tokens, concepts,
   entities, market_vars, axes and causal. The table above scores NAMES only; real items
   carry evidence-derived tokens, and rows 5–6 would likely merge on a shared axis or
   market variable. **This is untested against a real corpus** — the labelled set is names.
3. **Pass 2, mechanism match.** The only mechanism that can reach rows 7–8 in principle.

**What is actually still open**, and it is narrower than 4.8 first stated: not "which
metric", but **whether alias coverage and pass 2 carry the synonym cases on real
documents**. The threshold was tuned on 13 labelled *name* pairs whose only non-trivial
merge case is alias-anchored. Before trusting this, run the aggregator over a real
multi-source batch from `markdowns/` and count how many true duplicates survive as
separate clusters. If the number is high, the answer is more aliases or a stronger pass 2
— not a lower threshold, which would re-break rows 1–4.

---

# Part 4C — Closed since this document was written

Entries that were live in Part 4 and are now settled. **They keep their original numbers**
so older references still resolve, and **the original text is kept underneath each
resolution** — a resolution you cannot see the reasoning for is a resolution you cannot
tell has gone stale.

## 4.1 ✅ RESOLVED 2026-08-12 — the activation rule; the ontology was right

**Resolution.** The ONTOLOGY wins and the code was the regression. `abs()` is restored:
`engine/ledger/runner.py:107` now reads

```
active = sv.B >= ACTIVATION_BREADTH_MIN and abs(sv.S) >= ACTIVATION_ABS_SCORE_MIN
```

Recorded as `ONTOLOGY_DELTA` **D-09**, which names commit **e4b6740** ("orch task 1.5",
2026-08-10) as the regression that dropped the absolute value *and*, in the same commit,
added a test asserting the wrong behaviour — so the regression was self-ratifying. The
restoring commit is **86086ac**. The test was renamed
`test_negative_score_with_required_breadth_activates_as_contested`. No ONTOLOGY edit was
needed; it was already right.

**Verify in one command:** `grep -n "abs(sv.S)" engine/ledger/runner.py` — one hit.

This is a fixed bug, not a decision that could be revisited: it followed the sign-audit
precedent, established which side was right, and closed the divergence. Note the line
number moved from 84 to 107; grep for the expression, not the line.

**Original entry, kept for the reasoning:**

> `ONTOLOGY.md` defines activation twice — §Lifecycle and §Constants — as
> `B ≥ 2 ∧ |S| ≥ 2`. The absolute value is load-bearing: a contested theme is meant to go
> ACTIVE precisely so that it gets watched.
>
> Wave 1 removed the absolute value from `engine/ledger/runner.py:84`, treating it as a
> sign-blindness bug. No `ONTOLOGY_DELTA` entry was recorded, which §Constants requires.
> `engine/ledger/lifecycle.py` and `docs/ledger/PLAN_TRACKER.md` still state the rule with
> the absolute value, so the code is now the outlier, not the documents.
>
> **Decide:** either the ontology is right and the change is a regression to revert, or
> the ontology is wrong and needs an amendment plus a recorded delta. The sign audit is
> the precedent for how to settle it. *Under-claiming is free; a silent divergence is not.*

## 4.5 ✅ RESOLVED 2026-08-12 — the number tokenizer no longer deletes real figures

**Resolution.** Fixed as diagnosed: the boundary guard stays strict on the left edge and
stops deleting on the right, via a magnitude/tenor allow-list in
`engine/grounding/numbers.py`. Commit **473d095** ("grounding: stop the boundary guard
deleting magnitudes and tenors"). This was a bug fix, not a decision, so there is no delta
entry.

**Verify in one command:**

```
python -c "from engine.grounding.numbers import numbers_in; print([n.raw for s in ['\$1.2bn','\$1.1tn','\$440bn','500mn','250k','10y','5y','12m','3Q'] for n in numbers_in(s)])"
```

Expected: all nine tokens returned, each with a unit (`usd_bn`, `usd_tn`, `mn`, `k`, `y`,
`m`, `q`). Measured 2026-08-12: all nine present.

**One thing the fix did not address, and it is not the reported bug.** The left-edge guard
still lets a bare year through from inside a date: `numbers_in('2022-12-28')` returns
`2022` as an unbounded, unitless number, and `numbers_in('Q1 2022')` likewise returns
`2022`. The original entry listed `2022-12-28` as a phantom the guard *exists to block*.
It blocks the `12` and the `28`, not the year. Whether a year is a real figure or a
phantom is a judgement call — treat this as a note for whoever next touches the guard, not
as a reopening of 4.5.

**Original entry, kept for the reasoning:**

> Measured: any figure followed by a suffix the tokenizer does not recognise returns
> nothing at all — `$1.1tn`, `$440bn`, `500mn`, `250k`, and also the tenor and period
> forms `10y`, `5y`, `12m`, `3Q`. A sentence whose only figure is unreadable is discarded
> before it can become evidence (7 sentences in one credit research note, 0 in another —
> it is document-dependent).
>
> The diagnosis is clean and the fix is narrow. Every phantom number the guard exists to
> block (`Q1`, `2022-12-28`) is a **left-edge** violation. Every real figure it destroys
> is a **right-edge** violation. The guard can stay strict on the left and stop deleting
> on the right.
>
> Full detail in `reviews/2026_08_10_grounding_harness_review.md` (CR-BUG-001).

---

# Part 5 — Recommended build order, and why

The plans do not agree on what comes next, because they were written at different times
against different bottlenecks. Reconciled against the stated goal:

**Step 1 — ✅ tokenizer done; ⏳ the grounding default is now waiting on you.** The
tokenizer half shipped 2026-08-12 (Part 4C/4.5), which removes the reason strict mode was
unsafe. Inverting the default to HALT is a one-parameter change gated on your call in 4.4.

**Step 2 — Finish harness G4 (computed confidence).** The extractor currently attaches
three author-picked confidence constants. G4 replaces them with a number computed from
what the harness actually observed: span found, numbers verified, source reliability,
independence, freshness. The model's own confidence becomes a **cap** — it can lower,
never raise. Self-contained, deterministic, lands in two existing files plus one new one.

**Step 3 — Build ingestion (Phase 4) behind the harness.** The surveillance plan
sequenced this last so a failure could be localised to parsing rather than reasoning.
That reason has expired — the spine is green and demonstrable end-to-end. And the harness
now exists precisely to catch what a generative parser gets wrong. These two belong
together: ingestion is the moment the system first becomes capable of inventing, and G1,
G2 and G4 are the net under it.

**Step 4 — ✅ theme compression built** (`engine/compression.py`, commit 88b700b). It turns
a flat list of near-duplicates into three to seven parent themes with subthemes, and it
sits in the discovery flow, not the scripted expression path. **The remaining work is
validation, not construction:** §4.8b says the shipped merge metric fixes all four
over-merges and none of the four under-merges, and that the alias vocabulary covers
almost nothing. Run the aggregator over a real multi-source batch from `markdowns/` and
count surviving duplicates before trusting it.

**Step 5 — Then the lifecycle plan** (L1 ThemeView first; everything else reads it).
It is a reader's layer over work that must exist first, and it depends on harness Phase 3.

Steps 1 and 4 have landed. **Step 3 (ingestion) is now the substantial work, and it is the
one that changes what the engine can actually do** — it is still the only reason there is
no automatic path from a document to a theme (Part 3.1).

---

# Part 6 — Hardening the process

The discipline this project needs is already written down; it stopped being followed when
work was delegated.

Wave 1 ran four agents in parallel across separate worktrees. None of them was given
`ONTOLOGY.md`. One changed a rule that document defines twice, and recorded nothing. That
is not an agent failure — it is a briefing failure, and it is repeatable.

Three changes, in order of how much they actually bite.

**1. Make the specification executable.** A test that asserts the activation condition in
`runner.py` matches the constant and the rule in `ONTOLOGY.md`. This is the one that
works, because it fails loudly and does not depend on anyone remembering anything. The
repo already has the pattern: `test_theme_family_hint_typing.py` asserts the routable
family set equals exactly what the router can emit, and
`test_view_matches_python_definition` pins the SQL view to the Python math. Extend it to
the rules that currently live only in prose.

**2. Hand every delegated task its governing document.** An orch task description is the
entire agent prompt. If the ontology is not in it, the agent has not read it. This is
cheap and it is why wave 1 went wrong.

**3. Make unimplemented surface visible.** Twelve stubs are honest individually and
invisible collectively — you cannot tell built from planned without opening every file.
That is the exact mechanism by which a binding decision came to rest on a stub (4.2). A
generated inventory, checked by a test, closes it.

And one rule worth restating because two reviews have now had to invoke it:

> **When code and specification disagree, find out which is right before changing
> either.** The sign audit did this and closed the contradiction. Wave 1 did not, and
> opened one.

---

## Where to read next

| You want | Open |
|---|---|
| What a theme *is*, formally | `docs/ledger/ONTOLOGY.md` |
| The state machine that watches a live theme | `SURVEILLANCE_BUILD_PLAN.md` §5 |
| The anti-hallucination contract | `PLAN-authoritative-harness.md` |
| The shared typed state and stage order | `docs/theme_object_contract.md` |
| Why there are too many themes, and the fix | `docs/THEME_DISCIPLINE_AND_FAILURE_MODES.md` |
| Component-by-component status | Part 2 of this document |
| The reader-facing artifacts still to build | `PLAN-theme-lifecycle.md` |
| Current code-level findings | `reviews/2026_08_10_grounding_harness_review.md`, `reviews/2026_08_10_architecture_review.md` |

---

*Epistemic engine. Discovery stops at ranked strategy families. Expression remains
downstream and fenced. No trades are emitted.*
