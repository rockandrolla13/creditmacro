"""Worked example: AI issuance will steepen IG credit curves."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Optional

from .case_loader import load_case
from .scoring import compute_omega
from .scripted_provider import ScriptedProvider
from .schema import CandidateTheme, ConsensusSignal, Observation
from .stage0 import IngestionResult, rank_candidates
from .workflow import run_workflow

# ─────────────────────────────────────────────────────────────────────────────
# STAGE 0 — ingestion streams (hand-built; LLM stub bypassed). Cheap, pure data —
# kept eager so test_iceberg_wiring can import them without building the pipeline.
# ─────────────────────────────────────────────────────────────────────────────

OBS_SUPPLY = Observation(
    id="obs_001",
    date="2024-11-05",
    source="Citi Credit Weekly 2024-11-08",
    text="AI-linked issuers (MSFT, AMZN, GOOG, META, ORCL) supplied $185bn IG bonds YTD, "
         "30Y-tenor share at 42% vs 28% five-year average.",
    driver_tags=["supply_surge", "tenor_extension"],
)

OBS_DEMAND = Observation(
    id="obs_002",
    date="2024-11-01",
    source="Citi Credit Weekly 2024-11-08",
    text="Duration demand from LDI and insurance remains concentrated in 10–20Y; "
         "30Y IG paper seeing price-sensitive retail bid only.",
    driver_tags=["duration_demand_mismatch"],
)

OBS_CURVE = Observation(
    id="obs_003",
    date="2024-10-28",
    source="Citi Credit Weekly 2024-11-08",
    text="IG 5s30s OAS slope compressed to 52bps vs 75bps 3-year mean; "
         "historically this level precedes at least 15bps re-steepening within 6m.",
    driver_tags=["mean_reversion", "valuation"],
)

observations = [OBS_SUPPLY, OBS_DEMAND, OBS_CURVE]

CANDIDATE = CandidateTheme(
    id="ct_ai_curve",
    statement="AI capex cycle will steepen the IG credit curve as 30Y supply overwhelms "
              "duration demand, widening 5s30s OAS slope from current 52bps toward 75bps.",
    horizon="6–12 months",
    evidence_ids=["obs_001", "obs_002", "obs_003"],
    consensus_ids=["cs_001"],
)

CS_IG_FLOW = ConsensusSignal(
    id="cs_001",
    source="TAARSS / DB Flow Whisperer",
    topic="IG credit curve steepening",
    attention_strength=1.2,   # positive z-score = crowded / priced-in
    direction="positive",
    date="2024-11-07",
)

signals = [CS_IG_FLOW]

ranked = rank_candidates([CANDIDATE], observations, signals)

stage0_result = IngestionResult(
    observations=observations,
    candidate_themes=[CANDIDATE],
    consensus_signals=signals,
    ranked_candidates=ranked,
)

# ─────────────────────────────────────────────────────────────────────────────
# ENGINES 1–4 — loaded from the case and run through the generic runner.
# Built lazily + cached: no pipeline runs at import time.
# ─────────────────────────────────────────────────────────────────────────────

CASE_PATH = Path(__file__).resolve().parent.parent / "cases" / "ai_issuance.yaml"

_BUNDLE: Optional[SimpleNamespace] = None

def build_example() -> SimpleNamespace:
    """Build (once, then cache) the worked-example pipeline output. Returns a namespace of"""
    global _BUNDLE
    if _BUNDLE is not None:
        return _BUNDLE

    _case = load_case(CASE_PATH)
    # The worked example emits detailed legs, so it runs the expression pipeline explicitly
    # (run_workflow defaults to the firewalled discovery mode). The memo is the pipeline's
    # own canonical render — no second, untested renderer here.
    theme, memo = run_workflow(ScriptedProvider(_case), _case.resolved_policy(), mode="expression")

    _by_id = {e.id: e for e in theme.expressions}
    expr_steepener = _by_id["expr_cds_5s30s"]
    expr_etf_basis = _by_id["expr_etf_basis"]
    omega_steepener = compute_omega(
        [p.pnl for p in expr_steepener.scenario_pnl],
        weights=[s.p_s for s in theme.scenarios], tau=0.0,
    )

    _BUNDLE = SimpleNamespace(
        theme=theme,
        thesis=theme.thesis, axis=theme.axis, scenarios=theme.scenarios,
        pricing=theme.pricing, expressions=theme.expressions,
        sizing=theme.sizing, risk=theme.risk, pm_gate=theme.pm_gate,
        expr_steepener=expr_steepener, expr_etf_basis=expr_etf_basis,
        omega_steepener=omega_steepener, score_val=expr_steepener.score,
        theme_json=theme.model_dump_json(indent=2), memo=memo,
    )
    return _BUNDLE

def __getattr__(name: str):
    """PEP 562: serve the lazily-built example names on first access, so importing this"""
    bundle = build_example()
    try:
        return getattr(bundle, name)
    except AttributeError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None

def main() -> None:
    from .stage0 import print_ranked_candidates

    print_ranked_candidates(stage0_result)
    ex = build_example()
    print("=" * 80, "THEME OBJECT — JSON", "=" * 80, sep="\n")
    print(ex.theme_json)
    print("\n" + "=" * 80, "DECISION MEMO", "=" * 80, sep="\n")
    print(ex.memo)

if __name__ == "__main__":
    main()
