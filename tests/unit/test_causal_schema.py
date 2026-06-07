"""CausalChain schema: CausalNode / CausalEdge / CausalChain + ThemeObject fields.

Boundary rules enforced at construction (a malformed chain MUST fail):
  - a PROMOTED kind=="theme" node MUST carry an operational axis (it is being routed to a
    strategy family); a non-promoted theme CANDIDATE may exist without one (a broad hot
    topic is a valid discovery artifact, not a trade)
  - a dead-end (cause/consequence with axis=None) is valid — never an invented axis
  - every edge endpoint must reference an existing node id
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from engine.schema import (
    Axis,
    AxisHistory,
    CausalChain,
    CausalEdge,
    CausalNode,
)


def _axis(name="X = A OAS − B OAS, bps"):
    return Axis(
        definition=name, measurement="daily close, bps",
        current_value=40.0,
        history=AxisHistory(mean=70.0, vol=30.0, percentile=10.0, regime_tags=["x"]),
    )


def test_promoted_theme_node_requires_operational_axis():
    # A theme being ROUTED to a strategy family must carry a computable axis.
    with pytest.raises(ValidationError):
        CausalNode(id="n1", statement="tradeable", kind="theme", axis=None, promoted=True)


def test_unpromoted_theme_candidate_may_lack_axis():
    # A broad core-theme candidate (e.g. "AI capex funding") is a valid discovery
    # artifact without an axis — it just cannot be routed to a trade yet.
    n = CausalNode(id="n1", statement="AI capex funding (broad)", kind="theme", axis=None)
    assert n.promoted is False
    assert n.axis is None
    assert n.axis_operational is False


def test_theme_node_with_axis_is_valid():
    n = CausalNode(id="n1", statement="t", kind="theme", axis=_axis(),
                   axis_operational=True, promoted=True)
    assert n.axis_operational is True
    assert n.axis is not None


def test_axis_operational_true_requires_axis():
    with pytest.raises(ValidationError):
        CausalNode(id="n1", statement="t", kind="cause", axis=None, axis_operational=True)


def test_dead_end_mechanism_node_is_valid():
    # a cause/consequence with no axis is a valid mechanism link (dead end)
    n = CausalNode(id="n0", statement="driver", kind="cause", axis=None)
    assert n.axis is None and n.axis_operational is False


def test_edge_tags_and_feedback_default():
    e = CausalEdge(from_id="a", to_id="b", mechanism="m", inferred=True)
    assert e.inferred is True and e.feedback is False


def test_chain_rejects_edge_to_missing_node():
    nodes = [CausalNode(id="a", statement="s", kind="cause")]
    with pytest.raises(ValidationError):
        CausalChain(nodes=nodes, edges=[CausalEdge(from_id="a", to_id="ghost", mechanism="m", inferred=True)])


def test_valid_chain_constructs():
    nodes = [
        CausalNode(id="a", statement="driver", kind="cause"),
        CausalNode(id="b", statement="tradeable", kind="theme", axis=_axis(), axis_operational=True),
    ]
    edges = [CausalEdge(from_id="a", to_id="b", mechanism="transmission", inferred=False)]
    chain = CausalChain(nodes=nodes, edges=edges)
    assert len(chain.nodes) == 2 and len(chain.edges) == 1


def test_theme_object_causal_fields_optional_default_none():
    from engine.example import theme  # golden theme builds without causal fields
    assert theme.main_theme is None
    assert theme.causal_chain is None
    assert theme.shared_factor is None
