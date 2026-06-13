"""ThemeMonitorAgent — drive a ThemeWatch over the pure surveillance core (Phase 3, §5.8).

Discovery-class: it answers "is the thesis still true?" and STOPS at a status + alert. It never
sizes, never adjusts a hedge ratio.

The valence scorer is **provider-generic** (the user directive): `ValenceScorer` is a Protocol with
a deterministic default; an Anthropic or OpenAI adapter implements the same one-method interface and
plugs in unchanged. The confirmation-bias guard (§5.7) is enforced by CONSTRUCTION: the scorer is
called with ONLY a `BlindScoringContext`, which structurally cannot carry the watch status, lean,
P&L, or whether a trade is on — so the scorer cannot rationalize toward the conclusion.

This module contains NO live API calls and NO wall-clock; `now` is always supplied.
"""
from __future__ import annotations

from typing import Optional, Protocol, runtime_checkable

from .schema import EvidenceAtom
from .surveillance import (
    BlindScoringContext,
    StatusUpdate,
    SurveillancePolicy,
    ThemeWatch,
    ThemeWatchEvent,
    Tick,
    WatchAlert,
    is_terminal,
    transition,
)


# ── the provider-generic scoring seam ────────────────────────────────────────────────

@runtime_checkable
class ValenceScorer(Protocol):
    """Score new evidence BLIND. Receives ONLY a BlindScoringContext (no status / P&L / trade-on).
    Returns a signed valence: > 0 supports the causal chain, < 0 undermines it. Implementations:
    the deterministic default below, or an Anthropic/OpenAI adapter running the §5.7 three-pass
    (disconfirm steelman, confirm steelman, deterministic adjudication)."""

    def score(self, ctx: BlindScoringContext) -> float: ...


# disconfirm/confirm keyword lexicons for the deterministic default (blind to thesis sign beyond the
# causal-chain text it is given). The real LLM scorer replaces this with a steelman protocol.
_CONFIRM_WORDS = ("widen", "widens", "widening", "supports", "confirms", "deteriorat", "pressure",
                  "compress", "compresses", "decompress", "dispersion", "stress", "worsen")
_DISCONFIRM_WORDS = ("narrow", "narrows", "tighten", "tightens", "improves", "recover", "recovers",
                     "stabilis", "stabiliz", "resilient", "eases", "abates", "fades", "contradict")


class DeterministicValenceScorer:
    """Default blind scorer: per-atom keyword tally. Deterministic; no API, no wall-clock. It sees
    only the BlindScoringContext — never the watch status."""

    def score(self, ctx: BlindScoringContext) -> float:
        net = 0.0
        for atom in ctx.new_source_atoms:
            text = (atom.claim or "").lower()
            net += sum(1.0 for w in _CONFIRM_WORDS if w in text)
            net -= sum(1.0 for w in _DISCONFIRM_WORDS if w in text)
        return net


# ── status → alert mapping (§5.8 step 5) ─────────────────────────────────────────────

def alert_for(watch: ThemeWatch, at) -> WatchAlert:
    """The single human-facing output. price ≠ thesis: an adverse axis move with the thesis intact
    is a `hold`, not an exit; a breaching falsifier is the exit. Instrument-broke (axis decay) is
    flagged distinctly from thesis-broke."""
    s = watch.status
    if watch.axis_state.decay_flag and not is_terminal(s):
        return WatchAlert(alert_type="axis_decay", status=s, at=at,
                          message="axis decoupled from thesis (instrument broke, not thesis)")
    mapping = {
        "armed": ("hold", "monitoring — nominal"),
        "confirming": ("hold", "evidence supports the thesis"),
        "weakening": ("hold", "thesis weakening but falsifier intact (price ≠ thesis)"),
        "stalled": ("stalled", "theme going quiet — no new evidence"),
        "falsified_pending": ("falsifier_approaching", "falsifier breaching — buffering"),
        "falsified": ("exit_signal", "falsifier confirmed — exit"),
        "horizon_expired": ("exit_signal", "horizon elapsed without resolution"),
        "played_out": ("priced_in", "thesis realized — check remaining edge"),
    }
    atype, msg = mapping[s]
    return WatchAlert(alert_type=atype, status=s, at=at, message=msg)  # type: ignore[arg-type]


# ── the agent ─────────────────────────────────────────────────────────────────────────

class ThemeMonitorAgent:
    """Drive a frozen, persisted theme's watch. The causal object is read-only; the watch is an
    additive annotation stream keyed to snapshot_hash (never mutates the frozen reasoning)."""

    def __init__(self, scorer: Optional[ValenceScorer] = None,
                 policy: Optional[SurveillancePolicy] = None) -> None:
        self.scorer: ValenceScorer = scorer or DeterministicValenceScorer()
        self.policy = policy or SurveillancePolicy()

    def score_blind(self, *, causal_chain: str, operational_axis: str,
                    atoms: list[EvidenceAtom]) -> float:
        """Build the BlindScoringContext (NO status) and score. The construction is the guard."""
        ctx = BlindScoringContext(causal_chain=causal_chain, operational_axis=operational_axis,
                                  new_source_atoms=atoms)
        return self.scorer.score(ctx)

    def observe(self, watch: ThemeWatch, *, atoms: list[EvidenceAtom], now,
                causal_chain: str, operational_axis: str, bears_on: str = "driver",
                is_attention_only: bool = False) -> tuple[StatusUpdate, WatchAlert]:
        """Ingest a new evidence event: blind-score it, append, run the transition, return the
        status update + the human alert. STOP."""
        signed = 0.0 if is_attention_only else self.score_blind(
            causal_chain=causal_chain, operational_axis=operational_axis, atoms=atoms)
        valence = ("neutral" if signed == 0 else "confirming" if signed > 0 else "disconfirming")
        event = ThemeWatchEvent(valence=valence, signed_valence=signed, bears_on=bears_on,  # type: ignore[arg-type]
                                timestamp=now, is_attention_only=is_attention_only,
                                evidence_atoms=list(atoms))
        upd = transition(watch, Tick(now=now, is_evidence_event=True, event=event), self.policy)
        alert = alert_for(watch, now)
        watch.alerts.append(alert)
        return upd, alert

    def read_falsifier(self, watch: ThemeWatch, *, metric_value: float, now
                       ) -> tuple[StatusUpdate, WatchAlert]:
        """Ingest a scheduled falsifier read, run the transition, return the update + alert. STOP."""
        upd = transition(watch, Tick(now=now, is_falsifier_read=True, metric_value=metric_value),
                         self.policy)
        alert = alert_for(watch, now)
        watch.alerts.append(alert)
        return upd, alert
