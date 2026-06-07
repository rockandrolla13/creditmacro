"""Schemas for the source compiler — reuse engine.memory's access_class vocabulary."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from engine.memory import VALID_ACCESS_CLASSES
from tools.schemas import (
    ConversionManifest,
    EngineSpec,
    EvidenceAtom,
    MethodCard,
    SourceFrontmatter,
)


def test_access_class_vocabulary_is_shared_with_engine():
    # the tools must not invent their own firewall vocabulary
    assert set(VALID_ACCESS_CLASSES) == {"method", "case"}


def test_source_frontmatter_requires_valid_access_class():
    SourceFrontmatter(type="source", title="t", slug="s", access_class="method",
                      source_type="paper")
    with pytest.raises(ValidationError):
        SourceFrontmatter(type="source", title="t", slug="s", access_class="public",
                          source_type="paper")


def test_evidence_atom_requires_source_location():
    a = EvidenceAtom(evidence_id="e1", source_slug="s", source_location="page:3",
                     claim_type="fact", claim="x")
    assert a.source_location == "page:3"
    assert a.is_synthesis is False           # source fact by default
    with pytest.raises(ValidationError):
        EvidenceAtom(evidence_id="e1", source_slug="s", source_location="",
                     claim_type="fact", claim="x")


def test_method_card_and_engine_spec_maturity():
    mc = MethodCard(skill_name="max_entropy_q", theoretical_source="Cover-Thomas",
                    mathematical_primitive="min-KL tilt", software_primitive="solve_q_tilt",
                    pipeline_phase="pricing", implementation_maturity="active")
    assert mc.implementation_maturity == "active"
    EngineSpec(engine_name="causal_compiler", maturity="active")
    with pytest.raises(ValidationError):
        EngineSpec(engine_name="x", maturity="someday")


def test_conversion_manifest_round_trips():
    m = ConversionManifest(slug="s", source_pdf="raw/pdfs/s.pdf", sha256="ab", n_pages=2,
                           engine="pymupdf4llm", page_anchors=[1, 2], created_at="2026-06-07")
    assert m.n_pages == 2 and m.page_anchors == [1, 2]
