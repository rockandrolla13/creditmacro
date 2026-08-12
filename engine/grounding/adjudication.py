"""G3 — proposer-verifier adjudication. **SCAFFOLD ONLY (Phase 5). Not implemented.**

Every function here raises `NotImplementedError`. That is deliberate and it is the
honest state of this guardrail.

**Why a stub and not a working version.** G3's entire value is that a SECOND, INDEPENDENT
model refutes by default (D3: a different model id, not merely a different prompt). A
version of this built without live calls would have to fake the verifier — and a faked
verifier does not fail to work, it works WRONGLY: it returns `agree` on everything,
`assert_adjudicated` passes, and the pipeline gains a guardrail-shaped object that
certifies fabrications. `PLAN-authoritative-harness.md` puts G3 in Phase 5 behind
explicit provider selection for exactly this reason. A missing output is always
preferable to an unsourced one; a missing GUARDRAIL is preferable to a decorative one.

**The contract, so the shape is fixed before the model is wired.**

* Proposer = the existing seam call on `Provider` (`engine/protocols.py`).
* Verifier = an independent call, different model id per `model_manifest.MANIFEST`,
  with a refute-by-default system prompt: it sees the source text and the proposal and
  must either cite the grounding span(s) or refute. Absent explicit grounding, it
  rejects.
* Disagreement is NEVER resolved by picking one silently: one bounded re-ask carrying
  the objection, then `status="blocked"`, `block_reason="adjudication_failed:<seam>"`.
* Runs in Phase A only (fresh reasoning), captured via `engine/capture.py` so replay
  makes no live call.

**What building it needs, beyond code:** a pinned verifier model with prompt hashes
filled into `model_manifest.MANIFEST`, scripted proposer+verifier fixtures for the four
cases (agree / refute / re-ask-then-agree / re-ask-then-HALT), and a cost decision — the
verifier roughly doubles seam spend.
"""
from __future__ import annotations

from typing import Any, Optional, Protocol

from pydantic import BaseModel, ConfigDict

_PHASE = "G3 — Phase 5 (proposer-verifier adjudication)"


class AdjudicationVerdict(BaseModel):
    """The verifier's finding on one proposal. Harness-authored from the verifier's
    typed reply; the verifier does not author its own verdict object any more than an
    extractor authors its own `GroundingVerdict`."""

    model_config = ConfigDict(frozen=True)

    seam: str
    agree: bool
    #: Verbatim spans the verifier cited as grounding the proposal. Empty on a refutation.
    grounding_spans: tuple[str, ...] = ()
    #: Why it refused. Required when `agree` is False; carried into the bounded re-ask.
    objection: Optional[str] = None
    #: Which model produced this verdict, for the D3 independence check.
    verifier_model_id: Optional[str] = None


class AdjudicationBlocked(RuntimeError):
    """Unresolved disagreement after the bounded re-ask. HALT to the PM."""


class Verifier(Protocol):
    """The independent second opinion. Implementations live behind provider selection."""

    def verify(self, seam: str, proposal: Any, source_text: str) -> AdjudicationVerdict:
        ...


class AdjudicatedProvider:
    """Decorates a `Provider`, adjudicating the four high-stakes generative seams:
    `expand_causal`, `define_axis`, `propose_scenarios`, `build_system_map`.

    Not implemented — see the module docstring.
    """

    def __init__(self, provider: Any, verifier: Verifier, source_text: str) -> None:
        raise NotImplementedError(f"{_PHASE}: needs a live, independently-pinned verifier")


def adjudicate(
    seam: str,
    proposal: Any,
    verifier: Verifier,
    source_text: str,
    *,
    reask: Optional[Any] = None,
) -> AdjudicationVerdict:
    """Run proposer-verifier on one proposal, with at most one bounded re-ask.

    Not implemented — see the module docstring.
    """
    raise NotImplementedError(f"{_PHASE}: verifier must be a different pinned model (D3)")


def assert_adjudicated(verdicts: tuple[AdjudicationVerdict, ...]) -> None:
    """Raise `AdjudicationBlocked` on any surviving disagreement.

    Not implemented — see the module docstring. Note the failure direction if this were
    stubbed permissively instead: a no-op would report every seam as adjudicated.
    """
    raise NotImplementedError(f"{_PHASE}: no verifier exists, so nothing has been adjudicated")


__all__ = [
    "AdjudicatedProvider",
    "AdjudicationBlocked",
    "AdjudicationVerdict",
    "Verifier",
    "adjudicate",
    "assert_adjudicated",
]
