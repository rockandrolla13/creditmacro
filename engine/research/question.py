"""ResearchQuestion and SubQuestion per V4 spec sections 7, 8.1 through 8.4.

A ResearchQuestion is the exact canonical question confirmed after Gate 1;
it is NOT yet an experiment and does NOT immediately create hypotheses.

Modelled as a frozen pydantic structure with decision relevance, scope, primary target,
material assumptions, originating intake/gate reference, and status.

SubQuestion models subquestions with spec 8.3 fields: subquestion_id, research_question_id,
question, role, dependencies, current_state.

QuestionDecomposition holds a ResearchQuestion's subquestions plus dependency edge set,
exposing topological order, cycle detection, upstream/downstream relationships,
intermediate mechanisms, and endpoint decision-answering subquestions (Spec 8.4).

Call no wall clock (invariant I8).
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


# ── Spec 7 & 8 Vocabularies ────────────────────────────────────────────────────

class ResearchQuestionStatus(str, Enum):
    """Vocabulary for ResearchQuestion status (Spec 7)."""

    DRAFT = "draft"
    CONFIRMED = "confirmed"
    ACTIVE = "active"
    RESOLVED = "resolved"
    ARCHIVED = "archived"
    REJECTED = "rejected"


class SubQuestionRole(str, Enum):
    """Exact role vocabulary per Spec 8.3."""

    NECESSARY_CONDITION = "necessary_condition"
    MECHANISM = "mechanism"
    INTERMEDIATE_OUTCOME = "intermediate_outcome"
    ENDPOINT = "endpoint"
    BOUNDARY_CONDITION = "boundary_condition"
    ROBUSTNESS = "robustness"


class SubQuestionState(str, Enum):
    """Exact current_state vocabulary per Spec 8.3."""

    UNKNOWN = "unknown"
    PARTIALLY_KNOWN = "partially_known"
    SUPPORTED = "supported"
    CONTESTED = "contested"
    REFUTED = "refuted"
    BLOCKED = "blocked"


# Aliases for convenience
SubQuestionCurrentState = SubQuestionState
Role = SubQuestionRole


class DependencyCycleError(ValueError):
    """Raised when subquestion dependencies form a directed cycle."""

    pass


# ── Spec 7: ResearchQuestion ──────────────────────────────────────────────────

class ResearchQuestion(BaseModel):
    """The exact canonical question confirmed after Gate 1 (Spec 7).

    A ResearchQuestion is NOT yet an experiment and does NOT immediately create hypotheses.
    Modelled frozen with decision relevance, scope, primary target, material assumptions,
    originating intake/gate reference, and status.
    """

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    research_question_id: str
    question: str
    decision_relevance: str
    scope: str
    primary_target: str
    material_assumptions: Tuple[str, ...] = ()
    originating_intake_ref: str = Field(
        default="",
        description="Originating intake or gate reference confirmed after Gate 1",
    )
    status: ResearchQuestionStatus = ResearchQuestionStatus.CONFIRMED

    @model_validator(mode="before")
    @classmethod
    def _coerce_originating_ref(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "originating_intake_ref" not in data or not data["originating_intake_ref"]:
                for alt_key in (
                    "originating_gate_ref",
                    "originating_intake_gate_ref",
                    "originating_ref",
                    "gate_ref",
                    "intake_ref",
                ):
                    if alt_key in data and data[alt_key]:
                        data["originating_intake_ref"] = str(data[alt_key])
                        break
        return data

    @field_validator("material_assumptions", mode="before")
    @classmethod
    def _coerce_material_assumptions(cls, v: Any) -> Tuple[str, ...]:
        if v is None:
            return ()
        if isinstance(v, str):
            return (v,) if v.strip() else ()
        if isinstance(v, (list, tuple, set)):
            return tuple(str(x).strip() for x in v if x and str(x).strip())
        return ()

    @property
    def originating_gate_ref(self) -> str:
        return self.originating_intake_ref

    @property
    def originating_intake_gate_ref(self) -> str:
        return self.originating_intake_ref


# ── Spec 8.3: SubQuestion ─────────────────────────────────────────────────────

class SubQuestion(BaseModel):
    """SubQuestion model per Spec 8.3.

    Fields: subquestion_id, research_question_id, question, role, dependencies, current_state.
    Role and current_state are strict str Enums.
    """

    model_config = ConfigDict(frozen=True)

    subquestion_id: str
    research_question_id: str
    question: str
    role: SubQuestionRole
    dependencies: Tuple[str, ...] = ()
    current_state: SubQuestionState = SubQuestionState.UNKNOWN

    @field_validator("dependencies", mode="before")
    @classmethod
    def _coerce_dependencies(cls, v: Any) -> Tuple[str, ...]:
        if v is None:
            return ()
        if isinstance(v, str):
            return (v,) if v.strip() else ()
        if isinstance(v, (list, tuple, set)):
            return tuple(str(x).strip() for x in v if x and str(x).strip())
        return ()


# ── Spec 8.3 & 8.4: QuestionDecomposition ────────────────────────────────────

class QuestionDecomposition(BaseModel):
    """Container holding a ResearchQuestion's subquestions plus dependency graph (Spec 8.3, 8.4).

    Provides topological ordering, cycle detection, upstream/downstream navigation,
    and exposure of logically upstream, intermediate mechanism, and endpoint subquestions.
    """

    model_config = ConfigDict(frozen=True)

    research_question: Optional[ResearchQuestion] = None
    research_question_id: Optional[str] = None
    subquestions: Tuple[SubQuestion, ...] = ()
    dependency_edges: Tuple[Tuple[str, str], ...] = ()

    @field_validator("subquestions", mode="before")
    @classmethod
    def _coerce_subquestions(cls, v: Any) -> Tuple[SubQuestion, ...]:
        if v is None:
            return ()
        if isinstance(v, (list, tuple, set)):
            return tuple(v)
        return ()

    @field_validator("dependency_edges", mode="before")
    @classmethod
    def _coerce_dependency_edges(cls, v: Any) -> Tuple[Tuple[str, str], ...]:
        if v is None:
            return ()
        if isinstance(v, (list, tuple, set)):
            edges = []
            for item in v:
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    edges.append((str(item[0]), str(item[1])))
            return tuple(edges)
        return ()

    @model_validator(mode="after")
    def _populate_and_validate(self) -> QuestionDecomposition:
        # Auto-set research_question_id from research_question if not present
        if self.research_question is not None and self.research_question_id is None:
            object.__setattr__(
                self, "research_question_id", self.research_question.research_question_id
            )

        # Collect dependency edges from subquestion dependencies + explicit dependency_edges
        edges_set = set(self.dependency_edges)
        for sq in self.subquestions:
            for dep in sq.dependencies:
                # dep is upstream, sq.subquestion_id is downstream
                edges_set.add((dep, sq.subquestion_id))

        object.__setattr__(self, "dependency_edges", tuple(sorted(edges_set)))
        return self

    @property
    def by_id(self) -> Dict[str, SubQuestion]:
        """Map from subquestion_id to SubQuestion."""
        return {sq.subquestion_id: sq for sq in self.subquestions}

    def get_subquestion(self, subquestion_id: str) -> Optional[SubQuestion]:
        """Retrieve a SubQuestion by ID."""
        return self.by_id.get(subquestion_id)

    def get_subquestions_in_dependency_order(self) -> Tuple[SubQuestion, ...]:
        """Returns subquestions in topological/dependency order.

        RAISES DependencyCycleError (subclass of ValueError) if a cycle exists.
        """
        return tuple(self.topological_sort())

    def topological_sort(self) -> List[SubQuestion]:
        """Returns list of subquestions in topological dependency order.

        RAISES DependencyCycleError if dependencies contain a loop.
        """
        sq_map = self.by_id
        # All node IDs in graph (from subquestions and edges)
        node_ids: Set[str] = set(sq_map.keys())
        for u, v in self.dependency_edges:
            node_ids.add(u)
            node_ids.add(v)

        # Build in-degrees and adjacency list
        in_degree: Dict[str, int] = {nid: 0 for nid in node_ids}
        adj: Dict[str, List[str]] = {nid: [] for nid in node_ids}

        for u, v in self.dependency_edges:
            adj[u].append(v)
            in_degree[v] += 1

        # Zero in-degree queue (sorted by ID for deterministic ordering)
        zero_in = sorted([nid for nid in node_ids if in_degree[nid] == 0])

        order_ids: List[str] = []
        while zero_in:
            curr = zero_in.pop(0)
            order_ids.append(curr)
            for nxt in adj[curr]:
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    zero_in.append(nxt)
                    zero_in.sort()

        if len(order_ids) < len(node_ids):
            # Cycle detected
            unresolved = set(node_ids) - set(order_ids)
            raise DependencyCycleError(
                f"Dependency cycle detected in question decomposition involving nodes: {sorted(unresolved)}"
            )

        # Return SubQuestion objects present in this decomposition in topological order
        res: List[SubQuestion] = []
        for nid in order_ids:
            if nid in sq_map:
                res.append(sq_map[nid])
        return res

    @property
    def subquestions_in_dependency_order(self) -> Tuple[SubQuestion, ...]:
        """Property returning subquestions in topological dependency order."""
        return self.get_subquestions_in_dependency_order()

    # ── Spec 8.4: Upstream, Mechanism, and Endpoint query methods ─────────────

    def get_upstream_subquestions(self, subquestion_id: str) -> Tuple[SubQuestion, ...]:
        """Return all subquestions that are logically upstream (prerequisites) of subquestion_id."""
        sq_map = self.by_id
        if subquestion_id not in sq_map and subquestion_id not in {u for u, _ in self.dependency_edges}:
            return ()

        # Traverse backwards along dependency edges: (u, v) means u is upstream of v
        upstream_ids: Set[str] = set()
        stack = [subquestion_id]

        # Reverse adjacency list: v -> list of u
        rev_adj: Dict[str, List[str]] = {}
        for u, v in self.dependency_edges:
            rev_adj.setdefault(v, []).append(u)

        while stack:
            curr = stack.pop()
            for parent in rev_adj.get(curr, []):
                if parent not in upstream_ids:
                    upstream_ids.add(parent)
                    stack.append(parent)

        # Return in topological order
        all_ordered = self.get_subquestions_in_dependency_order()
        return tuple(sq for sq in all_ordered if sq.subquestion_id in upstream_ids)

    def get_downstream_subquestions(self, subquestion_id: str) -> Tuple[SubQuestion, ...]:
        """Return all subquestions that are logically downstream of subquestion_id."""
        sq_map = self.by_id
        downstream_ids: Set[str] = set()
        stack = [subquestion_id]

        fwd_adj: Dict[str, List[str]] = {}
        for u, v in self.dependency_edges:
            fwd_adj.setdefault(u, []).append(v)

        while stack:
            curr = stack.pop()
            for child in fwd_adj.get(curr, []):
                if child not in downstream_ids:
                    downstream_ids.add(child)
                    stack.append(child)

        all_ordered = self.get_subquestions_in_dependency_order()
        return tuple(sq for sq in all_ordered if sq.subquestion_id in downstream_ids)

    def is_upstream(self, candidate_upstream_id: str, subquestion_id: str) -> bool:
        """Check if candidate_upstream_id is logically upstream of subquestion_id."""
        upstream = self.get_upstream_subquestions(subquestion_id)
        return any(sq.subquestion_id == candidate_upstream_id for sq in upstream)

    def is_downstream(self, candidate_downstream_id: str, subquestion_id: str) -> bool:
        """Check if candidate_downstream_id is logically downstream of subquestion_id."""
        downstream = self.get_downstream_subquestions(subquestion_id)
        return any(sq.subquestion_id == candidate_downstream_id for sq in downstream)

    @property
    def logically_upstream_subquestions(self) -> Tuple[SubQuestion, ...]:
        """Return root subquestions (no upstream prerequisites) or those with prerequisite roles.

        Spec 8.4: expose subquestions that are logically upstream.
        """
        downstream_nodes = {v for _, v in self.dependency_edges}
        upstream_roles = {SubQuestionRole.NECESSARY_CONDITION, SubQuestionRole.BOUNDARY_CONDITION}

        return tuple(
            sq
            for sq in self.get_subquestions_in_dependency_order()
            if sq.subquestion_id not in downstream_nodes or sq.role in upstream_roles
        )

    def get_logically_upstream_subquestions(self) -> Tuple[SubQuestion, ...]:
        """Method alias for logically_upstream_subquestions."""
        return self.logically_upstream_subquestions

    @property
    def intermediate_mechanisms(self) -> Tuple[SubQuestion, ...]:
        """Return subquestions that represent intermediate mechanisms or intermediate outcomes.

        Spec 8.4: expose intermediate mechanisms.
        """
        mechanism_roles = {SubQuestionRole.MECHANISM, SubQuestionRole.INTERMEDIATE_OUTCOME}
        return tuple(sq for sq in self.subquestions if sq.role in mechanism_roles)

    def get_intermediate_mechanisms(self) -> Tuple[SubQuestion, ...]:
        """Method alias for intermediate_mechanisms."""
        return self.intermediate_mechanisms

    @property
    def endpoint_subquestions(self) -> Tuple[SubQuestion, ...]:
        """Return subquestions with role ENDPOINT that directly answer the decision.

        Spec 8.4: expose subquestions that directly answer the decision.
        """
        return tuple(sq for sq in self.subquestions if sq.role == SubQuestionRole.ENDPOINT)

    def get_endpoint_subquestions(self) -> Tuple[SubQuestion, ...]:
        """Method alias for endpoint_subquestions."""
        return self.endpoint_subquestions

    @property
    def direct_decision_subquestions(self) -> Tuple[SubQuestion, ...]:
        """Alias for endpoint subquestions that directly answer the decision."""
        return self.endpoint_subquestions

    def subquestions_by_role(self, role: SubQuestionRole | str) -> Tuple[SubQuestion, ...]:
        """Return all subquestions with the given role."""
        target_role = SubQuestionRole(role) if isinstance(role, str) else role
        return tuple(sq for sq in self.subquestions if sq.role == target_role)

    def subquestions_by_state(self, state: SubQuestionState | str) -> Tuple[SubQuestion, ...]:
        """Return all subquestions with the given current_state."""
        target_state = SubQuestionState(state) if isinstance(state, str) else state
        return tuple(sq for sq in self.subquestions if sq.current_state == target_state)
