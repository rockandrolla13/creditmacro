"""Memory Access Firewall — enforced by CONSTRUCTION, not instruction."""
from __future__ import annotations

from pathlib import Path

import pytest

from engine.case_loader import load_case
from engine.firewall import (
    FirewalledResult,
    default_calibrator,
    freeze,
    run_two_phase,
)
from engine.memory import MemoryRetriever, WikiPage, check_access_class
from engine.scripted_provider import ScriptedProvider

ROOT = Path(__file__).resolve().parents[2]
JPM = ROOT / "cases" / "discovery" / "jpm_ai_capex.yaml"

# ── in-memory wiki fixtures ───────────────────────────────────────────────────

def _method_page(slug="meadows-feedback-loops"):
    return WikiPage(slug=slug, access_class="method", type="concept",
                    frontmatter={"type": "concept"}, body="Reinforcing vs balancing loops.")

def _case_page(slug="theme-2024-ai-steepener", families=("steepener",)):
    return WikiPage(slug=slug, access_class="case", type="theme",
                    frontmatter={"type": "theme", "strategy_families": list(families)},
                    body="A 2024 AI-capex steepener theme that closed +12bp.")

def _pages():
    return {p.slug: p for p in (_method_page(), _case_page())}

def _provider():
    case = load_case(JPM)
    return ScriptedProvider(case), case.resolved_policy()

# ── 1. phase-A refuses case content (the firewall) ───────────────────────────

def test_phase_a_retrieval_of_case_slug_returns_nothing_and_logs_refusal():
    r = MemoryRetriever(_pages(), phase="A")
    got = r.retrieve("theme-2024-ai-steepener")
    assert got is None
    assert "theme-2024-ai-steepener" in r.refusals

def test_phase_a_fails_closed_on_missing_or_invalid_access_class():
    pages = {"weird": WikiPage(slug="weird", access_class=None, type="source",
                               frontmatter={}, body="x")}
    r = MemoryRetriever(pages, phase="A")
    assert r.retrieve("weird") is None          # not method ⇒ refused (fail closed)
    assert "weird" in r.refusals

# ── 4. method pages retrievable in BOTH phases ───────────────────────────────

def test_method_pages_are_retrievable_in_both_phases():
    r = MemoryRetriever(_pages(), phase="A")
    assert r.retrieve("meadows-feedback-loops") is not None
    r.advance_to_phase_b()
    assert r.retrieve("meadows-feedback-loops") is not None

def test_case_pages_become_readable_only_after_advancing_to_phase_b():
    r = MemoryRetriever(_pages(), phase="A")
    assert r.retrieve("theme-2024-ai-steepener") is None
    r.advance_to_phase_b()
    assert r.retrieve("theme-2024-ai-steepener") is not None

# ── access_class lint check ──────────────────────────────────────────────────

def test_check_access_class_flags_missing_or_invalid():
    pages = {
        "ok": WikiPage(slug="ok", access_class="method", type="concept", frontmatter={}, body=""),
        "bad": WikiPage(slug="bad", access_class="history", type="theme", frontmatter={}, body=""),
        "none": WikiPage(slug="none", access_class=None, type="source", frontmatter={}, body=""),
    }
    findings = check_access_class(pages)
    flagged = " ".join(findings)
    assert "bad" in flagged and "none" in flagged
    assert "ok" not in flagged

# ── 2/3. full run: freeze BEFORE any case read; provenance of the split ───────

def test_full_run_freezes_snapshot_with_hash_before_case_is_read():
    provider, policy = _provider()
    retriever = MemoryRetriever(_pages(), phase="A")
    result = run_two_phase(provider, policy, retriever=retriever, calibrator=default_calibrator)

    assert isinstance(result, FirewalledResult)
    # phase A ended at the locked lifecycle's routed terminal (never expression_complete)
    assert result.fresh_reasoning.theme.status == "strategy_family_routed"
    # the hash is recorded and matches the frozen content
    assert result.fresh_snapshot_hash
    assert result.fresh_snapshot_hash == result.fresh_reasoning.content_hash
    # EVERY case page was read only AFTER the snapshot was frozen
    case_reads = [r for r in retriever.reads if r["access_class"] == "case" and r["allowed"]]
    assert case_reads, "phase B should have read at least one case analogue"
    assert all(r["frozen_before_read"] for r in case_reads)

def test_calibration_is_additive_and_references_the_frozen_hash():
    provider, policy = _provider()
    retriever = MemoryRetriever(_pages(), phase="A")
    result = run_two_phase(provider, policy, retriever=retriever, calibrator=default_calibrator)

    cal = result.post_case_calibration
    assert cal is not None
    assert cal.fresh_snapshot_hash == result.fresh_snapshot_hash    # provenance link
    # the shared-family case page surfaced as an analogue
    assert any(a.slug == "theme-2024-ai-steepener" for a in cal.analogues)
    assert cal.lessons
    # adjustments copy the fresh confidence (recorded, not silently applied)
    assert all(adj.fresh_confidence == adj.adjusted_confidence for adj in cal.confidence_adjustments)

# ── immutability: phase B cannot mutate the frozen causal object ─────────────

def test_frozen_causal_object_rejects_mutation():
    provider, policy = _provider()
    result = run_two_phase(provider, policy, pages=_pages(), calibrator=default_calibrator)
    theme = result.fresh_reasoning.theme

    with pytest.raises((TypeError, ValueError)):
        theme.statement = "anchored on history"          # frozen ThemeObject
    with pytest.raises((TypeError, ValueError)):
        theme.strategy_families[0].confidence = 0.99     # frozen StrategyFamilyRec
    with pytest.raises((TypeError, ValueError)):
        result.fresh_reasoning.content_hash = "tampered"  # frozen snapshot

def test_identical_reasoning_hashes_equal_across_runs():
    # Two runs of the same case differ only in volatile id/created_at/last_updated; the
    # content hash must ignore those so identical fresh reasoning fingerprints equal.
    from engine.workflow import run_workflow
    provider, policy = _provider()
    t1, _ = run_workflow(provider, policy, mode="discovery")
    provider2, policy2 = _provider()
    t2, _ = run_workflow(provider2, policy2, mode="discovery")
    assert t1.id != t2.id                       # genuinely different objects
    assert freeze(t1).content_hash == freeze(t2).content_hash

def test_freeze_hash_changes_if_content_differs():
    provider, policy = _provider()
    from engine.workflow import run_workflow
    theme, _ = run_workflow(provider, policy, mode="discovery")
    snap = freeze(theme, now="2026-06-06T00:00:00+00:00")
    # a different statement ⇒ a different hash (the hash fingerprints the fresh reasoning)
    other = theme.model_copy(update={"statement": "different thesis"})
    snap2 = freeze(other, now="2026-06-06T00:00:00+00:00")
    assert snap.content_hash != snap2.content_hash

# ── backfilled real wiki pages all carry a valid access_class ────────────────

def test_real_wiki_pages_have_valid_access_class():
    from engine.memory import load_wiki_pages
    pages = load_wiki_pages(ROOT / "wiki")
    assert pages, "expected wiki pages to load"
    findings = check_access_class(pages)
    assert findings == [], f"wiki pages missing/invalid access_class: {findings}"


# ── coverage view: history sets the agenda, it does not supply the answer ─────
#
# The firewall keeps prior CONCLUSIONS out of fresh reasoning. It was never meant to
# keep out the knowledge that a question had already been asked -- reasoning fresh is
# not reasoning blind. These tests pin the line between the two.

from engine.memory import (  # noqa: E402
    CONCLUSION_KEYS, COVERAGE_FIELDS, CoverageEntry, CoverageStatus, MemoryRetriever, WikiPage,
)


def _cov_case_page(slug: str, **fm) -> WikiPage:
    frontmatter = {"type": "theme", "access_class": "case", "slug": slug, **fm}
    return WikiPage(slug=slug, access_class="case", type=frontmatter.get("type"),
                    frontmatter=frontmatter, body="CONCLUSION: spreads widened 40bp.")


def _cov_pages() -> dict[str, WikiPage]:
    return {
        "prior-funding": _cov_case_page(
            "prior-funding", status="closed", sources=["s1", "s2", "s3"], updated="2026-05-01",
            causal_chain=["funding stress -> spreads widen"],
            strategy_families=["long_short"], falsifiers=["differentials compress"],
        ),
        "prior-open": _cov_case_page("prior-open", status="active", sources=["s1"]),
        "how-to-reason": WikiPage(slug="how-to-reason", access_class="method", type="concept",
                                  frontmatter={"type": "concept"}, body="method content"),
    }


def test_coverage_is_readable_in_phase_a() -> None:
    """Phase A may learn WHERE prior work exists. That is agenda, not answer."""
    r = MemoryRetriever(_cov_pages(), phase="A")
    cov = r.coverage()

    assert [e.slug for e in cov] == ["prior-funding", "prior-open"]   # case pages only, sorted
    settled = cov[0]
    assert settled.status is CoverageStatus.SETTLED
    assert settled.evidence_breadth == 3          # a count, not the sources
    assert cov[1].status is CoverageStatus.OPEN


def test_coverage_entry_exposes_no_conclusion_bearing_field() -> None:
    """Structural guard: the field set is pinned.

    Adding a field that carries a conclusion -- the causal chain, the routed families,
    the falsifier -- fails HERE rather than silently widening what phase A can see.
    """
    assert set(CoverageEntry.model_fields) == COVERAGE_FIELDS
    assert not (set(CoverageEntry.model_fields) & CONCLUSION_KEYS)

    dumped = CoverageEntry(slug="x").model_dump()
    assert "body" not in dumped
    for leaky in CONCLUSION_KEYS:
        assert leaky not in dumped, f"coverage leaked {leaky!r}"


def test_coverage_does_not_open_a_back_door_to_case_bodies() -> None:
    """The load-bearing one. Coverage must not become a way to read a case page.

    If this ever fails, the firewall is gone: an agent could enumerate coverage and
    then fetch the very conclusions the freeze exists to keep out of phase A.
    """
    r = MemoryRetriever(_cov_pages(), phase="A")
    r.coverage()

    assert r.retrieve("prior-funding") is None           # still refused, still fail-closed
    assert "prior-funding" in r.refusals
    assert r.retrieve("how-to-reason") is not None       # method memory unaffected


def test_coverage_direction_of_a_settled_question_is_withheld() -> None:
    """'It was answered' is agenda. 'The answer was no' is the answer.

    A falsified prior theme reports SETTLED, exactly like a confirmed one -- phase A
    learns the ground is covered, not which way it fell.
    """
    pages = {
        "confirmed": _cov_case_page("confirmed", status="closed"),
        "falsified": _cov_case_page("falsified", status="falsified"),
    }
    by_slug = {e.slug: e.status for e in MemoryRetriever(pages, phase="A").coverage()}
    assert by_slug["confirmed"] is by_slug["falsified"] is CoverageStatus.SETTLED


def test_coverage_read_is_audited() -> None:
    """Every case-memory touch stays in the audit log, coverage included."""
    r = MemoryRetriever(_cov_pages(), phase="A")
    r.coverage()
    entry = next(x for x in r.reads if x["slug"] == "<coverage>")
    assert entry["phase"] == "A" and entry["entries"] == 2
