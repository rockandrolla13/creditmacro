"""End-to-end: current-input evidence seam, loader → RunContext → discovery → posterior.

Closes the gap between PART-2b/c (mapper + posterior), the current-input seam (RunContext), and
the loader: load the materialized JPM atoms for the CURRENT source, hand them in as current-input
evidence, run Phase-A discovery, and confirm the posterior tilts (and the gate suppresses it).
No trades / sizing / scenario generation; archived CASE store is never read here.
"""
from __future__ import annotations

from pathlib import Path

from engine.case_loader import load_case
from engine.evidence_loader import load_evidence_atoms_for_current_source
from engine.protocols import RunContext
from engine.scripted_provider import ScriptedProvider
from engine.workflow import run_workflow
from tests._helpers import CASES_DIR

WIKI = Path(__file__).resolve().parents[2] / "wiki"
JPM_FIXTURE = CASES_DIR / "discovery" / "jpm_ai_capex.yaml"
JPM_SLUG = "jpm-ai-capex-funding-2026-05-11"


class _LoaderFedProvider(ScriptedProvider):
    """ScriptedProvider whose RunContext carries current-input atoms produced by the LOADER."""

    def __init__(self, case, atoms, *, allowed=True):
        super().__init__(case)
        self._atoms = atoms
        self._allowed = allowed

    def context(self) -> RunContext:
        return super().context().model_copy(update={
            "current_input_source_slug": JPM_SLUG,
            "current_input_evidence_atoms": self._atoms,
            "current_input_evidence_source": "current_report",
            "phase_a_evidence_allowed": self._allowed,
        })


def test_loader_feeds_seam_into_discovery_and_tilts_posterior():
    case = load_case(JPM_FIXTURE)
    atoms = load_evidence_atoms_for_current_source(JPM_SLUG, WIKI)   # the loader
    assert len(atoms) == 15                                         # all JPM atoms
    theme, _ = run_workflow(_LoaderFedProvider(case, atoms), case.resolved_policy(),
                            mode="discovery")
    audit = theme.probability_justification.update_audit
    assert audit is not None
    assert audit.update_method == "softmax_evidence_tilt"           # evidence-weighted
    assert audit.posterior_vector != audit.prior_vector            # posterior moved
    assert any(m.impacts for m in audit.evidence_maps)             # real atoms mapped
    # discovery still STOPS at ranked families, with the audit stamped on the top family
    assert theme.status == "strategy_family_routed"
    top = theme.strategy_families[0]
    assert top.probability_update_method == "softmax_evidence_tilt"
    assert top.probability_update_audit_hash


def test_loader_fed_gate_off_keeps_prior():
    case = load_case(JPM_FIXTURE)
    atoms = load_evidence_atoms_for_current_source(JPM_SLUG, WIKI)
    theme, _ = run_workflow(_LoaderFedProvider(case, atoms, allowed=False),
                            case.resolved_policy(), mode="discovery")
    audit = theme.probability_justification.update_audit
    assert audit.update_method == "posterior_equals_prior"
    assert audit.posterior_vector == audit.prior_vector


def test_loaded_atoms_are_current_input_only_not_archive():
    # the loader returns ONLY the current source's atoms (all access_class=case, allowed because
    # they are the current input); no other source's atoms leak in.
    atoms = load_evidence_atoms_for_current_source(JPM_SLUG, WIKI)
    assert atoms and all(a.source_slug == JPM_SLUG for a in atoms)
    assert all(a.claim and a.claim_kind for a in atoms)
