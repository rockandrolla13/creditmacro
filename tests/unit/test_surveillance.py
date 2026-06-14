"""Phase 3 surveillance core — §5.10 acceptance tests (1–11) + §9 simulator-faithfulness.

These exercise the pure deterministic core (`engine/surveillance.py`): schemas + `derive()` +
`transition()`. Agent-level concerns (writing a `ThemeOutcomeRecord`, the current-input seam, the
blind LLM scorer) are covered when `ThemeMonitorAgent` lands; here we assert the state machine and
the guardrails match the reference simulator exactly.
"""
from __future__ import annotations

from datetime import date

import pytest
from pydantic import ValidationError

from engine.surveillance import (
    AxisState,
    BlindScoringContext,
    FalsifierState,
    ForwardHorizon,
    SurveillancePolicy,
    ThemeWatch,
    ThemeWatchEvent,
    Tick,
    WatchAlert,
    derive,
    is_terminal,
    realized_fraction,
    run_ticks,
    transition,
)

OPENED = date(2026, 1, 1)
POL = SurveillancePolicy()


# ── fixtures ─────────────────────────────────────────────────────────────────────────

def _horizon(window_days: int, label: str = "3m") -> ForwardHorizon:
    return ForwardHorizon(
        opened=OPENED,
        expected_close=date.fromordinal(OPENED.toordinal() + window_days),
        window_label=label, window_days=window_days)


def _falsifier(threshold: float = 20.0, direction: str = "below", buf: int = 3) -> FalsifierState:
    return FalsifierState(observable="PPI_minus_CPI_diff_bp", threshold=threshold,
                          direction=direction, breach_buffer=buf)


def _axis(current: float = 5.0, entry: float = 0.0, target: float = 100.0) -> AxisState:
    return AxisState(series="producer_minus_consumer_credit_diff_bp",
                     current=current, entry_level=entry, modeled_target=target)


def _watch(window_days: int = 91, *, last_evidence: date = OPENED,
           axis: AxisState | None = None, falsifier: FalsifierState | None = None) -> ThemeWatch:
    return ThemeWatch(
        theme_id="ppi-cpi-producer-consumer", snapshot_hash="sha256:deadbeef",
        forward_horizon=_horizon(window_days), falsifier=falsifier or _falsifier(),
        axis_state=axis or _axis(), last_evidence_date=last_evidence)


def _on(days_after: int) -> date:
    return date.fromordinal(OPENED.toordinal() + days_after)


def _read(days_after: int, metric: float) -> Tick:
    return Tick(now=_on(days_after), is_falsifier_read=True, metric_value=metric)


def _evidence(days_after: int, signed: float, *, attention: bool = False,
              valence: str = "confirming", bears_on: str = "driver") -> Tick:
    ev = ThemeWatchEvent(valence=valence, signed_valence=signed, bears_on=bears_on,  # type: ignore[arg-type]
                         timestamp=_on(days_after), is_attention_only=attention)
    return Tick(now=_on(days_after), is_evidence_event=True, event=ev)


# ── 1. whipsaw protection ──────────────────────────────────────────────────────────────

def test_1_whipsaw_one_breach_is_pending_then_unbreach_returns_and_logs():
    w = _watch(window_days=91)
    u1 = transition(w, _read(3, metric=15.0), POL)        # below 20 => breach
    assert u1.status == "falsified_pending" and not u1.terminal
    u2 = transition(w, _read(6, metric=25.0), POL)        # above 20 => clear
    assert u2.status == "armed"                            # back to prior health, not falsified
    assert any(e.kind == "whipsaw_averted" for e in w.log)
    assert w.consecutive_breach_count == 0


# ── 2. persisted breach => falsified (terminal) ─────────────────────────────────────────

def test_2_persisted_breach_reaches_terminal_falsified():
    w = _watch(window_days=91)
    transition(w, _read(3, 15.0), POL)
    transition(w, _read(10, 15.0), POL)
    u3 = transition(w, _read(17, 15.0), POL)              # 3 consecutive breaches == breach_buffer
    assert u3.status == "falsified" and u3.terminal
    assert w.falsifier.breached is True
    assert is_terminal(w.status)


# ── 3 & 4. dynamic staleness scales with the window ─────────────────────────────────────

def test_3_short_horizon_4_days_quiet_is_stalled():
    w = _watch(window_days=21)                            # 3w => stale_th ~3.15d
    u = transition(w, _read(4, metric=25.0), POL)         # non-breaching read, 4 days quiet
    assert u.status == "stalled"


def test_4_long_horizon_4_days_quiet_is_not_stalled():
    w = _watch(window_days=122)                           # 4m => stale_th ~18.3d
    u = transition(w, _read(4, metric=25.0), POL)
    assert u.status != "stalled"
    assert u.status == "armed"


# ── 5. price != thesis ───────────────────────────────────────────────────────────────────

def test_5_adverse_evidence_without_breach_is_weakening_never_exit():
    w = _watch(window_days=91, axis=_axis(current=-30.0))   # adverse axis move, far from target
    u = transition(w, _evidence(8, signed=-1.0, valence="disconfirming"), POL)
    assert u.status == "weakening" and not u.terminal
    assert w.falsifier.breached is False                     # falsifier never breached => no exit


# ── 6. confirmation-bias guard (by construction) ─────────────────────────────────────────

def test_6a_blind_context_forbids_the_conclusion_fields():
    assert set(BlindScoringContext.model_fields) == {"causal_chain", "operational_axis",
                                                     "new_source_atoms"}
    for forbidden in ("status", "lean", "pnl", "p_and_l", "trade_on", "conviction", "watch_history"):
        assert forbidden not in BlindScoringContext.model_fields
    with pytest.raises(ValidationError):                     # extra="forbid"
        BlindScoringContext(causal_chain="a->b->c", operational_axis="x",
                            status="confirming")              # type: ignore[call-arg]


def test_6b_disconfirm_asymmetry_tips_net_negative_on_equal_magnitudes():
    w = _watch(window_days=91)
    transition(w, _evidence(5, signed=+1.0, valence="confirming"), POL)
    transition(w, _evidence(5, signed=-1.0, valence="disconfirming"), POL)
    d = derive(w, _on(5), POL)
    assert d.net_valence < 0                                 # lambda_disconfirm > 1 => bear wins ties


# ── 7. attention != evidence ─────────────────────────────────────────────────────────────

def test_7_attention_only_flood_does_not_confirm():
    w = _watch(window_days=91)
    for day in (2, 3, 4):
        transition(w, _evidence(day, signed=+5.0, attention=True, valence="confirming"), POL)
    d = derive(w, _on(4), POL)
    assert d.net_valence == 0.0                              # excluded from net valence
    assert w.status != "confirming"


# ── 8. horizon expiry ────────────────────────────────────────────────────────────────────

def test_8_past_horizon_with_no_resolution_is_horizon_expired():
    w = _watch(window_days=21)
    u = transition(w, _read(29, metric=25.0), POL)          # elapsed 29 > 21, not played/falsified
    assert u.status == "horizon_expired" and u.terminal


# ── 9. played out ────────────────────────────────────────────────────────────────────────

def test_9_axis_target_reached_is_played_out():
    w = _watch(window_days=91, axis=_axis(current=80.0, entry=0.0, target=100.0))  # 80% >= 75%
    assert realized_fraction(w.axis_state) >= POL.axis_target_fraction
    u = transition(w, _read(10, metric=25.0), POL)
    assert u.status == "played_out" and u.terminal


def test_9b_played_out_wins_over_falsifier_wobble():
    # terminal priority: a realized thesis is a win even amid a breaching falsifier
    w = _watch(window_days=91, axis=_axis(current=80.0))
    transition(w, _read(3, 15.0), POL)                      # falsifier breaching
    u = transition(w, _read(10, 15.0), POL)
    assert u.status == "played_out"


# ── 10. firewall / additivity / no sizing ────────────────────────────────────────────────

def test_10_watch_is_additive_and_carries_no_sizing():
    w = _watch(window_days=91)
    before = w.snapshot_hash
    run_ticks(w, [_read(3, 15.0), _evidence(5, +1.0), _read(10, 25.0)], POL)
    assert w.snapshot_hash == before                        # frozen object binding never mutates
    # the only human-facing output is an epistemic alert — no legs/sizing fields exist
    assert set(WatchAlert.model_fields) == {"alert_type", "status", "message", "at"}
    for f in WatchAlert.model_fields:
        assert not any(bad in f for bad in ("size", "notional", "leg", "hedge", "stop"))


# ── 11. determinism ──────────────────────────────────────────────────────────────────────

def test_11_same_tick_sequence_same_path():
    ticks = [_read(3, 15.0), _read(10, 25.0), _evidence(12, -1.0, valence="disconfirming"),
             _read(17, 15.0)]
    a = _watch(window_days=91)
    b = _watch(window_days=91)
    pa = [u.status for u in run_ticks(a, ticks, POL)]
    pb = [u.status for u in run_ticks(b, ticks, POL)]
    assert pa == pb


# ── §9 simulator-faithfulness ────────────────────────────────────────────────────────────

def test_sim_breach_progression_pending_until_buffer_then_falsified():
    w = _watch(window_days=91)
    statuses = [transition(w, _read(7 * i, 15.0), POL).status for i in range(1, 4)]
    assert statuses == ["falsified_pending", "falsified_pending", "falsified"]


def test_sim_window_flip_changes_noise_to_stalled():
    # identical 4-day-quiet read; only the window differs
    short = transition(_watch(window_days=21), _read(4, 25.0), POL).status
    long = transition(_watch(window_days=122), _read(4, 25.0), POL).status
    assert short == "stalled" and long != "stalled"


def test_sim_terminal_is_absorbing():
    w = _watch(window_days=91, axis=_axis(current=80.0))
    transition(w, _read(3, 25.0), POL)                      # played_out
    assert w.status == "played_out"
    u = transition(w, _read(10, 15.0), POL)                 # further ticks are no-ops
    assert u.status == "played_out" and u.reason == "absorbing"
