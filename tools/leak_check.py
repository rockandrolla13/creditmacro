"""
Copyright leak guard.

Wiki pages must be paraphrase + citation, never reproduced source text. This detector
finds the longest contiguous run of words shared between a wiki page and a raw
normalized-md file; a run >= max_run_words is treated as a verbatim leak.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Union

_WORD = re.compile(r"\w+")


def _tokens(text: str) -> list[str]:
    return _WORD.findall(text.lower())


def longest_verbatim_run(a: str, b: str) -> int:
    """Longest common contiguous run of words between texts a and b (word count)."""
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0
    # DP longest common substring over word sequences (O(len(ta)*len(tb)), rolling rows).
    prev = [0] * (len(tb) + 1)
    best = 0
    for i in range(1, len(ta) + 1):
        cur = [0] * (len(tb) + 1)
        ai = ta[i - 1]
        for j in range(1, len(tb) + 1):
            if ai == tb[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best = cur[j]
        prev = cur
    return best


def assert_clean(
    wiki_dir: Union[str, Path],
    raw_md_dir: Union[str, Path],
    max_run_words: int = 25,
) -> list[str]:
    """Return one violation string per wiki page that shares a >= max_run_words verbatim
    run with any raw normalized-md file. Empty list = clean."""
    wiki_dir, raw_md_dir = Path(wiki_dir), Path(raw_md_dir)
    raw_texts = {p.stem: p.read_text(encoding="utf-8", errors="ignore")
                 for p in raw_md_dir.rglob("*.md")}
    violations: list[str] = []
    for page in wiki_dir.rglob("*.md"):
        body = page.read_text(encoding="utf-8", errors="ignore")
        for raw_slug, raw_text in raw_texts.items():
            run = longest_verbatim_run(body, raw_text)
            if run >= max_run_words:
                violations.append(
                    f"{page.stem}: {run}-word verbatim run from raw '{raw_slug}' "
                    f"(>= {max_run_words}) — paraphrase instead"
                )
                break
    return violations
