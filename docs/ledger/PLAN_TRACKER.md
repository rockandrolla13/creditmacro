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
- [ ] `tests/golden/corpus/` (5 synthetic docs + expected_*.json)
- [ ] `tests/golden/wiki/` (curated pages w/ revisions)
- [ ] Gate: `test_ci_harness_catches_planted_violations`

## Phase 1 — event log, fold, as-of queries
- [~] `substrate/events.py`, `substrate/hypothesis.py`, `substrate/identity.py`,
      `substrate/fold.py`, `substrate/store.py`, `substrate/queries.py` (stubs)
- [ ] Gates: as_of_exact_states, no_retroactive_mutation,
      fold_order_invariance (property), direction_consistency

## Phase 2 — wiki extractor + revision replayer (4 curated themes only)
- [~] `wiki/wiki_import.py`, `wiki/breadcrumbs.py` (stubs)
- [ ] Gates: golden_revisions, unparseable_routes_to_queue

## Phase 3 — Pass A extractor (blind)
- [~] `ingest/claim.py`, `ingest/pass_a.py` (stubs)
- [ ] Gate: golden_claims_exact (+ I2 import check green)

## Phase 4 — Pass B mapper + evidence ledger
- [~] `ingest/link.py`, `ingest/pass_b.py` (stubs)
- [ ] Gates: seam_extract_to_map, axis_flip_remap

## >>> HOLISTIC REVIEW CHECKPOINT (sign conventions) — after Phase 4
- [ ] `docs/ledger/SIGN_AUDIT.md`

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
