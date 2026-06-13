"""Stage-0 Multi-Source Theme Aggregator — schemas (PART 2).

Combine theme candidates from MULTIPLE current-input sources into one deduplicated,
source-attributed, ranked theme set. Product boundary:

    multi-source evidence → unique Stage-0 theme clusters → discovery-ready candidates → STOP

DISCIPLINE: no trades, no sizing, no hedge ratios, no scenario probabilities, no fair
values, no execution. Nothing here mutates q/edge/Omega/scoring. Archived CASE memory may
never confirm a CURRENT theme in Phase A — enforced by the cluster validators below.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

ContributionType = Literal[
    "supports", "contradicts", "mentions_only", "historical_analogue", "method_context",
]
ThemeStatus = Literal[
    "promote_to_discovery", "watchlist", "historical_case", "outcome_candidate",
    "reject", "needs_more_evidence",
]
SourceScope = Literal[
    "explicit_current_batch", "all_method_sources", "historical_case_batch", "mixed_batch",
]

# (L4) Strategy-family hint vocabulary. ROUTABLE_FAMILIES (12) is exactly what StrategyFamilyRec
# can emit today (kept in sync by a test). curve + sector_rotation are wiki-taxonomy only (no
# routing rule). `relative_value` is the parent the router resolves into the RV sub-types
# (etf_basket_rv / capital_structure / index_index_rv). A hint outside this set fails validation.
ROUTABLE_FAMILIES: tuple[str, ...] = (
    "steepener", "flattener", "long_short", "outright", "cash_cds_basis",
    "credit_vs_equity", "credit_vs_rates", "volatility_convexity", "watchlist_only",
    "etf_basket_rv", "capital_structure", "index_index_rv",
)
WIKI_ONLY_FAMILIES: tuple[str, ...] = ("curve", "sector_rotation")
StrategyFamilyName = Literal[
    # routable (12) — what the router can emit
    "steepener", "flattener", "long_short", "outright", "cash_cds_basis",
    "credit_vs_equity", "credit_vs_rates", "volatility_convexity", "watchlist_only",
    "etf_basket_rv", "capital_structure", "index_index_rv",
    # wiki-taxonomy only (no routing rule)
    "curve", "sector_rotation",
    # parent the router resolves into RV sub-types
    "relative_value",
]


class SourceAttribution(BaseModel):
    """How ONE source contributes to ONE theme cluster, with its independence + weight."""
    source_slug: str
    source_date: Optional[str] = None
    source_type: str
    access_class: str
    temporal_role: Optional[str] = None
    is_current_input: bool
    evidence_ids: list[str] = Field(default_factory=list)
    theme_candidate_ids: list[str] = Field(default_factory=list)
    contribution_type: ContributionType
    independence_group: Optional[str] = None
    source_weight: float = Field(default=1.0, ge=0.0)
    rationale: str = ""


class EvidenceBullet(BaseModel):
    """One human-readable evidence bullet backing a cluster, with provenance."""
    text: str
    evidence_ids: list[str] = Field(default_factory=list)
    source_slugs: list[str] = Field(default_factory=list)


class ThemeClusterMember(BaseModel):
    """One original (per-source) theme candidate that was merged into a cluster."""
    source_slug: str
    original_theme_name: str
    original_theme_description: Optional[str] = None
    evidence_ids: list[str] = Field(default_factory=list)
    axis_candidates: list[str] = Field(default_factory=list)
    strategy_family_hints: list[StrategyFamilyName] = Field(default_factory=list)
    temporal_role: Optional[str] = None
    similarity_score: float = Field(default=1.0, ge=0.0, le=1.0)
    rationale: str = ""
    from_hot_topic: bool = False  # the original came from a hot_topics list (attention signal)
    is_current_input: bool = True


class ThemeCluster(BaseModel):
    """One UNIQUE theme: merged members, attribution, corroboration/attention, routing."""
    cluster_id: str
    canonical_theme_name: str
    canonical_thesis: str
    theme_status: ThemeStatus
    members: list[ThemeClusterMember] = Field(default_factory=list)
    source_attributions: list[SourceAttribution] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    evidence_bullets: list[EvidenceBullet] = Field(default_factory=list)
    source_count: int = 0
    independent_source_count: int = 0
    evidence_count: int = 0
    contradiction_count: int = 0
    attention_score: float = Field(default=0.0, ge=0.0, le=1.0)
    corroboration_score: float = Field(default=0.0, ge=0.0, le=1.0)
    recency_score: float = Field(default=0.0, ge=0.0, le=1.0)
    temporal_quality: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence_attention_divergence: float = 0.0   # corroboration − attention (the p−q proxy)
    promotion_score: float = 0.0
    operational_axes: list[str] = Field(default_factory=list)
    causal_claims: list[str] = Field(default_factory=list)
    confounders: list[str] = Field(default_factory=list)
    falsifiers: list[str] = Field(default_factory=list)
    strategy_family_hints: list[StrategyFamilyName] = Field(default_factory=list)
    missing_data: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _discipline(self) -> "ThemeCluster":
        # Gate: theme_cluster_requires_source_attribution.
        if not self.source_attributions:
            raise ValueError(
                f"ThemeCluster '{self.cluster_id}' has no source_attribution — a cluster must "
                "name at least one contributing source."
            )
        # Gate: historical_case_cannot_confirm_current_theme / no_archived_case_in_phase_a.
        # A promoted cluster must rest on >=1 CURRENT-INPUT, source-backed evidence atom; a
        # purely historical/case-only cluster cannot be promote_to_discovery.
        if self.theme_status == "promote_to_discovery":
            current_evidence = any(
                a.is_current_input and a.contribution_type == "supports" and a.evidence_ids
                for a in self.source_attributions
            )
            if not current_evidence:
                raise ValueError(
                    f"ThemeCluster '{self.cluster_id}' is promote_to_discovery but has no "
                    "current-input, source-backed supporting evidence (archived/historical case "
                    "memory cannot confirm a current theme in Phase A)."
                )
        return self


class MultiSourceThemeSet(BaseModel):
    """The aggregator's deliverable: the unique ranked theme clusters for one batch."""
    model_config = ConfigDict(extra="forbid")
    batch_id: str
    source_scope: SourceScope
    source_slugs: list[str] = Field(default_factory=list)
    clusters: list[ThemeCluster] = Field(default_factory=list)
    rejected_merges: list[dict] = Field(default_factory=list)
    duplicate_theme_map: dict = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    no_trade_confirmation: str = (
        "Stage-0 theme aggregation only: unique theme clusters + discovery handoff. "
        "No trades, sizing, hedge ratios, scenario probabilities, or execution."
    )
