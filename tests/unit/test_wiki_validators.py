"""Tests for the wiki-persistence validator foundation (PART 9, engine/wiki_validators.py).

Exercises the pure predicates and the on-disk / plan-level scans against REAL pages produced by
the WikiIntegrator (no synthetic page strings where an integrator page will do), plus a handful of
hand-built minimal page strings for the negative cases the integrator never emits (missing
frontmatter, broken links, promoted-cluster-without-source, method page with a case conclusion,
live recommendation on a historical page, verbatim copyright run).

All on-disk tests write into a pytest tmp_path wiki root; the real wiki/ is never touched.

KNOWN PART-9 BUG (flagged, not patched): `check_log_single_entry` matches a log-line shape
(``WikiIntegrator: integrated `<slug>` ``) that the Part-8 integrator never writes — the
integrator emits ``## [<date>] ingest | <slug>``. The mismatch is pinned with an xfail below so
the human can reconcile the two siblings' log-line contract.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from engine.wiki_validators import (
    ValidationFinding,
    ValidationReport,
    check_access_class_present,
    check_case_page_phase_a,
    check_forecast_expiry_labeled,
    check_frontmatter_present,
    check_historical_cases_not_current,
    check_index_links_all,
    check_log_single_entry,
    check_memory_map_updated,
    check_method_pages_no_case_conclusions,
    check_no_long_copyright,
    check_no_trade_language,
    check_promoted_clusters_have_sources,
    check_theme_pages_cite_evidence,
    check_wikilinks_resolve,
    page_has_access_class,
    page_has_frontmatter,
    page_historical_case_disclaimed,
    page_method_has_no_case_conclusions,
    page_no_long_copyright,
    page_no_trade_language,
    page_promoted_cluster_has_source,
    page_theme_cites_evidence,
    validate_all,
)

# Reuse the integrator fixtures so the validators are tested against REAL integrator output.
from tests.unit.test_wiki_integrator import (
    _bundle,
    _classification,
    _input,
    _temporal,
    integrate,
)
from engine.wiki_integration import build_wiki_update_plan


# ── report model ──────────────────────────────────────────────────────────────────

def test_report_ok_and_partitions():
    rep = ValidationReport(findings=[
        ValidationFinding(check="a", severity="error", message="e"),
        ValidationFinding(check="b", severity="warning", message="w"),
        ValidationFinding(check="c", severity="info", message="i"),
    ])
    assert rep.ok is False
    assert len(rep.errors()) == 1
    assert len(rep.warnings()) == 1
    assert len(rep.infos()) == 1
    clean = ValidationReport()
    assert clean.ok is True
    clean.extend([ValidationFinding(check="x", severity="warning", message="w")])
    assert clean.ok is True  # warnings do not fail


# ── 1. frontmatter present ─────────────────────────────────────────────────────────

def test_page_has_frontmatter_predicate():
    assert page_has_frontmatter("---\ntype: source\n---\nbody") is None
    f = page_has_frontmatter("no frontmatter here")
    assert f is not None and f.check == "frontmatter_present" and f.severity == "error"


def test_check_frontmatter_present_on_real_plan(tmp_path):
    plan = build_wiki_update_plan(_input(tmp_path))
    assert check_frontmatter_present(plan) == []  # every full page has frontmatter


# ── 2. wikilinks resolve ────────────────────────────────────────────────────────────

def test_wikilinks_resolve_on_real_wiki(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    assert check_wikilinks_resolve(inp.wiki_root) == []


def test_wikilinks_resolve_flags_dangling(tmp_path):
    root = tmp_path / "wiki"
    (root / "themes").mkdir(parents=True)
    (root / "themes" / "t.md").write_text(
        "---\ntype: theme\naccess_class: case\n---\nlink [[does-not-exist]]")
    findings = check_wikilinks_resolve(str(root))
    assert findings and findings[0].check == "wikilink_resolves"


# ── 3. theme pages cite evidence ────────────────────────────────────────────────────

def test_theme_cites_evidence_real_page(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    assert check_theme_pages_cite_evidence(inp.wiki_root) == []


def test_theme_cites_evidence_predicate_flags_empty():
    page = "---\ntype: theme\naccess_class: case\nsource_evidence: []\n---\n## Evidence\n- (none)\n"
    f = page_theme_cites_evidence(page)
    assert f is not None and f.check == "theme_cites_evidence"
    ok = "---\ntype: theme\naccess_class: case\nsource_evidence: [\"ev-1\"]\n---\nbody"
    assert page_theme_cites_evidence(ok) is None


# ── 4. promoted clusters have a source ──────────────────────────────────────────────

def test_promoted_cluster_predicate():
    promoted_no_src = ("---\ntype: theme_cluster\naccess_class: case\n"
                       "theme_status: promote_to_discovery\nsource_slugs: []\n---\nbody")
    f = page_promoted_cluster_has_source(promoted_no_src)
    assert f is not None and f.check == "promoted_cluster_has_source"
    promoted_with_src = ("---\ntype: theme_cluster\naccess_class: case\n"
                         "theme_status: promote_to_discovery\nsource_slugs: [\"s1\"]\n---\nbody")
    assert page_promoted_cluster_has_source(promoted_with_src) is None
    # a non-promoted cluster is never flagged
    watchlist = ("---\ntype: theme_cluster\naccess_class: case\n"
                 "theme_status: watchlist\nsource_slugs: []\n---\nbody")
    assert page_promoted_cluster_has_source(watchlist) is None


def test_promoted_clusters_scan_on_real_wiki(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    # default cluster is 'watchlist', not promoted -> no findings
    assert check_promoted_clusters_have_sources(inp.wiki_root) == []


# ── 5. access_class present ─────────────────────────────────────────────────────────

def test_access_class_predicate():
    assert page_has_access_class("---\naccess_class: case\n---\nb") is None
    miss = page_has_access_class("---\ntype: x\n---\nb")
    assert miss is not None and miss.severity == "error"
    bad = page_has_access_class("---\naccess_class: nonsense\n---\nb")
    assert bad is not None and bad.severity == "warning"


def test_access_class_scan_real_wiki_clean(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    assert check_access_class_present(inp.wiki_root) == []


# ── 6. case page refused in Phase A ─────────────────────────────────────────────────

def test_case_phase_a_predicate_matrix():
    case = "---\naccess_class: case\n---\nbody"
    method = "---\naccess_class: method\n---\nbody"
    # case, phase A, not current input -> refused
    assert check_case_page_phase_a(case, phase="A", is_current_input=False)
    # case, phase A, IS current input -> admitted
    assert check_case_page_phase_a(case, phase="A", is_current_input=True) == []
    # method, phase A -> always admitted
    assert check_case_page_phase_a(method, phase="A", is_current_input=False) == []
    # phase B -> everything admitted
    assert check_case_page_phase_a(case, phase="B", is_current_input=False) == []


# ── 7. method pages have no case conclusions ────────────────────────────────────────

def test_method_no_case_conclusion_predicate():
    method_bad = "---\naccess_class: method\n---\nWe recommend going long; price target $250."
    findings = page_method_has_no_case_conclusions(method_bad)
    assert findings and all(f.severity == "warning" for f in findings)
    # a case page is never scanned by this predicate
    case = "---\naccess_class: case\n---\nWe recommend going long; forecast."
    assert page_method_has_no_case_conclusions(case) == []


def test_method_pages_scan_real_method_wiki(tmp_path):
    inp = _input(
        tmp_path,
        source_classification=_classification(slug="pearl-book-of-why", access="method",
                                              stype="book"),
        bundle=_bundle(slug="pearl-book-of-why"),
        temporal_context=_temporal(slug="pearl-book-of-why", role="method_source"),
        theme_set=None,
    )
    integrate(inp)
    # The integrator's method CONCEPT/ENTITY pages (the Part-7 method-source output) carry no
    # case-conclusion tells. (The method SOURCE page legitimately has a "Forecast horizons …"
    # heading which the heuristic flags as a WARNING — see the assertion below; it never errors.)
    findings = page_method_has_no_case_conclusions(
        (Path(inp.wiki_root) / "concepts" / "spread-dispersion.md").read_text())
    assert findings == []
    findings_e = page_method_has_no_case_conclusions(
        (Path(inp.wiki_root) / "entities" / "juli.md").read_text())
    assert findings_e == []
    # whole-wiki scan only ever yields warnings (heuristic), never errors
    all_findings = check_method_pages_no_case_conclusions(inp.wiki_root)
    assert all(f.severity == "warning" for f in all_findings)


# ── 8. historical cases not current ─────────────────────────────────────────────────

def test_historical_case_predicate():
    missing_disclaimer = "---\ntemporal_role: historical_case\naccess_class: case\n---\nplain body"
    findings = page_historical_case_disclaimed(missing_disclaimer)
    assert findings and findings[0].check == "historical_case_disclaimed"
    live_reco = ("---\ntemporal_role: historical_case\naccess_class: case\n---\n"
                 "as of 2019-01-01: we recommend going long here")
    findings2 = page_historical_case_disclaimed(live_reco)
    assert any("live recommendation" in f.message for f in findings2)
    ok = ("---\ntemporal_role: historical_case\naccess_class: case\n---\n"
          "as of 2019-01-01: spreads were wide. Historical case — stated for outcome scoring.")
    assert page_historical_case_disclaimed(ok) == []
    # non-historical pages are never flagged
    assert page_historical_case_disclaimed("---\ntemporal_role: current_report\n---\nb") == []


# ── 9. forecast expiry labelled ─────────────────────────────────────────────────────

def test_forecast_expiry_predicate():
    body = "---\ntemporal_status: current\n---\nbody"
    # past horizon, marked current -> error
    assert check_forecast_expiry_labeled(
        body, horizon_end_date="2020-01-01", current_date="2026-01-01")
    # labelled expired -> ok
    assert check_forecast_expiry_labeled(
        body, horizon_end_date="2020-01-01", current_date="2026-01-01",
        temporal_status="expired") == []
    # still-live horizon -> ok regardless
    assert check_forecast_expiry_labeled(
        body, horizon_end_date="2030-01-01", current_date="2026-01-01") == []
    # no horizon date -> no check
    assert check_forecast_expiry_labeled(body, horizon_end_date=None, current_date="2026-01-01") == []


# ── 10. no long copyright ───────────────────────────────────────────────────────────

def test_no_long_copyright_predicate():
    raw = " ".join(f"word{i}" for i in range(40))
    # a page line that reproduces >= 25 contiguous words verbatim is flagged
    page = "---\ntype: x\n---\n" + " ".join(f"word{i}" for i in range(30))
    f = page_no_long_copyright(page, raw)
    assert f is not None and f.check == "no_long_copyright"
    # a short paraphrase line is fine
    assert page_no_long_copyright("---\nx: 1\n---\nshort paraphrase", raw) is None
    # raw_text None -> no check
    assert page_no_long_copyright(page, None) is None


def test_check_no_long_copyright_on_real_plan_is_clean(tmp_path):
    raw = ("The quarterly outlook described a sustained widening of investment grade spreads "
           "driven by a heavy primary calendar.")
    plan = build_wiki_update_plan(_input(tmp_path, raw_text=raw))
    assert check_no_long_copyright(plan, raw) == []


# ── 11. no trade language ───────────────────────────────────────────────────────────

def test_no_trade_language_predicate():
    f = page_no_trade_language("body says go long here")
    assert f is not None and f.check == "no_trade_language"
    assert page_no_trade_language("a paraphrased durable memory note") is None


def test_no_trade_language_real_wiki_and_plan_clean(tmp_path):
    inp = _input(tmp_path)
    res = integrate(inp)
    assert check_no_trade_language(inp.wiki_root) == []
    assert check_no_trade_language(res.plan) == []


# ── 12. index links all ─────────────────────────────────────────────────────────────

def test_index_links_all_real_wiki(tmp_path):
    inp = _input(tmp_path)
    res = integrate(inp)
    assert check_index_links_all(inp.wiki_root, res) == []


def test_index_links_all_flags_missing(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    findings = check_index_links_all(inp.wiki_root, ["totally-unlinked-slug"])
    assert findings and findings[0].check == "index_links_all"


def test_index_links_all_missing_index_file(tmp_path):
    (tmp_path / "wiki").mkdir()
    findings = check_index_links_all(str(tmp_path / "wiki"), ["x"])
    assert findings and "does not exist" in findings[0].message


# ── 13. log single entry (KNOWN Part-9/Part-8 format mismatch) ──────────────────────

@pytest.mark.xfail(
    reason="PART-9 BUG: check_log_single_entry matches 'WikiIntegrator: integrated `<slug>`' but "
           "the PART-8 integrator writes '## [<date>] ingest | <slug>'. The two siblings disagree "
           "on the log-line contract; the validator therefore reports a false 'no entry' error "
           "against real integrator output. Flagged for the human to reconcile (do not patch "
           "production from a test).",
    strict=True,
)
def test_log_single_entry_matches_real_integrator_log(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    # EXPECTED (correct) behavior: exactly one ingest entry for the source -> no findings.
    assert check_log_single_entry(inp.wiki_root, "acme-credit-report-2026-05-01") == []


def test_log_single_entry_missing_file(tmp_path):
    (tmp_path / "wiki").mkdir()
    findings = check_log_single_entry(str(tmp_path / "wiki"), "s")
    assert findings and "does not exist" in findings[0].message


def test_log_single_entry_counts_matching_format(tmp_path):
    """The validator's counting logic IS correct against its OWN expected line shape
    (``WikiIntegrator: integrated `<slug>` ``): one match -> ok, two -> idempotency error. This
    isolates the bug to the FORMAT mismatch with Part-8, not the counting."""
    log = tmp_path / "log.md"
    log.write_text("WikiIntegrator: integrated `s` ...\n")
    assert check_log_single_entry(str(tmp_path), "s") == []
    log.write_text("WikiIntegrator: integrated `s`\nWikiIntegrator: integrated `s`\n")
    findings = check_log_single_entry(str(tmp_path), "s")
    assert findings and "expected exactly 1" in findings[0].message


# ── 14. memory-map updated ──────────────────────────────────────────────────────────

def test_memory_map_updated_real_wiki(tmp_path):
    inp = _input(tmp_path)
    integrate(inp)
    assert check_memory_map_updated(inp.wiki_root, "acme-credit-report-2026-05-01") == []


def test_memory_map_updated_missing_file(tmp_path):
    (tmp_path / "wiki").mkdir()
    findings = check_memory_map_updated(str(tmp_path / "wiki"), "s")
    assert findings and "does not exist" in findings[0].message


def test_memory_map_updated_unreferenced_source(tmp_path):
    root = tmp_path / "wiki"
    root.mkdir()
    (root / "memory-map.md").write_text("# Memory map\n(nothing here)\n")
    findings = check_memory_map_updated(str(root), "some-source")
    assert findings and findings[0].severity == "error"


# ── top-level aggregator over a real integration ────────────────────────────────────

def test_validate_all_plan_and_disk_clean(tmp_path):
    """Aggregate pass that AVOIDS source_slug (which would trigger the buggy log check). Plan-level
    + on-disk checks over a real integration must be clean."""
    inp = _input(tmp_path)
    res = integrate(inp)
    report = validate_all(wiki_root=inp.wiki_root, plan_or_result=res, raw_text=None)
    assert report.ok, [f.message for f in report.errors()]
