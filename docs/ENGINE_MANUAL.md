# Investment Research Engine Manual

> **Status of this document.** Written 2026-06-13 by inspecting code and tests directly
> (not the older audit reports). Every status claim below is grounded in source files and the
> test suite. Where something could not be verified from code, it says **Not verified.**
> Test baseline at writing: **723 tests collected, 722 passed, 1 xfailed** (`python3 -m pytest tests/ -q`).
>
> **Status tags used throughout:** ✅ implemented · ⚠️ partial · 🚧 contract_only / planned ·
> ❌ missing · 🔒 firewall/gate. Finer code-level labels: `implemented`, `partial`,
> `contract_only` (schema + registry entry, but `run()` raises `NotImplementedError`),
> `method_card_only`, `schema_only`, `registered_unwired`, `planned`, `deprecated`, `unknown`.

---

## 1. Executive summary

This is a **live discovery / research engine, not a trade engine.** It converts research input
into a *falsifiable thematic hypothesis* and a *ranked set of strategy families* with decomposed
confidence — and then it **STOPS**. It does not produce legs, sizes, hedge ratios, or execution.

**Product boundary (discovery mode):**

```
idea / report / batch of sources
  → source classification          (method | case | mixed | ignore)
  → evidence extraction            (typed evidence atoms + axes + falsifiers)
  → temporal classification        (current vs historical vs expired)
  → theme aggregation              (dedup into source-attributed clusters)
  → causal object / axes / families
  → confidence / missing data
  → STOP  (status = strategy_family_routed, or a blocked HALT)
```

- **Discovery mode must not emit exact trades, sizing, hedge ratios, or execution.** This is
  enforced by construction (semantic-contract gate + no-trade guards), not by convention.
- **Expression mode** (scenario pricing → fair value → scored expressions → sizing) is a
  *separate, downstream, fenced* path. It runs only on the deterministic `ScriptedProvider` for
  golden cases; the live LLM provider is structurally rejected in expression mode.
- The system is designed around **persistent wiki memory**, a **method/case firewall**, and
  **theme-to-strategy-family routing**.

**The single most important caveat:** end-to-end *automatic* ingestion of a raw research document
does **not** exist. The free-text→typed-stream parser (`engine/stage0.parse_research_text`) is a
`NotImplementedError` stub, and both providers bypass it. Real runs start from **pre-structured
inputs**: a scripted `CaseSpec` (golden cases) or injected `current_input_axes`/evidence atoms
(live discovery). See §3 and §4.

---

## 2. Design principles

1. **Raw sources are immutable.** `raw/` and `markdowns/` are never modified by the engine.
2. **Wiki memory is compiled and persistent.** `wiki/` is the generated/maintained memory layer
   over the immutable raw sources, written by the WikiIntegrator.
3. **METHOD memory teaches *how to reason*.** Concepts, causal mechanisms, how-to-reason cards
   compiled (paraphrased) from books/papers. Timeless. Phase-A readable.
4. **CASE memory records *what a source or past theme said*.** Past themes, scenarios, closed
   theses, source-specific market claims. Time-bound.
5. **Archived CASE memory is blocked during Phase A fresh reasoning.** A fail-closed retriever
   refuses case/missing/invalid pages in Phase A (§14).
6. **Current-input CASE evidence may be used during the current run** — but *only* when explicitly
   supplied as current input (the current-input seam, §4, §11).
7. **Fresh reasoning is frozen before Phase B.** A SHA-256 `FrozenSnapshot` is taken before any
   historical analogue / case page is read; the frozen object is never mutated.
8. **Discovery stops at strategy families.** No legs, no sizing in discovery mode.
9. **Probabilities are not invented.** `q`/`p` are derived only from supplied scenarios and
   supplied evidence; with no evidence the posterior equals the prior.
10. **Trades are not emitted in discovery.** Enforced by the semantic contract + no-trade guards.

---

## 3. Architecture diagram

```
raw sources (immutable: raw/, markdowns/)
        │
        ▼
  SourceIntakeAgent                  ✅ implemented (deterministic keyword classifier)
        │   → SourceClassification (method|case|mixed|ignore)
        ▼
  EvidenceExtractionAgent            ✅ implemented (deterministic regex/lexicon v1)
        │   → EvidenceExtractionBundle (atoms, axes, falsifiers, family hints)
        ▼
  TemporalContextAgent               ✅ implemented (no-wall-clock classifier)
        │   → TemporalContext (current/historical/expired; phase-A admissibility)
        ▼
  MultiSourceThemeAggregatorAgent    ✅ implemented (deterministic lexical v1)
        │   → MultiSourceThemeSet (deduped ThemeClusters + source attributions)
        ▼
  WikiIntegratorAgent                ✅ implemented (plan → apply, idempotent)
        │   → wiki/ pages (sources, evidence, themes, clusters, concepts, entities,
        │                  index.md, log.md, memory-map.md)
        ▼
  DiscoveryRunnerAgent               🚧 contract_only AS AN AGENT
        │   (the registered agent.run() raises NotImplementedError;
        │    the actual discovery pipeline exists as engine.workflow.run_workflow)
        ▼
  ThemeObject / ranked StrategyFamilyRec[]   ✅ implemented (workflow.run_workflow)
        │   status = strategy_family_routed   (or blocked HALT)
        ▼
  Outcome memory                     ⚠️ partial (JSONL store ✅; calibration ❌ NotImplementedError)
```

**Two important gaps visible in the diagram:**

- The arrow from raw sources into `SourceIntakeAgent` is **not automated by an LLM parser** — there
  is no live free-text ingestion (`parse_research_text` is a stub). Inputs are hand-built or
  injected.
- `DiscoveryRunnerAgent` is **contract_only as an agent**: there is no registry-driven
  "load a source slug → feed the current-input seam → run discovery" wrapper. The discovery
  capability is real but is invoked directly via `engine.workflow.run_workflow` /
  `engine.provider_select`.

There is also a parallel "expression" path (`engine.runner.run_case` over a `ScriptedProvider`) used
by the golden master — that path produces `expression_complete` ThemeObjects with pricing/sizing and
is intentionally fenced from the live LLM provider.

---

## 4. Current component inventory

| Component | File(s) | Status | What it does | Inputs | Outputs | Tests | Gaps |
|---|---|---|---|---|---|---|---|
| **SourceIntakeAgent** | `engine/wiki_agents.py` | ✅ `implemented` | Deterministic keyword classifier → access_class (method/case/mixed/ignore), per-page classes, ingestion policy | `SourceIntakeInput` (slug, type, pages) | `SourceClassification` | `tests/unit/test_wiki_agents.py` | Pure keyword heuristics; no semantic understanding; decks w/o page manifest only warn |
| **EvidenceExtractionAgent** | `engine/evidence_extraction.py` (+ agent wrapper) | ✅ `implemented` (rule-based) | CASE markdown → `EvidenceExtractionBundle` (atoms, causal claims, axes, confounders, falsifiers, family hints, themes); refuses non-case sources | `EvidenceExtractionInput` | `EvidenceExtractionBundle` | `tests/integration/test_evidence_extraction.py`, `test_jpm_evidence_atoms.py`, `test_evidence_temporal_integration.py` | Regex/lexicon, visibly tuned to AI-credit/JPM; **falsifiers are templated synthesis, not source-derived**; no LLM paraphrase |
| **TemporalContext / TemporalContextAgent** | `engine/temporal.py` (+ wrapper) | ✅ `implemented` | No-wall-clock classifier: source age/role, expired/active horizons, per-claim phase-A admissibility | `TemporalContextInput` (+ caller `current_date`) | `TemporalContextOutput` | `tests/unit/test_temporal_schema.py`, `test_horizon_extraction.py`, `tests/integration/test_temporal_agent.py` | Forecast detection is regex; **`current_date` must be supplied or context is silently skipped (warning only)** |
| **MultiSourceThemeAggregatorAgent** | `engine/theme_aggregation.py` (+ wrapper) | ✅ `implemented` (lexical v1) | Dedups theme candidates across current-input bundles → ranked `MultiSourceThemeSet`; enforces access/temporal firewall; computes corroboration/attention/divergence | `MultiSourceThemeAggregatorInput` | `MultiSourceThemeSet` | `tests/unit/test_theme_aggregation*.py`, `test_theme_aggregator_agent.py` | **Token/alias Jaccard only (no embeddings); greedy single-pass; canonical name = longest raw member; no hierarchy; no cap** — see §15 |
| **WikiIntegratorAgent** | `engine/wiki_integration.py` (+ wrapper) | ✅ `implemented` | Plan→apply wiki persistence: source/evidence/theme/cluster/concept/entity pages + index/log/memory-map; no-trade + ≥25-word copyright guards; idempotent | `WikiIntegratorInput` | `WikiUpdatePlan` / `WikiIntegrationResult` | `tests/unit/test_wiki_integrator.py` | Hardcoded `_CREATED/_UPDATED="2026-06-12"`; per-line copyright guard only |
| **WikiLintAgent** | `engine/wiki_agents.py` (contract) + `engine/wiki_validators.py` (library) | 🚧 `contract_only` (agent) / ✅ validator library | The *agent* `run()` raises `NotImplementedError`. The lint capability exists as a 14-check read-only validator library; orchestration is a **human/Claude workflow** (CLAUDE.md "Workflow 3"), not engine code | — | `ValidationReport` | `tests/unit/test_wiki_validators.py` | No agent wiring; batching/scratch/log is manual |
| **DiscoveryRunnerAgent** | `engine/wiki_agents.py` (contract) vs `engine/workflow.py`, `engine/runner.py`, `engine/provider_select.py` | 🚧 `contract_only` (agent) / ✅ pipeline | Registered agent `run()` raises `NotImplementedError`. Actual discovery = `workflow.run_workflow(mode="discovery")`: idea→drivers→mandatory causal object→firewall-gated Q4→falsifier-gated routing→STOP | `Provider` + `PolicyConfig` | `(ThemeObject, memo)` | `tests/integration/test_workflow.py`, `test_golden_master.py`, `test_discovery_firewall.py`, `test_french_banks.py` | The *agent wrapper* (slug→seam→run) is unbuilt; call `run_workflow` directly |
| **Q4 probability engine** | `engine/probability.py`, `engine/probability_evidence.py` | ✅ `implemented` (provenance layer) | Validate/tilt/justify/quality over **supplied** p_s (softmax tilt toward prior); map supplied evidence→scenarios; produce audited posterior. **Posterior is audit-only — pricing still reads `Scenario.p_s`** | scenarios + evidence atoms/maps | `ProbabilitySetJustification` / `ProbabilityUpdateAudit` | `tests/unit/test_probability.py`, `test_posterior_update.py`, `tests/integration/test_probability_wiring.py` | Never invents p_s or scenarios; tilt is heuristic softmax, not calibrated likelihood ratios |
| **current-input evidence seam** | `engine/protocols.py` (`RunContext`), consumed in `engine/workflow.py` | ✅ `implemented` | Only current-input evidence is mapped to scenarios; archived CASE stays firewall-refused; empty ⇒ posterior==prior | `RunContext` | mapped scenarios / posterior audit | `tests/unit/test_runcontext_current_input.py`, `tests/integration/test_current_input_consumption.py`, `test_evidence_seam_end_to_end.py` | Case-evidence detection is a **slug-marker heuristic** (`_CASE_SLUG_MARKERS`), flagged MVP; live LLM path supplies no maps (always posterior==prior) |
| **semantic contract** | `engine/semantic_contract.py` | ✅ `implemented` (narrow) | Economic-sanity gate before snapshot: per-input-kind axis/family expectations + always-on trade/expression-leakage fail-closed | ThemeObject + input_kind | `list[str]` violations | **No dedicated test file found — appears untested directly** | Only 4 enumerated input kinds (jpm_report/curve_steepener/etf_flow/margin_compression); unknown kind → violation |
| **memory firewall** | `engine/memory.py` (`MemoryRetriever`) | ✅ `implemented` 🔒 | Phase-gated fail-closed retriever: Phase A returns only method pages, refuses case/missing/invalid (returns None, logs); `mark_frozen` before Phase B; one-way `advance_to_phase_b` | `dict[slug, WikiPage]`, phase | gated pages | `tests/unit/test_memory_firewall.py` | In-memory only; access_class derivation heuristic for malformed pages |
| **discovery/expression firewall** | `engine/firewall.py` | ✅ `implemented` 🔒 | Two-phase runner: Phase A discovery → `freeze()` to immutable SHA-256 snapshot → publish hash → Phase B additive `PostCaseCalibration` only | provider, policy, pages | `FirewalledResult` | `tests/integration/test_discovery_firewall.py`, `test_posterior_firewall_and_output.py` | `default_calibrator` is a **reference impl that makes NO actual confidence change** (`adjusted=fresh`) |
| **skills registry** | `engine/skills.py` | ✅ `implemented` | Loads METHOD cards; `SEAM_TO_SKILLS` maps 10 seams → cards (fail-closed); tracks pending/readable/registered-unwired | `.claude/skills/*/SKILL.md` | loaded cards | `tests/integration/test_skills*.py`, `test_method_cards_*.py` | Only `LLMProvider` injects cards; many cards method-context-only and unwired (§8) |
| **outcome memory / calibration** | `engine/outcomes.py` | ⚠️ `partial` | `ThemeOutcomeRecord` + JSONL `append_outcome`/`read_outcomes` work. `calibration_report` and `edge_realization` **raise NotImplementedError** | records | JSONL store | `tests/unit/test_outcomes.py` (asserts stubs raise) | **No realized-outcome corpus**; calibration unimplemented by design |
| **Thesis Tracker** | `engine/thesis_tracker.py`, `engine/schema/thesis_tracker.py`, `db/migrations/0001_thesis_tracker.sql` | ✅ `implemented` (sidecar) | SQLite store + stateless service: upsert/get/list/close, audit log, computed view, JSON/MD export, `create_thesis_stub_from_theme` (invents nothing priceable) | `ThesisTrackerRecord`/`MarketDataRecord` + db_path | computed records / exports | `tests/unit/test_thesis_tracker_*.py` | Deliberately does NOT touch discovery/firewall; never infers prices/probabilities |
| **GDELT News Critic** | — | ❌ `missing` | — | — | — | — | No `gdelt`/news-critic code anywhere in `engine/` or `tests/`. Not planned in code |
| **Context Sufficiency / Humility Gate** | — | ❌ `missing` | — | — | — | — | No `sufficiency`/`humility`/`context_sufficiency` symbol. Nearest analogues: `discovery._data_confidence` floor 0.5, confidence ceilings in `select_strategy_families` |
| **Provider selection** | `engine/provider_select.py`, `engine/llm_provider.py`, `engine/scripted_provider.py` | ✅ `implemented` | `select_discovery_provider("scripted"|"llm")`; live LLM fails closed unless `ALLOW_LIVE_LLM_DISCOVERY=1`; LLM is **discovery-only** (no scenarios/expressions) | provider name / case | `Provider` | `tests/integration/test_provider_selection.py`, `test_live_discovery_harness.py` | LLM path generates no scenarios/probabilities (live Q4 posterior==prior); expression is scripted-only |

**Registry enumeration (source of truth, `engine/wiki_agents.py`).** `REGISTRY.list_agents()` returns
8 agents. Five override `run()` (implemented): `SourceIntakeAgent`, `EvidenceExtractionAgent`,
`TemporalContextAgent`, `MultiSourceThemeAggregatorAgent`, `WikiIntegratorAgent`. Three inherit the
base `run()` that raises `NotImplementedError` (contract_only): `SkillCompilerAgent`,
`WikiLintAgent`, `DiscoveryRunnerAgent`.

---

## 5. Source lifecycle

How a source *should* move through the system:

```
PDF / markdown (immutable in raw/, markdowns/)
  → source classification     → SourceClassification.access_class
  → temporal role             → TemporalContext.temporal_role
  → evidence atoms            → EvidenceExtractionBundle.evidence_atoms
  → themes                    → core_theme_candidates (per source)
  → theme clusters            → ThemeCluster[] (across sources)
  → wiki persistence          → wiki/ pages
  → discovery                 → ranked strategy families
```

**Source types (`access_class`):**

| Type | Meaning | Phase-A usable? |
|---|---|---|
| `method` | How-to-reason / timeless mechanism (books, papers) | ✅ yes (method memory) |
| `case` | Source-specific market claims, past themes, reports | 🔒 only if supplied as current input |
| `mixed` | Both method and case content | 🔒 conservatively treated as case / fail-closed in aggregation |
| `ignore` | Not useful as memory | n/a |

**Temporal roles (`TemporalRole`, `engine/temporal.py`):**

- `current_report` — a recent source usable as current market evidence.
- `historical_case` — time-bound; an analogue/outcome candidate, **never** a current signal.
- `stale_case` — older case material, superseded.
- `outcome_candidate` — contains an expired forecast that should be *scored*, not acted on.
- `method_source` — timeless mechanism; the only role admissible as Phase-A method context.
- `unknown` — could not classify (often because `current_date` was not supplied).

**Current-input exception (critical):** a CASE source can be used in Phase A **only** if it is
explicitly supplied as the current input for this run (via the current-input evidence seam,
`RunContext.current_input_*`). Archived case pages remain firewall-refused. This is what lets a
*fresh* report inform reasoning without re-opening the whole case archive.

---

## 6. Memory model

| Path | Stores | Written by |
|---|---|---|
| `raw/` | Original PDFs + page-aware normalized markdown (private, gitignored where copyrighted) | source compiler (`tools/`), human |
| `raw/normalized-md/`, `raw/manifests/` | Normalized markdown + page manifests | source compiler (**Not verified** these exact subpaths exist on disk; the compiler in `tools/` targets normalized-md) |
| `markdowns/` | Immutable raw source corpus (the books/papers/decks) | human (never the engine) |
| `wiki/sources/` | One durable summary page per ingested source (`access_class`-stamped) | WikiIntegratorAgent |
| `wiki/evidence/` | Atomic evidence pages (CASE), one per evidence atom | WikiIntegratorAgent |
| `wiki/themes/` | Per-source theme memory cards (CASE) | WikiIntegratorAgent |
| `wiki/theme-clusters/` | Deduped cross-source theme clusters (CASE) | WikiIntegratorAgent |
| `wiki/concepts/` | Concept pages (mechanics; access_class mirrors source) | WikiIntegratorAgent (Part 7) |
| `wiki/entities/` | Entity pages (issuers, indices, sectors) | WikiIntegratorAgent (Part 7) |
| `wiki/index.md` | Content-oriented index of every created page (wikilinks) | WikiIntegratorAgent (Part 8) |
| `wiki/log.md` | Append-only ingest log (one entry per integration) | WikiIntegratorAgent (Part 8) |
| `wiki/memory-map.md` | Current-state map (active themes, missing-evidence/axis/falsifier sets) | WikiIntegratorAgent (Part 8) |
| `.claude/skills/` | METHOD process cards compiled (paraphrased) from books/papers | human + `tools/extract_method_skills.py` skeletons |

**Method/case firewall (the core memory discipline):** every wiki page declares
`access_class: method | case`. Phase-A fresh reasoning loads METHOD pages only; the
`MemoryRetriever` is fail-closed and refuses CASE/missing/invalid pages until *after* the fresh
reasoning is frozen. Then Phase B may read CASE pages for analogue/calibration only, writing to an
*additive* block that references the snapshot hash. See §14.

---

## 7. Agent registry

For each *registered* agent (`engine/wiki_agents.py`). "Status" is the agent's `run()`.

### SourceIntakeAgent
- **Purpose:** Classify a source into method/case/mixed/ignore + per-page classes + ingestion policy.
- **Status:** ✅ `implemented` (deterministic keyword classifier).
- **Reads / Writes:** reads source metadata; writes nothing (pure function).
- **Inputs / Outputs:** `SourceIntakeInput` → `SourceClassification`.
- **Firewalls:** sets `access_class` — the *first* firewall gate.
- **Non-goals:** semantic understanding; LLM classification.
- **Limitations:** keyword signatures only; decks without a page manifest only warn.
- **Tests:** `tests/unit/test_wiki_agents.py`.

### EvidenceExtractionAgent
- **Purpose:** Turn CASE markdown into a structured `EvidenceExtractionBundle`.
- **Status:** ✅ `implemented` (rule/lexicon-based, deterministic).
- **Reads / Writes:** reads source markdown; writes nothing (the WikiIntegrator persists later).
- **Inputs / Outputs:** `EvidenceExtractionInput` → `EvidenceExtractionBundle`.
- **Firewalls:** refuses non-case sources; emits no trades/scenarios/probabilities.
- **Non-goals:** scenario generation, probabilities, trades.
- **Limitations:** regex/lexicon tuned to AI-credit/JPM; **falsifiers are templated**, not
  source-derived; no LLM paraphrase yet.
- **Tests:** `tests/integration/test_evidence_extraction.py`, `test_jpm_evidence_atoms.py`.

### TemporalContextAgent
- **Purpose:** Classify source age/role + forecast horizons + per-claim Phase-A admissibility.
- **Status:** ✅ `implemented` (no wall clock; `current_date` is caller-supplied).
- **Inputs / Outputs:** `TemporalContextInput` → `TemporalContextOutput`.
- **Firewalls:** 🔒 only a `method_rule` claim may be `method_context`; expired forecast forces
  `current_update_required=True`.
- **Limitations:** forecast detection is regex; if `current_date` is absent, context is skipped
  with a warning (a silent-ish degradation to watch).
- **Tests:** `tests/unit/test_temporal_schema.py`, `tests/integration/test_temporal_agent.py`.

### MultiSourceThemeAggregatorAgent
- **Purpose:** Dedup theme candidates across current-input sources into ranked clusters.
- **Status:** ✅ `implemented` (deterministic lexical v1).
- **Inputs / Outputs:** `MultiSourceThemeAggregatorInput` → `MultiSourceThemeSet`.
- **Firewalls:** 🔒 archived CASE dropped; METHOD = taxonomy only; all-historical clusters cannot
  `promote_to_discovery`.
- **Non-goals:** trades; embeddings; hierarchy.
- **Limitations:** **this is the locus of the theme-explosion problem (§15, §16).** Token/alias
  Jaccard similarity, greedy single-pass clustering, raw-member canonical naming, no parent/subtheme
  structure, no cap on clusters.
- **Tests:** `tests/unit/test_theme_aggregation*.py`, `test_theme_aggregator_agent.py`.

### WikiIntegratorAgent
- **Purpose:** Persist extraction/aggregation output into wiki pages, idempotently.
- **Status:** ✅ `implemented`.
- **Reads / Writes:** reads existing pages (for idempotent append); writes `wiki/` pages.
- **Inputs / Outputs:** `WikiIntegratorInput` → `WikiUpdatePlan` / `WikiIntegrationResult`.
- **Firewalls:** 🔒 no-trade regex guard; ≥25-word copyright-run guard; `access_class` stamped and
  never upgraded; method source produces no CASE evidence/theme pages.
- **Limitations:** deterministic dates are hardcoded constants; copyright guard is per-line.
- **Tests:** `tests/unit/test_wiki_integrator.py` (+ new `test_wiki_validators.py`).

### WikiLintAgent
- **Purpose (intended):** Lint the wiki for internal consistency.
- **Status:** 🚧 `contract_only` — `run()` raises `NotImplementedError`. **The capability exists**
  as the read-only validator library `engine/wiki_validators.py` (14 checks + `validate_all`), and
  as the human/Claude "Workflow 3: Lint" in CLAUDE.md. They are simply not wired into the agent.
- **Tests:** `tests/unit/test_wiki_validators.py` (library), not the agent.

### DiscoveryRunnerAgent
- **Purpose (intended):** Registry-driven discovery run (load source → seam → run).
- **Status:** 🚧 `contract_only` — `run()` raises `NotImplementedError`. **The discovery pipeline
  exists** as `engine.workflow.run_workflow` / `engine.provider_select`; only the agent wrapper is
  missing.
- **Tests (of the pipeline):** `tests/integration/test_workflow.py`, `test_golden_master.py`,
  `test_discovery_firewall.py`, `test_french_banks.py`.

### SkillCompilerAgent
- **Purpose (intended):** Compile method skill cards from sources.
- **Status:** 🚧 `contract_only` — `run()` raises `NotImplementedError`. Skeleton tooling exists in
  `tools/extract_method_skills.py` (TODO-bearing skeletons); the actual compilation is currently a
  human/Claude task.

---

## 8. Skills registry

**Source of truth: `engine/skills.py`.** A skill *card* existing under `.claude/skills/` does **not**
mean it is wired. Only cards present in `SEAM_TO_SKILLS` feed a live engine seam.

`SEAM_TO_SKILLS` (seam → cards):

```
classify_iceberg      → [iceberg-classifier]
parse_research_text   → [iceberg-classifier, causal-compiler]   (NB: the seam itself is a stub)
expand_causal         → [causal-compiler]
define_axis           → [causal-compiler, scenario-pricing-engine]
build_system_map      → [system-mapper]
diagnose_loops        → [trap-detector]
critique_mental_model → [causal-compiler, trap-detector]
justify_probabilities → [scenario-pricing-engine]
run_pricing           → [scenario-pricing-engine]
macro_context         → [macro-regime-classifier]
```

Registry constants:
- `PENDING_WIRING_SKILLS = ("evidence-weighting",)`
- `READABLE_DISCOVERY_SKILLS = ("priced-in-estimator", "edge-validity")`
- `REGISTERED_UNWIRED_SKILLS = ("macro-state-parser", "term-premium-estimator",
  "backdoor-identifiability-gate", "global-io-network", "factor-r2-router",
  "outcome-calibration-engine")`

| Skill | Card path | access_class | Wired seam(s) | Status | Teaches | Tests | Gaps |
|---|---|---|---|---|---|---|---|
| iceberg-classifier | `.claude/skills/iceberg-classifier/` | method | classify_iceberg, parse_research_text | ✅ `wired` | Iceberg layers → hot_topic/core_theme_candidate/key_event | test_skills, test_iceberg_classifier, test_iceberg_wiring | Card frontmatter lists 4 seams; only 2 in dict |
| causal-compiler | …/causal-compiler/ | method | parse_research_text, expand_causal, define_axis, critique_mental_model | ✅ `wired` | Build a valid causal chain; causal asymmetry ≠ constant conjunction | test_skills, test_method_cards_3/4 | — |
| scenario-pricing-engine | …/scenario-pricing-engine/ | method | define_axis, justify_probabilities, run_pricing | ✅ `wired` | Max-entropy q, scenario FV, residual edge | test_skills, test_method_cards_4 | — |
| system-mapper | …/system-mapper/ | method | build_system_map | ✅ `wired` | Stocks/flows, feedback loops, transmission | test_skills, test_method_cards_3/4 | — |
| trap-detector | …/trap-detector/ | method | diagnose_loops, critique_mental_model | ✅ `wired` | Archetype traps; Ellenberg bias supplement | test_skills, test_skills_batch2, test_method_cards_4 | — |
| macro-regime-classifier | …/macro-regime-classifier/ | method | macro_context | ✅ `wired` | Cross-asset regimes; bear/base/bull framing | test_skills, test_method_cards_3, test_macro_context | README "pending" note is **stale** — it IS wired |
| evidence-weighting | …/evidence-weighting/ | method | none | 🚧 `pending_wiring` | Base-rate + likelihood-ratio updating | test_skills_batch2 | Pending Q4 posterior≠prior; must not feed ConfidenceComponents |
| priced-in-estimator | …/priced-in-estimator/ | method | none | 🚧 `readable_discovery` | Separate valuation level from risk premium | test_skills_batch2, test_method_cards_4 | Read-only; must not change golden master |
| edge-validity | …/edge-validity/ | method | none | 🚧 `readable_discovery` | In/out-of-sample, overfitting checklist | test_skills_batch2, test_method_cards_4 | Read-only |
| macro-state-parser | …/macro-state-parser/ | method | none | 🚧 `registered_unwired` | Regime+factor state (HMM/DFM) | test_method_cards_4 | Intended `macro_context` not wired |
| term-premium-estimator | …/term-premium-estimator/ | method | none | 🚧 `registered_unwired` | Term premium ≠ level | test_method_cards_4 | Intended `define_axis` not wired |
| backdoor-identifiability-gate | …/backdoor-identifiability-gate/ | method | none | 🚧 `registered_unwired` | Backdoor identification gate | test_method_cards_4 | Intended `expand_causal` not wired |
| global-io-network | …/global-io-network/ | method | none | 🚧 `registered_unwired` | I/O network, Leontief propagation | test_method_cards_4 | Intended `build_system_map` not wired |
| factor-r2-router | …/factor-r2-router/ | method | none | 🚧 `registered_unwired` | Purity ρ² family routing | test_method_cards_4 | Intended `select_strategy_families` not wired |
| outcome-calibration-engine | …/outcome-calibration-engine/ | method | none | 🚧 `registered_unwired` | Strictly-proper scoring (Gneiting) for q calibration | test_method_cards_4 | Intended `justify_probabilities` not wired |
| multi-source-theme-aggregator | …/multi-source-theme-aggregator/ | method | none (card slug absent from skills.py) | 🚧 `card-only` | Cluster themes across sources w/ source attribution | test_theme_aggregator_agent, test_theme_aggregation* (test the **engine code**, not the card) | Card not in any `skills.py` constant; logic lives in `theme_aggregation.py` |
| fetch-investor-memos | …/fetch-investor-memos/ | n/a (acquisition skill, not a method card) | none | 🚧 `card-only` | Investor name/URL → download memos → STOP | test_fetch_investor_memos | Different frontmatter schema; absent from `skills.py` |

**The named skills the manual was asked to cover — EXISTS / MISSING:**

- ✅ Iceberg Classifier — **wired**
- ✅ Causal Compiler — **wired**
- ✅ System Mapper — **wired**
- ✅ Trap Detector — **wired**
- ✅ Scenario Pricing Engine — **wired**
- ✅ Macro Regime Classifier — **wired**
- ❌ "Theme Evidence & Selection Rationale" — **MISSING** (no card by this name; closest are
  `evidence-weighting` + `multi-source-theme-aggregator`)
- ⚠️ Multi-Source Theme Aggregator — exists as a card but **card-only / unwired**; the logic lives
  in `engine/theme_aggregation.py`
- ❌ "Outcome-Weighted Theme Memory" — **MISSING** by that name (closest is the unwired
  `outcome-calibration-engine`, a probability-calibration card)
- ❌ GDELT News Critic — **MISSING** entirely
- ❌ "Context Sufficiency & Humility Gate" — **MISSING** entirely
- 🚧 Backdoor Identifiability Gate — exists, `registered_unwired`
- 🚧 Factor-R2 Router — exists, `registered_unwired`
- ❌ "ETF Flow / Index Technical Router" — **MISSING** (TAARSS/ETF-flow material was treated as
  CASE/ingestion, not compiled into a skill card)

**Bottom line:** present only the **6 wired cards** as live engine seams. Of the requested named
list, 6 are wired, 2 exist-but-unwired (backdoor-identifiability-gate, factor-r2-router), 1 is
card-only (multi-source-theme-aggregator), and 5 are outright **missing**.

---

## 9. Core workflow: single source

Example — a 2019 **European Equity Strategy** PDF:

1. **SourceIntakeAgent** should classify it as a **CASE report** (`access_class: case`) — it is
   source-specific market commentary, not timeless method.
2. **TemporalContextAgent** should mark it **`historical_case` / outcome_candidate** — it is from
   2019, well past most of its forecast horizons (given a 2026 `current_date`).
3. **EvidenceExtractionAgent** extracts evidence atoms and operational axes (e.g. "Europe vs US
   valuation gap", "rates catch-up to growth"), plus confounders and (templated) falsifiers.
4. It must **not** be treated as current market advice — its forecasts are phrased *"as of
   15 March 2019, the source argued…"*, never *"the market is…"*.
5. It must **not** produce trades. The WikiIntegrator's no-trade guard blocks any page that leaks
   trade/sizing language.

This is the canonical example of **temporal discipline**: the same content is admissible as a
*historical analogue / outcome candidate* but inadmissible as a *current signal*.

---

## 10. Core workflow: multi-source batch

```
N current-input source bundles (EvidenceExtractionBundle[])
  → MultiSourceThemeAggregator
  → deduplicated ThemeClusters
  → source attributions (which source said what, is it current input?)
  → corroboration score (independent current sources agreeing)
  → attention score (how "hot"/widely-discussed)
  → evidence-attention divergence (corroboration − attention; the p−q proxy)
  → promoted clusters (promote_to_discovery) or watchlist
  → discovery handoff
```

**The goal is not "more themes."** It is **fewer, better, source-connected themes.** The current
aggregator does not yet achieve this (§15, §16): it is a deterministic lexical clusterer that tends
to leave near-duplicates separate and has no human-analyst compression pass.

The `evidence_attention_divergence` is the engine's pre-screen on latent edge: *high factual
support + low attention = high latent edge* (a proxy for `p − q`). Promotion additionally requires
current support, sufficient temporal quality, and a routable operational axis.

---

## 11. Q4 probability workflow

```
scenarios (SUPPLIED) + priors (SUPPLIED) + current-input evidence atoms
  → evidence-to-scenario mapping        (probability_evidence.map_evidence_to_scenarios)
  → posterior update                    (bounded move from prior; audit-only)
  → probability quality                 (caps for single-source / single-cluster)
  → confidence metadata                 (feeds StrategyFamilyRec.confidence_components)
```

**What it does NOT do (by design):**
- Scenarios are **not generated** unless supplied (the LLM provider's `propose_scenarios` returns `[]`).
- Probabilities are **not invented** — no evidence ⇒ posterior **equals** prior.
- `q` (priced-in, max-entropy) is kept **separate** from `p` (subjective).
- Fair value and expression mode are **downstream** and fenced.

**Consequence for live runs:** because `LLMProvider` supplies no scenarios and no evidence maps,
the live Q4 posterior is *always* equal to the prior today. The evidence→posterior machinery is
fully implemented and tested, but it has no live producer of scenarios feeding it. The golden master
is unaffected precisely because the posterior is audit-only (pricing reads `Scenario.p_s`).

---

## 12. Temporal workflow

Why temporal context matters: an old source's *time-bound forecast* must never be rendered as a
*current view*. The 2019 European Equity report's call should read:

> "As of 15 March 2019, the source argued global growth recovery was partly priced in equities but
> not fully priced in rates."

not:

> "The market is mispricing rates vs growth."

The temporal layer distinguishes:
- **expired forecasts** — past their horizon → become **outcome candidates** to *score*, and force
  `current_update_required = True`.
- **outcome candidates** — expired forecasts worth a realized-vs-predicted check (the calibration
  loop, currently ❌ unimplemented in `outcomes.py`).
- **still-relevant mechanisms** — the timeless causal mechanism inside a dated source may survive as
  method context even when the dated call does not.
- **`current_update_required`** — a flag that the source's view cannot be used as current without a
  refresh.

---

## 13. Output objects

| Object | File | What it is | Creates | Consumes | Gaps |
|---|---|---|---|---|---|
| **SourceClassification** | `engine/wiki_agents.py` | Intake verdict: access_class + per-page classes + ingestion policy | SourceIntakeAgent | aggregator `_eligibility`, temporal | No validators; `ingestion_policy` not enforced against `access_class` |
| **EvidenceAtom** | `engine/schema/probability.py` | Source-backed, unmapped fact (claim + provenance + entities/concepts/numbers) | `extract_evidence`, `from_record` | `map_evidence_to_scenarios`, temporal, aggregator | `freshness` overloaded; `claim_type` loose free-string parallel to typed `claim_kind`; source_slug optional |
| **EvidenceExtractionBundle** | `engine/evidence_extraction.py` | Full per-CASE-source extraction product | `extract_evidence` | aggregator, temporal, WikiIntegrator | `scenario_candidates`/`source_page_fields` untyped dicts; `no_trade_confirmation` defaults empty |
| **TemporalContext** | `engine/temporal.py` | Source-level temporal picture | `classify_temporal_context` | aggregator, embedded in bundle | Date parsing best-effort (silent None on bad ISO) |
| **ForecastHorizon** | `engine/temporal.py` | One dated claim + whether horizon is live | `_make_horizon` | TemporalContext, bundle | `outcome_variable` = first 6 words of claim (crude); no link to outcome record |
| **TemporalClaimStatus** | `engine/temporal.py` | Temporal class of ONE claim + Phase-A admissibility | `classify_temporal_context` | bundle | Keyword-lexicon driven (brittle) |
| **CandidateTheme** | `engine/schema/streams.py` | Stage-0 narrative stream + p−q pre-screen | Stage-0 parse (stubbed) | iceberg classifier | Largely superseded by `ThemeCluster` in multi-source path (two parallel theme reps) |
| **ThemeCluster** | `engine/schema/theme_aggregation.py` | One deduped theme: members + attributions + scores + status | `_build_cluster` | `MultiSourceThemeSet`, discovery handoff | Scores heuristic; `strategy_family_hints` free strings (not the routable Literal); **no parent/child** |
| **MultiSourceThemeSet** | `engine/schema/theme_aggregation.py` | The aggregator's batch deliverable | `aggregate_theme_candidates` | discovery, WikiIntegrator | `rejected_merges`/`duplicate_theme_map` untyped |
| **ThemeObject** | `engine/schema/theme.py` | Frozen, append-only pipeline output (discovery + optional expression) | `workflow._run_discovery` / `_run_expression` | firewall `freeze`, memo render, PM gate | Large optional surface; `macro_context` hint recorded but not wired to confidence |
| **StrategyFamilyRec** | `engine/schema/strategy_family.py` | One ranked strategy family + decomposed confidence | `discovery.select_strategy_families` | ThemeObject, firewall, memo | `direction` free string; `probability_*` optional on legacy path |
| **ProbabilityUpdateAudit** | `engine/schema/probability.py` | Deterministic audit of a scenario-prob update (prior/posterior/maps/method/quality) | `update_probabilities_from_evidence` | `ProbabilitySetJustification`, `StrategyFamilyRec.probability_update_audit_hash` | None notable — strongly invariant-enforced |
| **ThemeMemoryRecord** | — | ❌ **NOT FOUND.** Closest: `ThesisTrackerRecord` (SQLite sidecar) + a wiki-markdown "ThemeMemoryCard" artifact (not a model) | — | — | Name does not exist as a model |
| **ThemeOutcomeRecord** | `engine/outcomes.py` | `@dataclass` (not pydantic): p/q/X_s/market value/realized axis for a closed thesis | callers + `append_outcome` (JSONL) | `read_outcomes`; `calibration_report`/`edge_realization` (❌ stubs) | No realized corpus; not validated; not wired into discovery |
| **ContextSufficiencyReport** | — | ❌ **MISSING** (grep returns zero hits). Nearest analogues: `MacroContext.missing_data`, `ConfidenceComponents.data_confidence`, `bundle.extraction_warnings` | — | — | Does not exist |

**Strategy-family allowed values** (`StrategyFamilyRec.family`, test-enforced exact set, 12 values):
`steepener, flattener, long_short, outright, cash_cds_basis, credit_vs_equity, credit_vs_rates,
volatility_convexity, watchlist_only, etf_basket_rv, capital_structure, index_index_rv`.
`etf_basket_rv`/`capital_structure`/`index_index_rv` route as relative-value sub-types.
**Wiki-taxonomy-only (no routing rule):** `curve`, `sector_rotation`.

**ThemeObject status lifecycle** (`engine/schema/theme.py`): `blocked` → `discovery_complete` →
`strategy_family_routed` (default; discovery STOP) → `expression_complete` (expression mode only).
Phase A ends at `strategy_family_routed`; neither phase produces `expression_complete` in discovery.

---

## 14. Firewalls and gates

1. **🔒 Discovery/expression firewall** (`engine/firewall.py` + `engine/workflow.py`): a causal
   object is mandatory; with none, discovery emits a `blocked` record rather than fabricating a path
   to a trade. Expression mode (legs/pricing/sizing) never runs on the live LLM provider — the
   provider lacks `enumerate_expressions`/`size_and_risk` and `run_workflow` rejects it.
2. **🔒 Method/case memory firewall** (`engine/memory.py`): Phase A serves METHOD pages only and is
   fail-closed (refuses case/missing/invalid, returns `None`, logs the refused slug). Freeze → SHA-256
   snapshot → Phase B may read CASE pages for additive calibration only.
3. **🔒 Temporal firewall** (`engine/temporal.py`): only a `method_rule` claim may be
   `method_context`; an expired forecast forces `current_update_required`. Historical sources cannot
   be rendered as current.
4. **🔒 Semantic contract** (`engine/semantic_contract.py`): before any snapshot, checks the
   discovery output for economically-wrong axes and trade-leg/sizing/expression leakage; **fail
   closed** on violation. (Caveat: narrow — only 4 input kinds; no dedicated test file found.)
5. **🔒 Context sufficiency gate** — ❌ **does not exist as a named component.** The closest live
   behavior is `discovery._data_confidence` (a 0.5 floor) and the confidence ceilings in
   `select_strategy_families` (no scenarios → ≤0.45; no market value → ≤0.60). There is no humility
   gate that refuses to opine on thin context.
6. **🔒 Outcome memory phase-B gate**: archived outcome memory is case memory — readable only after
   the freeze. (The calibration *analytics* that would consume it are ❌ unimplemented.)

**Examples of blocked behavior (what the firewalls prevent):**
- Old case conclusion used as method memory → refused by the fail-closed retriever in Phase A.
- Historical forecast rendered as current → temporal layer phrases it "as of <date>" and sets
  `current_update_required`.
- Discovery output includes sizing → semantic-contract expression-leakage check fails closed.
- No scenario set but `p_s` invented → probability invariants force posterior == prior (R2/R3).
- News coverage treated as truth → **not currently guarded** (no news critic exists).
- Archived outcome memory read before snapshot → memory firewall refuses it pre-freeze.

---

## 15. Known failure modes

### Failure mode 1 — Theme explosion ⚠️ (the biggest current problem)

**Symptom:** the system produces too many themes — near-duplicates, no parent/subtheme hierarchy,
weak cross-source attribution, hot topics promoted as core themes, no human-style compression.

**Why it happens (grounded in `engine/theme_aggregation.py`):**
- **EvidenceExtractionAgent is source-local** — each source's themes are extracted independently;
  there is no global view at extraction time.
- **The theme lexicon can over-trigger** — `core_theme_candidates` are derived from keyword/lexicon
  signals tuned to the worked example.
- **The aggregator is a deterministic lexical v1.** Clustering (`_cluster_items`) is a **greedy,
  order-dependent single pass**: each item joins the *best* existing cluster only if
  `_similarity ≥ min_similarity_to_merge` (default **0.5**). `_similarity` is the **max** over six
  Jaccard overlaps (tokens, concepts, entities, market_vars, axes, causal). A 0.5 max-overlap bar is
  *high*, so two phrasings of the same theme that don't share ≥50% of tokens on any single dimension
  stay **separate** → near-duplicate clusters.
- **Canonical naming is raw-member based**: `canonical = max(members, key=(len(evidence_ids),
  len(name)))` — it picks the longest raw member name, it does not *synthesize* a parent theme name.
- **No parent-theme / subtheme structure** — clusters are flat. There is no "Main Development →
  Parent Theme → Subtheme" hierarchy in the schema.
- **No cap on the number of parent themes per batch** — the aggregator emits as many clusters as the
  greedy pass produces.
- **No explicit "human analyst compression pass"** — nothing merges related clusters into a small
  set of parent themes after the lexical pass.

**Fix direction (see §16 and §17):** add a Theme Compression / Human-Analyst-Synthesis stage that
(a) caps parent themes per batch, (b) requires each promoted theme to carry evidence + causal
mechanism + axis + temporal status + falsifier, (c) merges themes sharing driver/outcome/axis/family,
(d) keeps subthemes *under* parents, and (e) downgrades attention-only themes to hot-topic/watchlist.

### Failure mode 2 — Old reports read like current views ⚠️
A historical source's time-bound forecast presented as a current signal. **Mitigation exists** in
the temporal layer (§12) but depends on the caller supplying `current_date` (otherwise temporal
context is silently skipped) and on the downstream renderer honoring `temporal_role`. The lint
validators (`check_historical_cases_not_current`) catch un-disclaimed historical pages.

### Failure mode 3 — Evidence without reasoning ⚠️
A theme has evidence bullets but no explanation of *why it was selected*. The theme card has a
"Why this theme was picked" section, but extraction populates it weakly (it often restates the theme
name). There is no "selection rationale" object that ties chosen evidence to a stated mechanism.

### Failure mode 4 — Reasoning without evidence ⚠️
A theme selected because it *sounds* plausible, with weak evidence. Partial guard: a theme with no
evidence atoms is flagged "unpromotable", and clusters cannot `promote_to_discovery` without current
support. But there is no strong "every factual claim cites evidence" enforcement at extraction time
(the lint validator `check_theme_pages_cite_evidence` only checks *persisted* pages).

### Failure mode 5 — External context missing ⚠️/❌
The model opines confidently without current data/news. There is **no news critic** and **no context
sufficiency gate** (both ❌ missing). The only brakes are the data-confidence floor and the
no-scenario/no-market-value confidence ceilings. This is a real, unmitigated gap.

### Failure mode 6 — Case memory contamination 🔒 (well-guarded)
Old case conclusions leaking into Phase A. This is the firewall's *raison d'être* and is the
best-defended failure mode: fail-closed retriever + freeze + post-freeze case reads (§14).

### Failure mode 7 — Skill bloat ⚠️
Many cards, few wired. 17 skill directories exist; only **6 are wired** to seams. The rest are
pending/readable/registered-unwired/card-only (§8). Discoverability outruns integration. This is
*intentional* staging (the constants exist to prevent silent wiring), but it means the skill surface
overstates live capability unless read carefully.

### Failure mode 8 — No persistence ⚠️ (now largely closed)
Outputs correct in memory but never written to wiki. The WikiIntegratorAgent (§4, §7) closes this
for the extraction/aggregation half — but the **discovery output** (`ThemeObject` / ranked families)
has **no persistence path into the wiki**; there is no integrator that writes a routed ThemeObject
back as a durable theme page. That round-trip is still open.

---

## 16. Theme discipline: how a human analyst should think

A human analyst does **not** want 40 themes. A human analyst wants **3 to 7 parent themes**, each
with: supporting subthemes, evidence by source, a causal mechanism, an observable axis, why it
matters, why it might be wrong, what would confirm/invalidate it, which strategy family it maps to,
and what data is missing.

**Hierarchy (target):**

```
Main Development
  → Parent Theme
      → Subtheme
          → Evidence Cluster
              → Operational Axis
                  → Strategy Family
```

**Rules:**

1. Theme *candidates* are not themes.
2. Evidence *facts* are not themes.
3. *Hot topics* are not themes.
4. A theme must answer **"what economic mechanism is changing?"**
5. A theme must connect *multiple facts* into one coherent claim.
6. A theme must have an *observable axis* or be explicitly *watchlist*.
7. A theme must have a *falsifier*.
8. If two themes share driver, mechanism, outcome, and axis → **merge**.
9. If two themes share a driver but differ in axis/outcome → make them **subthemes** of one parent.
10. If a theme appears across *independent* sources → raise **corroboration**.
11. If a theme appears everywhere but with weak evidence → raise **attention**, not conviction.
12. If a theme is historical → it is an **outcome candidate / analogue**, not a current signal.
13. A theme should route to **one or two** primary strategy families, not all possible families.
14. Each batch should produce a short **"human analyst synthesis"** before discovery.

**Example.**

*Bad (theme explosion — 7 flat themes):*
- Europe rich vs fair value
- Europe underweight vs US
- bond yields not priced
- cyclicals vs defensives
- banks vs bond proxies
- F&B downgrade
- consumer durables downgrade

*Better (1 parent + 4 subthemes):*

> **Parent theme:** "DB 2019 argued global growth recovery was partly priced in equities but not
> fully priced in rates."
>
> **Subthemes:**
> 1. Europe vs US valuation gap
> 2. Rates catch-up to growth recovery
> 3. Sector rotation into cyclicals/banks and away from bond proxies
> 4. Defensive/luxury downgrades as source-stated sector expressions
>
> **Status:** Historical case / outcome candidate — *not* a current market view.

---

## 17. Proposed Theme Compression Agent 🚧 (PROPOSED — not implemented)

A new stage between aggregation and discovery.

**`ThemeCompressionAgent` (proposed).**

- **Input:** `MultiSourceThemeSet`, `EvidenceExtractionBundle[]`, `TemporalContext[]`,
  `ThemeEvidenceSupport[]` (a selection-rationale object — also proposed).
- **Output:** `AnalystThemeMap` (proposed schema):
  - `parent_themes` (capped count)
  - `subthemes` (grouped under parents)
  - `source_coverage_matrix` (theme × source)
  - `evidence_clusters`
  - `rejected_or_merged_themes`
  - `watchlist_items`
  - `hot_topics_not_promoted`
  - `human_readout` (the short synthesis)
- **Rules:** cap parent themes per batch; require evidence + falsifier + axis for promotion; keep
  subthemes but do not promote all of them; produce an explicit *"why these themes, why not the
  others."*

Mark clearly in any roadmap: **this stage does not exist today.** The current aggregator stops at
flat `ThemeCluster`s.

---

## 18. Current roadmap

Ranked by leverage on the current gaps. (Status reflects code as of 2026-06-13.)

| # | Build | State today | Why next | Unlocks | Acceptance tests | Do NOT include |
|---|---|---|---|---|---|---|
| 1 | **ThemeCompressionAgent / AnalystThemeMap** | 🚧 planned | Directly fixes the #1 failure mode (theme explosion) | Human-grade theme maps; parent/subtheme hierarchy; capped output | parent-theme cap honored; every promoted theme has evidence+axis+falsifier; merge rules unit-tested; "why not" populated | trades, sizing, embeddings-as-truth |
| 2 | **Theme Selection-Rationale object** (`ThemeEvidenceSupport`) | 🚧 planned | Closes failure modes 3 & 4 | Evidence↔mechanism binding; auditable "why selected" | every promoted theme cites ≥1 evidence atom + a stated mechanism | inventing evidence |
| 3 | **DiscoveryRunnerAgent wiring** | 🚧 contract_only | The pipeline exists; only the agent wrapper is missing | One-call registry-driven discovery from a source slug | agent loads slug → seam → returns routed ThemeObject; golden master unchanged | new numerics |
| 4 | **WikiLintAgent wiring** | 🚧 contract_only (library ✅) | Validators exist; orchestration doesn't | Automated health-checks; the xfail log-format bug becomes a real check | agent runs the 14 validators in batches; reconciles log/index/memory-map | deleting contradictions |
| 5 | **Discovery-output persistence** (ThemeObject → wiki) | ❌ missing | Closes failure mode 8 for the discovery half | Durable routed-theme pages; outcome tracking input | routed ThemeObject written as a CASE theme page w/ families + confidence | legs/sizing in the page |
| 6 | **TemporalContextAgent completion** (outcome-candidate linkage) | ⚠️ partial | Makes expired forecasts feed calibration | Closed-thesis corpus seeds | expired forecast → `ThemeOutcomeRecord` stub created | wall-clock dates |
| 7 | **Outcome memory / calibration** (`calibration_report`, `edge_realization`) | ❌ NotImplementedError | Needs a closed-thesis corpus first (depends on #5/#6) | q-calibration; edge realization regression | given a corpus, report reliability diagram + edge stats | inventing realized outcomes |
| 8 | **Context Sufficiency / Humility Gate** | ❌ missing | Closes failure mode 5 | Refuse-to-opine on thin context | gate blocks routing below a context-sufficiency floor; emits `blocked` | hard-coded thresholds w/o tests |
| 9 | **GDELT News Critic** | ❌ missing | Closes the "news as truth" gap | External corroboration / contradiction signal | news coverage tagged attention-not-evidence; never raises conviction alone | treating coverage as fact |
| 10 | **Skill wiring** (evidence-weighting → Q4; factor-r2 → routing) | 🚧 pending/registered_unwired | Cards exist; seams don't consume them | Bayesian Q4; purity-based routing | wiring changes confidence *only* via documented derivations; golden master gated | silent golden-master drift |

---

## 19. How to use this manual with ChatGPT / Claude

When feeding this manual to another model, **also include:**
- the **current status report** (run `python3 -m pytest tests/ -q` and paste the summary),
- **one example source output** (a real `wiki/sources/*.md` + its `wiki/themes/*.md`),
- **one failure case** (e.g. a batch that produced too many near-duplicate themes),
- the **desired next build** (e.g. "design the ThemeCompressionAgent").

Tell the model explicitly:
- **Do not assume planned features exist.** Trust this manual's status tags over the README.
- **Preserve the firewalls** (method/case, discovery/expression, temporal) — they are enforced by
  construction; do not propose changes that bypass them.
- **Keep discovery separate from trade execution.** No legs/sizing/hedge ratios in discovery output.
- **Focus on theme compression and memory persistence** — the two highest-leverage gaps.

---

## 20. Appendix: test commands and key files

**Test commands:**
```bash
python3 -m pytest tests/ -q                              # full suite (≈723 tests)
python3 -m pytest tests/integration/test_golden_master.py -q   # the locked numerics (do not change)
python3 -m pytest tests/unit/test_wiki_integrator.py tests/unit/test_wiki_validators.py -q
python3 -m pytest tests/integration/test_discovery_firewall.py -q
```

**Key directories:**
- `engine/` — the pipeline · `engine/schema/` — typed models · `.claude/skills/` — method cards ·
  `wiki/` — curated memory · `cases/` — scripted fixtures · `markdowns/`/`raw/` — immutable sources ·
  `tests/` — unit + integration · `tools/` — source/skill compilers · `db/` — thesis-tracker SQLite.

**Key schema files:**
- `engine/schema/theme.py` (ThemeObject), `strategy_family.py` (families + confidence),
  `probability.py` (EvidenceAtom, ProbabilityUpdateAudit), `theme_aggregation.py` (ThemeCluster,
  MultiSourceThemeSet), `streams.py` (Stage-0 streams), `wiki_integration.py`,
  `thesis_tracker.py`; plus `engine/temporal.py`, `engine/evidence_extraction.py`,
  `engine/outcomes.py`.

**Key skill cards (wired):** `iceberg-classifier`, `causal-compiler`, `scenario-pricing-engine`,
`system-mapper`, `trap-detector`, `macro-regime-classifier`.

**Key workflow files:** `engine/workflow.py` (run_workflow), `engine/discovery.py` (family routing),
`engine/firewall.py` (two-phase), `engine/memory.py` (retriever), `engine/provider_select.py`,
`engine/semantic_contract.py`, `engine/wiki_integration.py` + `engine/wiki_validators.py`.

---

*Epistemic engine. Discovery stops at ranked strategy families. Expression remains downstream and
fenced. No trades are emitted in discovery.*
