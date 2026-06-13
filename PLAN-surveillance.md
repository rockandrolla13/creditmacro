# PLAN — Theme Surveillance Engine (tracked execution)

> Tracked plan for `SURVEILLANCE_BUILD_PLAN.md`, executed autonomously per `CLAUDE_CODE_BUILD_PROMPT.md`.
> Branch: `surveillance-build`. Spine-first sequencing (§11 of the plan).

## Spec-gap resolution (recorded; see Execution Log 2026-06-13 #0)

The build prompt references plan sections that do not exist on disk (`§12` pre-resolved decisions,
`§13` done-list, `§0.5` integration map; and `§11` is a one-line summary, not "eight invariant
checks"). Resolved autonomously, per the prompt's "make every decision yourself and record it":

- **Invariants** = plan **§0.2** (6) + prompt hard rules → the 8 concrete gate commands below.
- **Resolved decisions** (stand-in for §12) = plan **§5.4** defaults + **§10** recommendations
  (`breach_mode="consecutive"` default; one falsifier for v1; terminal watch persists as its own
  CASE page per §10 Q6 "Recommended: yes"; `now` always supplied).
- **Done-criteria** = the prompt's **FINISH** demonstration.

## Pre-execution snapshot (Step 0, 2026-06-13)

- `pytest -q`: **722 passed, 1 xfailed** (723 collected).
- engine: **48 .py files / 9,964 lines**. tests: **67 files**.
- Base commit: `3dbc87c` on branch `surveillance-build`.

## Invariants (gate after EVERY step — all must stay green)

| # | Invariant | Gate command |
|---|---|---|
| I1 | Golden master byte-identical | `pytest tests/integration/test_golden_master.py -q` |
| I2 | Full suite green | `pytest -q` |
| I3 | No trades/legs/sizing in new output | `grep -rInE "\b(go (long|short)|hedge ratio|position size|stop[- ]?loss)\b" engine/surveillance*.py engine/compression.py engine/news_critic.py` → no engine-emitted directives |
| I4 | Memory/firewall tests green | `pytest tests/unit/test_memory_firewall.py tests/integration/test_discovery_firewall.py -q` |
| I5 | Determinism (no wall-clock) | `grep -rInE "datetime\.now|date\.today|time\.time" engine/surveillance*.py engine/compression.py engine/news_critic.py` → none |
| I6 | New frozen-model fields Optional w/ defaults | `pytest tests/integration/test_golden_master.py tests/integration/test_discovery_firewall.py -q` (field-set tests) |
| I7 | Temporal firewall intact | `pytest tests/unit/test_temporal_schema.py tests/integration/test_temporal_agent.py -q` |
| I8 | Surveillance core matches the reference simulator (§9 faithfulness) | `pytest tests/unit/test_surveillance.py -q` |

## Phases & steps

Status: ⬜ PENDING · 🔵 IN PROGRESS · ✅ DONE · ⛔ BLOCKED

| Phase | Step | Status | Commit | Notes |
|---|---|---|---|---|
| P3-core | S1 `engine/surveillance.py` — schemas + `SurveillancePolicy` + pure `transition()`/`derive()` (mirrors simulator) + `test_surveillance.py` (§5.10 1-11 pure-core) | ✅ | `b7c3fad` | 16 tests; 722→738; GM intact |
| P0 | S2 L1 `DiscoveryRunnerAgent` wraps `run_workflow` | ⬜ | | `engine/wiki_agents.py`; needs workflow.py read |
| P0 | S3 L2 `WikiLintAgent` orchestrates 14 validators | ✅ | `2f66cd3` | +xfail fix; 738→741, 0 xfailed |
| P0 | S4 L3 aggregator parent-cap + demote-tail + log | ⬜ | | `engine/theme_aggregation.py` |
| P0 | S5 L4 type strategy-family hints to routable Literal | ⬜ | | schema + validator |
| P0 | S6 L5 require `current_date` (fail-closed for discovery) | ⬜ | | `engine/temporal.py`, `workflow.py` |
| P1 | S7 `ForwardHorizon` on `ThemeObject` (Optional default) | ⬜ | | §3.2 |
| P1 | S8 D3a discovery-output persistence → CASE page | ⬜ | | `engine/wiki_integration.py` |
| P3 | S9 `ThemeMonitorAgent` + `BlindScoringContext` blind scorer | ⬜ | | `engine/surveillance_agent.py` |
| P3 | S10 terminal watch → `ThemeOutcomeRecord` + CASE page write-back | ⬜ | | §10 Q6 |
| P2 | S11 `ThemeCompressionAgent` + `AnalystThemeMap` (10 tests) | ⬜ | | `engine/compression.py`; discovery flow only |
| P4 | S12 `parse_research_text` LLM seam (fake-client tested) | ⬜ | | highest risk; deterministic/cached |
| P5 | S13 news critic + memory categorization + sufficiency gate | ⬜ | | `engine/news_critic.py` |
| P6 | S14 `calibration_report`/`edge_realization` | ⬜ | | corpus-gated — may BLOCK pending corpus |
| FINISH | S15 demo CLI + verification report | ⬜ | | `engine/cli.py` or `demo/` |

## Verification criteria (Done when — prompt FINISH)

- Full suite + 8 invariants green.
- Discover → persist on PPI/CPI fixture; routed CASE page in `wiki/`.
- Surveillance run: tick sequence shows `armed → falsified_pending → (whipsaw) confirming → … → falsified`; target-hit → `played_out`.
- Closed CASE page with its `ThemeOutcomeRecord`.

## Execution Log

### 2026-06-13 #0 — Orientation
- Confirmed repo anchors; spec + simulator present. Captured baseline (above).
- Logged spec-gap (missing §12/§13/§0.5; §11 mismatch; §10 "open" vs "pre-resolved" contradiction);
  resolution recorded above. **Decision:** proceed spine-first, decisions-by-documented-default.
- Reconciled module layout vs plan integration map: all target files exist as named
  (`engine/wiki_agents.py`, `engine/theme_aggregation.py`, `engine/temporal.py`, `engine/workflow.py`,
  `engine/wiki_integration.py`, `engine/protocols.py`, `engine/firewall.py`, `engine/outcomes.py`,
  `engine/stage0.py`). New modules to add: `engine/surveillance.py`, `engine/surveillance_agent.py`,
  `engine/compression.py`, `engine/news_critic.py`. No path drift.
- Branch `surveillance-build` created; base commit `3dbc87c` (prior green work + docs/plan).
- **Decision:** `ForwardHorizon` defined in `engine/surveillance.py`, imported onto `ThemeObject` in S7
  (Optional, default None) to avoid a circular import and protect `FrozenSnapshot`.
- **Decision:** §5.3 `transition()` is the single source of truth; Python mirrors the simulator's
  `derive()`/`transition()` exactly (attention-only events excluded from net valence; recency decay
  `0.5^(age/half_life)`; disconfirm asymmetry; terminal states absorbing).

### 2026-06-13 #1 — S1 surveillance core (commit `b7c3fad`)
- Added `engine/surveillance.py` + `tests/unit/test_surveillance.py` (16 tests: §5.10 1-11 + §9
  simulator-faithfulness). All green. Golden master byte-identical. No wall-clock. 722→738 passed.
- Invariants I1,I2,I5,I8 green.

### 2026-06-13 #2 — S3 / L2 WikiLintAgent (commit `2f66cd3`)
- Wired `WikiLintAgent.run()` → `validate_all`; added `WikiLintInput`.
- Resolved the known xfail: `check_log_single_entry` now matches PART-8 `## [<date>] ingest | <slug>`.
  Former `strict=xfail` is now a real passing check; `validate_all` test includes `source_slug`.
- 738→741 passed, **0 xfailed** (was 1). Golden master byte-identical. Invariants I1,I2,I4 green.
- **Note:** L1 (`DiscoveryRunnerAgent`) deferred to next session step — needs `engine/workflow.py` +
  `engine/protocols.py` (current-input seam) read to wire slug→seam→`run_workflow` correctly.

### Checkpoint status (2026-06-13)
- **DONE:** S1 (Phase 3 surveillance core — the prioritized centerpiece), S3/L2.
- **NEXT (spine):** S2/L1 (DiscoveryRunnerAgent) → S4/L3 (aggregator cap) → S5/L4 (typed family hints)
  → S6/L5 (require current_date) → S7 (ForwardHorizon on ThemeObject) → S8 (discovery→CASE persistence)
  → S9/S10 (ThemeMonitorAgent + write-back) → S11 (compression) → S12 (ingestion) → S13 (news/sufficiency)
  → S14 (calibration, corpus-gated) → S15 (demo CLI + verification report).
- Suite: **741 passed, 0 xfailed**. Branch `surveillance-build`, 3 commits atop base.
