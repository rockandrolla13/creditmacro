"""Wiki renderer + parser + drift detection (ONTOLOGY §Rendered view, AMEND A2).

Applies to THEME (case) pages ONLY (A2). One-master: event log --fold--> θ
--render--> page. Analyst edits enter via drift-diff → proposed events
(provenance='analyst') → review queue. Bidirectional sync is forbidden.

Round-trip requirement: parse(render(θ)) == θ on all structured fields.
Phase-7 deliverable — gate: test_render_parse_roundtrip.
"""
from __future__ import annotations

from ..substrate.hypothesis import ThemeHypothesis
from ..ingest.scoring_view import ScoreView


def render(theme: ThemeHypothesis, score: ScoreView) -> str:
    """Fold + score → markdown page (mechanism, σ, d(θ), X, S_θ/B_θ, F, timeline)."""
    raise NotImplementedError("Phase 7 — render per §Rendered view normative minimum")


def parse(page_text: str) -> ThemeHypothesis:
    """Recover a ThemeHypothesis from a rendered page (roundtrip inverse of render)."""
    raise NotImplementedError("Phase 7 — gate: test_render_parse_roundtrip")


def drift_diff(rendered_expected: str, wiki_actual: str) -> list:
    """Diff → proposed ThemeEvents (provenance='analyst') for the review queue."""
    raise NotImplementedError("Phase 7 — never auto-applied; review-gated")
