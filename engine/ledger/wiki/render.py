"""Wiki renderer + parser + drift detection (ONTOLOGY §Rendered view, AMEND A2).

Applies to THEME (case) pages ONLY. One-master: event log --fold--> θ --render-->
page. `parse` recovers a ThemeHypothesis VIA fold (I5-safe — it never constructs one
directly). Analyst edits enter through the front door: drift_diff → proposed events
(provenance='analyst') → review queue; never auto-applied.
"""
from __future__ import annotations

import yaml

from ..substrate.events import EventType, Provenance, ThemeEvent
from ..substrate.fold import fold
from ..substrate.hypothesis import Mechanism, ThemeHypothesis, TransmissionEdge, derived_direction
from ..ingest.scoring_view import ScoreView

_EPOCH = "1970-01-01T00:00:00+00:00"       # synthetic times for parse-reconstructed events


def render(theme: ThemeHypothesis, score: ScoreView) -> str:
    d = derived_direction(theme)
    edges = theme.mechanism.edges
    chain = " → ".join([edges[0].v_from] + [e.v_to for e in edges])
    frontmatter = {
        "theme_id": theme.theme_id,
        "mechanism": [[e.v_from, e.v_to, e.sign] for e in edges],
        "shock_direction": theme.shock_direction,
        "operational_axis": theme.operational_axis,
        "horizon_days": theme.horizon_days,
        "falsifier": theme.falsifier,
        "status": theme.status.value,
        "revision": theme.revision,
    }
    front = yaml.safe_dump(frontmatter, sort_keys=False).strip()
    rows = "\n".join(f"| {c.institution} | {c.net:+.2f} |" for c in score.by_institution)
    body = (
        f"# {theme.theme_id}\n\n"
        f"## Mechanism\n`{chain}`  (σ={theme.shock_direction:+d}, d(θ)={d:+d})\n\n"
        f"## Operational axis\n{theme.operational_axis}\n\n"
        f"## Score\nS_θ = {score.S:+.2f}   B_θ = {score.B}\n\n"
        f"### Per-institution evidence\n| institution | net |\n|---|---|\n{rows}\n\n"
        f"## Falsifier\n{theme.falsifier}\n\n"
        f"## Event-log timeline\nfolded revision {theme.revision}\n"
    )
    return f"---\n{front}\n---\n{body}"


def _fields(page_text: str) -> dict:
    return yaml.safe_load(page_text.split("---", 2)[1])


def parse(page_text: str) -> ThemeHypothesis:
    """Recover a ThemeHypothesis from a rendered page — via fold (I5-safe)."""
    fm = _fields(page_text)
    edges = tuple(TransmissionEdge(v_from=a, v_to=b, sign=int(s)) for a, b, s in fm["mechanism"])
    tid = fm["theme_id"]
    events = [ThemeEvent(
        event_id=f"{tid}:created", theme_id=tid, event_type=EventType.CREATED,
        payload={"mechanism": Mechanism(edges=edges).model_dump(),
                 "shock_direction": fm["shock_direction"], "operational_axis": fm["operational_axis"],
                 "horizon_days": fm["horizon_days"], "falsifier": fm["falsifier"]},
        effective_at=_EPOCH, recorded_at=_EPOCH, provenance=Provenance.WIKI_IMPORT,
    )]
    if fm["status"] != "CANDIDATE":
        events.append(ThemeEvent(
            event_id=f"{tid}:status", theme_id=tid, event_type=EventType.STATUS_CHANGED,
            payload={"status": fm["status"]}, effective_at=_EPOCH, recorded_at=_EPOCH,
            provenance=Provenance.ANALYST,
        ))
    return fold(events)


def drift_diff(rendered_expected: str, wiki_actual: str) -> list[ThemeEvent]:
    """Diff → proposed ThemeEvents (provenance='analyst') for the review queue.
    Never auto-applied. Compares the two pages' recovered structured fields."""
    exp, act = parse(rendered_expected), parse(wiki_actual)
    tid = act.theme_id
    proposed: list[ThemeEvent] = []

    def _propose(event_type: EventType, payload: dict) -> None:
        proposed.append(ThemeEvent(
            event_id=f"{tid}:drift:{event_type.value}", theme_id=tid, event_type=event_type,
            payload=payload, effective_at=_EPOCH, provenance=Provenance.ANALYST,
        ))

    if act.mechanism != exp.mechanism:
        _propose(EventType.MECHANISM_REVISED, {"mechanism": act.mechanism.model_dump()})
    if act.operational_axis != exp.operational_axis:
        _propose(EventType.AXIS_REVISED, {"operational_axis": act.operational_axis})
    if act.horizon_days != exp.horizon_days:
        _propose(EventType.HORIZON_EXTENDED, {"horizon_days": act.horizon_days})
    if act.falsifier != exp.falsifier:
        _propose(EventType.FALSIFIER_REVISED, {"falsifier": act.falsifier})
    return proposed
