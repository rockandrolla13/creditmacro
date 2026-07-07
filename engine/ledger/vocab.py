"""Controlled transmission-node vocabulary V (METHOD memory) + tracked-axis
registry + the crosswalk that de-islands the ledger (ONTOLOGY §Vocabulary,
AMEND A1).

Each node binds to the EXISTING method graph so Pass B's structural pre-match
and every wiki render can join `schema.causal.CausalNode` names and wiki
concept slugs. A node with neither a `causal_node` nor `wiki_concepts` is a
NEW method claim and must route through the review queue — never silently added.

STATUS: Phase-0 seed. ~20 of the ~60 target nodes are enumerated across the
Collin-Dufresne / credit-BMI factor families. Completing V to ~60 and filling
the crosswalk is a Phase-0 deliverable (see PLAN_TRACKER.md).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class VocabNode:
    """One transmission node. `causal_node` / `wiki_concepts` are the A1 crosswalk."""
    node_id: str
    family: str                                  # factor family (see FAMILIES)
    description: str
    synonyms: tuple[str, ...] = ()
    causal_node: Optional[str] = None            # schema.causal.CausalNode name, if any
    wiki_concepts: tuple[str, ...] = ()          # wiki concept slugs, if any
    driver_tags: tuple[str, ...] = ()            # legacy free-string Observation.driver_tags


@dataclass(frozen=True)
class TrackedAxis:
    """A member of the tracked-axis registry (WF clause c). `sign` maps
    'axis value up' → vk up (+1) or vk down (-1)."""
    axis_id: str
    description: str
    sign: int                                    # ∈ {+1, -1}
    data_feed: Optional[str] = None              # series identifier for the falsifier feed


FAMILIES = (
    "volatility", "momentum", "sentiment", "liquidity_funding",
    "supply", "business_cycle", "valuation", "policy", "structure",
)

# ── V seed (partial; TODO complete to ~60) ────────────────────────────────────
_SEED: tuple[VocabNode, ...] = (
    VocabNode("funding_stress", "liquidity_funding",
              "cost/availability of wholesale funding tightening",
              ("funding squeeze", "repo stress"), wiki_concepts=("funding",),
              driver_tags=("funding",)),
    VocabNode("dealer_balance_sheet_capacity", "liquidity_funding",
              "intermediary balance-sheet room to warehouse risk",
              ("dealer capacity", "intermediation capacity")),
    VocabNode("liquidity_premium", "liquidity_funding",
              "compensation for illiquidity in the spread",
              ("illiquidity premium",), wiki_concepts=("limited-syndication",)),
    VocabNode("default_expectations", "valuation",
              "expected default frequency / loss given default",
              ("expected default", "credit risk premium")),
    VocabNode("term_premium", "policy",
              "compensation for duration/term risk",
              ("duration premium",)),
    VocabNode("issuance_supply", "supply",
              "primary-market issuance technical / net supply",
              ("net supply", "primary supply"), wiki_concepts=("index-inclusion-technical",),
              driver_tags=("supply",)),
    VocabNode("risk_appetite", "sentiment",
              "aggregate appetite for risk assets",
              ("risk-on", "risk-off")),
    VocabNode("earnings_trajectory", "business_cycle",
              "corporate earnings / cash-flow trend",
              ("earnings trend", "margin trajectory")),
    VocabNode("policy_stance", "policy",
              "monetary-policy stance / rate path",
              ("Fed stance", "rate path")),
    VocabNode("realized_volatility", "volatility",
              "realized asset-price volatility",
              ("vol", "rv")),
    VocabNode("spread_momentum", "momentum",
              "trend persistence in credit spreads",
              ("credit momentum",)),
    VocabNode("index_inclusion_demand", "structure",
              "forced/again index-driven demand technical",
              ("index demand",), wiki_concepts=("index-inclusion-technical", "144a-for-life")),
    VocabNode("capex_funding_need", "supply",
              "capex-driven external funding requirement",
              ("capex funding",), wiki_concepts=("data-center-credit",),
              driver_tags=("ai-capex",)),
    VocabNode("hyperscaler_credit_demand", "supply",
              "hyperscaler IG issuance to fund capex",
              (), wiki_concepts=("hyperscaler-project-bond-basis-mechanics",)),
    VocabNode("project_bond_supply", "supply",
              "data-center project-bond issuance",
              (), wiki_concepts=("data-center-credit",)),
    VocabNode("crowding", "sentiment",
              "position crowding / consensus positioning",
              ("consensus positioning",), wiki_concepts=("high-performance-computing-credit",)),
    VocabNode("subordination_risk", "structure",
              "recourse / subordination / structural seniority",
              ("structural subordination",)),
    VocabNode("inflation_pass_through", "business_cycle",
              "inflation pricing pressure passed to spreads",
              ("inflation pass-through",)),
    VocabNode("financial_conditions", "policy",
              "aggregate financial-conditions tightness/looseness",
              ("FCI",)),
    VocabNode("related_obligation_linkage", "structure",
              "common-driver linkage across related obligations",
              (), wiki_concepts=("related-obligation-rv",)),
    VocabNode("credit_spread", "valuation",
              "terminal credit-spread level (a common vk)",
              ("spread", "oas")),
)

NODES: dict[str, VocabNode] = {n.node_id: n for n in _SEED}

# ── tracked-axis registry seed (WF clause c; TODO extend — see BLOCKED B-03) ──
TRACKED_AXES: dict[str, TrackedAxis] = {
    a.axis_id: a for a in (
        TrackedAxis("C0A0_OAS", "IG corporate OAS (ICE BofA)", +1, "C0A0"),
        TrackedAxis("H0A0_OAS", "HY corporate OAS (ICE BofA)", +1, "H0A0"),
        TrackedAxis("CDX_IG_5Y", "CDX.IG 5Y spread", +1, "CDX.IG.5Y"),
        TrackedAxis("CDX_HY_5Y", "CDX.HY 5Y spread", +1, "CDX.HY.5Y"),
        TrackedAxis("3M10Y", "3M–10Y Treasury slope", +1, "UST.3M10Y"),
        TrackedAxis("HYPER_IG_PROJECT_BASIS",
                    "hyperscaler IG OAS − IG DC-project OAS", +1, None),
    )
}


def is_node(node_id: str) -> bool:
    return node_id in NODES


def is_tracked_axis(axis_id: str) -> bool:
    return axis_id in TRACKED_AXES


def is_out_of_vocabulary(node_id: str) -> bool:
    """A tag not in V → routes to the review queue (§Admission, out-of-vocab)."""
    return node_id not in NODES
