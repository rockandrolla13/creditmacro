---
skill_name: iceberg-classifier
access_class: method
pipeline_phase: stage0_ingestion
provider_seam: [stage0.classify_iceberg, stage0.classify_candidate, stage0.rank_candidates, parse_research_text]
input_objects: [raw_thesis_text, report_text, evidence_atoms, source_metadata, method_context]
output_objects: [IcebergClassification, MainDevelopment, KeyEvent, HotTopic, CoreThemeCandidate, promotion_decision]
gates_created: [no_promotion_without_causal_chain_and_axis, hot_topic_is_not_investable]
allowed_to_influence: [iceberg layer assignment, candidate ranking pre-screen, promotion_decision]
not_allowed_to_influence: [pricing, sizing, expressions, scenario probabilities, strategy-family confidence numbers]
failure_modes: [promoting attention to a theme, confusing an event with a structure, treating a one-off as a development]
tests: [test_iceberg_hpc_is_hot_topic, test_iceberg_basis_is_core_candidate, test_iceberg_juli_is_key_event]
---

# Iceberg Classifier

> **Compiled from** *Thinking in Systems and Mental Models* (Dawson, "Super Thinker"), Ch.6
> "The Iceberg Model"; supplemented by the engine's `stage0` taxonomy. (The Citi theme book
> deck is image-only — see README source gap.) METHOD card: no case conclusions, no trades.

## Purpose
Classify raw research into the first market-intelligence layer — **Main Developments, Key
Events, Core Theme Candidates, Hot Topics** — and decide what may be *promoted* for causal work.

## Process primitives (paraphrased from the iceberg model)
The iceberg has four layers, each deeper one giving more understanding and more leverage:
- **Event** — a dated surface occurrence (the visible tip).
- **Pattern** — repeated/trending behaviour over time ("behaviour-over-time").
- **Structure** — the underlying system/market mechanism producing the pattern.
- **Mental model** — the belief/narrative shaping how the structure is interpreted.
Reasoning that stops at events stays reactive; the leverage is in naming the *structure* and
the *mental model*. Shift attention from events to behaviour-over-time to the structure beneath.

## When to use
On ingestion, before any causal compilation — to separate fact / attention / narrative /
mechanism so only structurally-grounded candidates advance.

## Inputs
Raw thesis text, report text, extracted evidence atoms, source metadata, optional method context.

## Outputs
`IcebergClassification`, `MainDevelopment[]`, `KeyEvent[]`, `HotTopic[]`, `CoreThemeCandidate[]`,
`promotion_decision`.

## Required fields
Per item: an iceberg layer (event/pattern/structure/mental_model), a one-line rationale, and —
for a `CoreThemeCandidate` — a named operational-axis candidate or `axis: none-yet`.

## Validation rules
- **Key Event** must have date / catalyst character (a surface occurrence).
- **Main Development** must be persistent (a pattern/structure), not a one-off event.
- **Hot Topic** is attention/narrative (mental-model layer) — *not* automatically investable.
- **Core Theme Candidate** must be causal, measurable, and potentially expressible (structure layer).
- **Do not promote** a hot topic to a core theme without a causal chain **and** an operational axis.

## Failure / blocked states
- Attention surfaced but no mechanism → keep as `HotTopic`, `promotion_decision = watchlist`.
- Event with no recurring pattern → `KeyEvent`, do not elevate to `MainDevelopment`.
- Candidate with no measurable axis → `CoreThemeCandidate(axis: none-yet)`, route to research_more.

## Example input
"A bank publishes a report showing a growing hyperscaler, data-center, and HY compute credit
ecosystem, and introduces a new Data-Center index sub-sector."

## Example output
- **Main Development** (structure): AI-infrastructure funding becoming a distinct credit ecosystem.
- **Key Event** (event): introduction of a Data-Center index sub-sector.
- **Hot Topic** (mental model): "AI capex / debt burden" narrative — high attention, not promoted.
- **Core Theme Candidate** (structure): project-level DC bonds valued via a related-obligation
  basis to hyperscalers — axis candidate: `project_OAS − hyperscaler_OAS`.

## Non-goals
No trades, no sizing, no instruments, no scenario probabilities. Classification only.
