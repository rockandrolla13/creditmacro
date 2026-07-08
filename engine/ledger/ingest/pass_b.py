"""Pass B — mapping claims to themes (ONTOLOGY §EvidenceLink, invariant I3).

Receives claims + ThemeDefinitionView(M, σ, X, H) ONLY — no ledger, no scores, no
status. Two-stage match: (1) structural pre-match on vocab node overlap +
market-variable compatibility, (2) semantic match → match_confidence. Claims whose
best confidence < τ_ORPHAN route to the orphan pool.

`polarity` is COMPUTED, never emitted by an LLM (I3):

    polarity = claim.direction × d(θ) × sign(X)

The sign(X) factor is required — an axis sign-convention flip inverts every polarity
(proven by test_axis_flip_remap), which is why AXIS_REVISED mandates a remap. The
ONTOLOGY §EvidenceLink shorthand "claim.direction × d(θ)" omits sign(X); see
SIGN_AUDIT.md / ONTOLOGY_DELTA D-07.

This module imports the DEFINITION view + the pure d(θ) formula + vocab only — never
the ledger stores or scoring (I3).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, Sequence

from .. import vocab
from ..constants import TAU_ORPHAN
from ..substrate.hypothesis import Mechanism, ThemeDefinitionView, derived_direction
from .claim import AtomicClaim
from .link import EvidenceLink


def _mechanism_nodes(m: Mechanism) -> set[str]:
    nodes: set[str] = set()
    for e in m.edges:
        nodes.add(e.v_from)
        nodes.add(e.v_to)
    return nodes


def structural_prematch(claim: AtomicClaim, definition: ThemeDefinitionView) -> bool:
    """claim.mechanism_tags ∩ nodes(M) ≠ ∅ AND market_variable compatible with vk or X."""
    nodes = _mechanism_nodes(definition.mechanism)
    tag_overlap = bool(set(claim.mechanism_tags) & nodes)
    variable_ok = claim.market_variable in (definition.operational_axis, definition.mechanism.vk)
    return tag_overlap and variable_ok


def match_confidence(claim: AtomicClaim, definition: ThemeDefinitionView) -> float:
    """Deterministic node-Jaccard (semantic-match seam; a real embedder lands per B-02)."""
    tags = set(claim.mechanism_tags)
    nodes = _mechanism_nodes(definition.mechanism)
    union = tags | nodes
    return len(tags & nodes) / len(union) if union else 0.0


def polarity(claim: AtomicClaim, definition: ThemeDefinitionView) -> int:
    """claim.direction × d(θ) × sign(X). Computed — never LLM-emitted (I3)."""
    return claim.direction * derived_direction(definition) * vocab.axis_sign(definition.operational_axis)


@dataclass(frozen=True)
class MapResult:
    links: list[EvidenceLink] = field(default_factory=list)
    orphans: list[AtomicClaim] = field(default_factory=list)


def _link_id(claim_id: str, theme_id: str, revision: int) -> str:
    return f"{claim_id}->{theme_id}@r{revision}"


class ThemeMapper(Protocol):
    def map(self, claims: Sequence[AtomicClaim], definitions: Sequence[ThemeDefinitionView],
            theme_revisions: dict[str, int]) -> "MapResult": ...


class StructuralSemanticMapper:
    """Structural pre-match then deterministic semantic score; τ_ORPHAN routing."""

    def map(self, claims: Sequence[AtomicClaim], definitions: Sequence[ThemeDefinitionView],
            theme_revisions: dict[str, int]) -> MapResult:
        links: list[EvidenceLink] = []
        orphans: list[AtomicClaim] = []
        for claim in claims:
            best: tuple[float, ThemeDefinitionView] | None = None
            for d in definitions:
                if not structural_prematch(claim, d):
                    continue
                conf = match_confidence(claim, d)
                if best is None or conf > best[0]:
                    best = (conf, d)
            if best is None or best[0] < TAU_ORPHAN:
                orphans.append(claim)
                continue
            conf, d = best
            rev = theme_revisions.get(d.theme_id, 0)
            links.append(EvidenceLink(
                link_id=_link_id(claim.claim_id, d.theme_id, rev),
                theme_id=d.theme_id, theme_revision=rev, claim_id=claim.claim_id,
                polarity=polarity(claim, d), match_confidence=conf,
            ))
        return MapResult(links=links, orphans=orphans)


def remap(prev_links: Sequence[EvidenceLink], claims: Sequence[AtomicClaim],
          definition: ThemeDefinitionView, *, theme_revision: int) -> list[EvidenceLink]:
    """AXIS_REVISED / MECHANISM_REVISED policy: supersede all prior links for the theme
    and re-run Pass B against the new definition (§Event link-policy). Each new link
    references the prior link it supersedes (matched by claim_id)."""
    prev_by_claim = {l.claim_id: l for l in prev_links if l.theme_id == definition.theme_id}
    fresh = StructuralSemanticMapper().map(claims, [definition], {definition.theme_id: theme_revision})
    out: list[EvidenceLink] = []
    for l in fresh.links:
        prior = prev_by_claim.get(l.claim_id)
        out.append(l.model_copy(update={"supersedes": prior.link_id if prior else None}))
    return out
