"""A2 — theme discovery + factor mapping, REFRAMED as enrichment. SCAFFOLD: `enrich` is a stub.

**The plan is out of date here, and following it literally would be the expensive mistake.**
`PLAN-theme-lifecycle.md` §3 specifies a new `ThemeCandidateSet` of `ThemeCandidate` objects,
written when `engine/compression.py` did not exist. It exists now, and `AnalystThemeMap` already
does most of A2's job. Building `ThemeCandidate` beside `ParentTheme` would give the repo two
overlapping theme types with two promotion gates.

What A2 asked for, and where it already lives:

    A2 ThemeCandidate field   already on compression's ParentTheme / AnalystThemeMap
    ----------------------    ------------------------------------------------------
    theme_id                  parent_id
    canonical_name            name
    thesis_statement          mechanism.as_sentence() + why_it_matters
    aliases_seen              merged_cluster_ids + DemotedTheme(destination="merged")
    supporting_atom_ids       evidence_ids / evidence_by_source
    source_coverage           SourceCoverageMatrix + EvidenceBySource
    falsification_triggers    ThemeFalsifier  (untyped vs D-A2-5 — see below)
    dedup_registry            merged_cluster_ids + every DemotedTheme reason
    funnel                    CompressionStats
    3..7 parent cap           AnalystThemeMap.parent_cap
    adversarial_case          why_it_might_be_wrong  (a string, not a structure)

So this module adds **only the blocks compression does not produce**, keyed by `parent_id`,
and never re-derives a parent. Compression owns selection; this owns scoring. `EnrichedThemeMap`
holds a reference to the map rather than a copy, so the two cannot drift.

The genuine gaps, and the two partial ones:

  * GAP    consensus_effect, surprise_metrics, mapped_regimes, factor_map,
           factor_tractability, initial_lifecycle, contradicting_atom_ids
           (compression counts contradictions but does not keep their ids)
  * PARTIAL adversarial_case — `why_it_might_be_wrong` is a sentence; D-A2-4 wants a structure
           with evidence and a system response. Enrich rather than replace.
  * PARTIAL falsification_triggers — `ThemeFalsifier(observable, threshold, kill_rule)` lacks
           D-A2-5's `deadline`, `implication` and `retirement_state`, so surveillance still has
           interpretive freedom when a trigger fires. Enrich rather than replace.

`engine/compression.py` and `engine/schema/compression.py` are READ-ONLY to this module.
Not to be confused with `engine/ledger/lifecycle.py`.
"""
from __future__ import annotations

from typing import Literal, Optional, Sequence

from pydantic import BaseModel, ConfigDict, Field

from ..schema.compression import AnalystThemeMap
from .decisions import (
    INITIAL_HALF_LIFE_DAYS,
    INITIAL_MAX_LIFE_DAYS,
    LIFECYCLE_DECISIONS_VERSION,
)
from .regime import RegimeVocabulary

#: Bumped from the plan's "themeset/3" because the shape changed: this is an enrichment keyed
#: to an AnalystThemeMap, not a standalone candidate set.
ENRICHMENT_CONTRACT: str = "enrichment/1"


class EnrichmentRefused(RuntimeError):
    """A2 could not enrich — e.g. a mandatory adversarial case is missing (D-A2-4)."""


class InitialLifecycle(BaseModel):
    """DEFAULTS only. Surveillance's state machine takes over at the first tick and owns
    `lifecycle_state` thereafter; A2 never authors runtime state."""

    model_config = ConfigDict(frozen=True)

    created_at: str
    expected_review_at: Optional[str] = None
    expected_retirement_at: Optional[str] = None
    half_life_days: int = INITIAL_HALF_LIFE_DAYS
    max_life_days: int = INITIAL_MAX_LIFE_DAYS


class EvidenceScores(BaseModel):
    """Every score harness-computed (G4). `None` where the input stream is absent — a
    `consensus_score` of 0.0 asserts measured indifference, which is a different claim from
    having no `ConsensusSignal` data at all."""

    model_config = ConfigDict(frozen=True)

    support_score: Optional[float] = None
    contradiction_score: Optional[float] = None
    freshness_score: Optional[float] = None
    novelty_score: Optional[float] = None
    consensus_score: Optional[float] = None
    crowding_score: Optional[float] = None


class ConsensusEffect(BaseModel):
    """D-A2-3, the quarantine rule. Sell-side agreement is evidence a theme is CROWDED, not
    that it is true, so the effect is SPLIT across three scores rather than compounded into
    one. Otherwise the mesh becomes a sell-side echo machine."""

    model_config = ConfigDict(frozen=True)

    independent_publishers: int = Field(default=0, ge=0)
    support_delta: float = 0.0                    # small — consensus supports EXISTENCE, weakly
    consensus_delta: float = 0.0                  # larger — agreement is agreement
    crowding_delta: float = 0.0                   # larger still — agreement raises priced-in risk
    confidence_gamma_capped: bool = False
    reason: str = ""                              # harness-written, not model narrative


class SurpriseMetrics(BaseModel):
    """D-A2-6 — NARRATIVE surprise, per theme. Distinct from `surprise.NumericContext`, which
    is numeric surprise per atom and drives the state machine. Both exist and are never
    conflated: a numerically surprising atom can land inside a narratively stale theme."""

    model_config = ConfigDict(frozen=True)

    narrative_surprise: Optional[float] = None    # new vs recent research consensus?
    market_surprise: Optional[float] = None       # not yet in spreads / basis / flows?
    revision_surprise: Optional[float] = None     # analysts changing view, not restating?
    contradiction_surprise: Optional[float] = None  # strong evidence against consensus?


class AdversarialCase(BaseModel):
    """D-A2-4 — the mandatory bear case, structured. Enriches `ParentTheme.why_it_might_be_wrong`
    (a sentence) with the evidence behind it and what the system did about it."""

    model_config = ConfigDict(frozen=True)

    against_theme: str                            # G8 closed-vocabulary; kept atoms only
    supporting_evidence: tuple[str, ...] = ()     # atom ids, contradicting or technical
    system_response: str = ""                     # rebut, or move the numbers — one of the two
    conviction_cap: Optional[float] = None        # applied if the bear case remains material


class FalsifierTrigger(BaseModel):
    """D-A2-5 — typed, not a free string. `retirement_state` is the EXPLICIT surveillance
    transition that fires on breach, so the state machine has no interpretive freedom."""

    model_config = ConfigDict(frozen=True)

    series: str
    condition: str
    deadline: Optional[str] = None                # None = open-ended
    implication: str = ""
    retirement_state: Literal["weakening", "contradicted", "invalidated", "played_out"]


class FactorMap(BaseModel):
    """Macro and credit kept SEPARATE. `credit` is what L5's tractability gate reads; `macro`
    is context. Conflating them is how "the trade is actually a rates duration bet" hides."""

    model_config = ConfigDict(frozen=True)

    macro: dict[str, float] = Field(default_factory=dict)
    credit: dict[str, float] = Field(default_factory=dict)


class FactorTractability(BaseModel):
    """Decided at INFERENCE time, once (D-L5-1). An untractable theme is still tracked; L5's
    gate short-circuits on it without recomputing."""

    model_config = ConfigDict(frozen=True)

    decision: Literal["pass", "fail", "insufficient_data"]
    score: Optional[float] = None                 # residual-alpha share
    reason: str = ""                              # harness-written


class ThemeEnrichment(BaseModel):
    """Everything A2 adds to ONE compression parent theme. Never restates what the parent
    already carries — `parent_id` is the join key back to it."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    parent_id: str
    contradicting_atom_ids: tuple[str, ...] = ()
    initial_lifecycle: Optional[InitialLifecycle] = None
    evidence_scores: EvidenceScores = EvidenceScores()
    consensus_effect: Optional[ConsensusEffect] = None
    surprise_metrics: SurpriseMetrics = SurpriseMetrics()
    adversarial_case: Optional[AdversarialCase] = None
    mapped_regime_ids: tuple[str, ...] = ()
    secondary_regime_ids: tuple[str, ...] = ()
    #: `None` means factor data was insufficient — never read as absence of factor exposure.
    #: L5's gate closes on `None` exactly as it closes on an explicit fail.
    factor_map: Optional[FactorMap] = None
    factor_tractability: Optional[FactorTractability] = None
    falsification_triggers: tuple[FalsifierTrigger, ...] = ()
    rv_layer_status: Literal["enabled", "disabled", "undetermined"] = "undetermined"


class EnrichedThemeMap(BaseModel):
    """The A2 emit: a REFERENCE to compression's map plus the blocks it does not produce.

    Holding the map itself rather than copying its parents is the point — one source of truth
    for what the themes are, one for how they score.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    contract_version: str = ENRICHMENT_CONTRACT
    decisions_version: str = LIFECYCLE_DECISIONS_VERSION
    as_of: str                                    # supplied, never the clock (I8)
    theme_map: AnalystThemeMap
    enrichments: tuple[ThemeEnrichment, ...] = ()
    regime_vocabulary: Optional[RegimeVocabulary] = None
    ledger_root: Optional[str] = None
    warnings: tuple[str, ...] = ()


def enrich(
    theme_map: AnalystThemeMap,
    *,
    as_of: str,
    regimes: Optional[RegimeVocabulary] = None,
    atoms: Sequence[object] = (),
) -> EnrichedThemeMap:
    """Add A2's scoring blocks to an existing analyst theme map.

    TODO(A2): for each `ParentTheme`, compute the consensus split (D-A2-3), the four narrative
    surprise axes (D-A2-6), the structured adversarial case (D-A2-4), typed triggers (D-A2-5),
    the regime mapping and the factor map + tractability (D-L5-1). Raise `EnrichmentRefused`
    when a mandatory adversarial case cannot be built. Never construct or reorder a parent
    theme — compression owns that.
    """
    raise NotImplementedError("A2 enrich — scaffold only, no implementation yet")
