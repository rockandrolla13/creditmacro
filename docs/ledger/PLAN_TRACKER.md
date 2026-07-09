# PLAN_TRACKER.md — Theme Hypothesis Ledger build status

Location: `engine/ledger/` (see `ONTOLOGY_DELTA.md` D-01).
Legend: `[ ]` not started · `[~]` scaffolded (stub + docstring, no logic) ·
`[x]` implemented + gate green.

## Phase 0 — vocabulary, governance, CI harness
- [~] `docs/ledger/ONTOLOGY.md` (patched, normative)
- [~] `docs/ledger/ONTOLOGY_DELTA.md`, `BLOCKED.md`, `BUILD_PROMPT.md`
- [~] `engine/ledger/constants.py` (complete — single source of truth)
- [~] `engine/ledger/vocab.py` (crosswalk skeleton + seed node families; TODO full ~60)
- [~] `tools/ledger_invariants.py` (Tier-1 grep/AST CI harness — runnable)
- [~] `tests/golden/corpus/` (2 docs + expected_claims.json committed; the
      admission-coverage docs + expected_registry.json land in Phase 6)
- [x] `tests/golden/wiki/` (3-revision page, axis-flip page, vibes page)
- [~] Gate: `test_ci_harness_catches_planted_violations` (harness proven to catch
      planted violations manually; automated pytest wrapper still TODO)

## Phase 1 — event log, fold, as-of queries  ✅ (TDD, 27 tests green)
- [x] `substrate/events.py`, `substrate/hypothesis.py`, `substrate/identity.py`,
      `substrate/fold.py`, `substrate/store.py`, `substrate/queries.py`
      (implemented; `queries.valid_over` deferred to Phase 6 — outcome attribution)
- [x] Gate: `test_as_of_exact_states` (tests/integration/test_ledger_as_of.py)
- [x] Gate: `test_no_retroactive_mutation` (byte-identical earlier as-of)
- [x] Gate: `test_fold_order_invariance` (property; tie-break proven to bite)
- [x] Gate: `test_direction_consistency` (WF clause e / I8e)
- [x] Support: append-only store, classify_event decision table, WF clauses a–e

## Phase 2 — wiki extractor + revision replayer (4 curated themes only)  ✅ (TDD, 11 tests)
- [x] `wiki/wiki_import.py`: extract (WF-gated), replay (cosine pre-filter +
      structural), import_curated (CREATED + PriorMassSeed); reuses Phase-1
      equiv / wf_predicate
- [~] `wiki/breadcrumbs.py` (stub — Phase 3, forward re-ingest companion)
- [x] Gate: `test_golden_revisions` (1 CREATED + 1 MECHANISM_REVISED; cosmetic→∅;
      axis-flip→AXIS_REVISED)
- [x] Gate: `test_unparseable_routes_to_queue` (k=1 vibes → NEEDS_STRUCTURING clause a)
- refactor: `substrate/hypothesis.ThemeShape` protocol lets WF validate a
  pre-fold WikiCandidate without constructing ThemeHypothesis (I5 preserved)

## Phase 3 — Pass A extractor (blind)  ✅ (TDD, 7 tests)
- [x] `ingest/claim.py` (AtomicClaim); `ingest/pass_a.py`: ClaimProvider seam,
      ScriptedClaimProvider (deterministic), PassAExtractor (validate domains,
      vocab-tag filter → out-of-vocab review, granularity merge, deterministic ids)
- [x] Gate: `test_golden_claims_exact` (exact market_variable/direction/tags per claim)
- [x] Gate: I2 import firewall wired into pytest + proven to bite on a planted import
- [~] `wiki/breadcrumbs.py` (Phase-3 companion; still stub — needs real corpus wiring)

## Phase 4 — Pass B mapper + evidence ledger  ✅ (TDD, 6 tests)
- [x] `ingest/link.py`: EvidenceLink + JsonlEvidenceLinkStore (append-only, I4/I7)
- [x] `ingest/pass_b.py`: structural pre-match, deterministic node-Jaccard
      match_confidence, τ_ORPHAN routing, polarity = dir × d(θ) × sign(X) (computed,
      I3), theme_revision binding, remap (supersede + re-run on AXIS/MECHANISM revision)
- [x] Gate: `test_seam_extract_to_map` (support +1 / contradict −1 / orphan routed)
- [x] Gate: `test_axis_flip_remap` (sign-flip → superseded + sign-flipped polarity;
      sign(X) proven load-bearing)
- [x] I3 "Pass B definitions-only" wired into tools/ledger_invariants.py

## >>> HOLISTIC REVIEW CHECKPOINT (sign conventions) — after Phase 4  ✅
- [x] `docs/ledger/SIGN_AUDIT.md` — 8 sign sites audited; 6 exact, 2 findings
- [x] CR-BUG-001 (Major): ONTOLOGY §EvidenceLink polarity omitted sign(X) → amended
      + ONTOLOGY_DELTA D-07 (code was already correct)
- [x] CR-BUG-002 (Minor): `axis_sign` KeyError → descriptive ValueError guard (TDD)

## Phase 5 — scoring view  ✅ (TDD, 9 tests)
- [x] `ingest/scoring_view.py`: pure S_θ/B_θ over the link ledger (I1, never stored) —
      decay λ^((t−t_i)/h) with h=H/2, novelty discount (same-inst cosine repeat),
      per-institution cap ±CAP_INST, breadth, prior-mass term, no-lookahead filter,
      superseded-link exclusion
- [x] `engine/ledger/textsim.py`: shared bag-of-words cosine (wiki + scoring use it;
      wiki_import.mechanism_text_cosine now delegates — DRY)
- [x] Gate: `test_score_order_invariance` (property)
- [x] Gate: `test_novelty_and_caps`
- [x] Gate: `test_score_is_pure` (identical output; ledger unmutated)

## Phase 6 — orphan clustering + admission  ✅ (TDD, 7 tests)
- [x] `ingest/admission.py`: cluster_orphans (shared-tag connected components),
      admission gate (N_MIN/I_MIN/W_ADMIT), deterministic synthesis (D-08) + WF,
      founding EvidenceLinks, out-of-vocab → review
- [x] `runner.forward_ingest`: Pass A → Pass B → cluster → admit → score → activate
      (CANDIDATE→ACTIVE on B≥2 ∧ |S|≥2)
- [x] Gate: `test_end_to_end_golden` — corpus → expected_registry.json (funding
      cluster ACTIVE; earnings cluster fails I_MIN, stays orphan)
- [x] admission-coverage golden docs (gc-003/004/005) + expected_registry.json
- [~] `lifecycle.py` still stub — surveillance→FALSIFIED wiring is Phase-6/7 follow-on

## Phase 7 — wiki renderer + drift detection  ✅ (TDD, 5 tests)
- [x] `wiki/render.py`: render (mechanism chain, axis, S_θ/B_θ, per-institution table,
      falsifier, timeline), parse (recovers ThemeHypothesis VIA fold — I5-safe),
      drift_diff (→ analyst-provenance proposed events, never auto-applied)
- [x] `projection.py`: ThemeHypothesis → engine ThemeObject (discovery_complete /
      blocked A3 mapping); builds a connected causal_chain + routable main_theme so the
      object passes the engine's discovery gates and `firewall.freeze` succeeds
- [x] Gate: `test_render_parse_roundtrip` (structured fields recovered)
- [x] Gate: `test_projection_roundtrip` (added) — θ → ThemeObject → freeze + recover;
      ledger and engine proven to be one system

## Status — BUILD COMPLETE
All 7 phases + the sign-audit checkpoint done under TDD. 73 ledger tests green;
full repo suite 849 passed (2 pre-existing fitz-import errors excluded). Tier-1 CI
(7 checks) green. SIGN_AUDIT clean (both findings fixed). ONTOLOGY_DELTA (D-01…D-08)
and BLOCKED (B-01…B-03) current. Remaining stubs by design: `wiki/wiki_import` full
82-page path (superseded by forward re-ingest, D-03), `lifecycle.py` surveillance→
FALSIFIED wiring, `queries.valid_over`, the wiki-prose extractor's LLM path.

## LLM seams wired (2026-07-09, TDD, 5 tests)
- [x] `ingest/pass_a.py::LLMClaimProvider` — Anthropic Messages API, blind (I2),
      default `claude-opus-4-8`, opt-in `ALLOW_LIVE_LLM_DISCOVERY=1`
- [x] `ingest/pass_b.py::LLMMatchScorer` — semantic match_confidence, definitions
      only (I3); `StructuralSemanticMapper(scorer=...)` default stays deterministic
- [x] `ingest/prompts/pass_a_extract.py`, `pass_b_match.py` (no polarity/EvidenceLink)
- [x] `engine/ledger/llm_json.py` — shared Messages-response / JSON extraction
- [ ] BLOCKED B-01: match_confidence calibration harness on the golden corpus
