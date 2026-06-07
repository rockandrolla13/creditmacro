"""PDF→markdown converter preserves page numbers and never mutates the source PDF."""
from __future__ import annotations

import fitz  # PyMuPDF (already a dependency via pymupdf4llm)

from tools.convert_pdf_to_markdown import convert


def _make_pdf(path, pages: int) -> None:
    doc = fitz.open()
    for i in range(pages):
        page = doc.new_page()
        page.insert_text((72, 72), f"Page {i+1}: credit spreads, entropy, and carry.")
    doc.save(str(path))
    doc.close()


def test_preserves_page_numbers(tmp_path):
    pdf = tmp_path / "src.pdf"
    _make_pdf(pdf, 3)
    out = tmp_path / "raw"
    manifest = convert(pdf, "src", out)

    assert manifest.n_pages == 3
    assert manifest.page_anchors == [1, 2, 3]
    md = (out / "normalized-md" / "src.md").read_text(encoding="utf-8")
    for n in (1, 2, 3):
        assert f"<!-- page:{n} -->" in md
    assert (out / "manifests" / "src.json").exists()


def test_does_not_overwrite_the_pdf(tmp_path):
    pdf = tmp_path / "src.pdf"
    _make_pdf(pdf, 2)
    before = pdf.stat().st_mtime_ns, pdf.read_bytes()
    convert(pdf, "src", tmp_path / "raw")
    after = pdf.stat().st_mtime_ns, pdf.read_bytes()
    assert before == after  # immutable raw


def test_converter_does_not_write_into_wiki(tmp_path):
    pdf = tmp_path / "src.pdf"
    _make_pdf(pdf, 1)
    out = tmp_path / "raw"
    convert(pdf, "src", out)
    # everything stays under raw/; the converter is wiki-blind
    assert not (tmp_path / "wiki").exists()
