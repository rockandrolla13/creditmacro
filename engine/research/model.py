"""ResearchModel per V4 spec sections 10.1 through 10.5.

A ResearchModel explicitly describes how the system believes a phenomenon may work,
and serves as the bridge from evidence state to hypotheses.
Modelled as a typed, frozen node/edge graph.
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, field_validator


class ModelType(str, Enum):
    """The seven supported research model types per V4 spec section 10.2."""
    MECHANISM_CHAIN = "mechanism_chain"
    CAUSAL_DAG = "causal_DAG"
    PREDICTION_CHAIN = "prediction_chain"
    DECISION_PIPELINE = "decision_pipeline"
    ESTIMATOR_FAILURE_MODEL = "estimator_failure_model"
    REPLICATION_LOGIC = "replication_logic"
    HYBRID = "hybrid"


class ElementStatus(str, Enum):
    """Resolution status for nodes and edges per V4 spec section 10.4."""
    UNRESOLVED = "unresolved"
    CONTESTED = "contested"
    RESOLVED = "resolved"


class ModelNode(BaseModel):
    """A node in a ResearchModel representing a phenomenon, driver, or variable."""
    model_config = ConfigDict(frozen=True)

    node_id: str
    label: str = ""
    status: ElementStatus = ElementStatus.UNRESOLVED
    claims: tuple[str, ...] = ()
    literature: tuple[str, ...] = ()
    experiments: tuple[str, ...] = ()
    decisions: tuple[str, ...] = ()

    @field_validator("claims", "literature", "experiments", "decisions", mode="before")
    @classmethod
    def _to_tuple(cls, v: Any) -> tuple[str, ...]:
        if isinstance(v, (list, set)):
            return tuple(v)
        return v if v is not None else ()

    @property
    def is_unresolved(self) -> bool:
        return self.status == ElementStatus.UNRESOLVED

    @property
    def is_contested(self) -> bool:
        return self.status == ElementStatus.CONTESTED

    @property
    def is_unresolved_or_contested(self) -> bool:
        return self.status in (ElementStatus.UNRESOLVED, ElementStatus.CONTESTED)

    @property
    def has_evidence(self) -> bool:
        return bool(self.claims or self.literature or self.experiments or self.decisions)


class ModelEdge(BaseModel):
    """A signed, typed causal or logical edge v_from --sign--> v_to in a ResearchModel."""
    model_config = ConfigDict(frozen=True)

    v_from: str
    v_to: str
    sign: int = 1
    status: ElementStatus = ElementStatus.UNRESOLVED
    claims: tuple[str, ...] = ()
    literature: tuple[str, ...] = ()
    experiments: tuple[str, ...] = ()
    decisions: tuple[str, ...] = ()

    @field_validator("sign", mode="before")
    @classmethod
    def _validate_sign(cls, v: Any) -> int:
        s = int(v)
        if s not in (+1, -1):
            raise ValueError(f"Edge sign must be +1 or -1, got {v}")
        return s

    @field_validator("claims", "literature", "experiments", "decisions", mode="before")
    @classmethod
    def _to_tuple(cls, v: Any) -> tuple[str, ...]:
        if isinstance(v, (list, set)):
            return tuple(v)
        return v if v is not None else ()

    @property
    def is_unresolved(self) -> bool:
        return self.status == ElementStatus.UNRESOLVED

    @property
    def is_contested(self) -> bool:
        return self.status == ElementStatus.CONTESTED

    @property
    def is_unresolved_or_contested(self) -> bool:
        return self.status in (ElementStatus.UNRESOLVED, ElementStatus.CONTESTED)

    @property
    def has_evidence(self) -> bool:
        return bool(self.claims or self.literature or self.experiments or self.decisions)


class UnresolvedElements(BaseModel):
    """Unresolved and contested elements extracted from a ResearchModel (Spec 10.5)."""
    model_config = ConfigDict(frozen=True)

    nodes: tuple[ModelNode, ...] = ()
    edges: tuple[ModelEdge, ...] = ()

    @property
    def is_empty(self) -> bool:
        return not self.nodes and not self.edges

    def __bool__(self) -> bool:
        return not self.is_empty


class ResearchModel(BaseModel):
    """A frozen, typed node/edge graph describing a phenomenon (V4 spec §§10.1-10.5)."""
    model_config = ConfigDict(frozen=True)

    model_id: str
    model_type: ModelType
    nodes: tuple[ModelNode, ...] = ()
    edges: tuple[ModelEdge, ...] = ()
    description: str = ""

    @field_validator("nodes", "edges", mode="before")
    @classmethod
    def _sequence_to_tuple(cls, v: Any) -> tuple:
        if isinstance(v, (list, set)):
            return tuple(v)
        return v if v is not None else ()

    @field_validator("model_type", mode="before")
    @classmethod
    def _validate_model_type(cls, v: Any) -> ModelType:
        if isinstance(v, ModelType):
            return v
        try:
            return ModelType(v)
        except ValueError:
            raise ValueError(
                f"Invalid model_type '{v}'. Supported model types are: "
                f"{[t.value for t in ModelType]}"
            )

    # ── Path & Graph reasoning (following Mechanism shape without ledger import) ──

    @property
    def k(self) -> int:
        """Number of edges in the model."""
        return len(self.edges)

    @property
    def v0(self) -> Optional[str]:
        """Start node of the edge chain (if any)."""
        return self.edges[0].v_from if self.edges else None

    @property
    def vk(self) -> Optional[str]:
        """End node of the edge chain (if any)."""
        return self.edges[-1].v_to if self.edges else None

    def sign_product(self) -> int:
        """Product of edge signs along the edge list: Π_j s_j."""
        p = 1
        for e in self.edges:
            p *= e.sign
        return p

    def intermediate_nodes(self) -> tuple[str, ...]:
        """Intermediate nodes in an edge chain: tuple of v_to for edges[:-1]."""
        return tuple(e.v_to for e in self.edges[:-1])

    @property
    def is_valid_theme_chain(self) -> bool:
        """Rejects a chain with fewer than 2 edges as a directional call rather than a theme."""
        return self.k >= 2

    # ── Spec 10.5: Unresolved & Contested elements extraction ──

    @property
    def unresolved_nodes(self) -> tuple[ModelNode, ...]:
        return tuple(n for n in self.nodes if n.is_unresolved_or_contested)

    @property
    def unresolved_edges(self) -> tuple[ModelEdge, ...]:
        return tuple(e for e in self.edges if e.is_unresolved_or_contested)

    def get_unresolved_edges(self) -> Optional[tuple[ModelEdge, ...]]:
        """Returns unresolved edges or None if fully resolved."""
        edges = self.unresolved_edges
        return edges if edges else None

    def get_unresolved_nodes(self) -> Optional[tuple[ModelNode, ...]]:
        """Returns unresolved nodes or None if fully resolved."""
        nodes = self.unresolved_nodes
        return nodes if nodes else None

    def unresolved_and_contested_elements(self) -> Optional[UnresolvedElements]:
        """Spec 10.5: Return unresolved and contested nodes and edges.

        Returns an UnresolvedElements object if any unresolved/contested nodes
        or edges exist, or None if the model is fully resolved.
        """
        nodes = self.unresolved_nodes
        edges = self.unresolved_edges
        if not nodes and not edges:
            return None
        return UnresolvedElements(nodes=nodes, edges=edges)

    def get_unresolved_and_contested_elements(self) -> Optional[UnresolvedElements]:
        """Alias for unresolved_and_contested_elements (Spec 10.5)."""
        return self.unresolved_and_contested_elements()
