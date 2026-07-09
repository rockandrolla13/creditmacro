# SESSION SUMMARY — Theme Hypothesis Ledger build

Branch `theme-hypothesis-ledger` · PR #1 · built inside `engine/ledger/` (not a
`src/` twin), reusing schema / memory firewall / surveillance / provider seams /
firewall.freeze / discovery.

## Outcome
All 7 phases + the sign-audit checkpoint complete under strict TDD (test written and
watched fail before each implementation). **73 ledger tests; full repo suite 849
passed** (2 pre-existing `fitz`-import errors excluded, unrelated). Tier-1 CI (7
grep/AST invariants) green. SIGN_AUDIT clean.

## Phases (each gate green)
| Phase | Deliverable | Gates |
|-------|-------------|-------|
| 0 | vocab + crosswalk, constants, governance docs, Tier-1 CI harness | harness catches planted violations |
| 1 | event log, fold (sole constructor), as-of queries, WF, event classifier | as_of_exact_states, no_retroactive_mutation, fold_order_invariance, direction_consistency |
| 2 | wiki extractor + revision replayer (4 curated only) | golden_revisions, unparseable_routes_to_queue |
| 3 | Pass A blind extractor | golden_claims_exact + I2 firewall |
| 4 | Pass B mapper + append-only evidence ledger | seam_extract_to_map, axis_flip_remap |
| — | **SIGN AUDIT** | 8 sites; CR-BUG-001 + CR-BUG-002 fixed |
| 5 | pure scoring view S_θ/B_θ | score_order_invariance, novelty_and_caps, score_is_pure |
| 6 | orphan clustering + admission + end-to-end pipeline | end_to_end_golden |
| 7 | wiki renderer + drift + projection bridge | render_parse_roundtrip, projection_roundtrip |

## Deltas (ONTOLOGY_DELTA.md)
- D-01 relocate build to `engine/ledger/` (no `src/` twin)
- D-02 Tier-1 enforcement via grep+AST (no import-linter dep)
- D-03 population path = forward re-ingest (WF spike: 82/86 pages fail WF)
- D-04 `wiki_import` scope = the 4 WF-surviving curated themes
- D-05 ONTOLOGY amendments A1–A3 + fixes F1–F2 (reconcile with existing engine)
- D-06 constants as module-level names; runtime config Pydantic
- D-07 **polarity carries sign(X)** (SIGN_AUDIT CR-BUG-001)
- D-08 deterministic mechanism-synthesis rule for admission

## Blocked items (BLOCKED.md) — resolved behind named constants
- B-01 Pass B match_confidence calibration (τ_ORPHAN; scripted-provider gates)
- B-02 embedding provider (bow_cosine seam via `textsim`)
- B-03 tracked-axis registry membership (seeded, review-gated)

## Sign audit (docs/ledger/SIGN_AUDIT.md)
8 sign sites; 6 exact. CR-BUG-001 (Major): ONTOLOGY §EvidenceLink omitted sign(X) —
code correct, spec amended (D-07). CR-BUG-002 (Minor): `axis_sign` KeyError → guard.

## Known stubs (by design, not oversight)
`wiki/wiki_import` full 82-page path (superseded by forward re-ingest), `lifecycle.py`
surveillance→FALSIFIED wiring, `queries.valid_over`, and the LLM prose providers
(Pass A / Pass B / wiki extractor) behind their deterministic seams. These are the
next increments; the substrate, ingest, scoring, admission, render, and projection
paths are complete and tested.
