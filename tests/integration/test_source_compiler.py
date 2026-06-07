"""End-to-end: convert → source card + evidence atoms → method/engine extraction,
with the method/case split enforced and the firewall vocabulary reused from engine.memory."""
from __future__ import annotations

import json

import fitz
import pytest

from engine.memory import parse_wiki_page
from tools.convert_pdf_to_markdown import convert
from tools.create_source_card import create_source_card
from tools.extract_method_skills import AccessClassError, extract_method_skills
from tools.schemas import EvidenceAtom


def _pdf(path):
    doc = fitz.open()
    doc.new_page().insert_text((72, 72), "A source about credit spreads, carry, and entropy.")
    doc.save(str(path)); doc.close()


def _setup(tmp_path, access_class, source_type):
    raw = tmp_path / "raw"; wiki = tmp_path / "wiki"
    pdf = tmp_path / "s.pdf"; _pdf(pdf)
    convert(pdf, "src", raw)
    atoms = [EvidenceAtom(evidence_id="e1", source_slug="src", source_location="page:1",
                          claim_type="fact", claim="the source discusses carry")]
    res = create_source_card(
        slug="src", title="A Source", normalized_md=raw / "normalized-md" / "src.md",
        access_class=access_class, source_type=source_type,
        out_wiki=wiki, raw_md_dir=raw / "normalized-md", atoms=atoms,
    )
    return raw, wiki, res


def test_source_card_has_correct_access_class(tmp_path):           # test 2
    _, wiki, _ = _setup(tmp_path, "method", "paper")
    page = parse_wiki_page(wiki / "sources" / "src.md")
    assert page.type == "source"
    assert page.access_class == "method"


def test_method_source_creates_method_cards_not_themes(tmp_path):  # test 3
    _, wiki, _ = _setup(tmp_path, "method", "paper")
    extract_method_skills(slug="src", wiki_dir=wiki)
    assert list((wiki / "process").glob("src*.md"))               # MethodCards
    assert not list((wiki / "themes").glob("src*.md"))            # no ThemeMemoryCard


def test_case_source_creates_atoms_and_theme_not_method(tmp_path):  # test 4
    _, wiki, _ = _setup(tmp_path, "case", "report")
    assert (wiki / "themes" / "src.md").exists()                  # ThemeMemoryCard
    assert (wiki / "evidence" / "evidence_atoms.jsonl").exists()
    with pytest.raises(AccessClassError):
        extract_method_skills(slug="src", wiki_dir=wiki)          # method extraction refuses case


def test_evidence_atoms_include_source_location(tmp_path):         # test 5
    _, wiki, _ = _setup(tmp_path, "case", "report")
    lines = (wiki / "evidence" / "evidence_atoms.jsonl").read_text().splitlines()
    assert lines
    assert all(json.loads(line)["source_location"] for line in lines)


def test_no_overwrite_without_force(tmp_path):
    raw, wiki, _ = _setup(tmp_path, "method", "paper")
    with pytest.raises(FileExistsError):
        create_source_card(
            slug="src", title="A Source", normalized_md=raw / "normalized-md" / "src.md",
            access_class="method", source_type="paper",
            out_wiki=wiki, raw_md_dir=raw / "normalized-md", atoms=[],
        )
