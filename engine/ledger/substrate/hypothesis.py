"""ThemeHypothesis θ = (M, σ, X, H, F) and its parts (ONTOLOGY §Theme).

Frozen. Constructed ONLY by fold.py (I5). `d(θ)` is a DERIVED property computed
here as a function — it is NEVER a stored field (I6).
"""
from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class LifecycleStatus(str, Enum):
    CANDIDATE = "CANDIDATE"
    ACTIVE = "ACTIVE"
    FALSIFIED = "FALSIFIED"
    EXPIRED = "EXPIRED"
    RETIRED = "RETIRED"
    MERGED = "MERGED"


class TransmissionEdge(BaseModel):
    """A typed, signed causal edge v_from --s--> v_to over the node vocabulary."""
    model_config = ConfigDict(frozen=True)
    v_from: str                        # vocab node_id
    v_to: str                          # vocab node_id
    sign: int                          # s_j ∈ {+1, -1}


class Mechanism(BaseModel):
    """Signed path M: v0 --s1--> ... --sk--> vk. k = len(edges)."""
    model_config = ConfigDict(frozen=True)
    edges: tuple[TransmissionEdge, ...]

    @property
    def k(self) -> int:
        return len(self.edges)

    @property
    def v0(self) -> Optional[str]:
        return self.edges[0].v_from if self.edges else None

    @property
    def vk(self) -> Optional[str]:
        return self.edges[-1].v_to if self.edges else None

    def sign_product(self) -> int:
        """Π_j s_j."""
        p = 1
        for e in self.edges:
            p *= e.sign
        return p

    def intermediate_nodes(self) -> tuple[str, ...]:
        return tuple(e.v_to for e in self.edges[:-1])


class ThemeHypothesis(BaseModel):
    """Frozen. Do not construct outside fold.py (I5)."""
    model_config = ConfigDict(frozen=True)

    theme_id: str
    mechanism: Mechanism               # M
    shock_direction: int               # σ ∈ {+1, -1}
    operational_axis: str              # X — a tracked-axis registry axis_id
    horizon_days: int                  # H (days); WF(d) requires ≤ H_MAX
    falsifier: str                     # F — decidable predicate (text form)
    status: LifecycleStatus = LifecycleStatus.CANDIDATE
    revision: int = 0                  # fold count at construction


def derived_direction(theme: ThemeHypothesis) -> int:
    """d(θ) = σ · Π_j s_j  (ONTOLOGY §Theme). DERIVED — never stored (I6)."""
    return theme.shock_direction * theme.mechanism.sign_product()


class ThemeDefinitionView(BaseModel):
    """What Pass B may see (I3): (M, σ, X, H) ONLY — no ledger, scores, status."""
    model_config = ConfigDict(frozen=True)
    theme_id: str
    mechanism: Mechanism
    shock_direction: int
    operational_axis: str
    horizon_days: int

    @classmethod
    def of(cls, theme: ThemeHypothesis) -> "ThemeDefinitionView":
        return cls(
            theme_id=theme.theme_id,
            mechanism=theme.mechanism,
            shock_direction=theme.shock_direction,
            operational_axis=theme.operational_axis,
            horizon_days=theme.horizon_days,
        )
