"""PART 3 — EvidenceExtractionAgent: turn CASE sources into structured evidence + discovery objects.

Deterministic, rule-assisted extraction validated on a JPM regression fixture + three non-JPM
fixtures. The acceptance bar is GENERALIZATION: different reports must produce different axes and
different top strategy families (no collapse to JPM-style related-obligation RV). Fixtures are
synthetic, paraphrased markdown — the extractor logic is generic; the fixtures are just inputs.
"""
from __future__ import annotations

import json

import pytest

from engine.evidence_extraction import EvidenceExtractionInput, EvidenceExtractionBundle
from engine.probability_evidence import map_evidence_to_scenarios
from engine.schema import EvidenceAtom, Scenario
from engine.wiki_agents import REGISTRY, EvidenceExtractionAgent

# ── fixtures (synthetic, paraphrased; figures + causal + axis + theme language) ──

JPM_MD = """
<!-- page:1 -->
AI infrastructure funding has become a distinct credit ecosystem spanning 27 issuers and over $450bn of related obligations.
The hyperscaler-to-IG-project relationship averages about 105bp, while the hyperscaler-to-HY-project relationship averages about 183bp, because project bonds carry construction risk and weaker guarantees.
Index-tracking ETFs and benchmark inclusion shape demand for data-center bonds.
<!-- page:6 -->
A new Data Center sub-sector entered the JULI index at about $49bn par, roughly 4.8% of Technology and 0.5% of JULI.
Data Centers trade around 181bp versus Technology around 101bp, due to longer duration and index-inclusion differences.
<!-- page:8 -->
HPC issuance reached $26.6bn YTD, which is 43% of non-refinancing HY issuance, and HPC index weight rose from 1.07% to 2.68%.
<!-- page:9 -->
HPC returned +9.99% YTD versus the HY index +1.61%, and HPC spreads tightened to 295bp, which reflects crowding and heavy demand.
"""

SOFTWARE_MD = """
<!-- page:1 -->
Software and private-credit issuers face refinancing stress because the 2021 LBO vintage hits a maturity wall into high rates.
This leads to distressed exchanges and rising defaults, which drives spread decompression versus the broad HY index.
The software-loan spread minus broad HY OAS has widened to 250bp.
Recovery skew and balance-sheet strength vary, and broad HY beta and rating mix differ across names.
"""

ETF_MD = """
<!-- page:1 -->
Credit ETF flows and create-redeem pressure are driving a non-fundamental demand shock.
The ETF trades at a premium to NAV, and the ETF-versus-basket OAS residual has widened to 30bp because of basket illiquidity.
Create and redeem activity reflects flow-driven dislocation rather than fundamentals.
"""

MARGIN_MD = """
<!-- page:1 -->
Inflation and rising input costs pressure margins for issuers with weak pricing power.
This creates sector spread dispersion because margin sensitivity differs across sectors.
Input-cost beta and pricing-power scores vary, driving a sector spread dispersion of 60bp.
"""

WEAK_MD = "A brief qualitative note with no figures and no relationships worth pricing."


def _extract(md, slug="src", **kw):
    inp = EvidenceExtractionInput(
        source_slug=slug, source_type="report", access_class="case",
        normalized_markdown=md, source_date="2026-05-11", **kw)
    return EvidenceExtractionAgent().run(inp)


def _fams(bundle):
    return {h.family for h in bundle.strategy_family_hints}


def _axis_blob(bundle):
    return " ".join(
        f"{a.axis_name} {a.observable_series}" for a in bundle.operational_axes).lower()


def _theme_blob(bundle):
    return " ".join(str(t) for t in bundle.core_theme_candidates).lower()


# ── PART 5 tests ────────────────────────────────────────────────────────────────

def test_agent_registered_and_implemented():
    a = REGISTRY.get_agent("EvidenceExtractionAgent")
    assert isinstance(a, EvidenceExtractionAgent)
    # implemented (does not raise NotImplementedError on a valid case input)
    out = a.run(EvidenceExtractionInput(source_slug="x", source_type="report",
                                        access_class="case", normalized_markdown=JPM_MD))
    assert isinstance(out, EvidenceExtractionBundle)


def test_rejects_non_case_source():
    with pytest.raises(ValueError):
        EvidenceExtractionInput(source_slug="x", source_type="book",
                                access_class="method", normalized_markdown="x")


def test_returns_bundle():
    assert isinstance(_extract(JPM_MD), EvidenceExtractionBundle)


def test_every_atom_has_source_and_provenance():
    b = _extract(JPM_MD, slug="jpm")
    assert b.evidence_atoms
    for a in b.evidence_atoms:
        assert a.source_slug == "jpm"
        assert a.source_location and a.source_location.strip()


def test_source_facts_and_synthesis_separated():
    b = _extract(JPM_MD)
    # evidence atoms are source-derived facts, never agent synthesis
    assert all(a.claim_kind != "agent_synthesis" for a in b.evidence_atoms)
    # synthesised material (falsifiers) lives in its own list, not among the atoms
    assert b.falsifiers
    atom_claims = {a.claim for a in b.evidence_atoms}
    assert not (set(b.falsifiers) & atom_claims)


def test_jpm_extracts_required_evidence_figures():
    b = _extract(JPM_MD, slug="jpm")
    blob = " ".join(a.claim for a in b.evidence_atoms) + " " + \
           " ".join(str(n) for a in b.evidence_atoms for n in a.numbers)
    for fig in ("27", "450", "105", "183", "49", "4.8", "0.5", "181", "101",
                "26.6", "43", "1.07", "2.68", "9.99", "1.61", "295"):
        assert fig in blob, f"missing figure {fig}"


def test_jpm_extracts_expected_themes_and_axes():
    b = _extract(JPM_MD)
    themes = _theme_blob(b)
    assert any(k in themes for k in ("ecosystem", "capex", "ai"))
    assert any(k in themes for k in ("hpc", "crowding", "supply"))
    assert any(k in themes for k in ("index", "inclusion", "data center", "data-center"))
    axes = _axis_blob(b)
    assert any(k in axes for k in ("versus", "minus", "vs"))     # relative-value axes
    assert "index weight" in axes or "weight" in axes


def test_software_routes_to_decompression_rv_not_jpm():
    b = _extract(SOFTWARE_MD, slug="sw")
    fams = _fams(b)
    assert "long_short" in fams
    assert "etf_basket_rv" not in fams
    assert not (fams & {"steepener", "flattener", "curve"})
    assert any(k in _theme_blob(b) for k in ("decompression", "refinancing", "software", "private"))


def test_etf_routes_to_etf_or_index_rv():
    b = _extract(ETF_MD, slug="etf")
    fams = _fams(b)
    assert fams & {"etf_basket_rv", "index_index_rv"}
    assert not (fams & {"steepener", "flattener", "curve"})
    assert any(k in _axis_blob(b) for k in ("nav", "premium", "basket", "etf"))


def test_margin_routes_to_long_short_or_sector_rotation():
    b = _extract(MARGIN_MD, slug="mg")
    fams = _fams(b)
    assert fams & {"long_short", "sector_rotation"}
    assert "etf_basket_rv" not in fams
    assert any(k in _theme_blob(b) for k in ("margin", "pricing", "dispersion", "inflation"))


def test_different_reports_produce_different_axes_and_families():
    jpm, sw, etf, mg = (_extract(JPM_MD), _extract(SOFTWARE_MD),
                        _extract(ETF_MD), _extract(MARGIN_MD))
    fam_sets = [_fams(jpm), _fams(sw), _fams(etf), _fams(mg)]
    # not all collapse to the same family set
    assert len({frozenset(f) for f in fam_sets}) >= 3
    # ETF axis vocabulary differs from software axis vocabulary
    assert _axis_blob(etf) != _axis_blob(sw)


def test_no_scenario_probabilities_invented():
    b = _extract(JPM_MD)
    # fixtures carry no explicit scenario language ⇒ no scenario candidates, no probabilities
    assert b.scenario_candidates == []
    blob = json.dumps(b.model_dump()).lower()
    assert "p_s" not in blob and "probability" not in blob


def test_no_trade_sizing_hedge_or_execution_emitted():
    b = _extract(JPM_MD)
    blob = json.dumps(b.model_dump()).lower()
    for forbidden in ("hedge_ratio", "position_size", "stop_loss", "execution", "dv01", "leg_ratio"):
        assert forbidden not in blob
    assert b.no_trade_confirmation


def test_weak_source_warns():
    b = _extract(WEAK_MD, slug="weak")
    assert b.extraction_warnings


def test_current_input_seam_consumes_extracted_atoms():
    b = _extract(JPM_MD, slug="jpm", current_input=True)
    atoms = b.evidence_atoms
    assert atoms
    scns = [Scenario(name="crowding_persists", p_s=0.5,
                     driver_path="HPC index weight rises, HPC OAS tightens, HPC return outperforms",
                     implied_axis_value=0.0, pnl_per_unit=0.0),
            Scenario(name="reversal", p_s=0.5, driver_path="HPC OAS widens, weight falls",
                     implied_axis_value=0.0, pnl_per_unit=0.0)]
    maps = map_evidence_to_scenarios(scns, atoms)
    assert len(maps) == 2
    assert any(m.impacts for m in maps)   # extracted atoms actually map


# ── PART 6 copyright / access tests ─────────────────────────────────────────────

def _longest_verbatim_run(a: str, b: str) -> int:
    from tools.leak_check import longest_verbatim_run
    return longest_verbatim_run(a, b)


def test_no_atom_contains_long_verbatim_text():
    for md in (JPM_MD, SOFTWARE_MD, ETF_MD, MARGIN_MD):
        b = _extract(md)
        for a in b.evidence_atoms:
            assert _longest_verbatim_run(a.claim, md) < 25, f"verbatim leak: {a.claim!r}"


def test_extracted_bundle_is_case_not_method():
    b = _extract(JPM_MD)
    # the bundle is CASE extraction output: atoms are source-derived (not method skill cards),
    # and nothing in the bundle declares method access.
    assert all(a.claim_kind in ("source_fact", "source_forecast", "source_opinion") for a in b.evidence_atoms)
    assert "skill_card" not in json.dumps(b.model_dump()).lower()
