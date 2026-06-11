"""Fetch an investor's published memos and ingest them into the source pipeline.

Given a registry key (e.g. `oaktree`) or explicit URLs, this downloads each memo, converts
it to clean text, and writes a wiki/sources card — ready for later analysis. It ACQUIRES +
INGESTS, then STOPS: no thesis generation, no engine run, no analysis.

Deterministic + offline-testable: the only network function is `fetch_url`, injected into
everything else, so tests pass a fake fetcher returning local fixture HTML.

    python tools/fetch_investor_memos.py oaktree
    python tools/fetch_investor_memos.py oaktree --limit 5 --access-class case
    python tools/fetch_investor_memos.py --url <memo-url> --investor oaktree

Raw memo HTML + full normalized text land under gitignored raw/; only the leak-guarded
wiki card (no verbatim text) is committable. Memos default to access_class='case' — a dated
investor opinion is an anchoring hazard the two-phase firewall keeps out of fresh reasoning.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional, Union
from urllib.parse import urljoin

# Allow direct-script invocation (python tools/fetch_investor_memos.py ...).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bs4 import BeautifulSoup  # noqa: E402

from tools.create_source_card import create_source_card  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY_PATH = _REPO_ROOT / "tools" / "investor_memos_registry.yaml"
DEFAULT_OUT_ROOT = _REPO_ROOT
DEFAULT_WIKI_ROOT = _REPO_ROOT / "wiki"
USER_AGENT = "creditmacro-research/1.0 (personal research; contact: local)"
_FETCH_DELAY_S = 1.0  # polite gap between live fetches
_CHROME_TAGS = ("script", "style", "nav", "header", "footer", "aside", "form", "noscript")


# ── data types ───────────────────────────────────────────────────────────────
@dataclass
class FetchResult:
    content: str
    content_type: str
    is_pdf: bool
    url: str


@dataclass
class MemoLink:
    url: str
    title: str
    date: Optional[str] = None


@dataclass
class RunSummary:
    investor: str
    fetched: int = 0
    skipped: int = 0
    errors: list[str] = field(default_factory=list)
    slugs: list[str] = field(default_factory=list)


class Registry(dict):
    """investor key -> entry dict. A thin dict subclass so callers can build one inline."""

    @classmethod
    def load(cls, path: Union[str, Path] = DEFAULT_REGISTRY_PATH) -> "Registry":
        import yaml
        data = yaml.safe_load(Path(path).read_text()) or {}
        return cls(data)


# ── network (the only live function; injected elsewhere) ─────────────────────
def fetch_url(url: str, *, timeout: float = 20.0) -> FetchResult:
    import requests
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    resp.raise_for_status()
    ctype = resp.headers.get("Content-Type", "")
    is_pdf = "pdf" in ctype.lower() or url.lower().endswith(".pdf")
    content = resp.content.decode("latin-1") if is_pdf else resp.text
    return FetchResult(content=content, content_type=ctype, is_pdf=is_pdf, url=url)


Fetcher = Callable[..., FetchResult]


# ── registry resolution ──────────────────────────────────────────────────────
def _norm(name: str) -> str:
    return re.sub(r"\s+", "-", name.strip().lower())


def resolve_investor(name: str, registry: Registry) -> Optional[dict]:
    key = _norm(name)
    if key in registry:
        return registry[key]
    for entry in registry.values():
        aliases = {_norm(a) for a in entry.get("aliases", [])}
        if key in aliases:
            return entry
    return None


# ── link extraction ──────────────────────────────────────────────────────────
def extract_memo_links(index_html: str, entry: dict, *, base_url: str = "") -> list[MemoLink]:
    soup = BeautifulSoup(index_html, "html.parser")
    selector = entry.get("link_selector", "a")
    seen: set[str] = set()
    links: list[MemoLink] = []
    for a in soup.select(selector):
        href = a.get("href")
        if not href:
            continue
        url = urljoin(base_url, href)
        if url in seen:
            continue
        seen.add(url)
        links.append(MemoLink(url=url, title=a.get_text(strip=True) or url))
    return links


# ── html -> markdown ─────────────────────────────────────────────────────────
def _main_node(soup: BeautifulSoup):
    for tag in ("article", "main"):
        node = soup.find(tag)
        if node is not None:
            return node
    # fallback: the <div>/<section> with the most text
    candidates = soup.find_all(["div", "section"])
    return max(candidates, key=lambda n: len(n.get_text()), default=soup.body or soup)


def html_to_markdown(html: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    page_title = soup.title.get_text(strip=True) if soup.title else ""
    for t in soup(list(_CHROME_TAGS)):
        t.decompose()
    node = _main_node(soup)

    lines: list[str] = []
    title = ""
    for el in node.find_all(["h1", "h2", "h3", "p", "li"]):
        text = el.get_text(" ", strip=True)
        if not text:
            continue
        if el.name == "h1":
            if not title:
                title = text
            lines.append(f"# {text}")
        elif el.name == "h2":
            lines.append(f"## {text}")
        elif el.name == "h3":
            lines.append(f"### {text}")
        elif el.name == "li":
            lines.append(f"- {text}")
        else:
            lines.append(text)
    if not title:
        title = (page_title.split("|")[0].strip() if page_title else "Untitled memo")
    return title, "\n\n".join(lines) + "\n"


# ── slug ─────────────────────────────────────────────────────────────────────
def slugify(investor: str, title: str, year: Optional[str] = None) -> str:
    base = f"{_norm(investor)}-{_norm(title)}"
    base = re.sub(r"[^a-z0-9-]+", "-", base).strip("-")
    base = re.sub(r"-{2,}", "-", base)
    return f"{base}-{year}" if year else base


def _year(date: Optional[str]) -> Optional[str]:
    m = re.search(r"(19|20)\d{2}", date or "")
    return m.group(0) if m else None


def _rel(path: Path, root: Union[str, Path]) -> str:
    """Path relative to out_root when possible (matches existing cards), else absolute."""
    try:
        return str(Path(path).relative_to(Path(root)))
    except ValueError:
        return str(path)


# ── ingest one memo ──────────────────────────────────────────────────────────
def ingest_memo(
    memo: MemoLink,
    investor: str,
    *,
    access_class: str = "case",
    out_root: Union[str, Path] = DEFAULT_OUT_ROOT,
    wiki_root: Union[str, Path] = DEFAULT_WIKI_ROOT,
    fetcher: Fetcher = fetch_url,
    force: bool = False,
) -> Optional[str]:
    """Fetch -> raw html + normalized md + manifest -> wiki source card. Returns the slug,
    or None if it already existed (idempotent skip). PDFs route to the PDF converter."""
    out_root, wiki_root = Path(out_root), Path(wiki_root)
    raw_md_dir = out_root / "raw" / "normalized-md"
    memos_dir = out_root / "raw" / "memos"
    manifests_dir = out_root / "raw" / "manifests"
    for d in (raw_md_dir, memos_dir, manifests_dir):
        d.mkdir(parents=True, exist_ok=True)

    res = fetcher(memo.url)
    if res.is_pdf:
        return _ingest_pdf_memo(res, memo, investor, access_class, out_root, wiki_root, force)

    title, md = html_to_markdown(res.content)
    slug = slugify(investor, memo.title or title, _year(memo.date))

    card_path = wiki_root / "sources" / f"{slug}.md"
    if card_path.exists() and not force:
        return None

    (memos_dir / f"{slug}.html").write_text(res.content, encoding="utf-8")
    md_with_anchor = f"<!-- source: {memo.url} -->\n\n{md}"
    (raw_md_dir / f"{slug}.md").write_text(md_with_anchor, encoding="utf-8")
    (manifests_dir / f"{slug}.json").write_text(json.dumps({
        "slug": slug, "investor": investor, "url": memo.url, "title": title,
        "date": memo.date, "sha256": hashlib.sha256(res.content.encode()).hexdigest(),
        "kind": "memo-html",
    }, indent=2))

    create_source_card(
        slug=slug, title=title, normalized_md=raw_md_dir / f"{slug}.md",
        access_class=access_class, source_type="memo",
        out_wiki=wiki_root, raw_md_dir=raw_md_dir,
        raw_source_path=_rel(memos_dir / f"{slug}.html", out_root), force=force,
    )
    return slug


def _ingest_pdf_memo(res, memo, investor, access_class, out_root, wiki_root, force):
    """Route a PDF memo through the existing page-aware PDF converter."""
    out_root = Path(out_root)
    pdf_dir = out_root / "raw" / "pdfs"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(investor, memo.title, _year(memo.date))
    card_path = Path(wiki_root) / "sources" / f"{slug}.md"
    if card_path.exists() and not force:
        return None
    pdf_path = pdf_dir / f"{slug}.pdf"
    pdf_path.write_bytes(res.content.encode("latin-1"))
    from tools.convert_pdf_to_markdown import convert_pdf  # imported lazily (heavy dep)
    convert_pdf(pdf=pdf_path, slug=slug, out=out_root / "raw")
    create_source_card(
        slug=slug, title=memo.title, normalized_md=out_root / "raw" / "normalized-md" / f"{slug}.md",
        access_class=access_class, source_type="memo",
        out_wiki=wiki_root, raw_md_dir=out_root / "raw" / "normalized-md",
        raw_source_path=_rel(pdf_path, out_root), force=force,
    )
    return slug


# ── run (top level) ──────────────────────────────────────────────────────────
def run(
    name: str,
    *,
    registry: Registry,
    urls: Optional[list[str]] = None,
    access_class: str = "case",
    limit: Optional[int] = None,
    force: bool = False,
    out_root: Union[str, Path] = DEFAULT_OUT_ROOT,
    wiki_root: Union[str, Path] = DEFAULT_WIKI_ROOT,
    fetcher: Fetcher = fetch_url,
    delay_s: float = 0.0,
) -> RunSummary:
    """Resolve the investor, gather memo links (from explicit urls or the registry index),
    and ingest each. Unknown investor with no explicit urls -> reported error, never silent."""
    summary = RunSummary(investor=name)

    if urls:
        memos = [MemoLink(url=u, title=u.rstrip("/").rsplit("/", 1)[-1]) for u in urls]
    else:
        entry = resolve_investor(name, registry)
        if entry is None:
            summary.errors.append(
                f"no registry entry for '{name}' and no --url given; "
                f"the skill should web-search the memo index, confirm it, and add it."
            )
            return summary
        memos = []
        for index_url in entry.get("index_urls", []):
            try:
                idx = fetcher(index_url)
                memos.extend(extract_memo_links(idx.content, entry, base_url=index_url))
            except Exception as e:  # noqa: BLE001 — surface, don't abort the whole run
                summary.errors.append(f"index fetch failed for {index_url}: {e}")

    if limit is not None:
        memos = memos[:limit]

    for memo in memos:
        try:
            slug = ingest_memo(memo, name, access_class=access_class, out_root=out_root,
                               wiki_root=wiki_root, fetcher=fetcher, force=force)
            if slug is None:
                summary.skipped += 1
            else:
                summary.fetched += 1
                summary.slugs.append(slug)
        except Exception as e:  # noqa: BLE001
            summary.errors.append(f"{memo.url}: {e}")
        if delay_s:
            time.sleep(delay_s)
    return summary


# ── CLI ──────────────────────────────────────────────────────────────────────
def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="fetch_investor_memos", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("investor", nargs="?", help="registry key or investor name")
    p.add_argument("--url", action="append", dest="urls", help="explicit memo URL (repeatable)")
    p.add_argument("--investor", dest="investor_opt", help="investor label when using --url")
    p.add_argument("--access-class", default="case", choices=["case", "method"])
    p.add_argument("--limit", type=int)
    p.add_argument("--force", action="store_true")
    p.add_argument("--registry", default=str(DEFAULT_REGISTRY_PATH))
    args = p.parse_args(argv)

    name = args.investor or args.investor_opt
    if not name:
        print("error: provide an investor name (or --investor with --url)", file=sys.stderr)
        return 2
    registry = Registry.load(args.registry) if Path(args.registry).exists() else Registry({})

    summary = run(name, registry=registry, urls=args.urls, access_class=args.access_class,
                  limit=args.limit, force=args.force, delay_s=_FETCH_DELAY_S)
    print(f"investor={summary.investor}  fetched={summary.fetched}  skipped={summary.skipped}")
    for s in summary.slugs:
        print(f"  + {s}")
    for e in summary.errors:
        print(f"  ! {e}", file=sys.stderr)
    return 0 if not summary.errors or summary.fetched else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
