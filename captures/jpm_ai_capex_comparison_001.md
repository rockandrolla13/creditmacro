# JPM AI Capex — Live Discovery vs Known-Correct Output (comparison_001)

**Run status:** BLOCKED at the first generative seam (`expand_causal`, `engine/llm_provider.py:105`).
**Reason:** no Anthropic credential in the environment (`ANTHROPIC_API_KEY` unset). The opt-in guard
(`ALLOW_LIVE_LLM_DISCOVERY=1`) passed; the wall is the missing credential. **Zero discovery stages
executed.** No fallback to scripted was performed (per instruction).

Because nothing ran, every **Actual** cell is `BLOCKED` and every gap is `BLOCKED`. To keep this file
useful as a regression baseline, a second column — **Capable w/ key?** — records whether the engine,
*as currently wired*, COULD produce the expected output once a credential is supplied. That column is a
static read of the code, not a live result.

Gap legend: BLOCKED = stage didn't run · CORRECT MISS = genuinely present in report but engine can't reach
it · HALLUCINATION = produced something not in report · PARTIAL = right direction, wrong specifics ·
ORDERING = found but ranked wrong.

---

## Stage 1 — Iceberg Classification

| Field | Expected | Actual | Match? | Capable w/ key? | Gap |
|---|---|---|---|---|---|
| Main Development | AI infra funding = distinct credit ecosystem (27 issuers, ~$455bn) | BLOCKED | BLOCKED | **No** | `LLMProvider` has no `classify_iceberg` seam; `parse()` returns empty streams. No IcebergClassification even on a successful run. |
| Key Event | DC sub-sector enters JULI ($49bn par, 0.5% of JULI) | BLOCKED | BLOCKED | No | Same — no iceberg seam wired. |
| Hot Topic (do NOT promote) | HPC-HY +9.99% YTD, 12bp through HY index — high attention/crowded | BLOCKED | BLOCKED | No | Same. The "divergence(evidence, attention)" pre-screen is not implemented in the live provider. |
| Core Theme (promote) | hyperscaler-vs-project basis; GPU-vs-DC dispersion; index-inclusion technical | BLOCKED | BLOCKED | No | Same. |

**Stage verdict:** BLOCKED (and, even unblocked, a CORRECT-MISS-by-construction: the seam is absent).

---

## Stage 2 — Causal Chain

| Field | Expected | Actual | Match? | Capable w/ key? | Gap |
|---|---|---|---|---|---|
| Spine | AI capex demand → hyperscaler leasing → project financing → DC/HPC issuance growth → valuation dispersion | BLOCKED | BLOCKED | Partial | `expand_causal` would build ONE chain from the 1-sentence input (not the PDF). Could plausibly recover the spine if the sentence carries it; this run never reached the call. |
| Edge: hyperscaler→neocloud (stated) | present, inferred=False | BLOCKED | BLOCKED | Partial | Depends entirely on the model; report supports it (p3 CRWV). |
| Edge: GPU obsolescence→collateral risk (inferred) | present, inferred=True | BLOCKED | BLOCKED | Partial | Report supports GPU-vs-DC business-model risk (p1/p7). |
| Edge: index exclusion→suppressed buyer base (stated, feedback=True) | present, feedback=True | BLOCKED | BLOCKED | Partial | Report supports (144A-for-life / limited syndication, p8). |
| Dead ends valid; never invent an axis | honored | BLOCKED | BLOCKED | Yes | `expand_causal` requires a routable main_theme with an operational axis or it blocks — consistent with "don't invent." |

**Stage verdict:** BLOCKED.

---

## Stage 3 — Operational Axes

| Expected axis | Actual | Match? | Capable w/ key? | Gap |
|---|---|---|---|---|
| OAS(project) − OAS(hyperscaler) per lease pair (105bp IG / 183bp HY) | BLOCKED | BLOCKED | Partial | Was passed in as `--axis` candidate; `define_axis` would select ONE axis only. |
| OAS(Data Centers) − OAS(Technology) (181 vs 101) | BLOCKED | BLOCKED | Partial | Passed as 2nd `--axis`; engine keeps only one promoted axis per run. |
| HPC spread − HY index spread (295 vs 307, through index) | BLOCKED | BLOCKED | No | Not passed; engine builds one axis, would not enumerate this separately. |
| Index-included vs index-excluded DC basis | BLOCKED | BLOCKED | No | Same — single-axis ceiling. |
| HPC issuance share of HY non-refi supply (43%) | BLOCKED | BLOCKED | No | Same. |

**Stage verdict:** BLOCKED. Structural note: the engine promotes **one** axis per causal object; the
report yields **five**. Recovering all five needs five runs or a multi-theme nomination stage.

---

## Stage 4 — System Map

| Element | Expected | Actual | Match? | Capable w/ key? | Gap |
|---|---|---|---|---|---|
| Stocks | outstanding DC/HPC debt, index weight, positioning, DC capacity | BLOCKED | BLOCKED | Partial | `build_system_map` seam exists (system-mapper card); never reached. |
| Flows | new issuance (43% non-refi HY), ETF/fund inflows, index-inclusion changes | BLOCKED | BLOCKED | Partial | Same. |
| Reinforcing loop | performance → attention/inflows → tightening → more performance | BLOCKED | BLOCKED | Partial | Same — `diagnose_loops` (trap-detector) would classify. |
| Balancing loop | issuance growth → supply pressure → cheapening | BLOCKED | BLOCKED | Partial | Same. |
| Delays | index-inclusion lag, construction lag, secondary-liquidity lag | BLOCKED | BLOCKED | Partial | Same. |

**Stage verdict:** BLOCKED.

---

## Stage 5 — Trap Detection

| Element | Expected | Actual | Match? | Capable w/ key? | Gap |
|---|---|---|---|---|---|
| Trap class | success-to-the-successful / crowding on HPC-HY (+9.99%, through index, 2.68% wt) | BLOCKED | BLOCKED | Partial | `diagnose_loops` could name it IF HPC is the routed theme — but HPC is exactly the theme that should NOT be promoted, so it may never become the routed causal object. |
| Early warnings | issuance rising while spreads stop tightening; flow reversal; concessions widening | BLOCKED | BLOCKED | Partial | Maps to `early_warning_indicators`. |
| Decision on HPC beta-long | watchlist or reject (not promote) | BLOCKED | BLOCKED | Partial | Router can emit `watchlist_only`, but only if HPC is the single routed theme. |

**Stage verdict:** BLOCKED.

---

## Stage 6 — Strategy Families (ranked)

| Rank | Expected family | Expected confidence posture | Actual | Match? | Capable w/ key? | Gap |
|---|---|---|---|---|---|---|
| 1 | hyperscaler-project basis → `cash_cds_basis`/`long_short` (basis, tighter) — highest latent edge | highest | BLOCKED | BLOCKED | Partial | A basis axis routes to `cash_cds_basis`; but only ONE family is returned. |
| 2 | GPU-vs-DC dispersion → `long_short` (relative_value) — high edge, lowest survivability | lower (liquidity bites) | BLOCKED | BLOCKED | No | Not emitted: single-family ceiling. |
| 3 | index-inclusion technical → `outright`/`long_short` — event-driven, low base rate | low | BLOCKED | BLOCKED | No | Same. |
| 4 | HPC-HY beta-long → `watchlist_only` (already +9.99%, through index) | lowest / reject | BLOCKED | BLOCKED | No | Same. |

**Stage verdict:** BLOCKED. Structural note: `select_strategy_families` returns a **single-element**
list. The ranked quartet cannot be produced from one run regardless of the LLM.

---

## Stage 7 — Confidence Flags

| Flag | Expected | Actual | Match? | Capable w/ key? | Gap |
|---|---|---|---|---|---|
| Liquidity gate bites on 144A-for-life / limited-syndication / Agg-excluded names | should fire (like ETF basis at λ 0.32) | BLOCKED | BLOCKED | No | Discovery `ConfidenceComponents` has no explicit liquidity term; the liquidity gate lives in Engine 3 (expression), which discovery never runs. |
| edge_basis flags `gross_of_risk_premium` (basis is mostly GPU/business-model risk premium) | should flag | BLOCKED | BLOCKED | No | No `edge_basis`/risk-premium field on `ConfidenceComponents`; `edge_survival` is "unknown" without scenarios. |
| data_confidence capped (snapshot-only, no history) | capped | BLOCKED | BLOCKED | Partial | `_data_confidence` DOES cap to 0.5 when scenarios/pricing absent — so this one would cap correctly, but for the generic "no scenarios" reason, not specifically "snapshot-only." |

**Stage verdict:** BLOCKED.

---

## Roll-up

| Stage | Actual | Classification |
|---|---|---|
| 1 Iceberg | BLOCKED | BLOCKED (+ seam absent even with key) |
| 2 Causal chain | BLOCKED | BLOCKED |
| 3 Operational axes | BLOCKED | BLOCKED (+ single-axis ceiling) |
| 4 System map | BLOCKED | BLOCKED |
| 5 Trap detection | BLOCKED | BLOCKED |
| 6 Strategy families | BLOCKED | BLOCKED (+ single-family ceiling) |
| 7 Confidence flags | BLOCKED | BLOCKED |

No HALLUCINATIONs observed (nothing was generated). No PARTIAL/ORDERING observed (no output to mis-rank).
The sole observed failure mode is BLOCKED, with two **distinct** root causes layered on top of each other:
a **credential blocker** (immediate) and an **architectural capability gap** (latent, would surface as
CORRECT MISSes the moment a key is supplied).
