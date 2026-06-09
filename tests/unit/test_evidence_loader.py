"""Tests for engine.evidence_loader — current-input evidence loading helper.

The loader reads ONLY the atoms for the CURRENT source slug (the document under
analysis). Archived CASE evidence for OTHER sources must never be loaded here — that
would leak prior cases into fresh reasoning. These tests pin that contract.
"""
from __future__ import annotations

import logging
from pathlib import Path

import pytest

from engine.evidence_loader import (
    load_evidence_atoms_for_current_source,
    load_evidence_maps_for_current_source,
)
from engine.schema import Scenario, ScenarioEvidenceMap

WIKI = Path(__file__).resolve().parents[2] / "wiki"
JPM_SLUG = "jpm-ai-capex-funding-2026-05-11"


def _hpc_scenarios() -> list[Scenario]:
    """A couple of HPC / AI-capex themed scenarios (supplied, never invented by the loader)."""
    return [
        Scenario(
            name="AI capex funding strain",
            p_s=0.4,
            driver_path="hyperscaler data center HPC issuer spreads widen on outstanding obligations",
            implied_axis_value=1.0,
            pnl_per_unit=1.0,
        ),
        Scenario(
            name="Benign funding base case",
            p_s=0.6,
            driver_path="hyperscaler data center HPC credit spreads stable",
            implied_axis_value=0.0,
            pnl_per_unit=1.0,
        ),
    ]


def test_loads_the_15_jpm_atoms_for_current_source():
    atoms = load_evidence_atoms_for_current_source(JPM_SLUG, WIKI)
    assert len(atoms) == 15
    assert all(a.source_slug == JPM_SLUG for a in atoms)
    assert all(a.claim for a in atoms)
    assert all(a.claim_kind for a in atoms)


def test_unrelated_source_returns_empty():
    atoms = load_evidence_atoms_for_current_source("some-other-source", WIKI)
    assert atoms == []


@pytest.mark.parametrize("bad", [None, "", "   "])
def test_missing_or_empty_source_returns_empty_and_warns(bad, caplog):
    with caplog.at_level(logging.WARNING, logger="engine.evidence_loader"):
        atoms = load_evidence_atoms_for_current_source(bad, WIKI)
    assert atoms == []
    assert any(r.levelno == logging.WARNING for r in caplog.records)


def test_loaded_atoms_are_current_input_not_other_cases():
    atoms = load_evidence_atoms_for_current_source(JPM_SLUG, WIKI)
    # current input is present...
    assert len(atoms) > 0
    # ...and nothing belongs to a different source_slug
    assert {a.source_slug for a in atoms} == {JPM_SLUG}


def test_load_evidence_maps_one_per_scenario_with_impacts():
    scenarios = _hpc_scenarios()
    maps = load_evidence_maps_for_current_source(JPM_SLUG, scenarios, WIKI)
    assert len(maps) == len(scenarios)
    assert all(isinstance(m, ScenarioEvidenceMap) for m in maps)
    assert {m.scenario_name for m in maps} == {s.name for s in scenarios}
    assert any(len(m.impacts) > 0 for m in maps)


def test_maps_empty_when_no_atoms_match():
    maps = load_evidence_maps_for_current_source("some-other-source", _hpc_scenarios(), WIKI)
    # no atoms → one empty map per scenario
    assert len(maps) == 2
    assert all(len(m.impacts) == 0 for m in maps)
