"""End-to-end surveillance loop demo (Phase 0 -> 1 -> 3): discover -> persist -> watch -> close.

Uses only the real engine APIs (no live LLM, no wall-clock — every date is supplied):
  1. DISCOVER  : run_workflow over the JPM AI-capex discovery case -> a routed ThemeObject.
  2. PERSIST   : stamp a ForwardHorizon, freeze (snapshot hash), persist as a CASE theme page.
  3. WATCH     : drive the PPI/CPI worked example (plan §5.11) through ThemeMonitorAgent over the
                 tick fixture -> show the status path (whipsaw -> falsified) and a played_out run.
  4. CLOSE     : terminal watch -> ThemeOutcomeRecord + CASE outcome page.

Run from the repo root:  python demo/surveillance_demo.py
Outputs pages under demo/_wiki/ (gitignored) and prints the path + the state tape.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # repo root on path

from engine.case_loader import load_case
from engine.firewall import freeze
from engine.outcomes import append_outcome
from engine.scripted_provider import ScriptedProvider
from engine.schema import ForwardHorizon
from engine.surveillance import AxisState, FalsifierState, ThemeWatch
from engine.surveillance_agent import (
    ThemeMonitorAgent,
    outcome_record_from_watch,
)
from engine.wiki_integration import (
    ClosedWatchPersistInput,
    ThemeObjectPersistInput,
    persist_closed_watch,
    persist_theme_object,
)
from engine.workflow import run_workflow

ROOT = Path(__file__).resolve().parent
WIKI = ROOT / "_wiki"
CASES = ROOT.parent / "cases"
OPENED = date(2026, 1, 1)


def _on(day: int) -> date:
    return date.fromordinal(OPENED.toordinal() + day)


def _hz(window_days: int = 91) -> ForwardHorizon:
    return ForwardHorizon(opened=OPENED, expected_close=_on(window_days),
                          window_label="3m", window_days=window_days)


def step_1_2_discover_and_persist() -> str:
    print("\n=== 1-2. DISCOVER -> PERSIST (JPM AI-capex discovery case) ===")
    case = load_case(CASES / "discovery" / "jpm_ai_capex.yaml")
    theme, _memo = run_workflow(ScriptedProvider(case), case.resolved_policy(), mode="discovery")
    theme = theme.model_copy(update={"forward_horizon": _hz()})
    snap = freeze(theme).content_hash
    print(f"  routed status : {theme.status}")
    print(f"  families      : {[f.family for f in theme.strategy_families]}")
    print(f"  snapshot hash : {snap[:16]}…")
    res = persist_theme_object(ThemeObjectPersistInput(
        theme=theme, snapshot_hash=snap, wiki_root=str(WIKI)))
    page = res.written_paths[0]
    print(f"  routed CASE page written: {page}")
    return page


def _ppi_cpi_watch(window_days: int = 91, *, current: float = 5.0) -> ThemeWatch:
    """The §5.11 worked example: producer- vs consumer-price-sensitive credit differential."""
    return ThemeWatch(
        theme_id="ppi-cpi-producer-consumer-credit-differential",
        snapshot_hash="sha256:demo-frozen-ppi-cpi",
        forward_horizon=_hz(window_days),
        falsifier=FalsifierState(observable="PPI_minus_CPI_diff_bp", threshold=20.0,
                                 direction="below", breach_buffer=3),
        axis_state=AxisState(series="producer_minus_consumer_credit_diff_bp",
                             current=current, entry_level=0.0, modeled_target=100.0),
        last_evidence_date=OPENED)


def step_3_watch_to_falsified() -> ThemeWatch:
    print("\n=== 3a. WATCH: PPI/CPI theme over the tick fixture (whipsaw -> falsified) ===")
    agent = ThemeMonitorAgent()
    w = _ppi_cpi_watch()
    ch = "margin compression -> producer credit spread widening -> PPI-CPI differential widens"
    ax = "PPI_minus_CPI_diff_bp"
    ticks = [json.loads(li) for li in (ROOT / "ppi_cpi_ticks.jsonl").read_text().splitlines() if li.strip()]
    print(f"  {'day':>4}  {'event':<30} {'status':<18} reason")
    for t in ticks:
        now = _on(t["day"])
        if t["kind"] == "falsifier":
            upd, _ = agent.read_falsifier(w, metric_value=t["metric"], now=now)
            ev = f"falsifier_read({t['metric']})"
        else:
            from engine.schema import EvidenceAtom
            atoms = [EvidenceAtom(evidence_id=f"d{t['day']}", source_slug="demo", claim=t["claim"])]
            upd, _ = agent.observe(w, atoms=atoms, now=now, causal_chain=ch, operational_axis=ax,
                                   is_attention_only=t.get("attention", False))
            ev = "evidence" + ("(attention)" if t.get("attention") else "")
        print(f"  {t['day']:>4}  {ev:<30} {upd.status:<18} {upd.reason}")
    whipsaws = [e for e in w.log if e.kind == "whipsaw_averted"]
    print(f"  whipsaws averted: {len(whipsaws)} ; final status: {w.status}")
    return w


def step_3b_played_out() -> ThemeWatch:
    print("\n=== 3b. WATCH: a target-hit run -> played_out ===")
    agent = ThemeMonitorAgent()
    w = _ppi_cpi_watch(current=80.0)            # 80% of modeled target
    upd, alert = agent.read_falsifier(w, metric_value=25.0, now=_on(20))
    print(f"  axis 80% of target -> status {upd.status} ; alert {alert.alert_type}")
    return w


def step_4_close(w: ThemeWatch, reason: str) -> str:
    print(f"\n=== 4. CLOSE: terminal watch '{w.status}' -> outcome record + CASE page ===")
    rec = outcome_record_from_watch(w, p=[0.5, 0.5], q=[0.45, 0.55], X_s=[0.0, 100.0],
                                    X_mkt=float(w.axis_state.current), predicted_edge=20.0,
                                    edge_std=5.0)
    append_outcome(rec, WIKI / "outcomes.jsonl")
    print(f"  ThemeOutcomeRecord: realized_axis_at_horizon={rec.realized_axis_at_horizon}")
    res = persist_closed_watch(ClosedWatchPersistInput(
        watch=w, terminal_reason=reason, outcome=rec, wiki_root=str(WIKI)))
    page = res.written_paths[0]
    print(f"  closed CASE outcome page written: {page}")
    return page


def main() -> None:
    routed_page = step_1_2_discover_and_persist()
    w_fals = step_3_watch_to_falsified()
    w_play = step_3b_played_out()
    closed_page = step_4_close(w_play, "axis_target_reached")
    print("\n=== SUMMARY ===")
    print(f"  routed theme page : {routed_page}")
    print(f"  closed outcome page: {closed_page}")
    print(f"  falsified-run final status: {w_fals.status}")
    print("  loop demonstrated: discover -> persist -> watch -> close. No trades emitted.")


if __name__ == "__main__":
    main()
