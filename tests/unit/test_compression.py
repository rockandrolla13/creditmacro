"""ThemeCompressionAgent — the ten acceptance tests from
docs/THEME_DISCIPLINE_AND_FAILURE_MODES.md, plus the synthesis-integrity checks that keep the
LLM seam honest.

The input here is a hand-built `MultiSourceThemeSet` rather than a real aggregator run: this
stage consumes the aggregator's OUTPUT CONTRACT, so the tests are written against that
contract and stay green through a rewrite of the clustering behind it.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from engine.compression import (
    CompressionPolicy,
    DeterministicThemeSynthesizer,
    ParentThemeProposal,
    ScriptedThemeSynthesizer,
    ThemeCompressionAgent,
    ThemeSynthesizer,
    compress_theme_set,
    evaluate_gate,
)
from engine.schema.compression import (
    PROMOTION_REQUIREMENTS,
    AnalystThemeMap,
    CausalMechanism,
    ParentTheme,
    ThemeFalsifier,
)
from engine.schema.theme_aggregation import (
    EvidenceBullet,
    MultiSourceThemeSet,
    SourceAttribution,
    ThemeCluster,
    ThemeClusterMember,
)
from engine.wiki_integration import _trade_hit

REPO_ROOT = Path(__file__).resolve().parents[2]


# ── builders ─────────────────────────────────────────────────────────────────
def _attr(slug, ev=("e1",), contrib="supports", current=True, stype="report", group=None):
    return SourceAttribution(
        source_slug=slug, source_type=stype, access_class="case", is_current_input=current,
        evidence_ids=list(ev), contribution_type=contrib, independence_group=group,
        temporal_role="current_report" if current else "historical_case",
    )


def _bullets(ev, kind="source_fact"):
    return [EvidenceBullet(text=f"[{kind} | p1 | {e}] claim {e}", evidence_ids=[e])
            for e in ev]


def _cluster(
    cid,
    name,
    *,
    driver="growth recovery",
    outcome="rates reprice",
    extra_claims=(),
    axes=("us 5s30s slope",),
    falsifiers=("us 5s30s slope above 120bp",),
    families=("steepener",),
    attrs=None,
    evidence=("e1",),
    status="promote_to_discovery",
    promotion=0.6,
    temporal_quality=1.0,
    attention=0.1,
    claim_kind="source_fact",
    contradictions=0,
    independent=2,
    confounders=(),
    missing=(),
):
    attrs = attrs if attrs is not None else [_attr("src-a", evidence),
                                             _attr("src-b", evidence, group="grp-b")]
    # An empty driver means "this cluster has no causal chain at all".
    claims = ([f"{driver} → {outcome}"] if driver else []) + list(extra_claims)
    return ThemeCluster(
        cluster_id=cid,
        canonical_theme_name=name,
        canonical_thesis=f"{name} — thesis",
        theme_status=status,
        members=[ThemeClusterMember(source_slug=a.source_slug, original_theme_name=name,
                                    evidence_ids=list(a.evidence_ids))
                 for a in attrs],
        source_attributions=attrs,
        evidence_ids=list(evidence),
        evidence_bullets=_bullets(evidence, claim_kind),
        source_count=len(attrs),
        independent_source_count=independent,
        evidence_count=len(evidence),
        contradiction_count=contradictions,
        attention_score=attention,
        corroboration_score=0.7,
        temporal_quality=temporal_quality,
        promotion_score=promotion,
        operational_axes=list(axes),
        causal_claims=claims,
        confounders=list(confounders),
        falsifiers=list(falsifiers),
        strategy_family_hints=list(families),
        missing_data=list(missing),
    )


def _set(*clusters, slugs=("src-a", "src-b")):
    return MultiSourceThemeSet(batch_id="batch-test", source_scope="explicit_current_batch",
                               source_slugs=list(slugs), clusters=list(clusters))


def _good(cid, driver, name=None, **kw):
    """A cluster that clears every screening rule."""
    return _cluster(cid, name or f"{driver} theme", driver=driver, **kw)


# ═══════════════════════════════════════════════════════════════════════════
# Acceptance test 1 — parent-theme cap honored, nothing dropped silently
# ═══════════════════════════════════════════════════════════════════════════
_TEN_DRIVERS = ("alpha inflow", "bravo outflow", "charlie supply", "delta demand",
                "echo issuance", "foxtrot refinancing", "golf leverage", "hotel dispersion",
                "india defaults", "juliett downgrades")


def test_1_parent_cap_honored_and_tail_logged():
    clusters = [
        _good(f"tc-{i:03d}", d, axes=(f"{d} spread",), falsifiers=(f"{d} spread above {100+i}bp",),
              promotion=0.9 - i * 0.01)
        for i, d in enumerate(_TEN_DRIVERS)
    ]
    out = compress_theme_set(_set(*clusters))

    assert len(out.parent_themes) == 7
    assert out.stats.clusters_in == 10
    capped = [d for d in out.hot_topics_not_promoted
              if d.reason_code == "parent_cap_exceeded"]
    assert len(capped) == 3
    assert all(d.reason for d in capped)
    # nothing dropped: every input cluster is either inside a parent or on a demotion list
    accounted = {cid for p in out.parent_themes for cid in p.member_cluster_ids}
    accounted |= {d.cluster_id for d in out.hot_topics_not_promoted}
    accounted |= {d.cluster_id for d in out.rejected_or_merged_themes}
    accounted |= {d.cluster_id for d in out.outcome_candidates}
    assert accounted == {c.cluster_id for c in clusters}
    assert any("parent_cap" in w for w in out.warnings)


def test_1b_cap_is_configurable():
    clusters = [_good(f"tc-{i:03d}", d, axes=(f"{d} spread",),
                      falsifiers=(f"{d} spread above {100+i}bp",))
                for i, d in enumerate(_TEN_DRIVERS[:5])]
    out = compress_theme_set(_set(*clusters), policy=CompressionPolicy(parent_cap=3))
    assert len(out.parent_themes) == 3
    assert out.parent_cap == 3


# ═══════════════════════════════════════════════════════════════════════════
# Acceptance test 2 — the full promotion gate
# ═══════════════════════════════════════════════════════════════════════════
def test_2_promoted_parents_carry_all_seven_requirements():
    out = compress_theme_set(_set(_good("tc-001", "growth recovery")))
    assert len(out.parent_themes) == 1
    p = out.parent_themes[0]
    assert p.evidence_ids and p.evidence_by_source                 # evidence
    assert p.mechanism.driver and p.mechanism.transmission and p.mechanism.outcome  # mechanism
    assert p.operational_axis or p.watchlist_tag                   # axis or watchlist
    assert p.falsifier.observable and p.falsifier.threshold        # falsifier
    assert p.temporal_status == "current"                          # temporal status
    assert 1 <= len(p.strategy_families) <= 2                      # routable family
    assert p.selection_rationale.strip()                           # selection rationale
    assert set(PROMOTION_REQUIREMENTS) == {
        "evidence", "mechanism", "axis_or_watchlist", "falsifier", "temporal_status",
        "routable_family", "selection_rationale"}


def _parent_kwargs(**over):
    base = dict(
        parent_id="pt-001", name="growth recovery mispriced",
        mechanism=CausalMechanism(driver="growth", transmission="term premium", outcome="curve"),
        evidence_by_source=(),
        evidence_ids=("e1",),
        operational_axis="us 5s30s slope",
        temporal_status="current",
        strategy_families=("steepener",),
        why_it_matters="matters", why_it_might_be_wrong="might be wrong",
        falsifier=ThemeFalsifier(observable="us 5s30s slope", threshold="120bp"),
        selection_rationale="because",
    )
    base["evidence_by_source"] = (
        __import__("engine.schema.compression", fromlist=["EvidenceBySource"])
        .EvidenceBySource(source_slug="src-a", evidence_ids=("e1",)),
    )
    base.update(over)
    return base


@pytest.mark.parametrize("missing,override", [
    ("evidence", {"evidence_ids": (), "evidence_by_source": ()}),
    ("axis_or_watchlist", {"operational_axis": None, "watchlist_tag": None}),
    ("routable_family", {"strategy_families": ()}),
    ("routable_family", {"strategy_families": ("curve",)}),      # wiki-only, not routable
    ("selection_rationale", {"selection_rationale": "  "}),
])
def test_2b_parent_theme_cannot_be_built_missing_a_requirement(missing, override):
    with pytest.raises(ValueError) as exc:
        ParentTheme(**_parent_kwargs(**override))
    assert "promotion gate" in str(exc.value)


def test_2c_falsifier_without_a_threshold_level_is_rejected():
    with pytest.raises(ValueError, match="no number"):
        ThemeFalsifier(observable="spreads", threshold="materially wider")


def test_2d_mechanism_needs_all_three_parts():
    with pytest.raises(ValueError, match="transmission"):
        CausalMechanism(driver="growth", transmission="", outcome="curve")


# ═══════════════════════════════════════════════════════════════════════════
# Acceptance test 3 — merge rule and keep-separate rule
# ═══════════════════════════════════════════════════════════════════════════
def test_3_identical_driver_mechanism_outcome_axis_family_merge_into_one_parent():
    a = _good("tc-001", "growth recovery", name="rates not pricing growth", promotion=0.8)
    b = _good("tc-002", "growth recovery", name="growth repricing lag", promotion=0.5)
    out = compress_theme_set(_set(a, b))

    assert len(out.parent_themes) == 1
    p = out.parent_themes[0]
    assert p.merged_cluster_ids == ("tc-002",)
    assert p.subthemes == ()
    merged = [d for d in out.rejected_or_merged_themes if d.cluster_id == "tc-002"]
    assert len(merged) == 1
    assert merged[0].reason_code == "merged_into_parent"
    assert merged[0].merged_into == "pt-001"
    assert "shares driver" in merged[0].reason


def test_3b_same_driver_different_outcome_becomes_a_subtheme_not_a_merge_nor_a_parent():
    a = _good("tc-001", "growth recovery", name="rates not pricing growth", promotion=0.8)
    b = _good("tc-002", "growth recovery", name="credit not pricing growth",
              outcome="credit spreads compress", promotion=0.5,
              axes=("ig cdx 5y spread",), falsifiers=("ig cdx 5y spread above 80bp",))
    out = compress_theme_set(_set(a, b))

    assert len(out.parent_themes) == 1, "same driver ⇒ one parent, not two"
    p = out.parent_themes[0]
    assert p.merged_cluster_ids == (), "different outcome ⇒ not merged"
    assert [s.source_cluster_id for s in p.subthemes] == ["tc-002"]
    assert p.subthemes[0].keep_separate_reason in (
        "different_outcome", "different_mechanism", "different_axis")


def test_3c_different_drivers_stay_separate_parents():
    a = _good("tc-001", "growth recovery")
    b = _good("tc-002", "issuance supply", axes=("ig new issue concession",),
              falsifiers=("ig new issue concession above 15bp",))
    out = compress_theme_set(_set(a, b))
    assert len(out.parent_themes) == 2


def test_3d_same_driver_but_historical_is_kept_out_of_the_current_parent():
    a = _good("tc-001", "growth recovery", promotion=0.8)
    b = _good("tc-002", "growth recovery", status="historical_case", temporal_quality=0.0,
              attrs=[_attr("src-a", ("e9",), contrib="historical_analogue", current=False)],
              evidence=("e9",), promotion=0.4)
    out = compress_theme_set(_set(a, b))
    assert [d.cluster_id for d in out.outcome_candidates] == ["tc-002"]
    assert out.parent_themes[0].member_cluster_ids == ("tc-001",)


# ═══════════════════════════════════════════════════════════════════════════
# Acceptance test 4 — downgrade rules force watchlist regardless of attention
# ═══════════════════════════════════════════════════════════════════════════
@pytest.mark.parametrize("code,kw", [
    ("attention_without_evidence", dict(evidence=(),
                                        attrs=[_attr("src-a", (), contrib="mentions_only")])),
    ("no_operational_axis", dict(axes=())),
    ("no_causal_chain", dict(driver="", outcome="")),
    ("no_falsifier", dict(falsifiers=())),
    ("no_falsifier", dict(falsifiers=("spreads widen a lot",))),   # no threshold level
    ("only_source_opinion", dict(claim_kind="source_opinion")),
    ("no_routable_family", dict(families=("watchlist_only",))),
])
def test_4_downgrade_rules_force_watchlist(code, kw):
    hot = _cluster("tc-001", "everyone is talking about ai capex", attention=1.0,
                   status="watchlist", **kw)
    out = compress_theme_set(_set(hot))

    assert out.parent_themes == (), "an attention-only theme must not be promoted"
    demoted = out.hot_topics_not_promoted
    assert [d.reason_code for d in demoted] == [code]
    assert demoted[0].reason.strip()
    assert demoted[0].attention_score == 1.0


def test_4b_attention_alone_never_beats_a_lower_attention_evidenced_theme():
    hot = _cluster("tc-001", "ai capex mania", driver="ai capex", attention=1.0, axes=(),
                   status="watchlist", promotion=0.95)
    solid = _good("tc-002", "growth recovery", attention=0.05, promotion=0.10)
    out = compress_theme_set(_set(hot, solid))
    assert [p.member_cluster_ids for p in out.parent_themes] == [("tc-002",)]
    assert [d.cluster_id for d in out.hot_topics_not_promoted] == ["tc-001"]


def test_4c_upstream_reject_is_recorded_not_dropped():
    rejected = _cluster("tc-001", "chatter only", status="reject", evidence=(),
                        attrs=[_attr("src-a", (), contrib="mentions_only")])
    out = compress_theme_set(_set(rejected))
    assert [d.reason_code for d in out.rejected_or_merged_themes] == ["rejected_upstream"]


# ═══════════════════════════════════════════════════════════════════════════
# Acceptance test 5 — subtheme preservation + coverage matrix
# ═══════════════════════════════════════════════════════════════════════════
def test_5_subtheme_axes_survive_under_the_parent():
    a = _good("tc-001", "growth recovery", promotion=0.8)
    b = _good("tc-002", "growth recovery", outcome="credit spreads compress", promotion=0.5,
              axes=("ig cdx 5y spread", "hy cdx 5y spread"),
              falsifiers=("ig cdx 5y spread above 80bp",))
    p = compress_theme_set(_set(a, b)).parent_themes[0]

    sub = p.subthemes[0]
    assert sub.operational_axes == ("hy cdx 5y spread", "ig cdx 5y spread")
    assert sub.evidence_ids == ("e1",)
    assert sub.causal_claims


def test_5b_coverage_matrix_has_a_row_per_parent_with_per_source_cells():
    a = _good("tc-001", "growth recovery", attrs=[_attr("src-a", ("e1", "e2")),
                                                  _attr("src-b", ("e3",), group="grp-b")],
              evidence=("e1", "e2", "e3"))
    b = _good("tc-002", "issuance supply", attrs=[_attr("src-a", ("e4",))],
              evidence=("e4",), axes=("ig new issue concession",),
              falsifiers=("ig new issue concession above 15bp",))
    out = compress_theme_set(_set(a, b, slugs=("src-a", "src-b", "src-c")))

    matrix = out.source_coverage_matrix
    assert matrix.source_slugs == ("src-a", "src-b", "src-c")
    parent_rows = [r for r in matrix.rows if r.status == "promote"]
    assert len(parent_rows) == len(out.parent_themes) == 2
    for row in parent_rows:
        assert [c.source_slug for c in row.cells] == ["src-a", "src-b", "src-c"]
        assert not [c for c in row.cells if c.source_slug == "src-c"][0].present
    first = [r for r in parent_rows if r.theme_id == "pt-001"][0]
    assert first.evidence_count == 3
    assert first.independent_sources == 2


def test_5c_coverage_matrix_carries_a_contradiction_column():
    c = _good("tc-001", "growth recovery", contradictions=1,
              attrs=[_attr("src-a", ("e1",)),
                     _attr("src-b", ("e2",), contrib="contradicts", group="grp-b")],
              evidence=("e1", "e2"))
    row = compress_theme_set(_set(c)).source_coverage_matrix.rows[0]
    assert row.contradictions == 1
    assert "src-b" in row.contradiction_note


# ═══════════════════════════════════════════════════════════════════════════
# Acceptance test 6 — "why not" populated
# ═══════════════════════════════════════════════════════════════════════════
def test_6_why_not_lists_are_populated_with_a_reason_per_entry():
    promoted = _good("tc-001", "growth recovery", promotion=0.9)
    merged = _good("tc-002", "growth recovery", name="growth repricing lag", promotion=0.5)
    no_axis = _cluster("tc-003", "ai capex chatter", driver="ai capex", axes=(),
                       status="watchlist", attention=0.9)
    out = compress_theme_set(_set(promoted, merged, no_axis))

    assert out.rejected_or_merged_themes and out.hot_topics_not_promoted
    for d in out.rejected_or_merged_themes + out.hot_topics_not_promoted:
        assert d.reason.strip(), f"{d.cluster_id} demoted without a reason"
        assert d.reason_code
    assert out.stats.merged_count == 1
    assert out.stats.demoted_to_watchlist_count == 1


def test_6b_readout_names_every_demotion():
    promoted = _good("tc-001", "growth recovery")
    no_axis = _cluster("tc-002", "ai capex chatter", driver="ai capex", axes=(),
                       status="watchlist")
    out = compress_theme_set(_set(promoted, no_axis))
    readout = out.human_readout
    assert "### Parent themes" in readout
    assert "### Downgraded to hot-topic / watchlist (with reason)" in readout
    assert "### Merged / rejected" in readout
    assert "### Why these themes, and why not the others" in readout
    assert "no_operational_axis" in readout
    assert "Nothing was dropped silently." in readout


# ═══════════════════════════════════════════════════════════════════════════
# Acceptance test 7 — historical discipline
# ═══════════════════════════════════════════════════════════════════════════
@pytest.mark.parametrize("status", ["historical_case", "outcome_candidate"])
def test_7_historical_only_theme_is_an_outcome_candidate_never_promoted(status):
    hist = _good("tc-001", "growth recovery", status=status, temporal_quality=0.0,
                 attrs=[_attr("src-a", ("e1",), contrib="historical_analogue", current=False)])
    out = compress_theme_set(_set(hist))

    assert out.parent_themes == ()
    assert [d.destination for d in out.outcome_candidates] == ["outcome_candidate"]
    assert out.outcome_candidates[0].reason_code == "historical_forecast_without_outcome_check"
    assert out.stats.outcome_candidate_count == 1


def test_7b_parent_theme_model_refuses_a_historical_temporal_status():
    with pytest.raises(ValueError, match="outcome candidate"):
        ParentTheme(**_parent_kwargs(temporal_status="historical_outcome_candidate"))


# ═══════════════════════════════════════════════════════════════════════════
# Acceptance test 8 — no trades / no sizing anywhere
# ═══════════════════════════════════════════════════════════════════════════
def test_8_ingested_execution_language_is_redacted_from_map_and_readout():
    dirty = _good("tc-001", "growth recovery",
                  name="go long european bank credit on growth recovery",
                  axes=("us 5s30s slope",),
                  missing=("position size for the book is unknown",))
    out = compress_theme_set(_set(dirty))

    blob = out.model_dump_json()
    assert _trade_hit(blob) is None
    assert _trade_hit(out.human_readout) is None
    assert "redacted" in out.parent_themes[0].name


def test_8b_a_synthesizer_that_emits_trade_language_is_rejected_not_scrubbed():
    proposal = ParentThemeProposal(
        name="growth recovery mispriced", driver="growth", transmission="term premium",
        outcome="curve steepens", why_it_matters="matters",
        why_it_might_be_wrong="size the position at 20mm and use a hedge ratio of 1.4",
        selection_rationale="because", falsifier_observable="us 5s30s slope",
        falsifier_threshold="120bp", strategy_families=("steepener",),
        cited_evidence_ids=("e1",), operational_axis="us 5s30s slope")
    agent = ThemeCompressionAgent(
        synthesizer=ScriptedThemeSynthesizer({"tc-001": proposal}))
    out = agent.compress(_set(_good("tc-001", "growth recovery")))

    assert out.parent_themes == ()
    assert [d.reason_code for d in out.rejected_or_merged_themes] == ["trade_language"]
    assert _trade_hit(out.model_dump_json()) is None


def test_8c_a_theme_name_that_leaks_a_direction_is_rejected():
    proposal = ParentThemeProposal(
        name="long the 5s30s steepener", driver="growth", transmission="term premium",
        outcome="curve steepens", why_it_matters="matters",
        why_it_might_be_wrong="might be wrong", selection_rationale="because",
        falsifier_observable="us 5s30s slope", falsifier_threshold="120bp",
        strategy_families=("steepener",), cited_evidence_ids=("e1",),
        operational_axis="us 5s30s slope")
    out = ThemeCompressionAgent(
        synthesizer=ScriptedThemeSynthesizer({"tc-001": proposal})
    ).compress(_set(_good("tc-001", "growth recovery")))

    assert out.parent_themes == ()
    assert [d.reason_code for d in out.rejected_or_merged_themes] == ["direction_leak"]


def test_8d_no_trade_confirmation_is_carried():
    out = compress_theme_set(_set(_good("tc-001", "growth recovery")))
    assert "No trades" in out.no_trade_confirmation
    assert "## No-trade boundary" in out.human_readout


# ═══════════════════════════════════════════════════════════════════════════
# Acceptance test 9 — determinism
# ═══════════════════════════════════════════════════════════════════════════
def _mixed_batch():
    return _set(
        _good("tc-001", "growth recovery", promotion=0.8),
        _good("tc-002", "growth recovery", name="growth repricing lag", promotion=0.5),
        _good("tc-003", "issuance supply", axes=("ig new issue concession",),
              falsifiers=("ig new issue concession above 15bp",), promotion=0.7),
        _cluster("tc-004", "ai capex chatter", driver="ai capex", axes=(), status="watchlist"),
        _good("tc-005", "bank funding", status="historical_case", temporal_quality=0.0,
              attrs=[_attr("src-a", ("e7",), contrib="historical_analogue", current=False)],
              evidence=("e7",)),
    )


def test_9_same_input_gives_a_byte_identical_map():
    a = compress_theme_set(_mixed_batch())
    b = compress_theme_set(_mixed_batch())
    assert a.model_dump_json() == b.model_dump_json()


def test_9b_cluster_order_does_not_change_the_result():
    base = _mixed_batch()
    shuffled = MultiSourceThemeSet(
        batch_id=base.batch_id, source_scope=base.source_scope,
        source_slugs=base.source_slugs, clusters=list(reversed(base.clusters)))
    assert (compress_theme_set(base).model_dump_json()
            == compress_theme_set(shuffled).model_dump_json())


def test_9c_no_wall_clock_in_the_readout():
    out = compress_theme_set(_mixed_batch())
    assert "date not supplied" in out.human_readout
    dated = compress_theme_set(_mixed_batch(), policy=CompressionPolicy(as_of="2026-06-13"))
    assert "2026-06-13" in dated.human_readout


# ═══════════════════════════════════════════════════════════════════════════
# Acceptance test 10 — golden master numerics unchanged
# ═══════════════════════════════════════════════════════════════════════════
def test_10_golden_master_still_passes_with_the_compression_stage_present():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/integration/test_golden_master.py"],
        cwd=REPO_ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout[-3000:]


def test_10b_compression_is_not_wired_into_the_scripted_expression_path():
    """Compression belongs to DISCOVERY. Nothing on the scripted/expression path may import
    it, which is what keeps the golden master numerics untouched."""
    importers = [
        path.name
        for path in sorted((REPO_ROOT / "engine").rglob("*.py"))
        if path.name != "compression.py"
        and "compression" in path.read_text()
        and ("import compression" in path.read_text()
             or "from .compression" in path.read_text()
             or "engine.compression" in path.read_text())
    ]
    assert importers == [], f"compression leaked into {importers}"


# ═══════════════════════════════════════════════════════════════════════════
# The LLM seam: swappable, and never trusted
# ═══════════════════════════════════════════════════════════════════════════
def test_seam_default_synthesizer_satisfies_the_protocol():
    assert isinstance(DeterministicThemeSynthesizer(), ThemeSynthesizer)
    assert isinstance(ScriptedThemeSynthesizer({}), ThemeSynthesizer)


def test_seam_is_the_only_generative_step_and_sees_a_scoped_request():
    scripted = ScriptedThemeSynthesizer({}, fallback=DeterministicThemeSynthesizer())
    ThemeCompressionAgent(synthesizer=scripted).compress(
        _set(_good("tc-001", "growth recovery", evidence=("e1", "e2"))))

    assert len(scripted.requests) == 1
    req = scripted.requests[0]
    assert req.allowed_evidence_ids == ("e1", "e2")
    assert req.allowed_families == ("steepener",)
    assert req.max_families == 2
    assert "no direction, no instrument" in req.instruction()
    assert req.clusters[0].cluster_id == "tc-001"


def test_seam_invented_theme_with_no_real_evidence_is_rejected_by_the_gate():
    """A theme the model makes up — citing evidence ids that exist nowhere in its clusters —
    must not be promoted."""
    invented = ParentThemeProposal(
        name="secret alpha regime shift", driver="a thing", transmission="another thing",
        outcome="a third thing", why_it_matters="trust me",
        why_it_might_be_wrong="it might not be", selection_rationale="intuition",
        falsifier_observable="some spread", falsifier_threshold="100bp",
        strategy_families=("steepener",), cited_evidence_ids=("e-does-not-exist",),
        operational_axis="some spread")
    out = ThemeCompressionAgent(
        synthesizer=ScriptedThemeSynthesizer({"tc-001": invented})
    ).compress(_set(_good("tc-001", "growth recovery")))

    assert out.parent_themes == ()
    demoted = out.rejected_or_merged_themes
    assert [d.reason_code for d in demoted] == ["ungrounded_synthesis"]
    assert "e-does-not-exist" in demoted[0].reason


def test_seam_proposal_citing_no_evidence_at_all_is_rejected():
    bare = ParentThemeProposal(
        name="a vibe", driver="d", transmission="t", outcome="o", why_it_matters="w",
        why_it_might_be_wrong="x", selection_rationale="r",
        falsifier_observable="obs", falsifier_threshold="10bp",
        strategy_families=("steepener",), cited_evidence_ids=(), operational_axis="obs")
    out = ThemeCompressionAgent(
        synthesizer=ScriptedThemeSynthesizer({"tc-001": bare})
    ).compress(_set(_good("tc-001", "growth recovery")))
    assert [d.reason_code for d in out.rejected_or_merged_themes] == ["ungrounded_synthesis"]


def test_seam_declining_to_name_a_group_demotes_it_with_a_reason():
    out = ThemeCompressionAgent(
        synthesizer=ScriptedThemeSynthesizer({})       # no fallback ⇒ returns None
    ).compress(_set(_good("tc-001", "growth recovery")))
    assert out.parent_themes == ()
    assert [d.reason_code for d in out.rejected_or_merged_themes] == ["malformed_synthesis"]


def test_seam_gate_reports_instead_of_raising():
    scripted = ScriptedThemeSynthesizer({}, fallback=DeterministicThemeSynthesizer())
    ThemeCompressionAgent(synthesizer=scripted).compress(
        _set(_good("tc-001", "growth recovery")))
    req = scripted.requests[0]
    passed, code, reason = evaluate_gate(None, req)
    assert (passed, code) == (False, "malformed_synthesis")
    assert reason


def test_seam_more_than_two_families_is_rejected():
    greedy = ParentThemeProposal(
        name="growth recovery mispriced", driver="d", transmission="t", outcome="o",
        why_it_matters="w", why_it_might_be_wrong="x", selection_rationale="r",
        falsifier_observable="obs", falsifier_threshold="10bp",
        strategy_families=("steepener", "flattener", "outright"),
        cited_evidence_ids=("e1",), operational_axis="obs")
    out = ThemeCompressionAgent(
        synthesizer=ScriptedThemeSynthesizer({"tc-001": greedy})
    ).compress(_set(_good("tc-001", "growth recovery")))
    assert [d.reason_code for d in out.rejected_or_merged_themes] == ["malformed_synthesis"]


# ═══════════════════════════════════════════════════════════════════════════
# Shape + housekeeping
# ═══════════════════════════════════════════════════════════════════════════
def test_map_is_frozen_and_json_round_trips():
    out = compress_theme_set(_mixed_batch())
    with pytest.raises(Exception):
        out.batch_id = "nope"                      # frozen
    again = AnalystThemeMap.model_validate(json.loads(out.model_dump_json()))
    assert again.model_dump_json() == out.model_dump_json()


def test_map_refuses_more_parents_than_the_cap():
    with pytest.raises(ValueError, match="over a cap"):
        AnalystThemeMap(batch_id="b", parent_cap=1,
                        parent_themes=(ParentTheme(**_parent_kwargs()),
                                       ParentTheme(**_parent_kwargs(parent_id="pt-002"))))


def test_below_the_floor_warns_rather_than_inventing_themes():
    out = compress_theme_set(_set(_good("tc-001", "growth recovery")))
    assert len(out.parent_themes) == 1
    assert any("no theme was invented" in w for w in out.warnings)


@pytest.mark.parametrize("text,expected", [
    # a bare digit glued to a word is part of an AXIS NAME, not a level
    ("us 5s30s slope above 120bp", ("us 5s30s slope", "above 120bp")),
    ("ig new issue concession above 15bp", ("ig new issue concession", "above 15bp")),
    ("unemployment rate reaches 5.2", ("unemployment rate", "reaches 5.2")),
    ("us 5s30s slope widens", ("", "")),
])
def test_falsifier_parse_keeps_the_relation_with_the_level(text, expected):
    from engine.compression import _falsifier_parts
    assert _falsifier_parts((text,)) == expected


def test_runs_on_a_real_aggregator_output():
    """The contract really connects: aggregator out → compression in. Deliberately makes no
    claim about the aggregator's clustering (that is its own module's tests) — only that
    every cluster it emits is accounted for here."""
    from engine.evidence_extraction import (
        EvidenceExtractionBundle,
        OperationalAxisCandidate,
        StrategyFamilyHint,
    )
    from engine.schema.probability import EvidenceAtom
    from engine.theme_aggregation import aggregate_theme_candidates
    from engine.wiki_agents import SourceClassification

    bundle = EvidenceExtractionBundle(
        source_slug="src-a",
        core_theme_candidates=["rates not pricing growth"],
        hot_topics=["ai capex chatter"],
        evidence_atoms=[EvidenceAtom(evidence_id="e1", source_slug="src-a",
                                     claim="term premium is compressed",
                                     themes=["rates not pricing growth"])],
        operational_axes=[OperationalAxisCandidate(
            axis_name="us 5s30s slope", axis_shape="curve",
            observable_series="ust 5s30s", source_evidence_ids=["e1"])],
        strategy_family_hints=[StrategyFamilyHint(family="steepener", rationale="curve shape",
                                                  confidence=0.7,
                                                  source_evidence_ids=["e1"])],
        falsifiers=["us 5s30s slope above 120bp"],
    )
    theme_set = aggregate_theme_candidates(
        [bundle],
        [SourceClassification(source_slug="src-a", source_type="report", access_class="case",
                              copyright_status="unknown", ingestion_policy="paraphrase")],
    )
    out = compress_theme_set(theme_set)

    accounted = {cid for p in out.parent_themes for cid in p.member_cluster_ids}
    accounted |= {d.cluster_id for d in out.hot_topics_not_promoted}
    accounted |= {d.cluster_id for d in out.rejected_or_merged_themes}
    accounted |= {d.cluster_id for d in out.outcome_candidates}
    assert accounted == {c.cluster_id for c in theme_set.clusters}
    assert out.stats.clusters_in == len(theme_set.clusters)
    assert _trade_hit(out.model_dump_json()) is None


def test_empty_batch_is_handled():
    out = compress_theme_set(_set())
    assert out.parent_themes == ()
    assert out.stats.clusters_in == 0
    assert "No candidate cleared the promotion gate" in out.human_readout
