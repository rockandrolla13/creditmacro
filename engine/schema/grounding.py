"""Grounding contract — the shared vocabulary of "is this text in the source".

Frozen on purpose, and authored ahead of the kernel that uses it. `engine/grounding/`
is built in two halves (span matching and numeric tokenizing) which must agree on
these types; fixing them here first is what stops the halves from diverging.

**The harness authors these, never the LLM.** A `GroundingVerdict` is a finding about
a claim, not a claim about a claim — nothing that a model emits may be deserialized
straight into one. See `PLAN-authoritative-harness.md` §2 and its non-negotiable:
*a missing output is always preferable to an unsourced one.*

Absence is representable throughout: `Optional` means "not established", never "zero".
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

#: How a span was located. Ordered weakest-last; `none` means it was not located.
#: `loose_human_confirmed` is reachable only through the D1 review queue — the kernel
#: itself never emits it, because no fuzzy match is ever auto-accepted.
GroundingMethod = Literal["exact", "normalized", "loose_human_confirmed", "none"]

#: `unverifiable` is distinct from `ungrounded`: the former means the check could not
#: run (no source index, empty quote), the latter means it ran and the text is absent.
#: Collapsing them would let a broken pipeline read as a clean rejection.
GroundingStatus = Literal["grounded", "ungrounded", "unverifiable"]


class Number(BaseModel):
    """A numeric token with both the raw source form and a canonical value (D6).

    Both are kept because they answer different questions. `raw` is what the page
    actually said, and is what a human is shown when confirming a claim. `value` +
    `unit` are what comparison runs on. Verification matches on `value`; display
    defaults to `raw`.

    A range ("120-140bp") is one token, not two: `value` carries the lower bound and
    `value_upper` the upper, so a range is never silently flattened to a point.
    """

    model_config = ConfigDict(frozen=True)

    raw: str                                    # verbatim substring, exactly as written
    value: float                                # canonical; lower bound if a range
    value_upper: Optional[float] = None         # set only for ranges
    unit: Optional[str] = None                  # normalized: "bp", "%", "usd", "x", None
    char_start: Optional[int] = None            # offset into the source text
    char_end: Optional[int] = None

    @property
    def is_range(self) -> bool:
        return self.value_upper is not None


class GroundingVerdict(BaseModel):
    """The harness's finding on whether a claim is supported by verbatim source text.

    Never author-set: the producer of a claim supplies a quote, and the kernel decides
    whether that quote exists. `reason` is required so a rejection is always explicable
    to the human who has to act on it.
    """

    model_config = ConfigDict(frozen=True)

    status: GroundingStatus
    method: GroundingMethod
    span_found: bool
    numbers_verified: bool
    reason: str
    span_char_start: Optional[int] = None
    span_char_end: Optional[int] = None
    verified_numbers: tuple[Number, ...] = Field(default_factory=tuple)
    #: Set only when the G3 proposer-verifier ran. `None` means "not assessed",
    #: which must never be read as "assessed and scored zero".
    entailment_score: Optional[float] = None

    @property
    def is_grounded(self) -> bool:
        return self.status == "grounded"
