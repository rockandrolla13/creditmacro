"""Case-B wiki import + revision replayer (ONTOLOGY §Bitemporal, D-04). Phase-2.

SCOPE (D-04): imports ONLY the 4 WF-surviving curated themes. Everything else is
handled by forward re-ingest (admission), not import.

Per theme: extract (M, σ, X, H, F) from the page → CREATED event at import date +
one synthetic prior-mass row (s_prior ∈ {1,2,3}, decays at half-life). t_x is
NEVER backdated in Case B (§Scoring). Revision replayer: mechanism-text cosine ≥
COS_COSMETIC → no event; else structural diff on extracted chains decides the
event type (§Event semantics).

Highest-risk module in the plan (backdating path I7) — gated first by the as-of
property tests.
"""
from __future__ import annotations

# The only pages this module may import as themes (D-04). Any other page routes
# to forward re-ingest, never here.
CURATED_WF_SURVIVORS = (
    "ai-capex-funding-credit-ecosystem",
    "hyperscaler-project-bond-basis",
    "hy-hpc-crowding-and-supply",
    "data-center-index-inclusion-technicals",
)


def import_curated(slug: str, page_text: str) -> None:
    """Emit CREATED + synthetic prior-mass for one curated survivor. Phase-2."""
    raise NotImplementedError("Phase 2 — gate: test_golden_revisions (CREATED + prior mass)")


def replay_revision(slug: str, prev_text: str, new_text: str) -> None:
    """Cosmetic pre-filter (COS_COSMETIC) then structural diff → event or nothing."""
    raise NotImplementedError("Phase 2 — cosmetic→none; mechanism-refine→MECHANISM_REVISED; axis→AXIS_REVISED")
