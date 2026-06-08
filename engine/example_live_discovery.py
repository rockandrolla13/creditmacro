"""Manual live-discovery smoke command (DISCOVERY ONLY — never expression).

    ALLOW_LIVE_LLM_DISCOVERY=1 python -m engine.example_live_discovery \
      --provider llm --mode discovery \
      --input "AI capex funding is creating RV opportunities across hyperscalers, \
               data-center project bonds and HY HPC issuers." \
      --current-source wiki/sources/jpm-ai-capex-funding-2026-05-11.md \
      --axis "project_bond_OAS_minus_related_hyperscaler_OAS" --axis "Data_Centers_OAS_minus_Technology_OAS"

Reads METHOD memory, treats --current-source as current input, refuses archived CASE memory,
produces the causal object / axes / system map / loop diagnosis / critique / ranked families,
freezes the snapshot, and STOPS. Writes a private (gitignored) capture record. No trades.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .capture import LiveRunRecord, input_hash, write_run_record
from .cases import PolicyConfig
from .memory import MemoryRetriever, load_wiki_pages
from .provider_select import run_discovery, select_discovery_provider


def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Live LLM discovery (discovery-only).")
    p.add_argument("--provider", choices=["scripted", "llm"], default="llm")
    p.add_argument("--mode", choices=["discovery"], default="discovery")
    p.add_argument("--input", required=True, help="research sentence / idea")
    p.add_argument("--current-source", default=None, help="path to a current-input source card")
    p.add_argument("--axis", action="append", default=[], help="source-derived axis candidate (repeatable)")
    p.add_argument("--wiki", default="wiki")
    p.add_argument("--no-capture", action="store_true")
    return p


def run(argv: Optional[list[str]] = None) -> LiveRunRecord:
    args = build_argparser().parse_args(argv)

    # METHOD-only retriever over the wiki (phase A; fail-closed on CASE).
    retriever = MemoryRetriever(load_wiki_pages(args.wiki), phase="A")
    current_sources = [Path(args.current_source).stem] if args.current_source else []

    provider = select_discovery_provider(
        args.provider, research_text=args.input, current_input_axes=args.axis,
        current_sources=current_sources, retriever=retriever,
    )
    theme, memo = run_discovery(provider, PolicyConfig())

    families = [f.family for f in theme.strategy_families]
    print(memo)
    print("\n=== ranked strategy families:", families or "(none — blocked)")
    print("=== status:", theme.status, "| block_reason:", theme.block_reason)
    print("=== NO-TRADE: pricing", theme.pricing, "| sizing", theme.sizing,
          "| expressions", theme.expressions)

    record = LiveRunRecord(
        run_id=f"live-{input_hash(args.input)}",
        timestamp=datetime.now(timezone.utc).isoformat(),
        model_name=getattr(provider, "model", "n/a"),
        provider=args.provider,
        input_hash=input_hash(args.input),
        source_slugs=current_sources,
        method_pages_read=getattr(provider, "memory_log", {}).get("method_pages_read", []),
        case_pages_refused=getattr(provider, "memory_log", {}).get("case_pages_refused", []),
        prompt_names=["expand_causal", "define_axis", "build_system_map",
                      "diagnose_loops", "critique_mental_model"],
        blocked_status=theme.block_reason,
        final_strategy_families=families,
        no_trade_confirmation=(theme.pricing is None and theme.sizing is None
                               and not theme.expressions),
    )
    if not args.no_capture:
        path = write_run_record(record, slug=current_sources[0] if current_sources else "adhoc")
        print("=== capture written:", path)
    return record


if __name__ == "__main__":
    run()
