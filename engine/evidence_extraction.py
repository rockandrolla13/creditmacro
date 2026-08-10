"""PART 3 — deterministic, rule-assisted CASE-source extraction.

Turns a CASE source's normalized markdown into an EvidenceExtractionBundle: source-backed
evidence atoms (figure-bearing, page-cited, concise), causal claims, operational axes,
confounders, candidate falsifiers, and strategy-family hints — the GENERAL replacement for the
hand-built JPM extraction. It never generates trades, scenarios, probabilities, fair values,
sizing, hedge ratios, or execution, and it reproduces no long verbatim source text. The bundle is
CASE memory (source-derived); the agent does not write wiki pages.
"""
from __future__ import annotations

import re
from typing import Literal, Optional

from pydantic import BaseModel, Field

from .schema import EvidenceAtom
from .temporal import ForecastHorizon, TemporalClaimStatus, TemporalContext

# ── schemas ─────────────────────────────────────────────────────────────────────

class EvidenceExtractionInput(BaseModel):
    source_slug: str
    source_type: str
    access_class: Literal["case"]          # extraction runs ONLY on case sources (rejects others)
    normalized_markdown: str
    page_manifest: Optional[dict] = None
    source_date: Optional[str] = None
    author_or_publisher: Optional[str] = None
    current_input: bool = False
    # caller-supplied current_date (ISO string) for temporal context. NEVER defaulted to "today":
    # if it (or source_date) is missing, temporal context is simply not computed and a warning fires.
    current_date: Optional[str] = None
    is_current_input: bool = False         # only a CURRENT input may be a 'current_report'
    # (L5) fail-closed temporal grounding. Default False = warn-and-skip (back-compatible). When a
    # discovery/strict run sets this True, a missing/unparseable current_date RAISES instead of
    # silently degrading — closing the "old report reads as current" path.
    require_current_date: bool = False


class CausalClaimCandidate(BaseModel):
    driver: str
    transmission: str
    outcome: str
    source_evidence_ids: list[str] = []
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str


class OperationalAxisCandidate(BaseModel):
    axis_name: str
    axis_shape: str
    axis_direction: Optional[str] = None
    observable_series: str
    source_evidence_ids: list[str] = []
    required_adjustments: list[str] = []
    data_needed_next: str = ""


class StrategyFamilyHint(BaseModel):
    family: str
    rationale: str
    source_evidence_ids: list[str] = []
    confidence: float = Field(ge=0.0, le=1.0)
    downstream_model_hint: str = ""


class EvidenceExtractionBundle(BaseModel):
    source_slug: str
    source_page_fields: dict = {}
    evidence_atoms: list[EvidenceAtom] = []
    main_developments: list[str] = []
    key_events: list[str] = []
    hot_topics: list[str] = []
    core_theme_candidates: list[str] = []
    causal_claims: list[CausalClaimCandidate] = []
    operational_axes: list[OperationalAxisCandidate] = []
    confounders: list[str] = []
    falsifiers: list[str] = []
    strategy_family_hints: list[StrategyFamilyHint] = []
    scenario_candidates: list[dict] = []
    open_questions: list[str] = []
    extraction_warnings: list[str] = []
    no_trade_confirmation: str = ""
    # PART 9 — optional temporal context (populated by EvidenceExtractionAgent only when BOTH
    # source_date AND current_date are supplied; otherwise None/[] and a warning fires). All
    # defaulted so existing callers are unaffected. No outcome_candidates schema exists, so none added.
    temporal_context: Optional[TemporalContext] = None
    temporal_claim_statuses: list[TemporalClaimStatus] = []
    forecast_horizons: list[ForecastHorizon] = []


# ── lexicons (general, multi-domain — NOT JPM-specific) ──────────────────────────

_CONNECTIVES = ("because", "due to", "leads to", "causes", "reflects", "drives", "driving",
                "results in", "implies", "as a result", "creates", "pressures", "supports",
                "weakens")
_FORECAST = ("expect", "expects", "forecast", "project", "guidance", "outlook", "anticipate")
_OPINION = ("we think", "we believe", "attractive", "unattractive", "cheap", "rich", "prefer",
            "crowded")
_ENTITY_KEYS = {
    "hyperscaler": "hyperscaler", "data-center": "data center", "data center": "data center",
    "hpc": "HPC", "technology": "technology", "etf": "ETF", "software": "software",
    "private credit": "private credit", "juli": "JULI", "hy index": "HY index", " hy ": "HY",
}
_MV_KEYS = {
    "oas": "OAS", "spread": "spread", "basis": "basis", "index weight": "index weight",
    "return": "return", "issuance": "issuance", "nav": "NAV", "premium": "premium",
    "discount": "discount", "dispersion": "dispersion", "margin": "margin",
    "input-cost": "input-cost", "pricing power": "pricing power", "pricing-power": "pricing power",
}
_CONFOUNDER_KEYS = (
    "rating", "duration", "liquidity", "sector beta", "market beta", "issue size",
    "index eligibility", "index-inclusion", "index inclusion", "vintage", "new issue concession",
    "guarantee", "construction risk", "tenant concentration", "funding structure", "recovery",
    "balance sheet", "beta",
)
# theme signal → concise theme label, with optional co-occurrence guard `requires_any` to avoid
# substring false positives (e.g. "non-refinancing" or a bare "ETFs" mention). General/multi-domain;
# themes EMERGE from which signals the text actually contains.
_THEME_SIGNALS = [
    ("ecosystem", "credit ecosystem", ()), ("capex", "AI capex funding", ()),
    ("ai infrastructure", "AI infrastructure credit", ()),
    ("hyperscaler", "hyperscaler-project basis", ()), ("hpc", "HPC supply", ()),
    ("crowding", "crowding and supply", ()),
    ("index inclusion", "index-inclusion technicals", ()), ("inclusion", "index-inclusion technicals", ()),
    ("data center", "data-center credit", ()), ("data-center", "data-center credit", ()),
    ("decompression", "spread decompression", ()),
    ("refinancing", "refinancing stress", ("stress", "distress", "default", "maturity")),
    ("software", "software credit", ()), ("private credit", "private-credit stress", ()),
    ("etf", "ETF flow dislocation", ("flow", "create", "redeem", "premium to nav")),
    ("create-redeem", "ETF flow dislocation", ()),
    ("margin", "margin compression", ()), ("pricing power", "pricing-power dispersion", ()),
    ("inflation", "inflation/pricing pressure", ()), ("dispersion", "sector dispersion", ()),
]
_DEV_VERBS = ("has become", "entered", "reached", "rose", "grown", "emerged", "widened", "tightened")

_NUM = re.compile(r"[-+]?\d+(?:\.\d+)?")

# Author-set confidences for the RULE extractor. Named rather than inlined because
# they encode a policy — how much to trust a pattern match — and an unnamed 0.5
# appearing twice for two different reasons reads as one decision when it is two.
#
# All three are provisional by design. They are what PLAN-authoritative-harness.md
# G4 calls the false-precision trap: a number the author picked, presented with the
# same authority as a measured one. G4 replaces them with confidence computed from
# harness-observed signals (span found, numbers verified, source reliability,
# independence, freshness). Naming them now makes that replacement reviewable —
# a diff that deletes named constants is legible; one that deletes stray 0.5s is not.
_RULE_ATOM_CONFIDENCE = 0.8       # a sentence matched the extraction rules verbatim
_CAUSAL_CANDIDATE_CONFIDENCE = 0.5  # an explicit connective was present; direction unverified
_FAMILY_HINT_CONFIDENCE = 0.5     # a family is plausible from signals alone; nothing scored yet

# Boilerplate that should never become an evidence atom (footers, contacts, disclosures).
_NOISE = ("research", "distributed", "disclosure", "certification", "source: bloomberg",
          "analyst certification", "mci(p)", "appendix")
_PHONE = re.compile(r"\+\d{2}-\d")


def _is_noise(sentence: str) -> bool:
    if _PHONE.search(sentence):
        return True
    low = sentence.lower()
    # a recurring page footer carries the publisher + date together
    if "deutsche bank" in low and ("march 2019" in low or "research" in low):
        return True
    return any(k in low for k in _NOISE)


def _trim(text: str, n: int = 18) -> str:
    return " ".join(text.split()[:n])


def _detect(text: str, keymap: dict) -> list[str]:
    t = f" {text.lower()} "
    out, seen = [], set()
    for k, v in keymap.items():
        if k in t and v not in seen:
            seen.add(v)
            out.append(v)
    return out


def _iter_sentences(md: str):
    page = None
    for raw_line in md.splitlines():
        m = re.search(r"page:(\d+)", raw_line)
        if m and "<!--" in raw_line:
            page = int(m.group(1))
            continue
        for sent in re.split(r"(?<=[.;])\s+", raw_line.strip()):
            s = sent.strip()
            if len(s.split()) >= 3:
                yield page, s


def _claim_kind(sentence: str) -> str:
    t = sentence.lower()
    if any(w in t for w in _OPINION):
        return "source_opinion"
    if any(w in t for w in _FORECAST):
        return "source_forecast"
    return "source_fact"


def _shape_for(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ("nav", "etf", "basket", "premium", "discount")):
        return "basis"
    if any(k in t for k in ("curve", "slope", "steepen", "flatten", "5s30s", "2s10s")):
        return "curve"
    if any(k in t for k in ("cash", "cds")):
        return "basis"
    if "equity" in t:
        return "cross_asset"
    return "relative_value"


def _direction_for(text: str) -> Optional[str]:
    t = text.lower()
    if "widen" in t or "wider" in t:
        return "wider"
    if "tighten" in t or "tighter" in t:
        return "tighter"
    if "steepen" in t:
        return "steeper"
    if "flatten" in t:
        return "flatter"
    return None


def extract_evidence(inp: EvidenceExtractionInput) -> EvidenceExtractionBundle:
    md = inp.normalized_markdown
    slug = inp.source_slug
    full = md.lower()
    sentences = list(_iter_sentences(md))

    # 1) evidence atoms — every figure-bearing sentence, concise + page-cited
    atoms: list[EvidenceAtom] = []
    for page, sent in sentences:
        nums = [float(x) for x in _NUM.findall(sent)]
        # keep figure-bearing sentences, dropping boilerplate footers/contacts/disclosures
        if not nums or _is_noise(sent):
            continue
        n = len(atoms) + 1
        atoms.append(EvidenceAtom(
            evidence_id=f"{slug}-{n:03d}",
            source_slug=slug,
            source_location=f"page:{page}" if page is not None else "source",
            claim=_trim(sent, 18),                       # concise; <25-word run ⇒ no verbatim leak
            claim_kind=_claim_kind(sent),
            entities=_detect(sent, _ENTITY_KEYS),
            market_variables=_detect(sent, _MV_KEYS),
            numbers=nums,
            confidence=_RULE_ATOM_CONFIDENCE,
            agent_use="case evidence (current-input eligible)",
        ))
    all_ids = [a.evidence_id for a in atoms if a.evidence_id]

    def _ids_on_page(page) -> list[str]:
        return [a.evidence_id for a in atoms
                if a.evidence_id and a.source_location == (f"page:{page}" if page is not None else "source")]

    # 2) causal claims — split on connectives
    causal: list[CausalClaimCandidate] = []
    for page, sent in sentences:
        low = sent.lower()
        for conn in _CONNECTIVES:
            if conn in low:
                i = low.index(conn)
                driver = _trim(sent[:i], 12).strip(" ,.")
                outcome = _trim(sent[i + len(conn):], 12).strip(" ,.")
                if driver and outcome:
                    causal.append(CausalClaimCandidate(
                        driver=driver, transmission=conn, outcome=outcome,
                        source_evidence_ids=_ids_on_page(page),
                        confidence=_CAUSAL_CANDIDATE_CONFIDENCE,
                        rationale=f"explicit causal connective '{conn}'"))
                break

    # 3) operational axes — relative-value / basis / index-weight / curve patterns
    axes: list[OperationalAxisCandidate] = []
    seen_axis: set = set()

    def _add_axis(name, observable, page):
        key = name.lower()
        if key in seen_axis:
            return
        seen_axis.add(key)
        axes.append(OperationalAxisCandidate(
            axis_name=name, axis_shape=_shape_for(observable),
            axis_direction=_direction_for(observable), observable_series=_trim(observable, 12),
            source_evidence_ids=_ids_on_page(page),
            required_adjustments=_detect(observable, {k: k for k in _CONFOUNDER_KEYS}),
            data_needed_next="both legs' live series and the listed adjustments (downstream)"))

    for page, sent in sentences:
        low = sent.lower()
        for m in re.finditer(r"([a-z0-9 \-]{3,40}?)\s+(?:versus|vs\.?|minus)\s+([a-z0-9 \-]{3,40})", low):
            x, y = m.group(1).strip(), m.group(2).strip()
            _add_axis(f"{x} minus {y}", sent, page)
        if "index weight" in low:
            _add_axis("index weight", "index weight " + sent, page)
        if "nav" in low or ("etf" in low and ("premium" in low or "discount" in low)):
            _add_axis("ETF premium/discount to NAV", "etf nav premium " + sent, page)
        if "dispersion" in low:
            _add_axis("sector spread dispersion", "dispersion " + sent, page)
        if any(k in low for k in ("curve", "slope", "5s30s", "2s10s", "steepen", "flatten")):
            _add_axis("curve slope", "curve " + sent, page)
        if "basis" in low or "relationship" in low:
            _add_axis(_trim(sent, 6) + " basis", "basis " + sent, page)

    # 4) confounders (detected + the standing risk premium)
    confounders = _detect(md, {k: k for k in _CONFOUNDER_KEYS})
    confounders.append("standing credit risk premium (a wide spread is not by itself mispricing)")

    # 5) candidate falsifiers (agent synthesis — separate from source-fact atoms)
    falsifiers: list[str] = [f"{a.axis_name} compresses or inverts instead of moving, and stays there"
                             for a in axes[:4]]
    falsifiers += [
        "the forecasted driver variable fails to move",
        "an alternative explanation (a listed confounder) fully explains the gap",
        "the flow/liquidity effect is absent",
        "fundamentals improve and the differential closes",
        "the relationship proves non-stationary",
    ]

    # 6) strategy-family hints — whole-text keyword routing (generalises across domains)
    fams: dict[str, str] = {}
    if ("etf" in full and ("nav" in full or "basket" in full or "create" in full or "redeem" in full)):
        fams["etf_basket_rv"] = "ETF / create-redeem / NAV-vs-basket language"
    if "index inclusion" in full or "index weight" in full or "benchmark" in full or ("index" in full and "inclusion" in full):
        fams["index_index_rv"] = "index-inclusion / benchmark-ownership language"
    if any(k in full for k in ("minus", "versus", " vs ", "differential", "basis", "relationship", "decompression", "dispersion")):
        fams["long_short"] = "relative-value spread/basis language"
    if "sector" in full and ("dispersion" in full or "rotation" in full):
        fams["sector_rotation"] = "sector-dispersion / rotation language"
    if any(k in full for k in ("curve", "slope", "5s30s", "2s10s", "steepen", "flatten")):
        fams["curve"] = "curve / maturity-slope language"
    if "market beta" in full or ("broad" in full and "beta" in full) or "outright" in full:
        fams["outright"] = "broad-beta language (directional, beta-model caveat)"
    if not fams:
        fams["watchlist_only"] = "no clean operational axis detected"
    _DOWN = {
        "etf_basket_rv": "ETF-vs-basket construction (downstream)",
        "index_index_rv": "index-vs-index construction (downstream)",
        "long_short": "relative-value pair construction (downstream)",
        "sector_rotation": "sector-basket construction (downstream)",
        "curve": "curve construction (downstream)",
        "outright": "instrument selection with a beta-model caveat (downstream)",
        "watchlist_only": "(none yet — needs an axis, scenarios, and a falsifier)",
    }
    hints = [StrategyFamilyHint(family=f, rationale=r, source_evidence_ids=all_ids[:5],
                                confidence=_FAMILY_HINT_CONFIDENCE,
                                downstream_model_hint=_DOWN.get(f, ""))
             for f, r in fams.items()]

    # 7) market intelligence + themes
    developments = [_trim(s, 16) for _, s in sentences if any(v in s.lower() for v in _DEV_VERBS)][:6]
    themes, seen_t = [], set()
    for sig, label, requires_any in _THEME_SIGNALS:
        if sig in full and (not requires_any or any(r in full for r in requires_any)):
            if label not in seen_t:
                seen_t.add(label)
                themes.append(label)
    hot_topics = _detect(md, _ENTITY_KEYS)[:6]

    # scenario candidates ONLY if explicit scenario language (never invent probabilities)
    scenario_candidates: list[dict] = []
    if any(k in full for k in ("scenario", "base case", "bull case", "bear case", "downside case", "upside case")):
        scenario_candidates = [{"name": "see source", "driver_path": "explicit in source",
                                "note": "no probability supplied — must be PM-supplied"}]

    warnings: list[str] = []
    if not atoms:
        warnings.append("no figure-bearing evidence atoms found in source")
    if not axes:
        warnings.append("no operational axis detected — likely watchlist_only")
    if not causal:
        warnings.append("no explicit causal language found")
    if list(fams) == ["watchlist_only"]:
        warnings.append("no strategy family mapped beyond watchlist_only")

    return EvidenceExtractionBundle(
        source_slug=slug,
        source_page_fields={"source_slug": slug, "source_type": inp.source_type,
                            "access_class": "case", "source_date": inp.source_date,
                            "author_or_publisher": inp.author_or_publisher},
        evidence_atoms=atoms,
        main_developments=developments,
        key_events=[s for _, s in sentences if re.search(r"\b20\d\d\b", s)][:5],
        hot_topics=hot_topics,
        core_theme_candidates=themes,
        causal_claims=causal,
        operational_axes=axes,
        confounders=confounders,
        falsifiers=falsifiers,
        strategy_family_hints=hints,
        scenario_candidates=scenario_candidates,
        open_questions=[f"Is the axis a clean differential or contaminated by {confounders[0]}?"]
        if confounders else [],
        extraction_warnings=warnings,
        no_trade_confirmation=("Discovery extraction only: no exact trades, no curve points, "
                               "no hedge ratios, no sizing, no order steps."),
    )
