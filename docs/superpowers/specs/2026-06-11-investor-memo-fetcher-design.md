# Investor Memo Fetcher — Design

**Date:** 2026-06-11 · **Status:** approved (full version)

## Goal
Given an investor name (e.g. `oaktree`), find their published investment memos online,
download them, convert each to clean text, and ingest them into the existing source
pipeline as `wiki/sources/` cards — ready for later analysis. It **acquires + ingests,
then STOPS**: no thesis generation, no engine run, no analysis.

## Responsibility split (why a tool AND a skill)
A committed Python script cannot call Claude's web tools, so:
- **`tools/fetch_investor_memos.py`** — deterministic, unit-tested. Given a registry key
  **or** explicit URLs, it fetches, extracts, converts, and ingests. No LLM, no Claude tools.
- **`.claude/skills/fetch-investor-memos/SKILL.md`** — orchestrator. Known investor →
  call the tool with the registry key. Unknown investor → the agent uses WebSearch/WebFetch
  to locate the memo index, confirms the URL with the user, appends it to the registry,
  then calls the tool. Agent owns discovery-of-unknowns; tool owns deterministic fetching.

## Data flow (fits the existing pipeline)
```
investor name ─▶ registry lookup ─▶ memo index URL(s)
   │ (miss) ─▶ agent WebSearch ─▶ confirm w/ user ─▶ add to registry
   ▼
fetch index page ─▶ extract memo links (CSS selector per registry entry)
   ▼  for each memo:
fetch memo page ─▶ raw/memos/<slug>.html        (gitignored)
   ▼  html_to_markdown (bs4)   [PDF memos → tools/convert_pdf_to_markdown.py]
raw/normalized-md/<slug>.md  +  raw/manifests/<slug>.json   (gitignored; full text)
   ▼  create_source_card(access_class="case", source_type="memo")
wiki/sources/<slug>.md   (committable skeleton card — leak-guarded, no verbatim text)
```
`slug = <investor>-<memo-title>-<year>`, e.g. `oaktree-the-best-of-2024`.

## Components & interfaces (`tools/fetch_investor_memos.py`)
- `resolve_investor(name, registry) -> Entry | None` — normalise (lower/strip), follow aliases.
- `fetch_url(url, *, timeout) -> FetchResult{content, content_type, is_pdf}` — `requests`;
  the **only** network function, injected into everything else so tests run offline.
- `extract_memo_links(index_html, entry) -> list[MemoLink{url,title,date}]` — bs4 + the
  entry's CSS selector; de-dupes, resolves relative URLs.
- `html_to_markdown(html) -> (title, markdown)` — bs4: pick `<article>/<main>` or the
  largest text block, strip script/style/nav/header/footer/aside, emit headings/paras/lists.
- `ingest_memo(memo, investor, *, access_class, out_root, fetcher, force) -> slug | None` —
  writes raw + normalized-md + manifest, routes PDFs to the PDF converter, calls
  `create_source_card`. Idempotent: skips an existing slug unless `force`.
- `run(name, *, urls=None, access_class="case", limit=None, force=False, out_root, registry,
  fetcher=fetch_url) -> RunSummary{fetched, skipped, errors}` — top-level orchestration.
- `main(argv)` — CLI.
- Idempotency index: `raw/memos/<investor>.index.json` records `{slug,url,sha256,date}`.

## Registry (`tools/investor_memos_registry.yaml`)
```yaml
oaktree:
  name: "Oaktree Capital (Howard Marks memos)"
  index_urls: ["https://www.oaktreecapital.com/insights/memos"]
  link_selector: "a[href*='/insights/memo/']"
  aliases: ["howard-marks", "howard marks", "marks"]
```
Seeded with `oaktree` only; the skill appends new investors after confirming with the user.

## Decisions
- **access_class = `case`** by default (investor memos are dated opinions — an anchoring
  hazard the two-phase firewall quarantines from fresh Phase-A reasoning). Override with
  `--access-class method` for timeless framework pieces.
- **HTML→text via `bs4`** (already installed). `trafilatura` dropped: the environment blocks
  `pip` (PEP 668). bs4 extraction is adequate for memo article pages.
- **Copyright/storage:** raw memo HTML + full normalized text live under gitignored `raw/`;
  only the leak-guarded wiki card (no verbatim runs ≥25 words) is committable. Consistent with
  the repo's existing private-corpus stance. The tool sets a polite User-Agent and respects
  obvious `robots`/rate limits (small fixed delay between fetches).

## CLI
```bash
python tools/fetch_investor_memos.py oaktree                 # registry key
python tools/fetch_investor_memos.py oaktree --limit 5       # cap memos
python tools/fetch_investor_memos.py --url <memo-url> --investor oaktree   # explicit URL
python tools/fetch_investor_memos.py oaktree --access-class method --force
```

## Testing (no external services)
Inject a fake `fetcher` returning local fixture HTML:
- `extract_memo_links` finds links via selector; resolves relative URLs; de-dupes.
- `html_to_markdown` strips chrome, keeps headings/paras, returns a title.
- `slugify` → `oaktree-the-best-of-2024`.
- `ingest_memo` writes raw/normalized-md/manifest and a `wiki/sources/<slug>.md` card with
  `access_class: case`, `source_type: memo`; second call **skips** (idempotent) unless `force`.
- `resolve_investor` resolves aliases; unknown name → `None`.
- PDF memo URL routes to the PDF converter (mocked).
No network in tests; fixtures live under `tests/fixtures/memos/`.

## Out of scope
Analysis, thesis creation, engine runs, scheduling/auto-refresh, paywalled/login-gated
sources, JS-rendered SPAs that need a headless browser (the agent's WebFetch can cover those
ad hoc via the skill, but the tool targets static HTML).
