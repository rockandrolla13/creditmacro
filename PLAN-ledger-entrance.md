# Plan: ledger-entrance

**Integration branch:** orch/ledger-entrance

> **Path B, wave 1.** Wire the Theme Hypothesis Ledger into the discovery workflow and prove
> ONE real corpus document goes `document → claims → theme → routed strategy families`.
> Nothing here extracts a shared substrate for a second project; that decision waits until
> this seam carries a real document end to end.

## The fact this plan exists to fix

`engine/ledger/**` (~20 modules, ~2000 lines) is imported by nothing in production. Its 15
test files and `tools/ledger_invariants.py` are the only importers. The designed bridge,
`engine/ledger/projection.py::to_theme_object`, has **zero** production callers. The ledger
tests pass because the tests call it directly.

Two concrete breaks stand between the ledger and `run_workflow`, both **measured, not
inferred**:

1. **The projected object is not routable.** Calling
   `engine/workflow.py::_validate_causal_chain` on a real `to_theme_object` output raises
   *"EXPAND_CAUSAL: main_theme must be one of the chain's nodes"* — projection synthesises
   `main_theme.id = "theme:<theme_id>"` while the chain carries vocabulary node ids. Nothing
   caught this because projection builds its `ThemeObject` directly instead of going through
   the workflow. → **BLOCKED B-05**.
2. **There is nothing to project.** `runner.forward_ingest` returns
   `AdmittedTheme(theme_id, status_string)` and discards `AdmissionOutcome.created_event`. It
   computes activation without emitting the `STATUS_CHANGED` event §Lifecycle requires. So the
   population path produces a registry that cannot be folded, and `fold` is the sole permitted
   constructor of a `ThemeHypothesis` (I5). → **BLOCKED B-06**.

A third question — whether the workflow setting `strategy_family_routed` is a second
status-axis mapping under AMEND A3 — is **BLOCKED B-07**. The plan implements the proposed
reading (it is not a mapping, because the workflow never reads the market-truth axis) behind
the named guard `LedgerProjectionNotRoutable`. It is recorded, not silently chosen.

## Governing documents — every agent must read these before editing

`docs/ledger/ONTOLOGY.md` is **NORMATIVE and wins every conflict**. Wave 1 of the grounding
build went wrong precisely because four parallel agents were never handed it. Each task below
names the sections that bind it. Also binding: `CLAUDE.md` (four discipline gates; discovery
never emits legs, sizing or hedge ratios) and `PLAN-authoritative-harness.md` (invariants I1,
I6, I8).

## Hard constraints — violating any of these fails the task

- **Never edit `tests/integration/test_golden_master.py`.** Its numerics stay byte-identical.
  It is gated after **every** task, not only at the end: each task below finishes with
  `python -m pytest -q` green, and the golden master runs inside that suite. A task that
  cannot leave the suite green stops and reports rather than merging — the conductor reverts
  a merge that breaks the merged tree, and a red phase boundary blocks every task downstream.
- **Never modify `markdowns/`** — immutable raw sources.
- **Never change a value in `engine/ledger/constants.py`.** That is an ONTOLOGY change
  requiring an `ONTOLOGY.md` §Constants edit plus an `ONTOLOGY_DELTA.md` entry — never a local
  override.
- **Any new field on a frozen model is `Optional` with a default** (I6), and excluded from
  `engine/firewall.py::_HASH_EXCLUDE` only if it can vary between two runs of identical
  reasoning. This plan adds **no** field to `ThemeObject`: the ledger link lives on the
  `LedgerDiscoveryResult` wrapper instead, so no snapshot hash moves.
- **No wall clock in any module touched here** (I8). `as_of` is a parameter; `recorded_at` is
  stamped only inside `substrate/store.py` (I7).
- Every task ends with `python -m pytest -q` green and reports the count. Baseline **914**,
  measured on the integration branch point (898 before this wave; +6 from
  `tests/unit/test_ledger_bridge_scaffold.py`, +10 from the D-09..D-12 defect fixes that
  landed alongside it). **`ONTOLOGY_DELTA.md` now ends at D-12** — task 3.2 continues from
  D-13 and must not reuse an id.

## Already on master — the scaffold these tasks fill in

- `engine/ledger_bridge.py` — `LedgerProvider`, the discovery-only Provider adapter, plus
  `DISCOVERY_SEAMS` / `EXPRESSION_SEAMS` and `LedgerProjectionNotRoutable`. All seams are
  typed stubs raising `NotImplementedError`.
- `engine/ledger_entrance.py` — `LedgerIngestSpec`, `LedgerDiscoveryResult`,
  `hypotheses_from_registry`, `project_all`, `run_ledger_discovery`. All stubs.
- `tests/unit/test_ledger_bridge_scaffold.py` — 6 passing structural gates.

## Phase 1: unblock the two ends

File-disjoint. 1.1 owns the ledger runner, 1.2 owns the projection; neither imports the other.

| # | Task | Files | Depends | Agent | Category | Status | Evidence |
|---|------|-------|---------|-------|----------|--------|----------|
| 1.1 | Make engine/ledger/runner.py forward_ingest return foldable events. READ docs/ledger/ONTOLOGY.md sections Bitemporal, Lifecycle and Admission FIRST - that document is normative and wins any conflict with this description. Today forward_ingest returns RegistryState containing AdmittedTheme(theme_id, status) where status is a bare string ACTIVE or CANDIDATE, and it throws away AdmissionOutcome.created_event entirely. The ledger is event-sourced: a theme IS a fold over its event stream, and substrate/fold.py is the ONLY permitted constructor of a ThemeHypothesis under invariant I5. So nothing downstream can reconstruct a theme from what forward_ingest returns. Fix this ADDITIVELY. Add an optional created_event field to AdmittedTheme carrying the ThemeEvent that admission already built, and add a second event whenever the activation gate fires: a STATUS_CHANGED event with payload status ACTIVE, because ONTOLOGY section Lifecycle says STATUS_CHANGED events govern the market-truth axis and the runner currently asserts activation without recording it. Give AdmittedTheme a method or the RegistryState a helper returning the ordered event list per admitted theme so a caller can fold it. Do NOT change the existing admitted, orphan_claim_ids, needs_structuring or review_tags fields or their sort order, and do NOT change any value in engine/ledger/constants.py: tests/golden/corpus/expected_registry.json must stay valid unchanged. Do NOT change the activation comparison itself: it now reads abs(sv.S) >= ACTIVATION_ABS_SCORE_MIN per ONTOLOGY_DELTA D-09, and the absolute value is load-bearing. That has a consequence you must get right - a theme with S negative and breadth 2 activates, because ONTOLOGY section Lifecycle calls a contested theme a reportable sub-state of ACTIVE, not dead. So the STATUS_CHANGED payload you emit is exactly status ACTIVE for that case too. Do NOT invent a CONTESTED status value: LifecycleStatus has no such member and fold would raise on it. Persistence is out of scope: write nothing to disk, stamp no recorded_at (invariant I7 reserves that for substrate/store.py) and call no wall clock (invariant I8) - effective_at comes from the claim doc dates exactly as admission already does it. Write tests/unit/test_ledger_runner_events.py proving that forward_ingest over the golden corpus tests/golden/corpus with doc ids gc-003-jpm, gc-004-gs and gc-005-solo yields events that fold via engine.ledger.substrate.fold.fold into a ThemeHypothesis whose theme_id, operational_axis and falsifier match the admitted theme, and whose folded status is ACTIVE - matching expected_registry.json. Also prove a CANDIDATE theme folds to CANDIDATE. Run python -m pytest -q and leave the full suite green. | engine/ledger/runner.py, tests/unit/test_ledger_runner_events.py |  |  | codegen | PENDING |  |
| 1.2 | Make the projected ThemeObject routable by engine/workflow.py. READ docs/ledger/ONTOLOGY.md sections Theme and Rendered view plus AMEND A3 FIRST - that document is normative and wins any conflict with this description. Also read docs/ledger/BLOCKED.md entry B-05, which states this problem and its proposed resolution. engine/ledger/projection.py::to_theme_object builds main_theme as CausalNode(id=f"theme:{theme_id}") while causal_chain carries the vocabulary node ids such as funding_stress, liquidity_premium and credit_spread. engine/workflow.py::_validate_causal_chain requires main_theme.id to be one of the chain node ids, so a projected object raises EXPAND_CAUSAL: main_theme must be one of the chain's nodes the moment it is fed to the discovery workflow. Verify that failure yourself before changing anything. Fix it per B-05: make the TERMINAL node vk of the transmission chain the routable main_theme - kind theme, carrying the projected Axis, axis_operational True - and delete the synthetic theme: node. vk is the node the operational axis X proxies according to ONTOLOGY section Theme, so this makes the code agree with the ontology rather than inventing a rule. Do NOT instead append the synthetic node to the chain: that adds a node with no transmission meaning and inflates k, which is WF-gated. Keep every other projected field identical, keep the A3 status mapping (discovery_complete for CANDIDATE or ACTIVE, blocked otherwise) exactly as it is, and keep the unmeasured fields unset - current_value and AxisHistory stay None because the ledger names an axis and does not observe one. Critically, PRESERVE the empty-mechanism guard added by ONTOLOGY_DELTA D-12 at the top of the function: to_theme_object raises ValueError when theme.mechanism.edges is empty, and your rewrite reads the same edges local, so do not reintroduce an IndexError by moving or dropping that check. tests/integration/test_ledger_render_projection.py must keep passing unchanged; do not edit it. Write tests/integration/test_ledger_projection_workflow_contract.py proving that engine.workflow._validate_causal_chain accepts a real projection output, that main_theme.is_routable() is True, that main_theme.id equals the chain's terminal node, and that engine.firewall.freeze still succeeds on the projected object. Run python -m pytest -q and leave the full suite green. | engine/ledger/projection.py, tests/integration/test_ledger_projection_workflow_contract.py |  |  | codegen | PENDING |  |

## Phase 2: fill in the seam

File-disjoint. 2.1 owns the adapter, 2.2 owns the two pure halves of the entrance. Neither
task writes `run_ledger_discovery` — that is phase 3, so the two agents cannot both claim the
orchestration.

| # | Task | Files | Depends | Agent | Category | Status | Evidence |
|---|------|-------|---------|-------|----------|--------|----------|
| 2.1 | Implement every seam of LedgerProvider in engine/ledger_bridge.py. The file already exists on master as a typed scaffold: read its module docstring, which states the three design rules, and follow them exactly. READ docs/ledger/ONTOLOGY.md AMEND A3 and CLAUDE.md's four discipline gates FIRST. Each seam is a projection of the ThemeObject the adapter was constructed with, and the per-method TODO comments already state what to return. The load-bearing one is diagnose_loops: engine/workflow.py promotes a theme to strategy_family_routed ONLY when loop_diagnosis.invalidation_evidence is non-empty, which is CLAUDE.md gate 4 - a thesis with no falsifier is not a thesis. The ledger guarantees a non-empty falsifier through WF clause b, and projection parks it in provenance.evidence as the string falsifier: followed by the text. Recover it from there and put it in invalidation_evidence, and set dominant_loop_now and possible_loop_shift to an explicit not diagnosed rather than inventing a loop the ledger never diagnosed; decision is watchlist. propose_scenarios returns an empty list because the ledger prices nothing - families are still routed but confidence is capped, which is the honest answer, not a degraded one. context() returns x_mkt None because the ledger names an axis and does not observe one; derive thesis_sign from the projected thesis direction_of_view. build_system_map, critique_mental_model and critique return None or empty. DO NOT add enumerate_expressions, size_and_risk or assess_trap_implications: their absence is what makes run_workflow reject expression mode for a theme with no observed mark, and tests/unit/test_ledger_bridge_scaffold.py asserts they are absent - that test must keep passing unchanged. Do not edit engine/workflow.py, engine/protocols.py or engine/ledger/projection.py. Write tests/unit/test_ledger_bridge_provider.py proving that run_workflow with a LedgerProvider in discovery mode reaches status strategy_family_routed with at least one strategy family, that the routed families carry no legs or sizing, that a provider whose falsifier is missing yields discovery_complete instead of routed, and that run_workflow in expression mode raises expression_mode_not_supported. Run python -m pytest -q and leave the full suite green. | engine/ledger_bridge.py, tests/unit/test_ledger_bridge_provider.py | 1.2 |  | codegen | PENDING |  |
| 2.2 | Implement hypotheses_from_registry and project_all in engine/ledger_entrance.py, and NOTHING ELSE in that file - leave run_ledger_discovery raising NotImplementedError, because task 3.1 owns it. The file already exists on master as a typed scaffold; read its module docstring first, and read docs/ledger/BLOCKED.md entry B-06. hypotheses_from_registry takes the RegistryState that task 1.1 has just taught to carry events, collects each admitted theme's ordered events, and folds them via engine.ledger.substrate.fold.fold into a ThemeHypothesis. Never construct a ThemeHypothesis directly: fold is the sole permitted construction site under invariant I5, and tools/ledger_invariants.py enforces it - run that script before you finish and leave all Tier-1 invariants holding. A theme whose events fold to None has no CREATED event and is dropped, not defaulted. Walk ONLY the admitted list: needs_structuring and orphan_claim_ids are claims that never became themes - ONTOLOGY_DELTA D-11 now routes a directionally contested cluster there, and folding one would manufacture a theme the admission gate refused. project_all maps each hypothesis through engine.ledger.projection.to_theme_object, which is the ONLY site permitted to map between the three status axes under ONTOLOGY AMEND A3 - do not replicate any part of that mapping here, and do not import LifecycleStatus into this module. Call no wall clock (invariant I8): as_of is already a parameter. Do not edit engine/ledger/runner.py, engine/ledger/projection.py or engine/ledger_bridge.py. Write tests/unit/test_ledger_entrance_fold.py proving that a registry from forward_ingest over the golden corpus tests/golden/corpus folds to exactly one ThemeHypothesis with status ACTIVE, that project_all turns it into a ThemeObject whose id is the ledger theme id, and that a registry with no admitted themes yields an empty list rather than raising. Run python -m pytest -q and leave the full suite green. | engine/ledger_entrance.py, tests/unit/test_ledger_entrance_fold.py | 1.1 |  | codegen | PENDING |  |

## Phase 3: the end-to-end proof, and the governance record

3.1 and 3.2 are file-disjoint: one is code, one is documentation.

| # | Task | Files | Depends | Agent | Category | Status | Evidence |
|---|------|-------|---------|-------|----------|--------|----------|
| 3.1 | Wire run_ledger_discovery in engine/ledger_entrance.py and prove one real corpus document reaches ranked strategy families. Read the function's existing TODO block, which states the five steps in order: forward_ingest, hypotheses_from_registry, project_all, then per projected object construct a LedgerProvider from engine.ledger_bridge and call engine.workflow.run_workflow in discovery mode, collecting a LedgerDiscoveryResult for each. Refusals are RESULTS, not exceptions: catch LedgerProjectionNotRoutable and record it in refused_reason with routed left None, because a run over five documents that routes two themes and refuses three must say so - silently returning two is how a gate stops being visible. Keep the spec.persist_events path optional and OFF by default so gate tests stay deterministic; when it is on, append through engine.ledger.substrate.store.JsonlEventStore and let it stamp recorded_at, which invariant I7 reserves to that module. Call no wall clock anywhere (invariant I8). Do not add any field to ThemeObject: the ledger link belongs on the LedgerDiscoveryResult wrapper, because ThemeObject is frozen behind engine/firewall.py::freeze and a ledger id varies between two runs of identical reasoning. Do not edit engine/workflow.py, engine/ledger_bridge.py, engine/ledger/runner.py or engine/ledger/projection.py. Write tests/integration/test_ledger_to_discovery_e2e.py running the whole path over the golden corpus tests/golden/corpus with doc ids gc-003-jpm, gc-004-gs and gc-005-solo, and assert the full chain: exactly one theme is admitted and ACTIVE, matching tests/golden/corpus/expected_registry.json; it projects to a ThemeObject; it routes to status strategy_family_routed with at least one StrategyFamilyRec; the memo names the family; and the result carries the ledger theme id. Then assert the discipline boundary holds - the routed object has no expressions, no sizing, no pricing and no pm_gate, because discovery stops at ranked strategy families. Finally assert tests/integration/test_golden_master.py still passes untouched; do not edit that file under any circumstances. Run python -m pytest -q and leave the full suite green. | engine/ledger_entrance.py, tests/integration/test_ledger_to_discovery_e2e.py | 2.1, 2.2 |  | codegen | PENDING |  |
| 3.2 | Record the governance trail for this wave in the three ledger documents, changing no code. Read docs/ledger/ONTOLOGY.md, docs/ledger/ONTOLOGY_DELTA.md, docs/ledger/BLOCKED.md and docs/SPEC_AND_STATE.md part 1.8 first - the protocol there is that every decision not derivable from the specification is recorded at the moment it is made, with decision, rationale, alternatives rejected and files affected, and that changing a constant is a specification change and never a local override. Append two numbered entries to docs/ledger/ONTOLOGY_DELTA.md, continuing the existing D-NN numbering without reusing an id: one recording that the terminal node vk of the transmission chain is the routable main_theme in projection (the B-05 resolution, with the rejected alternative of appending a synthetic node to the chain and why it was rejected - it inflates k, which is WF-gated), and one recording that forward_ingest returns the CREATED and derived STATUS_CHANGED events so the registry is foldable (the B-06 resolution, noting that persistence stays opt-in so recorded_at is still stamped only in substrate/store.py under invariant I7). Then update the Status lines of B-05 and B-06 in docs/ledger/BLOCKED.md to say resolved, naming the delta ids, and leave B-07 OPEN with its proposed reading marked as implemented behind LedgerProjectionNotRoutable - it is a question for a human, not a decision for an agent. Then update docs/ledger/PLAN_TRACKER.md with a new section for this wave listing what landed. Do NOT edit docs/ledger/ONTOLOGY.md itself: neither resolution changes a normative rule, and if you conclude one does, stop and say so in your report rather than amending the normative document. Do NOT edit docs/SPEC_AND_STATE.md - the main session owns it. Change no file under engine/ or tests/. | docs/ledger/ONTOLOGY_DELTA.md, docs/ledger/BLOCKED.md, docs/ledger/PLAN_TRACKER.md | 1.1, 1.2 |  | docs | PENDING |  |
