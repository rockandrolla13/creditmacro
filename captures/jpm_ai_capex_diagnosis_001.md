# JPM AI Capex — Diagnosis (diagnosis_001)

**Date:** 2026-06-08 · **Run:** live discovery, `mode="discovery"`, provider `llm`, opt-in enabled.
**Outcome:** BLOCKED at the first generative seam. Observation only — engine, features, golden masters,
and firewalls untouched.

## 0. What actually happened

The opt-in guard accepted `ALLOW_LIVE_LLM_DISCOVERY=1` and the run proceeded into `run_workflow`. It
reached the first generative seam — `expand_causal` — and raised at `engine/llm_provider.py:105`
(`messages.create`) with:

```
TypeError: Could not resolve authentication method. Expected either api_key or auth_token to be set ...
```

There is no `ANTHROPIC_API_KEY` (nor `ANTHROPIC_AUTH_TOKEN`) in the environment. A Claude Code OAuth
token exists at `~/.claude/.credentials.json`, but it is a subscription credential scoped to the CLI
client; repurposing it to drive programmatic SDK calls would be credential misuse and is not what the
engine's live provider expects. So the live run is **genuinely blocked on infrastructure**, not on a code
bug. No scripted fallback was used.

Because the failure is an uncaught auth `TypeError` raised *before* `validate_discovery_output`/`freeze`,
no `LiveRunRecord` was written by the harness; the JSON capture in this folder was authored to document
the blocked attempt faithfully.

This means the six questions below cannot be answered from a live result. They are answered instead from a
**static read of the pipeline** — which is itself the more valuable finding, because it shows that even a
keyed run would not reproduce the known-correct output as-wired.

## 1. Which skill cards need tightening? (which stage had the most gaps)

Not answerable from behaviour (no cards were exercised — the run died before any prompt was built). But
the static analysis relocates the question: **the biggest gaps are not in card wording, they are in seam
wiring.** Two stages dominate:

- **Iceberg classification (Stage 1)** — the `iceberg-classifier` card exists and `classify_iceberg` is in
  `SEAM_TO_SKILLS`, but `LLMProvider` implements **no `classify_iceberg` method** and `_run_discovery`
  calls only `provider.parse()`, which returns empty streams. The card cannot be "tightened" into effect;
  the seam is simply not called. This is the highest-leverage gap because Iceberg is where the
  divergence(evidence, attention) pre-screen — the thing that would say "HPC is hot, do not promote" —
  lives.
- **Strategy-family ranking (Stage 6)** — no card fixes this; `select_strategy_families` returns one
  family. The "ranked families" deliverable is a structural property of the router, not a prompt.

If a card *did* need tightening once seams are wired, the `causal-compiler` (drives `expand_causal`, the
sole seam that ran-to-attempt) is the one to scrutinise first, since the whole run hinges on it producing
a routable single theme.

## 2. Which seams hallucinated vs which were faithful to the source?

None hallucinated — nothing was generated. Worth recording for the next run: the live seams **never see
the 56k-character report**. `expand_causal` is handed `ctx.statement` (the one-sentence `--input`) twice;
`define_axis` sees only the `--axis` strings; `build_system_map`/`diagnose_loops`/`critique` see only
prior seam outputs plus METHOD memory. So on the next (keyed) run, "faithfulness to source" will really
measure faithfulness to the **input sentence + axis hints**, not to the PDF. Any figure in the output
(105bp, 295bp, 43%, $49bn) that is not in the input sentence would be a **hallucination by construction**,
because the engine has no path to read it. This is the single most important thing to watch once unblocked.

## 3. Did the confidence decomposition produce sensible numbers?

No numbers were produced. Statically, the decomposition **cannot yet** make the distinction the acceptance
fixture asks for ("crowded HPC low, basis highest"):

- `propose_scenarios` returns `[]` in discovery → `priced_in_available=False` → `edge_survival="unknown"`
  for *every* family, `data_confidence` capped at 0.5, and ceilings of 0.45/0.60 applied. So every live
  family lands at confidence ≤ 0.45, dominated by the no-scenarios ceiling.
- Consequence: the basis and the crowded HPC trade would receive **the same ceiling-bound confidence**,
  because the engine has no scenario edge to separate them and routes only one theme anyway. The
  "highest-for-basis, lowest-for-HPC" ordering is an **edge/crowding judgement that discovery does not
  currently compute** — it would have to come from the Iceberg divergence pre-screen (Stage 1, unwired) or
  from supplied scenarios (not generated in discovery).
- One component *would* behave correctly: `_data_confidence` caps to 0.5 on missing scenarios/pricing,
  matching the "snapshot-only → cap data_confidence" expectation — but for the generic reason, not the
  specific "no history" one.

## 4. Did the firewalls hold?

Yes, trivially, and verified statically:

- **Phase-A memory firewall:** the retriever is built `phase="A"`, METHOD-only and fail-closed on CASE.
  The run died before retrieval mattered, so no CASE page could enter. The current source
  (`wiki/sources/jpm-ai-capex-funding-2026-05-11.md`, `access_class: case`) is supplied as *current input*
  via `current_sources`, a separate allowed path — it is **not** retrieved from memory, so it does not
  breach the phase-A rule.
- **Trade-leakage firewall:** `validate_discovery_output` never ran, but the (empty) output trivially
  carries no pricing/sizing/expressions. `freeze()` was never reached, so no snapshot hash was minted.
- **No trades/sizing/legs** were produced anywhere. Compliant.

Caveat: the firewalls "held" because nothing flowed through them. This run does **not** constitute positive
evidence that the leakage gate or the freeze ordering work under live load — only that they were not
violated.

## 5. Did the semantic contract / leakage gate catch anything?

It never executed (it runs *after* discovery, in `run_live_discovery`, and the auth error short-circuited
before that). But a static read surfaces a sharp, repo-internal contradiction worth flagging now:

- The `jpm_report` contract (`semantic_contract.py:65-77`) is explicitly built to **reject a generic curve
  steepener as the sole axis** ("generic curve steepener is the only axis — expected source-derived
  RV/basis axes for this report") and to require a project/hyperscaler/DC-vs-Tech/index/HPC axis.
- Yet the seeded on-disk fixture `cases/discovery/jpm_ai_capex.yaml` encodes exactly a **5s30s curve
  steepener** thesis. That fixture is the *scripted* reading of the same report and would **fail its own
  input-kind's semantic contract** if it were run as a live `jpm_report`. The scripted golden and the live
  contract therefore disagree about what the correct answer to this report even is. (This is an
  observation, not a change — the fixture was not modified.)

So: the gate would *plausibly* have fired on a curve-only live answer — which is good — but we have no live
confirmation, and the existence of a golden fixture that contradicts the gate is a latent trap for future
regression work.

## 6. Single most impactful fix before running a second source

**Make a real Anthropic API key available to the live provider and re-run** — that is the literal blocker
and nothing downstream can be observed without it. Set `ANTHROPIC_API_KEY` (a real API key, not the CLI
OAuth token) alongside `ALLOW_LIVE_LLM_DISCOVERY=1`.

But the more important *engineering* fix — the one that determines whether the keyed run is even worth
grading against this acceptance fixture — is upstream of the key: **wire the `classify_iceberg` seam into
the live provider and `_run_discovery`.** Without it, a keyed run still emits no Iceberg classification, no
evidence-vs-attention divergence pre-screen, and (because the router promotes one theme and returns one
family) cannot produce the ranked quartet the fixture expects. The credential unblocks *a* run; the iceberg
seam is what makes the run *comparable* to the known-correct output.

Recommended order:
1. Supply `ANTHROPIC_API_KEY` and re-run to get a real `expand_causal → … → one-family` trace (smoke).
2. Then decide whether to (a) wire `classify_iceberg` + multi-theme nomination so the ranked-quartet
   comparison is meaningful, or (b) accept that live discovery is single-theme by design and **rewrite the
   acceptance fixture to grade one theme per run** (run the report four times, once per candidate axis).

## Appendix — report facts confirmed present (faithfulness ground truth)

All known-correct figures were verified to exist in `markdowns/JPM_AI_Capex_Funding_Dat_2026-05-11_5290840.md`:
27 issuers / >$450bn (p1); 105bp IG / 183bp HY hyperscaler-project basis (p1); DC sub-sector $49bn par,
4.8% of Tech, 0.5% of JULI (p6); DC 181bp vs Tech 101bp (p7); HPC $26.6bn YTD = 43% of non-refi HY supply
(p8); HPC 1.07%→2.68% of HY index, +9.99% vs +1.61%, STW 295bp vs HY 307bp = 12bp through (p2/p9);
144A-for-life + limited syndication index exclusions (p8). The acceptance fixture is faithful to source;
the gap is entirely on the engine side.
