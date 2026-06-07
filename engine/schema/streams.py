"""Stage-0 typed streams + the Market-Intelligence Iceberg classifier outputs."""
from __future__ import annotations

import uuid
from typing import Literal, Optional

from pydantic import BaseModel, Field

# ── Stage 0 typed streams ─────────────────────────────────────────────────────

class Observation(BaseModel):
    """Dated, sourced fact."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    date: str                    # ISO date of the observation
    source: str                  # e.g. "Citi credit weekly 2024-11-08"
    text: str                    # verbatim or paraphrased fact
    driver_tags: list[str] = []  # which Driver.name fields this updates

class CandidateTheme(BaseModel):
    """Durable narrative: the secular / cyclical story."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    statement: str
    horizon: str
    evidence_ids: list[str] = []   # Observation ids that support this theme
    consensus_ids: list[str] = []  # ConsensusSignal ids that measure attention

    # Stage 0 scoring — cheap p−q pre-screen
    evidence_score: float = 0.0    # recency-weighted count of supporting Observations
    attention_score: float = 0.0   # strength-weighted ConsensusSignal support
    pre_screen_score: float = 0.0  # evidence_score − attention_score ≈ p−q proxy

class ConsensusSignal(BaseModel):
    """Market attention / positioning."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    source: str                    # e.g. "TAARSS", "DB_flow_report", "GS_survey"
    topic: str
    attention_strength: float      # z-score or normalised [0, 1]
    direction: Literal["positive", "negative", "neutral"]
    date: str

# ── Stage 0: Market Intelligence Iceberg Classifier ──────────────────────────

class IcebergScores(BaseModel):
    """The six 0..1 sub-scores of the iceberg classifier (Meadows levels)."""
    event: float = 0.0              # EventScore: datedness × catalyst_potential
    pattern: float = 0.0           # PatternScore: persistence × breadth_of_trend
    structure: float = 0.0         # StructureScore: has_mechanism × has_operational_axis
    mental_model: float = 0.0      # MentalModelScore: how entrenched the belief is
    hot_topic_attention: float = 0.0  # HotTopicAttentionScore: current attention / crowding
    theme_promotion: float = 0.0   # ThemePromotionScore (may be negative)

class IcebergClassification(BaseModel):
    """One classified ingestion item: its iceberg layer, dashboard lane, typed"""
    layer: Literal[
        "surface_event", "pattern_trend", "system_structure", "mental_model"
    ]
    dashboard_lane: Literal[
        "KEY_EVENTS", "MAIN_DEVELOPMENTS", "CORE_THEMES", "HOT_TOPICS"
    ]
    typed_stream: Literal["Observation", "CandidateTheme", "ConsensusSignal"]
    scores: IcebergScores
    operational_axis: Optional[str] = None   # required for promotion; null ⇒ not yet investable
    decision: Literal["promote_to_theme", "watchlist", "narrative_noise"]
    confounder_flags: list[str] = []
    item_id: Optional[str] = None
    rationale: str = ""
