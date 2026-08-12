"""Multi-Source Theme Aggregator — deterministic Stage-0 component (PART 3).

Takes theme candidates from MULTIPLE current-input EvidenceExtractionBundles and produces
one deduplicated, source-attributed, ranked MultiSourceThemeSet:

    multi-source evidence → unique Stage-0 theme clusters → discovery-ready candidates → STOP

Deterministic + rule-assisted (no LLM seam in this build). It never emits trades, sizing,
hedge ratios, scenario probabilities, or fair values, and it never mutates q/edge/Omega/
scoring. Archived CASE / historical sources cannot CONFIRM a current theme in Phase A — that
gate is enforced both here (status routing) and by the ThemeCluster validator.

NOTE (scoring): the *_score formulas and the status-routing thresholds below are documented
DETERMINISTIC choices (the spec fixed the fields + the evidence−attention convention, not the
exact weights). All weights live on ThemeAggregationPolicy for tuning.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Optional

from engine.evidence_extraction import EvidenceExtractionBundle
from engine.schema.theme_aggregation import (
    EvidenceBullet,
    MultiSourceThemeSet,
    SourceAttribution,
    ThemeCluster,
    ThemeClusterMember,
)
from engine.temporal import TemporalContext
from engine.schema import SourceClassification

# ── policy ───────────────────────────────────────────────────────────────────
_DEFAULT_ALIASES = {
    "direct lending": "private credit",
    "hy hpc": "high performance computing credit",
    "europe vs us": "regional equity relative value",
    "etf basket basis": "etf cash basis",
    "rates not priced": "rates catch up",
}
# Related-but-DISTINCT token groups: matching opposite sides blocks a merge AND records a
# rejected_merge. (spec step 5)
_DEFAULT_DISTINCT_PAIRS = [
    (frozenset({"ai", "capex", "project", "bond", "basis"}),
     frozenset({"hpc", "crowding", "high", "performance", "computing"})),
    (frozenset({"europe", "rich", "fair", "value"}),
     frozenset({"cyclicals", "defensives"})),
    (frozenset({"etf", "flow", "dislocation"}),
     frozenset({"liquidity", "risk"})),
]
_STOPWORDS = frozenset({
    "the", "a", "an", "is", "are", "of", "to", "too", "in", "on", "and", "or", "vs",
    "for", "by", "with", "up", "down", "into", "as", "at", "be", "it", "its", "this",
})

# Mutually EXCLUSIVE qualifier vocabularies. Two themes that each name a qualifier from the
# same group, with no qualifier in common, are about different things however much of the rest
# of their wording they share ("european bank spreads" vs "japanese bank spreads" — same
# mechanism, different market). Blocking these is a MEANING judgement no token metric can make:
# the shared words are exactly the ones that make the pair look similar. Extensible via
# ThemeAggregationPolicy.discriminator_groups; geography only in v1, deliberately.
_DEFAULT_DISCRIMINATOR_GROUPS = [
    ("region", frozenset({
        "europe", "european", "eurozone", "emea",
        "us", "usa", "america", "american",
        "uk", "britain", "british",
        "japan", "japanese",
        "china", "chinese",
        "germany", "german", "france", "french", "italy", "italian", "spain", "spanish",
        "asia", "asian", "em", "emerging",
    })),
]


_BUZZ_TERMS = frozenset({
    "everyone", "consensus", "crowded", "popular", "hot", "bubble", "mania", "buzz",
    "frenzy", "hype", "story", "narrative", "darling", "froth", "euphoria",
})


@dataclass
class ThemeAggregationPolicy:
    """Tunable weights for clustering + PART-4 corroboration/attention/promotion scoring."""
    # Bar for the PASS-1 lexical merge, in units of `_similarity` (alias-anchored weighted
    # Jaccard — see `_weighted_jaccard`). RE-TUNED for that metric: 0.55 is the max-min-margin
    # point of the band (0.500, 0.600] over the labelled pair set in
    # tests/unit/test_theme_aggregation.py::test_merge_metric_separates_the_measured_cases.
    # It was 0.5 under the old overlap coefficient, where NO threshold separated the cases.
    min_similarity_to_merge: float = 0.55
    # Weight on tokens an alias substitution introduced. An alias is curated domain knowledge
    # that two phrasings MEAN the same thing, so agreeing on one is worth more than agreeing on
    # an incidental word. 1.0 turns this off and leaves plain Jaccard.
    alias_anchor_weight: float = 3.0
    alias_map: dict = field(default_factory=lambda: dict(_DEFAULT_ALIASES))
    distinct_pairs: list = field(default_factory=lambda: list(_DEFAULT_DISTINCT_PAIRS))
    discriminator_groups: list = field(
        default_factory=lambda: list(_DEFAULT_DISCRIMINATOR_GROUPS))
    # ── pass 2: mechanism merge ──
    # Pass 1 is a DISJUNCTION over six dimensions at a high bar ("any one signal is strong").
    # Pass 2 is a CONJUNCTION over three structural ones ("driver/outcome, mechanism AND
    # observable all agree"), so it is right for it to accept a lower per-dimension bar —
    # otherwise pass 1 has already fired on whichever dimension cleared 0.55 and pass 2 can
    # never add anything. Must stay < min_similarity_to_merge for the pass to do any work;
    # test_mechanism_bar_must_sit_below_the_lexical_bar pins that.
    mechanism_pass: bool = True
    min_mechanism_similarity: float = 0.34   # "more than a third of each structure in common"
    publisher_groups: dict = field(default_factory=dict)   # source_slug -> independence group
    # ── corroboration ──
    independent_source_bonus: float = 0.35
    same_publisher_discount: float = 0.5     # weight on extra non-independent sources
    stale_source_discount: float = 0.5
    historical_source_discount: float = 0.4
    source_fact_weight: float = 0.12
    source_opinion_weight: float = 0.05
    source_forecast_weight: float = 0.08
    evidence_cap: int = 5
    evidence_quality_weight: float = 0.10
    causal_completeness_weight: float = 0.15
    axis_availability_weight: float = 0.15
    diversity_weight: float = 0.10
    # ── attention ──
    attention_keyword_weight: float = 0.25
    hot_topic_weight: float = 0.50
    mention_without_evidence_weight: float = 0.20
    non_independent_weight: float = 0.20
    max_attention_penalty: float = 1.0
    # ── promotion ──
    promote_min_temporal: float = 0.5
    min_promote_score: float = 0.0
    contradiction_penalty: float = 0.30
    # ── (L3) parent cap — the theme-discipline down payment ──
    # Keep at most this many parent clusters (top by promotion_score); demote the tail to
    # `watchlist`. None = no cap (default; GM-neutral). Nothing is ever dropped silently.
    parent_cap: Optional[int] = None
    source_scope: Optional[str] = None      # override the inferred scope
    # ── PART 5 access/temporal firewall ──
    # Slugs the caller declares as the CURRENT INPUT batch. CASE sources listed here are
    # Phase-A eligible (rule 1); CASE sources NOT here (and not historical) are archived and
    # excluded from fresh aggregation (rule 2).
    current_input_slugs: Optional[frozenset] = None


# ── text normalisation ───────────────────────────────────────────────────────
def _normalize(name: str, alias_map: dict) -> tuple[str, frozenset]:
    s = name.lower()
    for phrase, repl in alias_map.items():
        s = s.replace(phrase, repl)
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    toks = []
    for t in s.split():
        if t in _STOPWORDS:
            continue
        if len(t) > 3 and t.endswith("s") and not t.endswith("ss"):
            t = t[:-1]  # trivial singularisation
        toks.append(t)
    return " ".join(toks), frozenset(toks)


def _containment(a: frozenset, b: frozenset) -> float:
    """Overlap coefficient — "how much of the SMALLER set is inside the larger".

    Correct for asking whether a short theme name is covered by a long evidence atom
    (`_CONTENT_LINK_MIN`), where Jaccard is always tiny because the atom has far more tokens.
    WRONG as a similarity: it returns 1.0 for any subset, so 'growth' scored 1.00 against
    'china growth slowdown' and merged at every threshold <= 1.0. Do not use it to merge.
    """
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def _weighted_jaccard(a: frozenset, b: frozenset, anchors: frozenset, weight: float) -> float:
    """Symmetric similarity: weighted |a ∩ b| / |a ∪ b|.

    Jaccard, so containment no longer saturates — the whole of BOTH sides counts, and a token
    set that is a subset of another is scored by how much it leaves out. Tokens in `anchors`
    (introduced by an alias substitution) count `weight` times, because a curated alias is
    evidence about MEANING while incidental word-sharing is not.

    Plain Jaccard alone was measured and rejected: it scores 'growth' vs 'china growth
    slowdown' (must not merge) and 'private credit risk' vs 'direct lending spreads' (must
    merge) at the same 0.333, so no threshold separates them. Anchoring the alias-derived
    tokens moves the second to 0.600 and leaves the first at 0.333.
    """
    union = a | b
    if not union:
        return 0.0
    if weight == 1.0 or not (anchors & union):
        return len(a & b) / len(union)
    mass = lambda s: sum(weight if t in anchors else 1.0 for t in s)   # noqa: E731
    return mass(a & b) / mass(union)


def _matches_side(tokens: frozenset, side: frozenset) -> bool:
    return len(tokens & side) >= 2


def _distinct_blocked(ta: frozenset, tb: frozenset, pairs) -> bool:
    for s1, s2 in pairs:
        if (_matches_side(ta, s1) and _matches_side(tb, s2)) or \
           (_matches_side(ta, s2) and _matches_side(tb, s1)):
            return True
    return False


def _discriminator_conflict(ta: frozenset, tb: frozenset, groups) -> Optional[str]:
    """Name the qualifier group on which `ta` and `tb` disagree outright, if any.

    Both sides must name a qualifier from the same group and share NONE of them. One-sided use
    is not a conflict: 'european bank spreads' vs 'bank spreads' is a candidate subtheme, not a
    contradiction, so it is left to the metric.
    """
    for name, vocab in groups:
        da, db = ta & vocab, tb & vocab
        if da and db and not (da & db):
            return name
    return None


# ── per-source temporal/classification helpers ───────────────────────────────
_RECENCY = {
    "current_report": 1.0, "method_source": 0.5, "stale_case": 0.2,
    "historical_case": 0.1, "outcome_candidate": 0.1, "unknown": 0.3, None: 0.7,
}
_CURRENT_ROLES = {"current_report", None}   # treated as current input by default


def _is_current(role: Optional[str]) -> bool:
    return role in _CURRENT_ROLES


def _eligibility(slug: str, sc, tc, policy: "ThemeAggregationPolicy") -> tuple:
    """PART 5 access/temporal firewall — classify ONE source for this Phase-A run.

    Returns (is_current_input, klass) where klass ∈
    {current, historical, method, archived_case_blocked}:
      • current  — counts as market evidence, can corroborate/promote a current theme.
      • historical — historical CASE; forms historical_case/outcome clusters, never corroborates.
      • method  — taxonomy/aliases only, NOT market evidence.
      • archived_case_blocked — archived CASE outside the current batch; dropped in Phase A.
    """
    role = tc.temporal_role if tc else None
    access = sc.access_class if sc else "method"
    if policy.current_input_slugs and slug in policy.current_input_slugs:
        return True, "current"          # rule 1: explicit current batch (even if CASE)
    if role == "current_report":
        return True, "current"
    if role in ("historical_case", "stale_case", "outcome_candidate"):
        return False, "historical"      # rule 4
    if access == "method" or role == "method_source":
        return False, "method"          # rule 3: taxonomy only
    if access in ("case", "mixed"):
        return False, "archived_case_blocked"   # rule 2 (mixed is fail-closed in v1)
    return True, "current"              # report/other, no temporal → current input


# ── raw item collection ──────────────────────────────────────────────────────
_CONTENT_LINK_MIN = 0.5   # overlap to link an atom to a theme by content (PART 7.1 fallback)


def _alias_anchors(name: str, alias_map: dict) -> frozenset:
    """Tokens an alias substitution INTRODUCED into `name` — the high-signal ones (see
    `_weighted_jaccard`). Recomputed rather than threaded out of `_normalize` so the
    normaliser keeps its two-value contract for its many other callers."""
    if not alias_map:
        return frozenset()
    low = name.lower()
    out: set = set()
    for phrase, repl in alias_map.items():
        if phrase in low:
            out |= _normalize(repl, {})[1]
    return frozenset(out)


def _tok_set(strings) -> frozenset:
    """Flatten a list of phrase strings into one normalised token set (for the
    concept / entity / market-variable similarity signals)."""
    toks: set = set()
    for s in strings or []:
        toks |= _normalize(s, {})[1]
    return frozenset(toks)


def _atom_tokens(atom) -> frozenset:
    """All content tokens of an atom (themes + concepts + entities + market_variables + claim)
    — used to link an atom to a theme when the atom did not declare the theme explicitly."""
    return (_tok_set(atom.themes) | _tok_set(atom.concepts) | _tok_set(atom.entities)
            | _tok_set(atom.market_variables) | _normalize(atom.claim or "", {})[1])


@dataclass
class _Item:
    slug: str
    raw_name: str
    norm: str
    tokens: frozenset
    from_hot: bool
    evidence_ids: list
    concepts: frozenset = frozenset()
    entities: frozenset = frozenset()
    market_vars: frozenset = frozenset()
    axes: frozenset = frozenset()
    causal: frozenset = frozenset()
    anchors: frozenset = frozenset()   # tokens an alias introduced — see _weighted_jaccard


def _collect_items(bundle: EvidenceExtractionBundle, alias_map: dict) -> list[_Item]:
    """Theme candidates from one bundle (PART 3 step 1): core themes, hot topics, theme-like
    causal claims + developments, and strategy-family hints TIED TO EVIDENCE. Each item also
    carries the shared-signal sets (concepts/entities/market_variables/axes/causal) gathered
    from its linked evidence atoms — used by the step-3 similarity."""
    atoms_by_id = {a.evidence_id: a for a in bundle.evidence_atoms if a.evidence_id}
    atoms_by_theme: dict[str, list] = {}
    for atom in bundle.evidence_atoms:
        for th in (atom.themes or []):
            atoms_by_theme.setdefault(_normalize(th, alias_map)[0], []).append(atom.evidence_id)

    # (name, is_hot, explicit_evidence_ids|None)
    raw: list[tuple] = []
    raw += [(t, False, None) for t in bundle.core_theme_candidates]
    raw += [(t, True, None) for t in bundle.hot_topics]
    raw += [(f"{c.driver} {c.outcome}", False, list(c.source_evidence_ids) or None)
            for c in bundle.causal_claims]
    raw += [(d, False, None) for d in bundle.main_developments if len(d.split()) >= 3]
    raw += [((fh.rationale or fh.family), False, list(fh.source_evidence_ids))
            for fh in bundle.strategy_family_hints if fh.source_evidence_ids]

    merged: dict[str, _Item] = {}
    for name, is_hot, explicit in raw:
        norm, toks = _normalize(name, alias_map)
        if not toks:
            continue
        ev = list(explicit) if explicit else list(atoms_by_theme.get(norm, []))
        # PART 7.1 fallback: link atoms that did NOT declare this theme but whose content
        # (entities/market_variables/claim) strongly overlaps it — so real extraction output
        # (atoms carry no `themes`) still gives each theme its source-backed evidence IDs.
        if not explicit:
            for a in bundle.evidence_atoms:
                if (a.evidence_id and a.evidence_id not in ev
                        and _containment(toks, _atom_tokens(a)) >= _CONTENT_LINK_MIN):
                    ev.append(a.evidence_id)
        evset = set(ev)
        concepts: set = set()
        entities: set = set()
        mvars: set = set()
        for eid in ev:
            a = atoms_by_id.get(eid)
            if a is not None:
                concepts |= _tok_set(a.concepts)
                entities |= _tok_set(a.entities)
                mvars |= _tok_set(a.market_variables)
        axes: set = set()
        causal: set = set()
        anchors = set(_alias_anchors(name, alias_map))
        for ax in bundle.operational_axes:
            if evset & set(ax.source_evidence_ids):
                axes |= _normalize(ax.axis_name, alias_map)[1]
                anchors |= _alias_anchors(ax.axis_name, alias_map)
        for cc in bundle.causal_claims:
            if evset & set(cc.source_evidence_ids):
                causal |= _normalize(cc.driver, alias_map)[1] | _normalize(cc.outcome, alias_map)[1]
                anchors |= (_alias_anchors(cc.driver, alias_map)
                            | _alias_anchors(cc.outcome, alias_map))

        if norm in merged:
            it = merged[norm]
            it.from_hot = it.from_hot or is_hot
            it.evidence_ids = sorted(set(it.evidence_ids) | evset)
            it.concepts |= frozenset(concepts)
            it.entities |= frozenset(entities)
            it.market_vars |= frozenset(mvars)
            it.axes |= frozenset(axes)
            it.causal |= frozenset(causal)
            it.anchors |= frozenset(anchors)
        else:
            merged[norm] = _Item(
                slug=bundle.source_slug, raw_name=name, norm=norm, tokens=toks,
                from_hot=is_hot, evidence_ids=ev, concepts=frozenset(concepts),
                entities=frozenset(entities), market_vars=frozenset(mvars),
                axes=frozenset(axes), causal=frozenset(causal), anchors=frozenset(anchors),
            )
    return list(merged.values())


# ── clustering ───────────────────────────────────────────────────────────────
@dataclass
class _Cluster:
    tokens: set
    concepts: set
    entities: set
    market_vars: set
    axes: set
    causal: set
    items: list
    anchors: set = field(default_factory=set)

    @property
    def key(self) -> str:
        """Content-derived identity, for deterministic tie-breaks and ordering."""
        return min(it.norm for it in self.items)

    def absorb(self, other: "_Cluster") -> None:
        self.items.extend(other.items)
        for attr in ("tokens", "concepts", "entities", "market_vars", "axes", "causal",
                     "anchors"):
            getattr(self, attr).update(getattr(other, attr))


def _as_cluster(it: _Item) -> _Cluster:
    return _Cluster(
        tokens=set(it.tokens), concepts=set(it.concepts), entities=set(it.entities),
        market_vars=set(it.market_vars), axes=set(it.axes), causal=set(it.causal),
        anchors=set(it.anchors), items=[it])


def _similarity(it: _Item, cl: _Cluster, policy: "ThemeAggregationPolicy") -> float:
    """PART 3 step 3: similarity is the STRONGEST shared signal across name tokens, concepts,
    entities, market_variables, axes, and causal driver/outcome — so two differently-worded
    themes that share a market variable or an axis still cluster.

    Each dimension is scored by `_weighted_jaccard`, which is SYMMETRIC: unlike the overlap
    coefficient this replaced, a theme whose tokens are a subset of another's no longer scores
    1.0 on that fact alone.
    """
    anchors = it.anchors | frozenset(cl.anchors)
    return _cluster_similarity(_as_cluster(it), cl, anchors, policy.alias_anchor_weight)


def _cluster_similarity(a: _Cluster, b: _Cluster, anchors: frozenset, weight: float) -> float:
    return max(
        _weighted_jaccard(frozenset(a.tokens), frozenset(b.tokens), anchors, weight),
        _weighted_jaccard(frozenset(a.concepts), frozenset(b.concepts), anchors, weight),
        _weighted_jaccard(frozenset(a.entities), frozenset(b.entities), anchors, weight),
        _weighted_jaccard(frozenset(a.market_vars), frozenset(b.market_vars), anchors, weight),
        _weighted_jaccard(frozenset(a.axes), frozenset(b.axes), anchors, weight),
        _weighted_jaccard(frozenset(a.causal), frozenset(b.causal), anchors, weight),
    )


def _blocked(ta: frozenset, tb: frozenset, policy) -> Optional[str]:
    """Reason these two token sets may never merge, or None. Both guards are checked in both
    passes: structure agreeing does not license merging things the guards call distinct."""
    if _distinct_blocked(ta, tb, policy.distinct_pairs):
        return "distinct_marker_guard: related but structurally distinct themes"
    group = _discriminator_conflict(ta, tb, policy.discriminator_groups)
    if group:
        return (f"discriminator_guard[{group}]: both name a {group} and they do not match — "
                "same mechanism, different market")
    return None


def _cluster_items(items: list, policy: ThemeAggregationPolicy):
    """Pass 1 (lexical recall) then pass 2 (mechanism precision), both deterministic.

    ORDER-INDEPENDENCE: items are sorted into a canonical, content-derived order first, so the
    result is a function of the input SET, not of the order the caller happened to supply. The
    pass stays greedy — it is not a global optimum — but the same themes now always produce the
    same clusters. Ties resolve to the lowest cluster key, not to whichever was seen first.
    """
    clusters: list[_Cluster] = []
    for it in sorted(items, key=lambda i: (i.norm, i.slug)):
        best, best_sim = None, 0.0
        for cl in clusters:
            if _blocked(it.tokens, frozenset(cl.tokens), policy):
                continue
            sim = _similarity(it, cl, policy)
            if sim > best_sim or (best is not None and sim == best_sim and cl.key < best.key):
                best_sim, best = sim, cl
        if best is not None and best_sim >= policy.min_similarity_to_merge:
            best.absorb(_as_cluster(it))
        else:
            clusters.append(_as_cluster(it))

    if policy.mechanism_pass:
        clusters = _mechanism_merge(clusters, policy)
    # canonical final order, so cluster_id is a function of CONTENT — not of formation order and
    # not of whether pass 2 ran.
    clusters.sort(key=lambda c: c.key)

    # record related-but-distinct near misses across the final clusters
    rejected: list[dict] = []
    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            reason = _blocked(frozenset(clusters[i].tokens), frozenset(clusters[j].tokens),
                              policy)
            if reason:
                rejected.append({
                    "theme_a": clusters[i].items[0].norm,
                    "theme_b": clusters[j].items[0].norm,
                    "reason": reason,
                })
    return clusters, rejected


def _mechanism_match(a: _Cluster, b: _Cluster, policy) -> bool:
    """Do two clusters describe the SAME causal story? Words are not consulted.

    All three must hold, using only the sets the clusters already carry:
      • driver + outcome — `causal`, the driver→outcome tokens of the linked causal claims
      • mechanism        — `axes`, the operational axis the transmission is observed on
      • outcome variable — `market_vars`, the observable that actually moves

    A missing set is never evidence of sameness: a cluster with no causal claim, no axis or no
    market variable cannot mechanism-merge at all. That keeps this pass strictly additive —
    it can only join clusters that both carry real structure.

    The bar is `min_mechanism_similarity`, deliberately BELOW the pass-1 bar: three moderate
    agreements that must all hold is stronger evidence than one strong agreement on its own.
    """
    t = policy.min_mechanism_similarity
    for x, y in ((a.causal, b.causal), (a.axes, b.axes), (a.market_vars, b.market_vars)):
        if not x or not y:
            return False
        if _weighted_jaccard(frozenset(x), frozenset(y), frozenset(), 1.0) < t:
            return False
    return True


def _mechanism_merge(clusters: list, policy) -> list:
    """Pass 2: merge clusters that agree on driver, mechanism and outcome even when they share
    no wording. This is the half that fixes FRAGMENTATION — two long, differently-worded
    descriptions of one theme have no tokens in common and pass 1 will never join them.

    Runs to a fixpoint over a deterministically ordered list, so merges compose transitively.
    """
    merged = True
    while merged:
        merged = False
        clusters.sort(key=lambda c: c.key)
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                a, b = clusters[i], clusters[j]
                if _blocked(frozenset(a.tokens), frozenset(b.tokens), policy):
                    continue
                if _mechanism_match(a, b, policy):
                    a.absorb(b)
                    clusters.pop(j)
                    merged = True
                    break
            if merged:
                break
    return clusters


# ── attribution + scoring ────────────────────────────────────────────────────
def _build_cluster(idx, cl, classes, temporals, bundles_by_slug, slug_cluster_counts,
                   atoms_by_id, elig_by_slug, policy) -> ThemeCluster:
    cluster_id = f"tc-{idx:03d}"
    members: list[ThemeClusterMember] = []
    by_source: dict[str, list] = {}
    for it in cl.items:
        by_source.setdefault(it.slug, []).append(it)

    cluster_tokens = frozenset(cl.tokens)
    cluster_anchors = frozenset(cl.anchors)
    evidence_ids: set = set()
    current_evidence_ids: set = set()    # PART 5: only current-input evidence corroborates
    attrs: list[SourceAttribution] = []
    hot_sources = 0
    bullets: list[EvidenceBullet] = []
    op_axes: set = set()
    fam_hints: set = set()
    causal: set = set()
    confounders: set = set()
    falsifiers: set = set()

    for slug, items in by_source.items():
        sc = classes.get(slug)
        tc = temporals.get(slug)
        role = tc.temporal_role if tc else None
        cur, klass = elig_by_slug.get(slug, (True, "current"))
        ev = sorted({e for it in items for e in it.evidence_ids if e})
        evidence_ids.update(ev)
        if klass == "current":
            current_evidence_ids.update(ev)
        from_hot = any(it.from_hot for it in items)
        if from_hot:
            hot_sources += 1
        for it in items:
            members.append(ThemeClusterMember(
                source_slug=slug, original_theme_name=it.raw_name,
                evidence_ids=it.evidence_ids, temporal_role=role,
                # the SAME metric the merge decision used, so a reader can see why it merged.
                # Under the old overlap coefficient this was 1.000 for every member (each
                # member's tokens are a subset of the cluster union), which said nothing.
                similarity_score=round(_weighted_jaccard(
                    it.tokens, cluster_tokens, it.anchors | cluster_anchors,
                    policy.alias_anchor_weight), 3),
                from_hot_topic=it.from_hot, is_current_input=cur,
                rationale="alias-anchored weighted Jaccard against the cluster",
            ))
        # contribution type from the firewall klass (PART 5)
        if klass == "method":
            contrib = "method_context"
        elif klass == "historical":
            contrib = "historical_analogue"
        elif ev and cur:
            contrib = "supports"
        elif from_hot and not ev:
            contrib = "mentions_only"
        else:
            contrib = "supports" if cur else "mentions_only"
        weight = 1.0
        if klass == "method":
            weight = 0.0
        elif klass == "historical":
            weight = policy.historical_source_discount
        elif contrib == "mentions_only":
            weight = policy.same_publisher_discount
        rationale = {
            "supports": f"supports via {len(ev)} source-backed evidence atom(s)",
            "mentions_only": "mentions only; high attention but weak (no source-backed) evidence",
            "historical_analogue": "historical analogue; cannot corroborate a current theme",
            "method_context": "method/taxonomy context only; not market evidence",
            "contradicts": "contradicts the theme",
        }.get(contrib, f"{slug} [{klass}] contributes {len(items)} candidate(s)")
        attrs.append(SourceAttribution(
            source_slug=slug, source_type=(sc.source_type if sc else "other"),
            access_class=(sc.access_class if sc else "method"),
            temporal_role=role, is_current_input=cur, evidence_ids=ev,
            contribution_type=contrib,
            independence_group=policy.publisher_groups.get(slug),
            source_weight=weight, rationale=rationale,
        ))
        # enrichment from this source's bundle when it feeds this cluster. Attach an item when
        # its evidence/tokens link to the cluster OR the source feeds exactly ONE cluster (then
        # attribution is unambiguous — e.g. a proxy axis that shares no surface tokens). v1 rule.
        b = bundles_by_slug.get(slug)
        single = slug_cluster_counts.get(slug, 1) == 1
        if b is not None:
            for ax in b.operational_axes:
                if single or (set(ax.source_evidence_ids) & set(ev)) or \
                   (_normalize(ax.axis_name, policy.alias_map)[1] & cluster_tokens):
                    op_axes.add(ax.axis_name)
            for fh in b.strategy_family_hints:
                if single or (set(fh.source_evidence_ids) & set(ev)):
                    fam_hints.add(fh.family)
            for cc in b.causal_claims:
                if single or (set(cc.source_evidence_ids) & set(ev)):
                    causal.add(f"{cc.driver} → {cc.outcome}")
            if single:
                confounders.update(b.confounders)
                falsifiers.update(b.falsifiers)

    # ── PART 4 scores (deterministic; all weights on policy) ──
    # Evidence bullets — one per linked atom, formatted [claim_kind | location | evidence_id] claim.
    for eid in sorted(evidence_ids):
        a = atoms_by_id.get(eid)
        if a is None:
            continue
        kind = a.claim_kind or a.claim_type or "claim"
        loc = a.source_location or "source"
        bullets.append(EvidenceBullet(
            text=f"[{kind} | {loc} | {eid}] {a.claim}",
            evidence_ids=[eid], source_slugs=[a.source_slug] if a.source_slug else []))

    # PART 5: corroboration counts only CURRENT-input sources (method/historical excluded).
    current_slugs = {a.source_slug for a in attrs if a.contribution_type == "supports"
                     and a.is_current_input}
    source_count = len(by_source)
    groups = {policy.publisher_groups.get(s, s) for s in current_slugs}
    independent_source_count = len(groups)
    evidence_count = len(current_evidence_ids)
    contradiction_count = sum(1 for a in attrs if a.contribution_type == "contradicts")
    has_axis = bool(op_axes)
    has_causal = bool(causal)
    source_types = {a.source_type for a in attrs if a.contribution_type == "supports"}

    # corroboration: independent sources + source-backed atoms + evidence quality + causal
    # completeness + axis availability + source-type diversity (PART 4).
    confs = [atoms_by_id[e].confidence for e in current_evidence_ids if e in atoms_by_id]
    evidence_quality = (sum(confs) / len(confs)) if confs else 0.0
    corroboration = (
        (independent_source_count - 1) * policy.independent_source_bonus
        + min(evidence_count, policy.evidence_cap) * policy.source_fact_weight
        + evidence_quality * policy.evidence_quality_weight
        + (policy.axis_availability_weight if has_axis else 0.0)
        + (policy.causal_completeness_weight if has_causal else 0.0)
        + (policy.diversity_weight if len(source_types) > 1 else 0.0)
    )
    corroboration = max(0.0, min(1.0, corroboration))

    # attention: hot-topic language + buzz terms + mentions-without-evidence + crowding from
    # non-independent sources (PART 4).
    buzz = 1.0 if (frozenset(cluster_tokens) & _BUZZ_TERMS) else 0.0
    no_ev_frac = (sum(1 for m in members if not m.evidence_ids) / len(members)
                  if members else 0.0)
    non_indep_frac = ((source_count - independent_source_count) / source_count
                      if source_count else 0.0)
    attention = (
        policy.hot_topic_weight * (hot_sources / source_count if source_count else 0.0)
        + policy.attention_keyword_weight * buzz
        + policy.mention_without_evidence_weight * no_ev_frac
        + policy.non_independent_weight * non_indep_frac
    )
    attention = max(0.0, min(policy.max_attention_penalty, attention))

    recencies = [_RECENCY.get(temporals[s].temporal_role if s in temporals else None, 0.7)
                 for s in by_source]
    recency = sum(recencies) / len(recencies) if recencies else 0.0
    current_sources = sum(1 for a in attrs if a.is_current_input)
    temporal_quality = current_sources / source_count if source_count else 0.0
    divergence = corroboration - attention
    promotion = (
        0.5 * corroboration + 0.3 * divergence + 0.2 * temporal_quality
        + (policy.axis_availability_weight if has_axis else 0.0)
        + (policy.causal_completeness_weight if has_causal else 0.0)
        - policy.contradiction_penalty * contradiction_count
    )
    promotion = max(-1.0, min(1.0, promotion))

    # ── status routing (precedence) ──
    has_current_support = any(
        a.is_current_input and a.contribution_type == "supports" and a.evidence_ids
        for a in attrs)
    all_historical = bool(attrs) and all(
        a.contribution_type == "historical_analogue" for a in attrs)
    all_method = bool(attrs) and all(a.contribution_type == "method_context" for a in attrs)
    status = _route_status(
        has_current_support, all_historical, all_method, has_axis, promotion, temporal_quality,
        attrs, policy)

    canonical = max(members, key=lambda m: (len(m.evidence_ids), len(m.original_theme_name)))
    warnings = []
    if status == "promote_to_discovery" and not op_axes:
        warnings.append("promoted without an operational axis candidate")
    if len([a for a in attrs if a.contribution_type == "supports"]) == 1:
        warnings.append("single-source theme — source concentration; corroboration is weak")
    missing = []
    if not evidence_ids:
        missing.append("no source-backed evidence atoms linked to this theme")
    if not op_axes:
        missing.append("no operational axis candidate")

    return ThemeCluster(
        cluster_id=cluster_id,
        canonical_theme_name=canonical.original_theme_name,
        canonical_thesis=f"{canonical.original_theme_name} — corroborated across "
                         f"{independent_source_count} independent source(s).",
        theme_status=status, members=members, source_attributions=attrs,
        evidence_ids=sorted(evidence_ids), evidence_bullets=bullets,
        source_count=source_count, independent_source_count=independent_source_count,
        evidence_count=evidence_count, contradiction_count=contradiction_count,
        attention_score=round(attention, 4), corroboration_score=round(corroboration, 4),
        recency_score=round(recency, 4), temporal_quality=round(temporal_quality, 4),
        evidence_attention_divergence=round(divergence, 4),
        promotion_score=round(promotion, 4),
        operational_axes=sorted(op_axes), causal_claims=sorted(causal),
        confounders=sorted(confounders), falsifiers=sorted(falsifiers),
        strategy_family_hints=sorted(fam_hints), missing_data=missing, warnings=warnings,
    )


def _route_status(has_current_support, all_historical, all_method, has_axis, promotion,
                  temporal_quality, attrs, policy) -> str:
    if not any(a.evidence_ids for a in attrs) and all(
            a.contribution_type == "mentions_only" for a in attrs):
        return "reject"
    if all_historical:   # PART 5 rule 4: historical CASE → historical/outcome, never promote
        if any(a.temporal_role == "outcome_candidate" for a in attrs):
            return "outcome_candidate"
        return "historical_case"
    if all_method:       # PART 5 rule 3: METHOD is taxonomy only, not market evidence
        return "needs_more_evidence"
    if (has_current_support and has_axis
            and promotion >= policy.min_promote_score
            and temporal_quality >= policy.promote_min_temporal):
        return "promote_to_discovery"
    if has_current_support:
        return "watchlist"
    return "needs_more_evidence"


# ── public entry point ───────────────────────────────────────────────────────
def aggregate_theme_candidates(
    bundles: list[EvidenceExtractionBundle],
    source_classifications: list[SourceClassification],
    temporal_contexts: Optional[list[TemporalContext]] = None,
    policy: Optional[ThemeAggregationPolicy] = None,
) -> MultiSourceThemeSet:
    policy = policy or ThemeAggregationPolicy()
    classes = {c.source_slug: c for c in source_classifications}
    temporals = {t.source_slug: t for t in (temporal_contexts or [])}
    bundles_by_slug = {b.source_slug: b for b in bundles}
    atoms_by_id = {a.evidence_id: a for b in bundles for a in b.evidence_atoms if a.evidence_id}

    # PART 5 firewall: classify every source; DROP archived CASE that is not in the current
    # batch (rule 2) before any clustering — it never touches fresh Phase-A aggregation.
    elig_by_slug: dict = {}
    warnings: list[str] = []
    eligible_bundles: list = []
    for b in bundles:
        cur, klass = _eligibility(b.source_slug, classes.get(b.source_slug),
                                  temporals.get(b.source_slug), policy)
        elig_by_slug[b.source_slug] = (cur, klass)
        if klass == "archived_case_blocked":
            warnings.append(
                f"archived CASE source '{b.source_slug}' excluded from Phase-A aggregation "
                "(not in current_input_slugs; pass it as current input to include it)."
            )
            continue
        eligible_bundles.append(b)

    items: list[_Item] = []
    for b in eligible_bundles:
        items.extend(_collect_items(b, policy.alias_map))

    clusters_raw, rejected = _cluster_items(items, policy)
    # how many clusters each source feeds (drives the single-cluster unambiguous attach rule)
    slug_cluster_counts: dict = {}
    for cl in clusters_raw:
        for s in {it.slug for it in cl.items}:
            slug_cluster_counts[s] = slug_cluster_counts.get(s, 0) + 1
    # keep each built cluster paired with its raw items so the duplicate map survives sorting
    built = [
        (_build_cluster(i, cl, classes, temporals, bundles_by_slug, slug_cluster_counts,
                        atoms_by_id, elig_by_slug, policy), cl)
        for i, cl in enumerate(clusters_raw)
    ]
    built.sort(key=lambda pair: pair[0].promotion_score, reverse=True)
    clusters = [b for b, _ in built]

    # (L3) parent cap — keep the top `parent_cap` by promotion_score; demote the tail to watchlist.
    # Default None => no cap (GM-neutral). Demotions are logged; nothing is dropped.
    if policy.parent_cap is not None and len(clusters) > policy.parent_cap:
        demoted = 0
        capped = []
        for idx, c in enumerate(clusters):
            if idx >= policy.parent_cap and c.theme_status != "watchlist":
                capped.append(c.model_copy(update={"theme_status": "watchlist"}))
                demoted += 1
            else:
                capped.append(c)
        clusters = capped
        if demoted:
            warnings.append(
                f"parent_cap={policy.parent_cap}: demoted {demoted} cluster(s) beyond the cap to "
                f"watchlist (tail by promotion_score); none dropped")

    slugs = sorted(bundles_by_slug)
    batch_id = "batch-" + hashlib.sha1("|".join(slugs).encode()).hexdigest()[:10]
    duplicate_theme_map = {it.norm: b.cluster_id for b, cl in built for it in cl.items}

    return MultiSourceThemeSet(
        batch_id=batch_id,
        source_scope=policy.source_scope or _infer_scope(temporals, slugs),
        source_slugs=slugs, clusters=clusters, rejected_merges=rejected,
        duplicate_theme_map=duplicate_theme_map, warnings=warnings,
    )


def _infer_scope(temporals: dict, slugs: list) -> str:
    roles = [temporals[s].temporal_role if s in temporals else None for s in slugs]
    if all(r in ("current_report", None) for r in roles):
        return "explicit_current_batch"
    if all(r == "method_source" for r in roles):
        return "all_method_sources"
    if all(r in ("historical_case", "stale_case", "outcome_candidate") for r in roles):
        return "historical_case_batch"
    return "mixed_batch"
