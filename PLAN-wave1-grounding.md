# Plan: wave1-grounding

**Integration branch:** orch/wave1-grounding

> **Orch execution plan — wave 1 of 3.** Derived from `PLAN-authoritative-harness.md` Phase 1
> and the confirmed defect set in `engine/ledger/`. Waves 0 and 2 are deliberately NOT in this
> file: both are solo and both contain decisions, which a parallel DAG cannot encode.

## Preconditions — wave 1 MUST NOT run until all four are true

Wave 0 is solo work. Running this plan before it lands will produce four agents inventing four
incompatible contracts.

1. **`engine/schema/grounding.py` exists and is frozen.** It declares `GroundingVerdict` and
   `Number`. This is the shared contract tasks 1.1 and 1.2 build against. Neither task owns it
   and neither may edit it — that is what stops the two halves of the kernel from diverging.
2. **`EvidenceAtom` is frozen** (`engine/schema/probability.py`). Grep found zero mutation
   sites, so this should be a one-line change; the full suite passing is the proof.
3. **Fabricated placeholders replaced with nulls** in `engine/ledger/projection.py`
   (`current_value`, `AxisHistory.mean/vol/percentile`, `Provenance.confidence`) so "no data"
   stops rendering as "measured zero".
4. **Tier A/B/C grounding distribution measured** over ≥5 real files in `markdowns/`. If Tier C
   (loose, human-gated) is a large share, D1's human gate is the bottleneck and the tier
   thresholds in task 1.1 need revisiting before it runs.

## Why these five tasks and no others

File-disjoint by construction. 1.1 and 1.2 create new files only. 1.3 and 1.4 touch
`engine/ledger/`, which has **zero production callers** — all live references are tests, and the
golden master does not reach it, so a bad merge there breaks nothing that runs.

1.1 and 1.2 are pinned to the **same agent** on purpose. The kernel is meant to be one
definition of "is this text in the source"; splitting it across models produces two dialects of
that definition. 2.1 is pinned to a **different** agent from the authors of 1.1/1.2, so the
verification is genuinely independent rather than the author marking its own work.

## Phase 1: Kernel and ledger fixes

| # | Task | Files | Depends | Agent | Category | Status | Evidence |
|---|------|-------|---------|-------|----------|--------|----------|
| 1.1 | Create engine/grounding/__init__.py, a pure dependency-free grounding kernel. Build class SourceIndex(markdown) exposing find_span(quote) -> Optional[tuple[int,int]] returning character offsets into the source text. Match in exactly two tiers: exact substring first, then a normalized match that collapses runs of whitespace and folds curly quotes and en/em dashes to ASCII. NO fuzzy, semantic or edit-distance matching under any circumstances - an approximate match is NOT grounding and must return None, because a near-match is exactly what a fabricating model produces. Import nothing from engine except engine.schema.grounding, which is already frozen; read GroundingVerdict from there and do NOT modify it. No wall-clock calls anywhere: any current time is a parameter. Write tests/unit/test_grounding.py covering an exact hit, a normalized hit via curly quotes, a normalized hit via collapsed whitespace, an en-dash variant, and an absent quote returning None. Run pytest -q and leave the full suite green. | engine/grounding/__init__.py, tests/unit/test_grounding.py |  | claude | codegen | PENDING |  |
| 1.2 | Create engine/grounding/numbers.py, a pure unit-aware numeric tokenizer. Import nothing from engine except engine.schema.grounding, which is already frozen; read the Number model from there and do NOT modify it. Provide numbers_in(text) -> list[Number] recognising decimals, thousands separators such as 1,250, signed values, ranges such as 120-140bp including the en-dash form, and the units bp, %, $ and x. Store BOTH forms for every token: the raw source substring exactly as written, and a canonical float value plus a normalized unit string. Downstream comparison uses the canonical value; display defaults to raw. Do NOT import engine/grounding/__init__.py - it is being written in parallel by another agent and will not exist in your worktree. Write tests/unit/test_grounding_numbers.py covering each unit, a range, a thousands separator, a negative value, a bare decimal, and text containing no numbers at all. Run pytest -q and leave the full suite green. | engine/grounding/numbers.py, tests/unit/test_grounding_numbers.py |  | claude | codegen | PENDING |  |
| 1.3 | Fix the timestamp comparison in engine/ledger/substrate/store.py. events_as_of currently filters with a raw ISO STRING comparison, e.recorded_at <= t_x, which is wrong in two distinct ways. A date-only cutoff such as 2026-08-09 lexically precedes 2026-08-09T21:30:00Z, so every event recorded that day is silently excluded. And a timestamp carrying a non-UTC offset compares lexically rather than instant-wise, so genuinely future events are admitted - a lookahead leak in a store whose entire purpose is bitemporal honesty. Parse both sides into timezone-aware UTC datetimes before comparing; treat a date-only cutoff as end-of-day UTC; treat a naive timestamp as UTC. This is a READ-path fix only: keep the store append-only and keep the JSONL on disk byte-compatible, changing nothing about what is written. Write tests/unit/test_ledger_store_temporal.py proving a date-only cutoff now includes same-day events and that an event in the future relative to a non-UTC cutoff is excluded. Run pytest -q and leave the full suite green. | engine/ledger/substrate/store.py, tests/unit/test_ledger_store_temporal.py |  | codex | codegen | PENDING |  |
| 1.4 | Two independent correctness fixes in the ledger scoring path. First, in engine/ledger/ingest/scoring_view.py the helper _decay divides by horizon_days/2.0 and raises ZeroDivisionError whenever horizon_days is 0; guard it so a zero or negative horizon yields no decay credit rather than crashing, and state the chosen semantics in the docstring. Second, in engine/ledger/runner.py the activation gate reads abs(sv.S) >= ACTIVATION_ABS_SCORE_MIN, which means a theme with score -4 and breadth 2 activates on evidence that CONTRADICTS it, identically to supporting evidence; change the condition to require a positive score so only confirming evidence can activate a theme. Do NOT change any value in engine/ledger/constants.py - the constants are correct, the comparison is not. Write tests/unit/test_ledger_activation.py proving that S=-4 with B=2 does not activate, that S=+4 with B=2 does activate, and that horizon_days=0 does not raise. Run pytest -q and leave the full suite green. | engine/ledger/ingest/scoring_view.py, engine/ledger/runner.py, tests/unit/test_ledger_activation.py |  | gemini | codegen | PENDING |  |

## Phase 2: Independent verification of the merged kernel

| # | Task | Files | Depends | Agent | Category | Status | Evidence |
|---|------|-------|---------|-------|----------|--------|----------|
| 2.1 | Adversarially verify that the two halves of the grounding kernel actually compose. engine/grounding/__init__.py providing SourceIndex.find_span and engine/grounding/numbers.py providing numbers_in were written in parallel by separate agents against the frozen contract in engine/schema/grounding.py; they merged cleanly, which proves only that they do not collide, not that they agree. Write tests/integration/test_grounding_integration.py that builds a SourceIndex over a REAL file from the markdowns directory, locates genuine verbatim quotes taken from that file, and asserts numbers_in over the returned span recovers exactly the numbers present in that text. Then try hard to BREAK it: assert that a paraphrase of a real sentence does NOT ground, that a verbatim quote taken from a DIFFERENT source file does NOT ground, and that a number absent from a span is never reported as present. Critically, do NOT modify anything under engine/ - if the two modules disagree about the Number contract or about span boundaries, write a FAILING test that documents the mismatch precisely rather than patching either module, because a patch here would hide the divergence this task exists to find. Run pytest -q. | tests/integration/test_grounding_integration.py | 1.1, 1.2 | codex | test | PENDING |  |
