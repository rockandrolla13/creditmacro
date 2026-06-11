---
name: fetch-investor-memos
description: >
  Use when the user wants to find or download a specific investor's published investment
  memos / letters BY NAME so they can be ingested for later analysis. Triggers: "fetch
  oaktree memos", "download Howard Marks memos", "find Klarman's letters", "get <investor>
  memos", "pull <firm>'s investor letters". Do NOT trigger for analysing memos already in
  wiki/sources, for the thesis tracker, or for running the discovery engine.
---

# Fetch Investor Memos

> Acquisition skill (NOT a method/case reasoning card). Turns an investor NAME into ingested
> source cards: find their memo index → download each memo → convert to clean text →
> `create_source_card`. It ACQUIRES + INGESTS, then STOPS. No analysis, no thesis, no engine
> run. Spec: `docs/superpowers/specs/2026-06-11-investor-memo-fetcher-design.md`.

## What it produces (per memo)
- `raw/memos/<slug>.html` — raw page (gitignored)
- `raw/normalized-md/<slug>.md` + `raw/manifests/<slug>.json` — full text (gitignored)
- `wiki/sources/<slug>.md` — committable, leak-guarded card (`source_type: memo`,
  `access_class: case` by default). Case sources also seed a `wiki/themes/<slug>.md` stub.

`access_class` defaults to **case**: a dated investor opinion is an anchoring hazard the
two-phase firewall keeps out of fresh Phase-A reasoning. Use `--access-class method` only for
genuinely timeless framework pieces, and say why.

## Procedure

1. **Normalise the name** the user gave (e.g. "Oaktree", "Howard Marks").

2. **Known investor?** Check `tools/investor_memos_registry.yaml` (keys + `aliases`). If it
   resolves, just run the tool:
   ```bash
   python tools/fetch_investor_memos.py <name> [--limit N] [--access-class case|method] [--force]
   ```

3. **Unknown investor?** The tool can't web-search — YOU do it:
   - Use WebSearch to find the firm/author's official memo or letter index page.
   - **Confirm the exact index URL with the user** before fetching (don't guess silently).
   - Append an entry to `tools/investor_memos_registry.yaml`:
     ```yaml
     <key>:
       name: "<Investor / firm>"
       index_urls: ["<confirmed index URL>"]
       link_selector: "<CSS selector matching the memo links>"   # inspect the page
       aliases: ["<other names>"]
     ```
     To find the selector, fetch the index once (WebFetch or the tool's `fetch_url`) and look
     at the memo anchor hrefs (a shared path fragment like `/memo/` or `/letters/` usually
     works as `a[href*='/memo/']`).
   - Then run the tool as in step 2.

4. **JS-rendered / paywalled index?** If a static fetch returns zero links (a React SPA, or a
   login wall), fall back to YOUR WebFetch to read the index and gather memo URLs, then feed
   them to the tool explicitly — it still does the per-memo download + convert + ingest:
   ```bash
   python tools/fetch_investor_memos.py --investor <name> --url <memo-url-1> --url <memo-url-2>
   ```

5. **Report**: list the slugs ingested and where they landed. STOP. If the user wants
   analysis, that is a separate, explicit step (engine run or manual review of the new cards).

## Guardrails
- Never invent a memo URL — confirm with the user or web search.
- Raw memo text stays under gitignored `raw/`; only the no-verbatim wiki card is committable
  (a leak guard rejects any card reproducing ≥25 verbatim words).
- Respect the site: the tool sets a polite User-Agent and spaces live fetches; honour obvious
  robots/ToS and don't hammer paginated archives — use `--limit` while exploring.
- This skill does not analyse, rank, price, or form theses. It only acquires sources.
