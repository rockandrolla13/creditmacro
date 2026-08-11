"""V4 ResearchStimulus — spec sections 5.1 through 5.4.

A ResearchStimulus records WHY research began and exists before any scientific framing.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StimulusOriginType(str, Enum):
    """Allowed origin types per V4 spec 5.2."""

    RESEARCHER = "researcher"
    PAPER = "paper"
    MARKET_OBSERVATION = "market_observation"
    EXPERIMENT_RESULT = "experiment_result"
    FAILED_EXPERIMENT = "failed_experiment"
    CONTRADICTION = "contradiction"
    LITERATURE_GAP = "literature_gap"
    SYNTHESIS = "synthesis"
    EXTERNAL_EVENT = "external_event"
    DATASET_EVENT = "dataset_event"
    AGENT_GENERATED = "agent_generated"


class StimulusOrigin(BaseModel):
    """Origin metadata specifying where and how the stimulus originated (spec 5.3)."""

    model_config = ConfigDict(frozen=True)

    type: StimulusOriginType
    actor_id: Optional[str] = None
    source_ref: Optional[str] = None
    derived_from: list[str] = Field(default_factory=list)

    @field_validator("derived_from", mode="before")
    @classmethod
    def _normalize_derived_from(cls, v: object) -> list[str]:
        if v is None:
            return []
        if isinstance(v, str):
            return [v]
        if isinstance(v, (list, tuple)):
            return [str(item) for item in v]
        return v


class StimulusContent(BaseModel):
    """Content payload per spec 5.3."""

    model_config = ConfigDict(frozen=True)

    raw: str
    summary: Optional[str] = None


class StimulusCapture(BaseModel):
    """Capture metadata per spec 5.3."""

    model_config = ConfigDict(frozen=True)

    actor_type: str
    actor_id: str
    timestamp: datetime


class ResearchStimulus(BaseModel):
    """A ResearchStimulus records WHY research began and exists before any scientific framing.

    Frozen pydantic model per V4 spec 5.1 - 5.4.
    """

    model_config = ConfigDict(frozen=True)

    stimulus_id: str
    origin: StimulusOrigin
    content: StimulusContent
    occurred_at: datetime
    captured_by: StimulusCapture
    context_refs: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    status: str = "captured"

    @field_validator("context_refs", "evidence_refs", mode="before")
    @classmethod
    def _normalize_string_lists(cls, v: object) -> list[str]:
        if v is None:
            return []
        if isinstance(v, str):
            return [v]
        if isinstance(v, (list, tuple)):
            return [str(item) for item in v]
        return v

    @model_validator(mode="after")
    def _validate_provenance_invariant(self) -> ResearchStimulus:
        """Enforce spec 5.4 provenance invariant:

        1. An origin of type 'agent_generated' MUST have a non-empty derived_from.
        2. Any other origin type MUST NOT take the capturing agent's id as its actor_id.
        """
        if self.origin.type == StimulusOriginType.AGENT_GENERATED:
            if not self.origin.derived_from:
                raise ValueError("An origin of type 'agent_generated' MUST have a non-empty 'derived_from'.")
        else:
            if (
                self.origin.actor_id is not None
                and self.captured_by.actor_id is not None
                and self.origin.actor_id == self.captured_by.actor_id
            ):
                raise ValueError(
                    f"Origin actor_id '{self.origin.actor_id}' cannot match capturing actor_id "
                    f"'{self.captured_by.actor_id}' for non-agent origin type '{self.origin.type}'."
                )
        return self


# Convenient aliases
OriginType = StimulusOriginType
Origin = StimulusOrigin
Content = StimulusContent
Capture = StimulusCapture
