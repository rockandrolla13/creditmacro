# creditmacro — Theme-to-Trade Conversion Engine

A disciplined, **epistemic** pipeline that converts a research document into a **falsifiable
thematic hypothesis** and a ranked set of strategy families. It is built on the Alaph four-step
process (theme → valuation → trade selection → portfolio construction), but it deliberately
**STOPS at a PM decision memo** — it does not generate trades.

> **Product boundary:** idea / report → causal object → ranked strategy families with confidence
> → **STOP**. No trades, no legs, no sizing, no hedge ratios, no execution.

---

## What it does

Stage 0 (ingestion) parses research into three **separate** typed streams — `Observation`
(facts), `CandidateTheme` (narratives), `ConsensusSignal` (attention) — and pre-screens
candidates by `divergence(evidence, attention)` (high factual support + low attention = latent
edge). Surviving candidates flow through a shared, typed `ThemeObject` populated by four engines:

| Engine | Produces | Status |
|---|---|---|
| **1 — Driver + axis** | Q1 theme, Q2 universe, Q3 **operational axis** (a computable spread/slope series) | real |
| **2 — Scenario pricing** | Q4 fair value, Q5 scenario FV = Σ pₛXₛ, Q6 priced-in **q** via max-entropy tilt, Q7 residual edge = ⟨p−q, X⟩ | real (golden-mastered) |
| **3 — Expression scoring** | Q8 candidates, Q9 best = gated multiplicative score (purity ρ² · Ω · convexity · liquidity · crowding) | real |
| **4 — Sizer + risk** | Q10 size, Q11 stop, Q12 falsifiers | real (expression mode) |
| **PM gate** | Q13 open questions → hands control to the human | real |

**"Best" is never `max E[P&L]`.** Gates come first (asymmetry Ω ≥ 2, liquidity ≥ min, finite worst
case), ranking second. A thesis with no falsifier is not emitted.

---

## Two modes, two firewalls

The engine runs in two modes and is protected by two firewalls **by construction** (not by
instruction):

- **Discovery mode** (default): idea/report → causal object → ranked strategy families with
  decomposed confidence → **STOP at `strategy_family_routed`** (or an inspectable `blocked` HALT
  if there is no clean causal object/axis). **Expression mode** (legs, scenario pricing, sizing)
  is fenced downstream and never runs on the discovery-only LLM provider.

- **Discovery/expression firewall** — a causal object is mandatory; with none, discovery emits a
  `blocked` record rather than fabricating a path to a trade.

- **Memory access firewall (two-phase)** — *reason fresh, freeze, then consult history.*
  - **Phase A:** a fail-closed `MemoryRetriever` serves **METHOD** pages only and refuses **CASE**
    pages (past themes, market reports, prior conclusions).
  - **FREEZE:** the phase-A causal object is serialized into an immutable `FrozenSnapshot` with a
    SHA-256 content hash before any case read.
  - **Phase B:** case pages become readable **only** for analogue/calibration, written to an
    additive block that references the snapshot hash — the frozen reasoning is never mutated.

  Every page declares `access_class: method | case`. The hazard this closes: old case conclusions
  leaking into fresh causal reasoning.

---

## Live discovery

The generative discovery seams run **live** behind an explicit opt-in:

- `LLMProvider` implements the discovery seams — `expand_causal`, `define_axis`,
  `build_system_map`, `diagnose_loops`, `critique_mental_model`, `macro_context` — each calling
  the model behind a purpose-specific prompt and validating the JSON into the engine schema.
- **Provider selection:** `ScriptedProvider` is the default (tests, golden cases); the live
  `LLMProvider` is selected explicitly and a real call fails closed unless
  `ALLOW_LIVE_LLM_DISCOVERY=1`.
- **Automatic semantic-contract gate:** before any snapshot, every live output is checked for
  economically-wrong axes and trade-leg/sizing/expression leakage — **fail closed** on violation.
- **Capture / replay:** live runs write private, gitignored records under `runs/live_discovery/`;
  captured outputs replay through the validators with no model call (deterministic).

Manual smoke run:

```bash
ALLOW_LIVE_LLM_DISCOVERY=1 python -m engine.example_live_discovery \
  --provider llm --mode discovery \
  --input "AI capex funding is creating RV opportunities across hyperscalers, \
           data-center project bonds and HY HPC issuers." \
  --current-source wiki/sources/jpm-ai-capex-funding-2026-05-11.md \
  --input-kind jpm_report
```

---

## Memory layers

| Layer | Path | Role |
|---|---|---|
| **Raw (immutable, private)** | `raw/`, `markdowns/` | original PDFs + page-aware normalized markdown; gitignored where copyrighted |
| **Wiki (curated memory)** | `wiki/` | sources, evidence atoms, concepts, themes, scenarios, ranked strategy families; `access_class`-tagged; lint conventions in `wiki/CONVENTIONS.md` |
| **Method skills** | `.claude/skills/` | reusable **PROCESS** cards compiled (paraphrased) from books/papers — iceberg-classifier, causal-compiler, system-mapper, trap-detector, scenario-pricing-engine, macro-regime-classifier, evidence-weighting, priced-in-estimator, edge-validity |

Copyright discipline: the wiki stores short paraphrases, schemas, gates, and code specs — never
reproduced source text (a ≤25-word verbatim-leak check enforces this).

---

## Layout

```
engine/            the pipeline: schema/, workflow, engine2 (pricing), discovery,
                   probability (Q4), firewall + memory, llm_provider, live_discovery,
                   semantic_contract, skills, provider_select, capture
engine/schema/     typed ThemeObject + sub-models (causal, pricing, risk, macro, …)
tools/             source compiler (PDF → normalized-md → source cards + method cards)
.claude/skills/    method skill cards (the agent's how-to-reason memory)
wiki/              curated memory layer (method + case pages)
cases/             scripted discovery/expression fixtures (incl. the AI-issuance golden case)
markdowns/         immutable raw source corpus
tests/             unit + integration (firewalls, golden master, live seams, skills)
```

## Stack

Python · Pydantic schema · SciPy for the max-entropy q solver · LLM calls behind provider
interfaces. One orchestrated workflow over the shared `ThemeObject`.

## Tests & invariants

```bash
python3 -m pytest tests/ -q
```

The **golden master** (AI-issuance expression case) is locked to 1e-6: scenario FV `75.0`,
`q = [0.125512, 0.184417, 0.328452, 0.361619]`, edge `20.0`, Ω `7.6667`, best score
`3.918220233274124`, ETF gated at `λ 0.32 < 0.40`, sizing `1.25 / 750000 / 747000`. The two
firewalls and the no-trade discovery boundary are regression-tested, including against the real
on-disk wiki.

---

*Epistemic engine. Discovery stops at ranked strategy families. Expression remains downstream and
fenced. No trades are emitted.*
