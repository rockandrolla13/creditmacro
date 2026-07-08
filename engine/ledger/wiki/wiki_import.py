"""Case-B wiki import + revision replayer (ONTOLOGY §Identity, §WF, §Event, §Scoring).

SCOPE (D-04): imports ONLY the curated WF-surviving themes. Everything else goes
through forward re-ingest (admission), not import.

- `extract`     : page text → WikiCandidate (M, σ, X, H, F) or NEEDS_STRUCTURING
                  with the failing WF clause named. Deterministic frontmatter parser
                  (golden + curated pages carry a machine-readable chain); an LLM
                  extractor for arbitrary prose is a later seam.
- `replay`      : consecutive candidates → event tuple. Mechanism-text cosine ≥
                  COS_COSMETIC suppresses mechanism-origin events (pre-filter, §Event);
                  σ flip and X/H/F changes are always decided structurally.
- `import_curated`: emit CREATED at import date + a synthetic prior-mass seed
                  (s_prior ∈ {1,2,3}); t_x is never backdated (§Scoring Case-B, I7).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import yaml

from ..constants import COS_COSMETIC
from ..substrate.events import EventType, Provenance, ThemeEvent
from ..substrate.hypothesis import Mechanism, TransmissionEdge
from ..substrate.identity import equiv, wf_predicate
from ..textsim import bow_cosine

# The only pages this module may import as themes (D-04).
CURATED_WF_SURVIVORS = (
    "ai-capex-funding-credit-ecosystem",
    "hyperscaler-project-bond-basis",
    "hy-hpc-crowding-and-supply",
    "data-center-index-inclusion-technicals",
)


@dataclass(frozen=True)
class WikiCandidate:
    """Extractor output — the (M, σ, X, H, F) tuple plus the prose used for the
    mechanism-text cosine pre-filter. Satisfies substrate.hypothesis.ThemeShape."""
    mechanism: Mechanism
    shock_direction: int
    operational_axis: str
    horizon_days: int
    falsifier: str
    mechanism_text: str


@dataclass(frozen=True)
class ExtractResult:
    candidate: Optional[WikiCandidate]
    failing_clause: Optional[str] = None

    @property
    def needs_structuring(self) -> bool:
        return self.candidate is None


@dataclass(frozen=True)
class PriorMassSeed:
    """Synthetic prior-evidence row for a wiki-imported theme (§Scoring Case-B)."""
    theme_id: str
    s_prior: int          # ∈ {1, 2, 3}
    t_import: str         # ISO; decays at the standard half-life


def _parse_frontmatter(page_text: str) -> dict:
    parts = page_text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("page has no YAML frontmatter block")
    return yaml.safe_load(parts[1])


def extract(page_text: str) -> ExtractResult:
    """Parse a page into a WikiCandidate, then gate on WF. Fail → NEEDS_STRUCTURING."""
    fm = _parse_frontmatter(page_text)
    edges = tuple(
        TransmissionEdge(v_from=a, v_to=b, sign=int(s)) for a, b, s in fm["mechanism"]
    )
    candidate = WikiCandidate(
        mechanism=Mechanism(edges=edges),
        shock_direction=int(fm["shock_direction"]),
        operational_axis=str(fm["operational_axis"]),
        horizon_days=int(fm["horizon_days"]),
        falsifier=str(fm["falsifier"]),
        mechanism_text=str(fm["mechanism_text"]),
    )
    wf = wf_predicate(candidate)
    if not wf.ok:
        return ExtractResult(candidate=None, failing_clause=wf.failing_clause)
    return ExtractResult(candidate=candidate)


def mechanism_text_cosine(a: str, b: str) -> float:
    """§Event cosmetic pre-filter — the shared deterministic embedder seam (textsim)."""
    return bow_cosine(a, b)


def replay(prev: WikiCandidate, new: WikiCandidate) -> tuple[EventType, ...]:
    """Decide the event(s) for a prev→new revision (§Event semantics)."""
    # σ flip is a genuine new hypothesis regardless of mechanism-text similarity.
    if new.shock_direction != prev.shock_direction:
        return (EventType.RETIRED, EventType.CREATED)

    events: list[EventType] = []
    # Mechanism: cosine ≥ COS_COSMETIC → deemed unchanged (pre-filter); else structural.
    if mechanism_text_cosine(prev.mechanism_text, new.mechanism_text) < COS_COSMETIC:
        if not equiv(new.mechanism, prev.mechanism):
            return (EventType.RETIRED, EventType.CREATED)      # M' ≇ M
        if new.mechanism != prev.mechanism:
            events.append(EventType.MECHANISM_REVISED)          # ≅ refinement

    # Non-mechanism attributes are exact fields, always compared structurally.
    if new.operational_axis != prev.operational_axis:
        events.append(EventType.AXIS_REVISED)
    if new.horizon_days != prev.horizon_days:
        events.append(EventType.HORIZON_EXTENDED)
    if new.falsifier != prev.falsifier:
        events.append(EventType.FALSIFIER_REVISED)
    return tuple(events)


def import_curated(
    slug: str, candidate: WikiCandidate, *, import_date: str, s_prior: int = 2
) -> tuple[ThemeEvent, PriorMassSeed]:
    """Emit a CREATED event + synthetic prior-mass seed for one curated survivor."""
    if s_prior not in (1, 2, 3):
        raise ValueError(f"s_prior must be in {{1,2,3}}, got {s_prior}")
    theme_id = f"wiki:{slug}"
    event = ThemeEvent(
        event_id=f"{theme_id}:created",
        theme_id=theme_id,
        event_type=EventType.CREATED,
        payload={
            "mechanism": candidate.mechanism.model_dump(),
            "shock_direction": candidate.shock_direction,
            "operational_axis": candidate.operational_axis,
            "horizon_days": candidate.horizon_days,
            "falsifier": candidate.falsifier,
        },
        effective_at=import_date,          # recorded_at left None — store stamps it (I7)
        provenance=Provenance.WIKI_IMPORT,
    )
    seed = PriorMassSeed(theme_id=theme_id, s_prior=s_prior, t_import=import_date)
    return event, seed
