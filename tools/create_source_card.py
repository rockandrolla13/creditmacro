"""
create_source_card — normalized-md + metadata → a wiki/sources card (in the existing
wiki/CONVENTIONS frontmatter, read by engine.memory.parse_wiki_page) + appended
EvidenceAtoms. CASE sources also seed a wiki/themes ThemeMemoryCard. Never reproduces
source text: a pre-write leak guard rejects any card that shares a long verbatim run
with raw normalized-md. Does NOT invent facts — empty sections stay empty.

CLI:
  python tools/create_source_card.py --normalized raw/normalized-md/<slug>.md --slug <slug>
      --access-class method|case --source-type book|paper|report|... [--title T] [--force]
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Optional, Union

from .leak_check import assert_clean
from .schemas import EvidenceAtom, SourceFrontmatter

_SECTIONS = [
    "What this source is", "Why it matters", "Main developments mentioned",
    "Key events mentioned", "Core theme candidates mentioned", "Hot topics mentioned",
    "Extracted facts", "Extracted causal claims", "Operational axes", "Confounders",
    "Falsifiers", "Strategy-family hints", "Open questions",
]


def _frontmatter_yaml(fm: SourceFrontmatter) -> str:
    import yaml
    data = fm.model_dump(exclude_none=True)
    return "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n"


def _card_body(fm: SourceFrontmatter, atoms: list[EvidenceAtom]) -> str:
    lines = [f"# {fm.title}\n"]
    extra = ["Method skills extracted"] if fm.access_class == "method" else ["Case themes updated"]
    for section in _SECTIONS[:6] + ["Extracted facts"]:
        lines.append(f"## {section}\n")
        if section == "Extracted facts" and atoms:
            for a in atoms:                       # paraphrased claim + cited atom id, never raw text
                lines.append(f"- {a.claim} ([[evidence:{a.evidence_id}]], {a.source_location})")
            lines.append("")
        else:
            lines.append("<!-- TODO: fill from the source; do not invent facts -->\n")
    for section in _SECTIONS[7:] + extra:
        lines.append(f"## {section}\n<!-- TODO -->\n")
    return "\n".join(lines)


def _theme_card(slug: str, title: str) -> str:
    return (
        f"---\ntype: theme\naccess_class: case\ntitle: {title}\nslug: {slug}\n"
        f"status: stub\ntheme_status: core_theme_candidate\n"
        f"main_developments: []\nkey_events: []\nhot_topics: []\ncausal_chain: []\n"
        f"operational_axes: []\nconfounders: []\nfalsifiers: []\nstrategy_families: []\n"
        f"sources: ['{slug}']\ncreated: {date.today().isoformat()}\n---\n"
        f"# {title}\n\n<!-- CASE memory: phase-B only. TODO: fill from evidence atoms. -->\n"
    )


def create_source_card(
    *,
    slug: str,
    title: str,
    normalized_md: Union[str, Path],
    access_class: str,
    source_type: str,
    out_wiki: Union[str, Path],
    raw_md_dir: Union[str, Path],
    atoms: Optional[list[EvidenceAtom]] = None,
    raw_source_path: Optional[str] = None,
    force: bool = False,
) -> dict:
    out_wiki = Path(out_wiki)
    atoms = atoms or []
    fm = SourceFrontmatter(                      # validates access_class
        title=title, slug=slug, access_class=access_class, source_type=source_type,
        raw_source_path=raw_source_path or str(normalized_md),
        created=date.today().isoformat(), updated=date.today().isoformat(),
    )
    card_text = _frontmatter_yaml(fm) + "\n" + _card_body(fm, atoms)

    src_dir = out_wiki / "sources"
    src_dir.mkdir(parents=True, exist_ok=True)
    src_path = src_dir / f"{slug}.md"
    if src_path.exists() and not force:
        raise FileExistsError(f"{src_path} exists — pass force=True to overwrite a curated card")
    src_path.write_text(card_text, encoding="utf-8")

    # Pre-write leak guard: the card must not reproduce raw source text.
    leaks = assert_clean(src_dir, raw_md_dir, max_run_words=25)
    if any(slug in v for v in leaks):
        src_path.unlink()
        raise ValueError(f"leak guard: card '{slug}' reproduces raw source text — paraphrase it")

    # Append evidence atoms (each carries a required source_location).
    ev_dir = out_wiki / "evidence"; ev_dir.mkdir(parents=True, exist_ok=True)
    ev_path = ev_dir / "evidence_atoms.jsonl"
    with ev_path.open("a", encoding="utf-8") as f:
        for a in atoms:
            f.write(a.model_dump_json() + "\n")

    theme_path = None
    if access_class == "case":
        themes = out_wiki / "themes"; themes.mkdir(parents=True, exist_ok=True)
        theme_path = themes / f"{slug}.md"
        if not theme_path.exists() or force:
            theme_path.write_text(_theme_card(slug, title), encoding="utf-8")

    return {"source": str(src_path), "theme": str(theme_path) if theme_path else None,
            "atoms": len(atoms)}


def main() -> None:
    ap = argparse.ArgumentParser(description="normalized-md → wiki source card + evidence atoms")
    ap.add_argument("--normalized", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--access-class", required=True, choices=["method", "case"])
    ap.add_argument("--source-type", required=True)
    ap.add_argument("--title", default=None)
    ap.add_argument("--out-wiki", default="wiki")
    ap.add_argument("--raw-md-dir", default="raw/normalized-md")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    res = create_source_card(
        slug=args.slug, title=args.title or args.slug, normalized_md=args.normalized,
        access_class=args.access_class, source_type=args.source_type,
        out_wiki=args.out_wiki, raw_md_dir=args.raw_md_dir, force=args.force,
    )
    print(f"OK source={res['source']} theme={res['theme']} atoms={res['atoms']}")


if __name__ == "__main__":
    main()
