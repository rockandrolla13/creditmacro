"""G4 contract — what a harness-computed confidence is made of.

Today's confidence is a product of hand-set multipliers. `_RULE_ATOM_CONFIDENCE = 0.8`
in `evidence_extraction.py` is an author's opinion wearing a decimal point, and
`ConfidenceComponents` on a `StrategyFamilyRec` records five such opinions multiplied
together. Nothing about those numbers was observed. G4's whole claim is that a
confidence should be **earned from what the harness saw**, not asserted.

Three types, and the split between them is the point:

* `ConfidenceSignals` — the OBSERVATIONS. Every field is something deterministic code
  established for itself (a span was located, a number matched, two distinct sources
  said it). The model's own self-reported confidence appears here too, but only as
  `model_confidence`, and `engine.grounding.confidence` may use it to LOWER a score and
  never to raise one.
* `AtomConfidenceComponents` — the per-term SUB-SCORES, kept so a low number is
  explicable. `None` means "not assessed" and must never be read as "assessed and
  scored zero"; the difference is exactly what makes abstention possible.
* `AtomConfidence` — the OUTCOME, which may be `abstained`. A harness that cannot say
  "I do not know" has to say something else, and what it says will be a number a PM
  reads as a finding.

`Insufficient` generalises `NoCleanAxisError`: abstention as a value a seam can return
rather than an exception one seam happens to raise.

All frozen. A confidence that downstream code can overwrite is not a finding, it is a
suggestion — and `PLAN-authoritative-harness.md` §3 G4 requires the harness to hold it.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from engine.schema.grounding import GroundingMethod


class ConfidenceSignals(BaseModel):
    """What the harness observed about one claim. Never model-authored except for the
    explicitly-named `model_confidence`, which is a ceiling and nothing else.

    Every optional field distinguishes "not established" from a low value. A source with
    no known publication date has `age_days=None`, not `age_days=99999` — the first
    abstains from the freshness term, the second invents a fact about the source.
    """

    model_config = ConfigDict(frozen=True)

    #: From the `GroundingVerdict`. `none` means the span was never located.
    grounding_method: GroundingMethod = "none"
    span_found: bool = False
    #: Two flags, not one. `numbers_checked=False` means the policy skipped the number
    #: check; `numbers_checked=True, numbers_verified=False` means it ran and failed.
    #: Collapsing them would score an unchecked atom the same as a caught transcription
    #: error.
    numbers_checked: bool = False
    numbers_verified: bool = False
    #: Set only when the G3 proposer-verifier ran (Phase 5). `None` = not assessed.
    entailment_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    #: From the source page frontmatter / claim-kind prior — see
    #: `engine.probability_evidence.RELIABILITY_DEFAULTS`. `None` = unknown source.
    source_reliability: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    #: How many DISTINCT sources carry this claim (its evidence cluster). One source
    #: repeating itself is one source.
    distinct_sources: Optional[int] = Field(default=None, ge=0)
    #: Age of the source at the analysis date, computed by
    #: `engine.grounding.confidence.age_in_days` from two SUPPLIED dates. There is no
    #: path here that consults the clock (I8).
    age_days: Optional[int] = None
    #: The model's self-report, if any. A CAP: it may lower the computed value, never
    #: raise it. This is the one place a generative number is allowed to matter, and it
    #: is allowed to matter only in the direction of less confidence.
    model_confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class AtomConfidenceComponents(BaseModel):
    """The decomposed sub-scores behind an `AtomConfidence`, so the number is auditable.

    `assessed_weight` is the fraction of the total weight that was actually observable.
    It is the abstention trigger: a score averaged over two of six terms is not a
    confident score computed from thin evidence, it is a number the harness had no
    business producing.
    """

    model_config = ConfigDict(frozen=True)

    grounding: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    numbers: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    reliability: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    independence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    freshness: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    entailment: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    assessed_weight: float = Field(ge=0.0, le=1.0)
    #: True when `model_confidence` bound the result — i.e. the harness would have said
    #: more than the model did, and deferred to the lower of the two.
    model_cap_applied: bool = False


#: `computed` carries a number. `abstained` carries none and is a first-class answer.
#: `ungrounded` carries 0.0 and is a verdict about the evidence, not a weak score.
ConfidenceOutcome = Literal["computed", "abstained", "ungrounded"]


class AtomConfidence(BaseModel):
    """A confidence the harness computed, or its refusal to compute one.

    `version` is stamped on every instance (D4). The weights are constants in code and
    changing them is a specification change, so an old stored score stays interpretable
    only if it says which constants produced it.
    """

    model_config = ConfigDict(frozen=True)

    version: str
    outcome: ConfidenceOutcome
    #: `None` iff `outcome == "abstained"`. Absence is the abstention, not a sentinel.
    value: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    reason: str
    components: AtomConfidenceComponents

    @model_validator(mode="after")
    def _outcome_matches_value(self) -> "AtomConfidence":
        if self.outcome == "abstained" and self.value is not None:
            raise ValueError("an abstention carries no value")
        if self.outcome != "abstained" and self.value is None:
            raise ValueError(f"outcome {self.outcome!r} requires a value")
        if self.outcome == "ungrounded" and self.value != 0.0:
            raise ValueError("an ungrounded claim scores exactly 0.0")
        return self


class Insufficient(BaseModel):
    """A seam's first-class "I do not know" — abstention as a value, not an exception.

    `NoCleanAxisError` established the precedent for one seam. Generalising it means the
    runner can route ANY seam's abstention to a blocked/degraded path instead of taking
    a fabricated slot, and means a confident-but-ungrounded answer can be ranked BELOW
    an abstention rather than above it (see `confidence.preference_key`).

    `missing` names what would settle the question, so an abstention is actionable
    rather than merely honest.
    """

    model_config = ConfigDict(frozen=True)

    seam: str
    reason: str
    missing: tuple[str, ...] = ()
