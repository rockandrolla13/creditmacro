"""G8 contract — the per-(source x theme) brief. **Schema only; the gate is a scaffold.**

The types are written now because they are declarative and fixing them early is what
stops the writer and the gate from diverging (the same reason `schema/grounding.py` was
authored ahead of its kernel). The behaviour lives in
`engine.grounding.brief_gate`, which is NOT implemented — see its docstring.

**What a brief is.** One short brief per (source, theme) pair the source contributes
evidence to. Not one per source: if a note supports three themes it gets three briefs,
each answering only *what does this source say about THIS theme*.

**Why it is the most dangerous object in the system.** A PM will not read forty
markdowns; they will read this. A fluent paragraph that blends two sources, or adds a
connective claim neither made, is invisible to a reader and invisible to G1/G2, which
inspect atoms rather than prose.

**The structural defence is closed-vocabulary generation.** The writer never sees the
raw markdown — only the `kept` atoms for that pair, already span-grounded and
number-verified. It cannot cite what it was never shown, so the factual vocabulary is
bounded before a token is generated. That is also why a brief is structurally immune to
G5's prompt injection: no untrusted text reaches the writer at all.

Hard limits below are enforced by the harness, not requested of the model.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

#: Hard format limits. Constants rather than magic numbers in the gate, for the same
#: reason D4 names the confidence weights: changing one is a specification change.
MIN_BULLETS = 3
MAX_BULLETS = 5
MAX_WORDS = 120
#: Per-bullet cap, matching the existing verbatim-leak rule (`tests/unit/test_leak_check`).
MAX_BULLET_WORDS = 25

#: What the source says about the theme. Three values, because "contradicts" must be
#: expressible: a brief that can only support is a brief that will always support.
BriefDirection = Literal["supports", "contradicts", "qualifies"]

#: `unavailable` is a legitimate outcome and the schema says so out loud. Per the plan:
#: a missing brief is a fine outcome, a wrong brief is not.
BriefStatus = Literal["available", "unavailable"]


class BriefBullet(BaseModel):
    """One bullet, and the atoms it rests on."""

    model_config = ConfigDict(frozen=True)

    text: str
    #: At least one, and every id must exist in the kept atom set for this (source,
    #: theme) pair. An unreferenced bullet is an unsourced sentence with a bullet point
    #: in front of it.
    atom_ids: tuple[str, ...] = Field(min_length=1)
    verdict_ref: Optional[str] = None


class SourceThemeBrief(BaseModel):
    """One brief, keyed (source_slug, theme_id). Frozen: the gate passes or the brief
    does not exist, and there is no third state in which it is edited into shape."""

    model_config = ConfigDict(frozen=True)

    source_slug: str
    theme_id: str
    bullets: tuple[BriefBullet, ...] = Field(min_length=MIN_BULLETS, max_length=MAX_BULLETS)
    #: Harness-computed, never model-reported.
    word_count: int
    direction: BriefDirection
    #: From G4 (`engine.grounding.confidence`) — the harness's number, not the model's.
    #: `None` when G4 abstained, which must render as "not assessed" and never as 0.
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    #: The G6 `synthesis` node this brief is recorded as. The emit gate's stricter
    #: synthesis rule (every parent grounded) therefore already applies to it.
    ledger_node_id: Optional[str] = None
