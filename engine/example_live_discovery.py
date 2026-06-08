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
from pathlib import Path
from typing import Optional

from .capture import LiveRunRecord
from .cases import PolicyConfig
from .live_discovery import SemanticContractViolation, run_live_discovery
from .memory import MemoryRetriever, load_wiki_pages


def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Live LLM discovery (discovery-only).")
    p.add_argument("--provider", choices=["scripted", "llm"], default="llm")
    p.add_argument("--mode", choices=["discovery"], default="discovery")
    p.add_argument("--input", required=True, help="research sentence / idea")
    p.add_argument("--current-source", default=None, help="path to a current-input source card")
    p.add_argument("--axis", action="append", default=[], help="source-derived axis candidate (repeatable)")
    p.add_argument("--input-kind", default=None,
                   choices=["jpm_report", "curve_steepener", "etf_flow", "margin_compression"],
                   help="enables the automatic axis/family semantic contract for this input kind")
    p.add_argument("--wiki", default="wiki")
    p.add_argument("--no-capture", action="store_true")
    return p


def run(argv: Optional[list[str]] = None) -> LiveRunRecord:
    args = build_argparser().parse_args(argv)

    # METHOD-only retriever over the wiki (phase A; fail-closed on CASE).
    retriever = MemoryRetriever(load_wiki_pages(args.wiki), phase="A")
    current_sources = [Path(args.current_source).stem] if args.current_source else []
    slug = current_sources[0] if current_sources else "adhoc"

    # The harness runs the AUTOMATIC semantic contract before any snapshot and fails closed.
    try:
        result = run_live_discovery(
            research_text=args.input, current_input_axes=args.axis,
            current_sources=current_sources, retriever=retriever,
            input_kind=args.input_kind, policy=PolicyConfig(),
            capture=not args.no_capture, slug=slug,
        )
    except SemanticContractViolation as exc:
        print("=== SEMANTIC CONTRACT FAILED CLOSED (no snapshot frozen) ===")
        for v in exc.violations:
            print("  -", v)
        return exc.record

    theme = result.theme
    print("\n=== ranked strategy families:", result.record.final_strategy_families or "(none — blocked)")
    print("=== status:", theme.status, "| block_reason:", theme.block_reason)
    print("=== axis:", theme.axis.definition if theme.axis else None)
    print("=== NO-TRADE: pricing", theme.pricing, "| sizing", theme.sizing,
          "| expressions", theme.expressions)
    print("=== snapshot_hash:", result.record.snapshot_hash)
    print("=== memory:", result.record.method_pages_read, "| refused:", result.record.case_pages_refused)
    return result.record


if __name__ == "__main__":
    run()
