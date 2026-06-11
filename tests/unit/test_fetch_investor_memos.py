"""Investor memo fetcher — offline tests. A fake `fetcher` returns local fixture HTML so
no network is touched. Verifies registry/alias resolution, link extraction, HTML→markdown,
slugging, and idempotent full ingest into a wiki/sources card (access_class=case)."""
from __future__ import annotations

from pathlib import Path

import pytest

from tools.fetch_investor_memos import (
    FetchResult,
    Registry,
    extract_memo_links,
    html_to_markdown,
    ingest_memo,
    resolve_investor,
    run,
    slugify,
)

FIX = Path(__file__).resolve().parent.parent / "fixtures" / "memos"
INDEX_HTML = (FIX / "index.html").read_text()
MEMO_HTML = (FIX / "memo_best_of.html").read_text()

REGISTRY = Registry({
    "oaktree": {
        "name": "Oaktree Capital (Howard Marks memos)",
        "index_urls": ["https://www.oaktreecapital.com/insights/memos"],
        "link_selector": "a[href*='/insights/memo/']",
        "aliases": ["howard-marks", "marks"],
    }
})


def _fake_fetcher(url, **_):
    """Map any memo URL to the memo fixture, index URLs to the index fixture."""
    if "/insights/memo/" in url:
        return FetchResult(content=MEMO_HTML, content_type="text/html", is_pdf=False, url=url)
    return FetchResult(content=INDEX_HTML, content_type="text/html", is_pdf=False, url=url)


# ── registry resolution ──────────────────────────────────────────────────────

def test_resolve_known_investor():
    e = resolve_investor("OAKTREE", REGISTRY)
    assert e is not None and "oaktreecapital" in e["index_urls"][0]


def test_resolve_alias():
    assert resolve_investor("Howard Marks", REGISTRY) is not None  # via 'howard-marks'


def test_resolve_unknown_returns_none():
    assert resolve_investor("nobody-here", REGISTRY) is None


# ── link extraction ──────────────────────────────────────────────────────────

def test_extract_links_dedupes_and_resolves_relative():
    links = extract_memo_links(INDEX_HTML, REGISTRY["oaktree"],
                               base_url="https://www.oaktreecapital.com/insights/memos")
    urls = [l.url for l in links]
    assert "https://www.oaktreecapital.com/insights/memo/the-best-of" in urls
    assert "https://www.oaktreecapital.com/insights/memo/sea-change" in urls
    assert len(urls) == len(set(urls))  # the duplicate 'the-best-of' collapses


# ── html -> markdown ─────────────────────────────────────────────────────────

def test_html_to_markdown_strips_chrome_keeps_body():
    title, md = html_to_markdown(MEMO_HTML)
    assert title == "The Best Of"
    assert "first paragraph of the memo" in md
    assert "## On Risk" in md
    assert "point one" in md
    for junk in ("site header", "nav links", "related junk", "copyright junk"):
        assert junk not in md


# ── slug ─────────────────────────────────────────────────────────────────────

def test_slugify_investor_title_year():
    assert slugify("oaktree", "The Best Of", "2024") == "oaktree-the-best-of-2024"


# ── full ingest (idempotent) ─────────────────────────────────────────────────

def test_ingest_writes_raw_md_and_wiki_card(tmp_path):
    from tools.fetch_investor_memos import MemoLink
    memo = MemoLink(url="https://www.oaktreecapital.com/insights/memo/the-best-of",
                    title="The Best Of", date="2024-05-01")
    slug = ingest_memo(memo, "oaktree", access_class="case", out_root=tmp_path,
                       wiki_root=tmp_path / "wiki", fetcher=_fake_fetcher)
    assert slug == "oaktree-the-best-of-2024"
    assert (tmp_path / "raw" / "normalized-md" / f"{slug}.md").exists()
    assert (tmp_path / "raw" / "memos" / f"{slug}.html").exists()
    card = (tmp_path / "wiki" / "sources" / f"{slug}.md").read_text()
    assert "access_class: case" in card
    assert "source_type: memo" in card


def test_ingest_is_idempotent(tmp_path):
    from tools.fetch_investor_memos import MemoLink
    memo = MemoLink(url="https://www.oaktreecapital.com/insights/memo/the-best-of",
                    title="The Best Of", date="2024-05-01")
    kw = dict(access_class="case", out_root=tmp_path, wiki_root=tmp_path / "wiki",
              fetcher=_fake_fetcher)
    assert ingest_memo(memo, "oaktree", **kw) == "oaktree-the-best-of-2024"
    assert ingest_memo(memo, "oaktree", **kw) is None  # second call skips


# ── run() end to end (offline) ───────────────────────────────────────────────

def test_run_fetches_all_memos_offline(tmp_path):
    summary = run("oaktree", registry=REGISTRY, out_root=tmp_path,
                  wiki_root=tmp_path / "wiki", fetcher=_fake_fetcher)
    assert summary.fetched >= 2  # the-best-of + sea-change
    cards = list((tmp_path / "wiki" / "sources").glob("oaktree-*.md"))
    assert len(cards) >= 2


def test_run_unknown_investor_reports_no_registry_entry(tmp_path):
    summary = run("nobody-here", registry=REGISTRY, out_root=tmp_path,
                  wiki_root=tmp_path / "wiki", fetcher=_fake_fetcher)
    assert summary.fetched == 0
    assert summary.errors  # surfaced, not silently empty
