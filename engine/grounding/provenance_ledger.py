"""G6 store — the append-only provenance ledger, behind a protocol.

Two implementations, one contract:

* `InMemoryProvenanceLedger` — a dict. What tests and a single run use.
* `SqliteProvenanceLedger`   — a real database file (D5), mirroring the
  `thesis_tracker.py` + `db/migrations` pattern, with append-only enforced by SQL
  triggers as well as by this module.

**The protocol is load-bearing, not decoration.** `docs/SPEC_AND_STATE.md` §4.3 records
an OPEN tension: D5 puts provenance in its own SQLite file on the grounds that joining
two in-flight systems is how both stall, while D1 routes the harness's human review gate
into `engine/ledger/wiki/review_queue.py` — a module inside that same in-flight
substrate, currently a stub with zero callers. Resolving that is a decision for the
user, not for this module. So `ProvenanceLedger` is a `Protocol`: everything downstream
(notably `emit_gate`) depends on the four methods below and on nothing else, which means
a later decision to fold provenance into the hypothesis ledger's event-sourced substrate
is a new class here and no change anywhere else.

Assumed meanwhile, and reversible: **D5 as written** — a separate SQLite file, separate
migration directory, no import edge into `engine/ledger/`. That preserves the property
§4.3 flags as worth preserving: `engine/ledger/` still has exactly one outward import
and nothing importing inward.

**Append-only, and why it needs no cycle check.** A node's parents must ALREADY exist
when it is appended. You cannot cite what has not been recorded, so the graph is a DAG
by construction. The alternative — accepting forward references and detecting cycles
later — buys nothing and loses the guarantee that every node was grounded at the moment
it was written.

No wall clock (I8): `created_at` arrives on the node.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable, Optional, Protocol, Union, runtime_checkable

from engine.schema.grounding import GroundingVerdict
from engine.schema.provenance import LedgerNode

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MIGRATIONS_DIR = _REPO_ROOT / "db" / "migrations" / "provenance"
DEFAULT_DB_PATH = _REPO_ROOT / "data" / "provenance_ledger.sqlite"


class LedgerAppendError(RuntimeError):
    """Base for every refusal to append. Append-only means a rejected write is a hard
    error, never a silent no-op — a provenance store that quietly drops a node is worse
    than none, because it looks complete."""


class DuplicateNodeError(LedgerAppendError):
    """A node id was appended twice. Ids are the citation handles; reusing one would
    silently re-point every claim that cites it."""


class UnknownParentError(LedgerAppendError):
    """A node cited a parent that does not exist yet. See the module docstring: this is
    the rule that makes the graph acyclic."""


@runtime_checkable
class ProvenanceLedger(Protocol):
    """The four operations the rest of G6 is allowed to depend on."""

    def append(self, node: LedgerNode) -> LedgerNode:
        """Record a node. Raises `LedgerAppendError` if it cannot be recorded."""
        ...

    def get(self, node_id: str) -> Optional[LedgerNode]:
        """One node, or `None` if it was never recorded."""
        ...

    def nodes(self) -> list[LedgerNode]:
        """Every node, in append order."""
        ...

    def children_of(self, node_id: str) -> list[LedgerNode]:
        """Nodes that cite `node_id` — the "what rests on this source" direction."""
        ...


def _check_appendable(node: LedgerNode, known_ids: set[str]) -> None:
    if node.id in known_ids:
        raise DuplicateNodeError(f"node {node.id!r} is already in the ledger")
    missing = [p for p in node.parents if p not in known_ids]
    if missing:
        raise UnknownParentError(
            f"node {node.id!r} cites unrecorded parent(s) {missing}; "
            "a node may only rest on something already written down"
        )


class InMemoryProvenanceLedger:
    """Dict-backed ledger. Same guarantees as the SQLite one, no file."""

    def __init__(self) -> None:
        self._nodes: dict[str, LedgerNode] = {}
        self._children: dict[str, list[str]] = {}

    def append(self, node: LedgerNode) -> LedgerNode:
        _check_appendable(node, set(self._nodes))
        self._nodes[node.id] = node
        for parent in node.parents:
            self._children.setdefault(parent, []).append(node.id)
        return node

    def extend(self, nodes: Iterable[LedgerNode]) -> None:
        """Append many, in order. Stops at the first refusal — a partially written
        graph with a hole in it is exactly what the emit gate cannot reason about."""
        for node in nodes:
            self.append(node)

    def get(self, node_id: str) -> Optional[LedgerNode]:
        return self._nodes.get(node_id)

    def nodes(self) -> list[LedgerNode]:
        return list(self._nodes.values())

    def children_of(self, node_id: str) -> list[LedgerNode]:
        return [self._nodes[c] for c in self._children.get(node_id, ())]


class SqliteProvenanceLedger:
    """Append-only SQLite ledger (D5). Use as a context manager.

    Deliberately parallel to `engine/thesis_tracker.py::ThesisTrackerDB` — same
    migration-table pattern, same `Path` handling, same `PRAGMA foreign_keys` — because
    a second persistence idiom in one repo is a thing every future reader has to learn
    twice. It reads a DIFFERENT migrations directory, which is what keeps the two stores
    from leaking schemas into each other.
    """

    def __init__(self, path: Union[str, Path] = DEFAULT_DB_PATH) -> None:
        self.path = Path(path)
        if str(self.path) != ":memory:":
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON;")

    def __enter__(self) -> "SqliteProvenanceLedger":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def close(self) -> None:
        self.conn.close()

    def migrate(self) -> None:
        """Apply every provenance migration not yet recorded, in filename order."""
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS provenance_migrations "
            "(filename TEXT PRIMARY KEY)"
        )
        applied = {
            r["filename"]
            for r in self.conn.execute("SELECT filename FROM provenance_migrations")
        }
        for sql_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
            if sql_file.name in applied:
                continue
            self.conn.executescript(sql_file.read_text())
            self.conn.execute(
                "INSERT INTO provenance_migrations (filename) VALUES (?)",
                (sql_file.name,),
            )
        self.conn.commit()

    def applied_migrations(self) -> list[str]:
        return [
            r["filename"]
            for r in self.conn.execute(
                "SELECT filename FROM provenance_migrations ORDER BY filename"
            )
        ]

    # ── the protocol ─────────────────────────────────────────────────────────
    def append(self, node: LedgerNode) -> LedgerNode:
        _check_appendable(node, self._known_ids())
        self.conn.execute(
            "INSERT INTO provenance_nodes "
            "(id, kind, source_slug, span_char_start, span_char_end, verdict, "
            " created_at, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                node.id,
                node.kind,
                node.source_slug,
                node.span_char_start,
                node.span_char_end,
                node.verdict.model_dump_json() if node.verdict else None,
                node.created_at,
                node.note,
            ),
        )
        self.conn.executemany(
            "INSERT INTO provenance_edges (child_id, parent_id, ordinal) VALUES (?, ?, ?)",
            [(node.id, parent, i) for i, parent in enumerate(node.parents)],
        )
        self.conn.commit()
        return node

    def get(self, node_id: str) -> Optional[LedgerNode]:
        row = self.conn.execute(
            "SELECT * FROM provenance_nodes WHERE id = ?", (node_id,)
        ).fetchone()
        return self._to_node(row) if row else None

    def nodes(self) -> list[LedgerNode]:
        return [
            self._to_node(r)
            for r in self.conn.execute("SELECT * FROM provenance_nodes ORDER BY rowid")
        ]

    def children_of(self, node_id: str) -> list[LedgerNode]:
        rows = self.conn.execute(
            "SELECT n.* FROM provenance_nodes n "
            "JOIN provenance_edges e ON e.child_id = n.id "
            "WHERE e.parent_id = ? ORDER BY n.rowid",
            (node_id,),
        )
        return [self._to_node(r) for r in rows]

    # ── internals ────────────────────────────────────────────────────────────
    def _known_ids(self) -> set[str]:
        return {r["id"] for r in self.conn.execute("SELECT id FROM provenance_nodes")}

    def _parents_of(self, node_id: str) -> tuple[str, ...]:
        return tuple(
            r["parent_id"]
            for r in self.conn.execute(
                "SELECT parent_id FROM provenance_edges WHERE child_id = ? "
                "ORDER BY ordinal",
                (node_id,),
            )
        )

    def _to_node(self, row: sqlite3.Row) -> LedgerNode:
        return LedgerNode(
            id=row["id"],
            kind=row["kind"],
            parents=self._parents_of(row["id"]),
            source_slug=row["source_slug"],
            span_char_start=row["span_char_start"],
            span_char_end=row["span_char_end"],
            verdict=(
                GroundingVerdict.model_validate(json.loads(row["verdict"]))
                if row["verdict"]
                else None
            ),
            created_at=row["created_at"],
            note=row["note"],
        )


__all__ = [
    "DEFAULT_DB_PATH",
    "DuplicateNodeError",
    "InMemoryProvenanceLedger",
    "LedgerAppendError",
    "ProvenanceLedger",
    "SqliteProvenanceLedger",
    "UnknownParentError",
]
