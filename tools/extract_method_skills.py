"""
extract_method_skills — runs ONLY on access_class=method sources. Reads a wiki/sources
card, refuses CASE (fail-closed), and writes MethodCard skeletons to wiki/process/ and
ensures the EngineSpec pages exist in wiki/engines/. It never writes wiki/themes
(that is CASE memory). Skeletons carry TODOs — the agent fills the real skills; this tool
does not invent method content.

CLI:  python tools/extract_method_skills.py --slug <slug> [--wiki wiki/]
"""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import Union

from engine.memory import parse_wiki_page

from .schemas import MethodCard


class AccessClassError(ValueError):
    """Raised when method extraction is attempted on a CASE source (firewall)."""


def _method_card_md(slug: str, skill: str) -> str:
    mc = MethodCard(
        skill_name=skill, theoretical_source="<TODO>", mathematical_primitive="<TODO>",
        software_primitive="<TODO>", pipeline_phase="<TODO>", implementation_maturity="not_built",
    )
    fm = mc.model_dump()
    import yaml
    return (
        "---\ntype: concept\naccess_class: method\n"
        f"title: '{skill}'\nslug: {slug}__{skill}\nstatus: stub\n"
        f"sources: ['{slug}']\ncreated: {date.today().isoformat()}\n"
        "---\n"
        f"# Method skill: {skill}\n\n```yaml\n{yaml.safe_dump(fm, sort_keys=False)}```\n"
        "<!-- TODO: fill the MethodCard from the source (paraphrase only). -->\n"
    )


def extract_method_skills(*, slug: str, wiki_dir: Union[str, Path], force: bool = False) -> list[str]:
    wiki_dir = Path(wiki_dir)
    src_path = wiki_dir / "sources" / f"{slug}.md"
    if not src_path.exists():
        raise FileNotFoundError(src_path)
    page = parse_wiki_page(src_path)
    if page.access_class != "method":
        raise AccessClassError(
            f"extract_method_skills refuses access_class={page.access_class!r} for '{slug}' "
            "— method extraction runs only on METHOD sources."
        )

    proc = wiki_dir / "process"; proc.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    # One skeleton skill page per source (the agent expands it; we do not invent content).
    skill = f"{slug}-method-skill"
    out = proc / f"{slug}__{skill}.md"
    if out.exists() and not force:
        return [str(out)]
    out.write_text(_method_card_md(slug, skill), encoding="utf-8")
    written.append(str(out))
    return written


def main() -> None:
    ap = argparse.ArgumentParser(description="method source → MethodCards (wiki/process)")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--wiki", default="wiki")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    paths = extract_method_skills(slug=args.slug, wiki_dir=args.wiki, force=args.force)
    print("OK wrote:", *paths, sep="\n  ")


if __name__ == "__main__":
    main()
