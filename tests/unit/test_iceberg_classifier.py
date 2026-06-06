"""
Market Intelligence Iceberg Classifier — Stage-0 classification stage.

Spec: docs/market_intelligence_iceberg_classifier_skill.md

Tests the pure classifier:
  - layer ↔ lane ↔ typed_stream mapping (Meadows iceberg → dashboard → typed stream)
  - ThemePromotionScore = StructureScore × (PatternScore + EventScore) − HotTopicAttentionScore
  - promotion_rules (promote_to_theme / watchlist / narrative_noise)
  - rejection_rules (a hot topic is NEVER promoted on attention alone; crowding confounder)
"""
from __future__ import annotations

import pytest

from engine.schema import IcebergClassification, IcebergScores
from engine.stage0 import classify_iceberg


# ── promotion_rules ───────────────────────────────────────────────────────────

def test_promote_to_theme_high_structure_axis_present_positive_promotion():
    c = classify_iceberg(
        {"event": 0.60, "pattern": 0.56, "structure": 0.90, "hot_topic_attention": 0.40},
        operational_axis="HY HPC OAS − hyperscaler IG OAS, duration-adjusted, bps",
    )
    assert c.decision == "promote_to_theme"
    assert c.layer == "system_structure"
    assert c.dashboard_lane == "CORE_THEMES"
    assert c.typed_stream == "CandidateTheme"
    # 0.90 × (0.56 + 0.60) − 0.40 = +0.644
    assert c.scores.theme_promotion == pytest.approx(0.644)
    assert c.scores.theme_promotion > 0


def test_watchlist_structurally_interesting_but_no_axis():
    c = classify_iceberg(
        {"event": 0.60, "pattern": 0.56, "structure": 0.80, "hot_topic_attention": 0.30},
        operational_axis=None,
    )
    assert c.decision == "watchlist"
    assert c.operational_axis is None


def test_narrative_noise_high_attention_low_structure():
    c = classify_iceberg(
        {"pattern": 0.0, "event": 0.0, "structure": 0.10,
         "mental_model": 0.85, "hot_topic_attention": 0.80},
        operational_axis=None,
    )
    assert c.decision == "narrative_noise"
    assert c.layer == "mental_model"
    assert c.dashboard_lane == "HOT_TOPICS"
    assert c.typed_stream == "ConsensusSignal"
    # crowding / risk-premium confounder flag must be raised on loud attention
    assert any("crowding" in f.lower() for f in c.confounder_flags)


def test_hot_topic_never_promoted_on_attention_alone():
    # Loud attention, an axis even exists, but structure is low → must NOT promote.
    c = classify_iceberg(
        {"structure": 0.10, "pattern": 0.0, "event": 0.0,
         "mental_model": 0.90, "hot_topic_attention": 0.90},
        operational_axis="some axis",
    )
    assert c.decision != "promote_to_theme"
    assert c.decision == "narrative_noise"


# ── scoring_model ─────────────────────────────────────────────────────────────

def test_theme_promotion_formula_numeric():
    # ThemePromotionScore = structure × (pattern + event) − attention
    c = classify_iceberg(
        {"structure": 0.5, "pattern": 0.4, "event": 0.2, "hot_topic_attention": 0.3},
    )
    expected = 0.5 * (0.4 + 0.2) - 0.3   # = 0.0
    assert c.scores.theme_promotion == pytest.approx(expected)


def test_promotion_sign_matches_evidence_minus_attention():
    # Same sign convention as rank_candidates' pre_screen_score = evidence − attention:
    # with structure=1 and event=0, theme_promotion == pattern − attention.
    c = classify_iceberg({"structure": 1.0, "pattern": 0.7, "event": 0.0,
                          "hot_topic_attention": 0.2})
    assert c.scores.theme_promotion == pytest.approx(0.7 - 0.2)


# ── classification_rules: layer ↔ lane ↔ typed_stream ─────────────────────────

@pytest.mark.parametrize(
    "dominant,exp_layer,exp_lane,exp_stream",
    [
        ("event",     "surface_event",    "KEY_EVENTS",        "Observation"),
        ("pattern",   "pattern_trend",    "MAIN_DEVELOPMENTS", "Observation"),
        ("structure", "system_structure", "CORE_THEMES",       "CandidateTheme"),
        ("mental_model", "mental_model",  "HOT_TOPICS",        "ConsensusSignal"),
    ],
)
def test_layer_lane_stream_mapping(dominant, exp_layer, exp_lane, exp_stream):
    scores = {"event": 0.1, "pattern": 0.1, "structure": 0.1, "mental_model": 0.1}
    scores[dominant] = 0.9
    c = classify_iceberg(scores)
    assert c.layer == exp_layer
    assert c.dashboard_lane == exp_lane
    assert c.typed_stream == exp_stream


def test_returns_iceberg_classification_with_typed_scores():
    c = classify_iceberg({"structure": 0.9, "pattern": 0.5, "event": 0.5},
                         operational_axis="x")
    assert isinstance(c, IcebergClassification)
    assert isinstance(c.scores, IcebergScores)
