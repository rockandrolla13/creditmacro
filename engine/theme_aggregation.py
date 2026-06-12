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
from engine.wiki_agents import SourceClassification

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


@dataclass
class ThemeAggregationPolicy:
    similarity_threshold: float = 0.5      # overlap-coefficient cut to merge
    alias_map: dict = field(default_factory=lambda: dict(_DEFAULT_ALIASES))
    distinct_pairs: list = field(default_factory=lambda: list(_DEFAULT_DISTINCT_PAIRS))
    publisher_groups: dict = field(default_factory=dict)   # source_slug -> independence group
    # scoring weights
    w_independent: float = 0.35
    w_evidence: float = 0.12
    evidence_cap: int = 5
    # promotion thresholds
    promote_min_divergence: float = 0.0
    promote_min_temporal: float = 0.5
    source_scope: Optional[str] = None      # override the inferred scope


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


def _overlap(a: frozenset, b: frozenset) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def _matches_side(tokens: frozenset, side: frozenset) -> bool:
    return len(tokens & side) >= 2


def _distinct_blocked(ta: frozenset, tb: frozenset, pairs) -> bool:
    for s1, s2 in pairs:
        if (_matches_side(ta, s1) and _matches_side(tb, s2)) or \
           (_matches_side(ta, s2) and _matches_side(tb, s1)):
            return True
    return False


# ── per-source temporal/classification helpers ───────────────────────────────
_RECENCY = {
    "current_report": 1.0, "method_source": 0.5, "stale_case": 0.2,
    "historical_case": 0.1, "outcome_candidate": 0.1, "unknown": 0.3, None: 0.7,
}
_CURRENT_ROLES = {"current_report", None}   # treated as current input by default


def _is_current(role: Optional[str]) -> bool:
    return role in _CURRENT_ROLES


# ── raw item collection ──────────────────────────────────────────────────────
@dataclass
class _Item:
    slug: str
    raw_name: str
    norm: str
    tokens: frozenset
    from_hot: bool
    evidence_ids: list


def _collect_items(bundle: EvidenceExtractionBundle, alias_map: dict) -> list[_Item]:
    """Theme candidates from one bundle: core themes, hot topics, theme-like causal claims
    and developments. Evidence is linked via EvidenceAtom.themes (normalised match)."""
    # index atom evidence ids by normalised theme name they declare support for
    atoms_by_theme: dict[str, list] = {}
    for atom in bundle.evidence_atoms:
        for th in (atom.themes or []):
            norm, _ = _normalize(th, alias_map)
            atoms_by_theme.setdefault(norm, []).append(atom.evidence_id)

    raw: list[tuple[str, bool]] = []
    raw += [(t, False) for t in bundle.core_theme_candidates]
    raw += [(t, True) for t in bundle.hot_topics]
    raw += [(f"{c.driver} {c.outcome}", False) for c in bundle.causal_claims]
    raw += [(d, False) for d in bundle.main_developments if len(d.split()) >= 3]

    # dedupe per (source, normalised name); from_hot = OR over raw items
    merged: dict[str, _Item] = {}
    for name, is_hot in raw:
        norm, toks = _normalize(name, alias_map)
        if not toks:
            continue
        if norm in merged:
            merged[norm].from_hot = merged[norm].from_hot or is_hot
        else:
            merged[norm] = _Item(
                slug=bundle.source_slug, raw_name=name, norm=norm, tokens=toks,
                from_hot=is_hot, evidence_ids=list(atoms_by_theme.get(norm, [])),
            )
    return list(merged.values())


# ── clustering ───────────────────────────────────────────────────────────────
@dataclass
class _Cluster:
    tokens: frozenset
    items: list


def _cluster_items(items: list, policy: ThemeAggregationPolicy):
    clusters: list[_Cluster] = []
    rejected: list[dict] = []
    for it in items:
        best = None
        best_sim = 0.0
        for cl in clusters:
            if _distinct_blocked(it.tokens, cl.tokens, policy.distinct_pairs):
                continue
            sim = _overlap(it.tokens, cl.tokens)
            if sim > best_sim:
                best_sim, best = sim, cl
        if best is not None and best_sim >= policy.similarity_threshold:
            best.items.append(it)
            best.tokens = best.tokens | it.tokens
        else:
            clusters.append(_Cluster(tokens=set(it.tokens), items=[it]))
    # record related-but-distinct near misses across the final clusters
    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            if _distinct_blocked(frozenset(clusters[i].tokens),
                                 frozenset(clusters[j].tokens), policy.distinct_pairs):
                rejected.append({
                    "theme_a": clusters[i].items[0].norm,
                    "theme_b": clusters[j].items[0].norm,
                    "reason": "distinct_marker_guard: related but structurally distinct themes",
                })
    return clusters, rejected


# ── attribution + scoring ────────────────────────────────────────────────────
def _build_cluster(idx, cl, classes, temporals, bundles_by_slug, slug_cluster_counts,
                   policy) -> ThemeCluster:
    cluster_id = f"tc-{idx:03d}"
    members: list[ThemeClusterMember] = []
    by_source: dict[str, list] = {}
    for it in cl.items:
        by_source.setdefault(it.slug, []).append(it)

    cluster_tokens = frozenset(cl.tokens)
    evidence_ids: set = set()
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
        cur = _is_current(role)
        ev = sorted({e for it in items for e in it.evidence_ids if e})
        evidence_ids.update(ev)
        from_hot = any(it.from_hot for it in items)
        if from_hot:
            hot_sources += 1
        for it in items:
            members.append(ThemeClusterMember(
                source_slug=slug, original_theme_name=it.raw_name,
                evidence_ids=it.evidence_ids, temporal_role=role,
                similarity_score=round(_overlap(it.tokens, cluster_tokens), 3),
                from_hot_topic=it.from_hot, is_current_input=cur,
                rationale="token/alias overlap with cluster",
            ))
        # contribution type
        if role in ("historical_case", "stale_case", "outcome_candidate"):
            contrib = "historical_analogue"
        elif (sc and sc.access_class == "method") and role == "method_source":
            contrib = "method_context"
        elif ev and cur:
            contrib = "supports"
        elif from_hot and not ev:
            contrib = "mentions_only"
        else:
            contrib = "supports" if cur else "mentions_only"
        attrs.append(SourceAttribution(
            source_slug=slug, source_type=(sc.source_type if sc else "other"),
            access_class=(sc.access_class if sc else "method"),
            temporal_role=role, is_current_input=cur, evidence_ids=ev,
            contribution_type=contrib,
            independence_group=policy.publisher_groups.get(slug),
            source_weight=(0.5 if contrib in ("historical_analogue", "mentions_only") else 1.0),
            rationale=f"{slug} contributes {len(items)} candidate(s)",
        ))
        if ev:
            bullets.append(EvidenceBullet(
                text=f"{slug}: {items[0].raw_name}", evidence_ids=ev, source_slugs=[slug]))
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

    # ── scores (deterministic; weights on policy) ──
    source_count = len(by_source)
    groups = {policy.publisher_groups.get(s, s) for s in by_source}
    independent_source_count = len(groups)
    evidence_count = len(evidence_ids)
    contradiction_count = sum(1 for a in attrs if a.contribution_type == "contradicts")

    corroboration = min(1.0, (independent_source_count - 1) * policy.w_independent
                        + min(evidence_count, policy.evidence_cap) * policy.w_evidence)
    attention = hot_sources / source_count if source_count else 0.0
    recencies = [_RECENCY.get(temporals[s].temporal_role if s in temporals else None, 0.7)
                 for s in by_source]
    recency = sum(recencies) / len(recencies) if recencies else 0.0
    current_sources = sum(1 for s in by_source
                          if _is_current(temporals[s].temporal_role if s in temporals else None))
    temporal_quality = current_sources / source_count if source_count else 0.0
    divergence = corroboration - attention
    promotion = max(-1.0, min(1.0, divergence)) * temporal_quality * (1.0 if op_axes else 0.5)

    # ── status routing (precedence) ──
    has_current_support = any(
        a.is_current_input and a.contribution_type == "supports" and a.evidence_ids
        for a in attrs)
    all_historical = all(not a.is_current_input for a in attrs)
    status = _route_status(
        has_current_support, all_historical, bool(op_axes), divergence, temporal_quality,
        evidence_count, attrs, policy)

    canonical = max(members, key=lambda m: (len(m.evidence_ids), len(m.original_theme_name)))
    warnings = []
    if status == "promote_to_discovery" and not op_axes:
        warnings.append("promoted without an operational axis candidate")
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


def _route_status(has_current_support, all_historical, has_axis, divergence,
                  temporal_quality, evidence_count, attrs, policy) -> str:
    if not any(a.evidence_ids for a in attrs) and all(
            a.contribution_type == "mentions_only" for a in attrs):
        return "reject"
    if all_historical:
        if any(a.temporal_role == "outcome_candidate" for a in attrs):
            return "outcome_candidate"
        return "historical_case"
    if (has_current_support and has_axis
            and divergence >= policy.promote_min_divergence
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

    items: list[_Item] = []
    for b in bundles:
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
                        policy), cl)
        for i, cl in enumerate(clusters_raw)
    ]
    built.sort(key=lambda pair: pair[0].promotion_score, reverse=True)
    clusters = [b for b, _ in built]

    slugs = sorted(bundles_by_slug)
    batch_id = "batch-" + hashlib.sha1("|".join(slugs).encode()).hexdigest()[:10]
    duplicate_theme_map = {it.norm: b.cluster_id for b, cl in built for it in cl.items}

    return MultiSourceThemeSet(
        batch_id=batch_id,
        source_scope=policy.source_scope or _infer_scope(temporals, slugs),
        source_slugs=slugs, clusters=clusters, rejected_merges=rejected,
        duplicate_theme_map=duplicate_theme_map, warnings=[],
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
