"""PART 6 — MultiSourceThemeAggregatorAgent: registry wiring, contract discipline, and the
required behaviours (dedup, no-overmerge, access/temporal firewall, multi-asset generalization)
exercised through the agent entry point."""
from __future__ import annotations

from datetime import date

from engine.evidence_extraction import EvidenceExtractionBundle
from engine.schema.probability import EvidenceAtom
from engine.schema.theme_aggregation import MultiSourceThemeSet
from engine.temporal import TemporalContext
from engine.wiki_agents import (
    REGISTRY,
    MultiSourceThemeAggregatorInput,
    SourceClassification,
    run_agent,
)


def _atom(eid, slug, themes, mvars=()):
    return EvidenceAtom(evidence_id=eid, source_slug=slug, claim="c",
                        themes=list(themes), market_variables=list(mvars))


def _bundle(slug, *, themes=(), atoms=()):
    return EvidenceExtractionBundle(source_slug=slug, core_theme_candidates=list(themes),
                                    evidence_atoms=list(atoms))


def _sc(slug, access="case"):
    return SourceClassification(source_slug=slug, source_type="report", access_class=access,
                                copyright_status="c", ingestion_policy="summarize")


def _tc(slug, role="current_report"):
    return TemporalContext(source_slug=slug, current_date=date(2026, 6, 12),
                           temporal_role=role, current_update_required=False)


# ── registry wiring ──────────────────────────────────────────────────────────
def test_agent_is_registered():
    assert "MultiSourceThemeAggregatorAgent" in REGISTRY.list_agents()


def test_contract_is_well_formed_and_read_only():
    c = REGISTRY.get_agent("MultiSourceThemeAggregatorAgent").contract
    assert c.allowed_paths_to_write == []          # writes nothing
    assert "no trades" in c.non_goals
    assert not REGISTRY.validate_agent_contracts()  # all contracts complete


def test_run_agent_returns_theme_set():
    inp = MultiSourceThemeAggregatorInput(
        bundles=[_bundle("s1", themes=["Private credit risk is mispriced"],
                         atoms=[_atom("e1", "s1", themes=["private credit risk is mispriced"])])],
        source_classifications=[_sc("s1")],
        temporal_contexts=[_tc("s1")],
        current_input_slugs=["s1"],
    )
    out = run_agent("MultiSourceThemeAggregatorAgent", inp)
    assert isinstance(out, MultiSourceThemeSet)
    assert out.clusters


def test_run_agent_accepts_dict_input():
    out = run_agent("MultiSourceThemeAggregatorAgent", {
        "bundles": [{"source_slug": "s1", "core_theme_candidates": ["x theme"]}],
        "source_classifications": [{"source_slug": "s1", "source_type": "report",
                                    "access_class": "method", "copyright_status": "c",
                                    "ingestion_policy": "summarize"}],
    })
    assert isinstance(out, MultiSourceThemeSet)


# ── firewall through the agent ───────────────────────────────────────────────
def test_agent_blocks_archived_case():
    inp = MultiSourceThemeAggregatorInput(
        bundles=[_bundle("jpm-archived", themes=["AI capex funding gap"]),
                 _bundle("fresh", themes=["European credit cheapening"])],
        source_classifications=[_sc("jpm-archived"), _sc("fresh")],
        temporal_contexts=[_tc("fresh", role="current_report")],   # jpm has no current marker
    )
    out = run_agent("MultiSourceThemeAggregatorAgent", inp)
    names = " ".join(c.canonical_theme_name.lower() for c in out.clusters)
    assert "ai capex funding gap" not in names
    assert any("jpm-archived" in w for w in out.warnings)


# ── multi-asset generalization ───────────────────────────────────────────────
def test_multi_asset_generalization():
    # credit, equity, and rates themes from independent current sources → 3 distinct clusters
    bundles = [
        _bundle("credit", themes=["Private credit risk is mispriced"],
                atoms=[_atom("e1", "credit", themes=["private credit risk is mispriced"])]),
        _bundle("equity", themes=["European equities rich vs fair value"],
                atoms=[_atom("e2", "equity", themes=["european equities rich vs fair value"])]),
        _bundle("rates", themes=["Front-end rates catch up"],
                atoms=[_atom("e3", "rates", themes=["front-end rates catch up"])]),
    ]
    out = run_agent("MultiSourceThemeAggregatorAgent", MultiSourceThemeAggregatorInput(
        bundles=bundles,
        source_classifications=[_sc("credit"), _sc("equity"), _sc("rates")],
        temporal_contexts=[_tc("credit"), _tc("equity"), _tc("rates")],
        current_input_slugs=["credit", "equity", "rates"],
    ))
    assert len(out.clusters) == 3   # no spurious cross-asset merges
    assert {c.canonical_theme_name for c in out.clusters}.__len__() == 3
