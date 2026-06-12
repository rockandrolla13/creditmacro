"""WikiIntegratorAgent schemas — the durable-persistence plan + result.

The integrator turns extraction/aggregation outputs into wiki pages. It PLANS first
(a WikiUpdatePlan: every page it would write) and then APPLIES (a WikiIntegrationResult).
DISCIPLINE: it persists structured summaries only — never raw source text (copyright),
never trades/sizing/hedge ratios/scenario probabilities. access_class is stamped, never
upgraded (old CASE never becomes METHOD).
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

PageKind = Literal[
    "source", "evidence", "theme", "theme_cluster", "concept", "entity", "outcome",
    "index", "log", "memory_map",
]
WriteAction = Literal["create", "update", "append", "skip"]


class WikiPageWrite(BaseModel):
    """One planned page write. `content` is the full file body for create/update, or the
    appended snippet for append. `skip` means an identical page already exists (idempotency)."""
    path: str
    kind: PageKind
    action: WriteAction
    access_class: Optional[str] = None
    content: str = ""


class WikiUpdatePlan(BaseModel):
    """Everything the integrator WOULD write — produced in dry-run, executed on apply."""
    writes: list[WikiPageWrite] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    blocked: list[str] = Field(default_factory=list)   # firewall / no-trade / copyright blocks
    no_trade_confirmation: str = (
        "WikiIntegrator persists structured memory only — no trades, sizing, hedge ratios, "
        "scenario probabilities, or execution; no raw source text."
    )


class WikiIntegrationResult(BaseModel):
    """The outcome of applying a plan (or a dry-run echo of the plan)."""
    plan: WikiUpdatePlan
    applied: bool
    written_paths: list[str] = Field(default_factory=list)
    skipped_paths: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
