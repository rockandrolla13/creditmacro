"""Engine-1 thesis + axis, and the Causal Theme Compiler (one depth-first chain)."""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, model_validator

# ── Engine 1 output: thesis + axis (Q1, Q2, Q3) ──────────────────────────────

class Driver(BaseModel):
    """One causal factor acting on the axis. Q1 / Driver Extractor."""
    name: str
    sign: Literal["+", "-"]       # direction of effect on axis
    proxy_observable: str         # the computable series proxying this driver
    current_level: Optional[float] = None
    mechanism: str                # one sentence: driver → axis
    # optional — requires historical signal regression
    edge_elasticity: Optional[float] = None  # ∂(edge)/∂(driver_level) / edge: % edge change per 1% driver change

class CausalChainStep(BaseModel):
    from_node: str
    to_node: str

class Thesis(BaseModel):
    """Engine 1 output. Answers Q1 (theme) and Q2 (universe, via drivers)."""
    drivers: list[Driver]
    causal_chain: list[CausalChainStep]  # DAG: driver → intermediate → axis
    direction_of_view: str               # signed claim, e.g. "axis steepens (+)"
    # optional — requires historical driver signal correlation matrix
    driver_diversification_multiplier: Optional[float] = None  # 1/sqrt(avg pairwise ρ); >1 when drivers are uncorrelated

class AxisHistory(BaseModel):
    mean: float          # long-run unconditional mean
    vol: float           # σ (same units as axis)
    percentile: float    # current value percentile in history
    regime_tags: list[str]

class Axis(BaseModel):
    """Engine 1 output. Answers Q2 (universe scoping) and Q3 (the hard gate)."""
    definition: str    # full operational description + universe
    measurement: str   # exactly how it is computed; data source
    current_value: float
    history: AxisHistory
    # optional — macro regime detected from central bank signals / HMM
    regime: Optional[Literal["easing", "neutral", "tightening", "crisis"]] = None
    # Routing inputs (discovery): SHAPE + DIRECTION together pick the family. When unset,
    # discovery derives shape from the operational text and direction from the thesis sign.
    axis_shape: Optional[
        Literal["level", "curve", "basis", "relative_value", "cross_asset", "volatility"]
    ] = None
    axis_direction: Optional[
        Literal["higher", "lower", "steeper", "flatter", "wider", "tighter",
                "dispersion_up", "dispersion_down"]
    ] = None

class AxisCandidate(BaseModel):
    """The richer output of the define_axis discovery seam (additive; the seam still
    RETURNS an Axis per the Provider contract). When `axis is None` / `recommend_watchlist`,
    no clean operational axis exists — route to watchlist_only, do not fabricate a series."""
    axis: Optional[Axis] = None
    confidence: float = 0.0
    reason: str = ""
    data_needed_next: str = ""
    recommend_watchlist: bool = False
    source_derived: bool = False             # True ⇒ taken from parse_research_text candidates


# ── Causal Theme Compiler — ONE causal chain whose theme nodes carry axes ─────

class CausalNode(BaseModel):
    """One node in the single depth-first causal chain."""
    id: str
    statement: str
    kind: Literal["cause", "theme", "consequence"]
    axis: Optional[Axis] = None
    axis_operational: bool = False
    promoted: bool = False   # True ⇒ this theme is being routed to a strategy family

    def is_routable(self) -> bool:
        """The single source of truth for "can this node be routed to a strategy family":"""
        return self.kind == "theme" and self.axis is not None and self.axis_operational

    @model_validator(mode="after")
    def _axis_rules(self) -> "CausalNode":
        if self.axis_operational and self.axis is None:
            raise ValueError(
                f"CausalNode '{self.id}': axis_operational=True requires an axis."
            )
        if self.promoted and not self.is_routable():
            raise ValueError(
                f"CausalNode '{self.id}': a PROMOTED kind='theme' node must carry an "
                "OPERATIONAL axis (axis set and axis_operational=True) before it can be "
                "routed. An unpromoted theme candidate may omit the axis."
            )
        return self

class CausalEdge(BaseModel):
    """A single hop. inferred=True if the agent derived it; False if stated in a"""
    from_id: str
    to_id: str
    mechanism: str
    inferred: bool
    feedback: bool = False

class CausalChain(BaseModel):
    """One main theme, one chain, depth-first (no tree). Edges must reference nodes."""
    nodes: list[CausalNode]
    edges: list[CausalEdge]

    @model_validator(mode="after")
    def _edges_reference_nodes(self) -> "CausalChain":
        ids = {n.id for n in self.nodes}
        if len(ids) != len(self.nodes):
            raise ValueError("CausalChain node ids must be unique.")
        for e in self.edges:
            if e.from_id not in ids or e.to_id not in ids:
                raise ValueError(
                    f"CausalChain edge {e.from_id}->{e.to_id} references a missing node."
                )
        return self

def _chain_is_connected(chain: "CausalChain") -> bool:
    """True if the chain's nodes form ONE connected component (edges undirected)."""
    ids = [n.id for n in chain.nodes]
    if len(ids) <= 1:
        return True
    adj: dict[str, set[str]] = {i: set() for i in ids}
    for e in chain.edges:
        if e.from_id in adj and e.to_id in adj:
            adj[e.from_id].add(e.to_id)
            adj[e.to_id].add(e.from_id)
    seen: set[str] = set()
    stack = [ids[0]]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(adj[node] - seen)
    return len(seen) == len(ids)
