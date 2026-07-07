# ONTOLOGY.md — Theme Hypothesis Ledger (normative specification)

Status: NORMATIVE. This document defines what must be true. It contains no
build instructions. Where this document and any other document (including
BUILD_PROMPT) conflict, this document wins and the conflict is a bug.
All constants are defined here exactly once; code references them by the
names given here.

> **Changelog**
> - 2026-07-07 — session amendments folded in (see `ONTOLOGY_DELTA.md`).
>   Three additions (A1 vocabulary crosswalk, A2 wiki-inversion scope,
>   A3 status-axis reconciliation) and two fixes (F1 prior-mass on
>   RETIRED+CREATED, F2 identity-vs-merge tie-break) reconcile this spec
>   with the existing `engine/` tree. Amendment blocks are marked
>   **⟦AMEND …⟧**. The original normative text is otherwise unchanged.

---

## §Theme — definition

A theme is a falsifiable hypothesis that a specific causal transmission is
currently active in the market. Formally a tuple

    θ = (M, σ, X, H, F)

**M — transmission chain.** A signed path in the market causal graph:

    M : v0 --s1--> v1 --s2--> ... --sk--> vk,   sj ∈ {+1, −1}

where v0 is a driver node (policy stance, funding conditions, issuance
technicals, ...), vk is the terminal market variable, and every node is
drawn from the controlled vocabulary (§Vocabulary). Edges are typed,
signed causal claims. k = number of edges; the chain has k−1 intermediate
nodes.

**σ ∈ {+1, −1} — shock direction.** The hypothesis asserts the channel M
is currently being driven at v0 in direction σ. A theme is not "this
channel exists" (that is method knowledge, §Memory) but "this channel is
active now, in this direction."

**X — operational axis.** The observable proxy for vk (e.g. C0A0 OAS,
H0A0 OAS, CDX.IG 5Y, 3M10Y). X is a measurement choice, not hypothesis
content: it carries a sign convention sign(X) ∈ {+1, −1} mapping "axis
value up" to "vk up" (+1) or "vk down" (−1). X must be a member of the
tracked-axis registry.

**H — forward horizon.** timedelta bounding valid time of the hypothesis.
Constraint: H ≤ H_MAX = 120 days.

**F — falsifier.** A decidable predicate over available market-data
series, evaluated by the surveillance layer through the Breach Buffer.
"Decidable" means: given the data feeds in the tracked-axis registry and
a timestamp, F(t) ∈ {breached, not-breached} is computable with no human
judgment.

**Derived direction.** The predicted direction of θ on vk is

    d(θ) = σ · Π_{j=1..k} sj

and the predicted direction on the axis is d_X(θ) = d(θ) · sign(X).
d(θ) is a derived property. It MUST NOT be stored as a field. Any
externally supplied direction (wiki, analyst, extractor) that disagrees
with σ·Πsj renders the theme malformed (§WF predicate, clause e).

**Interpretation.** A theme with score S < 0 (§Scoring) is CONTESTED, not
reversed. The hypothesis (M, −σ) is a distinct theme (§Identity). Never
represent "the opposite is happening" as a negative score on (M, +σ).

---

## §Vocabulary

A controlled set V of transmission nodes, |V| ≈ 60 at seed, each with
{node_id, description, synonyms}. Seed derivation: the Collin-Dufresne,
Goldstein & Martin (2001) credit-spread determinants plus the credit-BMI
factor families (volatility, momentum, sentiment, liquidity/funding,
supply, business-cycle, valuation), decomposed into atomic transmission
nodes (e.g. funding_stress, dealer_balance_sheet_capacity,
liquidity_premium, default_expectations, term_premium, issuance_supply,
risk_appetite, earnings_trajectory, ...).

V is closed under review: new nodes enter only through the review queue
(§Admission, out-of-vocabulary path). No component may silently mint a
node. Purpose: mechanism similarity becomes a graph problem (edge overlap)
rather than an embedding problem, and Pass B matching gains a structural
stage (§EvidenceLink).

> **⟦AMEND A1 — vocabulary crosswalk (normative)⟧**
> V is METHOD memory and MUST NOT be an island beside the method memory
> that already exists. Each `node_id` in V carries a **crosswalk** binding
> it to the existing graph:
>
>     node_id → { causal_node: schema.causal.CausalNode name | null,
>                 wiki_concepts: [concept slug, ...],
>                 driver_tags: [legacy free-string tag, ...] }
>
> Rules: (i) `vocab.py` owns this mapping and is the single source of
> truth for it; (ii) a V node with no `causal_node` and no `wiki_concepts`
> is a **new** method claim and routes through the review queue exactly
> like an out-of-vocabulary node — it is never silently added; (iii) Pass A
> tags claims with V `node_id`s only, but the crosswalk lets Pass B's
> structural pre-match and every wiki render join the existing causal graph
> and concept pages. The crosswalk is the join that de-islands the ledger.

---

## §Identity

Theme identity is the pair (M, σ). Everything else — X, H, F — is
attribute.

    θ1 ~ θ2  ⟺  M1 ≅ M2  ∧  σ1 = σ2

**Path equivalence ≅.** M1 ≅ M2 iff (i) same endpoint nodes v0, vk,
(ii) same edge-sign product Πsj, and (iii) node-overlap: the intermediate
node sets intersect, i.e. one chain is a refinement or coarsening of the
other. Chains with same endpoints and sign product but disjoint
intermediate nodes are NOT equivalent (different transmission stories to
the same conclusion).

Consequences (normative):
1. Same prediction ≠ same theme. Two themes agreeing on X and d(θ) but
   with M1 ≇ M2 are distinct: different falsifiers, different evidence
   bases, different survival behavior. Merge decisions (AnalystThemeMap)
   use chain overlap — Jaccard over typed signed edges

       J(E1, E2) = |E1 ∩ E2| / |E1 ∪ E2| ≥ J_MERGE = 0.5

   with equal sign product — never text-embedding similarity of theme
   summaries alone.
2. Axis change preserves identity. Swapping X for the same (M, σ) is
   re-measurement (event AXIS_REVISED, §Event semantics).
3. Shock reversal is a new theme. (M, +1) and (M, −1) are distinct
   hypotheses with independent evidence, falsifiers, lifecycles.

> **⟦AMEND F2 — identity-vs-merge tie-break (normative fix)⟧**
> ≅ (identity/refinement) and J ≥ J_MERGE (merge) can both hold for the
> same pair. Deterministic tie-break for Pass B / event classification:
> 1. When an extracted successor θ' is being classified against the theme
>    it was **matched to** (same `theme_id` lineage), ≅ wins: θ' is a
>    `MECHANISM_REVISED` revision of that theme, never a new `CREATED`.
> 2. `MERGED_INTO` applies ONLY across two **already-distinct** `theme_id`s
>    discovered independently. Merge never fires within a single theme's
>    revision history.
> 3. If a newly `CREATED` theme (e.g. orphan promotion) is ≅ to an existing
>    distinct theme at creation time, it is not created; the evidence maps
>    to the existing theme as a `MECHANISM_REVISED` instead. This prevents
>    the "create-then-immediately-merge" churn.

---

## §WF predicate

A theme is admissible iff

    WF(θ) := (a) k ≥ 2                       — at least 1 intermediate node
           ∧ (b) decidable(F)                — per §Theme
           ∧ (c) X ∈ tracked-axis registry
           ∧ (d) H ≤ H_MAX (= 120 days)
           ∧ (e) any externally stated direction equals d(θ) = σ·Πsj

Clause (a) is the theme/forecast boundary: a k = 1 "theme" ("spreads
widen because risk-off") has no transmission to surveil and no falsifier
other than its own prediction; it is a directional call and is rejected.
Objects failing WF route to the NEEDS_STRUCTURING queue with the failing
clause named. Nothing is ever force-admitted.

---

## §Bitemporal

Every theme fact carries two time axes:

- valid time t_v: when the hypothesis claims to hold in the market
  (its horizon window [effective_at, effective_at + H])
- transaction time t_x: when the system recorded the fact (recorded_at)

Distinct queries these support (never conflate):

    as-of (backtest, no lookahead):
        Θ(t_x) = { θ : recorded(θ) ≤ t_x < superseded(θ) }
    valid-over (outcome attribution):
        Θ_v(t)  = { θ : t ∈ [effective_at(θ), effective_at(θ) + H(θ)] }

`recorded_at` is set by the persistence layer only and is immutable.
Backdating `effective_at` is permitted only when provenance =
"wiki_import" AND a source revision timestamp exists. No event may
retroactively alter the result of any as-of query at an earlier t_x.

**Event sourcing.** Themes are never stored as mutable rows. A theme at
transaction time t_x is a fold over its event stream:

    θ(t_x) = ⊕_{e : e.recorded_at ≤ t_x} e.payload

ThemeEvent (frozen):
    event_id, theme_id,
    event_type ∈ { CREATED, MECHANISM_REVISED, AXIS_REVISED,
                   FALSIFIER_REVISED, HORIZON_EXTENDED, STATUS_CHANGED,
                   MERGED_INTO, RETIRED },
    payload (delta only), recorded_at, effective_at,
    provenance ∈ { wiki_import, surveillance, analyst, orphan_promotion },
    supersedes: event_id | null

Fold requirements: deterministic; invariant under replay-order
permutation among equal-recorded_at events; total (every event type has
fold semantics). The fold module is the ONLY constructor of
ThemeHypothesis values.

**Revision counter.** revision(θ, t_x) = number of events folded. Every
EvidenceLink binds theme_revision at mapping time (§EvidenceLink).

---

## §Event semantics

Given an extracted or proposed successor θ' to current θ:

    MECHANISM_REVISED     iff M' ≅ M            (refinement: same endpoints,
                                                 same sign product,
                                                 overlapping intermediates)
    RETIRED + CREATED     iff M' ≇ M  ∨  σ' ≠ σ (new hypothesis; evidence
                                                 NEVER migrates across this
                                                 boundary — see F1 below)
    AXIS_REVISED          iff (M', σ') = (M, σ) ∧ X' ≠ X
    HORIZON_EXTENDED      iff attribute-only change to H
    FALSIFIER_REVISED     iff attribute-only change to F
    STATUS_CHANGED        per §Lifecycle
    MERGED_INTO           per §Identity consequence 1 (J ≥ J_MERGE)

**Link policy per event type** (applied to existing EvidenceLinks):

    AXIS_REVISED, MECHANISM_REVISED  → REMAP: supersede all prior links,
                                       re-run Pass B against the new
                                       definition. (Axis sign-convention
                                       flips silently invert every
                                       historical polarity if carried —
                                       remap is mandatory.)
    HORIZON_EXTENDED, FALSIFIER_REVISED → CARRY: links remain valid.
    RETIRED + CREATED                → none carry; see below.

> **⟦AMEND F1 — prior-mass on RETIRED+CREATED (normative fix)⟧**
> The original phrase "new theme starts at prior mass only" was
> misleading: **prior mass is a wiki-import construct only** (§Scoring,
> Case B). A theme born from a mechanism/shock change (provenance =
> surveillance | analyst | orphan_promotion) has NO synthetic prior-mass
> row minted. It starts with an **empty EvidenceLink ledger**, hence
> S_θ = 0, and must re-earn evidence from scratch. No evidence migrates
> across the RETIRED+CREATED boundary. This is deliberate: a genuinely new
> transmission story has earned nothing yet.

**Wiki-revision pre-filter.** Text-level edits with mechanism-text
embedding cosine ≥ COS_COSMETIC = 0.92 between revisions are cosmetic:
no event. Below the threshold, the decision is made structurally on the
extracted chains per the table above — the cosine gate is a pre-filter
only, never the semantic decision.

---

## §Lifecycle

    status ∈ { CANDIDATE, ACTIVE, FALSIFIED, EXPIRED, RETIRED, MERGED }

    CANDIDATE → ACTIVE      iff B_θ ≥ 2 ∧ |S_θ| ≥ 2        (§Scoring)
    ACTIVE    → FALSIFIED   only via Breach Buffer confirmation of F.
                            Document contra-evidence NEVER falsifies;
                            it decrements S_θ. S_θ < 0 with no breach
                            is CONTESTED (a reportable sub-state of
                            ACTIVE), not dead.
    ACTIVE    → EXPIRED     at effective_at + H without renewal
                            (HORIZON_EXTENDED resets the clock).
    any       → RETIRED     via §Event semantics (identity change) or
                            analyst decision (review-gated).
    any       → MERGED      via MERGED_INTO, target recorded in payload.

Rationale for the falsification asymmetry: analyst disagreement is
opinion flow; market breach is realized state. Coupling theme death to
narrative shifts recreates on the evidence side the whipsaw the Breach
Buffer exists to prevent on the market side.

> **⟦AMEND A3 — status-axis reconciliation (normative)⟧**
> The existing `engine/` tree carries TWO other status enums. All three
> are **orthogonal axes** and MUST NOT be conflated:
>
> | Axis | Enum | Question it answers | Owner |
> |------|------|---------------------|-------|
> | Pipeline progress | `schema.ThemeObject.status` (blocked / discovery_complete / strategy_family_routed / expression_complete) | how far did the engine get? | discovery/engines |
> | Surveillance obs | `surveillance.WatchStatus` (terminal set) | what did the blind watcher observe? | surveillance_agent |
> | Market truth | §Lifecycle status (this section) | is the hypothesis alive in the market? | the ledger |
>
> `STATUS_CHANGED` events govern the **market-truth axis only**. The
> pipeline axis is a property of the projected `ThemeObject` (§Rendered
> view / projection); the surveillance axis is owned by the surveillance
> layer and is an *input* to the ACTIVE→FALSIFIED transition, not a copy
> of it. `projection.py` is the only site permitted to map between axes.

---

## §AtomicClaim

Output of Pass A (blind extraction — the extractor sees ONLY the
document; the theme registry is unreachable by construction).

    AtomicClaim (frozen):
        claim_id, doc_id, source_institution, doc_date,
        text                : one-sentence paraphrase
        market_variable     : normalized member of tracked-axis registry
                              or vk vocabulary
        direction           : ∈ {+1, −1, 0}   (0 = conditional/neutral)
        horizon             : timedelta, as stated or inferred
        stated_conviction   : ∈ {1, 2, 3}, from the document's own language
        mechanism_tags      : list of node_ids from §Vocabulary

Granularity: one claim per (market_variable, direction, horizon) tuple.
A document may support theme A and contradict theme B simultaneously;
document-level stance summaries are forbidden.

---

## §EvidenceLink

Output of Pass B (mapping). Pass B receives the claim set plus theme
DEFINITIONS only — a ThemeDefinitionView carrying (M, σ, X, H): no
ledger, no scores, no status. Matching is two-stage:

1. Structural pre-match: claim.mechanism_tags ∩ nodes(M) ≠ ∅ and
   claim.market_variable compatible with vk or X.
2. Semantic match producing match_confidence ∈ [0, 1].

    EvidenceLink (frozen, append-only):
        theme_id, theme_revision,          — fold count at mapping time
        claim_id,
        polarity  = claim.direction × d(θ)     — COMPUTED, never emitted
                                                 by an LLM
        match_confidence,
        supersedes: link_id | null

Routing: max over themes of match_confidence < τ_ORPHAN = 0.6 → the
claim enters the orphan pool. Claims with direction = 0 may link with
polarity 0 (recorded for coverage; zero score contribution).

Polarity is computed so that contra-evidence is found for free: a claim
that vk moves opposite to d(θ) on a matched axis automatically carries
polarity −1 without the mapper "deciding" to disagree.

---

## §Scoring

Scores are derived views over the EvidenceLink ledger. No score is ever
stored. For theme θ with link set L(θ) (non-superseded links, claims via
join), at evaluation time t:

    S_θ(t) = clip_[−10, +10] ( Σ_{i ∈ L(θ)}  p_i · s_i · λ^{(t − t_i)/h} · ν_i )

    p_i  = polarity ∈ {−1, 0, +1}
    s_i  = stated_conviction ∈ {1, 2, 3}
    t_i  = claim doc_date
    h    = H/2            (half-life; λ = 1/2 — a 120-day theme's
                           evidence half-lives at 60 days, consistent
                           with dynamic staleness keyed to horizon)
    ν_i  = NOVELTY_DISCOUNT = 0.15  if embedding cosine of claim i to any
           earlier claim from the SAME institution on the same theme
           > COS_NOVELTY = 0.88;  else 1.0.
           Cross-institution repetition keeps ν = 1.0: independent
           corroboration counts in full; a bank repeating its house view
           does not.

    Per-institution cap: the net contribution of any single institution
    to S_θ is clipped to [−CAP_INST, +CAP_INST], CAP_INST = 3, before
    the outer sum. No single source can saturate a theme.

    Breadth: B_θ(t) = |{ institutions with net contribution > 0 }|

Interpretation: a pseudo-Bayesian log-odds accumulator. Each claim is a
weak likelihood ratio with log-LR ≈ p·s; decay encodes staleness of
testimony about a bounded horizon; ν corrects for the non-independence of
the sell-side corpus. S and B are always reported together: S = +6 from
one institution and S = +6 from four are different epistemic states.

Purity requirements: S_θ(t) and B_θ(t) are pure functions of
(ledger, t); invariant under ledger append-order permutation at fixed
timestamps; evaluating them mutates nothing.

Prior mass (wiki import, Case B): an imported theme with no ledgered
evidence is seeded with one synthetic evidence row of strength
s_prior ∈ {1, 2, 3} (the wiki's implicit conviction), decaying at the
standard half-life:

    S_θ(t) = s_prior · λ^{(t − t_import)/h}

Rationale: the wiki is testimony of unknown vintage; it earns prior mass
that must decay so that within one half-life the score is dominated by
fresh, ledgered evidence. A theme receiving no corroboration sinks toward
zero on its own. t_x is NEVER backdated in Case B. (Prior mass is a
wiki-import construct ONLY — see §Event semantics AMEND F1.)

---

## §Admission

Orphan-pool clustering: group orphan claims by mechanism_tags overlap and
embedding proximity. A cluster is promoted to a CandidateTheme iff

    |claims| ≥ N_MIN = 3  ∧  |institutions| ≥ I_MIN = 2
    ∧  max doc_date − min doc_date ≤ W_ADMIT = 30 days

Synthesis: mechanism assembled over §Vocabulary from the cluster's modal
tags; X from the modal market_variable; the candidate must pass WF or it
routes to NEEDS_STRUCTURING. Promotion CANDIDATE → ACTIVE per §Lifecycle.

Out-of-vocabulary path: a cluster whose modal tag is not in V proposes a
vocabulary addition into the review queue. It is never auto-added.

Admission gating and compression (AnalystThemeMap merging) coexist:
admission slows registry growth at the door; compression merges
mechanism-duplicates (J ≥ J_MERGE) that get through.

> **Corpus note (2026-07-07).** A WF-survival spike over the 86 existing
> `wiki/themes/` pages found 82/86 (95%) fail WF clause (a) (k ≤ 1); only
> 4 curated pages survive. The population path is therefore **forward
> re-ingest**: Pass A over the source corpus → orphan pool → admission
> rebuilds the registry. `wiki_import` handles only the 4 survivors. The
> 82 cards are provenance breadcrumbs (card→source), not theme inputs.
> See `ONTOLOGY_DELTA.md` D-04.

---

## §Memory

Factorization along the two-axis taxonomy:

- The chain M (and V generally) is METHOD memory: transmission channels
  are reusable, regime-independent knowledge. The funding-stress →
  liquidity-premium channel exists whether or not it is active.
- The instantiated theme (M, σ, X, H, F) with its evidence and outcome is
  CASE memory, indexed regime × axis × mechanism × outcome status.

Access-class routing rules of the surveillance spec apply unchanged;
unknown access_class defaults to CASE (per the R1 resolution), never to
method.

---

## §Rendered view

The wiki is a rendered artifact of the ledger, never a source of truth:

    event log --fold--> θ(t_x) --render--> wiki page

Per-theme page contents (normative minimum): mechanism chain with signed
edges; σ and d(θ); X with sign convention; S_θ and B_θ as of render time;
falsifier text and current Breach Buffer state; per-institution evidence
table (net contribution, capped); event-log timeline.

Round-trip requirement: parse(render(θ)) recovers a ThemeHypothesis equal
to θ on all structured fields.

Analyst edits enter through the front door: a diff between
rendered-expected and wiki-actual is parsed into proposed ThemeEvents
(provenance = "analyst") entering a review queue. Drift is never
auto-applied. Bidirectional sync is forbidden (two-master problem).

> **⟦AMEND A2 — wiki-inversion scope (normative)⟧**
> "The wiki is a rendered artifact of the ledger" applies to **theme
> (case) pages ONLY** — `wiki/themes/`. It does NOT invert the rest of the
> wiki. Specifically, unchanged and still human-curated source-of-truth:
> method pages (`wiki/concepts/`, `wiki/engines/`, book/paper sources),
> and non-theme case pages (`wiki/scenarios/`, `wiki/outcomes/`,
> `wiki/entities/`, `wiki/sources/`). The `memory.MemoryRetriever`
> firewall and the lint workflow continue to treat those as the memory of
> record. Only `wiki/themes/*` is regenerated from folds; only those pages
> feed the drift-diff → review queue. This resolves the apparent conflict
> with §Memory ("access-class routing applies unchanged"): the ledger owns
> theme case memory; the wiki keeps owning method memory and all other
> case memory.

---

## §Constants (single point of definition)

    H_MAX            = 120 days
    J_MERGE          = 0.5
    COS_COSMETIC     = 0.92
    COS_NOVELTY      = 0.88
    NOVELTY_DISCOUNT = 0.15
    CAP_INST         = 3
    τ_ORPHAN         = 0.6
    N_MIN            = 3
    I_MIN            = 2
    W_ADMIT          = 30 days
    ACTIVATION       : B ≥ 2 ∧ |S| ≥ 2
    λ                = 1/2 with half-life h = H/2

Code references these by name (`engine/ledger/constants.py` is the sole
Python mirror). Changing a constant is an ONTOLOGY change: it requires an
edit here plus an `ONTOLOGY_DELTA.md` entry, never a local override.
