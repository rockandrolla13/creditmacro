---
skill_name: global-io-network
access_class: method
compiled_from: ["koopman_wang_wei_2014_value_added_exports.md"]
pipeline_phase: causal_system_network
provider_seam: [Provider.build_system_map]
input_objects: [CausalChain, driver, shock_node, region_sector_universe, icio_table, final_demand_vector, method_context]
output_objects: [GlobalIONetwork, region_sector_nodes, value_added_edges, leontief_inverse, upstream_downstream_exposure, propagated_shock_map, unlisted_supplier_exposure]
gates_created: [node_must_be_region_sector, edge_must_be_value_added_flow, shock_requires_leontief_propagation, double_counted_flow_not_an_exposure]
allowed_to_influence: [system-map topology, which region-sector nodes are exposed to a shock, upstream/downstream supplier exposure, candidate operational-axis nodes, confounder/falsifier list for the causal layer]
not_allowed_to_influence: [pricing numbers that change golden master, sizing, trades, execution]
failure_modes: [confusing gross-trade flow with value-added exposure, double-counting intermediate goods that cross borders twice, treating a node's direct supplier only and missing indirect upstream tiers, propagating a shock without the Leontief inverse, asserting a tradeable name instead of a structural node]
tests: [test_io_network_node_is_region_sector, test_io_network_edge_value_added_not_gross, test_io_network_leontief_propagation, test_io_network_double_counting_excluded, test_io_network_unlisted_supplier_surfaced]
---

# Global IO Network

> **Compiled from** Koopman, Wang & Wei, *Tracing Value-Added and Double Counting in Gross Exports*
> (NBER WP 18579 / AER 2014). Read: the gross-exports accounting concepts (§2.1), the inter-country
> input-output (ICIO) model and Leontief-inverse "total requirement" matrix (§2.2), the value-added
> decomposition and double-counting terms (§2.2–2.3), and the general G-country / N-sector block-matrix
> form (§2.5). Skipped: the database-construction details (§3) and the empirical revealed-comparative-
> advantage / trade-cost applications (§4). METHOD card: a structural primitive only — no case
> conclusions, no trades, no numbers that move pricing.

## Purpose
Build a **global input-output network** so the causal/system layer can take a shock at one node (a
tariff, an export ban, a capex block, a sanctioned sector) and **propagate the downstream impairment**
across the production web — including *unlisted* suppliers that never appear in a screen of tradeable
names. The network is a structural object: **region-sector nodes** joined by **value-added-flow edges**,
with the Leontief inverse giving the *total* (direct + all indirect) requirement of one node's output
per unit of final demand elsewhere. It is the substrate on which a shock travels; it is **not** a trade.

## When to use
In the causal/system phase, when a `CausalChain` names a driver whose transmission is *supply-chain
structural* — i.e. a shock to one producing node mechanically pulls on its up- and down-stream
neighbours. Use it to surface which region-sectors are exposed and to find candidate operational-axis
nodes. Build it in Phase A fresh reasoning; do not consult case history while constructing topology.

## Process primitives
- **Node = region × sector, not a company.** Each node is a producing (country/region, sector) cell of
  an inter-country input-output table. Resist collapsing a node to a single listed issuer; the point is
  to see the *structure* behind the issuer, including unlisted upstream tiers.
- **Edge = value-added flow, not gross trade.** Gross-export figures double-count any intermediate good
  that crosses a border more than once. An edge in this network carries *value added by a source node*,
  net of value that merely passes through. Treat a gross-flow number as a confounded measure: decompose
  it before using it as an exposure.
- **The accounting identity.** A node's gross output is fully absorbed as intermediate input or final
  good, at home or abroad: `x = A x + y`, where `A` is the matrix of input-output coefficients (units of
  a source node's output needed per unit of a destination node's output) and `y` is final demand.
- **The Leontief inverse is the propagation operator.** Solve `x = (I − A)^{-1} y = B y`. The entry
  `B[s,r]` is the *total* output of source node *s* required to sustain one unit of final demand at
  destination node *r* — it sums the direct requirement plus every indirect tier (s feeds a supplier
  that feeds a supplier … that feeds r). Propagating a shock means applying `B`, not just reading
  first-degree neighbours. This is what surfaces deep, unlisted upstream exposure.
- **Value-added share matrix.** Pre-multiply `B` by the diagonal direct value-added coefficients `V`
  (`V = I − column-sums of A`) to get `VB`, the share of each destination's output value contributed by
  each source node. Columns sum to one (all value added is someone's). `VB` is how a final-demand or
  cost shock is attributed back to the nodes that actually created the value.
- **Decompose every cross-border flow before treating it as exposure (Koopman-Wang-Wei).** Split a
  node's gross exports into: (1) value added absorbed abroad (true downstream exposure); (2) domestic
  value added that leaves and returns home; (3) foreign value added embedded in its exports; and
  (4) **pure double-counted terms** that arise only with two-way intermediate trade. Only the
  value-added components are real exposures; the double-counted terms must be netted out, or a shock's
  reach is overstated.
- **Direction matters.** Upstream exposure (a node *supplies* the shocked node) and downstream exposure
  (a node *buys from* the shocked node) are different transmission directions; label each edge so a
  shock can be pushed the correct way through `B`.
- **General block form.** For G regions and N sectors, `A` and `B` are GN×GN block matrices and `V`,
  `VB` are G×GN — the same identity scales to the full multi-region, multi-sector web.

## Inputs
A `CausalChain` with a structurally-transmitted driver, the shock node (region-sector being hit), the
region-sector universe, an ICIO table (or coefficient matrix `A`) and a final-demand vector `y`, plus
method memory. No case pages.

## Outputs
`GlobalIONetwork`: `region_sector_nodes`, value-added `edges` (directed, source→destination), the
`leontief_inverse` B (propagation operator), `upstream_downstream_exposure` per node, a
`propagated_shock_map` (which nodes absorb the shock and how strongly), and an explicit
`unlisted_supplier_exposure` list (deep tiers surfaced by B that a tradeable-name screen would miss).

## Required fields
Every node is a (region, sector) pair; every edge is a directed value-added flow with a source; the
Leontief inverse (or an equivalent total-requirement propagation rule) is present; double-counted
intermediate flows are explicitly excluded from exposures; ≥1 falsifier for the propagation claim (an
observable that, if absent, would void the structural link).

## Validation rules
- A node that names a single tradeable instrument instead of a region-sector cell is rejected
  (`node_must_be_region_sector`).
- An edge weighted by gross trade rather than value-added flow is rejected; decompose first
  (`edge_must_be_value_added_flow`).
- A shock propagated only to first-degree neighbours (no Leontief inverse / total-requirement step) is
  incomplete — indirect upstream tiers must be included (`shock_requires_leontief_propagation`).
- Pure double-counted terms (value crossing a border twice) are not exposures and must be netted out
  (`double_counted_flow_not_an_exposure`).
- The value-added share columns must sum to one (conservation check on `VB`); a violation means the
  coefficient matrix or final-demand split is malformed.

## Failure / blocked states
- No ICIO table / coefficient matrix available and none constructible → `blocked: no_io_structure`
  (cannot propagate; downgrade the driver to a non-structural channel).
- Driver's transmission is not supply-chain structural → `not_applicable` (use the plain System Mapper
  instead of an IO network).
- Gross-flow data only, no way to strip double counting → `degraded: gross_proxy_only` (flag exposures
  as upper bounds, do not treat as value-added exposure).

## Example input
CausalChain driver: "a tariff / export block on advanced-node semiconductors produced in region R,
sector S". Shock node: (R, S). Universe: a multi-region, multi-sector ICIO table covering electronics,
capital goods, autos, and downstream assembly across regions.

## Example output
- nodes: {(R, semiconductors), (region A, capital equipment), (region B, auto electronics),
  (region C, contract assembly), …} — region-sector cells, several of them with no single listed proxy.
- edges: directed value-added flows, e.g. (R, semis) → (region C, assembly) → (region D, final goods),
  each carrying source value added, double-counting removed.
- leontief_inverse B: total-requirement operator; applying the shock vector through B shows that
  (region A, capital equipment) — an *upstream* supplier two tiers back — absorbs material impairment,
  and several unlisted assembly suppliers in region C appear in `unlisted_supplier_exposure`.
- propagated_shock_map: ranked region-sector nodes by value-added exposure to the (R, S) shock;
  candidate operational-axis node = the most-exposed unlisted-supplier-heavy cell.
- falsifier: if the (R, S) value added embedded in region-C assembly is near zero once double-counting
  is netted out, the structural transmission claim is void.

## Non-goals
No pricing, no scenario probabilities, no sizing, no instrument legs, no hedge ratios, no execution.
This builds the structural network and propagates a shock through it — it does not value or trade the
exposure. It stops at "which nodes are exposed, and through which value-added paths".
