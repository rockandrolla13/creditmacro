"""Discovery output: ranked strategy families with decomposed confidence."""
from __future__ import annotations

from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

class ConfidenceComponents(BaseModel):
    """The decomposed factors behind a StrategyFamilyRec.confidence — stored so a low"""
    model_config = ConfigDict(frozen=True)
    causal_confidence: float = Field(ge=0.0, le=1.0)   # strength of the causal model
    axis_fit: float = Field(ge=0.0, le=1.0)            # how directly the family expresses the axis shape
    edge_survival: Union[float, Literal["unknown"]]    # thesis-aligned priced-in edge, or "unknown"
    purity: float = Field(ge=0.0, le=1.0)              # R² of the family monetisation on axis moves
    data_confidence: float = Field(ge=0.0, le=1.0)     # data sufficiency
    scenario_availability: bool                        # were scenarios supplied (never invented)?

class StrategyFamilyRec(BaseModel):
    """One ranked strategy FAMILY — the discovery half's deliverable. Routed from the"""
    model_config = ConfigDict(frozen=True)
    # Exactly the families the discovery router (engine/discovery._route_family) can produce.
    # Re-add a family only when its routing rule is implemented — the taxonomy must not
    # overstate capability. etf_basket_rv / capital_structure / index_index_rv are routed as
    # relative_value sub-types (engine/discovery._relative_value_subtype). Still wiki-taxonomy
    # only (no routing rule): curve (parent of steepener/flattener), sector_rotation.
    family: Literal[
        "steepener", "flattener", "long_short", "outright", "cash_cds_basis",
        "credit_vs_equity", "credit_vs_rates", "volatility_convexity", "watchlist_only",
        "etf_basket_rv", "capital_structure", "index_index_rv",
    ]
    direction: str                                   # the axis direction routed on (e.g. "steeper")
    rationale: str
    confidence: float = Field(ge=0.0, le=1.0)        # the capped product of the components
    why_not: Optional[str] = None                    # which factor/cap limited it (if any)
    required_downstream_model: str                   # what model turns this family into legs
    data_needed_next: str                            # what data to fetch to advance it
    confidence_components: ConfidenceComponents
    # Q4 PART-2c provenance (audit metadata, NOT a second confidence score). probability_quality
    # is the same number that floors confidence_components.data_confidence.
    probability_update_method: Optional[str] = None
    probability_quality: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    probability_warning: Optional[str] = None
    probability_update_audit_hash: Optional[str] = None
