# Theme Discipline and Failure Modes

> A focused design memo on the engine's biggest current problem: **too many themes, too little
> human-analyst-style compression.** Companion to `docs/SPEC_AND_STATE.md` (Part 3.2 and
> the failure-mode catalogue in Part 2.5), which superseded the `ENGINE_MANUAL` /
> `ENGINE_CONTEXT_PACK` pair on 2026-08-10.
> Written 2026-06-13 from code (`engine/theme_aggregation.py`,
> `engine/schema/theme_aggregation.py`). Status tags: ✅ implemented · ⚠️ partial · 🚧 planned ·
> ❌ missing.

## Problem statement

The engine extracts **too many themes**. It often treats *facts*, *subthemes*, *hot topics*, and
*strategy hints* as separate top-level themes. This produces **breadth without judgment**: long flat
lists of near-duplicate themes, no parent/subtheme structure, weak cross-source attribution, and hot
topics promoted as if they were core themes.

This is **structural, not a tuning bug.** Grounded in `engine/theme_aggregation.py`:

- **Greedy, order-dependent single-pass clustering** (`_cluster_items`): each candidate joins the
  *best* existing cluster only if `_similarity ≥ min_similarity_to_merge` (default **0.5**).
- `_similarity` is the **max** over six Jaccard overlaps (tokens, concepts, entities, market_vars,
  axes, causal). A 0.5 *max-overlap* bar is **high** — two phrasings of the same theme that don't
  share ≥50% of tokens on any single dimension stay **separate** → near-duplicate clusters survive.
- **Canonical naming is raw-member based**: `canonical = max(members, key=(len(evidence_ids),
  len(name)))`. It picks the longest existing member name; it never **synthesizes** a parent theme.
- **No parent-theme / subtheme schema** — `ThemeCluster` is flat (members, attributions, scores,
  status). There is no "Main Development → Parent Theme → Subtheme" hierarchy.
- **No cap** on clusters per batch; **no second-pass compression**; **no human-analyst synthesis.**

You cannot fix this by lowering a threshold. Lowering `min_similarity_to_merge` would over-merge
unrelated themes; the missing piece is a **compression / synthesis stage** that reasons about
mechanism, not token overlap.

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

> Today the merge decision is **token/alias Jaccard ≥ 0.5 on any one dimension** — a lexical proxy,
> not a mechanism match. Two themes with the same driver/outcome but different vocabulary do not
> merge. ⚠️

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
