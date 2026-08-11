"""Unit tests for ResearchStimulus per V4 spec 5.1 through 5.4."""
from datetime import datetime, timezone
import pytest
from pydantic import ValidationError

from engine.research.stimulus import (
    ResearchStimulus,
    StimulusOrigin,
    StimulusOriginType,
    StimulusContent,
    StimulusCapture,
)


def test_researcher_idea_captured_by_agent_retains_researcher_origin():
    """Case 1: A researcher idea captured by an agent retains researcher origin."""
    occurred_at = datetime(2026, 8, 11, 10, 0, tzinfo=timezone.utc)
    captured_at = datetime(2026, 8, 11, 10, 5, tzinfo=timezone.utc)

    stimulus = ResearchStimulus(
        stimulus_id="stim_001",
        origin=StimulusOrigin(
            type=StimulusOriginType.RESEARCHER,
            actor_id="andreas",
            source_ref="conversation_note_42",
        ),
        content=StimulusContent(
            raw="Hypothesis about GPU-backed debt basis widening.",
            summary="GPU debt basis hypothesis",
        ),
        occurred_at=occurred_at,
        captured_by=StimulusCapture(
            actor_type="agent",
            actor_id="assistant_agent_alpha",
            timestamp=captured_at,
        ),
    )

    assert stimulus.origin.type == StimulusOriginType.RESEARCHER
    assert stimulus.origin.actor_id == "andreas"
    assert stimulus.captured_by.actor_id == "assistant_agent_alpha"
    assert stimulus.origin.actor_id != stimulus.captured_by.actor_id


def test_paper_origin_retained():
    """Case 2: A paper origin is retained when captured by an agent."""
    occurred_at = datetime(2021, 2, 1, 0, 0, tzinfo=timezone.utc)
    captured_at = datetime(2026, 8, 11, 11, 0, tzinfo=timezone.utc)

    stimulus = ResearchStimulus(
        stimulus_id="stim_002",
        origin=StimulusOrigin(
            type=StimulusOriginType.PAPER,
            actor_id="vayanos_vila_2021",
            source_ref="arXiv:2102.12345",
        ),
        content=StimulusContent(
            raw="Preferred habitat demand shocks create localized rate effects.",
            summary="Preferred habitat model paper",
        ),
        occurred_at=occurred_at,
        captured_by=StimulusCapture(
            actor_type="agent",
            actor_id="literature_ingest_agent",
            timestamp=captured_at,
        ),
    )

    assert stimulus.origin.type == StimulusOriginType.PAPER
    assert stimulus.origin.source_ref == "arXiv:2102.12345"
    assert stimulus.origin.actor_id == "vayanos_vila_2021"
    assert stimulus.captured_by.actor_id == "literature_ingest_agent"


def test_experiment_result_references_originating_analysis():
    """Case 3: An experiment_result references its originating analysis."""
    occurred_at = datetime(2026, 8, 10, 15, 30, tzinfo=timezone.utc)
    captured_at = datetime(2026, 8, 10, 15, 31, tzinfo=timezone.utc)

    stimulus = ResearchStimulus(
        stimulus_id="stim_003",
        origin=StimulusOrigin(
            type=StimulusOriginType.EXPERIMENT_RESULT,
            source_ref="analysis_run_20260810_01",
            derived_from=["exp_setup_88"],
        ),
        content=StimulusContent(
            raw="Residual edge exceeded 25bp threshold across all pricing scenarios.",
            summary="Positive residual edge in experiment",
        ),
        occurred_at=occurred_at,
        captured_by=StimulusCapture(
            actor_type="agent",
            actor_id="exp_runner_agent",
            timestamp=captured_at,
        ),
    )

    assert stimulus.origin.type == StimulusOriginType.EXPERIMENT_RESULT
    assert stimulus.origin.source_ref == "analysis_run_20260810_01"
    assert "exp_setup_88" in stimulus.origin.derived_from


def test_agent_generated_without_derived_from_rejected():
    """Case 4: An agent_generated stimulus without derived_from is REJECTED."""
    occurred_at = datetime(2026, 8, 11, 12, 0, tzinfo=timezone.utc)
    captured_at = datetime(2026, 8, 11, 12, 0, tzinfo=timezone.utc)

    with pytest.raises(ValidationError) as exc_info:
        ResearchStimulus(
            stimulus_id="stim_004",
            origin=StimulusOrigin(
                type=StimulusOriginType.AGENT_GENERATED,
                actor_id="synthesis_agent",
                derived_from=[],
            ),
            content=StimulusContent(
                raw="Spontaneous idea without derivation.",
            ),
            occurred_at=occurred_at,
            captured_by=StimulusCapture(
                actor_type="agent",
                actor_id="synthesis_agent",
                timestamp=captured_at,
            ),
        )

    assert "agent_generated" in str(exc_info.value)
    assert "derived_from" in str(exc_info.value)


def test_agent_generated_with_derived_from_accepted():
    """An agent_generated stimulus WITH derived_from is accepted."""
    occurred_at = datetime(2026, 8, 11, 12, 0, tzinfo=timezone.utc)
    captured_at = datetime(2026, 8, 11, 12, 0, tzinfo=timezone.utc)

    stimulus = ResearchStimulus(
        stimulus_id="stim_005",
        origin=StimulusOrigin(
            type=StimulusOriginType.AGENT_GENERATED,
            actor_id="synthesis_agent",
            derived_from=["stim_001", "stim_002"],
        ),
        content=StimulusContent(
            raw="Synthesized hypothesis combining GPU debt and rate preferred habitat.",
        ),
        occurred_at=occurred_at,
        captured_by=StimulusCapture(
            actor_type="agent",
            actor_id="synthesis_agent",
            timestamp=captured_at,
        ),
    )

    assert stimulus.origin.type == StimulusOriginType.AGENT_GENERATED
    assert stimulus.origin.derived_from == ["stim_001", "stim_002"]


def test_invalid_origin_type_rejected():
    """Free string origin types are rejected."""
    occurred_at = datetime(2026, 8, 11, 12, 0, tzinfo=timezone.utc)
    captured_at = datetime(2026, 8, 11, 12, 0, tzinfo=timezone.utc)

    with pytest.raises(ValidationError):
        ResearchStimulus(
            stimulus_id="stim_bad_type",
            origin=StimulusOrigin(
                type="custom_free_string",  # type: ignore
            ),
            content=StimulusContent(raw="test"),
            occurred_at=occurred_at,
            captured_by=StimulusCapture(
                actor_type="agent",
                actor_id="agent_1",
                timestamp=captured_at,
            ),
        )


def test_non_agent_origin_matching_capturing_agent_rejected():
    """Non-agent origin MUST NOT take the capturing agent's id as its actor_id."""
    occurred_at = datetime(2026, 8, 11, 12, 0, tzinfo=timezone.utc)
    captured_at = datetime(2026, 8, 11, 12, 0, tzinfo=timezone.utc)

    with pytest.raises(ValidationError) as exc_info:
        ResearchStimulus(
            stimulus_id="stim_conflated",
            origin=StimulusOrigin(
                type=StimulusOriginType.RESEARCHER,
                actor_id="agent_alpha",  # Conflated with capturing agent
            ),
            content=StimulusContent(raw="Idea pretending to be researcher from agent"),
            occurred_at=occurred_at,
            captured_by=StimulusCapture(
                actor_type="agent",
                actor_id="agent_alpha",
                timestamp=captured_at,
            ),
        )

    assert "cannot match capturing actor_id" in str(exc_info.value)


def test_all_eleven_origin_types_exist():
    """Verify all 11 origin types specified in V4 5.2 are supported."""
    expected_types = {
        "researcher",
        "paper",
        "market_observation",
        "experiment_result",
        "failed_experiment",
        "contradiction",
        "literature_gap",
        "synthesis",
        "external_event",
        "dataset_event",
        "agent_generated",
    }
    actual_types = {item.value for item in StimulusOriginType}
    assert actual_types == expected_types


def test_model_is_frozen():
    """Verify ResearchStimulus is immutable (frozen)."""
    occurred_at = datetime(2026, 8, 11, 12, 0, tzinfo=timezone.utc)
    captured_at = datetime(2026, 8, 11, 12, 0, tzinfo=timezone.utc)

    stimulus = ResearchStimulus(
        stimulus_id="stim_frozen",
        origin=StimulusOrigin(
            type=StimulusOriginType.MARKET_OBSERVATION,
            source_ref="Bloomberg_123",
        ),
        content=StimulusContent(raw="Observation"),
        occurred_at=occurred_at,
        captured_by=StimulusCapture(
            actor_type="agent",
            actor_id="collector",
            timestamp=captured_at,
        ),
    )

    with pytest.raises(ValidationError):
        stimulus.status = "archived"  # type: ignore
