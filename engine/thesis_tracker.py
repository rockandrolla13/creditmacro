"""Thesis Tracker — SQLite persistence + service layer.

A standalone sidecar over the discovery engine. It stores one human thesis row per
ticker, serves a computed read model (probability check / weighted price / upside),
and keeps an append-only audit log. It imports only the thesis_tracker pydantic
schema and the stdlib (+ optional PyYAML for ingestion); it does NOT touch the
discovery pipeline, the memory firewall, or expression sizing.

Two surfaces:
  * `ThesisTrackerDB`  — low-level store (connection, migrations, row mapping, view).
  * module functions   — the stateless service API (PART 4): open a db_path, perform
                         one operation with audit logging, close.

The computed view is defined in SQL (db/migrations/0001_thesis_tracker.sql) and its
arithmetic mirrors ComputedThesisTrackerRecord.from_record; unit tests assert they agree.

DISCIPLINE: nothing here ever infers a target price, a probability, a current price,
a weight, or a recommendation. Incomplete rows persist and are FLAGGED.
"""
from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import date
from pathlib import Path
from typing import Optional, Union

from engine.schema.thesis_tracker import (
    ComputedThesisTrackerRecord,
    MarketDataRecord,
    ThesisTrackerRecord,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
MIGRATIONS_DIR = _REPO_ROOT / "db" / "migrations"
DEFAULT_DB_PATH = _REPO_ROOT / "data" / "thesis_tracker.sqlite"

# Stored columns for thesis_tracker, in a single canonical order (DRY for upsert).
_THESIS_COLUMNS = (
    "thesis_id", "ticker", "weight_placeholder", "thesis",
    "bull_case_price", "base_case_price", "bear_case_price",
    "p_bull", "p_base", "p_bear",
    "next_catalyst", "catalyst_date", "kill_criteria", "status",
    "source_theme_id", "source_run_id", "source_evidence_ids", "notes",
)

# Audit actions written to thesis_audit_log.
AuditAction = str  # one of: create | update | close | delete


def _iso(d: Optional[date]) -> Optional[str]:
    return d.isoformat() if d is not None else None


def _parse_date(s) -> Optional[date]:
    return date.fromisoformat(s) if s else None


# ════════════════════════════════════════════════════════════════════════════
# Low-level store
# ════════════════════════════════════════════════════════════════════════════
class ThesisTrackerDB:
    """Thin repository over a SQLite file. Use as a context manager."""

    def __init__(self, path: Union[str, Path] = DEFAULT_DB_PATH) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON;")

    # ── lifecycle ────────────────────────────────────────────────────────────
    def __enter__(self) -> "ThesisTrackerDB":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def close(self) -> None:
        self.conn.close()

    # ── migrations ───────────────────────────────────────────────────────────
    def migrate(self) -> None:
        """Apply every db/migrations/*.sql not yet recorded, in filename order."""
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations "
            "(filename TEXT PRIMARY KEY, applied_at TEXT NOT NULL DEFAULT (datetime('now')))"
        )
        applied = {r["filename"] for r in self.conn.execute(
            "SELECT filename FROM schema_migrations"
        )}
        for sql_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
            if sql_file.name in applied:
                continue
            self.conn.executescript(sql_file.read_text())
            self.conn.execute(
                "INSERT INTO schema_migrations (filename) VALUES (?)", (sql_file.name,)
            )
        self.conn.commit()

    def applied_migrations(self) -> list[str]:
        return [r["filename"] for r in self.conn.execute(
            "SELECT filename FROM schema_migrations ORDER BY filename"
        )]

    # ── market data ──────────────────────────────────────────────────────────
    def upsert_market_data(self, rec: MarketDataRecord) -> None:
        self.conn.execute(
            "INSERT INTO market_data (ticker, current_price, as_of_date, source, notes) "
            "VALUES (?, ?, ?, ?, ?) "
            "ON CONFLICT(ticker) DO UPDATE SET "
            "current_price=excluded.current_price, as_of_date=excluded.as_of_date, "
            "source=excluded.source, notes=excluded.notes",
            (rec.ticker, rec.current_price, _iso(rec.as_of_date), rec.source, rec.notes),
        )
        self.conn.commit()

    def get_market_data(self, ticker: str) -> Optional[MarketDataRecord]:
        row = self.conn.execute(
            "SELECT * FROM market_data WHERE ticker = ?", (ticker.strip().upper(),)
        ).fetchone()
        if row is None:
            return None
        return MarketDataRecord(
            ticker=row["ticker"], current_price=row["current_price"],
            as_of_date=_parse_date(row["as_of_date"]), source=row["source"],
            notes=row["notes"],
        )

    # ── thesis rows ──────────────────────────────────────────────────────────
    def upsert_thesis(self, rec: ThesisTrackerRecord) -> str:
        """Insert or replace by ticker with the record's full field set. Assigns a
        thesis_id if absent; preserves the existing thesis_id on update. Returns the
        stored thesis_id. (Field-level MERGE lives in the service function.)"""
        thesis_id = rec.thesis_id or uuid.uuid4().hex
        values = {
            "thesis_id": thesis_id,
            "ticker": rec.ticker,
            "weight_placeholder": rec.weight_placeholder,
            "thesis": rec.thesis,
            "bull_case_price": rec.bull_case_price,
            "base_case_price": rec.base_case_price,
            "bear_case_price": rec.bear_case_price,
            "p_bull": rec.p_bull,
            "p_base": rec.p_base,
            "p_bear": rec.p_bear,
            "next_catalyst": rec.next_catalyst,
            "catalyst_date": _iso(rec.catalyst_date),
            "kill_criteria": rec.kill_criteria,
            "status": rec.status,
            "source_theme_id": rec.source_theme_id,
            "source_run_id": rec.source_run_id,
            "source_evidence_ids": json.dumps(rec.source_evidence_ids),
            "notes": rec.notes,
        }
        placeholders = ", ".join("?" for _ in _THESIS_COLUMNS)
        updates = ", ".join(
            f"{c}=excluded.{c}" for c in _THESIS_COLUMNS
            if c not in ("ticker", "thesis_id")
        )
        self.conn.execute(
            f"INSERT INTO thesis_tracker ({', '.join(_THESIS_COLUMNS)}) "
            f"VALUES ({placeholders}) "
            f"ON CONFLICT(ticker) DO UPDATE SET {updates}",
            tuple(values[c] for c in _THESIS_COLUMNS),
        )
        self.conn.commit()
        stored = self.conn.execute(
            "SELECT thesis_id FROM thesis_tracker WHERE ticker = ?", (rec.ticker,)
        ).fetchone()
        return stored["thesis_id"]

    def get_thesis(self, ticker: str) -> Optional[ThesisTrackerRecord]:
        row = self.conn.execute(
            "SELECT * FROM thesis_tracker WHERE ticker = ?", (ticker.strip().upper(),)
        ).fetchone()
        return self._row_to_thesis(row) if row else None

    def list_thesis(self) -> list[ThesisTrackerRecord]:
        rows = self.conn.execute(
            "SELECT * FROM thesis_tracker ORDER BY ticker"
        ).fetchall()
        return [self._row_to_thesis(r) for r in rows]

    def set_status(self, ticker: str, status: str) -> None:
        self.conn.execute(
            "UPDATE thesis_tracker SET status = ? WHERE ticker = ?",
            (status, ticker.strip().upper()),
        )
        self.conn.commit()

    def delete_row(self, ticker: str) -> None:
        self.conn.execute(
            "DELETE FROM thesis_tracker WHERE ticker = ?", (ticker.strip().upper(),)
        )
        self.conn.commit()

    # ── computed view ────────────────────────────────────────────────────────
    def get_computed(self, ticker: str) -> Optional[ComputedThesisTrackerRecord]:
        row = self.conn.execute(
            "SELECT * FROM thesis_tracker_view WHERE ticker = ?",
            (ticker.strip().upper(),),
        ).fetchone()
        return self._row_to_computed(row) if row else None

    def list_computed(self, status: Optional[str] = None) -> list[ComputedThesisTrackerRecord]:
        if status is None:
            rows = self.conn.execute(
                "SELECT * FROM thesis_tracker_view ORDER BY ticker"
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM thesis_tracker_view WHERE status = ? ORDER BY ticker",
                (status,),
            ).fetchall()
        return [self._row_to_computed(r) for r in rows]

    # ── audit log ────────────────────────────────────────────────────────────
    def append_audit(
        self, action: AuditAction, ticker: str, thesis_id: Optional[str],
        reason: Optional[str], snapshot: Optional[dict],
    ) -> None:
        self.conn.execute(
            "INSERT INTO thesis_audit_log (action, ticker, thesis_id, reason, snapshot) "
            "VALUES (?, ?, ?, ?, ?)",
            (action, ticker.strip().upper(), thesis_id, reason,
             json.dumps(snapshot, default=str) if snapshot is not None else None),
        )
        self.conn.commit()

    def read_audit(self, ticker: Optional[str] = None) -> list[dict]:
        if ticker is None:
            rows = self.conn.execute(
                "SELECT * FROM thesis_audit_log ORDER BY id"
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM thesis_audit_log WHERE ticker = ? ORDER BY id",
                (ticker.strip().upper(),),
            ).fetchall()
        return [dict(r) for r in rows]

    # ── row -> model ─────────────────────────────────────────────────────────
    @staticmethod
    def _base_fields(row: sqlite3.Row) -> dict:
        return dict(
            thesis_id=row["thesis_id"],
            ticker=row["ticker"],
            weight_placeholder=row["weight_placeholder"],
            thesis=row["thesis"],
            bull_case_price=row["bull_case_price"],
            base_case_price=row["base_case_price"],
            bear_case_price=row["bear_case_price"],
            p_bull=row["p_bull"],
            p_base=row["p_base"],
            p_bear=row["p_bear"],
            next_catalyst=row["next_catalyst"],
            catalyst_date=_parse_date(row["catalyst_date"]),
            kill_criteria=row["kill_criteria"],
            status=row["status"],
            source_theme_id=row["source_theme_id"],
            source_run_id=row["source_run_id"],
            source_evidence_ids=json.loads(row["source_evidence_ids"] or "[]"),
            notes=row["notes"],
        )

    def _row_to_thesis(self, row: sqlite3.Row) -> ThesisTrackerRecord:
        return ThesisTrackerRecord(**self._base_fields(row))

    def _row_to_computed(self, row: sqlite3.Row) -> ComputedThesisTrackerRecord:
        return ComputedThesisTrackerRecord(
            **self._base_fields(row),
            current_price=row["current_price"],
            probability_sum=row["probability_sum"],
            probability_check=row["probability_check"],
            probability_weighted_price=row["probability_weighted_price"],
            upside_to_current=row["upside_to_current"],
        )


# ════════════════════════════════════════════════════════════════════════════
# Service API (PART 4) — stateless functions over a db_path, with audit logging
# ════════════════════════════════════════════════════════════════════════════
def _open(db_path: Union[str, Path]) -> ThesisTrackerDB:
    """Open the store and ensure the schema exists (idempotent)."""
    db = ThesisTrackerDB(db_path)
    db.migrate()
    return db


def init_thesis_db(db_path: Union[str, Path]) -> None:
    """Create the database file and apply all migrations."""
    _open(db_path).close()


def apply_migrations(db_path: Union[str, Path]) -> None:
    """Apply any pending migrations (idempotent)."""
    _open(db_path).close()


def upsert_market_data(db_path: Union[str, Path], record: MarketDataRecord) -> None:
    db = _open(db_path)
    try:
        db.upsert_market_data(record)
    finally:
        db.close()


def upsert_thesis(
    db_path: Union[str, Path],
    record: ThesisTrackerRecord,
    reason: Optional[str] = None,
) -> str:
    """Insert (action='create') or field-MERGE update (action='update') a thesis row.

    Merge rule: only fields EXPLICITLY set on `record` (pydantic model_fields_set)
    overwrite the stored row; all other stored fields are preserved. Never infers.
    Appends to the audit log. Returns the stored thesis_id.
    """
    db = _open(db_path)
    try:
        existing = db.get_thesis(record.ticker)
        if existing is None:
            thesis_id = db.upsert_thesis(record)
            action = "create"
        else:
            merged = _merge_records(existing, record)
            thesis_id = db.upsert_thesis(merged)
            action = "update"
        snapshot = db.get_thesis(record.ticker)
        db.append_audit(
            action, record.ticker, thesis_id, reason,
            snapshot.model_dump() if snapshot else None,
        )
        return thesis_id
    finally:
        db.close()


def get_thesis(
    db_path: Union[str, Path], ticker: str
) -> Optional[ComputedThesisTrackerRecord]:
    db = _open(db_path)
    try:
        return db.get_computed(ticker)
    finally:
        db.close()


def list_theses(
    db_path: Union[str, Path], status: Optional[str] = None
) -> list[ComputedThesisTrackerRecord]:
    db = _open(db_path)
    try:
        return db.list_computed(status=status)
    finally:
        db.close()


def close_thesis(db_path: Union[str, Path], ticker: str, reason: str) -> None:
    """Mark a thesis closed (status='closed') and audit it. Never deletes."""
    db = _open(db_path)
    try:
        existing = db.get_thesis(ticker)
        if existing is None:
            raise KeyError(f"no thesis row for {ticker.strip().upper()}")
        db.set_status(ticker, "closed")
        snapshot = db.get_thesis(ticker)
        db.append_audit(
            "close", ticker, existing.thesis_id, reason,
            snapshot.model_dump() if snapshot else None,
        )
    finally:
        db.close()


def delete_thesis(db_path: Union[str, Path], ticker: str, reason: str) -> None:
    """Delete a thesis row — but NEVER silently: the pre-delete snapshot is written to
    the audit log first, so the deletion is always recoverable from the log."""
    db = _open(db_path)
    try:
        existing = db.get_thesis(ticker)
        if existing is None:
            raise KeyError(f"no thesis row for {ticker.strip().upper()}")
        db.append_audit(
            "delete", ticker, existing.thesis_id, reason, existing.model_dump()
        )
        db.delete_row(ticker)
    finally:
        db.close()


def export_thesis_tracker_json(db_path: Union[str, Path]) -> list[dict]:
    """All computed rows as JSON-serialisable dicts (dates -> ISO strings)."""
    db = _open(db_path)
    try:
        return [json.loads(r.model_dump_json()) for r in db.list_computed()]
    finally:
        db.close()


def export_thesis_tracker_markdown(db_path: Union[str, Path]) -> str:
    """All computed rows as a Markdown table (the human discovery summary view)."""
    db = _open(db_path)
    try:
        rows = db.list_computed()
    finally:
        db.close()

    header = (
        "| Ticker | Weight | Check | Weighted Px | Current | Upside | "
        "Next Catalyst | Catalyst Date | Status |"
    )
    sep = "|" + "|".join(["---"] * 9) + "|"

    def _num(x: Optional[float]) -> str:
        return "" if x is None else f"{x:.2f}"

    def _pct(x: Optional[float]) -> str:
        return "" if x is None else f"{x * 100:.1f}%"

    lines = [header, sep]
    for r in rows:
        lines.append(
            f"| {r.ticker} | {_num(r.weight_placeholder)} | {r.probability_check} | "
            f"{_num(r.probability_weighted_price)} | {_num(r.current_price)} | "
            f"{_pct(r.upside_to_current)} | {r.next_catalyst or ''} | "
            f"{r.catalyst_date or ''} | {r.status} |"
        )
    return "\n".join(lines) + "\n"


def _merge_records(
    existing: ThesisTrackerRecord, incoming: ThesisTrackerRecord
) -> ThesisTrackerRecord:
    """Overwrite only the fields explicitly provided on `incoming`; preserve the rest
    from `existing`. Keeps the existing thesis_id."""
    data = existing.model_dump()
    for field in incoming.model_fields_set:
        data[field] = getattr(incoming, field)
    data["thesis_id"] = existing.thesis_id
    data["ticker"] = existing.ticker
    return ThesisTrackerRecord(**data)


# ════════════════════════════════════════════════════════════════════════════
# PART 7 — light discovery integration
# ════════════════════════════════════════════════════════════════════════════
def create_thesis_stub_from_theme(
    theme_object, ticker: str, weight_placeholder: Optional[float] = None
) -> ThesisTrackerRecord:
    """Build a thesis STUB linked to a discovery ThemeObject. Copies only what the
    theme already states in plain English; invents NOTHING priceable.

    Copies:  plain-English thesis (statement), source_theme_id, source_evidence_ids,
             kill_criteria (only if explicit falsifiers exist).
    Never sets: bull/base/bear prices, probabilities, current price, recommendation.
             weight_placeholder is set ONLY if passed in explicitly.
    """
    source_theme_id = getattr(theme_object, "id", None)
    source_run_id = getattr(theme_object, "run_id", None)  # not present today -> None

    provenance = getattr(theme_object, "provenance", None)
    evidence_ids = list(getattr(provenance, "evidence", []) or []) if provenance else []

    kill_criteria: Optional[str] = None
    risk = getattr(theme_object, "risk", None)
    falsifiers = getattr(risk, "falsifiers", None) if risk else None
    if falsifiers:
        kill_criteria = "; ".join(f.kill_rule for f in falsifiers if f.kill_rule)

    return ThesisTrackerRecord(
        ticker=ticker,
        weight_placeholder=weight_placeholder,
        thesis=getattr(theme_object, "statement", None),
        kill_criteria=kill_criteria,
        status="watchlist",
        source_theme_id=source_theme_id,
        source_run_id=source_run_id,
        source_evidence_ids=evidence_ids,
    )
