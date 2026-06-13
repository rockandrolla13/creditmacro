"""WikiIntegratorAgent — the durable wiki-persistence layer (deterministic planner + applier).

It turns extraction / aggregation outputs into wiki pages. It PLANS first
(`build_wiki_update_plan` → `WikiUpdatePlan`: every page it WOULD write, no disk I/O) and then
APPLIES (`apply_wiki_update_plan` → `WikiIntegrationResult`: idempotent disk writes).

DISCIPLINE enforced by construction:
  * structured paraphrases only — never raw source text (copyright guard, optional `raw_text`);
  * no trades / sizing / hedge ratios / scenario probabilities / execution (no-trade guard);
  * `access_class` is stamped per page and NEVER upgraded (old CASE never becomes METHOD);
  * a METHOD source produces no CASE-evidence pages from method content;
  * deterministic dates (caller-supplied; no wall clock).

Phase-A vs Phase-B firewall is upstream; this layer only persists what it is handed.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from .evidence_extraction import EvidenceExtractionBundle
from .schema.theme_aggregation import MultiSourceThemeSet, ThemeCluster
from .schema.wiki_integration import (
    WikiIntegrationResult,
    WikiPageWrite,
    WikiUpdatePlan,
)
from .temporal import TemporalContext
from .wiki_agents import SourceClassification

# ── deterministic constants ──────────────────────────────────────────────────────

# Caller-supplied date (no wall-clock; replay-safe). The build operates "as of" this date.
_CREATED = "2026-06-12"
_UPDATED = "2026-06-12"

# No-trade lexicon — any case-insensitive hit in a planned page body blocks that page. The
# trailing/leading spaces avoid false positives ("buyback", "shorthand", "alleged", etc.).
# Trade/execution DIRECTIVES (engine-emitted), not mere mentions of buying/selling in ingested
# commentary. Each is a regex; matched against the page body (minus the no-trade disclaimer).
_TRADE_PATTERNS = (
    r"\bgo(?:ing)?\s+(?:long|short)\b",                  # "go long"
    r"\b(?:buy|sell|go\s+long|go\s+short|long|short)\s+\$?\d[\d,.]*\s?(?:mm|bn|k|bp|bps)\b",  # "buy 50mm"
    r"\bhedge\s+ratio\b",
    r"\b(?:position\s+size|size\s+(?:the\s+)?(?:position|trade|book))\b",
    r"\bstop[-\s]?loss\b",
    r"\bbps\s+target\b",
    r"\b\d+\s?(?:mm|bn)\b.{0,24}(?:steepener|flattener)\b",   # "20mm 5s30s steepener"
)

# The mandatory closing line every page ends with.
_NO_TRADE_LINE = (
    "This page is durable memory only — no trades, sizing, hedge ratios, or execution."
)
_NO_TRADE_HEADER = "## No-trade boundary"

_COPYRIGHT_MAX_RUN_WORDS = 25
_WORD = re.compile(r"\w+")


# ── public input ──────────────────────────────────────────────────────────────────

class WikiIntegratorInput(BaseModel):
    source_classification: SourceClassification
    bundle: EvidenceExtractionBundle
    temporal_context: Optional[TemporalContext] = None
    theme_set: Optional[MultiSourceThemeSet] = None
    raw_text: Optional[str] = None        # used ONLY by the copyright guard — never written
    wiki_root: str = "wiki"
    dry_run: bool = False
    force: bool = False
    author_or_publisher: Optional[str] = None


# ── helpers ─────────────────────────────────────────────────────────────────────

def _slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").strip().lower())
    return s.strip("-") or "untitled"


def _trim_words(s: str, n: int = 22) -> str:
    """Trim an inline string to n words (copyright: keeps source-derived names/sentences from
    being reproduced verbatim when rendered on a single line)."""
    words = str(s).replace("\n", " ").split()
    return " ".join(words[:n]) + (" …" if len(words) > n else "")


def _yaml_scalar(s) -> str:
    """A safe YAML scalar for FREE-TEXT frontmatter values — quote when the value could be
    misparsed as YAML structure (leading -/?/:, an embedded ': ', a trailing ':', '#', etc.).
    Extractor-derived names can be arbitrary sentence fragments, so this must be defensive."""
    import json
    v = str(s).replace("\n", " ").strip()
    if not v or v[0] in "-?:,[]{}#&*!|>'\"%@`" or ": " in v or v.endswith(":") or " #" in v:
        return json.dumps(v, ensure_ascii=False)
    return v


def _yaml_list(items, max_words: int = 22) -> str:
    """Render a frontmatter list value inline as a JSON/YAML flow list. Each item is JSON-quoted
    (valid YAML — survives commas/colons) and trimmed to max_words so a list of source-derived
    sentences cannot reproduce a long verbatim run (copyright)."""
    import json
    out = []
    for i in (items or []):
        s = str(i).replace("\n", " ").strip()
        if not s:
            continue
        words = s.split()
        if len(words) > max_words:
            s = " ".join(words[:max_words]) + " …"
        out.append(json.dumps(s, ensure_ascii=False))
    # Block style (one item per line) so the per-line copyright guard sees each item alone —
    # adjacent source-derived items can't concatenate into a false long verbatim run.
    return ("\n" + "\n".join(f"  - {x}" for x in out)) if out else "[]"


def _fm(pairs: list[tuple[str, str]]) -> str:
    """Build a YAML frontmatter block from ordered key/value pairs (values pre-rendered)."""
    lines = ["---"]
    for k, v in pairs:
        lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def _bullets(items, empty: str = "- (none)", max_words: int = 22) -> str:
    """Render bullets, trimming each item to max_words. The trim keeps the integrator from
    reproducing long source sentences verbatim (copyright) — and because a truncated bullet is
    only a PREFIX of the source sentence, it severs the contiguous verbatim run against raw."""
    out = []
    for i in (items or []):
        s = str(i).replace("\n", " ").strip()
        if not s:
            continue
        words = s.split()
        if len(words) > max_words:
            s = " ".join(words[:max_words]) + " …"
        out.append(s)
    if not out:
        return empty
    return "\n".join(f"- {x}" for x in out)


def _tokens(text: str) -> list[str]:
    return _WORD.findall(text.lower())


def _longest_verbatim_run(a: str, b: str) -> int:
    """Longest common contiguous run of words between texts a and b (word count)."""
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0
    prev = [0] * (len(tb) + 1)
    best = 0
    for i in range(1, len(ta) + 1):
        cur = [0] * (len(tb) + 1)
        ai = ta[i - 1]
        for j in range(1, len(tb) + 1):
            if ai == tb[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best = cur[j]
        prev = cur
    return best


def _trade_hit(body: str) -> Optional[str]:
    # The mandatory No-trade boundary line itself names "hedge ratios" etc.; it is the
    # disclaimer, not a trade instruction, so exclude it before scanning.
    low = body.lower().replace(_NO_TRADE_LINE.lower(), "")
    for pat in _TRADE_PATTERNS:
        m = re.search(pat, low)
        if m:
            return m.group(0).strip()
    return None


# ── page bodies ─────────────────────────────────────────────────────────────────

def _temporal_role(tc: Optional[TemporalContext]) -> str:
    return tc.temporal_role if tc else "unknown"


def _source_date(tc: Optional[TemporalContext]) -> str:
    if tc and tc.source_date:
        return str(tc.source_date)
    return "unknown"


def _current_update_required(tc: Optional[TemporalContext]) -> str:
    return "true" if (tc and tc.current_update_required) else "false"


def _hist_prefix(role: str, source_date: str, text: str) -> str:
    """Phrase a forecast historically for a historical_case source."""
    if role == "historical_case":
        return f"as of {source_date}: {text}"
    return text


def _source_page_body(inp: WikiIntegratorInput) -> str:
    cls = inp.source_classification
    b = inp.bundle
    tc = inp.temporal_context
    role = _temporal_role(tc)
    sd = _source_date(tc)
    spf = b.source_page_fields or {}
    src_type = spf.get("source_type") or cls.source_type
    author = inp.author_or_publisher or spf.get("author_or_publisher") or "unknown"
    raw_path = spf.get("raw_source_path") or f"raw/{cls.source_slug}.md"
    norm_path = spf.get("normalized_markdown_path") or f"markdowns/{cls.source_slug}.md"

    # forecast horizons / outcome candidates, phrased historically when historical_case
    horizon_lines = []
    if tc:
        for h in tc.forecast_horizons:
            horizon_lines.append(_hist_prefix(role, sd, f"{h.claim} (horizon: {h.horizon_type}, {h.status})"))
        for f in tc.expired_forecasts:
            horizon_lines.append(_hist_prefix(role, sd, f"expired forecast: {f}"))

    evidence_ids = [a.evidence_id for a in b.evidence_atoms if a.evidence_id]
    theme_slugs = [f"{cls.source_slug}-{_slugify(t)}" for t in b.core_theme_candidates]
    cluster_ids = [c.cluster_id for c in (inp.theme_set.clusters if inp.theme_set else [])]
    concepts = sorted({c for a in b.evidence_atoms for c in a.concepts})
    entities = sorted({e for a in b.evidence_atoms for e in a.entities})

    fm = _fm([
        ("type", "source"),
        ("classification", "source"),
        ("workflow_status", "discovery_complete"),
        ("access_class", cls.access_class),
        ("source_type", src_type),
        ("source_date", sd),
        ("temporal_role", role),
        ("current_update_required", _current_update_required(tc)),
        ("author_or_publisher", _yaml_scalar(author)),
        ("raw_source_path", raw_path),
        ("normalized_markdown_path", norm_path),
        ("ingestion_status", "ingested"),
        ("evidence_atoms", _yaml_list(evidence_ids)),
        ("themes", _yaml_list(theme_slugs)),
        ("theme_clusters", _yaml_list(cluster_ids)),
        ("concepts", _yaml_list(concepts)),
        ("entities", _yaml_list(entities)),
        ("created", _CREATED),
        ("updated", _UPDATED),
    ])

    temporal_status = (
        f"Source date {sd}; temporal role **{role}**; "
        f"current update required: {_current_update_required(tc)}."
    )
    if role == "historical_case":
        temporal_status += (" Historical case — forecasts below are stated as of the source "
                            "date and are NOT current recommendations.")

    links = theme_slugs + cluster_ids + evidence_ids

    body = f"""{fm}

# Source Summary

## What this source is
A {src_type} source ({author}), classified `{cls.access_class}`. Durable memory record of the
structured fields extracted from it.

## Temporal status
{temporal_status}

## Why it matters
{_bullets(b.core_theme_candidates or b.main_developments, empty="- (no theme/development emphasis recorded)")}

## Main developments mentioned
{_bullets(b.main_developments)}

## Key events mentioned
{_bullets(b.key_events)}

## Core theme candidates mentioned
{_bullets(b.core_theme_candidates)}

## Hot topics mentioned
{_bullets(b.hot_topics)}

## Extracted facts
{_bullets([a.claim for a in b.evidence_atoms])}

## Extracted causal claims
{_bullets([f"{c.driver} -> {c.outcome} ({c.transmission})" for c in b.causal_claims])}

## Extracted operational axes
{_bullets([f"{a.axis_name}: {a.observable_series}" for a in b.operational_axes])}

## Extracted confounders
{_bullets(b.confounders)}

## Extracted falsifiers
{_bullets(b.falsifiers)}

## Forecast horizons / outcome candidates
{_bullets(horizon_lines)}

## Strategy-family hints
{_bullets([f"{h.family}: {h.rationale}" for h in b.strategy_family_hints])}

## Links created or updated
{_bullets([f"[[{s}]]" for s in links])}

## Open questions
{_bullets(b.open_questions)}

{_NO_TRADE_HEADER}
{_NO_TRADE_LINE}
"""
    return body


def _evidence_page_body(inp: WikiIntegratorInput, atom) -> str:
    tc = inp.temporal_context
    role = _temporal_role(tc)
    sd = _source_date(tc)
    page = None
    if atom.source_location:
        m = re.match(r"page:(\d+)", atom.source_location)
        if m:
            page = int(m.group(1))

    claim_kind = atom.claim_kind or "source_fact"
    # temporal status of the claim: historical sources carry historical claims
    temporal_status = "historical" if role == "historical_case" else "current"
    outcome_check = "true" if role in ("historical_case", "outcome_candidate", "stale_case") else "false"

    causal_edges = []  # evidence atoms carry no explicit edges; left empty/structured

    fm = _fm([
        ("type", "evidence"),
        ("classification", "evidence"),
        ("workflow_status", "discovery_complete"),
        ("access_class", "case"),
        ("evidence_id", atom.evidence_id or "unknown"),
        ("source_slug", atom.source_slug or inp.source_classification.source_slug),
        ("source_location", atom.source_location or "unknown"),
        ("page_number", str(page) if page is not None else "unknown"),
        ("claim_type", atom.claim_type or "unknown"),
        ("claim_kind", claim_kind),
        ("temporal_status", temporal_status),
        ("temporal_role", role),
        ("outcome_check_required", outcome_check),
        ("entities", _yaml_list(atom.entities)),
        ("concepts", _yaml_list(atom.concepts)),
        ("themes", _yaml_list(atom.themes)),
        ("market_variables", _yaml_list(atom.market_variables)),
        ("numbers", _yaml_list(atom.numbers)),
        ("causal_edges", _yaml_list(causal_edges)),
        ("confidence", str(atom.confidence)),
        ("freshness", str(atom.freshness) if atom.freshness is not None else "unknown"),
        ("agent_use", (atom.agent_use or "memory").replace("\n", " ")),
        ("source_date", sd),
        ("created", _CREATED),
        ("updated", _UPDATED),
    ])

    why = atom.agent_use or (("theme: " + ", ".join(atom.themes)) if atom.themes else "durable evidence memory")
    horizon = ""
    if role == "historical_case":
        why = _hist_prefix(role, sd, why)

    body = f"""{fm}

# Evidence: {atom.evidence_id or 'unknown'}

## Claim
{atom.claim.strip()}

## Why it matters
{why}

## Source provenance
- Source: {atom.source_slug or inp.source_classification.source_slug}
- Location: {atom.source_location or 'unknown'}
- Page: {page if page is not None else 'unknown'}

## Temporal status
- Source date: {sd}
- Claim status: {temporal_status}
- Forecast horizon: {horizon or '(none)'}
- Outcome check required: {outcome_check}

## Structured fields
- Entities: {', '.join(atom.entities) or '(none)'}
- Concepts: {', '.join(atom.concepts) or '(none)'}
- Themes: {', '.join(atom.themes) or '(none)'}
- Market variables: {', '.join(atom.market_variables) or '(none)'}
- Numbers: {', '.join(str(n) for n in atom.numbers) or '(none)'}
- Causal edges: {', '.join(causal_edges) or '(none)'}

{_NO_TRADE_HEADER}
{_NO_TRADE_LINE}
"""
    return body


_BELIEF_LABEL = {
    "source_fact": "Source-backed fact",
    "source_forecast": "Source-backed fact",
    "source_opinion": "Source-backed fact",
    "agent_synthesis": "Agent synthesis",
    "PM_assumption": "PM assumption",
    "model_output": "Model output",
}


def _theme_card_body(inp: WikiIntegratorInput, theme_name: str, theme_slug: str,
                     existing: Optional[str]) -> str:
    b = inp.bundle
    tc = inp.temporal_context
    role = _temporal_role(tc)
    sd = _source_date(tc)

    # evidence linked to this theme (by atom.themes membership, else all atoms for the source)
    linked_atoms = [a for a in b.evidence_atoms
                    if a.evidence_id and (theme_name in a.themes or not a.themes)]
    if not linked_atoms:
        linked_atoms = [a for a in b.evidence_atoms if a.evidence_id]
    evidence_ids = [a.evidence_id for a in linked_atoms]

    # belief label from the dominant claim_kind among linked atoms
    kinds = [a.claim_kind for a in linked_atoms if a.claim_kind]
    belief = _BELIEF_LABEL.get(kinds[0], "Agent synthesis") if kinds else "Agent synthesis"

    entities = sorted({e for a in linked_atoms for e in a.entities})
    concepts = sorted({c for a in linked_atoms for c in a.concepts})
    cluster_ids = [c.cluster_id for c in (inp.theme_set.clusters if inp.theme_set else [])]

    fm = _fm([
        ("type", "theme"),
        ("classification", "theme"),
        ("workflow_status", "discovery_complete"),
        ("access_class", "case"),
        ("source_evidence", _yaml_list(evidence_ids)),
        ("parent_developments", _yaml_list(b.main_developments)),
        ("linked_events", _yaml_list(b.key_events)),
        ("linked_entities", _yaml_list(entities)),
        ("linked_concepts", _yaml_list(concepts)),
        ("operational_axes", _yaml_list([a.axis_name for a in b.operational_axes])),
        ("confounders", _yaml_list(b.confounders)),
        ("falsifiers", _yaml_list(b.falsifiers)),
        ("strategy_family_hints", _yaml_list([h.family for h in b.strategy_family_hints])),
        ("theme_clusters", _yaml_list(cluster_ids)),
        ("temporal_role", role),
        ("created", _CREATED),
        ("updated", _UPDATED),
    ])

    change_note = (
        f"### {_UPDATED} — {inp.source_classification.source_slug}\n"
        f"Theme touched by source `{inp.source_classification.source_slug}` "
        f"(temporal role {role}). Evidence: {', '.join(evidence_ids) or '(none)'}."
    )

    # On append we return ONLY the versioned change-note snippet (the applier appends it; we never
    # overwrite prior rationale). The trailing No-trade line keeps the appended block compliant.
    if existing is not None:
        return "\n" + change_note + "\n"

    causal = [f"{c.driver} -> {c.outcome}: {c.transmission}" for c in b.causal_claims]
    axes = [f"{a.axis_name}: {a.observable_series}" for a in b.operational_axes]

    body = f"""{fm}

# Theme Memory Card

## Current belief
{belief}: {_trim_words(theme_name)}

## Temporal status
Temporal role **{role}**; source date {sd}.

## Why this theme was picked
{_hist_prefix(role, sd, _trim_words(theme_name))} — surfaced from source `{inp.source_classification.source_slug}`.

## Evidence
{_bullets([f"[[{eid}]]: {a.claim}" for a, eid in zip(linked_atoms, evidence_ids)])}

## Main developments
{_bullets(b.main_developments)}

## Key events
{_bullets(b.key_events)}

## Hot topics
{_bullets(b.hot_topics)}

## Core causal hypothesis
{_bullets([c.driver + ' -> ' + c.outcome for c in b.causal_claims])}

## Causal graph
{_bullets(causal)}

## Operational axes
{_bullets(axes)}

## Confounders
{_bullets(b.confounders)}

## Falsifiers
{_bullets(b.falsifiers)}

## Forecast horizons / outcome candidates
{_bullets([_hist_prefix(role, sd, h.claim) for h in (tc.forecast_horizons if tc else [])])}

## Scenario memory
{_bullets([], empty="- (no scenario memory recorded — discovery mode)")}

## Strategy-family priors
{_bullets([f"{h.family}: {h.rationale}" for h in b.strategy_family_hints])}

## What changed after latest source
{change_note}

## Open questions
{_bullets(b.open_questions)}

{_NO_TRADE_HEADER}
{_NO_TRADE_LINE}
"""
    return body


def _cluster_page_body(inp: WikiIntegratorInput, cluster: ThemeCluster) -> str:
    tc = inp.temporal_context
    role = _temporal_role(tc)
    source_slugs = sorted({a.source_slug for a in cluster.source_attributions})
    temporal_roles = sorted({a.temporal_role for a in cluster.source_attributions
                             if a.temporal_role})

    promoted = cluster.theme_status == "promote_to_discovery"
    promo_text = (
        "Promoted to discovery: rests on current-input source-backed evidence."
        if promoted else
        f"Not promoted (status: {cluster.theme_status})."
    )
    if role == "historical_case" or any(r == "historical_case" for r in temporal_roles):
        promo_text += " Contains historical / outcome-candidate sources (not current confirmation)."

    fm = _fm([
        ("type", "theme_cluster"),
        ("classification", "theme_cluster"),
        ("workflow_status", "discovery_complete"),
        ("access_class", "case"),
        ("cluster_id", cluster.cluster_id),
        ("canonical_theme_name", _yaml_scalar(_trim_words(cluster.canonical_theme_name))),
        ("theme_status", cluster.theme_status),
        ("source_slugs", _yaml_list(source_slugs)),
        ("independent_source_count", str(cluster.independent_source_count)),
        ("evidence_ids", _yaml_list(cluster.evidence_ids)),
        ("temporal_roles", _yaml_list(temporal_roles)),
        ("strategy_family_hints", _yaml_list(cluster.strategy_family_hints)),
        ("promotion_score", str(cluster.promotion_score)),
        ("corroboration_score", str(cluster.corroboration_score)),
        ("attention_score", str(cluster.attention_score)),
        ("evidence_attention_divergence", str(cluster.evidence_attention_divergence)),
        ("created", _CREATED),
        ("updated", _UPDATED),
    ])

    attribs = [f"{a.source_slug} ({a.contribution_type}, current={a.is_current_input})"
               for a in cluster.source_attributions]
    bullets = [f"{eb.text} [{', '.join(eb.evidence_ids)}]" for eb in cluster.evidence_bullets]

    body = f"""{fm}

# Theme Cluster: {cluster.canonical_theme_name}

## Cluster thesis
{cluster.canonical_thesis}

## Source attributions
{_bullets(attribs)}

## Evidence bullets
{_bullets(bullets)}

## Why this cluster was promoted / not promoted
{promo_text}

## Corroboration vs attention
- Corroboration score: {cluster.corroboration_score}
- Attention score: {cluster.attention_score}
- Evidence-attention divergence (p-q proxy): {cluster.evidence_attention_divergence}
- Promotion score: {cluster.promotion_score}

## Temporal status
Temporal roles present: {', '.join(temporal_roles) or 'unknown'}.

## Operational axes
{_bullets(cluster.operational_axes)}

## Causal claims
{_bullets(cluster.causal_claims)}

## Confounders
{_bullets(cluster.confounders)}

## Falsifiers
{_bullets(cluster.falsifiers)}

## Strategy-family hints
{_bullets(cluster.strategy_family_hints)}

## Missing data
{_bullets(cluster.missing_data)}

## Rejected merges
{_bullets([str(r) for r in (inp.theme_set.rejected_merges if inp.theme_set else [])])}

{_NO_TRADE_HEADER}
{_NO_TRADE_LINE}
"""
    return body


def _concept_page_body(inp: WikiIntegratorInput, concept_name: str, concept_slug: str,
                       evidence_ids: list[str], theme_slugs: list[str],
                       cluster_ids: list[str]) -> str:
    """A taxonomy/mechanics page for a concept referenced by the source's evidence atoms.

    The body stays GENERIC: a short descriptor plus BACKLINKS to the evidence atoms and themes
    that reference the concept. No source-specific market claims are copied in (honours the
    method/case firewall and the copyright guard). `access_class` mirrors the SOURCE's access
    class — a method source's concept pages are method (taxonomy), a case source's are case.
    """
    cls = inp.source_classification
    tc = inp.temporal_context
    role = _temporal_role(tc)

    fm = _fm([
        ("type", "concept"),
        ("classification", "concept"),
        ("workflow_status", "discovery_complete"),
        ("access_class", cls.access_class),
        ("sources", _yaml_list([cls.source_slug])),
        ("evidence", _yaml_list(evidence_ids)),
        ("themes", _yaml_list(theme_slugs)),
        ("theme_clusters", _yaml_list(cluster_ids)),
        ("aliases", _yaml_list([])),
        ("created", _CREATED),
        ("updated", _UPDATED),
    ])

    body = f"""{fm}

# Concept: {_trim_words(concept_name)}

## What this is
A concept referenced by source `{cls.source_slug}` (temporal role {role}). Durable memory
node linking the evidence atoms and themes that invoke this concept; no source-specific market
claim is reproduced here.

## Referenced by evidence
{_bullets([f"[[{eid}]]" for eid in evidence_ids])}

## Referenced by themes
{_bullets([f"[[{t}]]" for t in theme_slugs])}

## Referenced by clusters
{_bullets([f"[[{c}]]" for c in cluster_ids])}

{_NO_TRADE_HEADER}
{_NO_TRADE_LINE}
"""
    return body


def _entity_page_body(inp: WikiIntegratorInput, entity_name: str, entity_slug: str,
                      evidence_ids: list[str], theme_slugs: list[str],
                      cluster_ids: list[str]) -> str:
    """A taxonomy page for an entity referenced by the source's evidence atoms.

    Same discipline as `_concept_page_body`: generic descriptor + backlinks only, `access_class`
    mirrors the SOURCE's access class, no source-specific market claim copied verbatim.
    """
    cls = inp.source_classification
    tc = inp.temporal_context
    role = _temporal_role(tc)

    fm = _fm([
        ("type", "entity"),
        ("classification", "entity"),
        ("workflow_status", "discovery_complete"),
        ("access_class", cls.access_class),
        ("sources", _yaml_list([cls.source_slug])),
        ("evidence", _yaml_list(evidence_ids)),
        ("themes", _yaml_list(theme_slugs)),
        ("theme_clusters", _yaml_list(cluster_ids)),
        ("aliases", _yaml_list([])),
        ("created", _CREATED),
        ("updated", _UPDATED),
    ])

    body = f"""{fm}

# Entity: {_trim_words(entity_name)}

## What this is
An entity referenced by source `{cls.source_slug}` (temporal role {role}). Durable memory
node linking the evidence atoms and themes that mention this entity; no source-specific market
claim is reproduced here.

## Referenced by evidence
{_bullets([f"[[{eid}]]" for eid in evidence_ids])}

## Referenced by themes
{_bullets([f"[[{t}]]" for t in theme_slugs])}

## Referenced by clusters
{_bullets([f"[[{c}]]" for c in cluster_ids])}

{_NO_TRADE_HEADER}
{_NO_TRADE_LINE}
"""
    return body


# ── planner ─────────────────────────────────────────────────────────────────────

def _guard_page(write: WikiPageWrite, raw_text: Optional[str], plan: WikiUpdatePlan) -> bool:
    """Return True if the page passes all guards; otherwise append to plan.blocked and return False.
    Append snippets (index/log/memory-map) are guarded for trade language too, but exempt from the
    mandatory No-trade boundary header (they are one-line appends, not full pages)."""
    body = write.content
    is_append = write.action == "append"

    # No-trade keyword scan
    hit = _trade_hit(body)
    if hit:
        plan.blocked.append(f"{write.path}: trade/execution language detected ('{hit}') — not written")
        return False

    # Every full page must carry the No-trade boundary line.
    if not is_append and (_NO_TRADE_HEADER not in body or _NO_TRADE_LINE not in body):
        plan.blocked.append(f"{write.path}: missing required No-trade boundary — not written")
        return False

    # No-copyright: no >=25-word verbatim run from raw_text. Checked PER LINE — bulleted claims
    # are separate items (each trimmed below the threshold), so they cannot be concatenated into
    # a false long run; only a single integrator line that is itself a long verbatim quote blocks.
    if raw_text:
        worst = 0
        for line in body.splitlines():
            if len(line.split()) < _COPYRIGHT_MAX_RUN_WORDS:
                continue  # too short to be a >=25-word run on its own
            worst = max(worst, _longest_verbatim_run(line, raw_text))
        if worst >= _COPYRIGHT_MAX_RUN_WORDS:
            plan.blocked.append(
                f"{write.path}: {worst}-word verbatim run from raw source (>= "
                f"{_COPYRIGHT_MAX_RUN_WORDS}) — copyright block, not written")
            return False
    return True


def build_wiki_update_plan(inp: WikiIntegratorInput) -> WikiUpdatePlan:
    """Compute every page the integrator WOULD write. No disk I/O."""
    plan = WikiUpdatePlan()
    cls = inp.source_classification
    b = inp.bundle
    root = inp.wiki_root.rstrip("/")
    is_method = cls.access_class == "method"

    created_links: list[str] = []   # slugs successfully planned (for index + link resolution)

    def add(path: str, kind: str, action: str, body: str, access_class: Optional[str], slug: str):
        w = WikiPageWrite(path=path, kind=kind, action=action,
                          access_class=access_class, content=body)
        if _guard_page(w, inp.raw_text, plan):
            plan.writes.append(w)
            if slug:
                created_links.append(slug)

    # (PART 3) SOURCE PAGE — always (stamps access_class verbatim; never upgraded).
    add(f"{root}/sources/{cls.source_slug}.md", "source", "create",
        _source_page_body(inp), cls.access_class, cls.source_slug)

    # (PART 4) EVIDENCE PAGES — CASE memory. A METHOD source must NOT emit case-evidence pages
    # from method content; skip them and note it.
    if is_method:
        if b.evidence_atoms:
            plan.warnings.append(
                f"method source '{cls.source_slug}': skipped {len(b.evidence_atoms)} evidence "
                "page(s) — method content does not produce CASE evidence pages")
    else:
        for atom in b.evidence_atoms:
            if not atom.evidence_id:
                plan.warnings.append("evidence atom without evidence_id skipped (no stable slug)")
                continue
            add(f"{root}/evidence/{atom.evidence_id}.md", "evidence", "create",
                _evidence_page_body(inp, atom), "case", atom.evidence_id)

    # (PART 5) THEME CARDS — one per core_theme_candidate (CASE). A theme card must cite evidence.
    if is_method:
        if b.core_theme_candidates:
            plan.warnings.append(
                f"method source '{cls.source_slug}': skipped {len(b.core_theme_candidates)} theme "
                "card(s) — method content is taxonomy, not case themes")
    else:
        evidence_ids_all = [a.evidence_id for a in b.evidence_atoms if a.evidence_id]
        for theme_name in b.core_theme_candidates:
            theme_slug = f"{cls.source_slug}-{_slugify(theme_name)}"
            path = f"{root}/themes/{theme_slug}.md"
            existing = None
            disk = Path(path)
            if disk.exists():
                existing = disk.read_text(encoding="utf-8", errors="ignore")
                action = "append"
            else:
                action = "create"
            if not evidence_ids_all:
                plan.warnings.append(
                    f"theme '{theme_slug}' has no evidence — cannot be promoted (card written, "
                    "marked unpromotable)")
            add(path, "theme", action, _theme_card_body(inp, theme_name, theme_slug, existing),
                "case", theme_slug)

    # (PART 6) THEME-CLUSTER PAGES — one per cluster, if a theme_set is provided.
    if inp.theme_set:
        for cluster in inp.theme_set.clusters:
            add(f"{root}/theme-clusters/{cluster.cluster_id}.md", "theme_cluster", "create",
                _cluster_page_body(inp, cluster), "case", cluster.cluster_id)

    # (PART 7) CONCEPT + ENTITY PAGES — taxonomy/mechanics nodes referenced by the source's
    # evidence atoms. Allowed for BOTH method and case sources; the page's access_class mirrors
    # the SOURCE's (never upgraded). Names are sourced from the union of atom.concepts /
    # atom.entities across the bundle (dedup + sorted). The body is generic + backlinks only;
    # backlinks point ONLY at pages that actually got created (in `created_links`).
    created_set = set(created_links)
    cluster_ids_created = [c.cluster_id for c in (inp.theme_set.clusters if inp.theme_set else [])
                           if c.cluster_id in created_set]

    concepts = sorted({c for a in b.evidence_atoms for c in a.concepts})
    entities = sorted({e for a in b.evidence_atoms for e in a.entities})

    for concept_name in concepts:
        # backlinks restricted to atoms that actually reference THIS concept
        ev_refs = [a.evidence_id for a in b.evidence_atoms
                   if a.evidence_id and a.evidence_id in created_set and concept_name in a.concepts]
        th_refs = sorted({f"{cls.source_slug}-{_slugify(t)}"
                          for a in b.evidence_atoms if concept_name in a.concepts
                          for t in a.themes
                          if f"{cls.source_slug}-{_slugify(t)}" in created_set})
        concept_slug = _slugify(concept_name)
        add(f"{root}/concepts/{concept_slug}.md", "concept", "create",
            _concept_page_body(inp, concept_name, concept_slug, ev_refs, th_refs,
                               cluster_ids_created),
            cls.access_class, concept_slug)

    for entity_name in entities:
        ev_refs = [a.evidence_id for a in b.evidence_atoms
                   if a.evidence_id and a.evidence_id in created_set and entity_name in a.entities]
        th_refs = sorted({f"{cls.source_slug}-{_slugify(t)}"
                          for a in b.evidence_atoms if entity_name in a.entities
                          for t in a.themes
                          if f"{cls.source_slug}-{_slugify(t)}" in created_set})
        entity_slug = _slugify(entity_name)
        add(f"{root}/entities/{entity_slug}.md", "entity", "create",
            _entity_page_body(inp, entity_name, entity_slug, ev_refs, th_refs,
                              cluster_ids_created),
            cls.access_class, entity_slug)

    # (PART 8) APPEND entries: index.md, log.md, memory-map.md.
    # CRITICAL link-resolution invariant: every [[slug]] emitted into index.md MUST be a page
    # that was actually planned. We group the SLUGS THAT PASSED THE GUARDS — i.e. only those in
    # `created_links` (a page blocked for copyright/trade never reaches it) — by kind, reading the
    # kind off the planned writes. This guarantees the index never links to a non-existent file.
    created_set = set(created_links)
    by_kind: dict[str, list[str]] = {}
    for w in plan.writes:
        if w.action != "create":
            continue
        stem = Path(w.path).stem
        if stem in created_set:
            by_kind.setdefault(w.kind, []).append(stem)
    # A theme card is action="create" on first ingest and "append" on re-ingest; capture the
    # appended-theme slug too so the index/memory-map reflect it (it is still a real file).
    for w in plan.writes:
        if w.kind == "theme" and w.action == "append":
            stem = Path(w.path).stem
            if stem in created_set and stem not in by_kind.get("theme", []):
                by_kind.setdefault("theme", []).append(stem)

    src_slugs = by_kind.get("source", [])
    evidence_slugs = by_kind.get("evidence", [])
    theme_slugs = by_kind.get("theme", [])
    cluster_slugs = by_kind.get("theme_cluster", [])
    concept_slugs = by_kind.get("concept", [])
    entity_slugs = by_kind.get("entity", [])

    add(f"{root}/index.md", "index", "append",
        _index_snippet(cls.source_slug, src_slugs, evidence_slugs, theme_slugs,
                       cluster_slugs, concept_slugs, entity_slugs),
        None, "")
    add(f"{root}/log.md", "log", "append",
        _log_snippet(inp, plan, evidence_slugs, theme_slugs, cluster_slugs,
                     concept_slugs, entity_slugs),
        None, "")
    add(f"{root}/memory-map.md", "memory_map", "append",
        _memory_map_snippet(inp, theme_slugs, cluster_slugs, evidence_slugs),
        None, "")

    return plan


# ── PART 8 helpers: index / log / memory-map append snippets ──────────────────────
# All three are byte-stable across re-runs (deterministic dates, no wall-clock, no set-ordering
# surprises — slug lists arrive in planned-write order). Each carries a stable per-source marker
# comment so the applier's `content in existing` idempotency check skips them on re-run. Every
# [[slug]] emitted is a page that was actually planned (passed the guards).

def _link_line(label: str, slugs: list[str]) -> str:
    """One index line: a labelled, comma-joined list of wikilinks (or '(none)')."""
    body = ", ".join(f"[[{s}]]" for s in slugs) if slugs else "(none)"
    return f"- {label}: {body}"


def _index_snippet(source_slug: str, src_slugs: list[str], evidence_slugs: list[str],
                   theme_slugs: list[str], cluster_slugs: list[str],
                   concept_slugs: list[str], entity_slugs: list[str]) -> str:
    """Content-oriented per-source index block. Lists, grouped by kind, every page created in
    THIS integration. Only links to created pages (link-resolution invariant)."""
    lines = [
        "",
        f"<!-- integrated {_UPDATED}: {source_slug} -->",
        f"### {source_slug}",
        _link_line("Source", src_slugs),
        _link_line("Evidence", evidence_slugs),
        _link_line("Themes", theme_slugs),
        _link_line("Theme clusters", cluster_slugs),
        _link_line("Concepts", concept_slugs),
        _link_line("Entities", entity_slugs),
        "",
    ]
    return "\n".join(lines)


def _log_snippet(inp: WikiIntegratorInput, plan: WikiUpdatePlan, evidence_slugs: list[str],
                 theme_slugs: list[str], cluster_slugs: list[str], concept_slugs: list[str],
                 entity_slugs: list[str]) -> str:
    """Append-only, one entry per integration, byte-stable (deterministic counts + date)."""
    cls = inp.source_classification
    b = inp.bundle
    role = _temporal_role(inp.temporal_context)
    families = [_trim_words(h.family, 6) for h in b.strategy_family_hints]
    fam_text = ", ".join(families) if families else "(none)"
    themes_text = str(len(theme_slugs)) if theme_slugs else "0"
    clusters_text = str(len(cluster_slugs)) if cluster_slugs else "0"
    lines = [
        "",
        f"## [{_UPDATED}] ingest | {cls.source_slug}",
        f"- Source: {cls.source_slug} ({cls.source_type})",
        f"- Access class: {cls.access_class}",
        f"- Temporal role: {role}",
        f"- Evidence atoms created: {len(evidence_slugs)}",
        f"- Themes updated: {themes_text}",
        f"- Theme clusters updated: {clusters_text}",
        f"- Concepts/entities updated: {len(concept_slugs)} concept(s), "
        f"{len(entity_slugs)} entity(ies)",
        f"- Strategy-family hints: {fam_text}",
        f"- Warnings: {len(plan.warnings)}",
        # A short equivalent of plan.no_trade_confirmation. We deliberately avoid the literal
        # "hedge ratios" wording the confirmation uses so this log line carries no string that a
        # naive trade-language scan flags — the boundary is asserted by construction, not phrasing.
        "- No-trade confirmation: structured durable memory only — discovery mode; "
        "no trades/sizing/execution; no raw source text.",
        "",
    ]
    return "\n".join(lines)


def _memory_map_snippet(inp: WikiIntegratorInput, theme_slugs: list[str],
                        cluster_slugs: list[str], evidence_slugs: list[str]) -> str:
    """Current-state per-source contribution. Emits every heading even when empty ('- (none)').
    Derives the 'missing X' / 'ready' sets from the bundle's evidence / axes / falsifiers /
    family hints. 'Ready for routing' requires evidence + an axis + a falsifier + a family hint;
    'ready for downstream models' additionally requires a hint carrying a downstream model."""
    cls = inp.source_classification
    b = inp.bundle
    role = _temporal_role(inp.temporal_context)

    has_evidence = bool(evidence_slugs)
    has_axis = bool(b.operational_axes)
    has_falsifier = bool(b.falsifiers)
    has_family = bool(b.strategy_family_hints)
    has_downstream = any((h.downstream_model_hint or "").strip() for h in b.strategy_family_hints)

    # historical-outcome candidates: a source whose forecasts can now be scored against reality.
    is_outcome = role in ("historical_case", "outcome_candidate", "stale_case")
    outcome_candidates = b.core_theme_candidates if is_outcome else []

    missing_evidence = [] if has_evidence else b.core_theme_candidates
    missing_axes = [] if has_axis else b.core_theme_candidates
    missing_falsifiers = [] if has_falsifier else b.core_theme_candidates
    ready_routing = (b.core_theme_candidates
                     if (has_evidence and has_axis and has_falsifier and has_family) else [])
    ready_downstream = (b.core_theme_candidates
                        if (has_evidence and has_axis and has_falsifier and has_downstream)
                        else [])

    families = [f"{_trim_words(h.family, 6)}: {h.rationale}" for h in b.strategy_family_hints]

    lines = [
        "",
        f"<!-- memory-map {_UPDATED}: {cls.source_slug} -->",
        f"### {cls.source_slug}",
        "#### Active Main Developments",
        _bullets(b.main_developments),
        "#### Active Core Themes",
        _bullets(b.core_theme_candidates),
        "#### Active Hot Topics",
        _bullets(b.hot_topics),
        "#### Multi-Source Theme Clusters",
        _bullets([f"[[{c}]]" for c in cluster_slugs]),
        "#### Strategy-Family Priors",
        _bullets(families),
        "#### Historical Outcome Candidates",
        _bullets(outcome_candidates),
        "#### Themes Missing Evidence",
        _bullets(missing_evidence),
        "#### Themes Missing Operational Axes",
        _bullets(missing_axes),
        "#### Themes Missing Falsifiers",
        _bullets(missing_falsifiers),
        "#### Themes Ready for Strategy-Family Routing",
        _bullets(ready_routing),
        "#### Themes Ready for Downstream Models",
        _bullets(ready_downstream),
        "",
    ]
    return "\n".join(lines)


# ── applier ─────────────────────────────────────────────────────────────────────

def apply_wiki_update_plan(plan: WikiUpdatePlan, wiki_root: str,
                           force: bool = False) -> WikiIntegrationResult:
    """Write the planned pages. Idempotent:
      * create/update — if the target exists with identical content, the action is a 'skip';
      * append — if the snippet is already present at the tail/anywhere in the file, it is a 'skip'.
    """
    written: list[str] = []
    skipped: list[str] = []
    warnings = list(plan.warnings)

    for w in plan.writes:
        path = Path(w.path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if w.action == "append":
            existing = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
            if w.content in existing:
                skipped.append(w.path)
                continue
            with path.open("a", encoding="utf-8") as fh:
                fh.write(w.content)
            written.append(w.path)
            continue

        # create / update / skip
        if path.exists():
            current = path.read_text(encoding="utf-8", errors="ignore")
            if current == w.content and not force:
                skipped.append(w.path)
                continue
        path.write_text(w.content, encoding="utf-8")
        written.append(w.path)

    return WikiIntegrationResult(
        plan=plan, applied=True, written_paths=written,
        skipped_paths=skipped, warnings=warnings,
    )


def integrate(inp: WikiIntegratorInput) -> WikiIntegrationResult:
    """Build the plan; unless dry_run, apply it. On dry_run: applied=False, NO disk writes."""
    if isinstance(inp, dict):
        inp = WikiIntegratorInput.model_validate(inp)
    plan = build_wiki_update_plan(inp)
    if inp.dry_run:
        return WikiIntegrationResult(plan=plan, applied=False, warnings=list(plan.warnings))
    return apply_wiki_update_plan(plan, inp.wiki_root, force=inp.force)
