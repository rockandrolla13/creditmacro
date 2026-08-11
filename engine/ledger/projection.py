"""Bridge: ThemeHypothesis → engine ThemeObject (AMEND A3, D-01). Phase-7.

The ledger is the re-founded Stage-0/1 front end; `schema.ThemeObject` is downstream
and its DISCOVERY-half is a projection of a fold. This module is the ONLY site
permitted to map between the three status axes (A3): §Lifecycle (market truth) →
`ThemeObject.status` (pipeline). Edge-level signs are summarized by d(θ) (the thesis
direction the engine consumes); the falsifier is parked in provenance.evidence until
Engine-4 (Risk). `test_projection_roundtrip` proves the projected object is a valid,
freezable engine object whose discovery content equals the hypothesis.
"""
from __future__ import annotations

from engine.schema.theme import ThemeObject
from engine.schema.causal import (
    Axis, AxisHistory, CausalChain, CausalChainStep, CausalEdge, CausalNode, Driver, Thesis,
)
from engine.schema.risk import Provenance

from .substrate.hypothesis import LifecycleStatus, ThemeHypothesis, derived_direction

_LIVE = (LifecycleStatus.CANDIDATE, LifecycleStatus.ACTIVE)


def to_theme_object(theme: ThemeHypothesis, as_of: str) -> ThemeObject:
    edges = theme.mechanism.edges
    # fold() is the only constructor and deliberately does NOT run WF (I5), so a
    # malformed hypothesis can reach the bridge. An empty chain has no v0, no vk and
    # no transmission to render: every field below would be invented, not projected.
    # Refuse it — WF clause (a) already rejects k < 2, and a missing output beats an
    # unsourced one. Non-empty chains project as before; the projection is a renderer,
    # not the WF gate (identity.wf_predicate is).
    if not edges:
        raise ValueError(
            f"theme {theme.theme_id!r}: cannot project a mechanism with no edges "
            "(WF clause (a) requires k >= 2). Route it to NEEDS_STRUCTURING instead."
        )

    d = derived_direction(theme)
    thesis = Thesis(
        drivers=[Driver(
            name=edges[0].v_from,
            sign="+" if theme.shock_direction > 0 else "-",
            proxy_observable=theme.operational_axis,
            mechanism="ledger transmission chain",
        )],
        causal_chain=[CausalChainStep(from_node=e.v_from, to_node=e.v_to) for e in edges],
        direction_of_view=str(d),
    )
    # The ledger names an axis; it does not observe one. Leaving these unset is the
    # point: a projected theme has no measured level, history or scored confidence yet,
    # and 0.0 would present all three as findings. Downstream already handles the
    # absence — engine2.run_pricing skips the vol-adjusted edge when sigma is None.
    axis = Axis(
        definition=f"ledger axis {theme.operational_axis}",
        measurement=theme.operational_axis,
    )
    provenance = Provenance(evidence=[f"falsifier: {theme.falsifier}"])

    # Top-level causal object (Discovery Gate 1) + a routable main_theme (Gate 2).
    node_ids = [edges[0].v_from] + [e.v_to for e in edges]
    main_theme = CausalNode(
        id=node_ids[-1],
        statement=node_ids[-1],
        kind="theme",
        axis=axis,
        axis_operational=True,
    )
    causal_nodes = [
        CausalNode(
            id=nid,
            statement=nid,
            kind="cause" if i == 0 else "theme",
        )
        for i, nid in enumerate(node_ids[:-1])
    ] + [main_theme]
    causal_chain = CausalChain(
        nodes=causal_nodes,
        edges=[
            CausalEdge(from_id=e.v_from, to_id=e.v_to, mechanism="transmission", inferred=False)
            for e in edges
        ],
    )

    live = theme.status in _LIVE
    return ThemeObject(
        id=theme.theme_id,
        statement=f"{theme.mechanism.v0} → {theme.mechanism.vk} (d={d:+d})",
        horizon=f"{theme.horizon_days}d", author="ledger",
        status="discovery_complete" if live else "blocked",           # A3 axis mapping
        block_reason=None if live else f"ledger status {theme.status.value}",
        thesis=thesis, axis=axis, provenance=provenance,
        causal_chain=causal_chain, main_theme=main_theme,
    )
