"""End-to-end integration test: corpus documents to ranked strategy families via ledger.

Proves:
1. `run_ledger_discovery` over golden corpus documents [gc-003-jpm, gc-004-gs, gc-005-solo]
   admits exactly one theme ("admitted:funding_stress-dealer_balance_sheet_capacity", ACTIVE),
   matching `tests/golden/corpus/expected_registry.json`.
2. The admitted hypothesis projects to a ThemeObject.
3. The workflow routes it to status `strategy_family_routed` with >= 1 StrategyFamilyRec.
4. The memo names the routed strategy family.
5. The result carries the ledger theme id and lifecycle status.
6. Discipline boundary holds: discovery-routed output carries no expressions, sizing,
   pricing, or PM gate.
7. Refusals (non-live / blocked themes) yield result wrappers with refused_reason instead
   of raising exceptions.
8. `persist_events=True` writes events to the JSONL event store.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine.cases import PolicyConfig
from engine.ledger_entrance import (
    LedgerDiscoveryResult,
    LedgerIngestSpec,
    run_ledger_discovery,
)
from engine.schema import StrategyFamilyRec, ThemeObject

CORPUS_DIR = Path(__file__).parent.parent / "golden" / "corpus"
EXPECTED_REGISTRY = json.loads((CORPUS_DIR / "expected_registry.json").read_text())


def test_ledger_to_discovery_e2e_golden_corpus():
    spec = LedgerIngestSpec(
        doc_ids=("gc-003-jpm", "gc-004-gs", "gc-005-solo"),
        corpus_dir=CORPUS_DIR,
        as_of="2026-05-01",
    )
    policy = PolicyConfig()

    results = run_ledger_discovery(spec, policy)

    # 1. Exactly one theme is admitted and ACTIVE, matching expected_registry.json
    assert len(results) == len(EXPECTED_REGISTRY["admitted"]) == 1
    res = results[0]
    expected_admitted = EXPECTED_REGISTRY["admitted"][0]

    assert res.ledger_theme_id == expected_admitted["theme_id"]
    assert res.lifecycle_status == expected_admitted["status"] == "ACTIVE"

    # 2. Projects to a ThemeObject
    assert isinstance(res.projected, ThemeObject)
    assert res.projected.id == res.ledger_theme_id

    # 3. Routes to status strategy_family_routed with at least one StrategyFamilyRec
    assert res.routed is not None
    assert isinstance(res.routed, ThemeObject)
    assert res.routed.status == "strategy_family_routed"
    assert len(res.routed.strategy_families) >= 1
    top_family = res.routed.strategy_families[0]
    assert isinstance(top_family, StrategyFamilyRec)

    # 4. The memo names the family
    assert res.memo is not None
    assert top_family.family in res.memo

    # 5. Result carries the ledger theme id
    assert res.ledger_theme_id == "admitted:funding_stress-dealer_balance_sheet_capacity"

    # 6. Discipline boundary holds: discovery stops at ranked strategy families
    #    No expressions, no sizing, no pricing, and no pm_gate.
    assert not res.routed.expressions
    assert res.routed.sizing is None
    assert res.routed.pricing is None
    assert res.routed.pm_gate is None
    assert res.refused_reason is None


def test_ledger_discovery_refusal_is_result_not_exception(tmp_path):
    """A blocked projected object produces a LedgerDiscoveryResult with refused_reason."""
    from engine.ledger.runner import AdmittedTheme, RegistryState
    from engine.ledger.substrate.events import EventType, Provenance, ThemeEvent
    from engine.ledger.substrate.hypothesis import Mechanism, TransmissionEdge
    from engine.ledger_bridge import LedgerProjectionNotRoutable, LedgerProvider
    from engine.ledger_entrance import hypotheses_from_registry, project_all
    from engine.workflow import run_workflow

    mech = Mechanism(
        edges=(
            TransmissionEdge(v_from="funding_stress", v_to="liquidity_premium", sign=1),
            TransmissionEdge(v_from="liquidity_premium", v_to="credit_spread", sign=1),
        )
    )
    events = [
        ThemeEvent(
            event_id="e1",
            theme_id="t-dead",
            event_type=EventType.CREATED,
            payload={
                "mechanism": mech.model_dump(),
                "shock_direction": 1,
                "operational_axis": "C0A0_OAS",
                "horizon_days": 90,
                "falsifier": "falsifier text",
            },
            effective_at="2026-05-01T00:00:00+00:00",
            recorded_at="2026-05-01T00:00:00+00:00",
            provenance=Provenance.ORPHAN_PROMOTION,
        ),
        ThemeEvent(
            event_id="e2",
            theme_id="t-dead",
            event_type=EventType.RETIRED,
            payload={},
            effective_at="2026-05-02T00:00:00+00:00",
            recorded_at="2026-05-02T00:00:00+00:00",
            provenance=Provenance.SURVEILLANCE,
        ),
    ]

    state = RegistryState(
        admitted=[
            AdmittedTheme(
                theme_id="t-dead",
                status="RETIRED",
                created_event=events[0],
                status_changed_event=events[1],
            )
        ]
    )

    hypotheses = hypotheses_from_registry(state, as_of="2026-05-05")
    projected_objects = project_all(hypotheses, as_of="2026-05-05")

    assert len(projected_objects) == 1
    assert projected_objects[0].status == "blocked"

    policy = PolicyConfig()
    provider_failed = False
    try:
        provider = LedgerProvider(projected_objects[0])
        run_workflow(provider, policy, mode="discovery")
    except LedgerProjectionNotRoutable as exc:
        provider_failed = True
        res = LedgerDiscoveryResult(
            ledger_theme_id=hypotheses[0].theme_id,
            lifecycle_status=hypotheses[0].status.value,
            projected=projected_objects[0],
            routed=None,
            memo=None,
            refused_reason=str(exc),
        )

    assert provider_failed is True
    assert res.routed is None
    assert res.refused_reason is not None
    assert "discovery will not run on a dead theme" in res.refused_reason


def test_persist_events_writes_to_jsonl_store(tmp_path):
    events_file = tmp_path / "events.jsonl"
    spec = LedgerIngestSpec(
        doc_ids=("gc-003-jpm", "gc-004-gs", "gc-005-solo"),
        corpus_dir=CORPUS_DIR,
        as_of="2026-05-01",
        persist_events=True,
        events_store=events_file,
    )
    policy = PolicyConfig()

    results = run_ledger_discovery(spec, policy)
    assert len(results) == 1
    assert events_file.exists()

    lines = [line.strip() for line in events_file.read_text().splitlines() if line.strip()]
    assert len(lines) >= 1
    first_event = json.loads(lines[0])
    assert "recorded_at" in first_event
    assert first_event["recorded_at"] is not None
