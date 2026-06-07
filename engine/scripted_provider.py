"""
ScriptedProvider — one CaseSpec presented through the Provider seam.

Every seam returns the corresponding slice of the case and IGNORES its inputs, so it
is deterministic and input-blind. This single class replaces all per-case fixtures
(AR-BND-002): a new case is a YAML file, never a new class.
"""
from __future__ import annotations

from .cases import CaseSpec
from .protocols import RunContext, SizingRiskBundle
from .schema import Axis, Expression, Scenario, ThemeObject, Thesis
from .stage0 import IngestionResult


class ScriptedProvider:
    """Implements engine.protocols.Provider from a single CaseSpec."""

    def __init__(self, case: CaseSpec) -> None:
        self._case = case

    def context(self) -> RunContext:
        c = self._case
        return RunContext(
            statement=c.theme_sentence,
            horizon=c.horizon,
            author=c.author,
            x_mkt=c.x_mkt,
            prior=c.prior if isinstance(c.prior, list) else [],
            capital=c.capital,
            # conviction is an Engine-4 (expression) input; discovery-only cases carry no
            # sizing, so fall back to the RunContext default.
            conviction=c.sizing.conviction if c.sizing is not None else 3,
            thesis_sign=c.thesis_sign,
            run_edge_mc=c.edge_mc,
            provenance=c.provenance,
        )

    def expand_causal(self, research_text: str, parsed_theme: str):
        """Return the case's hand-built causal payload, or (None, None, None)."""
        c = self._case.causal
        if c is None:
            return None, None, None
        return c.main_theme, c.causal_chain, c.shared_factor

    def build_system_map(self, thesis, causal_chain):
        """Return the case's hand-built system map, or None."""
        return self._case.system_map

    def critique_mental_model(self, statement, causal_chain):
        """Return the case's hand-built bias critique, or None."""
        return self._case.bias_critique

    def diagnose_loops(self, system_map):
        """PRE-PRICING: return the case's hand-built loop diagnosis, or None."""
        return self._case.loop_diagnosis

    def assess_trap_implications(self, scenarios, pricing, expressions):
        """POST-PRICING: return the case's hand-built trap implications, or None."""
        return self._case.trap_implications

    def parse(self, raw: str) -> IngestionResult:
        # Stage-0 ingestion is not part of a CaseSpec; a scripted case starts from an
        # already-chosen theme. Return empty streams (the ThemeObject does not embed them).
        return IngestionResult(
            observations=[],
            candidate_themes=[],
            consensus_signals=[],
            ranked_candidates=[],
        )

    def extract_drivers(self, statement: str) -> Thesis:
        return self._case.thesis

    def define_axis(self, thesis: Thesis) -> Axis:
        return self._case.axis

    def normal_fair_value(self, axis: Axis) -> float:
        return self._case.normal_fv

    def propose_scenarios(self, thesis: Thesis, axis: Axis, loop_diagnosis=None) -> list[Scenario]:
        # scripted: scenarios are pre-built in the case (a generative provider would fold
        # loop_diagnosis.possible_loop_shift in as a reversal scenario).
        return self._case.scenarios

    def enumerate_expressions(
        self, thesis: Thesis, axis: Axis, scenarios: list[Scenario]
    ) -> list[Expression]:
        return self._case.expressions

    def size_and_risk(
        self, thesis: Thesis, axis: Axis, best: Expression, conviction: int
    ) -> SizingRiskBundle:
        c = self._case
        return SizingRiskBundle(sizing=c.sizing, risk=c.risk, pm_gate=c.pm_gate)

    def critique(self, theme: ThemeObject) -> list[str]:
        return self._case.pm_gate.open_questions
