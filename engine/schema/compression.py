"""Theme compression — schemas for the analyst layer (docs/THEME_DISCIPLINE_AND_FAILURE_MODES.md).

The aggregator's job is RECALL: it surfaces every candidate theme it can find, flat. This
layer's job is PRECISION: compress that flat list into the 3–7 parent themes a human analyst
would actually carry, each one carrying the reason it survived — and an explicit account of
everything that did not.

    MultiSourceThemeSet (flat clusters) → AnalystThemeMap (parent/subtheme, capped, gated)

DISCIPLINE:
  * A parent theme is the CAUSAL STORY ("growth is recovering but rates have not priced it").
    It is NOT a direction of expression. No direction, no instrument, no leg, no size, no
    hedge ratio, no execution — here or in the readout.
  * The promotion gate is a GATE, not a warning: `ParentTheme` structurally cannot be built
    without evidence + mechanism + axis-or-watchlist + falsifier + temporal status + ≥1
    routable family + a selection rationale.
  * Nothing is dropped silently. Every theme that does not become a parent theme appears in
    `rejected_or_merged_themes`, `hot_topics_not_promoted` or `outcome_candidates`, each
    entry carrying a reason.
  * Frozen models, tuple fields, deterministic ordering — no wall clock anywhere.
"""
from __future__ import annotations

import re
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .theme_aggregation import ROUTABLE_FAMILIES, StrategyFamilyName

# ── vocabularies ─────────────────────────────────────────────────────────────

#: A parent theme is either live ("current") or a closed forecast we can only score after
#: the fact ("historical_outcome_candidate"). The latter is never promoted.
TemporalStatus = Literal["current", "historical_outcome_candidate"]

#: The seven things a parent theme must have. Missing ANY one ⇒ not promoted.
PROMOTION_REQUIREMENTS: tuple[str, ...] = (
    "evidence",
    "mechanism",
    "axis_or_watchlist",
    "falsifier",
    "temporal_status",
    "routable_family",
    "selection_rationale",
)

#: Why a candidate theme did not become a parent theme. Every demotion carries one.
DemotionReasonCode = Literal[
    # the six downgrade rules (spec § "Downgrade rules")
    "attention_without_evidence",
    "no_operational_axis",
    "no_causal_chain",
    "only_source_opinion",
    "historical_forecast_without_outcome_check",
    "no_falsifier",
    # structural outcomes
    "no_routable_family",
    "merged_into_parent",
    "parent_cap_exceeded",
    "rejected_upstream",
    "gate_failed",
    # synthesis-integrity rejections (the LLM proposed something it could not back)
    "ungrounded_synthesis",
    "trade_language",
    "direction_leak",
    "malformed_synthesis",
]

#: Where a demoted theme ended up. `subtheme` never appears in the demotion lists — a
#: subtheme is preserved INSIDE its parent, it is not a demotion.
DemotionDestination = Literal["watchlist", "merged", "rejected", "outcome_candidate"]

#: Why two themes under the same driver were kept apart instead of merged.
KeepSeparateReason = Literal[
    "different_outcome",
    "different_mechanism",
    "different_axis",
    "different_temporal_status",
    "different_strategy_family",
    "representative",
]

_HAS_DIGIT = re.compile(r"\d")


# ── the pieces of a parent theme ─────────────────────────────────────────────

class CausalMechanism(BaseModel):
    """driver → transmission → outcome. The causal story, stated in three parts so the
    transmission cannot be skipped (a driver next to an outcome is a correlation, not a
    mechanism)."""
    model_config = ConfigDict(frozen=True)
    driver: str
    transmission: str
    outcome: str

    @model_validator(mode="after")
    def _all_three_present(self) -> "CausalMechanism":
        for field_name in ("driver", "transmission", "outcome"):
            if not str(getattr(self, field_name)).strip():
                raise ValueError(
                    f"CausalMechanism.{field_name} is empty — a mechanism needs all three of "
                    "driver, transmission and outcome."
                )
        return self

    def as_sentence(self) -> str:
        return f"{self.driver} → {self.transmission} → {self.outcome}"


class ThemeFalsifier(BaseModel):
    """The discovery-stage falsifier: an OBSERVABLE plus a THRESHOLD.

    The counterpart of `engine.schema.risk.Falsifier`, which demands a numeric τ because by
    expression stage the axis is a real series. At discovery the threshold is still prose
    ("above 120bp for two consecutive weeks"), so it is a string — but it must contain a
    number, because a 'threshold' with no level in it is not a threshold.
    """
    model_config = ConfigDict(frozen=True)
    observable: str
    threshold: str
    kill_rule: str = ""

    @model_validator(mode="after")
    def _observable_and_threshold(self) -> "ThemeFalsifier":
        if not self.observable.strip():
            raise ValueError("ThemeFalsifier.observable is empty — a falsifier needs something to watch.")
        if not self.threshold.strip():
            raise ValueError("ThemeFalsifier.threshold is empty — a falsifier needs a level.")
        if not _HAS_DIGIT.search(self.threshold):
            raise ValueError(
                f"ThemeFalsifier.threshold '{self.threshold}' carries no number — a threshold "
                "without a level is an opinion, not a falsifier."
            )
        return self


class Subtheme(BaseModel):
    """One candidate theme kept UNDER a parent rather than merged into it or split out.

    It exists because of a keep-separate rule: same driver, but a different outcome /
    mechanism / axis / temporal status. Its own axes survive here — that is the whole point
    of not flattening it away.
    """
    model_config = ConfigDict(frozen=True)
    subtheme_id: str
    name: str
    source_cluster_id: str
    keep_separate_reason: KeepSeparateReason
    operational_axes: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    source_slugs: tuple[str, ...] = ()
    temporal_status: TemporalStatus = "current"
    causal_claims: tuple[str, ...] = ()


class EvidenceBySource(BaseModel):
    """One source's contribution to one parent theme."""
    model_config = ConfigDict(frozen=True)
    source_slug: str
    evidence_ids: tuple[str, ...] = ()
    contribution_type: str = "supports"
    is_current_input: bool = True


class ParentTheme(BaseModel):
    """One of the 3–7 themes a human analyst would actually carry.

    The model IS the promotion gate: every requirement in `PROMOTION_REQUIREMENTS` is a
    validated field, so an object of this type cannot exist without all seven. Callers that
    want to *ask* whether a candidate would pass use `engine.compression.evaluate_gate`,
    which reports the missing pieces instead of raising.
    """
    model_config = ConfigDict(frozen=True)

    parent_id: str
    name: str                                       # the causal story; never a direction
    mechanism: CausalMechanism
    subthemes: tuple[Subtheme, ...] = ()
    evidence_by_source: tuple[EvidenceBySource, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    operational_axis: Optional[str] = None          # a named spread/slope …
    watchlist_tag: Optional[str] = None             # … or an explicit watchlist tag
    temporal_status: TemporalStatus
    strategy_families: tuple[StrategyFamilyName, ...] = ()   # 1–2 ROUTABLE families
    why_it_matters: str
    why_it_might_be_wrong: str
    falsifier: ThemeFalsifier
    selection_rationale: str                        # the stated reason it was selected
    missing_data: tuple[str, ...] = ()
    merged_cluster_ids: tuple[str, ...] = ()        # clusters folded in under the merge rule
    member_cluster_ids: tuple[str, ...] = ()        # every cluster this parent covers
    evidence_count: int = Field(default=0, ge=0)
    independent_source_count: int = Field(default=0, ge=0)
    contradiction_count: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def _promotion_gate(self) -> "ParentTheme":
        if not self.name.strip():
            raise ValueError(f"ParentTheme '{self.parent_id}' has no name.")
        # `mechanism` is a required field and `CausalMechanism` validates its three parts, so
        # the mechanism requirement is met structurally rather than checked here.
        missing: list[str] = []
        if not self.evidence_ids or not self.evidence_by_source:
            missing.append("evidence")
        if not (self.operational_axis or self.watchlist_tag):
            missing.append("axis_or_watchlist")
        families = [f for f in self.strategy_families if f in ROUTABLE_FAMILIES]
        if not families:
            missing.append("routable_family")
        if len(self.strategy_families) > 2:
            raise ValueError(
                f"ParentTheme '{self.parent_id}' names {len(self.strategy_families)} strategy "
                "families — the spec allows one or two, not a shopping list."
            )
        if not self.selection_rationale.strip():
            missing.append("selection_rationale")
        if not self.why_it_matters.strip():
            missing.append("selection_rationale")
        if missing:
            raise ValueError(
                f"ParentTheme '{self.parent_id}' fails the promotion gate — missing "
                f"{sorted(set(missing))}. A theme missing any of {list(PROMOTION_REQUIREMENTS)} "
                "is not a parent theme."
            )
        if self.temporal_status != "current":
            raise ValueError(
                f"ParentTheme '{self.parent_id}' is {self.temporal_status} — a historical-only "
                "theme is emitted as an outcome candidate, never promoted."
            )
        return self


# ── the "why not" side ───────────────────────────────────────────────────────

class DemotedTheme(BaseModel):
    """A candidate that did not become a parent theme, and the reason. Nothing vanishes."""
    model_config = ConfigDict(frozen=True)
    cluster_id: str
    theme_name: str
    destination: DemotionDestination
    reason_code: DemotionReasonCode
    reason: str
    merged_into: Optional[str] = None               # parent_id, when destination == "merged"
    attention_score: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence_count: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def _reason_is_stated(self) -> "DemotedTheme":
        if not self.reason.strip():
            raise ValueError(
                f"DemotedTheme '{self.cluster_id}' carries no reason — a theme that vanishes "
                "without a recorded reason is exactly the failure this stage exists to prevent."
            )
        return self


# ── cross-source coverage matrix ─────────────────────────────────────────────

class CoverageCell(BaseModel):
    """One theme × one source."""
    model_config = ConfigDict(frozen=True)
    source_slug: str
    present: bool
    contribution_type: str = "absent"
    evidence_count: int = Field(default=0, ge=0)


class CoverageRow(BaseModel):
    """One row of the theme × source matrix, with the contradiction column."""
    model_config = ConfigDict(frozen=True)
    theme_id: str
    theme_name: str
    cells: tuple[CoverageCell, ...] = ()
    evidence_count: int = Field(default=0, ge=0)
    independent_sources: int = Field(default=0, ge=0)
    contradictions: int = Field(default=0, ge=0)
    contradiction_note: str = ""
    status: Literal["promote", "watchlist", "outcome_candidate", "rejected"]


class SourceCoverageMatrix(BaseModel):
    """theme × source corroboration, so it is visible and auditable rather than asserted."""
    model_config = ConfigDict(frozen=True)
    source_slugs: tuple[str, ...] = ()
    rows: tuple[CoverageRow, ...] = ()


# ── the deliverable ──────────────────────────────────────────────────────────

class CompressionStats(BaseModel):
    """The audit counts. `clusters_in` must equal everything accounted for downstream."""
    model_config = ConfigDict(frozen=True)
    clusters_in: int = Field(default=0, ge=0)
    parent_themes_out: int = Field(default=0, ge=0)
    subthemes_out: int = Field(default=0, ge=0)
    merged_count: int = Field(default=0, ge=0)
    demoted_to_watchlist_count: int = Field(default=0, ge=0)
    rejected_count: int = Field(default=0, ge=0)
    outcome_candidate_count: int = Field(default=0, ge=0)


class AnalystThemeMap(BaseModel):
    """What the compression stage hands to discovery: parent themes only, capped and gated,
    plus the full account of what was left behind."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    batch_id: str
    parent_cap: int = Field(default=7, ge=1)
    parent_themes: tuple[ParentTheme, ...] = ()
    source_coverage_matrix: SourceCoverageMatrix = SourceCoverageMatrix()
    rejected_or_merged_themes: tuple[DemotedTheme, ...] = ()
    hot_topics_not_promoted: tuple[DemotedTheme, ...] = ()
    outcome_candidates: tuple[DemotedTheme, ...] = ()
    human_readout: str = ""
    stats: CompressionStats = CompressionStats()
    warnings: tuple[str, ...] = ()
    no_trade_confirmation: str = (
        "Analyst theme compression only: parent themes, subthemes, coverage and the reasons "
        "for every demotion. No trades, legs, sizing, hedge ratios, or execution."
    )

    @model_validator(mode="after")
    def _discipline(self) -> "AnalystThemeMap":
        if len(self.parent_themes) > self.parent_cap:
            raise ValueError(
                f"AnalystThemeMap '{self.batch_id}' emits {len(self.parent_themes)} parent "
                f"themes over a cap of {self.parent_cap}."
            )
        ids = [p.parent_id for p in self.parent_themes]
        if len(set(ids)) != len(ids):
            raise ValueError(f"AnalystThemeMap '{self.batch_id}' has duplicate parent_ids: {ids}")
        return self
