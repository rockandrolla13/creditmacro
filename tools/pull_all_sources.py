"""Pull new memos from every registry entry and refresh the index files.

Iterates over every key in investor_memos_registry.yaml and calls
fetch_investor_memos.run() for each one (limit=5, delay_s=0.5 per memo).
Existing slugs are skipped automatically (the fetcher is idempotent).
After pulling, rebuilds docs/markdowns-index.md and docs/investment-memos-index.md.

Usage:
    python3 tools/pull_all_sources.py

Cron usage (see docs/weekly-pull.md):
    0 7 * * 1 cd <repo> && /usr/bin/python3 tools/pull_all_sources.py >> /tmp/creditmacro_weekly_pull.log 2>&1
"""
from __future__ import annotations

import sys
from pathlib import Path

# Allow invocation as `python3 tools/pull_all_sources.py` from any cwd.
_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from tools.fetch_investor_memos import run, Registry  # noqa: E402


def main() -> None:
    reg = Registry.load()
    wiki_root = _REPO_ROOT / "wiki"
    out_root = _REPO_ROOT

    total_fetched = 0
    total_skipped = 0
    total_errors = 0

    for key in reg:
        print(f"[pull] {key} ...", flush=True)
        summary = run(
            key,
            registry=reg,
            out_root=out_root,
            wiki_root=wiki_root,
            limit=5,
            delay_s=0.5,
        )
        status_parts = [f"fetched={summary.fetched}", f"skipped={summary.skipped}"]
        if summary.errors:
            status_parts.append(f"errors={len(summary.errors)}")
            for err in summary.errors:
                print(f"  [error] {err}", flush=True)
        print(f"  {key}: {', '.join(status_parts)}", flush=True)
        total_fetched += summary.fetched
        total_skipped += summary.skipped
        total_errors += len(summary.errors)

    print(
        f"\n[pull] Done. fetched={total_fetched}, skipped={total_skipped},"
        f" errors={total_errors}",
        flush=True,
    )

    # Rebuild index files so they reflect any newly ingested memos.
    print("[index] Rebuilding docs/markdowns-index.md and docs/investment-memos-index.md ...", flush=True)
    from tools.build_indexes import main as build_indexes_main  # noqa: E402
    build_indexes_main()
    print("[index] Done.", flush=True)


if __name__ == "__main__":
    main()
