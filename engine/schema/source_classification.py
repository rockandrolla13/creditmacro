"""Source classification vocabulary — what a source IS, and what may be read from it.

Lives in `schema/` rather than in `wiki_agents.py` where it was first written, because
four modules need the vocabulary and only one of them needs the agent. Keeping it beside
the agent forced `theme_aggregation` to import `wiki_agents` at module level while
`wiki_agents` imported `theme_aggregation` back inside a function — a cycle survived by a
deferred import rather than resolved. A shared type belongs where shared types live.

`access_class` is load-bearing, not descriptive: it is what the two-phase memory firewall
reads to decide whether a page is reachable during phase A. `method` is always readable;
`case` is unreachable until the freeze.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

SourceTypeT = Literal["book", "paper", "report", "deck", "memo", "transcript",
                      "market_data", "other"]
AccessClassT = Literal["method", "case", "mixed", "ignore"]
# A page has no "mixed": a mixed SOURCE is one whose pages classify differently, so the
# per-page verdict must resolve to exactly one of the three.
PageAccessT = Literal["method", "case", "ignore"]


class PageClassification(BaseModel):
    page_number: int
    access_class: PageAccessT
    rationale: str


class SourceClassification(BaseModel):
    source_slug: str
    source_type: SourceTypeT
    access_class: AccessClassT
    page_classifications: list[PageClassification] = []
    copyright_status: str
    ingestion_policy: str
    recommended_compilers: list[str] = []
    warnings: list[str] = []
