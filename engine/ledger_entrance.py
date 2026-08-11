"""SCAFFOLD — the entrance: a corpus document to ranked strategy families.

This is the missing arrow at each END of the seam. `engine/ledger_bridge.py` adapts a
projected theme to the discovery workflow; this module gets a projected theme in the
first place, and collects what comes out.

    doc_ids + corpus_dir
      → ledger.runner.forward_ingest        # blind Pass A → Pass B → cluster → admit
      → fold(events)                        # ONLY constructor of ThemeHypothesis (I5)
      → projection.to_theme_object          # ONLY status-axis mapping site (A3)
      → ledger_bridge.LedgerProvider
      → workflow.run_workflow(mode="discovery")
      → LedgerDiscoveryResult[]             # STOP

**The known break, stated here so no one rediscovers it in the debugger.**
`forward_ingest` returns a `RegistryState` of `AdmittedTheme(theme_id, status)` — a bare
id and a status STRING. It discards `AdmissionOutcome.created_event` and it never emits
a `STATUS_CHANGED` event for the themes it activates. So there is no event stream to
fold, and therefore no `ThemeHypothesis` to project. `hypotheses_from_registry` below is
where that gap is closed, and it cannot be closed without an additive change to
`runner.py` (plan task 1, BLOCKED B-06). Folding is not optional: `fold` is the sole
permitted construction site for a `ThemeHypothesis` (I5), so this module must not build
one directly from an `AdmissionOutcome`.

Determinism: no wall clock in this module (invariant I8). `as_of` is a parameter.
Persistence to the append-only event store is opt-in and off by default, so gates stay
deterministic and `recorded_at` keeps being stamped only inside the store (I7).

Discovery mode. Stops at ranked strategy families — no legs, no sizing, no hedge ratios.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence

from pydantic import BaseModel, ConfigDict

from .cases import PolicyConfig
from .ledger.projection import to_theme_object
from .ledger.runner import RegistryState, forward_ingest
from .ledger.substrate.fold import fold
from .ledger.substrate.hypothesis import ThemeDefinitionView, ThemeHypothesis
from .ledger.substrate.store import JsonlEventStore
from .ledger_bridge import LedgerProjectionNotRoutable, LedgerProvider
from .schema import ThemeObject
from .workflow import run_workflow


class LedgerIngestSpec(BaseModel):
    """What one entrance run needs. Everything explicit — nothing read from the clock."""

    model_config = ConfigDict(frozen=True)

    doc_ids: tuple[str, ...]
    corpus_dir: Path
    as_of: str                                    # ISO date; the projection's as-of
    existing_definitions: tuple[ThemeDefinitionView, ...] = ()
    persist_events: bool = False                  # opt-in append to the JSONL event store
    events_store: Optional[Path] = None           # required when persist_events is True


class LedgerDiscoveryResult(BaseModel):
    """One ledger theme, carried all the way through discovery.

    Deliberately a WRAPPER rather than new fields on `ThemeObject`: `ThemeObject` is a
    frozen model behind `firewall.freeze`, and a ledger id varies between two runs of
    otherwise identical reasoning, so adding it there would either change existing
    snapshot hashes or need another `_HASH_EXCLUDE` entry. The link belongs beside the
    object, not inside it.
    """

    model_config = ConfigDict(frozen=True)

    ledger_theme_id: str
    lifecycle_status: str                # ledger §Lifecycle — MARKET TRUTH axis
    projected: ThemeObject               # projection output — pipeline axis, set by projection.py
    routed: Optional[ThemeObject] = None # run_workflow output; None when refused
    memo: Optional[str] = None
    refused_reason: Optional[str] = None # why this theme never reached the workflow


def hypotheses_from_registry(
    state: RegistryState,
    *,
    as_of: str,
) -> list[ThemeHypothesis]:
    """Fold each admitted theme's event stream into a `ThemeHypothesis`.

    BLOCKED B-06 / plan task 1: `RegistryState` carries no events today. This function is
    the consumer that makes the additive `runner.py` change necessary and defines its
    shape — it needs, per admitted theme, the `CREATED` event plus a `STATUS_CHANGED`
    event whenever the activation gate fired, so that the folded status reproduces the
    status `forward_ingest` computed instead of restating it as a string.
    """
    hypotheses: list[ThemeHypothesis] = []
    for admitted in state.admitted:
        events = admitted.events()
        hyp = fold(events)
        if hyp is not None:
            hypotheses.append(hyp)
    return hypotheses


def project_all(
    hypotheses: Sequence[ThemeHypothesis],
    *,
    as_of: str,
) -> list[ThemeObject]:
    """Map each hypothesis through `projection.to_theme_object` — the ONLY mapping site."""
    return [to_theme_object(h, as_of=as_of) for h in hypotheses]


def run_ledger_discovery(
    spec: LedgerIngestSpec,
    policy: PolicyConfig,
) -> list[LedgerDiscoveryResult]:
    """The entrance. Corpus documents in, ranked strategy families out.

    Refusals are RESULTS, not exceptions: a theme projected as `blocked` (a dead ledger
    status) yields a `LedgerDiscoveryResult` with `routed=None` and a stated
    `refused_reason`. A run over five documents that routes two themes and refuses three
    must say so — silently returning two is how a gate stops being visible.
    """
    if spec is None:
        raise NotImplementedError("run_ledger_discovery requires a LedgerIngestSpec")

    state = forward_ingest(
        spec.doc_ids,
        spec.corpus_dir,
        spec.existing_definitions,
    )
    hypotheses = hypotheses_from_registry(state, as_of=spec.as_of)
    projected_objects = project_all(hypotheses, as_of=spec.as_of)

    results: list[LedgerDiscoveryResult] = []
    for h, projected in zip(hypotheses, projected_objects):
        status_str = h.status.value if hasattr(h.status, "value") else str(h.status)
        try:
            provider = LedgerProvider(projected)
            routed_theme, memo = run_workflow(provider, policy, mode="discovery")
            results.append(
                LedgerDiscoveryResult(
                    ledger_theme_id=h.theme_id,
                    lifecycle_status=status_str,
                    projected=projected,
                    routed=routed_theme,
                    memo=memo,
                    refused_reason=None,
                )
            )
        except LedgerProjectionNotRoutable as exc:
            results.append(
                LedgerDiscoveryResult(
                    ledger_theme_id=h.theme_id,
                    lifecycle_status=status_str,
                    projected=projected,
                    routed=None,
                    memo=None,
                    refused_reason=str(exc),
                )
            )

    if spec.persist_events:
        if spec.events_store is None:
            raise ValueError("events_store path is required when persist_events is True")
        store = JsonlEventStore(str(spec.events_store))
        for admitted in state.admitted:
            for event in admitted.events():
                store.append(event)

    return results
