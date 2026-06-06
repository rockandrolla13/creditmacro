# Skill — MENTAL MODEL AND BIAS CRITIC

**Type:** adversarial review skill. Runs AFTER the causal compiler / iceberg classifier,
BEFORE a theme is promoted to a ThemeObject. **Does NOT price or trade** — it interrogates
the *thinking* behind a theme so the agent does not become a narrative-confirmation machine.

## Provenance (method references, not reproduced content)
- **Meadows, *Thinking in Systems*** — mental models are the DEEPEST leverage point and the
  hardest to see; the system's real goal can differ from its stated goal; stocks/flows,
  delays, and bounded rationality make actors "do sensible things that produce bad results."
- **Mental-models primer** — confirmation bias, base-rate neglect, narrative fallacy,
  survivorship, map≠territory, reflexivity, novice-vs-expert framing. Source-derived where the
  file exists; otherwise standard mental-models canon (flagged).
- **Engine grounding (this repo):** the critic enforces the same honesty the engine encodes —
  the standing risk-premium/crowding confounder (`edge_basis="gross_of_risk_premium"`,
  `−HotTopicAttentionScore`), the requirement of an *operational axis*, and falsifier-first
  discipline. Not a source; the discipline this skill defends at the human layer.

---

## Skill Card

**skill_name:** mental_model_and_bias_critic

**purpose:** For any proposed theme, surface the mental model the PM is (often unknowingly)
using, generate rival models that explain the same facts, separate assumptions from facts,
demand disconfirming evidence, expose ignored higher-order effects, and decide whether the
model is sound, needs reframing, or should be rejected — BEFORE the theme consumes pricing
resources or anchors the book.

**when_to_use:** On every theme before promotion; again whenever conviction rises sharply, the
theme is "obvious," everyone agrees, or the PM cites the *narrative* rather than the *axis*.
High agreement is a trigger, not a comfort.

**input_schema:**
```
{
  "theme_id": str,
  "statement": str,                 # the proposed theme, as the PM phrased it
  "pm_rationale": str,              # why the PM believes it (the words matter — they reveal the model)
  "claimed_axis": str|null,         # the operational spread/ratio, if any
  "evidence": [str], "consensus_signals": [str],
  "horizon": str|null
}
```

**output_schema:**
```
{
  "theme_id": str,
  "dominant_mental_model": str,
  "alternative_models": [ {"model": str, "explains_same_facts_how": str, "implication_flips": bool} ],
  "assumptions_treated_as_facts": [ {"assumption": str, "is_testable": bool, "test": str|null} ],
  "lens_findings": { "<lens>": {"reading": str, "challenges_dominant": bool} },   # >=5 lenses
  "disconfirming_evidence": [str],
  "false_positives": [str],
  "expert_vs_amateur": {"amateur_reading": str, "expert_reading": str},
  "second_third_order_effects": [str],
  "pm_questions": [str],
  "decision": "accept_model"|"challenge_model"|"reject_model",
  "rationale": str
}
```

**mental_model_inventory** (name the model the PM is running; common credit-research ones):
| Model | One-line | Failure when… |
|---|---|---|
| Story / "new asset class = opportunity" | growth & novelty ⇒ good | novelty = illiquidity + concession, not edge |
| Supply = demand (build-it-and-they-come) | more issuance ⇒ healthy market | supply ⇒ indigestion ⇒ *wider* spreads |
| Capital cycle (Marathon) | hot-sector capex ⇒ oversupply ⇒ poor forward returns | bullish capex is *bearish* for forward credit |
| Mean reversion | extremes snap back | regime change makes "cheap" a value trap |
| Carry / "yield is yield" | wide spread ⇒ paid to wait | spread = fair compensation for real risk |
| Reflexivity (Soros) | the belief moves the price | the narrative tightens spreads until it reverses |
| Map ≠ territory | the index/label is not the asset | "investable universe" ≠ tradeable liquidity |

**bias_checks** (flag each present):
- **Confirmation** — is the PM only citing evidence that fits? (count for vs against)
- **Narrative fallacy** — is a story standing in for a *mechanism + axis*?
- **Base-rate neglect** — what happened to the LAST "new credit universe" (telecom/fiber 2000,
  shale HY 2014–15, CLOs)? Quote the base rate.
- **Survivorship** — are the cited issuers the survivors of a cohort that already culled?
- **Recency / salience** — is conviction tracking headlines rather than the series?
- **Crowding / risk-premium (standing)** — does "bullish" really mean "already priced"?
- **Authority / consensus** — is "everyone agrees" being used as evidence?

**alternative_lenses** (force the theme through ≥5; flag which challenge the dominant model):
1. **Fundamental** — cashflows, leverage, recourse, collateral durability.
2. **Technical / flow** — primary supply, concessions, index inclusion/rebalance flows.
3. **Liquidity** — does a tradeable market with bid/offer actually exist (Xantimum score)?
4. **Positioning / crowding** — who already owns it; how consensus is the trade.
5. **Cross-asset** — what do equity / rates / vol / the underlying real asset say?
6. **Time-horizon** — does the thesis survive the driver→axis delay and the refi/utilisation lag?
7. **Failure-mode** — how does this lose money even if the narrative is "right"?

**disconfirming_evidence_questions** (what would CHALLENGE, not confirm):
- What observable, if it moved, would *kill* this? (must be a series + threshold)
- What does the *bearish* expert on this exact theme say, and what data backs them?
- Has the dominant model failed in an analogous setup before? What was different / same?

**expert_vs_amateur_diagnostic:**
| | Amateur | Expert |
|---|---|---|
| Object | trades the *narrative* | trades a *named, computable axis* |
| Supply | "more issuance = healthy" | "supply ⇒ concession ⇒ where does it clear?" |
| Spread | "wide = cheap" | "wide vs what? net of risk premium?" |
| Novelty | "new = opportunity" | "new = illiquid, unproven recovery, base-rate poor" |
| Agreement | comfort | warning (likely priced) |
| Edge | absolute level | a *differential* that nets the standing confounder |

**decision_rubric:**
- `accept_model` — dominant model survives ≥5 lenses, assumptions are testable and tested, a
  clean operational axis exists, base rate acknowledged, evidence > attention. (Rare on first pass.)
- `challenge_model` — a real system is present but the *stated* model is novice / one-lens, OR
  an axis is missing, OR base rate/disconfirming evidence unaddressed. → reframe + send the PM
  questions; do not promote yet. (Most common.)
- `reject_model` — the theme rests on a narrative with no mechanism/axis, is contradicted by ≥2
  lenses, or is pure crowded attention. → narrative_noise.

---

## example_output — applied theme
**Theme:** *"AI capex funding is bullish for data-center project bonds because it creates a new
investable credit universe."*

### 1. Dominant mental model
**"New asset class = opportunity"** fused with **"supply = demand / build-it-and-they-come"**:
the existence of a new, growing issuance universe is read as *bullish for its credit*. It
treats a growth FLOW (capex/issuance) as evidence of credit STRENGTH, and a *label* ("an
investable universe") as a *tradeable market*. It is the amateur reading on the diagnostic:
trading the narrative, equating novelty with opportunity, treating agreement as comfort.

### 2. Alternative models (same facts, often opposite implication)
- **Capital cycle (Marathon)** — heavy capex into a euphoric sector ⇒ oversupply ⇒ *poor* forward
  credit returns. *Implication flips: bullish capex ⇒ bearish credit.*
- **Supply ⇒ indigestion** — a wave of new issuance ⇒ concessions ⇒ *wider* spreads, not tighter.
  *Flips "bullish."*
- **Map ≠ territory** — "investable universe" describes a *label/index*, not liquidity; non-recourse
  SPV project bonds may have thin two-way markets. *Challenges "investable."*
- **Risk premium / carry trap** — wide new-issuer spreads are *fair compensation* (GPU obsolescence,
  single-tenant concentration, refinancing risk), not free edge. *Flips "cheap."*
- **Reflexivity** — the "new universe" story itself compresses spreads via inclusion flows until
  fundamentals or supply reverse it. *Makes early tightening self-limiting, not structural.*

### 3. Hidden assumptions treated as facts
- "Bullish" = spreads tighten (vs. carry, vs. dispersion — unspecified). *(testable: define the axis)*
- A new universe is *liquid/investable* (a tradeable bid/offer exists). *(testable: Xantimum liquidity)*
- Capex funding ⇒ demand for *these bonds*. *(testable: who buys, at what concession)*
- Data-center cashflows are stable/contracted (PPAs, tenant covenants hold). *(testable: utilisation, renewals)*
- GPU/equipment collateral retains value (recovery assumption). *(testable: depreciation/resale curves — likely model_required, possibly non-identifiable now)*
- Project structure protects creditors (recourse, ring-fencing). *(testable: covenant/structure read)*

### 4. Possible false positives
- Early spread tightening from **index-inclusion / yield-chasing flows** mistaken for fundamental strength.
- **Primary concession reversal** (new issue cheap → grinds to fair) booked as alpha when it's just normalisation.
- **Survivorship**: the marquee hyperscaler-backed deals quoted are the strong cohort; the HY HPC tail is invisible.
- **Carry** mistaken for edge: wide spread "working" simply because nothing has defaulted *yet* (delay).

### 5. What would prove the mental model wrong
- Spreads **WIDEN** as the universe grows (supply premium dominates).
- Data-center **utilisation / PPA renewals weaken**, or single-tenant concentration bites.
- **GPU depreciation accelerates** → recovery assumptions fall → ratings migrate.
- **Liquidity fails**: project-bond bid/offer blows out; the "universe" is not tradeable.
- First **project-bond defaults / covenant breaches** in the cohort (base-rate echo of fiber 2001).

### 6. Questions for the PM before promotion
- What is the **operational axis**, and is "bullish" a *spread direction*, a *carry* view, or a
  *dispersion* (e.g. `HY HPC OAS − hyperscaler IG OAS`)? "New universe" is not an axis.
- Who is the **marginal buyer** of project bonds, and at what concession does primary clear?
- **Recourse/structure**: are these non-recourse SPVs? What is the recovery assumption, and is it
  identifiable today or a hand-to-PM unknown (GPU residuals)?
- **Base rate**: how did the last "new investable credit universe" (telecom/fiber 2000, shale)
  perform 12–24m post-hype? Why is this different?
- **Crowding**: how consensus/owned is this already? (loud agreement ⇒ likely priced)
- Does the thesis survive the **driver→axis delay** (capex now, cashflows/defaults later)?

### 7. Final decision
**`challenge_model`.** There is a real underlying *system* (an AI-infrastructure credit complex
with genuine spread relationships), so this is not pure noise — but the *stated* mental model
("new universe ⇒ bullish") is the novice, single-lens reading and flips under at least three
lenses (capital-cycle, supply-indigestion, liquidity). Do **not** promote as phrased. Reframe
from a directional "bullish" call into a **structure/dispersion theme on a named operational
axis**, net of the standing risk-premium confounder, and require the PM answers in (6) plus at
least one disconfirming series from (5) before promotion to a ThemeObject.

---
**Standing reminder:** this skill critiques the *model*, not the market. It never prices or
recommends a trade; it decides whether the thinking is sound enough to compile and price.
