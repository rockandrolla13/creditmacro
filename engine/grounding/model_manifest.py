"""G7 — model and prompt pinning. What a live call is allowed to be.

Pure and deterministic: hashing and comparison. No network, no wall clock. The one
impure thing — reading an environment variable — is isolated in `override_enabled()`,
which takes an injected env mapping, so every other function stays testable.

**The gap this closes.** `test_golden_master` locks the pricing arithmetic byte for
byte. Nothing locks what comes out of an LLM seam. Swap a model id, nudge a temperature,
edit a prompt for clarity, and every seam output can move while every test stays green —
because the tests exercise `ScriptedProvider`, which is exactly why they are fast and
deterministic and exactly why they cannot see this.

**Pin, then refuse.** `MANIFEST` names the model id, the sampling parameters and a
content hash per seam prompt. A live call whose effective configuration differs is
REFUSED, not warned about, mirroring `provider_select.LiveDiscoveryNotEnabled`. The
override is an explicit environment flag, in the same spirit as
`ALLOW_LIVE_LLM_DISCOVERY`: possible, deliberate, and visible in a shell history.

**Prompt hashes are not filled in.** `SeamPin.prompt_hash` is `None` for every seam
here. Pinning a hash means reading `engine/prompts.py` and freezing its current text,
and that file belongs to work in flight — a hash pinned against a moving file fails on
the next honest edit and gets deleted rather than investigated. `assert_pinned` treats
an unpinned hash as "not asserted" and still checks model and params, so the module is
useful today and complete the moment the prompts settle. Fail-closed here would mean
refusing every live call, which is not the same as safety.

**D3 lives here.** The G3 verifier must run on a DIFFERENT model id from the proposer,
and the manifest validates that rather than trusting a caller to remember it.
"""
from __future__ import annotations

import hashlib
import os
from typing import Mapping, Optional

from pydantic import BaseModel, ConfigDict, model_validator

#: Bump when any pinned value below changes. Stamped on refusals so a mismatch report
#: names which manifest it was judged against.
MANIFEST_VERSION = "g7.v1"

#: Explicit opt-in, checked by the caller via `override_enabled`. Named to sit
#: alongside `provider_select.ALLOW_LIVE_LLM_DISCOVERY` rather than inventing a new
#: convention for the same idea.
ENV_OVERRIDE = "ALLOW_UNPINNED_LLM_MODEL"


class ModelPinMismatch(RuntimeError):
    """A live call's model, parameters or prompt differ from the manifest. Fail closed."""


class SamplingParams(BaseModel):
    """The parameters that make a seam reproducible. `temperature=0` is not a style
    preference: at any other temperature two identical runs are two different runs, and
    capture/replay stops being a description of what the system does."""

    model_config = ConfigDict(frozen=True)

    temperature: float = 0.0
    top_p: float = 1.0
    max_tokens: int = 4096


class SeamPin(BaseModel):
    """One generative seam, pinned."""

    model_config = ConfigDict(frozen=True)

    seam: str
    model_id: str
    params: SamplingParams = SamplingParams()
    prompt_version: str = "unversioned"
    #: SHA-256 of the seam's prompt text. `None` means "not yet pinned" — see the module
    #: docstring. It is never read as "any prompt is acceptable"; it is read as an
    #: assertion that has not been made.
    prompt_hash: Optional[str] = None


class ModelManifest(BaseModel):
    """Every pinned seam, plus the independent verifier model D3 requires."""

    model_config = ConfigDict(frozen=True)

    version: str
    seams: tuple[SeamPin, ...]
    #: D3 — the G3 verifier's model id. A different prompt on the same model is not
    #: independence: it shares the failure mode that produced the proposal.
    verifier_model_id: str

    @model_validator(mode="after")
    def _verifier_is_independent(self) -> "ModelManifest":
        proposers = {pin.model_id for pin in self.seams}
        if self.verifier_model_id in proposers:
            raise ValueError(
                f"D3: verifier model {self.verifier_model_id!r} is also a proposer; "
                "a verifier sharing the proposer's model shares its blind spots"
            )
        if len({pin.seam for pin in self.seams}) != len(self.seams):
            raise ValueError("a seam is pinned twice; the later pin would be invisible")
        return self

    def pin_for(self, seam: str) -> Optional[SeamPin]:
        return next((p for p in self.seams if p.seam == seam), None)


def prompt_hash(prompt_text: str) -> str:
    """SHA-256 of a prompt, whitespace-normalized at the line level.

    Trailing whitespace and line-ending differences are not prompt changes, and a hash
    that fires on them gets ignored within a week. Anything a reader would call an edit
    still changes the hash.
    """
    normalized = "\n".join(line.rstrip() for line in prompt_text.strip().splitlines())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


#: The pinned configuration. Constants in code, reviewed as a code change — the same
#: discipline D4 applies to the confidence weights, for the same reason: a value that
#: can move per run cannot anchor a regression test.
#:
#: Seam names match the `Provider` protocol in `engine/protocols.py`.
MANIFEST = ModelManifest(
    version=MANIFEST_VERSION,
    verifier_model_id="claude-sonnet-5",
    seams=(
        SeamPin(seam="expand_causal", model_id="claude-opus-5"),
        SeamPin(seam="define_axis", model_id="claude-opus-5"),
        SeamPin(seam="propose_scenarios", model_id="claude-opus-5"),
        SeamPin(seam="build_system_map", model_id="claude-opus-5"),
    ),
)


def override_enabled(env: Optional[Mapping[str, str]] = None) -> bool:
    """Is the unpinned-model override set? The only env read in this module."""
    env = os.environ if env is None else env
    return env.get(ENV_OVERRIDE) == "1"


def assert_pinned(
    seam: str,
    *,
    model_id: str,
    params: Optional[SamplingParams] = None,
    prompt_text: Optional[str] = None,
    manifest: ModelManifest = MANIFEST,
    allow_override: bool = False,
) -> SeamPin:
    """Check a live call against the manifest. Raise `ModelPinMismatch` on any drift.

    `allow_override` is a PARAMETER, not an env read, so the decision to bypass a pin is
    made at a call site a reviewer can see. Pass `override_enabled()` into it if the
    flag should govern.

    An unknown seam is a mismatch, not a pass: a seam nobody pinned is a seam nobody
    reviewed.
    """
    pin = manifest.pin_for(seam)
    problems: list[str] = []

    if pin is None:
        problems.append(f"seam {seam!r} is not pinned in manifest {manifest.version}")
    else:
        if model_id != pin.model_id:
            problems.append(
                f"model {model_id!r} != pinned {pin.model_id!r}"
            )
        if params is not None and params != pin.params:
            problems.append(f"params {params!r} != pinned {pin.params!r}")
        if prompt_text is not None and pin.prompt_hash is not None:
            actual = prompt_hash(prompt_text)
            if actual != pin.prompt_hash:
                problems.append(
                    f"prompt hash {actual[:12]} != pinned {pin.prompt_hash[:12]}"
                )

    if problems and not allow_override:
        raise ModelPinMismatch(
            f"[{manifest.version}] refusing live call for seam {seam!r}: "
            + "; ".join(problems)
            + f" (set {ENV_OVERRIDE}=1 and pass allow_override to bypass)"
        )
    return pin if pin is not None else SeamPin(seam=seam, model_id=model_id)


def assert_verifier_independent(
    proposer_model_id: str, verifier_model_id: str, manifest: ModelManifest = MANIFEST
) -> None:
    """D3 at the call site: refuse a G3 adjudication where both halves are one model."""
    if proposer_model_id == verifier_model_id:
        raise ModelPinMismatch(
            f"D3: proposer and verifier are both {proposer_model_id!r}; "
            f"the manifest pins the verifier to {manifest.verifier_model_id!r}"
        )


__all__ = [
    "ENV_OVERRIDE",
    "MANIFEST",
    "MANIFEST_VERSION",
    "ModelManifest",
    "ModelPinMismatch",
    "SamplingParams",
    "SeamPin",
    "assert_pinned",
    "assert_verifier_independent",
    "override_enabled",
    "prompt_hash",
]
