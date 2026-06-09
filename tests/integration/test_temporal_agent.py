"""Temporal layer PART 2 — TemporalContextAgent.

Populates TemporalContext / ForecastHorizon / TemporalClaimStatus from a SourceClassification +
EvidenceExtractionBundle + caller-supplied current_date. Deterministic (no wall clock). Regressions:
European-equity (old report with expired forecasts → outcome_candidate), a method source, and a
recent case.
"""
from __future__ import annotations

from datetime import date

from engine.evidence_extraction import CausalClaimCandidate, EvidenceExtractionBundle
from engine.schema import EvidenceAtom
from engine.wiki_agents import (
    REGISTRY,
    SourceClassification,
    TemporalContextAgent,
    TemporalContextInput,
    TemporalContextOutput,
)

CURRENT = date(2026, 6, 9)


def _cls(slug, access="case", stype="report"):
    return SourceClassification(
        source_slug=slug, source_type=stype, access_class=access,
        copyright_status="copyrighted_paraphrase_only",
        ingestion_policy="extract_evidence_atoms_case",
        recommended_compilers=["EvidenceExtractionAgent"])


def _atom(eid, claim, page=1, kind="source_fact"):
    return EvidenceAtom(evidence_id=eid, source_slug="s", source_location=f"page:{page}",
                        claim=claim, claim_kind=kind, numbers=[], confidence=0.8)


def _bundle(slug, atoms, mechanisms=None, source_date="2019-03-15"):
    return EvidenceExtractionBundle(
        source_slug=slug, evidence_atoms=atoms,
        source_page_fields={"source_slug": slug, "access_class": "case", "source_date": source_date},
        causal_claims=[CausalClaimCandidate(driver=d, transmission="drives", outcome=o,
                                            confidence=0.5, rationale="r")
                       for d, o in (mechanisms or [])])


def _run(cls, bundle, current=CURRENT, **kw):
    return TemporalContextAgent().run(TemporalContextInput(
        source_classification=cls, extraction_bundle=bundle, current_date=current, **kw))


# ── PART 1: contract + registry ──────────────────────────────────────────────

def test_agent_registered_and_runs():
    assert "TemporalContextAgent" in REGISTRY.list_agents()
    assert REGISTRY.validate_agent_contracts() == []
    out = REGISTRY.run_agent("TemporalContextAgent", TemporalContextInput(
        source_classification=_cls("x"), extraction_bundle=_bundle("x", [_atom("e", "a fact")]),
        current_date=CURRENT))
    assert isinstance(out, TemporalContextOutput)


# ── European Equity Strategy regression (2019 report, current 2026) ──────────

def test_european_equity_routes_to_outcome_candidate():
    atoms = [
        _atom("e1", "US 10-year yields rise to 3.2% by mid-Q2", page=3),
        _atom("e2", "Bund yields rise to 0.6% by Q3", page=3),
        _atom("e3", "Stoxx 600 is 8% above model fair value", page=2),
    ]
    bundle = _bundle("european-equity-strategy-2019-03-15", atoms,
                     mechanisms=[("China credit impulse", "China PMI improvement")],
                     source_date="2019-03-15")
    out = _run(_cls("european-equity-strategy-2019-03-15"), bundle)
    tc = out.temporal_context
    assert tc.temporal_role == "outcome_candidate"
    assert tc.current_update_required is True
    assert tc.source_age_days and tc.source_age_days > 2000
    assert tc.expired_forecasts                     # the dated forecasts are expired
    assert tc.still_relevant_mechanisms             # mechanisms survive

    horizons = {h.claim_id: h for h in out.forecast_horizons}
    assert horizons["e1"].status == "expired" and horizons["e1"].outcome_check_required
    assert horizons["e2"].status == "expired"
    assert "e3" not in horizons                     # not a forecast (no horizon language)

    st = {c.claim_id: c for c in out.claim_statuses}
    assert st["e1"].claim_kind == "historical_forecast" and st["e1"].temporal_status == "expired"
    assert st["e3"].claim_kind == "historical_fact"
    # firewall: no historical claim is ever method_context
    assert all(c.allowed_use_in_phase_a != "method_context" for c in out.claim_statuses)


# ── method source regression ─────────────────────────────────────────────────

def test_method_source_is_timeless_and_method_context():
    bundle = _bundle("pearl-book-of-why",
                     [_atom("m1", "do-calculus separates correlation from causation", kind="source_fact")],
                     source_date=None)
    out = _run(_cls("pearl-book-of-why", access="method", stype="book"), bundle)
    assert out.temporal_context.temporal_role == "method_source"
    assert out.temporal_context.current_update_required is False
    c = out.claim_statuses[0]
    assert c.claim_kind == "method_rule"
    assert c.temporal_status == "timeless_method"
    assert c.allowed_use_in_phase_a == "method_context"


# ── recent case regression ───────────────────────────────────────────────────

def test_recent_case_is_current_report_when_marked_current_input():
    recent = (CURRENT.replace(day=1)).isoformat()  # ~within current month
    atoms = [_atom("r1", "we expect IG spreads to tighten next quarter", page=1)]
    out = _run(_cls("recent-note"), _bundle("recent-note", atoms, source_date=recent),
               is_current_input=True)
    tc = out.temporal_context
    assert tc.temporal_role == "current_report"       # recent AND explicitly current input
    assert tc.current_update_required is False         # future horizon, not expired
    st = out.claim_statuses[0]
    assert st.temporal_status == "current"
    assert st.claim_kind in ("current_forecast", "current_fact")
    if out.forecast_horizons:
        assert out.forecast_horizons[0].status in ("active", "not_yet_started")


# ── PART 3: classify_temporal_role + threshold rules ─────────────────────────

def test_classify_temporal_role_returns_context():
    from datetime import date as _date
    from engine.temporal import TemporalContext, classify_temporal_role
    bundle = _bundle("eq", [_atom("e1", "yields rise to 3.2% by Q3", page=1)],
                     source_date="2019-03-15")
    tc = classify_temporal_role(_cls("eq"), bundle, _date(2026, 6, 9))
    assert isinstance(tc, TemporalContext)
    assert tc.temporal_role == "outcome_candidate"


def test_recent_case_without_current_input_is_historical():
    recent = CURRENT.replace(day=1).isoformat()
    out = _run(_cls("recent-note"), _bundle("recent-note", [_atom("r1", "a recent fact, 5%")],
               source_date=recent), is_current_input=False)
    assert out.temporal_context.temporal_role == "historical_case"


def test_source_date_missing_is_unknown_and_flagged():
    out = _run(_cls("nodate"), _bundle("nodate", [_atom("n1", "a claim with 3%")], source_date=None))
    tc = out.temporal_context
    assert tc.temporal_role == "unknown"
    assert tc.current_update_required is True
    assert any("source_date_missing" in w for w in tc.warnings)


def test_case_between_180d_and_2y_is_stale_case():
    older = (CURRENT - __import__("datetime").timedelta(days=300)).isoformat()
    out = _run(_cls("staleish"), _bundle("staleish", [_atom("s1", "a fact, 4%")], source_date=older))
    tc = out.temporal_context
    assert tc.temporal_role == "stale_case"
    assert tc.current_update_required is True          # >180 days ⇒ needs a current update


def test_method_source_never_stale_by_age():
    out = _run(_cls("old-method", access="method", stype="book"),
               _bundle("old-method", [_atom("m1", "a timeless rule")], source_date="1990-01-01"))
    assert out.temporal_context.temporal_role == "method_source"
    assert out.temporal_context.current_update_required is False


# ── PART 7: method source regression (Pearl / Meadows / Alaph / Xantium) ──────────
#
# TemporalContextAgent-level assertions for the four canonical research-corpus authors.
# A METHOD source (access_class="method") is temporal_role == "method_source", never needs a
# current update, and every claim is method_rule → timeless_method → method_context (the
# firewall invariant in engine/temporal.TemporalClaimStatus). A CASE source (the French-bank
# worked example, a specific Xantium trade) routes to a case role and its claims are NEVER
# method_context. SourceIntake-level (per-page) splits live in tests/unit/test_wiki_agents.py.


def _assert_timeless_method_context(claim_status):
    """The full firewall chain for a method rule: method_rule → timeless_method → method_context."""
    assert claim_status.claim_kind == "method_rule"
    assert claim_status.temporal_status == "timeless_method"
    assert claim_status.allowed_use_in_phase_a == "method_context"


# Pearl / Causal Compiler — method_source; method_rule / timeless_method / method_context.
def test_pearl_causal_method_rule_is_timeless_method_context():
    bundle = _bundle(
        "pearl-book-of-why",
        [_atom("m1", "do-calculus separates correlation from causation", kind="source_fact")],
        source_date=None,
    )
    out = _run(_cls("pearl-book-of-why", access="method", stype="book"), bundle)
    assert out.temporal_context.temporal_role == "method_source"
    assert out.temporal_context.current_update_required is False
    _assert_timeless_method_context(out.claim_statuses[0])


# Meadows / System Mapper — method_source; system concepts are timeless_method.
def test_meadows_system_concepts_are_timeless_method():
    bundle = _bundle(
        "meadows-thinking-in-systems",
        [
            _atom("m1", "stocks and flows with balancing and reinforcing feedback loops", kind="source_fact"),
            _atom("m2", "leverage points are where to intervene in a system", kind="source_fact"),
        ],
        source_date="1990-01-01",   # old, but a method source is never stale by age
    )
    out = _run(_cls("meadows-thinking-in-systems", access="method", stype="book"), bundle)
    assert out.temporal_context.temporal_role == "method_source"
    assert out.temporal_context.current_update_required is False
    for st in out.claim_statuses:
        _assert_timeless_method_context(st)


# Alaph — process pages are method_source / method_rule (the four-step process).
def test_alaph_process_page_is_method_rule():
    bundle = _bundle(
        "alaph-long-presentation-2014",
        [_atom("m1", "the four-step investment process: theme, valuation, "
                     "trade selection, portfolio construction", kind="source_fact")],
        source_date="2014-07-01",
    )
    out = _run(_cls("alaph-long-presentation-2014", access="method", stype="deck"), bundle)
    assert out.temporal_context.temporal_role == "method_source"
    _assert_timeless_method_context(out.claim_statuses[0])


# Alaph — the French-bank worked example is CASE, not method: a case temporal role whose
# claims are NEVER method_context (the firewall must not let a worked trade become method memory).
def test_alaph_french_bank_case_is_not_method_context():
    bundle = _bundle(
        "alaph-french-bank-2014",
        [_atom("c1", "we recommended the senior-vs-sovereign French bank basis position", kind="source_fact")],
        source_date="2014-07-01",
    )
    out = _run(_cls("alaph-french-bank-2014", access="case", stype="deck"), bundle)
    tc = out.temporal_context
    assert tc.temporal_role != "method_source"
    assert tc.temporal_role in ("historical_case", "stale_case", "outcome_candidate")
    st = out.claim_statuses[0]
    assert st.claim_kind != "method_rule"
    assert st.temporal_status != "timeless_method"
    assert st.allowed_use_in_phase_a != "method_context"


# Xantium — a specific, historical trade-like example is CASE; its claims are not method_context.
def test_xantium_specific_trade_case_is_not_method_context():
    bundle = _bundle(
        "xantium-trade-2013",
        [_atom("x1", "we were long the 5y CDX IG basis trade", kind="source_fact")],
        source_date="2013-06-01",
    )
    out = _run(_cls("xantium-trade-2013", access="case", stype="report"), bundle)
    tc = out.temporal_context
    assert tc.temporal_role != "method_source"
    assert tc.temporal_role in ("historical_case", "stale_case", "outcome_candidate")
    st = out.claim_statuses[0]
    assert st.claim_kind != "method_rule"
    assert st.allowed_use_in_phase_a != "method_context"


# Firewall cross-check: across all PART-7 method sources, every claim that is method_context is
# also method_rule + timeless_method, and no case claim is ever method_context.
def test_part7_firewall_only_method_rules_are_method_context():
    method_out = _run(
        _cls("pearl-book-of-why", access="method", stype="book"),
        _bundle("pearl-book-of-why", [_atom("m1", "do-calculus separates correlation from causation")],
                source_date=None),
    )
    for st in method_out.claim_statuses:
        if st.allowed_use_in_phase_a == "method_context":
            assert st.claim_kind == "method_rule" and st.temporal_status == "timeless_method"

    case_out = _run(
        _cls("alaph-french-bank-2014", access="case", stype="deck"),
        _bundle("alaph-french-bank-2014",
                [_atom("c1", "we recommended the French bank basis position")],
                source_date="2014-07-01"),
    )
    assert all(st.allowed_use_in_phase_a != "method_context" for st in case_out.claim_statuses)


# ── PART 8: recent case regression (JPM AI Capex Funding) ─────────────────────────
#
# Grounding: the real source page wiki/sources/jpm-ai-capex-funding-2026-05-11.md is a
# J.P. Morgan North America Credit Research data piece — source_type="report",
# access_class="case", source_date=2026-05-11. These tests pin TemporalContextAgent's
# behaviour against that source across two caller-supplied current_date scenarios and prove
# that FRESHNESS keys off the source's CONTENT DATE (source_date), never the file mtime /
# ingestion time. The plain factual atoms (no forecast verbs / forward horizons) keep the
# classification on the source-age path, isolating the freshness logic.
#
# Enum note (spec-vs-implementation): the spec text says "current_report or recent_case", but
# the TemporalRole Literal in engine/temporal.py has NO "recent_case" value — its members are
# {current_report, historical_case, method_source, outcome_candidate, stale_case, unknown}.
# We assert against current_report (the value that actually exists). The age field on
# TemporalContext is named `source_age_days` (confirmed), not e.g. `age_days`.

_JPM_SLUG = "jpm-ai-capex-funding-2026-05-11"
_JPM_SOURCE_DATE = "2026-05-11"   # the source's CONTENT date, from the real wiki page frontmatter


def _jpm_cls():
    """SourceClassification mirroring the real JPM report page: report + case."""
    return _cls(_JPM_SLUG, access="case", stype="report")


def _jpm_bundle(source_date=_JPM_SOURCE_DATE):
    """Plain factual atoms from the JPM AI-capex source (no forecast/horizon language)."""
    atoms = [
        _atom("jpm-2026-05-11-001", "27 issuers span over $450bn of related obligations", page=1),
        _atom("jpm-2026-05-11-013", "HPC outperformed at +9.99% vs HY +1.61%", page=9),
    ]
    return _bundle(_JPM_SLUG, atoms, source_date=source_date)


def test_jpm_classification_is_report_and_case():
    """source_type=report, access_class=case (mirrors the real page frontmatter)."""
    cls = _jpm_cls()
    assert cls.source_type == "report"
    assert cls.access_class == "case"


def test_jpm_near_current_date_is_current_report_and_not_stale():
    """current_date ≈ 2026-06-08: a recent CASE report that IS the current input is
    current_report, small source_age_days, and NOT automatically stale (no current update)."""
    out = _run(_jpm_cls(), _jpm_bundle(), current=date(2026, 6, 8), is_current_input=True)
    tc = out.temporal_context
    assert tc.temporal_role == "current_report"        # "recent_case" is not a defined enum value
    assert tc.source_age_days is not None and tc.source_age_days < 180   # small / within recent window
    assert tc.current_update_required is False          # NOT automatically stale
    assert not tc.expired_forecasts


def test_jpm_far_future_current_date_is_stale_case_needing_update():
    """current_date artificially set to 2028-01-01: the same source_date (2026-05-11) is now
    ~600 days old ⇒ a stale/historical case requiring a current update."""
    out = _run(_jpm_cls(), _jpm_bundle(), current=date(2028, 1, 1))
    tc = out.temporal_context
    # spec allows historical_case OR stale_case; 180d–2y age routes to stale_case here
    assert tc.temporal_role in ("historical_case", "stale_case")
    assert tc.temporal_role == "stale_case"
    assert tc.current_update_required is True


def test_jpm_freshness_is_driven_by_source_date_not_mtime():
    """A new upload of an OLD report must still be OLD by content date. Holding the source_date
    fixed at the JPM content date (2026-05-11), staleness depends ONLY on current_date vs that
    source_date — never on when the bundle/file was created (mtime / ingestion time)."""
    bundle = _jpm_bundle(source_date=_JPM_SOURCE_DATE)   # built 'now', but content date is fixed/old

    fresh = _run(_jpm_cls(), bundle, current=date(2026, 6, 8), is_current_input=True)
    stale = _run(_jpm_cls(), bundle, current=date(2028, 1, 1))

    # identical classification + identical bundle (same source_date) — only current_date differs.
    assert fresh.temporal_context.source_date == date(2026, 5, 11)
    assert stale.temporal_context.source_date == date(2026, 5, 11)
    assert fresh.temporal_context.current_update_required is False
    assert stale.temporal_context.current_update_required is True
    # age grows purely with current_date − source_date, proving freshness keys off content date.
    assert stale.temporal_context.source_age_days > fresh.temporal_context.source_age_days
    assert stale.temporal_context.source_age_days == (date(2028, 1, 1) - date(2026, 5, 11)).days


def test_jpm_old_report_freshly_uploaded_is_still_old():
    """Re-asserting the mtime invariant from the upload angle: even if the report is ingested
    'today' (2026-06-09, the session date), an OLD content date makes it old. Here we set the
    current_date well past the source_date and confirm it is not treated as a current report."""
    out = _run(_jpm_cls(), _jpm_bundle(source_date=_JPM_SOURCE_DATE), current=date(2028, 1, 1))
    tc = out.temporal_context
    assert tc.temporal_role != "current_report"
    assert tc.current_update_required is True
