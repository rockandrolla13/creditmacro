-- G6 / D5 — the provenance ledger: an append-only citation graph tying every emitted
-- claim to the source span it rests on. A SEPARATE database file from the Thesis
-- Tracker and from the Theme Hypothesis Ledger (engine/ledger/), per D5.
--
-- Why this lives in db/migrations/provenance/ and not db/migrations/ alongside 0001
-- and 0002, despite the plan naming the latter: ThesisTrackerDB.migrate() applies
-- `MIGRATIONS_DIR.glob("*.sql")` — a NON-recursive glob over db/migrations. A file
-- placed there would be applied to the thesis tracker's database too, putting
-- provenance tables inside the very store D5 says to keep separate. The subdirectory
-- is the whole fix: same numbering, same pattern, no cross-contamination.
--
-- Append-only is enforced here, not merely promised. The triggers below abort any
-- UPDATE or DELETE, so the guarantee survives a caller that bypasses the service layer.
--
-- No wall clock: created_at has NO DEFAULT. The caller supplies the instant (I8), so a
-- replayed run produces a byte-identical ledger.

CREATE TABLE IF NOT EXISTS provenance_nodes (
    id               TEXT PRIMARY KEY,
    kind             TEXT NOT NULL,
    source_slug      TEXT,
    span_char_start  INTEGER,
    span_char_end    INTEGER,
    verdict          TEXT,            -- JSON GroundingVerdict; set on source_span nodes
    created_at       TEXT NOT NULL,   -- caller-supplied ISO-8601
    note             TEXT NOT NULL DEFAULT '',
    CHECK (kind IN ('source_span', 'atom', 'causal_claim', 'axis',
                    'scenario_evidence', 'strategy_family', 'synthesis'))
);

-- Edges are a separate table rather than a JSON column so "every claim resting on this
-- source" is one join, which is the query D5 exists to make possible.
CREATE TABLE IF NOT EXISTS provenance_edges (
    child_id   TEXT NOT NULL REFERENCES provenance_nodes (id),
    parent_id  TEXT NOT NULL REFERENCES provenance_nodes (id),
    ordinal    INTEGER NOT NULL,      -- preserves the author's parent order
    PRIMARY KEY (child_id, parent_id)
);

CREATE INDEX IF NOT EXISTS ix_provenance_edges_parent ON provenance_edges (parent_id);
CREATE INDEX IF NOT EXISTS ix_provenance_nodes_source ON provenance_nodes (source_slug);

CREATE TRIGGER IF NOT EXISTS provenance_nodes_no_update
BEFORE UPDATE ON provenance_nodes
BEGIN
    SELECT RAISE(ABORT, 'provenance ledger is append-only: nodes cannot be updated');
END;

CREATE TRIGGER IF NOT EXISTS provenance_nodes_no_delete
BEFORE DELETE ON provenance_nodes
BEGIN
    SELECT RAISE(ABORT, 'provenance ledger is append-only: nodes cannot be deleted');
END;

CREATE TRIGGER IF NOT EXISTS provenance_edges_no_update
BEFORE UPDATE ON provenance_edges
BEGIN
    SELECT RAISE(ABORT, 'provenance ledger is append-only: edges cannot be updated');
END;

CREATE TRIGGER IF NOT EXISTS provenance_edges_no_delete
BEFORE DELETE ON provenance_edges
BEGIN
    SELECT RAISE(ABORT, 'provenance ledger is append-only: edges cannot be deleted');
END;
