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

from dataclasses import dataclass
from typing import Optional

from .schema import CandidateTheme, ConsensusSignal, Observation


# ── Typed stream container ────────────────────────────────────────────────────

@dataclass
class IngestionResult:
    observations: list[Observation]
    candidate_themes: list[CandidateTheme]
    consensus_signals: list[ConsensusSignal]
    ranked_candidates: list[CandidateTheme]  # sorted descending by pre_screen_score


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

    return IngestionResult(
        observations=obs,
        candidate_themes=candidates,
        consensus_signals=sigs,
        ranked_candidates=ranked[:top_n],
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
