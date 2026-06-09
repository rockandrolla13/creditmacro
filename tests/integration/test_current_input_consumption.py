"""Wire CURRENT-INPUT evidence consumption into Phase-A discovery.

Current-input evidence (the report/idea being processed NOW) is Phase-A eligible — it is NOT
archived CASE memory. When `phase_a_evidence_allowed` is True and current-input atoms/maps are
supplied, discovery maps them to the (supplied) scenarios and computes an evidence-tilted
posterior AUDIT. With the gate off, or with no current-input evidence, discovery is unchanged
(posterior_equals_prior) and the golden master is byte-identical.
"""
from __future__ import annotations

import json

from engine.case_loader import load_case
from engine.probability_evidence import map_evidence_to_scenarios, update_probabilities_from_evidence
from engine.protocols import RunContext
from engine.schema import EvidenceAtom
from engine.scripted_provider import ScriptedProvider
from engine.workflow import run_workflow
from tests._helpers import CASES_DIR

JPM_FIXTURE = CASES_DIR / "discovery" / "jpm_ai_capex.yaml"


def _hpc_atoms() -> list[EvidenceAtom]:
    """A few source-backed atoms about HPC index weight / OAS / issuance, with terms that
    overlap the JPM fixture's scenario names/driver paths (capex, supply, demand, 30Y)."""
    return [
        EvidenceAtom(
            evidence_id="ev1", source_slug="jpm-2026-05-11", source_location="p.3",
            claim="Hyperscaler 30Y IG supply accelerates as AI capex funding surges",
            claim_kind="source_fact", direction="increase",
            concepts=["capex", "supply"], market_variables=["30Y", "issuance"],
            confidence=0.8, freshness=1.0, evidence_cluster_id="supply",
        ),
        EvidenceAtom(
            evidence_id="ev2", source_slug="rtr-2026-05-12", source_location="wire",
            claim="HPC index weight rose and long-end supply continues to widen OAS",
            claim_kind="source_fact", direction="increase",
            concepts=["supply", "demand"], market_variables=["OAS", "30Y"],
            confidence=0.7, freshness=1.0, evidence_cluster_id="oas",
        ),
        EvidenceAtom(
            evidence_id="ev3", source_slug="ldi-2026-05-10", source_location="desk",
            claim="Long-end demand absorbs gradual steepening as supply continues",
            claim_kind="source_fact", direction="increase",
            concepts=["demand", "supply"], market_variables=["30Y"],
            confidence=0.6, freshness=1.0, evidence_cluster_id="demand",
        ),
    ]


class _CurrentInputProvider(ScriptedProvider):
    """ScriptedProvider whose RunContext carries CURRENT-INPUT evidence atoms (Phase-A eligible)."""

    def __init__(self, case, *, atoms=None, maps=None, allowed=True):
        super().__init__(case)
        self._atoms = atoms or []
        self._maps = maps or []
        self._allowed = allowed

    def context(self) -> RunContext:
        base = super().context()
        return base.model_copy(update={
            "current_input_source_slug": "jpm-2026-05-11",
            "current_input_evidence_atoms": self._atoms,
            "current_input_evidence_maps": self._maps,
            "current_input_evidence_source": "current_report",
            "phase_a_evidence_allowed": self._allowed,
        })


def _run(provider):
    case = provider._case
    theme, _ = run_workflow(provider, case.resolved_policy(), mode="discovery")
    return theme


# 1 ─ Supplying current-input atoms tilts the posterior ───────────────────────
def test_current_input_atoms_tilt_posterior():
    case = load_case(JPM_FIXTURE)
    theme = _run(_CurrentInputProvider(case, atoms=_hpc_atoms(), allowed=True))
    audit = theme.probability_justification.update_audit
    assert audit is not None
    assert audit.update_method == "softmax_evidence_tilt"
    assert audit.posterior_vector != audit.prior_vector


# 2 ─ Same atoms, gate OFF → posterior == prior ───────────────────────────────
def test_phase_a_gate_off_keeps_prior():
    case = load_case(JPM_FIXTURE)
    theme = _run(_CurrentInputProvider(case, atoms=_hpc_atoms(), allowed=False))
    audit = theme.probability_justification.update_audit
    assert audit is not None
    assert audit.update_method == "posterior_equals_prior"
    assert audit.posterior_vector == audit.prior_vector


# 3 ─ No current-input evidence → posterior == prior (golden discovery path) ───
def test_no_current_input_is_prior():
    case = load_case(JPM_FIXTURE)
    # Plain ScriptedProvider supplies NO current-input evidence.
    theme, _ = run_workflow(ScriptedProvider(case), case.resolved_policy(), mode="discovery")
    audit = theme.probability_justification.update_audit
    assert audit is not None
    assert audit.update_method == "posterior_equals_prior"
    assert audit.posterior_vector == audit.prior_vector


# 4 ─ Routed top family carries the probability-update metadata ───────────────
def test_top_family_carries_probability_metadata():
    case = load_case(JPM_FIXTURE)
    theme = _run(_CurrentInputProvider(case, atoms=_hpc_atoms(), allowed=True))
    assert theme.status == "strategy_family_routed"
    top = theme.strategy_families[0]
    assert top.probability_update_method == "softmax_evidence_tilt"
    assert top.probability_quality is not None
    assert top.probability_update_audit_hash


# 5 ─ Pre-built maps are used directly (no re-mapping needed) ─────────────────
def test_prebuilt_maps_used_directly():
    case = load_case(JPM_FIXTURE)
    maps = map_evidence_to_scenarios(case.scenarios, _hpc_atoms())
    theme = _run(_CurrentInputProvider(case, maps=maps, allowed=True))
    audit = theme.probability_justification.update_audit
    assert audit.update_method == "softmax_evidence_tilt"
    assert audit.posterior_vector != audit.prior_vector
