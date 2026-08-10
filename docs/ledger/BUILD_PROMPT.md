# BUILD_PROMPT — Theme Hypothesis Ledger (Alaph Stage 1 substrate)

> **Relocation note (2026-07-07).** This build prompt originally targeted a
> `src/themes` / `src/ingest` / `src/vocab` tree. Per `ONTOLOGY_DELTA.md`
> D-01 the build lives in **`engine/ledger/`** and reuses the existing
> `engine/` modules (schema, memory firewall, surveillance_agent,
> llm_provider, firewall.freeze, discovery). All Tier-1 paths below are
> retargeted accordingly. Where this prompt and `ONTOLOGY.md` conflict,
> ONTOLOGY wins.

## Session rules
- AUTONOMOUS MODE: do not stop for approval at default gates. Stopping
  conditions: (a) a phase gate test fails twice after a fix attempt,
  (b) a Tier-1 CI check cannot be satisfied without violating an invariant,
  (c) all phases complete.
- START of every phase: re-read the `ONTOLOGY.md` sections for that phase
  and the phase's gate test files. Completed code + passing gates are the
  contract.
- BLOCKED-ITEM PROTOCOL: append to `BLOCKED.md`, implement the proposed
  resolution behind a named module-level constant, continue. Never silently
  choose.
- DELTA PROTOCOL: any decision not derivable from `ONTOLOGY.md` is appended
  to `ONTOLOGY_DELTA.md` at the moment it is made.
- Gate tests are written and committed BEFORE the implementation they gate.

## Tier-1 invariants (enforced by construction — `tools/ledger_invariants.py`)
- I1  Theme scores are never stored. `score(theme_id, as_of)` is a pure
      function over the EvidenceLink ledger.
      CI: no `score.*: *float` field in `engine/ledger/substrate/hypothesis.py`.
- I2  Pass A (claim extraction) is blind to the theme registry.
      CI: `engine/ledger/ingest/pass_a.py` (and module) MUST NOT import
      `engine.ledger.substrate`.
- I3  Pass B sees theme DEFINITIONS only (ThemeDefinitionView: mechanism,
      shock_direction, operational_axis, horizon — no ledger, no scores).
      Polarity is COMPUTED as claim.direction × d(θ), never LLM-emitted.
      CI: no `EvidenceLink` in `ingest/pass_b.py` prompt builders; no
      `polarity` in `ingest/prompts/`.
- I4  EvidenceLink and ThemeEvent stores are append-only. Corrections are
      new rows with `supersedes` set. No UPDATE/DELETE paths exist.
- I5  ThemeHypothesis is frozen and has no public constructor outside the
      fold module. Themes exist only as folds over ThemeEvent.
      CI: `ThemeHypothesis(` occurs only in `substrate/fold.py` + tests.
- I6  No `predicted_direction` FIELD anywhere. d(θ) = σ · Π s is derived.
- I7  `recorded_at` set by the persistence layer only. Backdating
      `effective_at` only when provenance == "wiki_import" + a source
      revision timestamp exists.
- I8  Well-formedness gate WF(θ): (a) k ≥ 2, (b) decidable falsifier,
      (c) axis in tracked-axis registry, (d) H ≤ 120d, (e) stated direction
      == d(θ). Failing themes route to NEEDS_STRUCTURING; never force-admitted.

## Phase DAG (deliverables → gates)
See `PLAN_TRACKER.md` for live status. Phases: 0 vocab/golden/CI · 1 event
log+fold+as-of · 2 wiki import+replayer (4 curated themes) · 3 Pass A blind ·
4 Pass B mapper+ledger · [SIGN AUDIT] · 5 scoring view · 6 orphan+admission ·
7 renderer+drift+projection.

Two gates added beyond the original prompt (bridge to `engine/`):
- `projection_roundtrip` (Phase 7): ThemeHypothesis → ThemeObject → freeze →
  as_of equals the fold — proves ledger and engine are one system.
- Phase 2 scoped to the 4 WF-surviving curated themes (D-04).

## Completion criteria
All phase gates green, all Tier-1 CI green, `SIGN_AUDIT.md` clean,
`ONTOLOGY_DELTA.md` + `BLOCKED.md` current. Final: regenerate
`PLAN_TRACKER.md` and emit a session summary of every delta + blocked item.
