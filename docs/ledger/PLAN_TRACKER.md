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

## >>> HOLISTIC REVIEW CHECKPOINT (sign conventions) — after Phase 4
- [ ] `docs/ledger/SIGN_AUDIT.md` (running now)

## Phase 5 — scoring view
- [~] `ingest/scoring_view.py` (stub)
- [ ] Gates: score_order_invariance (property), novelty_and_caps, score_is_pure

## Phase 6 — orphan clustering + admission
- [~] `ingest/admission.py`, `lifecycle.py` (stubs)
- [ ] Gate: end_to_end_golden

## Phase 7 — wiki renderer + drift detection
- [~] `wiki/render.py`, `wiki/review_queue.py`, `projection.py`, `runner.py` (stubs)
- [ ] Gates: render_parse_roundtrip, projection_roundtrip (added — bridges to engine/)

## Status
Phase 0 foundation committed. Phases 1–7 are stubs awaiting TDD implementation
(gate tests first, per BUILD_PROMPT session rules).
