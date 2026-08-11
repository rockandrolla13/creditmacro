# BLOCKED.md — decisions requiring input the ONTOLOGY does not determine

Format: ID | question | proposed resolution (implemented behind a named
constant) | affected files. Nothing here is silently chosen.

---

### B-01 — Pass B `match_confidence` calibration
**Question.** τ_ORPHAN = 0.6 gates orphan routing, but `match_confidence`
is an LLM property, not a knob. Miscalibration → everything orphans or
nothing does. What calibration target / method?
**Proposed resolution.** Implement a calibration harness over the golden
corpus; gate Pass A/B with `scripted_provider` so gates are deterministic.
Expose `MATCH_CONFIDENCE_FLOOR = τ_ORPHAN` and measure precision/recall of
routing on the golden set before trusting live values.
**Status (2026-07-09).** LLM seams wired: `LLMClaimProvider` (Pass A) and
`LLMMatchScorer` (Pass B) call `anthropic.Anthropic().messages.create`
(default `claude-opus-4-8`), gated behind `ALLOW_LIVE_LLM_DISCOVERY=1`; a real
client is built only under the opt-in, tests inject a fake client. The
StructuralSemanticMapper default scorer stays deterministic (node-Jaccard) so
gates remain LLM-free. STILL OPEN: the calibration harness measuring
match_confidence precision/recall on the golden corpus.
**Affected.** `ingest/pass_a.py`, `ingest/pass_b.py`, `ingest/prompts/`,
`llm_json.py`, `tests/golden/corpus/`.

### B-02 — Embedding provider for novelty (ν) and clustering
**Question.** §Scoring ν and §Admission clustering need sentence
embeddings + cosine (COS_NOVELTY, COS_COSMETIC). Which embedding model,
and is it available offline for deterministic gates?
**Proposed resolution.** Behind an `Embedder` protocol; a deterministic
hash-based stub embedder for gates, real model wired at runtime via
`LedgerRunConfig`. Constant names unchanged.
**Affected.** `ingest/scoring_view.py`, `ingest/admission.py`,
`wiki/wiki_import.py` (cosmetic pre-filter).

### B-03 — Tracked-axis registry contents
**Question.** WF(c) requires X ∈ tracked-axis registry, but the registry's
membership (which OAS/CDX/curve series, with which sign conventions and
data feeds) is not enumerated in the ONTOLOGY.
**Proposed resolution.** Seed `vocab.py::TRACKED_AXES` from the operational
axes already named on the 4 curated theme pages + the standard credit
indices (C0A0, H0A0, CDX.IG/HY, 3M10Y); mark it a review-gated registry
like V. Out-of-registry axis → WF(c) fail → NEEDS_STRUCTURING.
**Affected.** `vocab.py`, `substrate/identity.py` (WF).

### B-04 — Is there an economically meaningful `H_MIN` above 1 day?
**Question.** D-10 gives WF clause (d) a lower bound of `H > 0`, which the
ONTOLOGY determines (empty valid-time window at H = 0; degenerate half-life
h = H/2). It does NOT determine whether a *meaningful* floor sits above that.
A 1-day theme passes WF today, but a one-day transmission story is arguably a
directional call rather than a theme — the same objection WF clause (a) makes
to a k = 1 chain. Half-life h = H/2 also means a 1-day theme discards ~all
evidence within a day, so its S_θ is dominated by whatever landed this morning.
**Proposed resolution (interim, implemented).** Strict positivity only:
`0 < H ≤ H_MAX`, no new constant. If a floor is later wanted, it becomes
`H_MIN` in §Constants + `constants.py` (an ONTOLOGY change), with the natural
candidates being the surveillance sampling interval or W_ADMIT = 30 days.
Needs an analyst decision, not a code decision.
**Affected.** `substrate/identity.py` (WF clause d), `constants.py` (would gain
`H_MIN`), `docs/ledger/ONTOLOGY.md` §WF + §Constants.

### B-05 — the projected `main_theme` is not a node of the projected chain
**Question.** `projection.to_theme_object` synthesises
`main_theme = CausalNode(id=f"theme:{theme_id}", …)` while `causal_chain` carries
the vocabulary node ids (`funding_stress`, `liquidity_premium`, `credit_spread`).
`engine/workflow.py::_validate_causal_chain` requires `main_theme.id ∈
{n.id for n in causal_chain.nodes}`. **Measured, not inferred:** calling that
validator on a real projection output raises *"EXPAND_CAUSAL: main_theme must be
one of the chain's nodes"*. The projected object is therefore constructible but
not routable — nothing caught it because `to_theme_object` has no production
caller and builds the `ThemeObject` directly instead of going through
`run_workflow`. The ONTOLOGY does not say which node of `M` is the theme node.
**Proposed resolution.** Make the terminal node `vk` the routable `main_theme`:
set `kind="theme"`, attach the projected `Axis`, `axis_operational=True`, and
drop the synthetic `theme:<id>` node. `vk` is the node the operational axis `X`
proxies (ONTOLOGY §Theme: *"X is the observable proxy for vk"*), so this makes
the code say what the ontology already says. The alternative — appending the
synthetic node to the chain with an edge from `vk` — adds a node with no
transmission meaning and would inflate `k`, which is a WF-gated quantity.
**Which side is right.** The engine invariant is right and the projection is
wrong; the ONTOLOGY is silent, so this needs a `D-NN` delta once decided, not a
local override.
**Status (2026-08-11).** Resolved by `D-13`.
**Affected.** `engine/ledger/projection.py`,
`tests/integration/test_ledger_render_projection.py`, `engine/ledger_bridge.py`.

### B-06 — `forward_ingest` emits no events, so nothing can be folded
**Question.** The ledger is event-sourced: §Bitemporal defines a theme as a fold
over its event stream, and I5 makes `fold` the sole constructor of
`ThemeHypothesis`. But `runner.forward_ingest` returns
`AdmittedTheme(theme_id, status)` — a bare id and a status **string** — and
discards `AdmissionOutcome.created_event`. It also computes activation
(`B ≥ … ∧ S ≥ …`) without emitting the `STATUS_CHANGED` event that §Lifecycle
says governs the market-truth axis. So the population path (D-03, forward
re-ingest) produces a registry that cannot be folded, cannot be projected, and
cannot be queried as-of. Where do those events get created, and who persists
them?
**Proposed resolution.** Additive only: carry `created_event` on `AdmittedTheme`
and add the derived `STATUS_CHANGED` event when the activation gate fires, so
`fold` reproduces the status the runner computed rather than the runner
restating it as a string. Persistence to `JsonlEventStore` stays **opt-in** via
`LedgerRunConfig.events_store` so gate tests remain deterministic and
`recorded_at` keeps being stamped only inside the store (I7). No constant
changes; no change to `RegistryState`'s existing fields, so
`tests/golden/corpus/expected_registry.json` stays valid.
**Status (2026-08-11).** Resolved by `D-14`.
**Affected.** `engine/ledger/runner.py`, `engine/ledger_entrance.py`,
`tests/integration/test_ledger_admission.py`.

### B-07 — two pipeline statuses for one theme
**Question.** AMEND A3 says `projection.py` is *"the only site permitted to map
between axes"*, and it sets `ThemeObject.status` to `discovery_complete` or
`blocked`. Routing that same theme through `run_workflow` produces a SECOND
`ThemeObject` whose status is `strategy_family_routed`. Two objects, two
pipeline statuses, one theme. Is the workflow's status a second mapping (an A3
violation) or an independent computation?
**Proposed resolution.** It is an independent computation, and the distinction
is that `run_workflow` never reads the market-truth axis: it derives pipeline
progress from its own work (falsifier present ⇒ routed). The bridge preserves A3
by letting the lifecycle status influence exactly one thing — whether discovery
runs at all (`LedgerProjectionNotRoutable` on a `blocked` projection) — and never
the resulting status. The projected object is retained beside the routed one in
`LedgerDiscoveryResult` so both are auditable. If this reading is rejected, the
alternative is to have `projection.py` own the routed status too, which would put
strategy routing inside the ledger package.
**Status (2026-08-11).** OPEN. Proposed reading is implemented behind
`LedgerProjectionNotRoutable`; this remains a human question, not an agent
decision.
**Affected.** `engine/ledger_bridge.py`, `engine/ledger_entrance.py`,
`docs/ledger/ONTOLOGY.md` §Lifecycle (AMEND A3 wording).
