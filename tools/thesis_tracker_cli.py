"""Human-facing CLI for the Thesis Tracker (PART 5/6).

    python tools/thesis_tracker_cli.py init          --db data/thesis_tracker.sqlite
    python tools/thesis_tracker_cli.py upsert-market --ticker AAPL --current-price 200 \
        --as-of-date 2026-06-10 --source manual
    python tools/thesis_tracker_cli.py upsert-thesis --ticker AAPL --thesis "..." \
        --bull 300 --base 250 --bear 150 --pbull 0.25 --pbase 0.5 --pbear 0.25
    python tools/thesis_tracker_cli.py upsert-thesis --json path/to/thesis.json   # or .yaml
    python tools/thesis_tracker_cli.py list
    python tools/thesis_tracker_cli.py show --ticker AAPL [--verbose]
    python tools/thesis_tracker_cli.py export-json
    python tools/thesis_tracker_cli.py export-md

It persists ONLY what you provide. It never infers a target price, a probability, or
a current price; rows with missing/off-sum probabilities are stored and shown FLAGGED
(probability_check = MISSING / CHECK). Free-text notes are hidden unless --verbose.

A `--json` file may be a single row object or a bulk `{"rows": [ {...}, {...} ]}`
document, in JSON or YAML. Only the keys present in each object are written (merge);
absent fields on an existing row are preserved.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Sequence

# Allow direct-script invocation (python tools/thesis_tracker_cli.py ...) by putting
# the repo root on sys.path before importing the engine package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pydantic import ValidationError

from engine.schema.thesis_tracker import (
    ComputedThesisTrackerRecord,
    MarketDataRecord,
    ThesisTrackerRecord,
)
from engine.thesis_tracker import (
    DEFAULT_DB_PATH,
    export_thesis_tracker_json,
    export_thesis_tracker_markdown,
    get_thesis,
    init_thesis_db,
    list_theses,
    upsert_market_data,
    upsert_thesis,
)


def _fmt(x: Optional[float], nd: int = 2) -> str:
    return "—" if x is None else f"{x:.{nd}f}"


def _pct(x: Optional[float]) -> str:
    return "—" if x is None else f"{x * 100:.1f}%"


# ── ingestion (PART 6) ───────────────────────────────────────────────────────
def _load_json_or_yaml(path: Path) -> dict:
    text = path.read_text()
    if path.suffix.lower() in (".yaml", ".yml"):
        import yaml  # PyYAML; only imported when a YAML file is supplied
        return yaml.safe_load(text)
    return json.loads(text)


def _rows_from_file(path: Path) -> list[dict]:
    """A `--json` file is either one row object or {"rows": [ ... ]}."""
    data = _load_json_or_yaml(path)
    if isinstance(data, dict) and "rows" in data:
        return list(data["rows"])
    return [data]


# ── rendering ────────────────────────────────────────────────────────────────
def _print_row(c: ComputedThesisTrackerRecord, verbose: bool) -> None:
    print(f"{c.ticker}  [{c.status}]  check={c.probability_check}")
    print(f"  thesis            : {c.thesis or '—'}")
    print(f"  weight            : {_fmt(c.weight_placeholder, 4)}")
    print(f"  targets B/Ba/Be   : {_fmt(c.bull_case_price)} / "
          f"{_fmt(c.base_case_price)} / {_fmt(c.bear_case_price)}")
    print(f"  probs  B/Ba/Be    : {_pct(c.p_bull)} / {_pct(c.p_base)} / {_pct(c.p_bear)}")
    print(f"  weighted price    : {_fmt(c.probability_weighted_price)}")
    print(f"  current price     : {_fmt(c.current_price)}")
    print(f"  upside to current : {_pct(c.upside_to_current)}")
    print(f"  next catalyst     : {c.next_catalyst or '—'} ({c.catalyst_date or '—'})")
    print(f"  kill criteria     : {c.kill_criteria or '—'}")
    if verbose:
        print(f"  notes             : {c.notes or '—'}")
        print(f"  source theme/run  : {c.source_theme_id or '—'} / {c.source_run_id or '—'}")
        print(f"  source evidence   : {', '.join(c.source_evidence_ids) or '—'}")


def _print_table(rows: list[ComputedThesisTrackerRecord]) -> None:
    cols = ("Ticker", "Weight", "Check", "Weighted Px", "Current", "Upside",
            "Next Catalyst", "Catalyst Date", "Status")
    print("  ".join(f"{c:<13}" for c in cols).rstrip())
    for r in rows:
        cells = (
            r.ticker, _fmt(r.weight_placeholder, 4), r.probability_check,
            _fmt(r.probability_weighted_price), _fmt(r.current_price),
            _pct(r.upside_to_current), (r.next_catalyst or "—")[:13],
            str(r.catalyst_date or "—"), r.status,
        )
        print("  ".join(f"{str(c):<13}" for c in cells).rstrip())


# ── parser ───────────────────────────────────────────────────────────────────
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="thesis_tracker_cli", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def _with_db(sp):
        sp.add_argument("--db", default=str(DEFAULT_DB_PATH), help="path to the SQLite file")
        return sp

    _with_db(sub.add_parser("init", help="create the database and apply migrations"))

    m = _with_db(sub.add_parser("upsert-market", help="insert/update a ticker's current price"))
    m.add_argument("--ticker", required=True)
    m.add_argument("--current-price", type=float)
    m.add_argument("--as-of-date", help="ISO date YYYY-MM-DD")
    m.add_argument("--source")
    m.add_argument("--notes")

    t = _with_db(sub.add_parser("upsert-thesis", help="insert/merge a thesis row (args or --json)"))
    t.add_argument("--json", dest="json_path", help="JSON/YAML file: one row or {\"rows\":[...]}")
    t.add_argument("--ticker")
    t.add_argument("--thesis")
    t.add_argument("--weight", type=float)
    t.add_argument("--bull", type=float)
    t.add_argument("--base", type=float)
    t.add_argument("--bear", type=float)
    t.add_argument("--pbull", type=float)
    t.add_argument("--pbase", type=float)
    t.add_argument("--pbear", type=float)
    t.add_argument("--next-catalyst")
    t.add_argument("--catalyst-date", help="ISO date YYYY-MM-DD")
    t.add_argument("--kill")
    t.add_argument("--status", default="active")
    t.add_argument("--notes")
    t.add_argument("--reason", help="audit-log reason for this change")

    _with_db(sub.add_parser("list", help="table of all theses"))

    s = _with_db(sub.add_parser("show", help="show one thesis row"))
    s.add_argument("--ticker", required=True)
    s.add_argument("--verbose", action="store_true", help="also print notes + provenance")

    _with_db(sub.add_parser("export-json", help="print all rows as JSON"))
    _with_db(sub.add_parser("export-md", help="print all rows as a Markdown table"))
    return p


# ── dispatch ─────────────────────────────────────────────────────────────────
def _thesis_args_to_kwargs(args: argparse.Namespace) -> dict:
    """Only the flags the operator actually passed become record fields (so merge
    preserves the rest). `status` defaults to 'active' on a fresh row."""
    mapping = {
        "ticker": args.ticker, "thesis": args.thesis, "weight_placeholder": args.weight,
        "bull_case_price": args.bull, "base_case_price": args.base, "bear_case_price": args.bear,
        "p_bull": args.pbull, "p_base": args.pbase, "p_bear": args.pbear,
        "next_catalyst": args.next_catalyst, "catalyst_date": args.catalyst_date,
        "kill_criteria": args.kill, "notes": args.notes,
    }
    kwargs = {k: v for k, v in mapping.items() if v is not None}
    if args.status != "active":  # only override when explicitly changed
        kwargs["status"] = args.status
    return kwargs


def _dispatch(args: argparse.Namespace) -> int:
    db = args.db

    if args.cmd == "init":
        init_thesis_db(db)
        print(f"initialized {db}")
        return 0

    if args.cmd == "upsert-market":
        upsert_market_data(db, MarketDataRecord(
            ticker=args.ticker, current_price=args.current_price,
            as_of_date=args.as_of_date, source=args.source, notes=args.notes,
        ))
        print(f"saved market data for {args.ticker.strip().upper()}")
        return 0

    if args.cmd == "upsert-thesis":
        if args.json_path:
            rows = _rows_from_file(Path(args.json_path))
        else:
            if not args.ticker:
                print("error: upsert-thesis needs --ticker or --json", file=sys.stderr)
                return 2
            rows = [_thesis_args_to_kwargs(args)]
        for row in rows:
            tid = upsert_thesis(db, ThesisTrackerRecord(**row), reason=getattr(args, "reason", None))
            print(f"saved {ThesisTrackerRecord(**row).ticker} (thesis_id={tid})")
        return 0

    if args.cmd == "list":
        rows = list_theses(db)
        if not rows:
            print("(no thesis rows yet)")
            return 0
        _print_table(rows)
        return 0

    if args.cmd == "show":
        c = get_thesis(db, args.ticker)
        if c is None:
            print(f"no thesis row for {args.ticker.strip().upper()}", file=sys.stderr)
            return 1
        _print_row(c, verbose=args.verbose)
        return 0

    if args.cmd == "export-json":
        print(json.dumps(export_thesis_tracker_json(db), indent=2))
        return 0

    if args.cmd == "export-md":
        print(export_thesis_tracker_markdown(db), end="")
        return 0

    return 1  # pragma: no cover — argparse enforces a valid subcommand


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        return _dispatch(args)
    except ValidationError as e:
        print(f"error: invalid input — {e.error_count()} problem(s):", file=sys.stderr)
        for err in e.errors():
            loc = ".".join(str(p) for p in err["loc"])
            print(f"  {loc}: {err['msg']}", file=sys.stderr)
        return 2
    except (KeyError, FileNotFoundError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
