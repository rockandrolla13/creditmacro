"""The twelve lifecycle decisions (PLAN-theme-lifecycle.md §6) as named constants.

§6 marks all twelve **resolved and binding on the build** (2026-08-09). They live here as
module constants under one version stamp — never as function defaults — so that changing
one is a reviewed code change plus a bump, and every past pack and book stays interpretable
against the version it was built under. This mirrors `CONFIDENCE_VERSION` (harness D4).

TWO OF THE TWELVE CANNOT BE EXPRESSED IN CODE YET. Both are flagged below with the reason
and the constant that stays empty until a human ratifies a translation. A decision stated in
vocabulary the codebase does not have is not yet a buildable decision, and writing a plausible
translation here would be exactly the unsourced default this repo refuses.
"""
from __future__ import annotations

from typing import Final

#: Bumped whenever any constant below changes. Stamped onto every emitted lifecycle object.
LIFECYCLE_DECISIONS_VERSION: Final[str] = "lifecycle-decisions/1"


# ── A1 — regime discovery ────────────────────────────────────────────────────

#: D-A1-1 — regime vocabulary is capped 3..7. Fewer than three ⇒ A1 halts and keeps last
#: week's vocabulary with `stale_regime=True`. No false-narrow.
REGIME_COUNT_FLOOR: Final[int] = 3
REGIME_COUNT_CAP: Final[int] = 7

#: D-A1-2 / D-A2-2 — assessment cadence: weekly by default, manual re-fire on large ingests
#: or on request. NEVER automatic on ingest.
ASSESSMENT_CADENCE: Final[str] = "weekly"
ASSESSMENT_AUTOMATIC_ON_INGEST: Final[bool] = False

#: D-A1-3 — A1 clusters on OPINION-BEARING atoms only; a regime is the market's posture, not
#: its measurement.
#:
#: BLOCKED, and deliberately left empty. §6 states the rule as
#: ``claim_kind in {view, forecast, framing, mechanism}``, excluding
#: ``{measurement, level, tabular}``. **None of those seven strings exist in this codebase.**
#: The two real vocabularies are:
#:
#:   * ``engine.temporal.ClaimKind`` — historical_fact, historical_forecast, source_opinion,
#:     current_fact, current_forecast, method_rule, unknown
#:   * ``engine.evidence_extraction._claim_kind`` — source_opinion, source_forecast, source_fact
#:
#: A mapping is guessable (view→source_opinion, forecast→source_forecast/current_forecast),
#: but "framing" and "mechanism" have no counterpart — a mechanism is a *causal claim*, a
#: separate extraction stream, not a claim kind at all. Filling this in from inference would
#: silently redefine what a regime is. It needs one human sentence; until then A1 refuses.
OPINION_CLAIM_KINDS: Final[frozenset[str]] = frozenset()
OPINION_CLAIM_KINDS_UNRESOLVED: Final[str] = (
    "D-A1-3 names claim kinds {view, forecast, framing, mechanism} that no extractor in this "
    "repo emits. Ratify a mapping onto engine.temporal.ClaimKind before A1 can cluster."
)


# ── A2 — theme discovery + factor mapping ────────────────────────────────────

#: D-A2-1 — dedup thresholds per asset class. Cross-asset takes the stricter of the two so
#: cross-class merging is deliberate; "other" is a placeholder pending data.
DEDUP_THRESHOLDS: Final[dict[str, float]] = {
    "ig": 0.85,
    "hy": 0.75,
    "cross_asset": 0.85,
    "other": 0.80,
}

#: A2 supplies lifecycle DEFAULTS only; surveillance owns runtime state from the first tick.
INITIAL_HALF_LIFE_DAYS: Final[int] = 21
INITIAL_MAX_LIFE_DAYS: Final[int] = 90

#: D-A2-3 — consensus quarantine. Extra sell-side agreement SPLITS: a small bump to support
#: (the theme exists), a larger bump to consensus, a larger bump still to crowding. Consensus
#: is evidence of crowding, not of truth. Per additional independent publisher.
CONSENSUS_SUPPORT_DELTA: Final[float] = 0.10
CONSENSUS_CONSENSUS_DELTA: Final[float] = 0.20
CONSENSUS_CROWDING_DELTA: Final[float] = 0.25

#: D-A2-4 — a theme shipped without an `AdversarialCase` is rejected at A2 emit. A theme
#: without a challenger is a theme without a fair test.
ADVERSARIAL_CASE_REQUIRED: Final[bool] = True

#: D-A2-5 — minimum typed falsification triggers per theme.
MIN_FALSIFICATION_TRIGGERS: Final[int] = 1

#: D-A2-6 — the four narrative-surprise axes, scored alongside L2's per-atom numeric surprise.
SURPRISE_AXES: Final[tuple[str, ...]] = (
    "narrative_surprise",
    "market_surprise",
    "revision_surprise",
    "contradiction_surprise",
)


# ── L2 — surprise vs level ───────────────────────────────────────────────────

#: D-L2-1 — expectation source is TIERED: a grounded consensus span first, the prior print as
#: fallback, NEVER a model-generated expectation. None available ⇒ kind="level", which cannot
#: move status toward `confirming`.
EXPECTATION_TIERS: Final[tuple[str, ...]] = ("grounded_consensus", "prior_print")
MODEL_GENERATED_EXPECTATION_ALLOWED: Final[bool] = False


# ── L3 — evidence packs ──────────────────────────────────────────────────────

#: D-L3-1 — packs keep full raw atom text for 24 months, then age it out. Metadata, outcomes
#: and scorecard inputs are kept forever.
PACK_FULL_RETENTION_MONTHS: Final[int] = 24


# ── L4 — the weekly book ─────────────────────────────────────────────────────

#: D-L4-1 — Monday morning, private to the PM. Distribution decided once the format has
#: earned trust.
BOOK_RENDER_WEEKDAY: Final[str] = "monday"
BOOK_RECIPIENTS: Final[tuple[str, ...]] = ("pm",)


# ── L5 — factor projection + expression gate ─────────────────────────────────

#: D-L5-1 — residual-alpha share below this ⇒ tractability fails and the RV layer is disabled.
#: Revisit after a quarter of data.
RESIDUAL_ALPHA_THRESHOLD: Final[float] = 0.40

#: The aliveness half of L5's two-part gate. A theme can be perfectly true and still fail it.
ALIVE_STATUSES: Final[frozenset[str]] = frozenset({"armed", "confirming"})
