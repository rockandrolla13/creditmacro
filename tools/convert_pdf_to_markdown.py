"""
convert_pdf_to_markdown — page-aware PDF → raw/normalized-md + manifest.

Writes ONLY under the raw/ root (never wiki/, never the source PDF). Emits a
`<!-- page:N -->` anchor before every page so downstream cards can cite `page:N`.
Flags low-confidence / table-heavy / image-heavy pages in the manifest. Primary engine
pymupdf4llm; per-page text falls back to PyMuPDF `get_text`. Optional `pdfplumber` for
table CSVs (degrades to a flag if absent).

CLI:
  python tools/convert_pdf_to_markdown.py --pdf raw/pdfs/<f>.pdf --slug <slug> [--out raw/]
"""
from __future__ import annotations

import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Union

import fitz  # PyMuPDF

from .schemas import ConversionManifest

try:  # optional table extraction
    import pdfplumber  # noqa: F401
    _HAVE_PDFPLUMBER = True
except Exception:
    _HAVE_PDFPLUMBER = False


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def convert(pdf: Union[str, Path], slug: str, out_root: Union[str, Path]) -> ConversionManifest:
    pdf = Path(pdf)
    out_root = Path(out_root)
    nmd_dir = out_root / "normalized-md"
    man_dir = out_root / "manifests"
    nmd_dir.mkdir(parents=True, exist_ok=True)
    man_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf))
    n_pages = doc.page_count

    # Per-page markdown via pymupdf4llm; fall back to PyMuPDF get_text per page.
    chunks = None
    engine = "pymupdf4llm"
    try:
        import pymupdf4llm
        chunks = pymupdf4llm.to_markdown(str(pdf), page_chunks=True)
    except Exception:
        chunks = None
        engine = "pymupdf"

    parts: list[str] = []
    anchors: list[int] = []
    low, table_heavy, image_heavy = [], [], []
    for i in range(n_pages):
        page = doc[i]
        pno = i + 1
        anchors.append(pno)
        if chunks is not None and i < len(chunks):
            ptext = chunks[i].get("text", "") or ""
        else:
            ptext = page.get_text() or ""
        if len(ptext.strip()) < 10:
            low.append(pno)
        try:
            if page.find_tables().tables:
                table_heavy.append(pno)
        except Exception:
            pass
        if page.get_images():
            image_heavy.append(pno)
        parts.append(f"<!-- page:{pno} -->\n{ptext.rstrip()}\n")

    (nmd_dir / f"{slug}.md").write_text("\n".join(parts), encoding="utf-8")

    manifest = ConversionManifest(
        slug=slug,
        source_pdf=str(pdf),
        sha256=hashlib.sha256(pdf.read_bytes()).hexdigest()[:16],
        n_pages=n_pages,
        engine=engine,
        page_anchors=anchors,
        low_confidence_pages=low,
        table_heavy_pages=table_heavy,
        image_heavy_pages=image_heavy,
        created_at=_now(),
    )
    (man_dir / f"{slug}.json").write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
    doc.close()
    return manifest


def main() -> None:
    ap = argparse.ArgumentParser(description="PDF → raw/normalized-md + manifest")
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--out", default="raw")
    args = ap.parse_args()
    m = convert(args.pdf, args.slug, args.out)
    print(f"OK {m.slug}: {m.n_pages} pages → {args.out}/normalized-md/{m.slug}.md "
          f"(low={len(m.low_confidence_pages)}, tables={len(m.table_heavy_pages)}, "
          f"images={len(m.image_heavy_pages)}; pdfplumber={_HAVE_PDFPLUMBER})")


if __name__ == "__main__":
    main()
