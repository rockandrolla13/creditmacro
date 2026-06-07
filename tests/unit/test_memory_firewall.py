"""Memory Access Firewall — enforced by CONSTRUCTION, not instruction.

The hazard: CASE memory (past themes/scenarios/closed-thesis outcomes) leaking into FRESH
causal reasoning, so the agent anchors on old conclusions. METHOD memory (concepts, causal
mechanisms, how-to-reason pages) carries no such hazard.

Mechanism:
  PHASE A — method-only retriever; case pages are REFUSED (None + logged). Build the causal
            object + route families fresh.
  FREEZE  — serialize phase-A output, record content hash + timestamp (immutable).
  PHASE B — case pages now readable, ONLY to find analogues + calibrate confidence; the
            frozen causal object must NOT be mutated (additive calibration block only).
"""
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
