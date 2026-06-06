"""
Stage 0 — Ingestion.

Takes raw research text and emits three typed streams:
  Observation     (facts)      → update Driver.current_level
  CandidateTheme  (narratives) → become ThemeObjects
  ConsensusSignal (attention)  → prior for q_s and crowding c

Then nominates CandidateThemes ranked by
    pre_screen_score = evidence_score − attention_score
which is a cheap pre-screen on p − q before any pricing is run.

The LLM-call that parses text into typed streams is stubbed.
The ranking logic (divergence computation) is real.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Optional

from .schema import (
    CandidateTheme,
    ConsensusSignal,
    IcebergClassification,
    IcebergScores,
    Observation,
)


# ── Typed stream container ────────────────────────────────────────────────────

@dataclass
class IngestionResult:
    observations: list[Observation]
    candidate_themes: list[CandidateTheme]
    consensus_signals: list[ConsensusSignal]
    ranked_candidates: list[CandidateTheme]  # sorted descending by pre_screen_score
    # Stage-0 iceberg classifications (additive; empty by default so existing
    # construction in example.py / scripted_provider.py is unaffected).
    iceberg_classifications: list[IcebergClassification] = field(default_factory=list)


# ── Evidence and attention scoring ───────────────────────────────────────────

def _evidence_score(
    theme: CandidateTheme,
    observations: list[Observation],
    recency_halflife_days: int = 30,
) -> float:
    """
    Recency-weighted count of Observations whose driver_tags overlap with
    the theme statement keywords.
    Simple proxy: count matched obs, decay by age.
    Real implementation: LLM embedding similarity + date weighting.
    """
    linked = [o for o in observations if o.id in theme.evidence_ids]
    if not linked:
        return 0.0
    # All linked obs count equally in this stub — real: weight by recency
    return float(len(linked))


def _attention_score(
    theme: CandidateTheme,
    signals: list[ConsensusSignal],
) -> float:
    """
    Strength-weighted sum of ConsensusSignals linked to this theme.
    Positive attention_strength on a topic → market already focused → high q.
    """
    linked = [s for s in signals if s.id in theme.consensus_ids]
    if not linked:
        return 0.0
    return sum(abs(s.attention_strength) for s in linked) / len(linked)


def rank_candidates(
    candidates: list[CandidateTheme],
    observations: list[Observation],
    signals: list[ConsensusSignal],
) -> list[CandidateTheme]:
    """
    For each candidate: compute evidence_score, attention_score, pre_screen_score.
    Sort descending by pre_screen_score.

    High pre_screen_score = strong factual support + low market attention
                          = likely p > q → residual edge candidate.
    """
    scored: list[CandidateTheme] = []
    for c in candidates:
        ev = _evidence_score(c, observations)
        att = _attention_score(c, signals)
        updated = c.model_copy(update={
            "evidence_score": round(ev, 4),
            "attention_score": round(att, 4),
            "pre_screen_score": round(ev - att, 4),
        })
        scored.append(updated)
    return sorted(scored, key=lambda x: x.pre_screen_score, reverse=True)


# ── Market Intelligence Iceberg Classifier (Stage-0 classification) ───────────
#
# Implements docs/market_intelligence_iceberg_classifier_skill.md: score ANY
# incoming item across the four Meadows iceberg layers, route it to its dashboard
# lane / typed stream, and decide promotion. Same sign convention as
# rank_candidates: theme_promotion = evidence − attention (here, the generalised
# evidence = structure × (pattern + event)).

# Iceberg layer → dashboard lane → Stage-0 typed stream (the doc's table).
_LAYER_TO_LANE = {
    "surface_event": "KEY_EVENTS",
    "pattern_trend": "MAIN_DEVELOPMENTS",
    "system_structure": "CORE_THEMES",
    "mental_model": "HOT_TOPICS",
}
_LAYER_TO_STREAM = {
    "surface_event": "Observation",
    "pattern_trend": "Observation",
    "system_structure": "CandidateTheme",
    "mental_model": "ConsensusSignal",
}

# Decision thresholds. "high" / "low" per the promotion + rejection rules.
STRUCTURE_HIGH = 0.5    # StructureScore considered "high" (investable mechanism + axis)
ATTENTION_HIGH = 0.5    # HotTopicAttentionScore considered "high" (loud / crowded)

_CROWDING_FLAG = (
    "crowding/risk-premium: loud attention => likely already priced, not mispriced"
)


def _layer_from_scores(s: IcebergScores) -> str:
    """Dominant iceberg layer = argmax over the four layer-representative scores.

    hot_topic_attention is NOT a layer selector — it feeds the promotion math and
    the crowding confounder. The mental_model layer is selected by mental_model.
    Ties resolve toward the deeper (more investable) layer.
    """
    # Order matters: max() returns the FIRST maximal element, so list the deeper
    # (more investable) layers first to resolve ties toward structure.
    candidates = [
        ("system_structure", s.structure),
        ("pattern_trend", s.pattern),
        ("surface_event", s.event),
        ("mental_model", s.mental_model),
    ]
    return max(candidates, key=lambda kv: kv[1])[0]


def classify_iceberg(
    item_scores: Mapping[str, float],
    operational_axis: Optional[str] = None,
) -> IcebergClassification:
    """Pure classifier. Score → layer/lane/stream → promotion decision.

    item_scores keys (all 0..1, missing ⇒ 0.0): event, pattern, structure,
    mental_model, hot_topic_attention. operational_axis is required for promotion;
    None ⇒ not yet investable.

    Promotion rules (applied EXACTLY):
      promote_to_theme  — structure high AND operational_axis present AND theme_promotion > 0
      narrative_noise   — high hot_topic_attention AND low structure
      watchlist         — structurally interesting but no axis yet, or event pending (default)

    A hot topic is NEVER promoted on attention alone.
    """
    event = float(item_scores.get("event", 0.0))
    pattern = float(item_scores.get("pattern", 0.0))
    structure = float(item_scores.get("structure", 0.0))
    mental_model = float(item_scores.get("mental_model", 0.0))
    attention = float(item_scores.get("hot_topic_attention", 0.0))

    # ThemePromotionScore = structure × (pattern + event) − attention
    #   = evidence − attention ; identical sign convention to rank_candidates.
    theme_promotion = structure * (pattern + event) - attention

    scores = IcebergScores(
        event=event,
        pattern=pattern,
        structure=structure,
        mental_model=mental_model,
        hot_topic_attention=attention,
        theme_promotion=theme_promotion,
    )

    layer = _layer_from_scores(scores)

    # Standing credit confounder: loud attention ⇒ likely already priced. Always
    # flag it (it has already pulled theme_promotion down via −attention).
    confounder_flags: list[str] = []
    if attention >= ATTENTION_HIGH:
        confounder_flags.append(_CROWDING_FLAG)

    if structure >= STRUCTURE_HIGH and operational_axis is not None and theme_promotion > 0:
        decision = "promote_to_theme"
        rationale = (
            "structure high, operational axis present, evidence exceeds attention "
            f"(theme_promotion={theme_promotion:+.3f} > 0)"
        )
    elif attention >= ATTENTION_HIGH and structure < STRUCTURE_HIGH:
        # belief layer with no system beneath it — never promoted on attention alone
        decision = "narrative_noise"
        rationale = (
            f"high attention ({attention:.2f}), low structure ({structure:.2f}): "
            "priced / crowded narrative, kept only as a prior for q"
        )
    else:
        decision = "watchlist"
        if operational_axis is None:
            rationale = "structurally interesting but no operational axis yet — re-score when it lands"
        else:
            rationale = "held for confirmation (event pending or evidence not yet > attention)"

    return IcebergClassification(
        layer=layer,
        dashboard_lane=_LAYER_TO_LANE[layer],
        typed_stream=_LAYER_TO_STREAM[layer],
        scores=scores,
        operational_axis=operational_axis,
        decision=decision,
        confounder_flags=confounder_flags,
        rationale=rationale,
    )


def _candidate_item_scores(candidate: CandidateTheme) -> dict[str, float]:
    """Derive iceberg sub-scores for a ranked CandidateTheme.

    A CandidateTheme is a system-structure item by construction, so structure=1.0;
    pattern carries the (clamped) evidence_score and attention carries the
    attention_score. This makes theme_promotion = evidence − attention, exactly the
    candidate's pre_screen_score.
    """
    return {
        "structure": 1.0,
        "pattern": min(max(candidate.evidence_score, 0.0), 1.0),
        "event": 0.0,
        "mental_model": min(max(candidate.attention_score, 0.0), 1.0),
        "hot_topic_attention": min(max(candidate.attention_score, 0.0), 1.0),
    }


def classify_candidate(
    candidate: CandidateTheme,
    operational_axis: Optional[str] = None,
) -> IcebergClassification:
    """Classify a ranked CandidateTheme into an IcebergClassification.

    operational_axis is None at Stage 0 unless an axis has already been named, so
    candidates land on the watchlist (CORE THEMES, axis pending) until one does.
    """
    c = classify_iceberg(_candidate_item_scores(candidate), operational_axis=operational_axis)
    return c.model_copy(update={"item_id": candidate.id})


# ── LLM-call stub ────────────────────────────────────────────────────────────

def parse_research_text(text: str) -> tuple[
    list[Observation],
    list[CandidateTheme],
    list[ConsensusSignal],
]:
    """
    TODO: LLM call.

    Input:  raw research document text
    Output: three typed streams

    Contract:
      - Every Observation must have a date and source.
      - Every CandidateTheme.statement must be a falsifiable, directional sentence.
      - Every ConsensusSignal must have an attention_strength in [−1, 1] (or z-score).
      - The three types must be kept SEPARATE: a theme that is a hot topic is
        both a CandidateTheme AND a ConsensusSignal; emit both, do not collapse.

    Why separation matters:
      A sentence appearing as both a CandidateTheme (strong evidence_score)
      AND a ConsensusSignal (high attention_score) will score LOW on
      pre_screen_score — the market has already priced the story.
      A theme with evidence but no consensus signal scores HIGH — latent edge.
    """
    raise NotImplementedError(
        "parse_research_text: stub. "
        "Replace with LLM call that parses text into three typed streams.\n"
        "Prompt contract:\n"
        "  - Classify each sentence as Observation / CandidateTheme / ConsensusSignal\n"
        "  - A sentence can be multiple types — emit all applicable\n"
        "  - Observations: must be falsifiable facts (developments, events, data)\n"
        "  - CandidateThemes: must be directional narratives (secular / cyclical)\n"
        "  - ConsensusSignals: must reflect WHAT THE MARKET IS FOCUSED ON, not what "
        "the author believes"
    )


# ── Main ingestion entry point ────────────────────────────────────────────────

def ingest(
    text: str,
    top_n: int = 5,
    observations: Optional[list[Observation]] = None,
    signals: Optional[list[ConsensusSignal]] = None,
) -> IngestionResult:
    """
    Full Stage 0 pipeline.
    Returns an IngestionResult with ranked CandidateThemes.

    When parse_research_text is stubbed, caller may pass pre-built
    observations and signals directly (used in example.py).
    """
    if observations is None or signals is None:
        obs, candidates, sigs = parse_research_text(text)
    else:
        # Allow caller to inject pre-built streams (for testing / worked example)
        obs = observations
        sigs = signals
        candidates = []  # caller must also inject candidates if bypassing LLM

    ranked = rank_candidates(candidates, obs, sigs)
    top = ranked[:top_n]

    # Stage-0 iceberg classification of the ranked candidates (routing + promotion).
    classifications = [classify_candidate(c) for c in top]

    return IngestionResult(
        observations=obs,
        candidate_themes=candidates,
        consensus_signals=sigs,
        ranked_candidates=top,
        iceberg_classifications=classifications,
    )


def print_ranked_candidates(result: IngestionResult) -> None:
    """Print the pre-screen ranking table."""
    print("\n── Stage 0: Ranked CandidateThemes (pre-screen on p − q) ──")
    print(f"{'Rank':<5} {'Pre-screen':>11} {'Evidence':>9} {'Attention':>10}  Statement")
    print("─" * 90)
    for i, c in enumerate(result.ranked_candidates, 1):
        stmt = c.statement[:60] + "…" if len(c.statement) > 60 else c.statement
        print(
            f"{i:<5} {c.pre_screen_score:>+11.3f} "
            f"{c.evidence_score:>9.3f} {c.attention_score:>10.3f}  {stmt}"
        )
    print()
