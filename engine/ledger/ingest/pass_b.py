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

import os
from dataclasses import dataclass, field
from typing import Callable, Protocol, Sequence

from .. import vocab
from ..constants import TAU_ORPHAN
from ..llm_json import LEDGER_MODEL, extract_text, parse_json_object
from ..substrate.hypothesis import Mechanism, ThemeDefinitionView, derived_direction
from .claim import AtomicClaim
from .link import EvidenceLink
from .prompts.pass_b_match import MATCH_PROMPT, MATCH_SYSTEM

LIVE_ENV_FLAG = "ALLOW_LIVE_LLM_DISCOVERY"

# A semantic scorer maps (claim, definition) → confidence in [0,1]. The default is
# the deterministic node-Jaccard; LLMMatchScorer is the live Anthropic seam.
Scorer = Callable[[AtomicClaim, ThemeDefinitionView], float]


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


class LLMMatchScorer:
    """Semantic match confidence via the Anthropic Messages API (B-01).

    Sees the ThemeDefinitionView (mechanism nodes + axis) and the claim ONLY (I3);
    it is never asked for a direction/polarity. Real client built under the opt-in.
    """

    def __init__(self, client=None, *, model: str = LEDGER_MODEL, max_tokens: int = 256) -> None:
        self._client = client
        self._model = model
        self._max_tokens = max_tokens

    def _get_client(self):
        if self._client is None:
            if os.environ.get(LIVE_ENV_FLAG) != "1":
                raise RuntimeError(f"live LLM not enabled (set {LIVE_ENV_FLAG}=1)")
            import anthropic
            self._client = anthropic.Anthropic()
        return self._client

    def score(self, claim: AtomicClaim, definition: ThemeDefinitionView) -> float:
        user = MATCH_PROMPT.format(
            nodes=", ".join(sorted(_mechanism_nodes(definition.mechanism))),
            axis=definition.operational_axis, market_variable=claim.market_variable,
            tags=", ".join(claim.mechanism_tags), text=claim.text,
        )
        response = self._get_client().messages.create(
            model=self._model, max_tokens=self._max_tokens, system=MATCH_SYSTEM,
            messages=[{"role": "user", "content": user}],
        )
        return float(parse_json_object(extract_text(response))["match_confidence"])


class StructuralSemanticMapper:
    """Structural pre-match then semantic score; τ_ORPHAN routing.

    `scorer` defaults to the deterministic node-Jaccard `match_confidence`; inject
    `LLMMatchScorer(...).score` for the live semantic stage.
    """

    def __init__(self, scorer: Scorer = match_confidence) -> None:
        self._scorer = scorer

    def map(self, claims: Sequence[AtomicClaim], definitions: Sequence[ThemeDefinitionView],
            theme_revisions: dict[str, int]) -> MapResult:
        links: list[EvidenceLink] = []
        orphans: list[AtomicClaim] = []
        for claim in claims:
            best: tuple[float, ThemeDefinitionView] | None = None
            for d in definitions:
                if not structural_prematch(claim, d):
                    continue
                conf = self._scorer(claim, d)
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
