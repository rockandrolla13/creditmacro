"""Temporal context + historical-case discipline — PART 1: schemas.

The engine must distinguish a HISTORICAL source fact, an EXPIRED forecast, a CURRENT-input
claim, a TIMELESS method rule, and a case that should be routed to OUTCOME evaluation rather
than current-strategy discovery. These models carry that distinction with firewall-critical
invariants enforced by construction:

  * a method rule is timeless and is the ONLY thing usable as Phase-A method context;
  * a historical / stale / expired / current claim can NEVER be loaded as method context;
  * an expired forecast forces an outcome check and a current-update flag (you cannot present a
    historical forecast as a current market view without re-grounding it).

`current_date` is always supplied by the caller (deterministic — no wall-clock call here), so the
layer is reproducible and replay-safe. The classifier that POPULATES these models is a later part.
"""
from __future__ import annotations

from datetime import date, timedelta
from typing import Literal, Optional

from pydantic import BaseModel, model_validator

HorizonType = Literal["days", "weeks", "months", "quarter", "year", "unspecified"]
HorizonStatus = Literal["active", "expired", "not_yet_started", "unknown"]
TemporalRole = Literal[
    "current_report", "historical_case", "method_source", "outcome_candidate",
    "stale_case", "unknown",
]
ClaimKind = Literal[
    "historical_fact", "historical_forecast", "source_opinion", "current_fact",
    "current_forecast", "method_rule", "unknown",
]
TemporalStatus = Literal["current", "stale", "expired", "timeless_method", "unknown"]
AllowedUse = Literal[
    "current_input_evidence", "method_context", "historical_context_only",
    "phase_b_only", "not_allowed",
]


class ForecastHorizon(BaseModel):
    """A dated/forward-looking claim and whether its horizon is still live. An expired horizon
    forces an outcome check (the forecast becomes something to SCORE, not to act on)."""
    claim_id: Optional[str] = None
    source_page: Optional[int] = None
    claim: str
    forecast_start_date: Optional[date] = None
    forecast_end_date: Optional[date] = None
    horizon_text: Optional[str] = None
    horizon_type: HorizonType
    status: HorizonStatus
    outcome_check_required: bool
    outcome_variable: Optional[str] = None

    @model_validator(mode="after")
    def _temporal_invariants(self) -> "ForecastHorizon":
        if (self.forecast_start_date and self.forecast_end_date
                and self.forecast_end_date < self.forecast_start_date):
            raise ValueError("forecast_end_date precedes forecast_start_date")
        if self.status == "expired" and not self.outcome_check_required:
            raise ValueError("an expired forecast horizon must set outcome_check_required=True")
        return self


class TemporalClaimStatus(BaseModel):
    """The temporal classification of ONE claim and how it may be used in Phase A. Encodes the
    firewall: only a timeless method rule is Phase-A method context; nothing else ever is."""
    claim_id: str
    claim_text: str
    claim_kind: ClaimKind
    temporal_status: TemporalStatus
    allowed_use_in_phase_a: AllowedUse
    rationale: str

    @model_validator(mode="after")
    def _firewall_invariants(self) -> "TemporalClaimStatus":
        is_method = self.claim_kind == "method_rule"
        if is_method:
            if self.temporal_status != "timeless_method":
                raise ValueError("a method_rule must have temporal_status='timeless_method'")
            if self.allowed_use_in_phase_a != "method_context":
                raise ValueError("a method_rule must be used as 'method_context'")
        if self.temporal_status == "timeless_method" and not is_method:
            raise ValueError("temporal_status 'timeless_method' requires claim_kind='method_rule'")
        if not is_method and self.allowed_use_in_phase_a == "method_context":
            raise ValueError(
                "only a method_rule may be used as Phase-A method_context; a historical / "
                "current / case claim must not be loaded as method memory")
        return self


class TemporalContext(BaseModel):
    """Source-level temporal picture: how old the source is, which forecasts have expired, which
    mechanisms survive, and whether the case needs a current update / outcome evaluation."""
    source_slug: str
    source_date: Optional[date] = None
    publication_date: Optional[date] = None
    as_of_date: Optional[date] = None
    current_date: date
    source_age_days: Optional[int] = None
    temporal_role: TemporalRole
    forecast_horizons: list[ForecastHorizon] = []
    time_sensitive_claims: list[str] = []
    stale_claims: list[str] = []
    expired_forecasts: list[str] = []
    still_relevant_mechanisms: list[str] = []
    current_update_required: bool
    warnings: list[str] = []

    @model_validator(mode="after")
    def _temporal_invariants(self) -> "TemporalContext":
        # auto-derive age from the best available source date when not supplied
        anchor = self.source_date or self.publication_date or self.as_of_date
        if self.source_age_days is None and anchor is not None:
            object.__setattr__(self, "source_age_days", (self.current_date - anchor).days)
        # an expired forecast (named in the list OR a horizon) means the source's forward view
        # cannot be presented as current without re-grounding ⇒ a current update is required.
        has_expired = bool(self.expired_forecasts) or any(
            h.status == "expired" for h in self.forecast_horizons)
        if has_expired and not self.current_update_required:
            raise ValueError("expired forecasts present: current_update_required must be True")
        return self


# ── PART 2: deterministic temporal classifier (no wall clock; current_date is supplied) ──

import re as _re

_RECENT_DAYS = 180           # <= this age ⇒ 'recent' (current_report only if it IS the current input)
_TWO_YEARS = 730             # > this age ⇒ historical_case (outcome_candidate if forecasts expired)
_OPINION = ("we think", "we believe", "attractive", "unattractive", "cheap", "rich", "prefer",
            "neutral", "underweight", "overweight", "downgrade", "upgrade", "we remain")
# forecast VERBS make a claim a forecast even without a datable horizon phrase (PART-5)
_FORECAST_VERBS = ("expect", "project", "forecast", "points to", "point to", "implies", "imply",
                   "should", "upside to", "upside for", "downside by", "downside for", "set to",
                   "target", "we see")
_MONTHS = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}
_Q_END_MONTH = {1: 3, 2: 6, 3: 9, 4: 12}
# FORWARD markers make a claim a forecast (a forward horizon with a resolvable end date).
_FORWARD_PAT = _re.compile(
    r"by\s+(?:early |mid[- ]?|late )?q[1-4]?"
    r"|by\s+(?:end[- ])?(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*"
    r"|(?:over\s+the\s+)?coming\s+(?:six\s+)?months|next\s+(?:quarter|month|year)"
    r"|by\s+(?:year[- ]?end|mid[- ]?year|20\d\d)|by\s+(?:early|mid|late)[- ]?20\d\d"
    r"|going\s+forward", _re.I)
# BACKWARD markers anchor a realized window's START — they do NOT make a fact a forecast.
_BACKWARD_PAT = _re.compile(
    r"\bytd\b|year\s+to\s+date|since\s+the\s+start\s+of\s+the\s+year"
    r"|since\s+(?:early\s+)?(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*", _re.I)


def _add_months(d: date, n: int) -> date:
    m = d.month - 1 + n
    y = d.year + m // 12
    return date(y, m % 12 + 1, min(d.day, 28))


def _last_day(year: int, month: int) -> date:
    first_of_next = date(year + (month == 12), (month % 12) + 1, 1)
    return first_of_next - timedelta(days=1)


def _horizon_type(text: str) -> HorizonType:
    low = text.lower()
    if "q1" in low or "q2" in low or "q3" in low or "q4" in low or "quarter" in low:
        return "quarter"
    if "months" in low or any(f"by {m}" in low or f"by end-{m}" in low for m in _MONTHS):
        return "months"
    if "year" in low or _re.search(r"20\d\d", low):
        return "year"
    if "weeks" in low:
        return "weeks"
    if "days" in low:
        return "days"
    return "unspecified"


def _resolve_forward_end(text: str, src: Optional[date]) -> Optional[date]:
    """Approximate forecast_end_date for a forward horizon, generic by year/quarter (PART-4)."""
    if src is None:
        return None
    low = text.lower()
    yr = src.year
    m = _re.search(r"(early|mid|late)?[- ]?q\s*([1-4])", low)
    if m:
        qn = int(m.group(2))
        end_month = _Q_END_MONTH[qn]            # quarter-end month (3/6/9/12)
        pos = m.group(1)
        if pos == "early":
            return _last_day(yr, end_month - 2)  # early Q2 → 30 Apr
        if pos == "mid":
            return date(yr, end_month - 1, 15)   # mid-Q2 → 15 May
        return _last_day(yr, end_month)          # late / plain → quarter end
    if "mid-year" in low or "mid year" in low:
        return date(yr, 6, 30)
    if "year-end" in low or "year end" in low:
        return date(yr, 12, 31)
    if "coming" in low and ("six months" in low or "six-month" in low):
        return _add_months(src, 6)
    if "coming months" in low or "going forward" in low:
        return _add_months(src, 3)              # default forward window unless a stronger cue exists
    if "next quarter" in low:
        return _add_months(src, 3)
    if "next month" in low:
        return _add_months(src, 1)
    if "next year" in low:
        return _add_months(src, 12)
    for name, mon in _MONTHS.items():
        if f"by {name}" in low or f"by end-{name}" in low or f"by end {name}" in low:
            return _last_day(yr, mon)
    ym = _re.search(r"by\s+(?:early|mid|late)?[- ]?(20\d\d)", low)
    if ym:
        return date(int(ym.group(1)), 12, 31)
    return None


def _resolve_backward_start(text: str, src: Optional[date]) -> Optional[date]:
    """START of a realized window from a backward marker (PART-4). Anchors forecast_start_date;
    does NOT make a realized fact a forecast."""
    if src is None:
        return None
    low = text.lower()
    if "ytd" in low or "year to date" in low or "since the start of the year" in low:
        return date(src.year, 1, 1)
    m = _re.search(r"since\s+(?:early\s+)?(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*", low)
    if m:
        mon = _MONTHS[m.group(1)]
        year = src.year if mon <= src.month else src.year - 1   # 'since Dec' in a March report ⇒ prior Dec
        return date(year, mon, 1)
    return None


def _make_horizon(claim_id, page, text, src, current_date, age_days) -> ForecastHorizon:
    end = _resolve_forward_end(text, src)
    start = _resolve_backward_start(text, src) or src      # backward window anchors the start
    if start is not None and end is not None and end < start:
        start = src                                         # guard against inconsistent windows
    if end is None:
        status = "expired" if (age_days is not None and age_days > 365) else "unknown"
    elif end < current_date:
        status = "expired"
    elif src is not None and src > current_date:
        status = "not_yet_started"
    else:
        status = "active"
    expired = status == "expired"
    return ForecastHorizon(
        claim_id=claim_id, source_page=page, claim=text,
        forecast_start_date=start, forecast_end_date=end,
        horizon_text=text, horizon_type=_horizon_type(text),
        status=status, outcome_check_required=expired,
        outcome_variable=(" ".join(text.split()[:6]) if expired else None))


def _page(source_location: Optional[str]) -> Optional[int]:
    m = _re.match(r"page:(\d+)", source_location or "")
    return int(m.group(1)) if m else None


def _role_and_update(access_class, age, has_expired, source_missing, is_current_input):
    """Source-level role + whether a current update is required (PART-3 thresholds).

    A METHOD source is never stale by age. A CASE source: missing date → unknown; <=180d →
    current_report only if it IS the current input, else a recent historical_case; 180d–2y →
    stale_case; >2y → historical_case, or outcome_candidate if it carries expired forecasts.
    A historical report stays useful (process/analogue/outcome) but cannot be a current view —
    so anything older than 180 days (or undated, or with expired forecasts) flags a current update.
    """
    if access_class == "method":
        return "method_source", False
    if source_missing or age is None:
        return "unknown", True
    if age <= _RECENT_DAYS:
        return ("current_report" if is_current_input else "historical_case"), has_expired
    if age > _TWO_YEARS:
        return ("outcome_candidate" if has_expired else "historical_case"), True
    return "stale_case", True


def _allowed_use(kind: str, is_current_input: bool) -> AllowedUse:
    """Phase-A admissibility (PART-5 rules). Only a method_rule is method_context. When the source
    IS the current input (incl. a historical-case analysis run), its claims are current_input_evidence.
    When it is archived, forecasts/opinions are phase_b_only and facts are historical_context_only —
    a non-method claim is NEVER method_context."""
    if kind == "method_rule":
        return "method_context"
    if is_current_input:
        return "current_input_evidence"
    if kind in ("historical_forecast", "current_forecast", "source_opinion"):
        return "phase_b_only"
    return "historical_context_only"


def classify_temporal_context(*, source_slug, access_class, source_date, current_date,
                              claims, mechanisms, explicit_as_of_date=None, is_current_input=False):
    """claims: list of (claim_id, page|None, text). mechanisms: list[str] (driver → outcome)."""
    src = explicit_as_of_date or source_date
    age = (current_date - src).days if src else None
    is_method = access_class == "method"
    source_missing = src is None and not is_method
    warnings: list[str] = []
    if source_missing:
        warnings.append("source_date_missing: temporal classification is best-effort")
    # claims are 'current' only when the source is a current report (recent AND the current input)
    is_current = (age is not None and age <= _RECENT_DAYS and is_current_input)

    horizons: list[ForecastHorizon] = []
    statuses: list[TemporalClaimStatus] = []
    for cid, page, text in claims:
        low = (text or "").lower()
        is_horizon = bool(_FORWARD_PAT.search(text or ""))           # has a datable forward horizon
        is_forecast = is_horizon or any(v in low for v in _FORECAST_VERBS)
        opinion = any(w in low for w in _OPINION)
        if is_horizon and not is_method:
            h = _make_horizon(cid, page, text, src, current_date, age)
            horizons.append(h)
            horizon_expired = h.status == "expired"
        else:
            horizon_expired = False
        # a forecast lapses if its horizon expired, or (no datable horizon) the source is > 1y old
        forecast_expired = horizon_expired or (not is_horizon and age is not None and age > 365)

        if is_method:
            kind, tstatus = "method_rule", "timeless_method"
        elif is_forecast:                                            # forecast/projection (PART-5 rule 2)
            kind = "current_forecast" if is_current else "historical_forecast"
            tstatus = "current" if is_current else ("expired" if forecast_expired else "stale")
        elif opinion:                                                # source opinion (rule 4)
            kind, tstatus = "source_opinion", ("current" if is_current else "stale")
        else:                                                        # factual observation (rule 1)
            kind = "current_fact" if is_current else "historical_fact"
            tstatus = "current" if is_current else "stale"
        use = _allowed_use(kind, is_current_input)
        statuses.append(TemporalClaimStatus(
            claim_id=cid, claim_text=text, claim_kind=kind, temporal_status=tstatus,
            allowed_use_in_phase_a=use,
            rationale=f"{kind}/{tstatus} (source age {age}d)" if age is not None else f"{kind}/{tstatus}"))

    has_expired = any(h.status == "expired" for h in horizons)
    role, current_update = _role_and_update(access_class, age, has_expired, source_missing,
                                            is_current_input)

    ctx = TemporalContext(
        source_slug=source_slug, source_date=src, current_date=current_date,
        temporal_role=role, forecast_horizons=horizons,
        time_sensitive_claims=[t for _, _, t in claims
                               if _FORWARD_PAT.search(t or "") or _BACKWARD_PAT.search(t or "")],
        stale_claims=[s.claim_text for s in statuses if s.temporal_status == "stale"],
        expired_forecasts=[h.claim for h in horizons if h.status == "expired"],
        still_relevant_mechanisms=list(mechanisms or []),
        current_update_required=current_update, warnings=warnings)
    return ctx, statuses, horizons, warnings


def classify_temporal_role(source_classification, extraction_bundle, current_date,
                           is_current_input: bool = False) -> "TemporalContext":
    """PART-3 source-level entry point: build the TemporalContext from a SourceClassification +
    EvidenceExtractionBundle (duck-typed to avoid an import cycle). Returns only the context."""
    raw = (getattr(extraction_bundle, "source_page_fields", {}) or {}).get("source_date")
    src = None
    if isinstance(raw, str) and raw.strip():
        try:
            src = date.fromisoformat(raw.strip())
        except ValueError:
            src = None
    claims = [(a.evidence_id or f"c{i}", _page(a.source_location), a.claim)
              for i, a in enumerate(extraction_bundle.evidence_atoms)]
    mechanisms = [f"{c.driver} → {c.outcome}" for c in extraction_bundle.causal_claims]
    ctx, _statuses, _horizons, _warnings = classify_temporal_context(
        source_slug=source_classification.source_slug,
        access_class=source_classification.access_class, source_date=src,
        current_date=current_date, claims=claims, mechanisms=mechanisms,
        is_current_input=is_current_input)
    return ctx
