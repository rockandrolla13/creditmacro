# THE COMBINED SCHEMA — one ThemeObject, five stages

This is the artifact that turns five skills into one system. Every stage reads and
writes the **same** typed state. The skills are not summaries that sit beside the
engine; each one is a prompt authored to **emit exactly the slice of this schema** its
stage owns, and the next stage consumes it. Get this contract right and authoring is
just "write each prompt against these types."

> Ground truth: `engine/schema.py` (the `ThemeObject` and all nested models) and
> `engine/stage0.py` (`IngestionResult`). This doc mirrors the code; the code is canonical.
> Every stage field below is **Optional/additive** unless it predates the skills — so the
> AI-issuance golden master (which sets none of the skill fields) stays exact (147 tests).

---

## 1. The shared typed state

Two objects span the whole pipeline:

```
IngestionResult          # Stage 0 — the streams the classifier routes
  observations:            list[Observation]
  candidate_themes:        list[CandidateTheme]      # the "core themes" lane
  consensus_signals:       list[ConsensusSignal]     # the "hot topics" lane
  ranked_candidates:       list[CandidateTheme]      # sorted by pre_screen_score = evidence − attention
  iceberg_classifications: list[IcebergClassification]  # layer→lane→stream + promote/watchlist/noise

ThemeObject              # the shared state every later stage reads & writes
  # — identity (pre-skill core) —
  id, statement, horizon, author, created_at, version
  # — Engine 1 (driver/axis) —
  thesis:        Thesis
  axis:          Axis                      # = main_theme.axis when the causal stage ran
  # — Engine 2 (scenario pricing) —
  scenarios:     list[Scenario]            # each {p_s, X_s, sigma_g_s, hist_freq}
  pricing:       Pricing                   # q, residual_edge, scenario_fv(_std), edge_attribution,
                                           #   edge_basis="gross_of_risk_premium", snr…
  # — Engine 3 / 4 —
  expressions:   list[Expression]          # scored; gates-before-rank
  sizing:        Sizing
  risk:          Risk                      # falsifiers  ← assumptions + invalidation evidence
  pm_gate:       PMGate                     # open_questions ← non-identifiability + stage PM_questions
  provenance:    Provenance
  # — the five skill stages (all Optional, additive) —
  iceberg_classification: Optional[IcebergClassification]  # Stage 0: this theme's own classification
  main_theme:             Optional[CausalNode]             # EXPAND_CAUSAL
  causal_chain:           Optional[CausalChain]            # EXPAND_CAUSAL
  shared_factor:          Optional[str]                    # EXPAND_CAUSAL / SYSTEM_MAP (portfolio layer)
  system_map:             Optional[SystemMap]              # SYSTEM_MAP (embeds the chain)
  bias_critique:          Optional[BiasCritique]           # CRITIQUE
  trap_detection:         Optional[TrapDetection]          # TRAP (consumes the loop map)
```

### The skill-owned nested types (what each prompt must emit)
```
IcebergClassification {layer, dashboard_lane, typed_stream, scores:IcebergScores,
                       operational_axis|null, decision, confounder_flags}
CausalNode  {id, statement, kind:cause|theme|consequence, axis:Axis|null, axis_operational}
            # invariant: kind=="theme" ⇒ axis set AND axis_operational (else a dead-end mechanism)
CausalEdge  {from_id, to_id, mechanism, inferred, feedback}
CausalChain {nodes:[CausalNode], edges:[CausalEdge]}        # one depth-first spine
SystemMap   {boundary_inside/outside, function_purpose, elements:[CausalNode],
             interconnections:[CausalEdge], stocks:[Stock], flows:[Flow],
             feedback_loops:[FeedbackLoop(type:reinforcing|balancing)], delays:[Delay],
             external_shocks, internal_responses, observable_variables, surprise_modes}
BiasCritique {dominant_mental_model, alternative_models, assumptions_treated_as_facts,
              lenses_examined, disconfirming_evidence, decision:accept|challenge|reject_model}
TrapDetection {feedback_loop_map:[FeedbackLoop], dominant_loop_now, possible_loop_shift,
               system_traps, leverage_points:[LeveragePoint], early_warning_indicators,
               scenario_implications, expression_risk_implications, invalidation_evidence,
               pm_questions, decision:promote_to_scenario_pricing|watchlist|reject|needs_more_data}
Pricing     {normal_fv, scenario_fv(_std), priced_in:{q_s,frac}, residual_edge,
             edge_attribution:[EdgeContribution], edge_direction_ok, vol_adjusted_edge,
             edge_basis, q_status, snr, p_success, infeasible_fraction}
```

---

## 2. The pipeline order — who reads what, who writes what

`run_workflow(provider, policy)` drives the provider seams in this exact order
(`engine/workflow.py`); Stage 0 (`engine/stage0.py`) runs first and selects the theme.

| # | Stage (skill) | Seam | READS | WRITES | Decision / gate |
|---|---|---|---|---|---|
| 0 | **Iceberg Classifier** | `stage0.classify_iceberg` / `ingest` | raw items, `evidence/attention` | `IngestionResult.iceberg_classifications`; selects a `CandidateTheme`; `ThemeObject.iceberg_classification` | promote / watchlist / narrative_noise |
| 1 | context + drivers (Engine 1) | `context`, `extract_drivers`, `define_axis` | statement | `RunContext`, `thesis`, `axis` | — |
| 2 | **Causal Theme Compiler** | `expand_causal` | statement | `main_theme`, `causal_chain`, `shared_factor`; **main_theme.axis → the priced `axis`** | theme node ⇒ operational axis (else dead end); boundary-validated |
| 3 | **System Structure Mapper** | `build_system_map(thesis, causal_chain)` | `causal_chain` (embeds it) | `system_map` (stocks/flows/loops/delays) | reuses chain nodes/edges; Stock≠Flow; loop R/B |
| 4 | **Mental Model & Bias Critic** | `critique_mental_model(statement, causal_chain)` | `causal_chain` | `bias_critique` | accept / challenge / reject_model |
| 5 | **Feedback / Trap Detector** | `detect_traps(system_map)` | `system_map.feedback_loops` (consumes) | `trap_detection` | promote / watchlist / reject / needs_more_data |
| 6 | **Scenario & Counterfactual Pricing** (Engine 2) | `propose_scenarios`, `run_pricing` | `scenarios`, `axis`, `X_mkt`, `prior`, `thesis_sign`, `sigma_axis` | `pricing` (q via tilt + feasibility, `residual_edge`, attribution, `edge_basis=gross_of_risk_premium`) | INFEASIBLE if X_mkt outside scenario span |
| 7 | Expression scoring (Engine 3) | `enumerate_expressions` + `score_expression(policy)` | `expressions`, `scenarios`, `policy` | scored `expressions` | gates FIRST (Ω, λ, cost), rank SECOND |
| 8 | Sizing + risk (Engine 4) | `size_and_risk(best, conviction)` | best expression | `sizing`, `risk`, `pm_gate` | — |
| 9 | Emit | `ThemeObject(...)` | all of the above | the validated `ThemeObject` | **4 discipline gates** (below) fire on construction |

**Flow of the diagnoses into existing fields** (no new fields invented):
the standing **credit-risk-premium confounder** → `pricing.edge_basis`; skill **assumptions
+ testable/invalidation evidence** → `risk.falsifiers`; skill **non-identifiability +
PM_questions** → `pm_gate.open_questions`; the **shared_factor** → the portfolio layer.

**Governance posture.** Stages 0/4/5 record `decision`s on the object; they are **advisory,
not gating** — the only hard stops are the four discipline gates at emit. (Flipping
`reject_model` / `reject` into a hard stop is a one-line policy change; today every
diagnosis is *persisted* so the PM sees where agreement and risk live.)

---

## 3. The four discipline gates (the only hard stops)

A `ThemeObject` cannot be constructed unless (`schema.py:discipline_gates`):
1. **axis is operational** — `axis.definition` and `axis.measurement` are real computable series.
2. **residual_edge is computed** — `pricing.residual_edge` is not None.
3. **≥1 expression survived** the Ω / liquidity / cost gates (`expressions[i].score is not None`).
4. **≥1 falsifier** with an observable + threshold.

These are type constraints, not quality checks. A thesis missing any of them is never emitted.

---

## 4. Why this is *the* artifact

- **One state, many lenses.** Five independent skills (ingest, compile, map, critique, trap)
  write disjoint slices of one `ThemeObject`; none can emit a shape the next stage rejects,
  because the schema — not prose — is the interface. That is "process primitives, not summaries."
- **The same epistemic rule, enforced three times.** `−attention` at Stage 0
  (`narrative_noise`), `reject/challenge` under reinforcing-loop dominance at CRITIQUE/TRAP,
  and `edge_basis="gross_of_risk_premium"` at pricing are the *same* confounder (the market is
  already looking) surfaced at three depths of the schema.
- **Authoring reduces to typing.** Each skill prompt's job is now narrow: read its input
  slice, emit its output type, tag `inferred`/`feedback`/`PM_assumption`/`model_required`,
  and stop. The combined schema is the spec all six prompts (ScriptedProvider today,
  LLMProvider live) are written against.

**Add a stage** = add an Optional field + a `Provider` seam + a workflow line.
**Add a case** = a YAML file. The schema is the system; everything else authors against it.
