"""Current-input evidence seam — PART 1: RunContext fields.

These pin the SHAPE only. Phase-A consumption (mapping the current-input atoms into the Q4
posterior) is a later part; the archived-CASE firewall is unchanged and tested elsewhere.
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from engine.protocols import RunContext
from engine.schema import EvidenceAtom, Provenance, ScenarioEvidenceMap


def _ctx(**kw):
    base = dict(statement="s", horizon="3m", author="a", prior=[0.5, 0.5],
                provenance=Provenance(evidence=["x"], confidence=0.5))
    base.update(kw)
    return RunContext(**base)


def test_current_input_fields_default_empty_and_none():
    c = _ctx()
    assert c.current_input_source_slug is None
    assert c.current_input_evidence_atoms == []
    assert c.current_input_evidence_maps == []
    assert c.current_input_evidence_source == "none"
    assert c.phase_a_evidence_allowed is True


def test_accepts_current_input_atoms_and_slug():
    atom = EvidenceAtom(claim="HPC index weight rose", source_slug="jpm-ai-capex-funding-2026-05-11",
                        themes=["hy-hpc-crowding-and-supply"], market_variables=["HPC HY index weight"])
    c = _ctx(current_input_evidence_atoms=[atom],
             current_input_source_slug="jpm-ai-capex-funding-2026-05-11",
             current_input_evidence_source="current_report")
    assert c.current_input_evidence_atoms[0].claim == "HPC index weight rose"
    assert c.current_input_source_slug == "jpm-ai-capex-funding-2026-05-11"
    assert c.current_input_evidence_source == "current_report"


def test_accepts_current_input_maps():
    m = ScenarioEvidenceMap(scenario_name="A", evidence_for_count=0, evidence_against_count=0,
                            contradiction_count=0, cluster_count=0, mapping_confidence=0.0)
    c = _ctx(current_input_evidence_maps=[m])
    assert c.current_input_evidence_maps[0].scenario_name == "A"


def test_rejects_unknown_evidence_source():
    with pytest.raises(ValidationError):
        _ctx(current_input_evidence_source="archived_case")


def test_phase_a_evidence_allowed_is_toggleable():
    assert _ctx(phase_a_evidence_allowed=False).phase_a_evidence_allowed is False
