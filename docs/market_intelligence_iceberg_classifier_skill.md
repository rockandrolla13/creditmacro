# Skill — MARKET INTELLIGENCE ICEBERG CLASSIFIER

**Type:** Stage-0 process skill (classification + routing). **Does NOT price or trade.**

## Provenance (method references, not reproduced content)
- **Meadows, *Thinking in Systems*** — the iceberg / levels-of-perspective lens (events →
  patterns → system structure → mental models) and the systems claim that leverage lives
  *below* the event line. Source-derived.
- **"Super Thinker" mental-models primer** — base rates, confounders, the warning that a
  loud consensus belief is the *mental-model* layer, not evidence (attention ≠ truth).
  Source-derived where the file exists; otherwise standard mental-models knowledge (flagged).
- **Engine grounding (this repo):** the four lanes are the existing Stage-0 typed streams
  (`engine/stage0.py`, `engine/schema.py`), and `ThemePromotionScore` is the generalisation
  of `rank_candidates`' `pre_screen_score = evidence − attention`. Not a source; the wiring target.

---

## Skill Card

**skill_name:** market_intelligence_iceberg_classifier

**purpose:** Classify ANY research note / event / news item / transcript / PM comment into
the four Meadows iceberg layers, score each, route to the Stage-0 dashboard lanes, and
decide what is promotable into the Theme Object pipeline. It separates *what is investable
structure* from *what is merely loud narrative*.

**when_to_use:** At ingestion (Stage 0), before any causal compilation or pricing. Run it on
every incoming item. Run it again when an item's status changes (a watchlist event fires).

**input_schema:**
```
{
  "item_id": str,
  "text": str,                       # the raw note / headline / comment / transcript chunk
  "source": str,                     # e.g. "sell-side credit report 2026-06"
  "date": str|null,                  # ISO date if the item is dated (drives EventScore)
  "links": {"observation_ids": [str], "consensus_ids": [str]}  # optional prior context
}
```

**output_schema:**
```
{
  "item_id": str,
  "layer": "surface_event"|"pattern_trend"|"system_structure"|"mental_model",
  "dashboard_lane": "KEY_EVENTS"|"MAIN_DEVELOPMENTS"|"CORE_THEMES"|"HOT_TOPICS",
  "typed_stream": "Observation"|"CandidateTheme"|"ConsensusSignal",
  "scores": {                        # each 0..1, tagged PM_assumption | model_required
    "EventScore": float, "PatternScore": float, "StructureScore": float,
    "MentalModelScore": float, "HotTopicAttentionScore": float,
    "ThemePromotionScore": float    # may be negative
  },
  "operational_axis": str|null,      # required for promotion; null => not yet investable
  "decision": "promote_to_theme"|"watchlist"|"narrative_noise",
  "rationale": str,
  "confounder_flags": [str]          # e.g. "crowding / risk-premium: loud attention => likely priced"
}
```

**classification_rules** (iceberg layer → dashboard lane → Stage-0 typed stream):
| Iceberg layer | Dashboard lane | Typed stream | Test for membership |
|---|---|---|---|
| Surface Event | **KEY EVENTS** | `Observation` (event) | a DATED catalyst that confirms / weakens / creates a theme |
| Pattern / Trend | **MAIN DEVELOPMENTS** | `Observation` (development) | a PERSISTENT change in the market system (repeats, broadens) |
| System Structure | **CORE THEMES** | `CandidateTheme` | a CAUSAL, MEASURABLE, INVESTABLE hypothesis (mechanism + operational axis) |
| Mental Model | **HOT TOPICS** | `ConsensusSignal` | a high-attention narrative — the belief / consensus layer |
An item may occupy MORE THAN ONE layer (a thesis that is also a crowded narrative is both a
`CandidateTheme` AND a `ConsensusSignal`); emit both — do not collapse. That dual emission is
exactly what drives a LOW promotion score (evidence already met by attention).

**scoring_model** (all 0..1 unless noted):
```
EventScore            = datedness x catalyst_potential
PatternScore          = persistence x breadth_of_trend
StructureScore        = has_causal_mechanism x has_operational_axis     # measurable AND investable
MentalModelScore      = how entrenched / consensus the belief is
HotTopicAttentionScore= current attention / crowding
ThemePromotionScore   = StructureScore x (PatternScore + EventScore) - HotTopicAttentionScore
                        # = evidence − attention ; same sign convention as
                        #   stage0.rank_candidates' pre_screen_score (ev − att)
```

**promotion_rules:**
- `promote_to_theme` — `StructureScore` high **AND** an operational axis exists **AND**
  `ThemePromotionScore > 0` (evidence exceeds attention). → enters the causal compiler.
- `watchlist` — structurally interesting but **no operational axis yet**, OR a key event is
  pending. → held in CORE THEMES with `operational_axis=null`; re-score when the axis lands
  or the event fires.
- `narrative_noise` — high `HotTopicAttentionScore`, low `StructureScore` (priced / crowded,
  not investable). → the belief layer with no system beneath it; stays in HOT TOPICS as a
  *prior for q*, never promoted.

**rejection_rules / standing checks:**
- A HOT TOPIC is **never promoted on attention alone**. High `MentalModelScore` /
  `HotTopicAttentionScore` is evidence the market is *already looking*, i.e. likely priced.
- **Standing confounder (credit):** the **risk-premium / crowding confounder** — loud
  attention or a wide spread usually means *already priced*, not *mispriced*. Always set a
  `confounder_flag` when attention is high; let it pull `ThemePromotionScore` down via the
  `− HotTopicAttentionScore` term.
- Reject as `narrative_noise` anything whose only claim to relevance is that "everyone is
  talking about it."

**PM_questions:** (handed up, not resolved here)
- Are the scores from data or my judgment? (each is tagged PM_assumption | model_required)
- For a promote: is the operational axis a *clean, theme-free* series, or already contaminated
  by the very narrative (crowding)?
- For a watchlist: what observable would create the missing axis / fire the pending event?
- Is a high-attention item genuinely priced, or is attention loud but positioning light?

**next_agent:** `causal_theme_compiler` (for each `promote_to_theme`).

---

## example_output — applied to a generic input
*Input (illustration, not baked in): a sell-side credit report revealing a growing
multi-issuer ecosystem with spread relationships (e.g. an AI-infrastructure credit complex:
hyperscaler IG, data-center project/ABS, HY HPC issuers). Every score below is tagged
`PM_assumption` (PM judgment) or `model_required` (needs a computed series).*

### 1. MAIN DEVELOPMENTS (Pattern/Trend → `Observation`)
- "AI-linked IG net issuance has risen for several consecutive quarters; 30Y-tenor share is
  expanding." → PatternScore = persistence(0.8 `model_required`) × breadth(0.7 `model_required`)
  ≈ **0.56**. Persistent, broad → a real development, not a one-off.

### 2. KEY EVENTS (Surface Event → `Observation`)
- "A hyperscaler priced a large 30Y deal at a notable new-issue concession (dated)." →
  EventScore = datedness(1.0) × catalyst_potential(0.6 `PM_assumption`) = **0.60**. A dated
  catalyst that *confirms* the supply development.

### 3. CORE THEME CANDIDATES (System Structure → `CandidateTheme`)
- **C1 — AI-credit dispersion:** "AI capex funding shifts relative value across hyperscaler IG,
  data-center project bonds, and HY HPC." Mechanism: supply/quality-ladder transmission.
  Operational axis = `HY HPC issuer OAS − hyperscaler IG OAS, duration/rating-adjusted, bps`.
  StructureScore = has_mechanism(0.9 `PM_assumption`) × has_operational_axis(1.0) = **0.90**.
- **C2 — data-center project-structure premium:** mechanism plausible (SPV subordination /
  illiquidity) but no liquid traded axis yet. StructureScore = 0.8 × has_axis(0.3
  `model_required`) = **0.24**.

### 4. HOT TOPICS (Mental Model → `ConsensusSignal`)
- "'AI bubble in credit' is the consensus narrative; long-AI-credit positioning looks crowded."
  MentalModelScore = entrenched(0.85 `PM_assumption`); HotTopicAttentionScore = 0.80
  (`model_required`, e.g. TAARSS/flow z-score). The belief layer.

### Routing decisions
`ThemePromotionScore = StructureScore × (PatternScore + EventScore) − HotTopicAttentionScore`

| Item | Structure | Pattern+Event | Attention | PromotionScore | Decision |
|---|---|---|---|---|---|
| **C1 AI-credit dispersion** | 0.90 | 0.56+0.60=1.16 | 0.40 (`PM_assumption`, dispersion trade less crowded than outright) | 0.90×1.16 − 0.40 = **+0.64** | **promote_to_theme** |
| **C2 data-center premium** | 0.24 | 1.16 | 0.30 | 0.24×1.16 − 0.30 = **−0.02** | **watchlist** (no axis yet) |
| **"AI bubble" narrative** | 0.10 | — | 0.80 | 0.10×1.16 − 0.80 = **−0.68** | **narrative_noise** |

### 5. promoted_to_theme_object
- **C1 — AI-credit dispersion** (StructureScore 0.90, operational axis exists,
  ThemePromotionScore **+0.64** > 0). → `next_agent: causal_theme_compiler`.
  `confounder_flags: ["crowding/risk-premium: net attention 0.40 already discounts the edge;
  axis must be a clean theme-free differential"]`.

### 6. watchlist
- **C2 — data-center project-structure premium** (structurally interesting, axis not yet liquid
  → `operational_axis=null`). Re-score when a traded project-bond/ABS spread series exists.

### 7. narrative_noise
- **"AI bubble in credit"** (attention 0.80, structure 0.10). Priced/crowded belief layer;
  retained only as a **prior for q** (the consensus the pricing stage measures *against*),
  never promoted on attention alone.

---

**Standing reminder:** this skill classifies and routes only. Promotion means "worth
compiling into a causal Theme Object," NOT "worth trading." Pricing and expression selection
happen downstream. No trade is recommended.
