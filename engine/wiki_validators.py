"""Wiki-persistence validator foundation (PART 9).

A library of small, well-typed, composable validators that a future ``WikiLintAgent`` can
call to health-check the durable wiki memory layer produced by the WikiIntegrator
(``engine/wiki_integration.py``). This module deliberately builds ONLY the reusable
validator functions plus a finding model — it does NOT implement the agent, orchestration,
or any disk mutation. Every validator is read-only.

Two flavours of validator live here:

  * **plan/result validators** — operate on an in-memory ``WikiUpdatePlan`` /
    ``WikiIntegrationResult`` (the integrator's output, no disk I/O); and
  * **on-disk validators** — scan a materialized wiki tree under a ``wiki_root``.

A handful are **pure predicates** over a single page string (+ flags) so they can be unit
tested without any filesystem at all (checks 6, 7, 8, 9 expose a predicate; several others
also expose a single-page helper).

Discipline mirrored from ``wiki_integration.py`` (constants reused, not re-derived):

  * the no-trade lexicon ``_TRADE_PATTERNS`` / the ``_NO_TRADE_LINE`` disclaimer (check 11);
  * the ``>= _COPYRIGHT_MAX_RUN_WORDS`` (25) verbatim-run copyright cap (check 10);
  * the ``access_class: method | case`` firewall discipline (checks 5, 6, 7).

No wall-clock is ever read here: any check that needs "today" or a horizon end date takes
it as an explicit parameter (``current_date``).
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Literal, Optional, Union

from pydantic import BaseModel, Field

# Reuse the REAL logic/constants from the integrator so thresholds never drift.
from .wiki_integration import (
    _COPYRIGHT_MAX_RUN_WORDS,
    _NO_TRADE_HEADER,
    _NO_TRADE_LINE,
    _TRADE_PATTERNS,
    _longest_verbatim_run,
)
from .schema.wiki_integration import (
    WikiIntegrationResult,
    WikiPageWrite,
    WikiUpdatePlan,
)

PathLike = Union[str, Path]
Severity = Literal["error", "warning", "info"]

# Operational machinery files that carry NO access_class / frontmatter knowledge contract
# (see wiki/CONVENTIONS.md "Exempt — operational files"). The validators skip them where a
# knowledge-page contract is being checked.
_OPERATIONAL_FILES = frozenset({
    "index.md", "log.md", "memory-map.md", "memory_map.md",
    "lint-status.md", "lint-scratch.md", "CONVENTIONS.md",
})

# A wikilink token: [[target]] where target may be namespaced ("evidence:foo") and may carry
# a display alias ("[[slug|Label]]") — only the target before any '|' is the resolvable slug.
_WIKILINK = re.compile(r"\[\[([^\]\|]+)(?:\|[^\]]*)?\]\]")

# A YAML frontmatter key at column 0 (e.g. "access_class: case").
_FM_KEY = re.compile(r"^([A-Za-z0-9_]+)\s*:\s*(.*)$")


# ── finding + report models ─────────────────────────────────────────────────────


class ValidationFinding(BaseModel):
    """A single lint observation.

    Attributes:
        check: stable rule id (e.g. ``"frontmatter_present"``).
        severity: ``"error"`` blocks; ``"warning"`` is suspicious; ``"info"`` is advisory.
        path: the offending page / file (wiki-relative or absolute), or ``None`` for a
            whole-wiki finding.
        message: human-readable explanation.
    """

    check: str
    severity: Severity = "error"
    path: Optional[str] = None
    message: str


class ValidationReport(BaseModel):
    """Aggregated findings from one or more validators.

    ``ok`` is True iff there are no ``error``-severity findings (warnings/info do not fail).
    """

    findings: list[ValidationFinding] = Field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True iff no error-severity finding is present."""
        return not any(f.severity == "error" for f in self.findings)

    def errors(self) -> list[ValidationFinding]:
        """All error-severity findings."""
        return [f for f in self.findings if f.severity == "error"]

    def warnings(self) -> list[ValidationFinding]:
        """All warning-severity findings."""
        return [f for f in self.findings if f.severity == "warning"]

    def infos(self) -> list[ValidationFinding]:
        """All info-severity findings."""
        return [f for f in self.findings if f.severity == "info"]

    def extend(self, findings: Iterable[ValidationFinding]) -> "ValidationReport":
        """Append findings in place and return self (for fluent composition)."""
        self.findings.extend(findings)
        return self


# ── shared parsing helpers (no disk I/O unless a Path is passed) ──────────────────


def _split_frontmatter(text: str) -> tuple[Optional[dict[str, str]], str]:
    """Parse a leading ``---`` ... ``---`` YAML frontmatter block.

    Returns ``(fields, body)``. ``fields`` is ``None`` when no well-formed frontmatter block
    (opening ``---`` on line 1 and a closing ``---``) is present. Only top-level scalar keys
    are captured (block-list items are ignored — these validators only need scalar fields
    like ``type`` / ``access_class`` / ``temporal_role``). Values keep their raw text.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fields: dict[str, str] = {}
            for raw in lines[1:i]:
                if raw[:1] in (" ", "\t"):
                    continue  # nested / list item — not a top-level scalar key
                m = _FM_KEY.match(raw)
                if m:
                    fields[m.group(1)] = m.group(2).strip()
            body = "\n".join(lines[i + 1:])
            return fields, body
    return None, text


def _fm_value(text: str, key: str) -> Optional[str]:
    """Return a single top-level frontmatter scalar value, or ``None``."""
    fields, _ = _split_frontmatter(text)
    if fields is None:
        return None
    return fields.get(key)


def _wikilinks(text: str) -> list[str]:
    """All wikilink targets (slugs) in ``text``, alias/namespace-stripped of the display part."""
    return [m.group(1).strip() for m in _WIKILINK.finditer(text)]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _is_operational(path: PathLike) -> bool:
    return Path(path).name in _OPERATIONAL_FILES


def _iter_pages(wiki_root: PathLike) -> list[Path]:
    """All ``*.md`` knowledge pages under ``wiki_root`` (operational machinery files excluded)."""
    root = Path(wiki_root)
    if not root.exists():
        return []
    return [p for p in sorted(root.rglob("*.md")) if not _is_operational(p)]


def _slug_index(wiki_root: PathLike) -> dict[str, Path]:
    """Map every resolvable slug under ``wiki_root`` to its file.

    A page is addressable by its bare filename stem (``foo`` for ``foo.md``) AND by any
    namespaced form recorded in its own ``slug:``/``evidence_id:`` frontmatter, plus the
    ``<dir>:<stem>`` convention seen in the index (e.g. ``evidence:foo`` for
    ``evidence/foo.md``). This keeps link resolution permissive — a link is "broken" only if
    it matches none of these.
    """
    idx: dict[str, Path] = {}
    root = Path(wiki_root)
    if not root.exists():
        return idx
    for p in sorted(root.rglob("*.md")):
        stem = p.stem
        idx.setdefault(stem, p)
        # <dir>:<stem> namespaced form (evidence:foo, themes:foo, …) for non-root files
        try:
            rel_parent = p.parent.relative_to(root)
        except ValueError:
            rel_parent = Path()
        if rel_parent != Path():
            top = rel_parent.parts[0].rstrip("s")  # evidence/ → "evidence", themes/ → "theme"
            idx.setdefault(f"{rel_parent.parts[0]}:{stem}", p)
            idx.setdefault(f"{top}:{stem}", p)
        text = _read(p)
        for key in ("slug", "evidence_id", "cluster_id"):
            v = _fm_value(text, key)
            if v:
                idx.setdefault(v.strip().strip('"'), p)
    return idx


def _plan_writes(obj: Union[WikiUpdatePlan, WikiIntegrationResult]) -> list[WikiPageWrite]:
    plan = obj.plan if isinstance(obj, WikiIntegrationResult) else obj
    return list(plan.writes)


# ════════════════════════════════════════════════════════════════════════════════
# The 14 checks. Each returns list[ValidationFinding]. Pure predicates are noted.
# ════════════════════════════════════════════════════════════════════════════════


# ── 1. frontmatter present ────────────────────────────────────────────────────────

def page_has_frontmatter(content: str, path: Optional[str] = None) -> Optional[ValidationFinding]:
    """Pure predicate: a created/updated page body has a ``---`` ... ``---`` frontmatter block.

    Returns a finding when absent, else ``None``."""
    fields, _ = _split_frontmatter(content)
    if fields is None:
        return ValidationFinding(
            check="frontmatter_present", severity="error", path=path,
            message="page has no YAML frontmatter (opening/closing '---' block missing)")
    return None


def check_frontmatter_present(
    plan_or_result: Union[WikiUpdatePlan, WikiIntegrationResult],
) -> list[ValidationFinding]:
    """Check 1: every created/updated full page in the plan has YAML frontmatter.

    ``append`` writes (index/log/memory-map snippets) are exempt — they are one-line appends,
    not full pages. Returns a list of findings (empty when clean)."""
    out: list[ValidationFinding] = []
    for w in _plan_writes(plan_or_result):
        if w.action == "append":
            continue
        f = page_has_frontmatter(w.content, w.path)
        if f:
            out.append(f)
    return out


# ── 2. wikilinks resolve ──────────────────────────────────────────────────────────

def check_wikilinks_resolve(
    wiki_root: PathLike,
    *,
    extra_slugs: Optional[Iterable[str]] = None,
) -> list[ValidationFinding]:
    """Check 2: every ``[[slug]]`` on disk resolves to an existing page.

    On-disk scan. Builds a slug index over ``wiki_root`` (filename stem + namespaced forms +
    frontmatter ``slug``/``evidence_id``/``cluster_id``); ``extra_slugs`` augments it (e.g.
    slugs about to be created in the same batch). Each unresolved link is one ``error``
    finding tagged with the page that contains it. Evidence links are a strict subset of this
    general check."""
    out: list[ValidationFinding] = []
    idx = _slug_index(wiki_root)
    known = set(idx) | {s.strip() for s in (extra_slugs or [])}
    root = Path(wiki_root)
    if not root.exists():
        return out
    for p in sorted(root.rglob("*.md")):
        if _is_operational(p):
            continue
        rel = str(p.relative_to(root))
        for target in _wikilinks(_read(p)):
            if target not in known:
                out.append(ValidationFinding(
                    check="wikilink_resolves", severity="error", path=rel,
                    message=f"unresolved wikilink [[{target}]] (no matching page/slug under root)"))
    return out


# ── 3. theme pages cite evidence ──────────────────────────────────────────────────

def page_theme_cites_evidence(content: str, path: Optional[str] = None) -> Optional[ValidationFinding]:
    """Pure predicate: a ``type: theme`` page carries at least one evidence citation.

    Satisfied by a non-empty ``source_evidence`` frontmatter list OR an ``[[evidence...]]``
    wikilink in the body / an ``## Evidence`` section that contains a wikilink. Returns a
    finding (error) when a theme page cites nothing; ``None`` for non-theme pages or when at
    least one citation is present."""
    fields, body = _split_frontmatter(content)
    if fields is None or fields.get("type") != "theme":
        return None
    # frontmatter source_evidence non-empty? (inline flow list OR a following block list)
    se = fields.get("source_evidence", "")
    has_fm_evidence = bool(se) and se.strip() not in ("[]", "")
    if not has_fm_evidence:
        # block-list form: source_evidence: \n  - "evidence:x"
        m = re.search(r"^source_evidence:\s*$", content, re.M)
        if m:
            tail = content[m.end():]
            has_fm_evidence = bool(re.match(r"\s*\n\s+- \S", tail))
    # any evidence-ish wikilink in the body?
    links = _wikilinks(body)
    has_link = any(("evidence" in t.lower()) for t in links) or bool(links)
    if has_fm_evidence or has_link:
        return None
    return ValidationFinding(
        check="theme_cites_evidence", severity="error", path=path,
        message="theme page cites no evidence (empty source_evidence and no [[evidence]] link)")


def check_theme_pages_cite_evidence(wiki_root: PathLike) -> list[ValidationFinding]:
    """Check 3: every theme page on disk cites at least one piece of evidence.

    On-disk scan over ``type: theme`` pages; delegates per-page to
    :func:`page_theme_cites_evidence`."""
    out: list[ValidationFinding] = []
    for p in _iter_pages(wiki_root):
        text = _read(p)
        f = page_theme_cites_evidence(text, str(p.relative_to(Path(wiki_root))))
        if f:
            out.append(f)
    return out


# ── 4. promoted clusters have a source attribution ───────────────────────────────

def page_promoted_cluster_has_source(content: str, path: Optional[str] = None) -> Optional[ValidationFinding]:
    """Pure predicate: a cluster page with ``theme_status: promote_to_discovery`` names at least
    one source.

    A promoted cluster must carry a non-empty ``source_slugs`` list (frontmatter inline/block
    list) or a ``## Source attributions`` section with content. Returns a finding when a
    promoted cluster has no source attribution; ``None`` otherwise (incl. non-promoted /
    non-cluster pages)."""
    fields, body = _split_frontmatter(content)
    if fields is None:
        return None
    if fields.get("theme_status") != "promote_to_discovery":
        return None
    src = fields.get("source_slugs", "")
    has_inline = bool(src) and src.strip() not in ("[]", "")
    has_block = bool(re.search(r"^source_slugs:\s*$", content, re.M) and
                     re.search(r"^source_slugs:\s*\n\s+- \S", content, re.M))
    # section fallback: "## Source attributions" with a non-"(none)" bullet
    sect = re.search(r"##\s*Source attributions\s*\n((?:- .*\n?)+)", body)
    has_section = bool(sect and sect.group(1).strip() not in ("- (none)", ""))
    if has_inline or has_block or has_section:
        return None
    return ValidationFinding(
        check="promoted_cluster_has_source", severity="error", path=path,
        message="cluster promoted_to_discovery but has no source attribution (empty source_slugs)")


def check_promoted_clusters_have_sources(wiki_root: PathLike) -> list[ValidationFinding]:
    """Check 4: every promoted theme cluster on disk has at least one source attribution.

    On-disk scan; delegates per-page to :func:`page_promoted_cluster_has_source`."""
    out: list[ValidationFinding] = []
    for p in _iter_pages(wiki_root):
        f = page_promoted_cluster_has_source(_read(p), str(p.relative_to(Path(wiki_root))))
        if f:
            out.append(f)
    return out


# ── 5. access_class present ───────────────────────────────────────────────────────

_VALID_ACCESS_CLASSES = frozenset({"method", "case"})


def page_has_access_class(content: str, path: Optional[str] = None) -> Optional[ValidationFinding]:
    """Pure predicate: a knowledge page declares a valid ``access_class`` (``method``/``case``).

    Returns an error finding when missing, a warning when present-but-invalid, ``None`` when
    valid. Caller is responsible for skipping operational files (see
    :func:`check_access_class_present`)."""
    val = _fm_value(content, "access_class")
    if val is None:
        return ValidationFinding(
            check="access_class_present", severity="error", path=path,
            message="page missing required 'access_class' frontmatter field")
    cleaned = val.strip().strip('"').strip("'")
    if cleaned not in _VALID_ACCESS_CLASSES:
        return ValidationFinding(
            check="access_class_present", severity="warning", path=path,
            message=f"invalid access_class {cleaned!r} (expected 'method' or 'case')")
    return None


def check_access_class_present(wiki_root: PathLike) -> list[ValidationFinding]:
    """Check 5: every knowledge page on disk has a valid ``access_class``.

    On-disk scan (operational machinery files are exempt and skipped); delegates per-page to
    :func:`page_has_access_class`."""
    out: list[ValidationFinding] = []
    for p in _iter_pages(wiki_root):
        f = page_has_access_class(_read(p), str(p.relative_to(Path(wiki_root))))
        if f:
            out.append(f)
    return out


# ── 6. CASE pages refused in Phase A unless current input ─────────────────────────

def check_case_page_phase_a(
    content: str,
    *,
    phase: Literal["A", "B"],
    is_current_input: bool,
    path: Optional[str] = None,
) -> list[ValidationFinding]:
    """Check 6 (PURE PREDICATE): mirror the firewall rule for one page.

    In **Phase A** a ``case`` page that is NOT the current input is a firewall violation
    (fresh causal reasoning must not read prior conclusions). A ``method`` page is always
    admissible; a ``case`` page that IS the current input is admissible; Phase B admits
    everything. This re-expresses the rule WITHOUT importing the live firewall, so it stays a
    pure, side-effect-free predicate over (page, phase, is_current_input). Returns a one-item
    list with an error finding on violation, else an empty list."""
    access = (_fm_value(content, "access_class") or "case").strip().strip('"').strip("'")
    if phase == "A" and access == "case" and not is_current_input:
        return [ValidationFinding(
            check="case_refused_phase_a", severity="error", path=path,
            message="case page read in Phase A without being the current input "
                    "(firewall: fresh reasoning must not consult prior case conclusions)")]
    return []


# ── 7. METHOD pages contain no case conclusions ───────────────────────────────────

# Case-like outcome/forecast tells that should not appear on a how-to-reason (method) page.
_CASE_CONCLUSION_PATTERNS = (
    re.compile(r"\bas of\s+\d{4}-\d{2}-\d{2}\s*:", re.I),     # "as of 2026-05-01:"
    re.compile(r"\bforecast\b", re.I),
    re.compile(r"\bprice target\b", re.I),
    re.compile(r"\btarget\s+(?:of\s+)?\$?\d", re.I),          # "target of 250", "target $4"
    re.compile(r"\bwe (?:recommend|are long|are short|expect|forecast)\b", re.I),
    re.compile(r"\b(?:bullish|bearish)\s+on\b", re.I),
)


def page_method_has_no_case_conclusions(content: str, path: Optional[str] = None) -> list[ValidationFinding]:
    """Check 7 (PURE PREDICATE over one page): a ``method`` page should carry no case-like
    forward market calls / outcome language.

    Heuristic — flags dated outcome framing (``as of <date>:``), ``forecast``, explicit price
    targets, recommendation verbs, directional calls. Only fires for ``access_class: method``
    pages; emits a **warning** per distinct tell found (method content is how-to-reason, so a
    conclusion here is suspicious, not provably wrong). Returns a list (possibly empty)."""
    access = (_fm_value(content, "access_class") or "").strip().strip('"').strip("'")
    if access != "method":
        return []
    _, body = _split_frontmatter(content)
    out: list[ValidationFinding] = []
    for pat in _CASE_CONCLUSION_PATTERNS:
        m = pat.search(body)
        if m:
            out.append(ValidationFinding(
                check="method_no_case_conclusion", severity="warning", path=path,
                message=f"method page contains case-like conclusion language: {m.group(0).strip()!r}"))
    return out


def check_method_pages_no_case_conclusions(wiki_root: PathLike) -> list[ValidationFinding]:
    """Check 7 (on-disk scan): every ``method`` page on disk is free of case-conclusion tells.

    Delegates per-page to :func:`page_method_has_no_case_conclusions`."""
    out: list[ValidationFinding] = []
    for p in _iter_pages(wiki_root):
        out.extend(page_method_has_no_case_conclusions(_read(p), str(p.relative_to(Path(wiki_root)))))
    return out


# ── 8. historical cases not rendered as current recommendations ───────────────────

# Present-tense live-recommendation phrasing that a historical_case page must NOT use.
_LIVE_RECO_PATTERNS = (
    re.compile(r"\bwe (?:recommend|are long|are short|are buying|are selling)\b", re.I),
    re.compile(r"\b(?:go|going)\s+(?:long|short)\b", re.I),
    re.compile(r"\b(?:current|live)\s+recommendation\b", re.I),
    re.compile(r"\bwe expect\b", re.I),
)


def page_historical_case_disclaimed(content: str, path: Optional[str] = None) -> list[ValidationFinding]:
    """Check 8 (PURE PREDICATE over one page): a ``temporal_role: historical_case`` page must
    carry the historical / ``as of <source_date>`` framing and must NOT phrase forecasts as
    live present-tense recommendations.

    Emits an **error** if the historical disclaimer / ``as of`` framing is missing, and an
    **error** per live-recommendation phrasing found. Only fires for historical_case pages.
    Returns a list (possibly empty)."""
    fields, body = _split_frontmatter(content)
    if fields is None or fields.get("temporal_role") != "historical_case":
        return []
    out: list[ValidationFinding] = []
    has_disclaimer = (
        re.search(r"\bas of\b", body, re.I) is not None
        or re.search(r"\bhistorical case\b", body, re.I) is not None
        or re.search(r"not (?:a )?current recommendation", body, re.I) is not None
    )
    if not has_disclaimer:
        out.append(ValidationFinding(
            check="historical_case_disclaimed", severity="error", path=path,
            message="historical_case page lacks 'as of <source_date>' / historical-case framing"))
    for pat in _LIVE_RECO_PATTERNS:
        m = pat.search(body)
        if m:
            out.append(ValidationFinding(
                check="historical_case_disclaimed", severity="error", path=path,
                message=f"historical_case page phrases a live recommendation: {m.group(0).strip()!r}"))
    return out


def check_historical_cases_not_current(wiki_root: PathLike) -> list[ValidationFinding]:
    """Check 8 (on-disk scan): every ``historical_case`` page is disclaimed and free of live
    recommendations. Delegates per-page to :func:`page_historical_case_disclaimed`."""
    out: list[ValidationFinding] = []
    for p in _iter_pages(wiki_root):
        out.extend(page_historical_case_disclaimed(_read(p), str(p.relative_to(Path(wiki_root)))))
    return out


# ── 9. expired forecasts labelled expired / outcome-candidate ─────────────────────

def check_forecast_expiry_labeled(
    content: str,
    *,
    horizon_end_date: Optional[str],
    current_date: str,
    temporal_status: Optional[str] = None,
    path: Optional[str] = None,
) -> list[ValidationFinding]:
    """Check 9 (PURE PREDICATE): a forecast past its horizon must be labelled ``expired`` or
    ``outcome_candidate`` — never left as ``current``.

    Dates are ISO ``YYYY-MM-DD`` strings supplied by the caller (no wall-clock here).
    ``temporal_status`` defaults to the page's ``temporal_status`` frontmatter when omitted.
    A forecast is "past horizon" when ``horizon_end_date < current_date``. Emits an error when
    a past-horizon forecast is still marked ``current`` (or carries no expiry label at all).
    Returns a list (possibly empty)."""
    if horizon_end_date is None:
        return []
    if horizon_end_date >= current_date:  # ISO strings compare lexicographically by date
        return []
    status = temporal_status
    if status is None:
        status = (_fm_value(content, "temporal_status") or "").strip().strip('"').strip("'")
    if status in ("expired", "outcome_candidate"):
        return []
    return [ValidationFinding(
        check="expired_forecast_labeled", severity="error", path=path,
        message=f"forecast past horizon ({horizon_end_date} < {current_date}) is labelled "
                f"{status!r}, not 'expired'/'outcome_candidate'")]


# ── 10. no long copyrighted text copied ──────────────────────────────────────────

def page_no_long_copyright(
    content: str,
    raw_text: Optional[str],
    path: Optional[str] = None,
) -> Optional[ValidationFinding]:
    """Pure predicate: no ``>= _COPYRIGHT_MAX_RUN_WORDS`` (25) contiguous verbatim run from
    ``raw_text``.

    Reuses the integrator's :func:`_longest_verbatim_run`. Checked PER LINE (matching the
    integrator's guard) so separately-trimmed bullets cannot concatenate into a false long
    run. ``raw_text=None`` ⇒ no check. Returns an error finding on a too-long run, else
    ``None``."""
    if not raw_text:
        return None
    worst = 0
    for line in content.splitlines():
        if len(line.split()) < _COPYRIGHT_MAX_RUN_WORDS:
            continue
        worst = max(worst, _longest_verbatim_run(line, raw_text))
    if worst >= _COPYRIGHT_MAX_RUN_WORDS:
        return ValidationFinding(
            check="no_long_copyright", severity="error", path=path,
            message=f"{worst}-word verbatim run from raw source "
                    f"(>= {_COPYRIGHT_MAX_RUN_WORDS}) — copyright violation")
    return None


def check_no_long_copyright(
    plan_or_result: Union[WikiUpdatePlan, WikiIntegrationResult],
    raw_text: Optional[str],
) -> list[ValidationFinding]:
    """Check 10: no planned page reproduces a ``>= 25``-word verbatim run from ``raw_text``.

    Plan-level; delegates per-page to :func:`page_no_long_copyright`. Returns a list (empty
    when clean or when ``raw_text`` is None)."""
    out: list[ValidationFinding] = []
    if not raw_text:
        return out
    for w in _plan_writes(plan_or_result):
        f = page_no_long_copyright(w.content, raw_text, w.path)
        if f:
            out.append(f)
    return out


# ── 11. no trade legs / sizing / hedge ratios / execution ─────────────────────────

def _trade_scan(body: str) -> Optional[str]:
    """Return the first no-trade-lexicon hit in ``body`` (minus the disclaimer line), or None.

    Re-implements the integrator's ``_trade_hit`` here (rather than importing it) so the
    validator stays robust to that private helper being renamed — but it reuses the SAME
    ``_TRADE_PATTERNS`` and ``_NO_TRADE_LINE`` constants, so the lexicon never drifts."""
    low = body.lower().replace(_NO_TRADE_LINE.lower(), "")
    for pat in _TRADE_PATTERNS:
        m = re.search(pat, low)
        if m:
            return m.group(0).strip()
    return None


def page_no_trade_language(content: str, path: Optional[str] = None) -> Optional[ValidationFinding]:
    """Pure predicate: a page body carries no trade/sizing/hedge-ratio/execution directive.

    Reuses ``_TRADE_PATTERNS`` (the mandatory ``_NO_TRADE_LINE`` disclaimer is excluded before
    scanning, exactly as the integrator does). Returns an error finding on a hit, else
    ``None``."""
    hit = _trade_scan(content)
    if hit:
        return ValidationFinding(
            check="no_trade_language", severity="error", path=path,
            message=f"trade/execution directive detected: {hit!r} "
                    "(discovery mode emits no trades/sizing/hedge ratios)")
    return None


def check_no_trade_language(
    target: Union[WikiUpdatePlan, WikiIntegrationResult, PathLike],
) -> list[ValidationFinding]:
    """Check 11: no page body contains trade/sizing/hedge-ratio/execution language.

    Accepts EITHER a plan/result (scans planned writes) OR a ``wiki_root`` path (scans pages
    on disk). Delegates per-page to :func:`page_no_trade_language`. Returns a list (empty when
    clean)."""
    out: list[ValidationFinding] = []
    if isinstance(target, (WikiUpdatePlan, WikiIntegrationResult)):
        for w in _plan_writes(target):
            f = page_no_trade_language(w.content, w.path)
            if f:
                out.append(f)
        return out
    # on-disk
    root = Path(target)
    for p in _iter_pages(root):
        f = page_no_trade_language(_read(p), str(p.relative_to(root)))
        if f:
            out.append(f)
    return out


# ── 12. index.md links to all created pages ──────────────────────────────────────

def check_index_links_all(
    wiki_root: PathLike,
    created_slugs: Union[Iterable[str], WikiIntegrationResult, WikiUpdatePlan],
) -> list[ValidationFinding]:
    """Check 12: every created page slug appears as a ``[[slug]]`` in ``index.md``.

    On-disk scan of ``<wiki_root>/index.md``. ``created_slugs`` may be an explicit iterable of
    slugs, or a plan/result (from which created knowledge-page slugs — non-``append`` writes —
    are derived via each write's filename stem). Emits an error per missing slug, plus one
    error if ``index.md`` is absent. Returns a list (empty when clean)."""
    if isinstance(created_slugs, (WikiUpdatePlan, WikiIntegrationResult)):
        slugs = [Path(w.path).stem for w in _plan_writes(created_slugs)
                 if w.action != "append"]
    else:
        slugs = [s.strip() for s in created_slugs]

    index = Path(wiki_root) / "index.md"
    if not index.exists():
        return [ValidationFinding(
            check="index_links_all", severity="error", path="index.md",
            message="index.md does not exist — created pages are unreachable from the index")]
    linked = set(_wikilinks(_read(index)))
    out: list[ValidationFinding] = []
    for slug in slugs:
        if not slug:
            continue
        # accept the bare stem or any namespaced [[ns:stem]] form
        if slug in linked or any(t.split(":")[-1] == slug for t in linked):
            continue
        out.append(ValidationFinding(
            check="index_links_all", severity="error", path="index.md",
            message=f"created page [[{slug}]] is not linked from index.md"))
    return out


# ── 13. log.md has exactly one append entry for an integration ────────────────────

def check_log_single_entry(
    wiki_root: PathLike,
    source_slug: str,
) -> list[ValidationFinding]:
    """Check 13: ``log.md`` contains exactly ONE WikiIntegrator ingest entry for ``source_slug``.

    On-disk scan of ``<wiki_root>/log.md``. Counts lines that record an integration of this
    source (the integrator writes ``... WikiIntegrator: integrated \\`<slug>\\` ...``). Zero ⇒
    error (not recorded); more than one ⇒ error (idempotency violated — a re-run double-logged).
    Useful as an idempotency assertion. Returns a list (empty when exactly one)."""
    log = Path(wiki_root) / "log.md"
    if not log.exists():
        return [ValidationFinding(
            check="log_single_entry", severity="error", path="log.md",
            message="log.md does not exist — integration was not recorded")]
    text = _read(log)
    # Match the PART-8 integrator's append format: a header line ``## [<date>] ingest | <slug>``
    # (one per integration; idempotent re-runs skip). Anchored on the slug at end-of-line so a
    # slug that is a prefix of another cannot double-count.
    pat = re.compile(
        r"^##\s*\[[^\]]*\]\s*ingest\s*\|\s*" + re.escape(source_slug) + r"\s*$", re.I | re.M)
    n = len(pat.findall(text))
    if n == 1:
        return []
    if n == 0:
        return [ValidationFinding(
            check="log_single_entry", severity="error", path="log.md",
            message=f"no WikiIntegrator ingest entry for '{source_slug}' in log.md")]
    return [ValidationFinding(
        check="log_single_entry", severity="error", path="log.md",
        message=f"{n} WikiIntegrator ingest entries for '{source_slug}' in log.md "
                "(expected exactly 1 — idempotency violation)")]


# ── 14. memory-map.md updated ─────────────────────────────────────────────────────

def check_memory_map_updated(
    wiki_root: PathLike,
    source_slug: str,
    *,
    theme_slugs: Optional[Iterable[str]] = None,
) -> list[ValidationFinding]:
    """Check 14: ``memory-map.md`` exists and references the integrated source (and themes).

    On-disk scan of ``<wiki_root>/memory-map.md`` (``memory_map.md`` accepted as a fallback
    name). Errors if the file is absent or the ``source_slug`` is not mentioned; warns per
    ``theme_slug`` not referenced. Returns a list (empty when fully referenced)."""
    root = Path(wiki_root)
    mm = root / "memory-map.md"
    if not mm.exists():
        alt = root / "memory_map.md"
        mm = alt if alt.exists() else mm
    if not mm.exists():
        return [ValidationFinding(
            check="memory_map_updated", severity="error", path="memory-map.md",
            message="memory-map.md does not exist")]
    text = _read(mm)
    out: list[ValidationFinding] = []
    if source_slug not in text:
        out.append(ValidationFinding(
            check="memory_map_updated", severity="error", path="memory-map.md",
            message=f"memory-map.md does not reference integrated source '{source_slug}'"))
    for t in (theme_slugs or []):
        if t and t not in text:
            out.append(ValidationFinding(
                check="memory_map_updated", severity="warning", path="memory-map.md",
                message=f"memory-map.md does not reference theme '{t}' for source '{source_slug}'"))
    return out


# ── top-level aggregator ──────────────────────────────────────────────────────────


def validate_all(
    *,
    wiki_root: Optional[PathLike] = None,
    plan_or_result: Optional[Union[WikiUpdatePlan, WikiIntegrationResult]] = None,
    raw_text: Optional[str] = None,
    source_slug: Optional[str] = None,
    theme_slugs: Optional[Iterable[str]] = None,
    extra_slugs: Optional[Iterable[str]] = None,
) -> ValidationReport:
    """Run every applicable validator and aggregate into a :class:`ValidationReport`.

    Each check runs only when its inputs are supplied, so this composes cleanly for either a
    PLAN-LEVEL pass (pass ``plan_or_result`` [+ ``raw_text``]) or an ON-DISK pass (pass
    ``wiki_root`` [+ ``source_slug``/``theme_slugs``]) or both:

      * ``plan_or_result``       → checks 1 (frontmatter), 10 (copyright, needs ``raw_text``),
                                    11 (no-trade), 12 (index, needs ``wiki_root``).
      * ``wiki_root``            → checks 2 (links), 3 (theme evidence), 4 (promoted source),
                                    5 (access_class), 7 (method conclusions),
                                    8 (historical disclaimer), 11 (no-trade on disk).
      * ``wiki_root`` + ``source_slug`` → checks 13 (log), 14 (memory-map).

    Checks 6 (case/phase-A) and 9 (forecast expiry) are per-call PURE PREDICATES that need
    caller-supplied flags/dates, so they are NOT auto-run here — call them directly.
    """
    report = ValidationReport()

    if plan_or_result is not None:
        report.extend(check_frontmatter_present(plan_or_result))
        report.extend(check_no_trade_language(plan_or_result))
        if raw_text is not None:
            report.extend(check_no_long_copyright(plan_or_result, raw_text))

    if wiki_root is not None:
        report.extend(check_wikilinks_resolve(wiki_root, extra_slugs=extra_slugs))
        report.extend(check_theme_pages_cite_evidence(wiki_root))
        report.extend(check_promoted_clusters_have_sources(wiki_root))
        report.extend(check_access_class_present(wiki_root))
        report.extend(check_method_pages_no_case_conclusions(wiki_root))
        report.extend(check_historical_cases_not_current(wiki_root))
        report.extend(check_no_trade_language(wiki_root))
        if plan_or_result is not None:
            report.extend(check_index_links_all(wiki_root, plan_or_result))
        if source_slug is not None:
            report.extend(check_log_single_entry(wiki_root, source_slug))
            report.extend(check_memory_map_updated(wiki_root, source_slug, theme_slugs=theme_slugs))

    return report
