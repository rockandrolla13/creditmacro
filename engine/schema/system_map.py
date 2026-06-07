"""System Structure Mapper (Meadows) — embeds the causal chain in a system."""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel

from .causal import CausalEdge, CausalNode


class Stock(BaseModel):
    """A LEVEL measurable at an instant (outstanding debt, index weight, AUM)."""
    name: str
    unit: str
    observable: Optional[str] = None


class Flow(BaseModel):
    """A RATE over time that changes a stock (issuance, fund flows, defaults).
    Distinct type from Stock — misclassifying level vs rate is the common error."""
    name: str
    changes_stock: str          # which Stock.name this flow moves
    unit_per_time: str
    observable: Optional[str] = None


class FeedbackLoop(BaseModel):
    """Reinforcing (amplifies) or balancing (stabilises). Reflexive links are marked
    feedback on the underlying CausalEdge."""
    id: str
    type: Literal["reinforcing", "balancing"]
    path: list[str]             # node-id sequence the loop traverses
    delay: Optional[str] = None
    closes_via: str = ""        # what closes the loop back on itself


class Delay(BaseModel):
    """A lag between a flow and its stock, or a driver and its price response — where
    the system surprises investors."""
    between: str
    length: str
    why_it_matters: str = ""


class SystemMap(BaseModel):
    """Theme embedded in a system (Meadows). Reuses the causal chain's nodes/edges as
    elements/interconnections; adds stocks, flows, loops, delays, shocks, observables."""
    boundary_inside: list[str]
    boundary_outside: list[str]
    boundary_rationale: str = ""
    function_purpose: str
    elements: list[CausalNode] = []            # reuse the chain's nodes
    interconnections: list[CausalEdge] = []     # reuse the chain's edges (+ ones a chain misses)
    stocks: list[Stock] = []
    flows: list[Flow] = []
    feedback_loops: list[FeedbackLoop] = []
    delays: list[Delay] = []
    external_shocks: list[str] = []
    internal_responses: list[str] = []
    observable_variables: list[str] = []
    surprise_modes: list[str] = []
