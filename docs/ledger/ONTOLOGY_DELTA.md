# ONTOLOGY_DELTA.md — institutional memory of design decisions

Every decision NOT directly derivable from the original ONTOLOGY, recorded
at the moment it was made. Format: ID | decision | rationale | alternatives
rejected | affected files.

---

### D-01 — Relocate the build from `src/` to `engine/ledger/`
**Decision.** The Theme Hypothesis Ledger is built as a subpackage of the
existing `engine/` tree, not the `src/themes` / `src/ingest` / `src/vocab`
layout named in BUILD_PROMPT.
**Rationale.** A `src/` twin would duplicate `schema`, the two-phase memory
firewall, `surveillance_agent`, `llm_provider`, `firewall.freeze`, and
`discovery` — producing two sources of truth for "what is a theme" that
drift. The ledger is the re-founded Stage-0/1 front end plus a temporal
lifecycle; `ThemeObject` is downstream and becomes a projection.
**Rejected.** (a) `src/` greenfield sibling — creates the twin-engine
disaster. (b) Full replacement of `engine/` — unnecessary; engines 2–4 are
sound and unchanged.
**Affected.** All Tier-1 CI grep/import paths retarget `engine/ledger/…`.

### D-02 — Tier-1 enforcement is grep + AST, not import-linter
**Decision.** The repo has no `pyproject.toml` / import-linter dependency.
I2/I3 import firewalls are enforced by an AST walk in
`tools/ledger_invariants.py`; I1/I5/I6 by grep. Runnable with stdlib only.
**Rationale.** Zero new dependencies; matches the existing `tools/leak_check.py`
style.
**Rejected.** Adding import-linter + pyproject — heavier, and the AST check
is equivalent for these contracts.
**Affected.** `tools/ledger_invariants.py`.

### D-03 — Population path is forward re-ingest (user decision, 2026-07-07)
**Decision.** The registry is rebuilt by running Pass A fresh over the
source corpus (`markdowns/`, `wiki/sources/`) → orphan pool → admission.
The 82 non-WF-surviving theme cards are discarded as themes and kept only
as provenance breadcrumbs (`wiki/breadcrumbs.py`, card→source map).
**Rationale.** WF-survival spike: 82/86 existing theme pages fail WF(a)
(k ≤ 1). Importing them would inject vibes; admission must reconstruct
themes from claims with the discipline gate applied.
**Rejected.** (a) Reuse evidence atoms as seed claims — deferred, not chosen.
(b) Treat each card as a pre-clustered claim group — risks importing vibes.
**Affected.** `ingest/pass_a.py`, `ingest/admission.py`, `wiki/wiki_import.py`
(now handles only 4 curated themes), `wiki/breadcrumbs.py`.

### D-04 — `wiki_import` scope: only the 4 WF survivors
**Decision.** `wiki_import` emits CREATED + prior-mass for exactly
`ai-capex-funding-credit-ecosystem`, `hyperscaler-project-bond-basis`,
`hy-hpc-crowding-and-supply`, `data-center-index-inclusion-technicals`.
**Rationale.** These are the only current `wiki/themes/` pages carrying a
k≥2 chain + operational axis + falsifier (the curated core-theme set).
**Affected.** `wiki/wiki_import.py`, Phase-2 gate tests.

### D-05 — ONTOLOGY amendments A1/A2/A3 + fixes F1/F2 (see ONTOLOGY.md)
**Decision.** Folded five amendments into ONTOLOGY.md: A1 vocabulary
crosswalk (V ↔ CausalNode/wiki concepts), A2 wiki-inversion scoped to
theme case pages only, A3 three-status-axis reconciliation, F1 prior-mass
is wiki-import-only (RETIRED+CREATED starts empty), F2 identity-vs-merge
tie-break.
**Rationale.** The original ONTOLOGY was written blind to `engine/`; per its
own preamble ("conflict is a bug") these reconcile it with the existing
tree and fix two internal under-specifications.
**Rejected.** Leaving them for code-time — the ONTOLOGY is the contract;
resolving in code would let deltas silently contradict it.
**Affected.** `docs/ledger/ONTOLOGY.md`, `vocab.py`, `projection.py`,
`wiki/render.py`, `substrate/fold.py`, `substrate/identity.py`.

### D-08 — Deterministic mechanism-synthesis rule for admission
**Decision.** §Admission says "mechanism assembled over the vocabulary from the
cluster's modal tags" but leaves the assembly unspecified. Chosen rule
(`ingest/admission.py`): chain = top-2 modal in-vocab tags (sorted by −frequency then
name) → `SYNTH_VK` ("credit_spread"), all edge signs +1; σ = sign(Σ claim.direction);
X = modal market_variable; H = min horizon; F synthesized. `theme_id = admitted:<a>-<b>`.
A cluster with fewer than 2 distinct in-vocab tags → NEEDS_STRUCTURING (can't reach
k≥2). Founding EvidenceLinks are emitted for the clustered claims (they ARE the
theme's evidence; match_confidence 1.0), so activation scores against real polarity.
**Rationale.** Determinism (needed for the golden end-state) + guarantees WF(a) k≥2.
**Rejected.** Embedding-ordered chains (non-deterministic); richer multi-tag chains
(no principled ordering without an LLM). This is a v1 heuristic; a learned synthesizer
is a later seam.
**Affected.** `ingest/admission.py`, `runner.forward_ingest`, golden `expected_registry.json`.

### D-07 — Polarity carries sign(X) (from the post-Phase-4 SIGN_AUDIT)
**Decision.** `polarity = claim.direction × d(θ) × sign(X)`, applied uniformly
(including vk-measured claims). Polarity is stored in the operational-axis frame.
**Rationale.** SIGN_AUDIT CR-BUG-001: the ONTOLOGY §EvidenceLink shorthand
`claim.direction × d(θ)` omitted sign(X), contradicting §Theme's
`d_X(θ)=d(θ)·sign(X)` and the `test_axis_flip_remap` gate. Without sign(X), an
inverted-convention axis silently inverts every polarity and downstream S_θ sign.
**Rejected.** Applying sign(X) only to axis-measured claims — leaves vk-claims in a
different frame from axis-claims within one theme; the uniform axis-frame convention
is simpler and matches what the Breach Buffer observes.
**Affected.** `ingest/pass_b.py` (already correct), `docs/ledger/ONTOLOGY.md`
§EvidenceLink (amended), `vocab.axis_sign` (CR-BUG-002 guard).

### D-06 — ONTOLOGY constants live in `constants.py` as module-level names
**Decision.** `engine/ledger/constants.py` mirrors §Constants as
module-level named values (not a Pydantic config object). Runtime settings
(paths, provider) use a separate Pydantic `LedgerRunConfig`.
**Rationale.** §Constants mandates single-point named references and treats
a change as an ONTOLOGY edit — these are invariants, not serialisable config.
**Affected.** `constants.py`, `runner.py`.

### D-09 — Activation is `|S_θ| ≥ 2`; commit e4b6740 dropped the absolute value
**Decision.** The ONTOLOGY wins. `runner.forward_ingest` restores
`abs(sv.S) >= ACTIVATION_ABS_SCORE_MIN`, and the test that codified the
regression (`test_negative_score_with_required_breadth_does_not_activate`)
is amended to assert ACTIVE, renamed
`test_negative_score_with_required_breadth_activates_as_contested`.
**Rationale.** §Lifecycle and §Constants both state the gate as
`B_θ ≥ 2 ∧ |S_θ| ≥ 2`, and §Theme "Interpretation" plus §Lifecycle both say a
theme with `S_θ < 0` and no breach is CONTESTED — "a reportable sub-state of
ACTIVE, not dead". `engine/ledger/lifecycle.py:4,20` and `PLAN_TRACKER.md`
already carried `|S|`, and the constant is literally named
`ACTIVATION_ABS_SCORE_MIN`; only `runner.py:84` disagreed. Commit **e4b6740**
("orch task 1.5", 2026-08-10) changed that line FROM `abs(sv.S) >= …` TO
`sv.S >= …` and, in the same commit, added a test asserting the new wrong
behaviour — so the regression was self-ratifying. The effect was not cosmetic:
a theme the whole street agrees is NOT happening (strong negative consensus,
breadth ≥ 2) is exactly as informative as one it agrees IS, and under the
regression it was permanently parked at CANDIDATE and never reported.
**Rejected.** (a) Amend the ONTOLOGY to match the code (drop the absolute
value) — it would contradict §Theme's CONTESTED interpretation in two places
and make `ACTIVATION_ABS_SCORE_MIN` a lie. (b) A local override in `runner.py`
with a comment — Tier-1 discipline forbids it; the ONTOLOGY is the contract.
**Affected.** `engine/ledger/runner.py:84`,
`tests/unit/test_ledger_activation.py`. No ONTOLOGY edit: it was already
right. Golden end-state unchanged (the golden theme scores S > 0).

### D-10 — WF clause (d) is two-sided: `0 < H ≤ H_MAX`
**Decision.** Amend ONTOLOGY §WF clause (d) and §Theme H to `0 < H ≤ H_MAX`;
`substrate/identity.wf_predicate` rejects `horizon_days ≤ 0` as clause (d).
The bound is expressed as strict positivity, not a new tunable constant, so
`constants.py` is unchanged.
**Rationale.** The predicate had only an upper bound, so `H = 0` and `H = -30`
were well-formed. The consequence is silent, not loud: `ingest/scoring_view.
_decay` returns 0.0 for `horizon_days ≤ 0`, so on identical evidence (three
unanimous conviction-3 claims from three institutions dated 2026-04-01/03/06,
as-of 2026-04-06) `H = 90` gives S = 8.64 / B = 3 and activates, while `H = 0`
and `H = -30` both give S = 0.0 / B = 0 and can never activate under any
evidence. Such a theme is admitted, well-formed, and permanently invisible —
the worst failure mode for a ledger whose job is surfacing. The ONTOLOGY
determines the bound rather than leaving it open: §Bitemporal defines valid
time as the window `[effective_at, effective_at + H]` (empty at H = 0) and
§Scoring keys the evidence half-life to `h = H/2` (degenerate at H = 0). At
day granularity that fixes the interim floor at H ≥ 1 day.
**Rejected.** (a) Leave WF alone and treat the `_decay` zero-guard as the
defence — it converts a malformed theme into a silent one, which is what the
NEEDS_STRUCTURING queue exists to prevent. (b) Introduce an `H_MIN` constant
above 1 day (e.g. 7 or 30) — not determined by the ONTOLOGY, and a new
constant is a §Constants edit; routed to BLOCKED **B-04** instead.
**Affected.** `docs/ledger/ONTOLOGY.md` §Theme + §WF + §Constants (amended),
`engine/ledger/substrate/identity.py`, `tests/unit/test_ledger_identity_wf.py`,
`tests/unit/test_ledger_activation.py`, `docs/ledger/BLOCKED.md` (B-04).

### D-11 — A directionless orphan cluster is CONTESTED, not bullish
**Decision.** `ingest/admission.admit` routes a cluster whose claim directions
cancel exactly (`Σ claim.direction == 0`) to `needs_structuring`. It no longer
synthesizes a direction. No ONTOLOGY edit: §Theme already fixes the domain.
**Rationale.** The synthesis rule (D-08) read `σ = 1 if sum(...) >= 0 else -1`,
so the `>= 0` silently resolved an exact tie to +1. Reproduced, not inferred: a
cluster of three claims from three distinct institutions with directions +1, −1
and 0 — a maximally contested cluster — was **admitted with σ = +1**, with no
flag and no review tag. §Theme line 36 fixes the domain at `σ ∈ {+1, −1}`, so
`sign(0) = 0` has no legal representation and the old rule had to invent one.
This is worse than a mislabel: §Identity line 111 makes theme identity the pair
`(M, σ)`, so breaking the tie MINTS A DISTINCT THEME — evidence supporting
neither direction founds the bullish one, and the bearish twin `(M, −σ)` is a
different theme that now cannot be founded from the same claims. §Theme line 68
forbids exactly this conflation: *"Never represent 'the opposite is happening'
as a negative score on (M, +σ)."* It is also the failure the project exists to
prevent — CLAUDE.md: *"A missing output is always preferable to an unsourced
one. Blocked beats plausible."*
**Rejected.** (a) Admit with σ = +1 and set a review tag — the theme is still
founded with a fabricated identity; a tag on a wrong object does not unmake it.
(b) Break the tie by conviction-weighted sum — invents a tie-break the ONTOLOGY
does not license, and merely moves the exact-zero case rather than removing it.
(c) Emit both `(M, +1)` and `(M, −1)` — founds two themes from evidence that
supports neither, and doubles the registry on the least informative clusters.
**Affected.** `engine/ledger/ingest/admission.py`,
`tests/integration/test_ledger_admission.py`. Golden end-state unchanged (the
golden corpus cluster has a non-zero net direction).

### D-12 — `to_theme_object` refuses an empty mechanism rather than crashing
**Decision.** `projection.to_theme_object` raises `ValueError` naming the theme
when `mechanism.edges` is empty, and the dead `theme.mechanism.v0 or "driver"`
fallback is deleted. No ONTOLOGY edit: WF clause (a) already rejects `k < 2`.
**Rationale.** Two lines of one function disagreed about whether edges could be
empty. Line 29 guarded for it (`v0 or "driver"`); line 48 indexed `edges[0]`
unguarded and raised `IndexError: tuple index out of range`. Reproduced by
folding a `CREATED` event carrying `{"edges": []}` — legal, because `fold` is
the sole constructor (I5) and deliberately does NOT run WF, so a malformed
hypothesis can reach the bridge. The guard was the wrong half to keep: a chain
with no `v0` and no `vk` has no transmission to render, so `"driver"` was a
fabricated node name entering a causal chain. Refusing names the failure at the
boundary and routes the theme to NEEDS_STRUCTURING, where WF clause (a) already
says it belongs.
**Rejected.** (a) Keep the `"driver"` placeholder and guard line 48 to match —
completes a `ThemeObject` whose driver name appears in no source. (b) Run
`wf_predicate` inside the projection — makes the renderer a second WF gate;
`substrate/identity.wf_predicate` is the single gate, and duplicating it invites
the two copies to diverge, which is the failure D-09 records.
**Affected.** `engine/ledger/projection.py`,
`tests/integration/test_ledger_render_projection.py`.

### D-13 — In projection, the routable `main_theme` is the terminal node `vk`
**Decision.** `projection.to_theme_object` uses the terminal node `vk` of the
transmission chain as the routable `main_theme` in the projected `ThemeObject`,
with the operational axis attached there, rather than synthesising a separate
`theme:<id>` node outside the chain.
**Rationale.** B-05 established a measured contract failure: the synthetic
`main_theme` was not a member of `causal_chain.nodes`, so the projection was
constructible but not routable. ONTOLOGY §Theme already fixes `X` as the
observable proxy for `vk`, so making `vk` the routable theme node makes the
projection say what the ontology already says without changing a normative rule.
**Rejected.** Appending a synthetic node after `vk` and extending the chain to
route through it — rejected because the synthetic node carries no transmission
meaning and inflates `k`, which is WF-gated.
**Affected.** `engine/ledger/projection.py`,
`tests/integration/test_ledger_render_projection.py`, `engine/ledger_bridge.py`.

### D-14 — `forward_ingest` returns foldable events, persistence stays opt-in
**Decision.** `runner.forward_ingest` returns each admitted theme's `CREATED`
event and any derived `STATUS_CHANGED` event needed to reflect activation, so
the resulting registry is foldable and queryable as an event-sourced ledger.
Persistence remains opt-in via `LedgerRunConfig.events_store`.
**Rationale.** B-06 identified a mismatch between the ONTOLOGY's event-sourced
contract and the forward re-ingest population path: computing status as a bare
string discarded the event stream required by `fold`, projection, and as-of
queries. Returning the created and derived status events restores parity with
the contract while preserving deterministic tests. Because persistence remains
optional, `recorded_at` is still stamped only in `substrate/store.py` under
invariant I7; the runner does not mint transaction time locally.
**Rejected.** Keeping `forward_ingest` as a status-only summary — it leaves the
registry non-foldable. Auto-persisting from the runner — rejected because it
would move `recorded_at` ownership out of the store and make persistence
mandatory rather than opt-in.
**Affected.** `engine/ledger/runner.py`, `engine/ledger_entrance.py`,
`tests/integration/test_ledger_admission.py`.
