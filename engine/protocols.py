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
    CausalChain,
    CausalNode,
    Expression,
    PMGate,
    Provenance,
    Risk,
    Scenario,
    Sizing,
    ThemeObject,
    Thesis,
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
    x_mkt: float
    prior: list[float]
    capital: float = 0.0
    conviction: int = 3              # PM conviction (Alaph grid) — input to Engine 4
    thesis_sign: Literal[-1, 1] = 1
    run_edge_mc: bool = False        # whether run_pricing should run the MC edge
    provenance: Provenance


class ScenarioSource(Protocol):
    def propose_scenarios(self, thesis: Thesis, axis: Axis) -> list[Scenario]: ...


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

    def extract_drivers(self, statement: str) -> Thesis: ...

    def define_axis(self, thesis: Thesis) -> Axis: ...

    def normal_fair_value(self, axis: Axis) -> float: ...

    def critique(self, theme: ThemeObject) -> list[str]: ...
