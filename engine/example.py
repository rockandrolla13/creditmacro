"""
Worked example: "AI issuance will steepen IG credit curves"

Runs Stage 0 → Engine 1 → Engine 2 → Engine 3 → Engine 4 → PM Gate.
Emits (a) a fully populated ThemeObject as JSON and
      (b) a markdown decision memo answering Q1–Q13.

As of the case-system refactor, Engine 1–4 are no longer hand-built here: the theme
is loaded from cases/ai_issuance.yaml and run through the generic runner
(ScriptedProvider → run_workflow). The Stage-0 block and the memo renderer are
unchanged, so this module's output is identical (modulo the inherently non-
deterministic id / created_at / last_updated fields).

LEGEND used throughout this file:
  [REAL]        — computed here from stated inputs; no external data needed
  [PLACEHOLDER] — requires live Bloomberg / index data; value shown is indicative

Run with:  python -m engine.example
"""
from __future__ import annotations

from pathlib import Path

from .case_loader import load_case
from .engines import compute_omega
from .scripted_provider import ScriptedProvider
from .schema import CandidateTheme, ConsensusSignal, Observation
from .stage0 import IngestionResult, rank_candidates
from .workflow import run_workflow


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 0 — ingestion streams (hand-built; LLM stub bypassed)
# ─────────────────────────────────────────────────────────────────────────────

# Three Observations that support the AI-issuance thesis
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

# One CandidateTheme derived from the observations
CANDIDATE = CandidateTheme(
    id="ct_ai_curve",
    statement="AI capex cycle will steepen the IG credit curve as 30Y supply overwhelms "
              "duration demand, widening 5s30s OAS slope from current 52bps toward 75bps.",
    horizon="6–12 months",
    evidence_ids=["obs_001", "obs_002", "obs_003"],
    consensus_ids=["cs_001"],
)

# One ConsensusSignal — TAARSS ETF flow z-score for IG credit
CS_IG_FLOW = ConsensusSignal(
    id="cs_001",
    source="TAARSS / DB Flow Whisperer",
    topic="IG credit curve steepening",
    attention_strength=1.2,   # [PLACEHOLDER] positive z-score = crowded / priced-in
    direction="positive",
    date="2024-11-07",
)

signals = [CS_IG_FLOW]

# ── Stage 0 ranking [REAL] ─────────────────────────────────────────────────

ranked = rank_candidates([CANDIDATE], observations, signals)

stage0_result = IngestionResult(
    observations=observations,
    candidate_themes=[CANDIDATE],
    consensus_signals=signals,
    ranked_candidates=ranked,
)


# ─────────────────────────────────────────────────────────────────────────────
# ENGINES 1–4 — loaded from the case and run through the generic runner
# ─────────────────────────────────────────────────────────────────────────────

CASE_PATH = Path(__file__).resolve().parent.parent / "cases" / "ai_issuance.yaml"

_case = load_case(CASE_PATH)
theme, _memo = run_workflow(ScriptedProvider(_case), _case.resolved_policy())

# Re-expose the objects the memo renderer (and the golden-master tests) reference.
thesis = theme.thesis
axis = theme.axis
scenarios = theme.scenarios
pricing = theme.pricing
expressions = theme.expressions
sizing = theme.sizing
risk = theme.risk
pm_gate = theme.pm_gate

X_MKT = _case.x_mkt        # [PLACEHOLDER] live market price of the axis, bps
NORMAL_FV = _case.normal_fv  # [PLACEHOLDER] unconditional / regime mean

_by_id = {e.id: e for e in expressions}
expr_steepener = _by_id["expr_cds_5s30s"]
expr_etf_basis = _by_id["expr_etf_basis"]

# [REAL] derived quantities used in the memo tables
STEEPENER_PROBS = [s.p_s for s in scenarios]
STEEPENER_PNL = [p.pnl for p in expr_steepener.scenario_pnl]
omega_steepener = compute_omega(STEEPENER_PNL, weights=STEEPENER_PROBS, tau=0.0)
score_val = expr_steepener.score
EXPECTED_PNL_STEEPENER = sum(p * pnl for p, pnl in zip(STEEPENER_PROBS, STEEPENER_PNL))
RHO2 = expr_steepener.purity
LIQUIDITY = expr_steepener.liquidity
COST_STEEPENER = expr_steepener.round_trip_cost_bps
COST_ETF = expr_etf_basis.round_trip_cost_bps


# ─────────────────────────────────────────────────────────────────────────────
# EMIT (a) ThemeObject JSON
# ─────────────────────────────────────────────────────────────────────────────

THEME_JSON = theme.model_dump_json(indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# EMIT (b) Markdown decision memo — Q1 through Q13
# ─────────────────────────────────────────────────────────────────────────────

q_s_fmt = ", ".join(f"{q:.3f}" for q in pricing.priced_in.q_s)
scenario_rows = "\n".join(
    f"| {s.name} | {s.p_s:.0%} | {s.implied_axis_value:.0f}bps | "
    f"{pricing.priced_in.q_s[i]:.3f} | {s.pnl_per_unit:+.0f}bps |"
    for i, s in enumerate(scenarios)
)
falsifier_rows = "\n".join(
    f"| {f.observable} | {f.threshold} | {f.kill_rule} |"
    for f in risk.falsifiers
)

MEMO = f"""# Decision Memo — AI Issuance Steepening IG Credit Curves
*Generated by Theme-to-Trade Conversion Engine v0.1 — prototype*

> **[REAL]** = computed from stated inputs (no external data required)
> **[PLACEHOLDER]** = requires live Bloomberg / index data; value shown is indicative

---

## Q1 — What is the thesis?

{theme.statement}

**Direction:** {thesis.direction_of_view}
**Horizon:** {theme.horizon}

---

## Q2 — What is the universe?

Top-25 IG issuers by AI capex intensity (Bloomberg BICS Tech sector),
min $1bn outstanding, OAS ≤ 300bps. See `axis.definition` for full spec.

Drivers:
| Driver | Sign | Proxy Observable | Current Level |
|--------|------|-----------------|--------------|
| AI supply surge | + | Bloomberg BICS Tech net IG issuance, 30Y, YTD ($bn) | 185bn [PLACEHOLDER] |
| Duration demand mismatch | + | LDI inflows to 20Y+ IG ($bn/month, EPFR) | unwired [PLACEHOLDER] |
| Mean reversion from compressed slope | + | IG AI-issuer 5s30s OAS slope (bps) | 52bps [PLACEHOLDER] |

---

## Q3 — What is the axis? (Gate 1)

**Definition:** {axis.definition}

**Measurement:** {axis.measurement}

**Current value:** {axis.current_value}bps [PLACEHOLDER]
**3Y mean:** {axis.history.mean}bps [PLACEHOLDER] | **Vol:** {axis.history.vol}bps [PLACEHOLDER]
**Percentile:** {axis.history.percentile}th [PLACEHOLDER]

Gate 1 PASS: axis is a named, computable time series with a full data recipe.

---

## Q4 — What is fair value under normal conditions?

**Normal FV:** {pricing.normal_fv}bps [PLACEHOLDER] (midpoint of current and 3Y mean)

---

## Q5 — What is fair value under our scenario distribution?

**Scenario FV = Σ p_s × X_s = {pricing.scenario_fv}bps [REAL]**

| Scenario | p_s | X_s | q_s (mkt-implied) | P&L/unit |
|----------|-----|-----|-------------------|---------|
{scenario_rows}

---

## Q6 — What does the market price in? (max-entropy q)

Market price: X_mkt = {X_MKT}bps [PLACEHOLDER]

**q_s = [{q_s_fmt}] [REAL — SLSQP max-entropy solver]**

q* minimises KL(q ‖ uniform) subject to Σ q_s X_s = {X_MKT}bps, Σ q_s = 1.
The solver assigns more probability to the Risk-Off and Capex Pause scenarios than our p_s,
reflecting that the market prices less steepening than our thesis implies.

Priced-in fraction: **{pricing.priced_in.frac:.0%}** of the range from normal_fv to scenario_fv.

Gate 2 PASS: residual_edge is computed.

---

## Q7 — What is the residual edge?

**Edge = ⟨p − q, X⟩ = {pricing.residual_edge:+.1f}bps [REAL]**

Interpretation: our thesis implies the axis is worth ~{pricing.residual_edge:.0f}bps more
than the market currently prices. This is the raw edge *before* transaction costs,
crowding, and expression-specific purity discounts.

---

## Q8 — What is the best expression? (Gate 3)

Candidates scored (gates FIRST, rank SECOND):

| Expression | Ω [REAL] | ρ² | λ | Cost | Score | Gate |
|-----------|---------|-----|---|------|-------|------|
| 5s30s IG CDS steepener | {omega_steepener:.2f} | {RHO2} [PH] | {LIQUIDITY} [PH] | {COST_STEEPENER:.1f}bps={COST_STEEPENER/EXPECTED_PNL_STEEPENER:.0%} of E[PnL] [PH] | {score_val:.2f} [REAL*] | PASS |
| IG ETF 5s30s basis (LQD/VCLT) | — | 0.48 [PH] | 0.32 [PH] | {COST_ETF:.1f}bps [PH] | — | FAIL: λ<0.40 |

*score [REAL given PLACEHOLDER inputs]: ρ² × Ω × (1+a·κ) × λ × exp(−g·c) / (1+capital)
 cost gate: round_trip_cost / E[PnL] must be < 33% (Carver)

**Best expression:** {expr_steepener.strategy_family}
**Long:** {expr_steepener.long_leg}
**Short:** {expr_steepener.short_leg}
**Hedge ratio:** {expr_steepener.hedge_ratio} (DV01-neutral [PLACEHOLDER])

Gate 3 PASS: at least one expression survived the Omega ≥ 2 and liquidity gates.

---

## Q9 — What does the P&L distribution look like?

| Scenario | Prob | P&L/unit |
|----------|------|---------|
| AI Surge | 40% | +40bps [REAL] |
| Base | 35% | +20bps [REAL] |
| Risk-Off | 15% | −10bps [REAL] |
| Capex Pause | 10% | −15bps [REAL] |

**Omega ratio Ω(0) = {omega_steepener:.2f} [REAL]**
E[gain] = 0.40×40 + 0.35×20 = 23bps | E[loss] = 0.15×10 + 0.10×15 = 3bps

---

## Q10 — What is the size?

Conviction: **{sizing.conviction}/4** (Alaph grid) [PLACEHOLDER judgment]
Sizing factor: **{sizing.sizing_factor:.0%}** [PLACEHOLDER — Alaph grid output]
Gross target P&L: **${sizing.target_pnl:,.0f}** [REAL given PLACEHOLDER inputs]

Vol targeting (Carver): vol_target={sizing.vol_target_bps}bps / realized={sizing.realized_vol_bps}bps
→ vol_scalar = **{sizing.vol_scalar:.3f}** [REAL] — position sized up slightly (realized < target)

Cost (Carver): {sizing.round_trip_cost_bps}bps/round-trip × {sizing.expected_roundtrips:.0f} trips/yr
→ annual cost ≈ **${(sizing.target_pnl - sizing.net_target_pnl):,.0f}**
→ **Net target P&L: ${sizing.net_target_pnl:,.0f}** [REAL given PLACEHOLDER inputs]

**Position:** {sizing.position}

---

## Q11 — What is the stop?

**Stop level:** axis < **{risk.stop_loss.level}bps** [PLACEHOLDER — 1.5× vol below entry]
*{risk.stop_loss.rationale}*

---

## Q12 — What proves us wrong? (Gate 4)

| Observable | Threshold | Kill Rule |
|-----------|-----------|-----------|
{falsifier_rows}

Gate 4 PASS: 3 falsifiers, all with computable observables and numeric thresholds.

---

## Q13 — What can the agent NOT resolve? (PM Gate)

The agent stops here. The following questions require PM judgment or live data:

{chr(10).join(f"{i+1}. {q}" for i, q in enumerate(pm_gate.open_questions))}

**The agent does not execute, route orders, or touch a broker.**
Hand this memo to the PM for final decision.

---
*Theme-to-Trade Conversion Engine v0.1 — prototype | {theme.created_at}*
"""


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    from .stage0 import print_ranked_candidates

    print_ranked_candidates(stage0_result)

    print("=" * 80)
    print("THEME OBJECT — JSON")
    print("=" * 80)
    print(THEME_JSON)

    print("\n")
    print("=" * 80)
    print("DECISION MEMO — Q1 through Q13")
    print("=" * 80)
    print(MEMO)


if __name__ == "__main__":
    main()
