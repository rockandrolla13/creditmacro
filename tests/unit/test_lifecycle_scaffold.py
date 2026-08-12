"""Scaffold-stage tests for `engine.lifecycle`.

There is no behaviour to test yet, so these assert the two things a scaffold CAN get wrong:
the package does not import, or the contract types quietly permit a fabricated value. The
second is the one that matters — this repo's governing rule is that a missing output is
preferable to an unsourced one, and a required `float` on a projection field is how that rule
gets broken at the type level rather than in code review.
"""
from __future__ import annotations

import inspect
from datetime import date

import pytest
from pydantic import ValidationError

from engine import lifecycle
from engine.lifecycle import (
    decisions,
    evidence_pack,
    factor_projection,
    regime,
    scorecard,
    surprise,
    theme_book,
    theme_enrichment,
    theme_view,
)

MODULES = [
    decisions,
    evidence_pack,
    factor_projection,
    regime,
    scorecard,
    surprise,
    theme_book,
    theme_enrichment,
    theme_view,
]


# ── import smoke ─────────────────────────────────────────────────────────────

def test_package_imports_and_exports_the_l1_contract():
    assert lifecycle.THEME_VIEW_CONTRACT == "themeview/1"
    assert lifecycle.ThemeView is theme_view.ThemeView


@pytest.mark.parametrize("module", MODULES, ids=lambda m: m.__name__.rsplit(".", 1)[-1])
def test_every_module_has_a_docstring(module):
    assert module.__doc__ and module.__doc__.strip()


def test_no_module_reads_the_wall_clock():
    """Invariant I8. `as_of` / `now` are parameters everywhere in this layer, so no source file
    may call `datetime.now`, `date.today` or `time.time`."""
    banned = ("datetime.now(", "date.today(", "time.time(", "utcnow(")
    for module in MODULES:
        src = inspect.getsource(module)
        for token in banned:
            assert token not in src, f"{module.__name__} reads the clock via {token}"


# ── stubs announce themselves ────────────────────────────────────────────────

STUBS = [
    (theme_view.project, "L1"),
    (theme_view.require_contract, "L1"),
    (regime.discover_regimes, "A1"),
    (theme_enrichment.enrich, "A2"),
    (surprise.classify_number, "L2"),
    (surprise.collapse_levels, "L2"),
    (evidence_pack.pack_terminal, "L3"),
    (scorecard.compute_scorecard, "L3"),
    (theme_book.render_week, "L4"),
    (theme_book.to_markdown, "L4"),
    (factor_projection.decompose, "L5"),
    (factor_projection.expression_gate, "L5"),
]


@pytest.mark.parametrize("fn,phase", STUBS, ids=[f.__name__ for f, _ in STUBS])
def test_stub_raises_naming_its_phase(fn, phase):
    sig = inspect.signature(fn)
    kwargs = {
        name: None
        for name, p in sig.parameters.items()
        if p.default is inspect.Parameter.empty
    }
    with pytest.raises(NotImplementedError) as exc:
        fn(**kwargs)
    assert phase in str(exc.value)


# ── the absence rule, enforced at the type level ─────────────────────────────

def _minimal_view(**overrides) -> theme_view.ThemeView:
    kwargs = dict(
        as_of="2026-08-10",
        theme_id="t1",
        statement="a theme",
        status="discovery_complete",
        assembled_from=(theme_view.ViewSource(kind="theme_object", ref="t1"),),
    )
    kwargs.update(overrides)
    return theme_view.ThemeView(**kwargs)


def test_theme_view_accepts_a_theme_with_no_watch_no_confidence_no_hash():
    """The plan types `surveillance_status`, `confidence`, `horizon` and `ledger_root` as
    required, which would force a guessed status and a fabricated 0.0. They are Optional here,
    and this is the test that pins that decision."""
    view = _minimal_view(
        unavailable=("surveillance_status", "confidence") + theme_view.DEFERRED_TO_V2
    )
    assert view.surveillance_status is None
    assert view.confidence is None
    assert view.snapshot_hash is None
    assert view.ledger_root is None
    assert "surveillance_status" in view.unavailable


def test_theme_view_is_frozen_and_forbids_unknown_fields():
    view = _minimal_view()
    with pytest.raises(ValidationError):
        view.theme_id = "t2"
    with pytest.raises(ValidationError):
        _minimal_view(smuggled_field="nope")


def test_theme_view_pins_its_contract_version():
    with pytest.raises(ValidationError):
        _minimal_view(contract_version="themeview/2")


def test_deferred_fields_are_absent_from_the_v1_shape():
    """`briefs`, `no_view_twin` and `factor_decomposition` have no producer (G8, harness §7,
    L5), so v1 must not carry them — and `extra="forbid"` must make that structural."""
    for field in theme_view.DEFERRED_TO_V2:
        assert field not in theme_view.ThemeView.model_fields


def test_falsifier_view_distinguishes_unread_from_read_zero():
    unread = theme_view.FalsifierView(observable="CCC/BB OAS ratio")
    read_zero = theme_view.FalsifierView(observable="CCC/BB OAS ratio", last_read_value=0.0)
    assert unread.last_read_value is None
    assert read_zero.last_read_value == 0.0


def test_scorecard_on_an_empty_corpus_reports_unknown_not_zero():
    card = scorecard.Scorecard(as_of="2026-08-10", unavailable=("hit_rate",))
    assert card.hit_rate is None
    assert card.packs_considered == 0


def test_factor_decomposition_absent_shares_are_none():
    decomp = factor_projection.FactorDecomposition(
        theme_id="t1", as_of="2026-08-10", insufficient_data_reason="no factor premia supplied"
    )
    assert decomp.residual_alpha_share is None
    assert decomp.harvested_premium_share is None


def test_numeric_context_defaults_to_level():
    """A number is a level until something proves it is a surprise, never the other way round
    (D-L2-1)."""
    ctx = surprise.NumericContext(series="oas", observed_at=date(2026, 8, 10), realized=412.0)
    assert ctx.kind == "level"
    assert ctx.expected is None
    assert ctx.expected_tier == "none"
    assert ctx.collapsed_count == 1


# ── the two blocked decisions are recorded, not guessed ──────────────────────

def test_opinion_claim_kinds_is_empty_and_says_why():
    """D-A1-3 names claim kinds no extractor in this repo emits. The constant stays empty and
    carries the reason rather than shipping a plausible mapping."""
    assert decisions.OPINION_CLAIM_KINDS == frozenset()
    assert "D-A1-3" in decisions.OPINION_CLAIM_KINDS_UNRESOLVED


def test_decision_constants_carry_the_resolved_values():
    assert decisions.REGIME_COUNT_FLOOR == 3
    assert decisions.REGIME_COUNT_CAP == 7
    assert decisions.RESIDUAL_ALPHA_THRESHOLD == 0.40
    assert decisions.MODEL_GENERATED_EXPECTATION_ALLOWED is False
    assert decisions.ALIVE_STATUSES == frozenset({"armed", "confirming"})
    assert decisions.DEDUP_THRESHOLDS["hy"] == 0.75


def test_every_emitted_model_stamps_the_decisions_version():
    stamped = [
        theme_view.ThemeView,
        regime.RegimeVocabulary,
        theme_enrichment.EnrichedThemeMap,
        surprise.NumericContext,
        evidence_pack.EvidencePack,
        scorecard.Scorecard,
        theme_book.ThemeBook,
        factor_projection.FactorDecomposition,
    ]
    for model in stamped:
        assert "decisions_version" in model.model_fields, model.__name__


# ── A2 does not duplicate compression ────────────────────────────────────────

def test_enrichment_references_the_analyst_map_rather_than_copying_parents():
    """The failure this guards against: a second theme type beside `ParentTheme` with a second
    promotion gate. `EnrichedThemeMap` holds the map itself, and no enrichment field restates a
    parent's name, mechanism, falsifier or evidence."""
    assert "theme_map" in theme_enrichment.EnrichedThemeMap.model_fields
    parent_owned = {"name", "canonical_name", "mechanism", "falsifier", "evidence_ids",
                    "thesis_statement", "strategy_families", "source_coverage"}
    assert parent_owned.isdisjoint(theme_enrichment.ThemeEnrichment.model_fields)
    assert "parent_id" in theme_enrichment.ThemeEnrichment.model_fields


def test_nothing_in_the_engine_imports_the_lifecycle_package_yet():
    """The layer sits strictly downstream. Until it is wired, no existing module may depend on
    it — that is what keeps the golden master untouched."""
    import pathlib

    root = pathlib.Path(theme_view.__file__).parent.parent
    offenders = []
    for path in root.rglob("*.py"):
        if "lifecycle" in path.parts or path.parent.name == "lifecycle":
            continue
        if "from .lifecycle" in path.read_text() or "engine.lifecycle" in path.read_text():
            offenders.append(str(path))
    assert not offenders, f"lifecycle is not wired yet, but imported by {offenders}"
