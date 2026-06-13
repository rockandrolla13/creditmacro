"""Theme surveillance core — watch a confirmed, frozen theme while trades are on.

This is the deterministic heart of Phase 3. It is a faithful Python realization of the reference
simulator (`theme_surveillance_simulator.html`) and of §5.3 of `SURVEILLANCE_BUILD_PLAN.md`: the
prioritized state-transition function plus the three guardrails (breach buffer, horizon-keyed
dynamic staleness, disconfirmation asymmetry).

DISCIPLINE (enforced here):
  * Surveillance is **discovery-class**: it answers "is the thesis still true?" and STOPS at a
    status + alert. It NEVER sizes, never adjusts a hedge ratio, never emits legs.
  * Deterministic: no wall clock. Every tick carries its own `now` (caller-supplied).
  * The frozen causal object is never mutated; a `ThemeWatch` is an additive annotation stream
    keyed to `snapshot_hash` (the same shape as `PostCaseCalibration`).
  * Terminal states are absorbing.

The module is intentionally free of I/O and of any engine import that could couple it to the
golden-master path. `ThemeMonitorAgent` (a separate module) wires it to extraction + persistence.
"""
from __future__ import annotations

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from .schema import EvidenceAtom
from .schema.horizon import ForwardHorizon  # canonical definition; re-exported here

# ── status taxonomy (§5.2) ──────────────────────────────────────────────────────────

WatchStatus = Literal[
    # non-terminal (active monitoring)
    "armed", "confirming", "weakening", "stalled", "falsified_pending",
    # terminal (absorbing)
    "falsified", "horizon_expired", "played_out",
]

_TERMINAL: frozenset[str] = frozenset({"falsified", "horizon_expired", "played_out"})


def is_terminal(status: str) -> bool:
    return status in _TERMINAL


# ForwardHorizon (§3.2) is defined in engine.schema.horizon (a leaf module, so ThemeObject can also
# import it without a cycle) and re-exported above.


# ── policy (§5.4 — defaults verbatim) ────────────────────────────────────────────────

class SurveillancePolicy(BaseModel):
    # Guardrail 1 — breach buffer
    breach_buffer: int = 3          # consecutive qualifying reads to confirm falsification
    breach_obs_freq: str = "weekly"  # the read cadence the buffer counts in
    breach_mode: Literal["consecutive", "integral"] = "consecutive"  # §10 Q1 default
    # Guardrail 2 — horizon-keyed dynamics
    k_stale: float = 0.15           # staleness threshold = k_stale * window_days
    stale_floor: int = 2
    stale_cap: int = 30
    k_decay: float = 0.25           # evidence half-life = k_decay * window_days
    decay_floor: int = 3
    decay_cap: int = 45
    # Guardrail 3 — disconfirmation asymmetry
    lambda_disconfirm: float = 1.5  # disconfirming evidence weighted >= confirming
    # health dead-band + win threshold
    valence_band: float = 0.5       # |net_val| <= band stays armed (no flicker)
    axis_target_fraction: float = 0.75  # fraction of modeled target move => played_out


# ── falsifier (§5.5) ─────────────────────────────────────────────────────────────────

class FalsifierState(BaseModel):
    observable: str                                   # e.g. "PPI_minus_CPI_diff_bp"
    threshold: float                                  # X
    direction: Literal["below", "above"]
    breach_buffer: int = 3
    current_value: Optional[float] = None
    distance_to_threshold: Optional[float] = None     # signed; for the "how close" alert
    consecutive_breach_count: int = 0
    breached: bool = False                            # True only when the buffer has elapsed


# ── axis (§5.8) ──────────────────────────────────────────────────────────────────────

class AxisState(BaseModel):
    series: str
    current: float
    entry_level: float
    modeled_target: float                             # from discovery scenario FV (NOT a trade level)
    realized_move: Optional[float] = None
    direction_vs_thesis: Literal["with", "against", "flat"] = "flat"
    decay_flag: bool = False                          # regime shift / index recomposition decoupled it


def realized_fraction(axis: AxisState) -> float:
    """|move| / |modeled target move|, guarded against a zero-width target. The simulator drives
    this directly as `axisFrac`; here we derive it from the axis levels so the agent can compute it
    from a real series."""
    target_move = axis.modeled_target - axis.entry_level
    if target_move == 0:
        return 0.0
    move = axis.realized_move if axis.realized_move is not None else (axis.current - axis.entry_level)
    return abs(move) / abs(target_move)


# ── events / alerts / log (§5.8) ─────────────────────────────────────────────────────

EvidenceValence = Literal["confirming", "disconfirming", "neutral", "falsifying"]
BearsOn = Literal["driver", "transmission", "outcome", "falsifier", "axis"]


class ThemeWatchEvent(BaseModel):
    """One scored monitoring event. `signed_valence` is the BLIND-scored magnitude (§5.7); the
    scorer never saw the watch status. `is_attention_only` (news flood, no new atoms) cannot raise
    conviction — it is excluded from net valence."""
    valence: EvidenceValence
    signed_valence: float
    bears_on: BearsOn
    timestamp: date
    is_attention_only: bool = False
    source_slug: Optional[str] = None
    evidence_atoms: list[EvidenceAtom] = Field(default_factory=list)


AlertType = Literal[
    "hold", "falsifier_approaching", "exit_signal", "stalled", "axis_decay", "priced_in",
]


class WatchAlert(BaseModel):
    """The ONLY output to the human. No legs, no sizing — an epistemic alert only."""
    alert_type: AlertType
    status: WatchStatus
    message: str
    at: date


class WatchLogEntry(BaseModel):
    """Audit trail: whipsaw_averted, transitions, decay flags."""
    kind: str
    reason: str
    at: date
    detail: dict = Field(default_factory=dict)


# ── blind scoring context (§5.7) — confirmation-bias guard by construction ───────────

class BlindScoringContext(BaseModel):
    """The ONLY thing the valence scorer sees. `extra="forbid"` makes it structurally impossible to
    add the conclusion the scorer might be tempted to justify (current status, lean, P&L, whether a
    trade is on, prior conviction, watch history). Acceptance test 6 asserts these are absent."""
    model_config = ConfigDict(extra="forbid")

    causal_chain: str                # driver -> transmission -> outcome (rendered mechanism)
    operational_axis: str            # the named series
    new_source_atoms: list[EvidenceAtom] = Field(default_factory=list)


# ── the watch object (§5.8) ──────────────────────────────────────────────────────────

class ThemeWatch(BaseModel):
    theme_id: str
    snapshot_hash: str                                # binds to the FROZEN causal object; never mutates it
    status: WatchStatus = "armed"
    forward_horizon: ForwardHorizon
    falsifier: FalsifierState
    axis_state: AxisState
    last_evidence_date: date
    events: list[ThemeWatchEvent] = Field(default_factory=list)
    consecutive_breach_count: int = 0
    breach_started_at: Optional[date] = None
    alerts: list[WatchAlert] = Field(default_factory=list)        # OUTPUT to human; no legs/sizing
    log: list[WatchLogEntry] = Field(default_factory=list)


# ── tick + result ────────────────────────────────────────────────────────────────────

class Tick(BaseModel):
    """One surveillance step: a falsifier read (scheduled) OR an evidence event. `now` is supplied
    (determinism)."""
    now: date
    is_falsifier_read: bool = False
    metric_value: Optional[float] = None
    is_evidence_event: bool = False
    event: Optional[ThemeWatchEvent] = None


class Derived(BaseModel):
    H: int
    elapsed: int
    stale_threshold: float
    half_life: float
    quiet: int
    net_valence: float
    axis_done: float


class StatusUpdate(BaseModel):
    status: WatchStatus
    reason: str
    terminal: bool


# ── pure helpers (mirror the simulator) ──────────────────────────────────────────────

def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _is_breach(value: float, threshold: float, direction: str) -> bool:
    return value < threshold if direction == "below" else value > threshold


def _days(a: date, b: date) -> int:
    """Whole days from b to a (a - b). Caller-supplied dates only — no wall clock."""
    return (a - b).days


def derive(w: ThemeWatch, now: date, pol: SurveillancePolicy) -> Derived:
    """All horizon-keyed derived quantities (Guardrail 2). Mirrors the simulator `derive()`:
    attention-only events are excluded from net valence; confirming/disconfirming events decay with
    recency (half-life keyed to the window) and disconfirming events carry the asymmetry weight."""
    H = w.forward_horizon.window_days
    stale_threshold = _clamp(pol.k_stale * H, pol.stale_floor, pol.stale_cap)
    half_life = _clamp(pol.k_decay * H, pol.decay_floor, pol.decay_cap)
    quiet = _days(now, w.last_evidence_date)
    net = 0.0
    for e in w.events:
        if e.is_attention_only:                       # attention != evidence
            continue
        weight = 0.5 ** (_days(now, e.timestamp) / half_life)         # recency decay
        lam = pol.lambda_disconfirm if e.signed_valence < 0 else 1.0  # disconfirm asymmetry
        net += e.signed_valence * weight * lam
    return Derived(
        H=H, elapsed=_days(now, w.forward_horizon.opened),
        stale_threshold=stale_threshold, half_life=half_life, quiet=quiet,
        net_valence=net, axis_done=realized_fraction(w.axis_state),
    )


# ── the transition function (§5.3 — single source of truth) ──────────────────────────

def transition(w: ThemeWatch, tick: Tick, pol: SurveillancePolicy) -> StatusUpdate:
    """Ingest the tick into `w` (raw state), derive, then route by priority (FIRST match wins).
    Mutates `w` (the additive watch state) but NEVER the frozen causal object. Terminal states are
    absorbing: a tick on an already-terminal watch is a no-op."""
    if is_terminal(w.status):
        return StatusUpdate(status=w.status, reason="absorbing", terminal=True)

    # ---- 1. ingest the tick, update raw state variables ----
    if tick.is_falsifier_read and tick.metric_value is not None:
        breaching = _is_breach(tick.metric_value, w.falsifier.threshold, w.falsifier.direction)
        if breaching:
            w.consecutive_breach_count += 1
            if w.breach_started_at is None:
                w.breach_started_at = tick.now
        else:
            if w.consecutive_breach_count > 0:                       # Guardrail 1: whipsaw averted
                w.log.append(WatchLogEntry(
                    kind="whipsaw_averted", reason="falsifier un-breached before buffer elapsed",
                    at=tick.now, detail={"count": w.consecutive_breach_count}))
            w.consecutive_breach_count = 0
            w.breach_started_at = None
        # reflect the read on the falsifier state (signed distance for the "how close" alert)
        w.falsifier.current_value = tick.metric_value
        if w.falsifier.direction == "below":
            w.falsifier.distance_to_threshold = tick.metric_value - w.falsifier.threshold
        else:
            w.falsifier.distance_to_threshold = w.falsifier.threshold - tick.metric_value
        w.falsifier.consecutive_breach_count = w.consecutive_breach_count

    if tick.is_evidence_event and tick.event is not None:
        w.events.append(tick.event)                                 # valence was scored BLIND
        if not tick.event.is_attention_only:                        # attention does NOT reset staleness
            w.last_evidence_date = tick.now

    # ---- 2. derive (all horizon-keyed; Guardrail 2) ----
    d = derive(w, tick.now, pol)

    # ---- 3. prioritized routing (FIRST match wins) ----
    def terminal(status: str, reason: str) -> StatusUpdate:
        w.status = status  # type: ignore[assignment]
        if status == "falsified":
            w.falsifier.breached = True
        w.log.append(WatchLogEntry(kind="transition", reason=reason, at=tick.now,
                                   detail={"status": status, "terminal": True}))
        return StatusUpdate(status=status, reason=reason, terminal=True)  # type: ignore[arg-type]

    def active(status: str, reason: str) -> StatusUpdate:
        w.status = status  # type: ignore[assignment]
        return StatusUpdate(status=status, reason=reason, terminal=False)  # type: ignore[arg-type]

    if d.axis_done >= pol.axis_target_fraction:
        return terminal("played_out", "axis_target_reached")
    if w.consecutive_breach_count >= w.falsifier.breach_buffer:         # Guardrail 1 (confirmed)
        return terminal("falsified", "falsifier_persisted")
    if d.elapsed > d.H:
        return terminal("horizon_expired", "horizon_elapsed")
    if w.consecutive_breach_count >= 1:                                 # Guardrail 1 (pending)
        return active("falsified_pending", "falsifier_breaching_buffering")
    if d.quiet > d.stale_threshold:                                     # Guardrail 2
        return active("stalled", "evidence_stale")
    if d.net_valence < -pol.valence_band:
        return active("weakening", "valence_negative")
    if d.net_valence > pol.valence_band:
        return active("confirming", "valence_positive")
    return active("armed", "nominal")


def run_ticks(w: ThemeWatch, ticks: list[Tick], pol: SurveillancePolicy) -> list[StatusUpdate]:
    """Drive a watch through a tick sequence, returning the status path. Deterministic: same ticks →
    same path. Stops mutating once terminal (absorbing)."""
    return [transition(w, t, pol) for t in ticks]
