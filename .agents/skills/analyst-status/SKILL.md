---
name: analyst-status
description: >
  Use when you want to step back from the build and look at the PRODUCT rather than the code —
  see what the analyst actually produces on the real research notes in the repo and how close it
  is to the goal. Triggers: "analyst status", "show me the analyst's output / brief", "what does
  the analyst produce", "run a status and demonstration pass", "is this the thing I set out to
  build / how close are we", "render the brief", "product status", "step back and show me the
  product". Read-only on engine logic. Do NOT trigger for building new features, changing engine
  behaviour, running discovery for trading, or commit/log summaries.
---

# Analyst Status & Output

> **This is a STATUS + DEMONSTRATION pass — read-only on engine logic. NOT a method/case reasoning
> card.** The only artifact you may *add* is a thin *rendering* script if none exists. **Change no
> engine behaviour.** It is generic: it runs on whatever research notes are in the repo, with no
> phase numbers or hardcoded themes — so re-running it later shows how the product has moved.
>
> Put this line at the top of the output doc: *"This is a product-status + output pass; re-run it
> to see movement."*

## The point

A human looks at the rendered brief and answers ONE question: **is this the thing I set out to
build, and how close?** Make that answerable at a glance — real output up front, honest fit read
beside it. An honest "unresolved / no analogue yet" IS the correct output, not a gap to paper over.
**Never fabricate to make the brief look fuller.**

## THE GOAL (the yardstick — restate it, judge output against it)

A macro-credit **discovery** engine (not a trade engine): ingest research notes / investment memos
→ surface **~5–6 themes** that will drive markets over a **3–4 month horizon** → for each, a
**mechanism**, a **trackable operational axis** (a real, computable series), and a recommended
**strategy *type*** (a routable family — never a trade) → persist + surveil live themes → **learn
from how historical analogues resolved**. It **STOPS** before trade construction.

## Procedure

Produce a single doc — `docs/ANALYST_STATUS.md` — and print it to the session. Four parts:

### PART 1 — THE WORKFLOW (product view, plain language — NOT the S-number build phases)

One clear map: what goes **in**, the stages, what comes **out**. A simple diagram + one line
"consumes → emits" per stage. Product-level, no build-phase jargon.

```
research notes/memos
   → INGEST            (case-only, trade language stripped)
   → EXTRACT themes    (mechanism + evidence atoms)
   → COMPRESS          (merge by mechanism, cap 5–7, 7-criterion promotion gate)
   → ROUTE             (→ a strategy family; STOP — no trade)
   → PERSIST           (CASE page: axis + falsifier + horizon)
   → SURVEIL           (state machine; falsifier-gated; alerts only)
   → CLOSE             (ThemeOutcomeRecord)
   → CALIBRATE/LEARN   (from historical analogues + their outcomes)
```

### PART 2 — THE OUTPUT (the thing to judge — render THE ANALYST'S BRIEF on real input)

Run the analyst **end-to-end on the research notes actually in the repo** and render the
**human-facing artifact a user would receive** — "The Analyst's Brief." If no renderer exists,
write a **thin** one (`demo/analyst_brief.py`) over the real APIs — **do not change engine logic.**
Populate it from the **real run**. For each promoted theme show:

- the **theme statement**
- **mechanism**: driver → transmission → outcome
- **track via**: the operational axis (the trackable series) + current level / direction
- **strategy**: the routable family
- **confidence**: score + what drives it
- **falsified if**: the pre-registered falsifier
- **coverage**: how many sources / which institutions
- **history**: closest analogue (regime, outcome worked/failed) — or "no analogue yet"

Then:
- **WATCHLIST** — themes that did **not** promote + the gate reason (no axis / no falsifier / single source)
- **UNDER SURVEILLANCE** — any live themes + status + alert
- **WHAT HISTORY SAYS** — analogues retrieved from case memory with their outcomes

Where a field is thin (history empty because the corpus is small; an extracted level is
`unresolved` because the markdown number was ambiguous), **say so plainly.**

### PART 3 — FIT TO GOAL (does the rendered brief match the yardstick? honest)

Map the **real** brief against THE GOAL, line by line:

| Goal property | Delivered? |
|---|---|
| ~5–6 themes, ranked | |
| 3–4 month horizon on each | |
| strategy **types**, not trades (STOPs before construction) | |
| every promoted theme tied to a **trackable** axis | |
| learns from historical analogues + outcomes | |

Each: ✅ delivered / ⚠️ partial (say exactly why) / 🚧 machinery-present-but-data-gated. If history
is thin or extraction approximate, **mark it** — the value of this pass is an honest fit read, not a
green checkmark.

### PART 4 — STATUS IN PRODUCT TERMS (capabilities, not commits)

A short table — each **product capability** → its true state. **Not a commit log.** What can the
user rely on **today**:

| Capability | State |
|---|---|
| Ingest research → typed, case-only streams | |
| Discover + compress to 5–6 themes | |
| Route to a strategy family (and STOP) | |
| Persist a theme + surveil it live | |
| Close a theme → outcome record | |
| Calibrate / learn from history | |

✅ works end-to-end / ⚠️ provisional / 🚧 data-or-config-gated, one line each, with the **one thing**
that would most move each ⚠️/🚧 toward ✅ (usually: more research notes, or the DB feed).

## Rules (do not break)

- **Read-only on engine logic.** No behaviour changes. The only thing you may add is a thin
  renderer (`demo/analyst_brief.py`) over the existing public APIs, and only if none exists.
- **Render the REAL run** on the repo's actual notes. No hardcoded themes, no phase numbers.
- **Do not fabricate.** Thin/empty fields are reported as `unresolved` / `no analogue yet`.
- Output goes to `docs/ANALYST_STATUS.md` AND is printed to the session.

## Common mistakes

- Summarising the build (S-numbers / commits) instead of the **product**. → PART 4 is capabilities,
  not a changelog.
- Inventing themes, levels, or analogues to fill the brief. → Empty is the honest, correct output.
- "Improving" the engine while rendering. → This pass changes no engine logic; if a number is
  wrong, report it, don't patch it.
- Writing a generic template instead of the real run. → Populate from actual repo notes via the
  real APIs.
