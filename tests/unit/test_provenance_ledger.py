"""G6 store — append-only, DAG by construction, and the same contract in both backends.

Every behavioural test runs against BOTH implementations. That is the point of the
protocol: if the D1/D5 tension (`docs/SPEC_AND_STATE.md` §4.3) is later resolved the
other way, a third implementation has to pass this same file.
"""
from __future__ import annotations

import sqlite3

import pytest

from engine.grounding.provenance_ledger import (
    DuplicateNodeError,
    InMemoryProvenanceLedger,
    ProvenanceLedger,
    SqliteProvenanceLedger,
    UnknownParentError,
)
from engine.schema.grounding import GroundingVerdict
from engine.schema.provenance import LedgerNode

NOW = "2026-08-12T00:00:00+00:00"        # supplied, never read from a clock (I8)

GROUNDED = GroundingVerdict(status="grounded", method="exact", span_found=True,
                            numbers_verified=True, reason="span located")
UNGROUNDED = GroundingVerdict(status="ungrounded", method="none", span_found=False,
                              numbers_verified=False, reason="quote not found in source")


def span(node_id: str, verdict: GroundingVerdict = GROUNDED) -> LedgerNode:
    return LedgerNode(id=node_id, kind="source_span", source_slug="jpm_ai_capex_001",
                      span_char_start=10, span_char_end=60, verdict=verdict,
                      created_at=NOW)


def claim(node_id: str, *parents: str, kind: str = "atom") -> LedgerNode:
    return LedgerNode(id=node_id, kind=kind, parents=tuple(parents), created_at=NOW)


@pytest.fixture(params=["memory", "sqlite"])
def ledger(request, tmp_path) -> ProvenanceLedger:
    if request.param == "memory":
        return InMemoryProvenanceLedger()
    store = SqliteProvenanceLedger(tmp_path / "provenance.sqlite")
    store.migrate()
    request.addfinalizer(store.close)
    return store


# ── the contract, both backends ──────────────────────────────────────────────

def test_both_backends_satisfy_the_protocol(ledger):
    assert isinstance(ledger, ProvenanceLedger)


def test_a_node_round_trips_with_its_verdict_and_parents(ledger):
    ledger.append(span("s1"))
    ledger.append(claim("a1", "s1"))

    stored = ledger.get("a1")
    assert stored.parents == ("s1",)
    assert ledger.get("s1").verdict == GROUNDED
    assert ledger.get("s1").is_grounded_root is True


def test_parent_order_is_preserved(ledger):
    ledger.append(span("s1"))
    ledger.append(span("s2"))
    ledger.append(span("s3"))
    ledger.append(claim("a1", "s3", "s1", "s2"))
    assert ledger.get("a1").parents == ("s3", "s1", "s2")


def test_nodes_come_back_in_append_order(ledger):
    ledger.append(span("s1"))
    ledger.append(claim("a1", "s1"))
    ledger.append(claim("c1", "a1", kind="causal_claim"))
    assert [n.id for n in ledger.nodes()] == ["s1", "a1", "c1"]


def test_children_of_answers_what_rests_on_this_source(ledger):
    """D5's stated goal: 'show me every claim that rests on this source.'"""
    ledger.append(span("s1"))
    ledger.append(claim("a1", "s1"))
    ledger.append(claim("a2", "s1"))
    ledger.append(claim("c1", "a1", kind="causal_claim"))

    assert {n.id for n in ledger.children_of("s1")} == {"a1", "a2"}
    assert [n.id for n in ledger.children_of("a1")] == ["c1"]
    assert ledger.children_of("c1") == []


def test_an_unrecorded_id_reads_as_absent_not_as_an_error(ledger):
    assert ledger.get("never-written") is None


# ── append-only ──────────────────────────────────────────────────────────────

def test_a_duplicate_id_is_refused(ledger):
    ledger.append(span("s1"))
    with pytest.raises(DuplicateNodeError):
        ledger.append(claim("s1", kind="atom"))


def test_a_forward_reference_is_refused_which_is_what_makes_it_a_dag(ledger):
    with pytest.raises(UnknownParentError):
        ledger.append(claim("a1", "s_does_not_exist_yet"))
    assert ledger.get("a1") is None          # a refused append writes nothing


def test_a_cycle_cannot_be_constructed(ledger):
    ledger.append(span("s1"))
    ledger.append(claim("a1", "s1"))
    with pytest.raises(UnknownParentError):
        ledger.append(claim("a2", "a1", "a3"))     # a3 would have to cite a2 back


def test_extend_stops_at_the_first_refusal_rather_than_leaving_a_hole():
    store = InMemoryProvenanceLedger()
    with pytest.raises(UnknownParentError):
        store.extend([span("s1"), claim("a1", "missing"), claim("a2", "s1")])
    assert [n.id for n in store.nodes()] == ["s1"]


# ── the schema refuses incoherent nodes ──────────────────────────────────────

def test_a_source_span_must_carry_its_verdict_and_source():
    with pytest.raises(ValueError):
        LedgerNode(id="s1", kind="source_span", source_slug="x", created_at=NOW)
    with pytest.raises(ValueError):
        LedgerNode(id="s1", kind="source_span", verdict=GROUNDED, created_at=NOW)


def test_a_source_span_is_a_root():
    with pytest.raises(ValueError):
        LedgerNode(id="s2", kind="source_span", source_slug="x", verdict=GROUNDED,
                   parents=("s1",), created_at=NOW)


def test_a_derived_claim_may_not_assert_its_own_verdict():
    """Grounding descends; it is not something a claim can stamp on itself."""
    with pytest.raises(ValueError):
        LedgerNode(id="a1", kind="atom", parents=("s1",), verdict=GROUNDED, created_at=NOW)


def test_an_ungrounded_span_is_recorded_not_discarded(ledger):
    ledger.append(span("s_bad", UNGROUNDED))
    assert ledger.get("s_bad").verdict.status == "ungrounded"
    assert ledger.get("s_bad").is_grounded_root is False


def test_a_node_is_frozen():
    node = span("s1")
    with pytest.raises(Exception):
        node.note = "edited after the fact"


# ── SQLite specifics: D5 says a real, separate database ──────────────────────

def test_the_sqlite_store_is_a_real_file_with_its_own_migration(tmp_path):
    path = tmp_path / "nested" / "provenance.sqlite"
    with SqliteProvenanceLedger(path) as store:
        store.migrate()
        assert store.applied_migrations() == ["0003_provenance_ledger.sql"]
    assert path.exists()


def test_migration_is_idempotent(tmp_path):
    with SqliteProvenanceLedger(tmp_path / "p.sqlite") as store:
        store.migrate()
        store.migrate()
        assert store.applied_migrations() == ["0003_provenance_ledger.sql"]


def test_the_provenance_migration_is_not_in_the_thesis_tracker_migration_directory():
    """D5 keeps the two stores separate. `ThesisTrackerDB.migrate` globs
    `db/migrations/*.sql` non-recursively, so a sibling file there would land the
    provenance schema inside the thesis tracker's own database."""
    from engine.thesis_tracker import MIGRATIONS_DIR as THESIS_DIR
    from engine.grounding.provenance_ledger import MIGRATIONS_DIR as PROV_DIR

    assert PROV_DIR != THESIS_DIR
    assert "0003_provenance_ledger.sql" not in {p.name for p in THESIS_DIR.glob("*.sql")}


def test_sql_triggers_enforce_append_only_even_behind_the_service_layer(tmp_path):
    with SqliteProvenanceLedger(tmp_path / "p.sqlite") as store:
        store.migrate()
        store.append(span("s1"))
        with pytest.raises(sqlite3.IntegrityError, match="append-only"):
            store.conn.execute("UPDATE provenance_nodes SET note = 'x' WHERE id = 's1'")
        with pytest.raises(sqlite3.IntegrityError, match="append-only"):
            store.conn.execute("DELETE FROM provenance_nodes WHERE id = 's1'")


def test_created_at_has_no_sql_default_so_the_store_never_reads_the_clock(tmp_path):
    with SqliteProvenanceLedger(tmp_path / "p.sqlite") as store:
        store.migrate()
        with pytest.raises(sqlite3.IntegrityError):
            store.conn.execute(
                "INSERT INTO provenance_nodes (id, kind) VALUES ('x', 'atom')"
            )


def test_the_ledger_survives_a_reopen(tmp_path):
    path = tmp_path / "p.sqlite"
    with SqliteProvenanceLedger(path) as store:
        store.migrate()
        store.append(span("s1"))
        store.append(claim("a1", "s1"))
    with SqliteProvenanceLedger(path) as reopened:
        reopened.migrate()
        assert reopened.get("a1").parents == ("s1",)
        with pytest.raises(DuplicateNodeError):
            reopened.append(span("s1"))
