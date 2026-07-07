"""Phase-2 GATES: test_golden_revisions, test_unparseable_routes_to_queue
(ONTOLOGY §Identity, §WF, §Event semantics, §Scoring Case-B).
"""
from __future__ import annotations

from pathlib import Path

from engine.ledger.substrate.events import EventType, Provenance
from engine.ledger.substrate.fold import fold
from engine.ledger.wiki.wiki_import import (
    extract, replay, mechanism_text_cosine, import_curated, WikiCandidate,
)

GOLDEN = Path(__file__).parent.parent / "golden" / "wiki"


def _page(name: str) -> str:
    return (GOLDEN / name).read_text()


def _extract(name: str):
    return extract(_page(name))


# ── extractor ────────────────────────────────────────────────────────────────
def test_extract_wellformed_page_yields_candidate():
    res = _extract("funding_liquidity_r1.md")
    assert res.needs_structuring is False
    c = res.candidate
    assert isinstance(c, WikiCandidate)
    assert c.mechanism.k == 2
    assert c.operational_axis == "C0A0_OAS"
    assert c.shock_direction == 1
    assert c.horizon_days == 90


def test_unparseable_routes_to_queue():
    # vibes page: k=1 chain → WF clause (a) → NEEDS_STRUCTURING, no theme created.
    res = _extract("vibes_riskoff.md")
    assert res.needs_structuring is True
    assert res.failing_clause == "a"
    assert res.candidate is None


# ── cosine pre-filter (deterministic embedder) ───────────────────────────────
def test_cosmetic_reword_is_above_threshold():
    a = _extract("funding_liquidity_r1.md").candidate
    b = _extract("funding_liquidity_r2.md").candidate
    assert mechanism_text_cosine(a.mechanism_text, b.mechanism_text) >= 0.92


def test_mechanism_refinement_is_below_threshold():
    b = _extract("funding_liquidity_r2.md").candidate
    c = _extract("funding_liquidity_r3.md").candidate
    assert mechanism_text_cosine(b.mechanism_text, c.mechanism_text) < 0.92


# ── revision replayer ────────────────────────────────────────────────────────
def test_replay_cosmetic_emits_nothing():
    a = _extract("funding_liquidity_r1.md").candidate
    b = _extract("funding_liquidity_r2.md").candidate
    assert replay(a, b) == ()


def test_replay_refinement_emits_mechanism_revised():
    b = _extract("funding_liquidity_r2.md").candidate
    c = _extract("funding_liquidity_r3.md").candidate
    assert replay(b, c) == (EventType.MECHANISM_REVISED,)


def test_replay_axis_flip_emits_axis_revised():
    a = _extract("hyperscaler_axis_r1.md").candidate
    b = _extract("hyperscaler_axis_r2.md").candidate
    assert replay(a, b) == (EventType.AXIS_REVISED,)


def test_replay_shock_reversal_is_retire_create():
    a = _extract("funding_liquidity_r1.md").candidate
    flipped = WikiCandidate(
        mechanism=a.mechanism, shock_direction=-a.shock_direction,
        operational_axis=a.operational_axis, horizon_days=a.horizon_days,
        falsifier=a.falsifier, mechanism_text=a.mechanism_text,
    )
    assert replay(a, flipped) == (EventType.RETIRED, EventType.CREATED)


def test_replay_disjoint_mechanism_is_retire_create():
    a = _extract("funding_liquidity_r1.md").candidate      # funding_stress → … → credit_spread
    d = _extract("hyperscaler_axis_r1.md").candidate        # capex_funding_need → … (disjoint v0)
    assert replay(a, d) == (EventType.RETIRED, EventType.CREATED)


def test_golden_revisions():
    # r1 import → CREATED; r1→r2 cosmetic → nothing; r2→r3 refine → MECHANISM_REVISED.
    revs = [_extract(f"funding_liquidity_r{i}.md").candidate for i in (1, 2, 3)]
    emitted: list[EventType] = [EventType.CREATED]              # the import
    for prev, new in zip(revs, revs[1:]):
        emitted.extend(replay(prev, new))
    assert emitted == [EventType.CREATED, EventType.MECHANISM_REVISED]
    assert emitted.count(EventType.CREATED) == 1
    assert emitted.count(EventType.MECHANISM_REVISED) == 1


# ── Case-B import (CREATED + synthetic prior mass) ───────────────────────────
def test_import_curated_emits_created_and_prior_mass():
    c = _extract("funding_liquidity_r1.md").candidate
    event, seed = import_curated("funding-liquidity-golden", c,
                                 import_date="2026-03-01T00:00:00+00:00", s_prior=2)
    assert event.event_type == EventType.CREATED
    assert event.provenance == Provenance.WIKI_IMPORT
    assert event.effective_at == "2026-03-01T00:00:00+00:00"
    assert event.recorded_at is None                           # store stamps it (I7)
    assert seed.s_prior == 2
    assert seed.t_import == "2026-03-01T00:00:00+00:00"

    # the CREATED event folds back to the imported candidate's fields
    stamped = event.model_copy(update={"recorded_at": "2026-03-01T00:00:00+00:00"})
    theme = fold([stamped])
    assert theme.operational_axis == c.operational_axis
    assert theme.mechanism.k == c.mechanism.k
    assert theme.shock_direction == c.shock_direction
