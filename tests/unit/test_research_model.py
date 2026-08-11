"""Unit tests for ResearchModel (engine/research/model.py)."""
import pytest
from pydantic import ValidationError

from engine.research.model import (
    ElementStatus,
    ModelEdge,
    ModelNode,
    ModelType,
    ResearchModel,
)


def test_model_types_acceptance_and_rejection():
    """Seven model types accepted, unknown model type rejected."""
    valid_types = [
        "mechanism_chain",
        "causal_DAG",
        "prediction_chain",
        "decision_pipeline",
        "estimator_failure_model",
        "replication_logic",
        "hybrid",
    ]

    for model_type in valid_types:
        model = ResearchModel(
            model_id=f"model-{model_type}",
            model_type=model_type,
        )
        assert model.model_type == ModelType(model_type)

    for enum_val in ModelType:
        model = ResearchModel(
            model_id=f"model-enum-{enum_val.value}",
            model_type=enum_val,
        )
        assert model.model_type == enum_val

    with pytest.raises((ValidationError, ValueError)):
        ResearchModel(
            model_id="invalid-type-model",
            model_type="unknown_model_type",
        )


def test_evidence_links_attach_to_nodes_and_edges():
    """Evidence links (claims, literature, experiments, decisions) attach to nodes & edges."""
    node = ModelNode(
        node_id="v0",
        label="Policy Stance",
        claims=("claim-1", "claim-2"),
        literature=("paper-1",),
        experiments=("exp-1",),
        decisions=("dec-1",),
    )
    assert node.claims == ("claim-1", "claim-2")
    assert node.literature == ("paper-1",)
    assert node.experiments == ("exp-1",)
    assert node.decisions == ("dec-1",)
    assert node.has_evidence is True

    edge = ModelEdge(
        v_from="v0",
        v_to="v1",
        sign=1,
        claims=("claim-edge-1",),
        literature=("paper-edge-1",),
        experiments=("exp-edge-1",),
        decisions=("dec-edge-1",),
    )
    assert edge.claims == ("claim-edge-1",)
    assert edge.literature == ("paper-edge-1",)
    assert edge.experiments == ("exp-edge-1",)
    assert edge.decisions == ("dec-edge-1",)
    assert edge.has_evidence is True

    # Default evidence links are empty
    bare_node = ModelNode(node_id="bare")
    assert bare_node.claims == ()
    assert bare_node.literature == ()
    assert bare_node.experiments == ()
    assert bare_node.decisions == ()
    assert bare_node.has_evidence is False


def test_exposes_unresolved_edges():
    """Model exposes its unresolved and contested edges."""
    node0 = ModelNode(node_id="v0", status=ElementStatus.RESOLVED)
    node1 = ModelNode(node_id="v1", status=ElementStatus.RESOLVED)
    node2 = ModelNode(node_id="v2", status=ElementStatus.RESOLVED)

    edge_resolved = ModelEdge(v_from="v0", v_to="v1", sign=1, status=ElementStatus.RESOLVED)
    edge_unresolved = ModelEdge(v_from="v1", v_to="v2", sign=-1, status=ElementStatus.UNRESOLVED)
    edge_contested = ModelEdge(v_from="v2", v_to="v3", sign=1, status=ElementStatus.CONTESTED)

    model = ResearchModel(
        model_id="m1",
        model_type=ModelType.MECHANISM_CHAIN,
        nodes=(node0, node1, node2),
        edges=(edge_resolved, edge_unresolved, edge_contested),
    )

    unresolved_edges = model.unresolved_edges
    assert len(unresolved_edges) == 2
    assert edge_unresolved in unresolved_edges
    assert edge_contested in unresolved_edges
    assert edge_resolved not in unresolved_edges

    elements = model.unresolved_and_contested_elements()
    assert elements is not None
    assert len(elements.edges) == 2
    assert elements.edges == (edge_unresolved, edge_contested)


def test_fully_resolved_model_returns_none():
    """A fully-resolved model returns None for unresolved/contested elements."""
    node0 = ModelNode(node_id="v0", status=ElementStatus.RESOLVED)
    node1 = ModelNode(node_id="v1", status=ElementStatus.RESOLVED)

    edge0 = ModelEdge(v_from="v0", v_to="v1", sign=1, status=ElementStatus.RESOLVED)

    model = ResearchModel(
        model_id="fully-resolved",
        model_type=ModelType.MECHANISM_CHAIN,
        nodes=(node0, node1),
        edges=(edge0,),
    )

    assert model.unresolved_edges == ()
    assert model.unresolved_nodes == ()
    assert model.get_unresolved_edges() is None
    assert model.get_unresolved_nodes() is None
    assert model.unresolved_and_contested_elements() is None
    assert model.get_unresolved_and_contested_elements() is None


def test_mechanism_shape_properties():
    """Properties following Mechanism shape: sign_product, intermediate_nodes, endpoints, depth."""
    edge1 = ModelEdge(v_from="v0", v_to="v1", sign=-1)
    edge2 = ModelEdge(v_from="v1", v_to="v2", sign=-1)

    model = ResearchModel(
        model_id="m-path",
        model_type=ModelType.MECHANISM_CHAIN,
        edges=(edge1, edge2),
    )

    assert model.k == 2
    assert model.v0 == "v0"
    assert model.vk == "v2"
    assert model.sign_product() == 1  # (-1) * (-1)
    assert model.intermediate_nodes() == ("v1",)
    assert model.is_valid_theme_chain is True

    # Single-edge model fails depth check (k < 2 is a directional call, not a theme)
    single_edge_model = ResearchModel(
        model_id="m-single",
        model_type=ModelType.MECHANISM_CHAIN,
        edges=(edge1,),
    )
    assert single_edge_model.k == 1
    assert single_edge_model.is_valid_theme_chain is False


def test_model_immutability():
    """ResearchModel, ModelNode, ModelEdge are frozen/immutable."""
    node = ModelNode(node_id="n1")
    edge = ModelEdge(v_from="n1", v_to="n2")
    model = ResearchModel(model_id="m1", model_type=ModelType.HYBRID, nodes=(node,), edges=(edge,))

    with pytest.raises(ValidationError):
        node.label = "changed"  # type: ignore

    with pytest.raises(ValidationError):
        edge.sign = -1  # type: ignore

    with pytest.raises(ValidationError):
        model.description = "changed"  # type: ignore
