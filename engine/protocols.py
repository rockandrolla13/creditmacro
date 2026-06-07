"""
The Provider seam — the input-blind contract the runner depends on.

Provider is composed of three narrower seam protocols (AR-ABS-002 / Interface
Segregation) so a future provider can be scripted for some seams and generative for
others. ScriptedProvider (and, later, an LLM provider) implement the full Provider.

These are typing.Protocols — structural contracts, no behaviour. SizingRiskBundle
replaces the previous bare 3-tuple return of size_and_risk (AR-ABS-002).
"""
from __future__ import annotations

from typing import Literal, Optional, Protocol, runtime_checkable

from pydantic import BaseModel

from .schema import (
    Axis,
    BiasCritique,
    CausalChain,
    CausalNode,
    Expression,
    PMGate,
    Provenance,
    Risk,
    Scenario,
    Sizing,
    LoopDiagnosis,
    Pricing,
    SystemMap,
    ThemeObject,
    Thesis,
    TrapImplications,
)
from .stage0 import IngestionResult


class SizingRiskBundle(BaseModel):
    """Grouped Engine-4 output — sizing, risk, and the PM gate."""
    sizing: Sizing
    risk: Risk
    pm_gate: PMGate


class RunContext(BaseModel):
    """Non-seam inputs the runner needs: identity + market data that are NOT engine
    outputs (a generative provider would source x_mkt/prior from a data layer, not an
    LLM). Keeping them off the engine seams stops the seams from leaking market data."""
    statement: str
    horizon: str
    author: str
    # Optional: a freshly-discovered theme may have no live mark. Discovery degrades
    # gracefully (edge_survival="unknown", capped confidence); expression mode requires it.
    x_mkt: Optional[float] = None
    prior: list[float]
    capital: float = 0.0
    conviction: int = 3              # PM conviction (Alaph grid) — input to Engine 4
    thesis_sign: Literal[-1, 1] = 1
    run_edge_mc: bool = False        # whether run_pricing should run the MC edge
    provenance: Provenance


@runtime_checkable
class CausalExpander(Protocol):
    """The single seam a causal-compiler adapter must satisfy: research text → one causal
    object. `LLMProvider` implements THIS (not the full `Provider`) — it cannot drive
    `run_workflow`, which needs all the seams below."""

    def expand_causal(
        self, research_text: str, parsed_theme: str
    ) -> tuple[Optional[CausalNode], Optional[CausalChain], Optional[str]]: ...


class ScenarioSource(Protocol):
    def propose_scenarios(
        self, thesis: Thesis, axis: Axis, loop_diagnosis: Optional[LoopDiagnosis] = None
    ) -> list[Scenario]:
        """Propose scenarios; when a loop diagnosis is supplied, the balancing limit /
        reversal point should appear as a reversal scenario."""
        ...


class ExpressionSource(Protocol):
    def enumerate_expressions(
        self, thesis: Thesis, axis: Axis, scenarios: list[Scenario]
    ) -> list[Expression]: ...


class RiskSource(Protocol):
    def size_and_risk(
        self, thesis: Thesis, axis: Axis, best: Expression, conviction: int
    ) -> SizingRiskBundle: ...


@runtime_checkable
class Provider(ScenarioSource, ExpressionSource, RiskSource, Protocol):
    """Full pipeline seam set. The runner calls these in order and cannot tell a
    scripted provider from a generative one."""

    def context(self) -> RunContext: ...

    def parse(self, raw: str) -> IngestionResult: ...

    def expand_causal(
        self, research_text: str, parsed_theme: str
    ) -> tuple[Optional[CausalNode], Optional[CausalChain], Optional[str]]:
        """Compile research text into ONE causal chain (main_theme, chain, shared_factor).
        Returns (None, None, None) when the provider carries no causal payload."""
        ...

    def build_system_map(
        self, thesis: Thesis, causal_chain: Optional[CausalChain]
    ) -> Optional[SystemMap]:
        """Embed the causal chain in a Meadows system map (stocks/flows/loops/delays).
        Returns None when the provider carries no system map."""
        ...

    def critique_mental_model(
        self, statement: str, causal_chain: Optional[CausalChain]
    ) -> Optional[BiasCritique]:
        """Adversarial review of the theme's mental model. None when not supplied."""
        ...

    def diagnose_loops(self, system_map: Optional[SystemMap]) -> Optional[LoopDiagnosis]:
        """PRE-PRICING: diagnose loops/leverage/traps from the system map's loop map and
        the reversal point that feeds scenario construction. None when not supplied."""
        ...

    def assess_trap_implications(
        self, scenarios: list[Scenario], pricing: Pricing, expressions: list[Expression]
    ) -> Optional[TrapImplications]:
        """POST-PRICING: map loop states to scenario fair values and name the expression
        families that break on reversal. None when not supplied."""
        ...

    def extract_drivers(self, statement: str) -> Thesis: ...

    def define_axis(self, thesis: Thesis) -> Axis: ...

    def normal_fair_value(self, axis: Axis) -> float: ...

    def critique(self, theme: ThemeObject) -> list[str]: ...
