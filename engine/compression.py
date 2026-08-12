"""ThemeCompressionAgent — the analyst layer (docs/THEME_DISCIPLINE_AND_FAILURE_MODES.md).

    MultiSourceThemeAggregator  →  [ ThemeCompressionAgent ]  →  discovery handoff
       (flat ThemeClusters)         (AnalystThemeMap: parent/subtheme,
                                     coverage matrix, readout)

The aggregator is a RECALL stage: it surfaces every candidate it can find, flat and
near-duplicated. This is the PRECISION stage. A human analyst does not want forty themes;
they want three to seven parent themes, each with its subthemes, mechanism, evidence,
falsifier and a stated reason it was selected — plus an explicit account of what was
demoted and why.

Structure of the pass (all of it deterministic; see the LLM seam note below):

  1. SCREEN    — the six downgrade rules. Attention without evidence, no axis, no causal
                 chain, only source opinion, historical forecast without an outcome check,
                 or no falsifier ⇒ FORCED to watchlist regardless of attention score.
                 Historical-only themes route to outcome candidates, never to promotion.
  2. GROUP     — cluster the survivors by DRIVER, not by tokens.
  3. MERGE     — inside a group, two themes sharing driver + mechanism + outcome + axis +
                 family collapse into one. Themes sharing only the driver stay apart as
                 SUBTHEMES of one parent — not merged, not separate parents.
  4. CAP       — keep the top `parent_cap` groups (default 7); the tail is demoted, logged,
                 never dropped.
  5. SYNTHESIS — name the parent theme and write its mechanism. This is the ONLY generative
                 step, and it sits behind the `ThemeSynthesizer` protocol seam.
  6. GATE      — the promotion gate. Evidence + mechanism + axis-or-watchlist + falsifier +
                 temporal status + ≥1 routable family + selection rationale. Every proposal
                 must also cite REAL evidence ids from its own group: a theme the model
                 invents with nothing behind it is rejected here, with a reason.
  7. RENDER    — coverage matrix + the human readout, both no-trade guarded.

DISCIPLINE. A theme is the CAUSAL STORY; the direction of expression is a different output
and belongs to a later stage. A parent-theme name that carries a direction or an instrument
is rejected. No legs, sizes, hedge ratios or execution reach the map or the readout — the
guard is `engine.wiki_integration`'s, reused rather than rewritten.

DETERMINISM. No wall clock, no set iteration, stable sort keys everywhere. The same
`MultiSourceThemeSet` and the same policy produce a byte-identical `AnalystThemeMap`.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict

from .schema.compression import (
    AnalystThemeMap,
    CausalMechanism,
    CompressionStats,
    CoverageCell,
    CoverageRow,
    DemotedTheme,
    EvidenceBySource,
    ParentTheme,
    SourceCoverageMatrix,
    Subtheme,
    ThemeFalsifier,
)
from .schema.theme_aggregation import (
    ROUTABLE_FAMILIES,
    MultiSourceThemeSet,
    ThemeCluster,
)
# The no-trade guard is the WikiIntegrator's, imported rather than reimplemented — one
# lexicon, one place to fix it.
from .wiki_integration import _trade_hit


class CompressionDisciplineError(RuntimeError):
    """Raised when a discipline invariant the agent is supposed to guarantee is violated
    on the way OUT (e.g. trade language survived into the readout). Never raised for bad
    INPUT — bad input is demoted with a reason, which is the whole point of this stage."""


# ── local text helpers ───────────────────────────────────────────────────────
# Deliberately local rather than imported from engine.theme_aggregation: this stage consumes
# the aggregator's OUTPUT contract, not its internals, so a rewrite of its clustering cannot
# silently change how parents are grouped here.

_STOPWORDS = frozenset({
    "the", "a", "an", "is", "are", "of", "to", "too", "in", "on", "and", "or", "vs",
    "for", "by", "with", "up", "down", "into", "as", "at", "be", "it", "its", "this",
    "that", "from", "not", "but", "than", "have", "has",
})

#: Words that name a DIRECTION OF EXPRESSION or an instrument. A theme is the causal story;
#: if one of these appears in a proposed parent-theme name, the name is describing the trade,
#: not the theme, and the proposal is rejected.
_DIRECTION_WORDS = frozenset({
    "long", "short", "buy", "buying", "sell", "selling", "overweight", "underweight",
    "receive", "receiver", "payer", "pay", "steepener", "flattener", "bullish", "bearish",
    "add", "trim", "hedge", "hedged", "position", "trade", "leg", "size", "sized",
})

_ARROW = re.compile(r"\s*(?:→|->|=>|➔)\s*")
_WORDS = re.compile(r"[a-z0-9]+")
#: The aggregator formats evidence bullets as "[{claim_kind} | {location} | {id}] {claim}".
_BULLET_KIND = re.compile(r"^\[\s*([a-zA-Z_]+)\s*\|")
#: A number WITH a market unit — the strong form of a threshold. Tried first, because axis
#: names are full of bare digits ("us 5s30s slope") that are not levels.
_UNIT_THRESHOLD = re.compile(r"[-+]?\d[\d,.]*\s*(?:bps|bp|%|pp|x|mm|bn|k)\b", re.IGNORECASE)
#: A bare number, only where it is not glued to a word (so "5s30s" is not a level).
_BARE_THRESHOLD = re.compile(r"[-+]?\d[\d,.]*(?!\w)")
#: Words that connect an observable to its level. They belong with the LEVEL ("above 120bp"),
#: not with the observable, or the falsifier reads as "watch the slope above".
_RELATION_WORDS = frozenset({
    "above", "below", "over", "under", "beyond", "past", "through", "at", "exceeds",
    "exceed", "crosses", "cross", "breaches", "breach", "than", "more", "less", "greater",
    "wider", "tighter", "higher", "lower", "reaches", "hits",
})


def _tokens(text: str) -> frozenset:
    out = set()
    for tok in _WORDS.findall((text or "").lower()):
        if tok in _STOPWORDS:
            continue
        if len(tok) > 3 and tok.endswith("s") and not tok.endswith("ss"):
            tok = tok[:-1]
        out.add(tok)
    return frozenset(out)


def _overlap(a: frozenset, b: frozenset) -> float:
    """Overlap coefficient — |a ∩ b| / min(|a|, |b|)."""
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def _split_claim(claim: str) -> tuple[str, str]:
    """'driver → outcome' → ('driver', 'outcome'). An arrowless claim is all driver."""
    parts = [p.strip() for p in _ARROW.split(claim or "") if p.strip()]
    if len(parts) >= 2:
        return parts[0], parts[-1]
    return (parts[0] if parts else ""), ""


def _scrub(text: str) -> tuple[str, bool]:
    """Redact execution language that arrived in INGESTED text (a source's own theme name
    can say anything). Engine-GENERATED text is rejected outright instead — see
    `_validate_proposal`; the distinction matters because a directive the engine emits is a
    discipline failure, while a phrase a source used is just dirty input."""
    out = str(text or "")
    touched = False
    for _ in range(8):
        hit = _trade_hit(out)
        if hit is None:
            break
        idx = out.lower().find(hit.lower())
        if idx < 0:
            break
        out = out[:idx] + "[redacted: execution detail]" + out[idx + len(hit):]
        touched = True
    return out, touched


def _scrub_all(items) -> tuple:
    return tuple(_scrub(i)[0] for i in (items or ()))


def _strip_direction(name: str) -> str:
    """Drop direction/instrument words from a candidate name so what remains is the causal
    story. Used by the DEFAULT synthesizer to compose a compliant name; proposals from any
    other synthesizer are gated, not rewritten."""
    kept = [w for w in str(name or "").split()
            if _WORDS.findall(w.lower()) and
            not any(t in _DIRECTION_WORDS for t in _WORDS.findall(w.lower()))]
    return " ".join(kept).strip(" -–—,")


def _direction_leak(name: str) -> Optional[str]:
    for tok in _WORDS.findall((name or "").lower()):
        if tok in _DIRECTION_WORDS:
            return tok
    return None


# ── policy ───────────────────────────────────────────────────────────────────

@dataclass
class CompressionPolicy:
    """Tunables. Every default here is a documented choice, not a tuned constant."""
    parent_cap: int = 7                     # the 3–7 band's upper bound
    min_parent_themes: int = 3              # below this we WARN (we never invent a theme)
    max_families_per_parent: int = 2
    driver_overlap_to_group: float = 0.5    # driver-token overlap that puts two themes under
                                            # one parent (they still stay separate subthemes)
    current_temporal_min: float = 0.5       # temporal_quality at/above which a theme is "current"
    max_subthemes_per_parent: int = 12
    as_of: Optional[str] = None             # caller-supplied date for the readout; NO wall clock
    batch_label: Optional[str] = None
    # Sources whose contribution is opinion-only can be named here when the caller knows
    # better than the evidence bullets do.
    opinion_only_slugs: frozenset = field(default_factory=frozenset)


# ── the generative seam ──────────────────────────────────────────────────────

class ClusterDigest(BaseModel):
    """One input cluster, flattened to exactly what a synthesizer is allowed to see. It
    carries no scores that would let a proposer reverse-engineer the ranking, and no wiki
    CASE content — the firewall is upstream and this stage never widens it."""
    model_config = ConfigDict(frozen=True)
    cluster_id: str
    theme_name: str
    thesis: str
    driver: str
    outcome: str
    causal_claims: tuple[str, ...] = ()
    operational_axes: tuple[str, ...] = ()
    falsifiers: tuple[str, ...] = ()
    confounders: tuple[str, ...] = ()
    strategy_family_hints: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    source_slugs: tuple[str, ...] = ()
    evidence_count: int = 0
    independent_source_count: int = 0
    contradiction_count: int = 0
    temporal_status: str = "current"
    missing_data: tuple[str, ...] = ()


class ParentThemeRequest(BaseModel):
    """What the agent asks the synthesizer for: name one parent theme over these clusters."""
    model_config = ConfigDict(frozen=True)
    group_id: str
    clusters: tuple[ClusterDigest, ...]
    allowed_evidence_ids: tuple[str, ...]      # the ONLY ids a proposal may cite
    allowed_families: tuple[str, ...]          # routable families visible in this group
    max_families: int = 2

    def instruction(self) -> str:
        """The prompt text an LLM adapter renders. Kept here so the contract — including the
        theme-is-not-a-direction rule — lives with the request, not in an adapter."""
        return (
            "Name ONE parent theme covering the clusters below and state its causal "
            "mechanism as driver → transmission → outcome. The name must describe the "
            "CAUSAL STORY only: no direction, no instrument, no trade, no sizing. Cite only "
            "evidence ids drawn from allowed_evidence_ids, and choose one or two families "
            "from allowed_families. State why it matters, why it might be wrong, a falsifier "
            "with an observable and a numeric threshold, and why you selected it."
        )


class ParentThemeProposal(BaseModel):
    """The synthesizer's answer. It is a PROPOSAL: the gate decides whether it survives."""
    model_config = ConfigDict(frozen=True)
    name: str
    driver: str
    transmission: str
    outcome: str
    why_it_matters: str
    why_it_might_be_wrong: str
    selection_rationale: str
    falsifier_observable: str
    falsifier_threshold: str
    falsifier_kill_rule: str = ""
    strategy_families: tuple[str, ...] = ()
    cited_evidence_ids: tuple[str, ...] = ()
    operational_axis: Optional[str] = None
    watchlist_tag: Optional[str] = None
    missing_data: tuple[str, ...] = ()


@runtime_checkable
class ThemeSynthesizer(Protocol):
    """The one generative seam in this module.

    Naming a parent theme and writing its mechanism need generation; everything else here is
    deterministic. An Anthropic/OpenAI adapter implements this single method and plugs in
    unchanged, and `ScriptedThemeSynthesizer` stands in for it under test. The agent never
    calls a model directly, and it never trusts what comes back: `_validate_proposal` checks
    grounding, families, falsifier, trade language and direction leakage before the proposal
    can become a `ParentTheme`.

    Returning None means "I cannot name this group" — the group is then rejected WITH a
    reason rather than silently dropped.
    """

    def propose_parent_theme(
        self, request: ParentThemeRequest
    ) -> Optional[ParentThemeProposal]: ...


class DeterministicThemeSynthesizer:
    """The default: composes the proposal from the clusters' own fields. No model, no
    network, no wall clock — so the whole pipeline runs and is testable without an LLM, and
    a generative synthesizer is a drop-in upgrade rather than a dependency."""

    def propose_parent_theme(
        self, request: ParentThemeRequest
    ) -> Optional[ParentThemeProposal]:
        clusters = request.clusters
        if not clusters:
            return None
        rep = clusters[0]

        name = _strip_direction(_scrub(rep.theme_name)[0]) or _strip_direction(rep.driver)
        if not name:
            return None

        axis = rep.operational_axes[0] if rep.operational_axes else None
        driver = rep.driver or rep.theme_name
        outcome = rep.outcome or (rep.causal_claims[0] if rep.causal_claims else rep.thesis)
        # With two or more causal claims the middle of the chain IS the transmission; with
        # one, the observable axis is the channel the driver reaches the outcome through.
        if len(rep.causal_claims) >= 2:
            mid_driver, mid_outcome = _split_claim(rep.causal_claims[1])
            transmission = f"{mid_driver} feeds {mid_outcome}" if mid_outcome else mid_driver
        else:
            transmission = f"transmits through {axis}" if axis else "transmission not yet named"

        families = tuple(f for f in request.allowed_families
                         if f != "watchlist_only")[: request.max_families]
        if not families:
            families = tuple(request.allowed_families[: request.max_families])

        observable, threshold = _falsifier_parts(rep.falsifiers)
        if not threshold:
            return None

        indep = max(c.independent_source_count for c in clusters)
        n_ev = len(request.allowed_evidence_ids)
        contradictions = sum(c.contradiction_count for c in clusters)

        why_wrong = (rep.confounders[0] if rep.confounders else
                     "corroboration may reflect shared sourcing rather than independent "
                     "confirmation of the mechanism")
        if contradictions:
            why_wrong += f"; {contradictions} source contradiction(s) on record"

        return ParentThemeProposal(
            name=name,
            driver=driver,
            transmission=transmission,
            outcome=outcome,
            why_it_matters=(
                f"{n_ev} source-backed evidence atom(s) across {indep} independent source(s), "
                f"and the mechanism is observable on {axis or 'a watchlist tag only'}."
            ),
            why_it_might_be_wrong=why_wrong,
            selection_rationale=(
                f"selected over {len(clusters)} candidate cluster(s) sharing this driver: it "
                f"has evidence ({n_ev} atom(s)), a named causal chain, an operational axis "
                f"({axis or 'watchlist'}), a falsifier with a threshold, and a routable family."
            ),
            falsifier_observable=observable,
            falsifier_threshold=threshold,
            falsifier_kill_rule=f"if {observable} goes {threshold}, the theme is dead",
            strategy_families=families,
            cited_evidence_ids=request.allowed_evidence_ids,
            operational_axis=axis,
            watchlist_tag=None if axis else "watchlist: no operational axis named yet",
            missing_data=tuple(sorted({m for c in clusters for m in c.missing_data})),
        )


class ScriptedThemeSynthesizer:
    """Test double for the seam. Keyed on the FIRST cluster id in the request (the tests know
    those ids; group ids are generated). Anything unscripted falls through to `fallback`, or
    returns None when there is none."""

    def __init__(
        self,
        by_cluster_id: dict,
        fallback: Optional[ThemeSynthesizer] = None,
    ) -> None:
        self._by_cluster_id = dict(by_cluster_id)
        self._fallback = fallback
        self.requests: list[ParentThemeRequest] = []

    def propose_parent_theme(
        self, request: ParentThemeRequest
    ) -> Optional[ParentThemeProposal]:
        self.requests.append(request)
        for digest in request.clusters:
            if digest.cluster_id in self._by_cluster_id:
                return self._by_cluster_id[digest.cluster_id]
        if request.group_id in self._by_cluster_id:
            return self._by_cluster_id[request.group_id]
        if self._fallback is not None:
            return self._fallback.propose_parent_theme(request)
        return None


def _falsifier_parts(falsifiers: tuple) -> tuple[str, str]:
    """Split the first threshold-bearing falsifier string into (observable, threshold).

    "us 5s30s slope above 120bp" → ("us 5s30s slope", "above 120bp"). A falsifier with no
    level in it is not a falsifier, so it yields ('', '').
    """
    for f in falsifiers:
        text = str(f or "").strip()
        m = _UNIT_THRESHOLD.search(text) or _BARE_THRESHOLD.search(text)
        if not m:
            continue
        level = m.group(0).strip()
        head = text[: m.start()].strip(" .,:;-")
        words = head.split()
        relation: list[str] = []
        while words and words[-1].lower().strip(",.") in _RELATION_WORDS:
            relation.insert(0, words.pop())
        observable = " ".join(words).strip(" .,:;-")
        threshold = " ".join(relation + [level]).strip()
        return observable, threshold
    return "", ""


# ── screening: the downgrade rules ───────────────────────────────────────────

@dataclass(frozen=True)
class _Screened:
    cluster: ThemeCluster
    eligible: bool
    destination: str = "watchlist"
    reason_code: str = "gate_failed"
    reason: str = ""


def _claim_kinds(cluster: ThemeCluster) -> set:
    """Claim kinds behind this cluster, read off the aggregator's evidence-bullet format.
    Returns an empty set when nothing parses — the caller must then SKIP the opinion rule
    rather than guess (we never demote a theme on an unreadable signal)."""
    kinds = set()
    for bullet in cluster.evidence_bullets:
        m = _BULLET_KIND.match(bullet.text or "")
        if m:
            kinds.add(m.group(1))
    return kinds


def _temporal_status(cluster: ThemeCluster, policy: CompressionPolicy) -> str:
    if cluster.theme_status in ("historical_case", "outcome_candidate"):
        return "historical_outcome_candidate"
    if cluster.temporal_quality < policy.current_temporal_min:
        return "historical_outcome_candidate"
    return "current"


def _routable_families(cluster: ThemeCluster) -> tuple[str, ...]:
    """The cluster's hints, filtered to what the router can actually emit and stripped of
    `watchlist_only` — a theme whose only implication is "watch it" has no routable family,
    which is precisely why it should not be promoted."""
    return tuple(sorted({h for h in cluster.strategy_family_hints
                         if h in ROUTABLE_FAMILIES and h != "watchlist_only"}))


def _screen(cluster: ThemeCluster, policy: CompressionPolicy) -> _Screened:
    """Apply the downgrade rules. Any hit FORCES the theme out of promotion regardless of
    its attention score — that is the rule this stage exists to enforce."""
    name = cluster.canonical_theme_name

    if cluster.theme_status == "reject":
        return _Screened(cluster, False, "rejected", "rejected_upstream",
                         f"'{name}' was already rejected by the aggregator "
                         "(mentions only, no source-backed evidence).")

    # Historical discipline first: its destination differs from every other downgrade.
    if _temporal_status(cluster, policy) == "historical_outcome_candidate":
        return _Screened(
            cluster, False, "outcome_candidate", "historical_forecast_without_outcome_check",
            f"'{name}' rests on historical/closed-forecast sources; it is emitted as an "
            "outcome candidate for after-the-fact scoring, never promoted.")

    current_evidence = any(
        a.is_current_input and a.contribution_type == "supports" and a.evidence_ids
        for a in cluster.source_attributions
    )
    if not current_evidence or not cluster.evidence_ids:
        return _Screened(cluster, False, "watchlist", "attention_without_evidence",
                         f"'{name}' has attention (score {cluster.attention_score:.2f}) but no "
                         "current-input, source-backed evidence atom.")

    if not cluster.operational_axes:
        return _Screened(cluster, False, "watchlist", "no_operational_axis",
                         f"'{name}' names no operational axis — nothing to observe, so it "
                         "cannot be a parent theme.")

    if not cluster.causal_claims:
        return _Screened(cluster, False, "watchlist", "no_causal_chain",
                         f"'{name}' has no causal chain — a driver beside an outcome is a "
                         "correlation, not a mechanism.")

    kinds = _claim_kinds(cluster)
    opinion_slugs = {a.source_slug for a in cluster.source_attributions
                     if a.source_slug in policy.opinion_only_slugs}
    supporting = {a.source_slug for a in cluster.source_attributions
                  if a.contribution_type == "supports"}
    if (kinds and kinds <= {"source_opinion"}) or (supporting and supporting <= opinion_slugs):
        return _Screened(cluster, False, "watchlist", "only_source_opinion",
                         f"'{name}' rests on source opinion only — no fact or forecast atom "
                         "behind it.")

    observable, threshold = _falsifier_parts(tuple(cluster.falsifiers))
    if not cluster.falsifiers:
        return _Screened(cluster, False, "watchlist", "no_falsifier",
                         f"'{name}' has no falsifier. A thesis with no falsifier is not a "
                         "thesis.")
    if not threshold:
        return _Screened(cluster, False, "watchlist", "no_falsifier",
                         f"'{name}' has falsifier text but no threshold in it — a falsifier "
                         "needs an observable AND a level.")
    if not observable:
        return _Screened(cluster, False, "watchlist", "no_falsifier",
                         f"'{name}' has a threshold but names no observable to watch.")

    if not _routable_families(cluster):
        return _Screened(cluster, False, "watchlist", "no_routable_family",
                         f"'{name}' maps to no routable strategy family (hints: "
                         f"{sorted(cluster.strategy_family_hints) or 'none'}).")

    return _Screened(cluster, True)


# ── grouping, merging, keep-separate ─────────────────────────────────────────

def _driver_tokens(cluster: ThemeCluster) -> frozenset:
    """The driver side of this cluster's causal claims — the axis on which parents group."""
    toks: set = set()
    for claim in sorted(cluster.causal_claims):
        driver, _ = _split_claim(claim)
        toks |= _tokens(driver)
    return frozenset(toks) or _tokens(cluster.canonical_theme_name)


def _outcome_tokens(cluster: ThemeCluster) -> frozenset:
    toks: set = set()
    for claim in sorted(cluster.causal_claims):
        _, outcome = _split_claim(claim)
        toks |= _tokens(outcome)
    return frozenset(toks)


@dataclass
class _Group:
    group_id: str
    clusters: list
    driver: set


def _merge_signature(cluster: ThemeCluster, policy: CompressionPolicy) -> tuple:
    """The five dimensions the merge rule requires themes to share, plus temporal status
    (one current and one historical are kept separate)."""
    return (
        tuple(sorted(_driver_tokens(cluster))),
        tuple(sorted(_tokens(" ".join(sorted(cluster.causal_claims))))),   # mechanism
        tuple(sorted(_outcome_tokens(cluster))),
        tuple(sorted(_tokens(" ".join(sorted(cluster.operational_axes))))),
        _routable_families(cluster),
        _temporal_status(cluster, policy),
    )


#: Positionally aligned with `_merge_signature`. Index 0 is the driver: inside a group the
#: drivers OVERLAP but need not be identical, and a differently-framed driver is a difference
#: of mechanism, not of driver.
_SIGNATURE_DIMENSION_REASONS = (
    "different_mechanism",        # 0 driver phrasing
    "different_mechanism",        # 1 causal chain
    "different_outcome",          # 2
    "different_axis",             # 3
    "different_strategy_family",  # 4
    "different_temporal_status",  # 5
)


def _keep_separate_reason(sig_a: tuple, sig_b: tuple) -> str:
    """Name the FIRST dimension on which two same-driver themes differ — the reason they are
    subthemes of one parent rather than one merged theme."""
    for i, (a, b) in enumerate(zip(sig_a, sig_b)):
        if a != b:
            return _SIGNATURE_DIMENSION_REASONS[i]
    return "representative"


def _group_clusters(screened: list, policy: CompressionPolicy) -> list:
    """Single-link agglomeration on DRIVER tokens, walked in a deterministic order."""
    groups: list[_Group] = []
    for s in screened:
        driver = _driver_tokens(s.cluster)
        placed = False
        for g in groups:
            if _overlap(driver, frozenset(g.driver)) >= policy.driver_overlap_to_group:
                g.clusters.append(s.cluster)
                g.driver |= driver
                placed = True
                break
        if not placed:
            groups.append(_Group(group_id=f"pg-{len(groups) + 1:03d}",
                                 clusters=[s.cluster], driver=set(driver)))
    return groups


def _rank_key(group: _Group) -> tuple:
    """Deterministic ranking: best promotion score, then evidence, then independence, then id."""
    best = max(c.promotion_score for c in group.clusters)
    evidence = sum(c.evidence_count for c in group.clusters)
    indep = max(c.independent_source_count for c in group.clusters)
    return (-best, -evidence, -indep, group.clusters[0].cluster_id)


# ── proposal validation (the gate's grounding half) ──────────────────────────

def _proposal_text(p: ParentThemeProposal) -> str:
    return " \n".join([
        p.name, p.driver, p.transmission, p.outcome, p.why_it_matters,
        p.why_it_might_be_wrong, p.selection_rationale, p.falsifier_observable,
        p.falsifier_threshold, p.falsifier_kill_rule, *(p.missing_data or ()),
    ])


def _validate_proposal(
    proposal: Optional[ParentThemeProposal], request: ParentThemeRequest
) -> tuple[Optional[str], str]:
    """Return (reason_code, reason) when the proposal must be rejected, else (None, "").

    Engine-generated text is REJECTED for trade language, never scrubbed: a directive the
    engine emits is a discipline failure, and quietly rewriting it would hide that.
    """
    if proposal is None:
        return ("malformed_synthesis",
                "the synthesizer declined to name this group; no parent theme was invented "
                "to fill the gap.")

    for field_name in ("name", "driver", "transmission", "outcome", "why_it_matters",
                       "why_it_might_be_wrong", "selection_rationale"):
        if not str(getattr(proposal, field_name) or "").strip():
            return ("malformed_synthesis",
                    f"proposal '{proposal.name or '(unnamed)'}' left {field_name} empty.")

    cited = tuple(proposal.cited_evidence_ids or ())
    allowed = set(request.allowed_evidence_ids)
    if not cited:
        return ("ungrounded_synthesis",
                f"proposal '{proposal.name}' cites no evidence id — a theme with nothing "
                "behind it is not promoted.")
    invented = sorted(set(cited) - allowed)
    if invented:
        return ("ungrounded_synthesis",
                f"proposal '{proposal.name}' cites evidence ids not present in its own "
                f"clusters: {invented}.")

    families = tuple(proposal.strategy_families or ())
    routable = [f for f in families if f in ROUTABLE_FAMILIES and f != "watchlist_only"]
    if not routable:
        return ("no_routable_family",
                f"proposal '{proposal.name}' names no routable strategy family "
                f"(got {list(families) or 'none'}).")
    if len(families) > request.max_families:
        return ("malformed_synthesis",
                f"proposal '{proposal.name}' names {len(families)} strategy families; the "
                f"cap is {request.max_families}.")

    if not proposal.falsifier_observable.strip() or not proposal.falsifier_threshold.strip():
        return ("gate_failed",
                f"proposal '{proposal.name}' has no falsifier observable + threshold.")
    if not re.search(r"\d", proposal.falsifier_threshold):
        return ("gate_failed",
                f"proposal '{proposal.name}' has a falsifier threshold with no level in it "
                f"('{proposal.falsifier_threshold}').")

    if not (proposal.operational_axis or proposal.watchlist_tag):
        return ("gate_failed",
                f"proposal '{proposal.name}' has neither an operational axis nor an explicit "
                "watchlist tag.")

    leak = _direction_leak(proposal.name)
    if leak:
        return ("direction_leak",
                f"proposal name '{proposal.name}' carries the direction/instrument word "
                f"'{leak}'. A theme is the causal story; the direction of expression is a "
                "different output.")

    hit = _trade_hit(_proposal_text(proposal))
    if hit:
        return ("trade_language",
                f"proposal '{proposal.name}' contains execution language ('{hit}').")

    return (None, "")


def evaluate_gate(
    proposal: Optional[ParentThemeProposal], request: ParentThemeRequest
) -> tuple[bool, str, str]:
    """Public form of the promotion gate: (passed, reason_code, reason). `ParentTheme` also
    enforces the gate structurally by raising; this reports instead, so the agent can demote
    with a reason rather than crash on ordinary bad input."""
    code, reason = _validate_proposal(proposal, request)
    return (code is None, code or "", reason)


# ── the agent ────────────────────────────────────────────────────────────────

class ThemeCompressionAgent:
    """Compress a `MultiSourceThemeSet` into an `AnalystThemeMap`.

    Deterministic apart from the `ThemeSynthesizer` seam, which defaults to a deterministic
    implementation — so the whole agent is reproducible out of the box.
    """

    def __init__(
        self,
        synthesizer: Optional[ThemeSynthesizer] = None,
        policy: Optional[CompressionPolicy] = None,
    ) -> None:
        self.synthesizer: ThemeSynthesizer = synthesizer or DeterministicThemeSynthesizer()
        self.policy = policy or CompressionPolicy()

    # -- public entry point -------------------------------------------------
    def compress(self, theme_set: MultiSourceThemeSet) -> AnalystThemeMap:
        policy = self.policy
        warnings: list[str] = []
        rejected_or_merged: list[DemotedTheme] = []
        not_promoted: list[DemotedTheme] = []
        outcome_candidates: list[DemotedTheme] = []

        clusters = sorted(theme_set.clusters,
                          key=lambda c: (-c.promotion_score, c.cluster_id))

        # 1 — screen
        eligible: list[_Screened] = []
        for cluster in clusters:
            s = _screen(cluster, policy)
            if s.eligible:
                eligible.append(s)
                continue
            demoted = self._demote(s.cluster, s.destination, s.reason_code, s.reason)
            if s.destination == "outcome_candidate":
                outcome_candidates.append(demoted)
            elif s.destination == "rejected":
                rejected_or_merged.append(demoted)
            else:
                not_promoted.append(demoted)

        # 2/3 — group by driver, then decide merge vs keep-separate inside each group
        groups = _group_clusters(eligible, policy)
        ranked = sorted(groups, key=_rank_key)

        # 4 — cap
        kept, tail = ranked[: policy.parent_cap], ranked[policy.parent_cap:]
        for g in tail:
            for c in g.clusters:
                not_promoted.append(self._demote(
                    c, "watchlist", "parent_cap_exceeded",
                    f"'{c.canonical_theme_name}' ranks below the top {policy.parent_cap} "
                    "parent themes by promotion score; demoted to watchlist, not dropped."))
        if tail:
            warnings.append(
                f"parent_cap={policy.parent_cap}: {len(tail)} group(s) covering "
                f"{sum(len(g.clusters) for g in tail)} cluster(s) demoted to watchlist.")

        # 5/6 — synthesize and gate
        parents: list[ParentTheme] = []
        for g in kept:
            parent, demotions = self._build_parent(g, len(parents) + 1, policy)
            rejected_or_merged.extend(d for d in demotions if d.destination != "watchlist")
            not_promoted.extend(d for d in demotions if d.destination == "watchlist")
            if parent is not None:
                parents.append(parent)

        if len(parents) < policy.min_parent_themes:
            warnings.append(
                f"only {len(parents)} parent theme(s) cleared the gate (target band is "
                f"{policy.min_parent_themes}–{policy.parent_cap}); no theme was invented to "
                "reach the floor.")

        # 7 — render
        matrix = self._coverage_matrix(theme_set, parents, not_promoted, outcome_candidates,
                                       rejected_or_merged)
        readout = self._readout(theme_set, parents, not_promoted, rejected_or_merged,
                                outcome_candidates, policy)
        hit = _trade_hit(readout)
        if hit is not None:                                  # unreachable by construction
            raise CompressionDisciplineError(
                f"the analyst readout contains execution language ('{hit}')")

        stats = CompressionStats(
            clusters_in=len(theme_set.clusters),
            parent_themes_out=len(parents),
            subthemes_out=sum(len(p.subthemes) for p in parents),
            merged_count=sum(len(p.merged_cluster_ids) for p in parents),
            demoted_to_watchlist_count=len(not_promoted),
            rejected_count=len(rejected_or_merged),
            outcome_candidate_count=len(outcome_candidates),
        )
        return AnalystThemeMap(
            batch_id=policy.batch_label or theme_set.batch_id,
            parent_cap=policy.parent_cap,
            parent_themes=tuple(parents),
            source_coverage_matrix=matrix,
            rejected_or_merged_themes=tuple(rejected_or_merged),
            hot_topics_not_promoted=tuple(not_promoted),
            outcome_candidates=tuple(outcome_candidates),
            human_readout=readout,
            stats=stats,
            warnings=tuple(warnings),
        )

    # -- pieces -------------------------------------------------------------
    @staticmethod
    def _demote(cluster: ThemeCluster, destination: str, code: str, reason: str,
                merged_into: Optional[str] = None) -> DemotedTheme:
        name, _ = _scrub(cluster.canonical_theme_name)
        scrubbed_reason, _ = _scrub(reason)
        return DemotedTheme(
            cluster_id=cluster.cluster_id, theme_name=name,
            destination=destination, reason_code=code, reason=scrubbed_reason,
            merged_into=merged_into, attention_score=cluster.attention_score,
            evidence_count=cluster.evidence_count,
        )

    def _digest(self, cluster: ThemeCluster, policy: CompressionPolicy) -> ClusterDigest:
        driver_claim = sorted(cluster.causal_claims)[0] if cluster.causal_claims else ""
        driver, outcome = _split_claim(driver_claim)
        return ClusterDigest(
            cluster_id=cluster.cluster_id,
            theme_name=_scrub(cluster.canonical_theme_name)[0],
            thesis=_scrub(cluster.canonical_thesis)[0],
            driver=driver or _scrub(cluster.canonical_theme_name)[0],
            outcome=outcome,
            # The digest is the scrub boundary: everything a synthesizer sees has already had
            # ingested execution language redacted, so any trade language in a PROPOSAL came
            # from the synthesizer itself — and is rejected rather than quietly cleaned up.
            causal_claims=_scrub_all(sorted(cluster.causal_claims)),
            operational_axes=_scrub_all(sorted(cluster.operational_axes)),
            falsifiers=_scrub_all(sorted(cluster.falsifiers)),
            confounders=_scrub_all(sorted(cluster.confounders)),
            strategy_family_hints=_routable_families(cluster),
            evidence_ids=tuple(sorted(cluster.evidence_ids)),
            source_slugs=tuple(sorted({a.source_slug for a in cluster.source_attributions})),
            missing_data=_scrub_all(sorted(cluster.missing_data)),
            evidence_count=cluster.evidence_count,
            independent_source_count=cluster.independent_source_count,
            contradiction_count=cluster.contradiction_count,
            temporal_status=_temporal_status(cluster, policy),
        )

    def _build_parent(self, group: _Group, index: int, policy: CompressionPolicy):
        """Resolve merges and subthemes inside one group, ask the seam to name it, gate the
        answer. Returns (parent_or_None, demotions)."""
        demotions: list[DemotedTheme] = []
        ordered = sorted(group.clusters, key=lambda c: (-c.promotion_score, c.cluster_id))
        parent_id = f"pt-{index:03d}"

        # merge rule: identical on driver + mechanism + outcome + axis + family (+ temporal)
        rep = ordered[0]
        rep_sig = _merge_signature(rep, policy)
        merged: list[ThemeCluster] = []
        separate: list[tuple[ThemeCluster, str]] = []
        for c in ordered[1:]:
            sig = _merge_signature(c, policy)
            if sig == rep_sig:
                merged.append(c)
            else:
                separate.append((c, _keep_separate_reason(rep_sig, sig)))

        digests = tuple(self._digest(c, policy) for c in ordered)
        allowed_evidence = tuple(sorted({e for c in ordered for e in c.evidence_ids}))
        allowed_families = tuple(sorted({f for c in ordered for f in _routable_families(c)}))
        request = ParentThemeRequest(
            group_id=group.group_id, clusters=digests,
            allowed_evidence_ids=allowed_evidence, allowed_families=allowed_families,
            max_families=policy.max_families_per_parent,
        )
        proposal = self.synthesizer.propose_parent_theme(request)
        passed, code, reason = evaluate_gate(proposal, request)
        if not passed:
            for c in ordered:
                demotions.append(self._demote(
                    c, "rejected" if code in ("ungrounded_synthesis", "trade_language",
                                              "direction_leak", "malformed_synthesis")
                    else "watchlist", code, reason))
            return None, demotions

        assert proposal is not None                       # evaluate_gate guarantees it
        for c in merged:
            demotions.append(self._demote(
                c, "merged", "merged_into_parent",
                f"'{c.canonical_theme_name}' merged into '{proposal.name}' — shares driver, "
                "mechanism, outcome, axis and strategy family.", merged_into=parent_id))

        subthemes = tuple(
            Subtheme(
                subtheme_id=f"{parent_id}-s{i:02d}",
                name=_scrub(c.canonical_theme_name)[0],
                source_cluster_id=c.cluster_id,
                keep_separate_reason=why,          # type: ignore[arg-type]
                operational_axes=_scrub_all(sorted(c.operational_axes)),
                evidence_ids=tuple(sorted(c.evidence_ids)),
                source_slugs=tuple(sorted({a.source_slug for a in c.source_attributions})),
                temporal_status=_temporal_status(c, policy),   # type: ignore[arg-type]
                causal_claims=_scrub_all(sorted(c.causal_claims)),
            )
            for i, (c, why) in enumerate(separate[: policy.max_subthemes_per_parent], start=1)
        )

        by_source: dict[str, tuple] = {}
        for c in ordered:
            for a in c.source_attributions:
                ev, contrib, cur = by_source.get(a.source_slug, ((), a.contribution_type, a.is_current_input))
                by_source[a.source_slug] = (
                    tuple(sorted(set(ev) | set(a.evidence_ids))),
                    "supports" if "supports" in (contrib, a.contribution_type) else a.contribution_type,
                    cur or a.is_current_input,
                )
        evidence_by_source = tuple(
            EvidenceBySource(source_slug=slug, evidence_ids=ev, contribution_type=contrib,
                             is_current_input=cur)
            for slug, (ev, contrib, cur) in sorted(by_source.items())
        )

        families = tuple(f for f in proposal.strategy_families
                         if f in ROUTABLE_FAMILIES)[: policy.max_families_per_parent]
        parent = ParentTheme(
            parent_id=parent_id,
            name=proposal.name,
            mechanism=CausalMechanism(driver=proposal.driver,
                                      transmission=proposal.transmission,
                                      outcome=proposal.outcome),
            subthemes=subthemes,
            evidence_by_source=evidence_by_source,
            evidence_ids=allowed_evidence,
            operational_axis=proposal.operational_axis,
            watchlist_tag=proposal.watchlist_tag,
            temporal_status="current",
            strategy_families=families,          # type: ignore[arg-type]
            why_it_matters=proposal.why_it_matters,
            why_it_might_be_wrong=proposal.why_it_might_be_wrong,
            falsifier=ThemeFalsifier(observable=proposal.falsifier_observable,
                                     threshold=proposal.falsifier_threshold,
                                     kill_rule=proposal.falsifier_kill_rule),
            selection_rationale=proposal.selection_rationale,
            missing_data=tuple(sorted(set(proposal.missing_data))),
            merged_cluster_ids=tuple(c.cluster_id for c in merged),
            member_cluster_ids=tuple(c.cluster_id for c in ordered),
            evidence_count=len(allowed_evidence),
            independent_source_count=max(c.independent_source_count for c in ordered),
            contradiction_count=sum(c.contradiction_count for c in ordered),
        )
        return parent, demotions

    # -- coverage matrix ----------------------------------------------------
    def _coverage_matrix(self, theme_set, parents, not_promoted, outcome_candidates,
                         rejected) -> SourceCoverageMatrix:
        slugs = tuple(sorted(theme_set.source_slugs))
        by_cluster = {c.cluster_id: c for c in theme_set.clusters}
        rows: list[CoverageRow] = []

        for p in parents:
            per_slug = {e.source_slug: e for e in p.evidence_by_source}
            contradicting = sorted(
                {a.source_slug
                 for cid in p.member_cluster_ids
                 for a in by_cluster[cid].source_attributions
                 if a.contribution_type == "contradicts"})
            rows.append(CoverageRow(
                theme_id=p.parent_id, theme_name=p.name,
                cells=tuple(
                    CoverageCell(
                        source_slug=s, present=s in per_slug,
                        contribution_type=per_slug[s].contribution_type if s in per_slug else "absent",
                        evidence_count=len(per_slug[s].evidence_ids) if s in per_slug else 0,
                    ) for s in slugs),
                evidence_count=p.evidence_count,
                independent_sources=p.independent_source_count,
                contradictions=p.contradiction_count,
                contradiction_note=(f"contradicted by {', '.join(contradicting)}"
                                    if contradicting else ""),
                status="promote",
            ))

        status_by_list = (
            (not_promoted, "watchlist"),
            (outcome_candidates, "outcome_candidate"),
            (rejected, "rejected"),
        )
        for demoted_list, status in status_by_list:
            for d in demoted_list:
                cluster = by_cluster.get(d.cluster_id)
                if cluster is None:
                    continue
                per_slug = {a.source_slug: a for a in cluster.source_attributions}
                contradicting = sorted({a.source_slug for a in cluster.source_attributions
                                        if a.contribution_type == "contradicts"})
                rows.append(CoverageRow(
                    theme_id=d.cluster_id, theme_name=d.theme_name,
                    cells=tuple(
                        CoverageCell(
                            source_slug=s, present=s in per_slug,
                            contribution_type=(per_slug[s].contribution_type
                                               if s in per_slug else "absent"),
                            evidence_count=(len(per_slug[s].evidence_ids)
                                            if s in per_slug else 0),
                        ) for s in slugs),
                    evidence_count=cluster.evidence_count,
                    independent_sources=cluster.independent_source_count,
                    contradictions=cluster.contradiction_count,
                    contradiction_note=(f"contradicted by {', '.join(contradicting)}"
                                        if contradicting else ""),
                    status=status,      # type: ignore[arg-type]
                ))
        return SourceCoverageMatrix(source_slugs=slugs, rows=tuple(rows))

    # -- human readout ------------------------------------------------------
    def _readout(self, theme_set, parents, not_promoted, rejected, outcome_candidates,
                 policy) -> str:
        date = policy.as_of or "date not supplied"
        lines = [f"## Analyst synthesis — batch {theme_set.batch_id} ({date})", ""]
        lines.append(f"### Parent themes ({len(parents)})")
        if not parents:
            lines.append("_None cleared the promotion gate._")
        for i, p in enumerate(parents, start=1):
            n_sources = len(p.evidence_by_source)
            lines += [
                f"{i}. {p.name} — {p.mechanism.driver} → {p.mechanism.outcome}",
                f"   - Subthemes: {', '.join(s.name for s in p.subthemes) or '(none)'}",
                f"   - Evidence: {p.evidence_count} atom(s) across {n_sources} source(s)  "
                f"(corroboration: {p.independent_source_count} independent source(s))",
                f"   - Operational axis: {p.operational_axis or p.watchlist_tag or 'watchlist'}",
                f"   - Temporal status: {p.temporal_status}",
                f"   - Strategy family: {', '.join(p.strategy_families)}",
                f"   - Why it matters: {p.why_it_matters}",
                f"   - Why it might be wrong: {p.why_it_might_be_wrong}",
                f"   - Falsifier: watch {p.falsifier.observable}; dead if it goes "
                f"{p.falsifier.threshold}",
                f"   - Missing data: {', '.join(p.missing_data) or '(none recorded)'}",
            ]
        lines.append("")

        lines.append("### Downgraded to hot-topic / watchlist (with reason)")
        if not not_promoted:
            lines.append("- (none)")
        for d in not_promoted:
            lines.append(f"- {d.theme_name} — {d.reason_code}: {d.reason}")
        lines.append("")

        lines.append("### Merged / rejected")
        if not rejected:
            lines.append("- (none)")
        for d in rejected:
            target = f" into {d.merged_into}" if d.merged_into else ""
            lines.append(f"- {d.theme_name}{target} — {d.reason_code}: {d.reason}")
        lines.append("")

        lines.append("### Historical / outcome candidates (never promoted)")
        if not outcome_candidates:
            lines.append("- (none)")
        for d in outcome_candidates:
            lines.append(f"- {d.theme_name} — {d.reason}")
        lines.append("")

        lines.append("### Why these themes, and why not the others")
        if parents:
            lines.append(
                f"{len(parents)} theme(s) cleared the full promotion gate — evidence, a named "
                "mechanism, an operational axis, a falsifier with a threshold, a current "
                "temporal status and a routable strategy family. "
                + " ".join(f"{p.name}: {p.selection_rationale}" for p in parents))
        else:
            lines.append("No candidate cleared the promotion gate on this batch.")
        demoted_total = len(not_promoted) + len(rejected) + len(outcome_candidates)
        lines.append(
            f"{demoted_total} candidate(s) did not become parent themes; each is listed above "
            "with the rule that demoted it. Nothing was dropped silently.")
        lines += ["", "## No-trade boundary",
                  "This synthesis is discovery memory only — no trades, sizing, hedge ratios, "
                  "or execution."]

        body = "\n".join(lines)
        scrubbed, _ = _scrub(body)
        return scrubbed


def compress_theme_set(
    theme_set: MultiSourceThemeSet,
    synthesizer: Optional[ThemeSynthesizer] = None,
    policy: Optional[CompressionPolicy] = None,
) -> AnalystThemeMap:
    """Functional entry point — the aggregator's output in, the analyst map out."""
    return ThemeCompressionAgent(synthesizer=synthesizer, policy=policy).compress(theme_set)
