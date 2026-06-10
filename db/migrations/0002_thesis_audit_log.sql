-- Append-only audit trail for the Thesis Tracker. Every create / update / close /
-- delete writes one row here BEFORE/AFTER the change so no mutation is silent — a
-- delete in particular stores the full pre-delete snapshot, making it recoverable.

CREATE TABLE IF NOT EXISTS thesis_audit_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    ts         TEXT NOT NULL DEFAULT (datetime('now')),
    action     TEXT NOT NULL,   -- create | update | close | delete
    ticker     TEXT NOT NULL,
    thesis_id  TEXT,
    reason     TEXT,
    snapshot   TEXT,            -- JSON row state (post-change; pre-delete for deletes)
    CHECK (action IN ('create', 'update', 'close', 'delete'))
);

CREATE INDEX IF NOT EXISTS ix_thesis_audit_ticker ON thesis_audit_log (ticker, id);
