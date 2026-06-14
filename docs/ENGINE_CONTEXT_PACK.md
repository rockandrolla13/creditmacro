# Engine Context Pack

> A compact, paste-into-ChatGPT/Claude briefing for the investment-research engine.
> Companion to `docs/ENGINE_MANUAL.md` (full detail) and
> `docs/THEME_DISCIPLINE_AND_FAILURE_MODES.md` (the theme problem).
> Written 2026-06-13 from code/tests. Status tags: ✅ implemented · ⚠️ partial ·
> 🚧 contract_only/planned · ❌ missing · 🔒 firewall/gate. **Do not assume planned features exist.**

## 1. System summary (one paragraph)

This is a **live discovery / research engine, not a trade engine**. It ingests research, classifies
sources, extracts typed evidence, judges temporal validity, aggregates themes across sources into
deduplicated clusters, persists everything to a markdown **wiki memory**, then routes a falsifiable
causal object to a **ranked set of strategy families with decomposed confidence — and STOPS**. It
never emits legs, sizes, hedge ratios, or execution in discovery mode. It is built around three
firewalls (method/case memory, discovery/expression, temporal) and a wiki that is the agent's
persistent memory. The engine's reasoning is mostly **deterministic rule/lexicon code today**, with
live LLM calls only on the *discovery* generative seams.

## 2. Product boundary

```
idea / report / batch of sources
  → source classification (method|case|mixed|ignore)
  → evidence extraction (typed atoms + axes + falsifiers)
  → temporal classification (current vs historical vs expired)
  → theme aggregation (dedup → source-attributed clusters)
  → causal object / axes / strategy families + confidence / missing data
  → STOP   (status = strategy_family_routed, or a blocked HALT)
```

**Discovery must not emit trades/sizing/hedge ratios/execution.** Expression mode (scenario pricing
→ fair value → scored expressions → sizing) is **separate, downstream, and fenced** — it runs only
on the deterministic scripted provider for golden cases, never on the live LLM provider.

**Biggest honesty caveat:** there is **no live free-text ingestion**. The raw-document parser
(`stage0.parse_research_text`) is a `NotImplementedError` stub; both providers bypass it. Runs start
from pre-structured inputs (a scripted `CaseSpec`, or injected `current_input_axes`/evidence atoms).

## 3. Currently implemented components ✅

- **SourceIntakeAgent** — deterministic keyword classifier → `SourceClassification`.
- **EvidenceExtractionAgent** — CASE markdown → `EvidenceExtractionBundle` (atoms, causal claims,
  axes, confounders, **templated** falsifiers, family hints). Regex/lexicon, tuned to AI-credit/JPM.
- **TemporalContextAgent** — no-wall-clock classifier (source role, expired/active horizons,
  per-claim Phase-A admissibility). Needs caller-supplied `current_date`.
- **MultiSourceThemeAggregatorAgent** — deterministic lexical clustering → `MultiSourceThemeSet`
  (corroboration / attention / evidence-attention divergence). *This is where theme explosion lives.*
- **WikiIntegratorAgent** — plan→apply wiki persistence (sources, evidence, themes, clusters,
  concepts, entities, index/log/memory-map). No-trade + ≥25-word copyright guards; idempotent.
- **Q4 probability engine** — validates/tilts **supplied** p_s; maps supplied evidence→scenarios;
  audited posterior. **Posterior is audit-only** (pricing reads `Scenario.p_s`), so golden master is
  unchanged; with no evidence, posterior == prior.
- **Current-input evidence seam** — only current-input evidence reaches scenarios; archived CASE
  stays firewall-refused.
- **Memory firewall** (fail-closed Phase-A retriever) 🔒, **Discovery/expression firewall**
  (freeze → SHA-256 snapshot → additive Phase-B) 🔒, **Temporal firewall** 🔒.
- **Semantic contract** — economic-sanity + leakage gate (narrow: 4 input kinds; no dedicated test).
- **Skills registry** — loads method cards; `SEAM_TO_SKILLS` wires 6 cards to seams.
- **Thesis Tracker** — standalone SQLite sidecar (upsert/close/export; invents nothing priceable).
- **Provider selection** — scripted (default) vs live LLM (discovery-only; fails closed unless
  `ALLOW_LIVE_LLM_DISCOVERY=1`).

**Test baseline:** 723 collected, 722 passed, 1 xfailed (a known validator/log-format mismatch).

## 4. Not-implemented / partial / missing components

- 🚧 **DiscoveryRunnerAgent** — *contract_only* (agent `run()` raises `NotImplementedError`); the
  discovery pipeline itself exists as `engine.workflow.run_workflow`.
- 🚧 **WikiLintAgent** — *contract_only*; lint capability exists as the read-only validator library
  `engine/wiki_validators.py` (14 checks) + the human/Claude "Workflow 3" in CLAUDE.md.
- 🚧 **SkillCompilerAgent** — *contract_only*; skeleton tooling only.
- ⚠️ **Outcome memory / calibration** — JSONL store ✅, but `calibration_report` and
  `edge_realization` **raise NotImplementedError** (need a closed-thesis corpus).
- ❌ **Live free-text ingestion** (`parse_research_text` is a stub).
- ❌ **Discovery-output persistence** — no path writes a routed `ThemeObject` back to the wiki.
- ❌ **ThemeCompressionAgent / AnalystThemeMap** — the human-analyst synthesis stage does not exist.
- ❌ **Context Sufficiency / Humility Gate** — no such component.
- ❌ **GDELT News Critic** — does not exist.
- ❌ **ThemeMemoryRecord / ContextSufficiencyReport** objects — do not exist.

## 5. Skill list (source of truth: `engine/skills.py`)

**Wired to live seams (6):** `iceberg-classifier`, `causal-compiler`, `scenario-pricing-engine`,
`system-mapper`, `trap-detector`, `macro-regime-classifier`.

**Registered but NOT wired (9):**
- pending: `evidence-weighting` (awaiting Q4 posterior≠prior derivation)
- readable-only: `priced-in-estimator`, `edge-validity`
- registered_unwired: `macro-state-parser`, `term-premium-estimator`,
  `backdoor-identifiability-gate`, `global-io-network`, `factor-r2-router`,
  `outcome-calibration-engine`

**Card-only (logic lives elsewhere or different schema):** `multi-source-theme-aggregator`,
`fetch-investor-memos`.

**Outright missing** (named in older plans, no card/code): "Theme Evidence & Selection Rationale",
"Outcome-Weighted Theme Memory", "GDELT News Critic", "Context Sufficiency & Humility Gate",
"ETF Flow / Index Technical Router".

> Rule of thumb: a card existing under `.claude/skills/` does **not** mean it is wired. Only
> `SEAM_TO_SKILLS` membership = live.

## 6. Firewalls 🔒

1. **Method/case memory firewall** — Phase A serves METHOD pages only, fail-closed (refuses
   case/missing/invalid). Freeze (SHA-256) → Phase B reads CASE pages for additive calibration only.
   The frozen causal object is never mutated.
2. **Discovery/expression firewall** — causal object mandatory (else `blocked`); expression mode
   (legs/pricing/sizing) never runs on the live LLM provider.
3. **Temporal firewall** — only a `method_rule` claim may be method context; expired forecasts force
   `current_update_required`; historical sources cannot be rendered as current.
4. **Semantic contract** — pre-snapshot economic-sanity + trade/expression-leakage check, fail-closed
   (narrow: 4 input kinds).
- **Not present:** a context-sufficiency / humility gate, and a news critic. The only "thin context"
  brakes are a data-confidence floor (0.5) and confidence ceilings (no scenarios → ≤0.45, no market
  value → ≤0.60).

## 7. Biggest issue: too many themes / weak human-analyst compression ⚠️

The aggregator (`engine/theme_aggregation.py`) is a deterministic lexical v1:
- **Greedy, order-dependent single-pass clustering**; an item merges only if a **max** over six
  Jaccard overlaps ≥ **0.5** — a high bar, so near-duplicate themes stay **separate**.
- **Canonical name = the longest raw member** (no synthesis).
- **No parent-theme / subtheme hierarchy**; clusters are flat.
- **No cap** on themes per batch; **no human-analyst compression pass**.

Result: breadth without judgment — many near-duplicate themes, hot topics promoted as core themes,
weak cross-source coherence. A human analyst wants **3–7 parent themes**, each with subthemes,
per-source evidence, a causal mechanism, an observable axis, a falsifier, a temporal status, and a
strategy-family mapping. **The fix is a new ThemeCompressionAgent (proposed, not built).** Full
treatment in `docs/THEME_DISCIPLINE_AND_FAILURE_MODES.md`.

## 8. Current roadmap (ranked)

1. **ThemeCompressionAgent / AnalystThemeMap** — fixes theme explosion (parent/subtheme hierarchy,
   capped output, merge rules, "why these themes, why not the others").
2. **Theme selection-rationale object** — bind chosen evidence to a stated mechanism (fixes
   evidence-without-reasoning and reasoning-without-evidence).
3. **DiscoveryRunnerAgent wiring** — wrap the existing pipeline as a registry agent.
4. **WikiLintAgent wiring** — orchestrate the existing 14 validators.
5. **Discovery-output persistence** — write routed `ThemeObject`s back to the wiki.
6. **TemporalContext outcome-candidate linkage** — feed expired forecasts into outcome records.
7. **Outcome calibration** — implement `calibration_report`/`edge_realization` once a closed-thesis
   corpus exists.
8. **Context Sufficiency / Humility Gate** — refuse to opine on thin context.
9. **GDELT News Critic** — external corroboration, tagged attention-not-evidence.
10. **Skill wiring** — evidence-weighting → Q4, factor-r2 → routing (gated on golden master).

## 9. What I usually want help with

- Designing the **ThemeCompressionAgent** and its `AnalystThemeMap` schema (the #1 priority).
- Making theme output read like a **human analyst's** (fewer, hierarchical, source-connected themes).
- Strengthening **memory persistence** (round-tripping discovery output into the wiki).
- Wiring **contract_only agents** (DiscoveryRunner, WikiLint) without breaking the golden master.
- Keeping every change **inside the firewalls** and **out of trade execution**.

> When helping: trust the status tags over the README; preserve the firewalls; keep discovery
> separate from expression/trades; prioritise theme compression and memory persistence.
