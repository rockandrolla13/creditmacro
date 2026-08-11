"""Orphan clustering + admission (ONTOLOGY §Admission). Forward-reingest keystone.

Cluster orphan claims by shared in-vocab mechanism tag; a cluster is admitted iff
|claims| ≥ N_MIN ∧ |institutions| ≥ I_MIN ∧ span ≤ W_ADMIT. Admission synthesizes a
CandidateTheme over the vocab (deterministic rule below), passes it through WF, and
emits founding EvidenceLinks (the clustered claims ARE the theme's evidence). Out-of-
vocab modal tag → review queue (never auto-added).

Synthesis rule (deterministic; ONTOLOGY leaves it heuristic — see ONTOLOGY_DELTA D-08):
mechanism = top-2 modal in-vocab tags → SYNTH_VK, signs +1; σ = sign(Σ claim.direction);
X = modal market_variable; H = min horizon; F = synthesized. theme_id = admitted:<a>-<b>.
Σ claim.direction = 0 yields sign 0, which is not a legal σ ∈ {+1, −1} (§Theme): the
cluster is CONTESTED and routes to needs_structuring, never to a synthesized direction
(ONTOLOGY_DELTA D-11).
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from typing import Optional, Sequence

from .. import vocab
from ..constants import I_MIN, N_MIN, W_ADMIT
from ..substrate.events import EventType, Provenance, ThemeEvent
from ..substrate.hypothesis import Mechanism, ThemeDefinitionView, TransmissionEdge
from ..substrate.identity import wf_predicate
from .claim import AtomicClaim
from .link import EvidenceLink
from .pass_b import polarity

SYNTH_VK = "credit_spread"     # canonical terminal node for synthesized chains


@dataclass(frozen=True)
class OrphanCluster:
    claims: tuple[AtomicClaim, ...]

    @property
    def institutions(self) -> set[str]:
        return {c.source_institution for c in self.claims}

    @property
    def span_days(self) -> int:
        dates = [date.fromisoformat(c.doc_date[:10]) for c in self.claims]
        return (max(dates) - min(dates)).days

    def tag_freq(self) -> Counter:
        return Counter(t for c in self.claims for t in c.mechanism_tags)


@dataclass(frozen=True)
class SynthesizedCandidate:
    """Satisfies substrate.hypothesis.ThemeShape — WF validates it pre-fold (I5-safe)."""
    mechanism: Mechanism
    shock_direction: int
    operational_axis: str
    horizon_days: int
    falsifier: str


@dataclass(frozen=True)
class AdmissionOutcome:
    status: str                                   # admitted | rejected_gate | needs_structuring | out_of_vocab
    theme_id: Optional[str] = None
    definition: Optional[ThemeDefinitionView] = None
    created_event: Optional[ThemeEvent] = None
    founding_links: tuple[EvidenceLink, ...] = ()
    review_tags: tuple[str, ...] = ()
    reason: str = ""


def cluster_orphans(orphans: Sequence[AtomicClaim]) -> list[OrphanCluster]:
    """Connected components by shared in-vocab mechanism tag (deterministic)."""
    parent = {c.claim_id: c.claim_id for c in orphans}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)     # smaller id as root → stable

    tag_rep: dict[str, str] = {}
    for c in orphans:
        for t in c.mechanism_tags:
            if not vocab.is_node(t):
                continue
            if t in tag_rep:
                union(c.claim_id, tag_rep[t])
            else:
                tag_rep[t] = c.claim_id

    groups: dict[str, list[AtomicClaim]] = defaultdict(list)
    for c in orphans:
        groups[find(c.claim_id)].append(c)

    clusters = [
        OrphanCluster(claims=tuple(sorted(g, key=lambda c: c.claim_id)))
        for g in groups.values()
    ]
    return sorted(clusters, key=lambda cl: cl.claims[0].claim_id)


def admit(cluster: OrphanCluster) -> AdmissionOutcome:
    claims = cluster.claims
    if len(claims) < N_MIN or len(cluster.institutions) < I_MIN or cluster.span_days > W_ADMIT.days:
        return AdmissionOutcome(status="rejected_gate", reason="admission gate")

    freq = cluster.tag_freq()
    modal_sorted = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
    if not modal_sorted or not vocab.is_node(modal_sorted[0][0]):
        oov = tuple(sorted(t for t in freq if not vocab.is_node(t)))
        return AdmissionOutcome(status="out_of_vocab", review_tags=oov, reason="modal tag out of vocabulary")

    in_vocab_modal = [t for t, _ in modal_sorted if vocab.is_node(t)]
    if len(in_vocab_modal) < 2:
        return AdmissionOutcome(status="needs_structuring", reason="fewer than 2 distinct in-vocab tags (k<2)")

    # σ = sign(Σ direction). A cluster whose directions cancel exactly is CONTESTED:
    # the evidence supports no σ ∈ {+1, −1}, and §Theme forbids representing "the
    # market disagrees" as a direction. Breaking the tie toward +1 would invent a
    # bullish theme out of a directionless one, silently. Route it for structuring.
    net_direction = sum(c.direction for c in claims)
    if net_direction == 0:
        return AdmissionOutcome(
            status="needs_structuring",
            reason="contested cluster: Σ claim.direction == 0, no σ ∈ {+1,-1} supported",
        )
    sigma = 1 if net_direction > 0 else -1

    a, b = in_vocab_modal[0], in_vocab_modal[1]
    mechanism = Mechanism(edges=(
        TransmissionEdge(v_from=a, v_to=b, sign=1),
        TransmissionEdge(v_from=b, v_to=SYNTH_VK, sign=1),
    ))
    axis = Counter(c.market_variable for c in claims).most_common(1)[0][0]
    horizon = min(c.horizon_days for c in claims)
    falsifier = f"synthesized: axis {axis} fails to track the {a} channel over the horizon"

    candidate = SynthesizedCandidate(mechanism, sigma, axis, horizon, falsifier)
    wf = wf_predicate(candidate)
    if not wf.ok:
        return AdmissionOutcome(status="needs_structuring", reason=f"WF clause {wf.failing_clause}")

    theme_id = f"admitted:{a}-{b}"
    definition = ThemeDefinitionView(
        theme_id=theme_id, mechanism=mechanism, shock_direction=sigma,
        operational_axis=axis, horizon_days=horizon,
    )
    effective_at = max(c.doc_date for c in claims)
    created = ThemeEvent(
        event_id=f"{theme_id}:created", theme_id=theme_id, event_type=EventType.CREATED,
        payload={"mechanism": mechanism.model_dump(), "shock_direction": sigma,
                 "operational_axis": axis, "horizon_days": horizon, "falsifier": falsifier},
        effective_at=effective_at, provenance=Provenance.ORPHAN_PROMOTION,
    )
    founding = tuple(
        EvidenceLink(
            link_id=f"{c.claim_id}->{theme_id}@r1", theme_id=theme_id, theme_revision=1,
            claim_id=c.claim_id, polarity=polarity(c, definition), match_confidence=1.0,
        )
        for c in claims
    )
    return AdmissionOutcome(status="admitted", theme_id=theme_id, definition=definition,
                            created_event=created, founding_links=founding)
