# Theme Discipline and Failure Modes

> A focused design memo on the engine's biggest current problem: **too many themes, too little
> human-analyst-style compression.** Companion to `docs/SPEC_AND_STATE.md` (Part 3.2 and
> the failure-mode catalogue in Part 2.5), which superseded the `ENGINE_MANUAL` /
> `ENGINE_CONTEXT_PACK` pair on 2026-08-10.
> Written 2026-06-13 from code (`engine/theme_aggregation.py`,
> `engine/schema/theme_aggregation.py`). Status tags: ✅ implemented · ⚠️ partial · 🚧 planned ·
> ❌ missing.
>
> **Revised 2026-08-11.** The original description of the similarity metric was wrong — it named a
> function the code did not contain and drew the opposite conclusion about the threshold. See
> "Correction" below and the rewritten "Merge rules". Measurements here are reproduced as tests in
> `tests/unit/test_theme_aggregation.py`; that file, not this memo, is authoritative.

## Problem statement

The engine extracts **too many themes**. It often treats *facts*, *subthemes*, *hot topics*, and
*strategy hints* as separate top-level themes. This produces **breadth without judgment**: long flat
lists of near-duplicate themes, no parent/subtheme structure, weak cross-source attribution, and hot
topics promoted as if they were core themes.

This is **structural, not a tuning bug.** Grounded in `engine/theme_aggregation.py`:

- **Greedy single-pass clustering** (`_cluster_items`): each candidate joins the *best* existing
  cluster only if `_similarity ≥ min_similarity_to_merge`.
- **Canonical naming is raw-member based**: `canonical = max(members, key=(len(evidence_ids),
  len(name)))`. It picks the longest existing member name; it never **synthesizes** a parent theme.
- **No parent-theme / subtheme schema** — `ThemeCluster` is flat (members, attributions, scores,
  status). There is no "Main Development → Parent Theme → Subtheme" hierarchy.
- **No cap** on clusters per batch; **no human-analyst synthesis.**

You cannot fix this by moving a threshold. The missing piece is a **compression / synthesis stage**
that reasons about mechanism, not token overlap.

### Correction (2026-08-11): what the similarity metric actually was

An earlier revision of this memo described `_similarity` as "the **max** over six Jaccard overlaps"
and concluded that "a 0.5 max-overlap bar is **high**", so near-duplicates survived. **Both claims
were wrong, and they described code that did not exist.** The function was:

```python
def _overlap(a, b):                      # the OVERLAP COEFFICIENT, not Jaccard
    return len(a & b) / min(len(a), len(b))
```

Because the denominator was `min`, **any token set that was a subset of another scored exactly
1.0**. Measured:

| pair | old `_overlap` | Jaccard |
|---|---|---|
| `growth` vs `rates not pricing growth` | **1.00** | 0.25 |
| `growth` vs `china growth slowdown` | **1.00** | 0.33 |
| `growth` vs `growth in ai capex funding needs` | **1.00** | 0.20 |
| `european bank spreads` vs `japanese bank spreads` | 0.67 → merged | 0.50 |

So the bar was not uniformly high: every one of those `growth` pairs merged at **any** threshold
≤ 1.0, and `min_similarity_to_merge` was not doing the work this memo claimed for it. Meanwhile two
long, differently-worded descriptions of the same theme share no tokens, score 0.0, and stay apart.

**Both failure modes were live at once** — that is the finding that matters. Raising the threshold
worsened fragmentation; lowering it worsened over-merging. No single dial fixed it, which is why the
fix was a change of metric plus a second pass, not a retune. See "Merge rules" below for what
replaced it.

## Desired behavior

A human analyst compresses many facts into a **small number of coherent parent themes**. They do not
want 40 themes — they want **3 to 7 parent themes**, each carrying:

- supporting **subthemes**,
- **evidence by source**,
- a **causal mechanism**,
- an **observable axis** (or an explicit watchlist tag),
- **why it matters**,
- **why it might be wrong**,
- **what would confirm or invalidate it** (a falsifier),
- which **strategy family** it maps to (one or two, not all),
- **what data is missing**.

## Theme hierarchy (target)

```
Main Development
  → Parent Theme
      → Subtheme
          → Evidence Cluster
              → Operational Axis
                  → Strategy Family
```

The current engine produces only the flat `ThemeCluster → (operational_axes, strategy_family_hints)`
slice of this. The **Main Development → Parent → Subtheme** layers are not modeled.

## Promotion rules

A **parent theme** must have *all* of:

- source-backed **evidence** (≥1 evidence atom, ideally from ≥1 *current* source),
- a **causal mechanism** (driver → transmission → outcome),
- an **operational axis** *or* an explicit **watchlist** tag,
- a **falsifier** (observable + threshold),
- a **temporal status** (current vs historical/outcome-candidate),
- a **strategy-family implication** (1–2 routable families),
- a stated **reason it was selected** (selection rationale).

> Today: the aggregator partially enforces evidence (flags "unpromotable" without atoms) and blocks
> all-historical clusters from `promote_to_discovery`. It does **not** enforce mechanism + axis +
> falsifier + rationale *together* as a promotion gate. ⚠️

## Merge rules

**Merge** candidate themes when they share **all** of:

- driver,
- mechanism,
- outcome,
- axis,
- strategy family.

> Today (2026-08-11) the aggregator runs **two passes**, and the mechanism half of this rule is
> implemented. ⚠️→✅ for driver/mechanism/outcome; axis + family are not yet required. ⚠️

**Pass 1 — lexical recall.** `_similarity` is still the **max** over the six dimensions (tokens,
concepts, entities, market_vars, axes, causal), but each is now scored by `_weighted_jaccard`:
symmetric weighted Jaccard, so containment no longer saturates. Tokens introduced by an **alias**
substitution carry `alias_anchor_weight` (default 3.0), because a curated alias is evidence about
*meaning* whereas incidental word-sharing is not. `min_similarity_to_merge` was **re-tuned to
0.55** for this metric — the max-min-margin point of the measured band `(0.500, 0.600]`; the old
0.5 was calibrated against a different function.

Plain Jaccard was measured and **rejected**: it scores `growth` vs `china growth slowdown` (must
not merge) and `private credit risk` vs `direct lending spreads` (must merge) at the **same 0.333**,
so it has no separating threshold either. The alias anchoring is what breaks that tie.

**Pass 2 — mechanism precision** (`_mechanism_merge`). Merges two clusters only when *all three*
hold, using the sets the clusters already carry:

| rule element | cluster set |
|---|---|
| driver + outcome | `causal` (driver→outcome tokens of the linked causal claims) |
| mechanism | `axes` (the operational axis the transmission is observed on) |
| outcome variable | `market_vars` (the observable that actually moves) |

A missing set is never evidence of sameness, so a cluster lacking any of the three cannot
mechanism-merge at all — the pass is strictly **additive**. Its bar (`min_mechanism_similarity`,
0.34) sits **below** the pass-1 bar on purpose: pass 1 is a *disjunction* over six dimensions
("any one signal is strong"), pass 2 a *conjunction* over three ("all three agree at once"). Set
them equal and pass 2 becomes dead code, because whichever dimension cleared 0.55 already caused
pass 1 to merge. This is the pass that fixes **fragmentation**: two long, differently-worded
descriptions of one theme share no tokens and pass 1 can never join them.

**Guards** (both passes). A merge is refused, and recorded in `rejected_merges`, when either the
existing `distinct_pairs` marker guard fires, or the **discriminator guard** does: both sides name a
qualifier from the same closed vocabulary (geography in v1) and share none of them —
`european bank spreads` vs `japanese bank spreads`, same mechanism, different market. Structure
agreeing does not license merging what the guards call distinct. The guards are **defence in
depth**: the threshold alone classifies the whole labelled pair set correctly with the guards
switched off, so an incomplete discriminator vocabulary degrades the result rather than breaking it.

**Ordering.** Items are sorted into a canonical, content-derived order before pass 1, so the output
is a function of the input *set*, not of the order the caller supplied. The pass remains greedy —
it is not a global optimum — but the same themes now always yield the same clusters, and ties
resolve to the lowest cluster key rather than to whichever cluster happened to be seen first.

## Keep-separate rules (make them subthemes, not merges)

Keep themes **separate** (as subthemes under one parent) when:

- same driver but **different outcome**,
- same sector but **different mechanism**,
- same source but **different axis**,
- one is **current** and one is **historical**.

> Today there is no subtheme relation to express this — themes are either merged (one cluster) or
> not (two clusters). ⚠️/❌

## Downgrade rules

**Downgrade to hot-topic / watchlist** (do *not* promote to a core theme) when any of:

- attention without evidence,
- no operational axis,
- no causal chain,
- only source opinion,
- historical forecast without an outcome check,
- no falsifier.

> Today: `theme_status` can be `watchlist` and the engine computes an `attention_score`, but there
> is no explicit rule that an attention-only / no-axis / no-falsifier theme is *forced* to
> watchlist. The promotion path checks temporal quality + axis presence, not the full downgrade set.
> ⚠️

## Cross-source coverage matrix

Require a **theme × source** matrix so corroboration is visible and auditable:

| Theme | Source A | Source B | Source C | Evidence count | Independent sources | Contradictions | Status |
|---|---|---|---|---|---|---|---|
| Rates not pricing growth | ✅ | ✅ | — | 4 | 2 | 0 | promote |
| Europe rich vs FV | ✅ | — | — | 1 | 1 | 0 | watchlist |
| AI-capex credit supply | ✅ | ✅ | ✅ | 7 | 3 | 1 (B vs C) | promote (flag contradiction) |

> Today: `ThemeCluster.source_attributions` carries per-source contribution + `is_current_input`, and
> the engine computes `corroboration_score` / `independent_source_count`. The **matrix view** and an
> explicit **contradiction column** are not produced — that's a rendering + a small schema addition.
> ⚠️

## Human-analyst synthesis template

Each batch should produce a short readout *before* discovery:

```markdown
## Analyst synthesis — batch <id> (<date>)

### Parent themes (3–7)
1. <Parent theme name> — <one-sentence mechanism: driver → outcome>
   - Subthemes: <a>, <b>, <c>
   - Evidence: <n atoms across m sources>  (corroboration: <independent sources>)
   - Operational axis: <named spread/slope, or "watchlist">
   - Temporal status: <current | historical/outcome-candidate>
   - Strategy family: <1–2 routable families>
   - Why it matters: <…>
   - Why it might be wrong / falsifier: <observable + threshold>
   - Missing data: <…>

### Downgraded to hot-topic / watchlist (with reason)
- <theme> — <attention without evidence | no axis | no falsifier | …>

### Merged / rejected
- <theme X> merged into <parent> — shares driver/mechanism/outcome/axis/family
- <theme Y> rejected — <reason>

### Why these themes, and why not the others
<2–4 sentences of explicit judgment>
```

## Acceptance tests (for the proposed ThemeCompressionAgent / AnalystThemeMap) 🚧

These define "done" for the compression stage (which **does not exist yet**):

1. **Parent-theme cap honored.** Given a batch that lexically yields N>7 clusters, the agent emits
   ≤ a configured cap (default 7) parent themes; the rest become subthemes/watchlist — never dropped
   silently (the count of demoted/merged themes is logged).
2. **Every promoted parent theme passes the full promotion gate** — evidence + mechanism + axis +
   falsifier + temporal status + ≥1 routable family + selection rationale. A theme missing any is
   not promoted.
3. **Merge rule unit-tested** — two themes sharing driver/mechanism/outcome/axis/family merge into
   one parent; two sharing only a driver become subthemes of one parent (not merged, not separate).
4. **Downgrade rule unit-tested** — an attention-only / no-axis / no-falsifier theme is forced to
   watchlist regardless of attention score.
5. **Subtheme preservation** — subthemes and their axes survive under the parent (not flattened
   away); the `source_coverage_matrix` lists each parent with its per-source evidence.
6. **"Why not" populated** — `rejected_or_merged_themes` and `hot_topics_not_promoted` are non-empty
   whenever themes were demoted, with a reason per entry.
7. **Historical discipline** — a historical-only theme is emitted as outcome-candidate/analogue,
   never `promote_to_discovery` (preserve the existing aggregator invariant).
8. **No trades / no sizing** — the `AnalystThemeMap` and `human_readout` contain no legs, sizes,
   hedge ratios, or execution (reuse the WikiIntegrator no-trade guard).
9. **Determinism** — same input → same `AnalystThemeMap` (no wall-clock; stable ordering).
10. **Golden master unchanged** — adding the compression stage must not alter
    `tests/integration/test_golden_master.py` numerics.

## Where this plugs in

```
MultiSourceThemeAggregator  →  [ ThemeCompressionAgent 🚧 ]  →  discovery handoff
   (flat ThemeClusters)          (AnalystThemeMap:                (parent themes only,
                                  parent/subtheme hierarchy,        capped, gated)
                                  coverage matrix, readout)
```

The compression agent consumes the existing `MultiSourceThemeSet` (so the lexical pass is still a
useful *recall* stage — it surfaces candidates), and adds the **precision / judgment** layer the
engine currently lacks. It is the single highest-leverage build on the roadmap.
