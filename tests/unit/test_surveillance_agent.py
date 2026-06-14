"""S9 — ThemeMonitorAgent: drive a watch with a provider-generic blind scorer.

Asserts the agent maps the pure core to status updates + human alerts, that the blind scorer is
called with ONLY a BlindScoringContext (no status / lean / P&L), and that the provider-generic seam
accepts an injected scorer (Anthropic/OpenAI plug in the same way).
"""
from __future__ import annotations

from datetime import date

from engine.schema import EvidenceAtom
from engine.surveillance import (
    AxisState,
    BlindScoringContext,
    FalsifierState,
    ForwardHorizon,
    SurveillancePolicy,
    ThemeWatch,
)
from engine.surveillance_agent import (
    DeterministicValenceScorer,
    ThemeMonitorAgent,
    ValenceScorer,
    alert_for,
)

OPENED = date(2026, 1, 1)


def _on(d):
    return date.fromordinal(OPENED.toordinal() + d)


def _watch(window_days=91, *, decay=False):
    return ThemeWatch(
        theme_id="ppi-cpi", snapshot_hash="sha256:abc",
        forward_horizon=ForwardHorizon(opened=OPENED, expected_close=_on(window_days),
                                       window_label="3m", window_days=window_days),
        falsifier=FalsifierState(observable="ppi_minus_cpi", threshold=20.0, direction="below"),
        axis_state=AxisState(series="diff", current=5.0, entry_level=0.0, modeled_target=100.0,
                             decay_flag=decay),
        last_evidence_date=OPENED)


def _atoms(claim):
    return [EvidenceAtom(evidence_id="e1", source_slug="s", claim=claim)]


CH, AX = "margin compression -> producer spread widening", "ppi_minus_cpi"


def test_confirming_evidence_routes_confirming_with_hold_alert():
    agent = ThemeMonitorAgent()
    upd, alert = agent.observe(_watch(), atoms=_atoms("producer spreads widen on margin pressure"),
                               now=_on(3), causal_chain=CH, operational_axis=AX)
    assert upd.status == "confirming"
    assert alert.alert_type == "hold"


def test_disconfirming_evidence_routes_weakening_not_exit():
    agent = ThemeMonitorAgent()
    upd, alert = agent.observe(_watch(), atoms=_atoms("the differential tightens as margins recover"),
                               now=_on(3), causal_chain=CH, operational_axis=AX)
    assert upd.status == "weakening" and not upd.terminal
    assert alert.alert_type == "hold"          # price≠thesis: weakening is a hold, never an exit


def test_attention_only_does_not_confirm():
    agent = ThemeMonitorAgent()
    w = _watch()
    upd, _ = agent.observe(w, atoms=_atoms("everyone is talking about producer spreads widening"),
                           now=_on(2), causal_chain=CH, operational_axis=AX, is_attention_only=True)
    assert upd.status != "confirming"


def test_falsifier_persistence_reaches_exit_signal():
    agent = ThemeMonitorAgent()
    w = _watch()
    u1, a1 = agent.read_falsifier(w, metric_value=15.0, now=_on(7))
    assert u1.status == "falsified_pending" and a1.alert_type == "falsifier_approaching"
    agent.read_falsifier(w, metric_value=15.0, now=_on(14))
    u3, a3 = agent.read_falsifier(w, metric_value=15.0, now=_on(21))
    assert u3.status == "falsified" and u3.terminal and a3.alert_type == "exit_signal"


def test_played_out_alert_is_priced_in():
    agent = ThemeMonitorAgent()
    w = _watch()
    w.axis_state.current = 80.0                       # 80% of target
    _, alert = agent.read_falsifier(w, metric_value=25.0, now=_on(10))
    assert w.status == "played_out" and alert.alert_type == "priced_in"


def test_axis_decay_alert_distinct_from_thesis_break():
    w = _watch(decay=True)
    w.status = "confirming"
    alert = alert_for(w, _on(5))
    assert alert.alert_type == "axis_decay"


# ── the confirmation-bias guard, by construction ─────────────────────────────────────

class _SpyScorer:
    def __init__(self):
        self.seen = []

    def score(self, ctx):
        self.seen.append(ctx)
        return 1.0


def test_scorer_sees_only_blind_context_no_status():
    spy = _SpyScorer()
    agent = ThemeMonitorAgent(scorer=spy)
    w = _watch()
    w.status = "weakening"                            # a conclusion the scorer must NOT see
    agent.observe(w, atoms=_atoms("producer spreads widen"), now=_on(3),
                  causal_chain=CH, operational_axis=AX)
    assert len(spy.seen) == 1
    ctx = spy.seen[0]
    assert isinstance(ctx, BlindScoringContext)
    assert set(type(ctx).model_fields) == {"causal_chain", "operational_axis", "new_source_atoms"}
    assert not hasattr(ctx, "status")


def test_provider_generic_scorer_is_injectable():
    # any object implementing ValenceScorer.score plugs in (Anthropic/OpenAI adapter, etc.)
    class _AlwaysBear:
        def score(self, ctx):
            return -5.0
    assert isinstance(_AlwaysBear(), ValenceScorer)   # structural Protocol check
    agent = ThemeMonitorAgent(scorer=_AlwaysBear())
    upd, _ = agent.observe(_watch(), atoms=_atoms("anything"), now=_on(3),
                           causal_chain=CH, operational_axis=AX)
    assert upd.status == "weakening"


def test_default_scorer_is_deterministic():
    s = DeterministicValenceScorer()
    ctx = BlindScoringContext(causal_chain=CH, operational_axis=AX,
                              new_source_atoms=_atoms("spreads widen and dispersion rises"))
    assert s.score(ctx) == s.score(ctx) > 0
