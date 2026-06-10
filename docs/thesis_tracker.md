# Thesis Tracker

> A persistent, SQLite-backed record of **one human thesis row per ticker**, with a
> computed read model (probability check, probability-weighted price, upside to current)
> and an append-only audit log. It is a **standalone sidecar**: it does not feed the
> discovery engine, the memory firewall, or expression sizing, and it **never infers**
> a target price, a probability, a current price, a weight, or a recommendation.
> Incomplete rows are allowed — they persist and are **flagged**, never silently fixed.

---

## Why this exists

This replaces a spreadsheet "Thesis_Tracker" sheet. The same information lives in a
queryable, auditable database instead of an `.xlsx`. The two derived numbers a human
wants — *what's the probability-weighted price?* and *what's the upside to where it
trades now?* — are computed automatically and re-derived on every read, so they can
never go stale relative to the inputs.

## Discipline (what it will NOT do)

- No inference of bull/base/bear targets, probabilities, current prices, weights, or
  recommendations. You type them; it stores them.
- Probabilities, if all three are present, are **not forced** to sum to 1 at write time.
  An off-sum row persists and is flagged `probability_check = CHECK`. A row missing any
  probability is flagged `MISSING`. Only an `OK` row gets a weighted price.
- No trade execution, no leg/hedge/sizing output. This is a tracking record, not a trade.
- Free-text notes are private: the CLI hides them unless you pass `--verbose`.

## Field conventions

- **It is a persistent SQLite store, not a workbook.** There is no `.xlsx`; the canonical
  store is `data/thesis_tracker.sqlite`.
- **Probabilities are decimals: 40% = `0.40`** (each of `p_bull`/`p_base`/`p_bear` is in
  `[0, 1]`). The three are `OK` only when they sum to 1.0 (within `1e-4`).
- **Bull / base / bear target prices are user inputs** — never inferred.
- **Probability-weighted price is computed**: `Σ price·p`, only on an `OK` row.
- **Upside to current comes from `market_data`** (`weighted_price / current_price − 1`);
  if the ticker has no `market_data` row, upside stays blank.
- **Kill criteria** should describe *what would invalidate the thesis* — the observable
  condition under which you'd abandon it (e.g. "exit if the funding gap closes / driver
  fails / PW upside turns negative"). It is a discipline field, not a stop-loss order.
- **Rows may be incomplete** — they persist and are flagged (`probability_check` =
  `MISSING` / `CHECK`); only complete, consistent rows produce derived numbers.
- **This is not an execution system.**

---

## Layout

| Path | Role |
|---|---|
| `engine/schema/thesis_tracker.py` | Pydantic models: `MarketDataRecord`, `ThesisTrackerRecord`, `ComputedThesisTrackerRecord` (+ `from_record` factory — the math). |
| `engine/thesis_tracker.py` | `ThesisTrackerDB` low-level store **and** the stateless service API (PART 4) + `create_thesis_stub_from_theme` (PART 7). |
| `db/migrations/0001_thesis_tracker.sql` | Tables `market_data`, `thesis_tracker`; the computed view `thesis_tracker_view`. |
| `db/migrations/0002_thesis_audit_log.sql` | Append-only `thesis_audit_log`. |
| `tools/thesis_tracker_cli.py` | Human CLI (PART 5/6). |
| `data/thesis_tracker.sqlite` | The live DB. **Gitignored** (may contain private notes). |

The schema/migrations/code/tests/docs are committed; the `.sqlite` data file is not
(`.gitignore`: `data/*.sqlite`, `-shm`, `-wal`).

## Data model

`ThesisTrackerRecord` (stored), one row per ticker:

```
thesis_id · ticker · weight_placeholder · thesis
bull_case_price · base_case_price · bear_case_price
p_bull · p_base · p_bear
next_catalyst · catalyst_date · kill_criteria
status ∈ {active, watchlist, closed, killed, stale, needs_review}
source_theme_id · source_run_id · source_evidence_ids[]   (discovery links, PART 7)
notes
```

`ComputedThesisTrackerRecord` adds the derived view fields:

| Field | Rule |
|---|---|
| `probability_sum` | `p_bull + p_base + p_bear` if all three present, else `None`. |
| `probability_check` | `MISSING` if any prob absent; `OK` if `|sum − 1| < 1e-4`; else `CHECK`. |
| `probability_weighted_price` | `Σ price·p` — **only** when `check == OK` and all three targets present; else `None`. |
| `current_price` | from `market_data` (left join); `None` if the ticker is absent there. |
| `upside_to_current` | `weighted_price / current_price − 1` when both exist and current ≠ 0; else `None`. |

The math has **one definition** (`ComputedThesisTrackerRecord.from_record`) mirrored by the
SQL view; `tests/unit/test_thesis_tracker_db.py::test_view_matches_python_definition`
pins them together. The `1e-4` tolerance equals the original spreadsheet rule
`ABS(SUM−100%) < 0.0001`.

## Service API (`engine/thesis_tracker.py`)

```python
init_thesis_db(db_path)                       # create file + apply migrations (idempotent)
apply_migrations(db_path)                      # apply pending migrations
upsert_market_data(db_path, MarketDataRecord)
upsert_thesis(db_path, ThesisTrackerRecord, reason=None) -> thesis_id
get_thesis(db_path, ticker)   -> ComputedThesisTrackerRecord | None
list_theses(db_path, status=None) -> list[ComputedThesisTrackerRecord]
close_thesis(db_path, ticker, reason)          # status -> closed; never deletes
delete_thesis(db_path, ticker, reason)         # snapshots to audit log, THEN removes
export_thesis_tracker_json(db_path) -> list[dict]
export_thesis_tracker_markdown(db_path) -> str
create_thesis_stub_from_theme(theme_object, ticker, weight_placeholder=None) -> ThesisTrackerRecord
```

Key semantics:

- **Merge on upsert.** Only fields explicitly set on the incoming record (pydantic
  `model_fields_set`) overwrite the stored row; everything else is preserved. So
  `upsert_thesis(db, ThesisTrackerRecord(ticker="AAPL", thesis="revised"))` updates the
  thesis text and leaves targets/probabilities untouched.
- **Stable identity.** `ticker` is the user-facing key; `thesis_id` is the stable DB key,
  assigned once and preserved across updates.
- **Everything is audited.** `create` / `update` / `close` / `delete` each append to
  `thesis_audit_log` with a reason and a JSON snapshot. `delete` writes the **pre-delete**
  snapshot first, so no row is ever lost silently.

## CLI (`tools/thesis_tracker_cli.py`)

```bash
python tools/thesis_tracker_cli.py init          --db data/thesis_tracker.sqlite
python tools/thesis_tracker_cli.py upsert-market --ticker AAPL --current-price 200 \
    --as-of-date 2026-06-10 --source manual
python tools/thesis_tracker_cli.py upsert-thesis --ticker AAPL --thesis "..." \
    --bull 300 --base 250 --bear 150 --pbull 0.25 --pbase 0.5 --pbear 0.25
python tools/thesis_tracker_cli.py upsert-thesis --json path/to/thesis.json     # PART 6
python tools/thesis_tracker_cli.py list
python tools/thesis_tracker_cli.py show --ticker AAPL [--verbose]               # notes need --verbose
python tools/thesis_tracker_cli.py export-json
python tools/thesis_tracker_cli.py export-md
```

Invalid input (e.g. a probability outside `[0,1]`) exits non-zero and persists nothing.

### Placeholder ingestion (PART 6)

`--json` accepts JSON or YAML, a single row or a bulk document. Only the keys present
are written (merge-friendly). Single row:

```json
{
  "ticker": "ABC",
  "weight_placeholder": 0.05,
  "thesis": "Two to three sentence thesis goes here.",
  "bull_case_price": 150, "base_case_price": 110, "bear_case_price": 70,
  "p_bull": 0.25, "p_base": 0.50, "p_bear": 0.25,
  "next_catalyst": "Earnings", "catalyst_date": "2026-07-30",
  "kill_criteria": "Exit if the thesis driver fails or PW upside turns negative."
}
```

Bulk:

```json
{ "rows": [ { "ticker": "ABC", ... }, { "ticker": "XYZ", ... } ] }
```

## Discovery link (PART 7)

`create_thesis_stub_from_theme(theme_object, ticker, weight_placeholder=None)` builds a
`watchlist` stub linked to a discovery `ThemeObject`. It copies the plain-English thesis
(`statement`), `source_theme_id` (`theme.id`), `source_evidence_ids`
(`theme.provenance.evidence`), and `kill_criteria` (joined from `theme.risk.falsifiers`
**only if explicit falsifiers exist**). It sets **no** prices, probabilities, current
price, weight, or recommendation. Stubs are created on request only — discovery output
is never auto-converted into ticker theses.

## Tests

```
tests/unit/test_thesis_tracker_schema.py    # validators + computed math
tests/unit/test_thesis_tracker_db.py        # store, migrations, view==python
tests/unit/test_thesis_tracker_service.py   # merge, audit, close/delete, export, stub
tests/unit/test_thesis_tracker_cli.py       # CLI surface incl. JSON/YAML, --verbose
```
