# Claude Code — Autonomous Build Prompt: Theme Surveillance Engine

> Paste this whole file as the prompt to Claude Code, run from the **engine repository root** (the
> directory containing `engine/`, `wiki/`, `tests/`, `docs/`). It assumes the **blueprint** skills are
> installed and available (`ideate`, `architect`, `design`, `scaffold`, `refactor`, `plan-tracker`,
> `code-review`, `review-architecture`, `review-depth`) along with the commands (`/full-build`,
> `/execute-plan`, `/test`, `/review-cycle`, `/scout`, `/map`, `/extend`).

---

## MANDATE — read first, applies throughout

Build the **entire** plan in `SURVEILLANCE_BUILD_PLAN.md` end-to-end, **autonomously**. **Do not ask me
for permission or approval at any point.** Do not stop at phase boundaries to confirm. Make every
decision yourself and record it; the decisions the blueprint skills would normally gate on are
**pre-resolved in §12 of the plan** — apply them directly.

**This overrides the blueprint skills' default gates.** Specifically:

- `plan-tracker` Mode 1 says "Do NOT begin execution until the user approves" → **ignore**: create the
  plan file and immediately begin execution.
- `/full-build` and `/build` gate each phase ("Gate: I approve…") → **ignore the gates**: proceed
  IDEATE→ARCHITECT→DESIGN→SCAFFOLD without stopping; log each phase's decision to the plan.
- `/execute-plan` says "If no tests cover affected code, stop and ask" → **never stop**: the plan
  already specifies the tests (§5.10, §3, §10). Write the test file **before** the implementation for
  each unit so coverage always exists, then make it pass.
- `plan-tracker` Mode 2 / on `FAILED` / on invariant failure says "ask the user" → **apply the plan's
  §12.0 autonomy policy instead**: one fix-forward attempt; if still red, mark the step `BLOCKED` with
  the failing command + output in the Execution Log and move to the next independent step. Continue.

The **only** reason to stop and message me is a genuinely irreversible/destructive action (force-push,
history rewrite, deleting the wiki) — none are required here. Otherwise: keep going until done, then
report completion with the demonstration in §"FINISH" below.

Still honor the non-negotiables: the **Intent Declaration** before each code change, the **STATE block**,
and the **eight invariant checks after every step** (plan §11). These are discipline, not gates — they
never require my input.

---

## STEP 0 — Orient (no gates)

1. Confirm you are in the right repo: `engine/workflow.py` and
   `tests/integration/test_golden_master.py` exist. If not, stop and tell me the cwd is wrong.
2. Read, in order: `SURVEILLANCE_BUILD_PLAN.md` (the spec — especially §0, §11, §12, §13), then
   `docs/SPEC_AND_STATE.md`, `docs/THEME_DISCIPLINE_AND_FAILURE_MODES.md`.
3. `/scout` (or `/map`) the `engine/` package to ground yourself in the real module layout, then
   reconcile against the plan's §0.5 integration map. Note any path drift in the Execution Log; trust the
   **status tags** over any README.
4. Capture the pre-execution snapshot: `pytest -q` (record pass/fail counts), `.py` file count, line
   count. This is the baseline `plan-tracker` Verify will diff against.

## STEP 1 — Create the tracked plan (then immediately proceed)

Use `plan-tracker` (Mode 1) to write `PLAN-surveillance.md` at the repo root:

- **Phases** = the plan's Phase 0 → Phase 6, in the §1 sequencing (spine-first per §12.1):
  `L1,L2,L3,L4,L5 → P1 persistence → P3 surveillance → P2 compression → P4 ingestion → P5 hardening →
  P6 calibration`. One table row per buildable step; each step small enough for one turn and leaving the
  tree green.
- **Invariants table** = copy the plan's §11 block **verbatim** (the eight check commands).
- **Verification Criteria** = the plan's §13 "Done when" list.
- Record the pre-execution snapshot from Step 0.

Do **not** ask "ready to begin?" — begin.

## STEP 2 — Build each phase (architecture-first, autonomous)

For every phase, follow this loop without gating:

1. **STATE + Intent Declaration** (`INTENT / NOT DOING / AFFECTED FILES / VERIFY BY`).
2. **New modules** (`engine/surveillance.py`, `engine/surveillance_agent.py`, `engine/compression.py`,
   `engine/news_critic.py`, and the stubs in `engine/stage0.py` / `engine/outcomes.py`): run the
   `/full-build` chain — `architect` (rate-of-change decomposition, DAG check) → `design`
   (protocols, file structure, wiring) → `scaffold` (typed stubs, import smoke test). Apply §12's
   resolved decisions where a skill would otherwise gate. The plan already gives you the schemas and the
   §5.3 transition function — implement them as specified, not from scratch.
3. **Surgical refactors** (L1–L5, the `forward_horizon` field, the `WikiIntegrator` persistence path):
   edit the minimum. Reuse existing seams — the **current-input seam** (`engine/protocols.py`) for new
   evidence, the **no-trade guard** (`engine/wiki_integration.py`), the freeze→additive
   `PostCaseCalibration` pattern (`engine/firewall.py`) for the watch annotation stream.
4. **Tests first, per unit.** Write the test file from the plan (§5.10 is the centrepiece —
   property-based via Hypothesis for the pure `transition()` and the guardrail formulas; characterization
   for the agent and persistence) **before** filling the implementation body, then `/execute-plan`-style
   fill the body until the test passes. Use `/test` to generate any property tests the plan leaves
   implicit (pure functions with type hints → `st.from_type`).
5. **Invariant gate after every step** (plan §11, all eight). Update the `plan-tracker` step status
   (`PENDING → IN PROGRESS → DONE`), record the commit hash, append a timestamped Execution Log entry.
   On red: §12.0 policy (one fix-forward, else `BLOCKED` + continue). **Never cross a phase boundary
   with a red tree.**
6. Commit after each step.

**Hard rules carried from the plan (enforce as invariants, do not violate):**

- `tests/integration/test_golden_master.py` numerics are **byte-identical** throughout — **never edit
  that file**; gate on it after every step. Compression and surveillance go in the **discovery flow**
  (`run_workflow` / `DiscoveryRunnerAgent`), **never** the scripted `runner.run_case` expression path.
- New `ThemeObject` fields are **Optional with defaults** (protects `FrozenSnapshot`).
- The method/case memory gate, the discovery/expression fence, and the temporal fail-closed stay intact.
- **No legs / sizing / hedge ratios** emitted anywhere. The watch outputs alerts only.
- Determinism: no wall-clock; `now` is always supplied; stable ordering.
- The Python `transition()` must reproduce the reference simulator's routing
  (`theme_surveillance_simulator.html`) exactly — it is the executable spec.

## STEP 3 — Review pass (autonomous)

After the spine (P0→P3) and again at the end, run `/review-cycle` (`review-architecture` +
`code-review` → `refactoring-plan`). Apply only the findings that don't risk an invariant; defer the
rest into the plan's Notes. Do not gate.

## FINISH — Verify, demonstrate, report

1. **`plan-tracker` Verify (Mode 3):** completion check, diff summary vs the Step-0 snapshot, **active**
   verification (actually run `pytest -q`), and the architecture before/after if scored. Append the
   `## Verification Report` to `PLAN-surveillance.md`. Target verdict: `COMPLETE`.
2. **Run the plan's §13 demonstration**, capturing output into the Execution Log:
   - full suite + the §11 invariant commands all green;
   - end-to-end **discover → persist** on the PPI/CPI fixture, then show the routed CASE page in `wiki/`;
   - a **surveillance run**: feed a tick sequence and show the state path
     (`armed → falsified_pending → (whipsaw) confirming → … → falsified`), then a target-hit sequence →
     `played_out`;
   - the **closed** CASE page with its `ThemeOutcomeRecord`.
   - If no CLI entrypoint exists, build a thin one (`engine/cli.py` or a `demo/` script + a
     `demo/ppi_cpi_ticks.jsonl` fixture) using the real `run_workflow` / agent APIs — you may add files.
3. **Report done** with: the `## Verification Report` (verdict + N/N steps DONE + all invariants green),
   the wiki showing the PPI/CPI theme **routed → watched → closed**, and the demonstrated state path.
   Phrase it as: *"Build complete. PLAN verdict COMPLETE, N/N steps DONE, eight invariants green. Wiki:
   PPI/CPI theme routed → watched → closed. Surveillance path demonstrated end-to-end. Verification
   report and closed CASE page below."*

Begin now at Step 0. Do not wait for confirmation.
