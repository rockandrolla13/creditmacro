"""Memory Access Firewall — the two-phase runner with a FROZEN SNAPSHOT between phases."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Callable, Optional

from pydantic import BaseModel, ConfigDict, model_validator

from .cases import PolicyConfig
from .memory import MemoryRetriever, WikiPage
from .protocols import Provider
from .schema import ThemeObject
from .workflow import run_workflow

# ── the frozen snapshot ───────────────────────────────────────────────────────

# Volatile identity/timestamp fields excluded from the content hash so that two runs of
# IDENTICAL fresh reasoning fingerprint equal (the hash is over CONTENT, not provenance).
_HASH_EXCLUDE = {"id": True, "created_at": True, "provenance": {"last_updated": True},
                 # forward_horizon is an additive Phase-1 field; exclude it so existing snapshot
                 # hashes stay byte-identical (the frozen causal-reasoning identity is unchanged).
                 "forward_horizon": True}

class FrozenSnapshot(BaseModel):
    """Immutable record of the phase-A fresh reasoning."""
    model_config = ConfigDict(frozen=True)
    content_hash: str
    created_at: str
    theme: ThemeObject

def _hash_theme(theme: ThemeObject) -> str:
    """SHA-256 over the CANONICAL JSON of the causal object + routed families, excluding"""
    payload = theme.model_dump(mode="json", exclude=_HASH_EXCLUDE)
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

def freeze(theme: ThemeObject, now: Optional[str] = None) -> FrozenSnapshot:
    """Freeze phase-A output into an immutable snapshot with a content hash + timestamp."""
    created_at = now if now is not None else datetime.now(timezone.utc).isoformat()
    return FrozenSnapshot(content_hash=_hash_theme(theme), created_at=created_at, theme=theme)

# ── phase-B calibration (additive; never mutates the frozen object) ───────────

class Analogue(BaseModel):
    slug: str          # the case page consulted (post-freeze)
    note: str

class ConfidenceAdjustment(BaseModel):
    """A recorded calibration of one routed family. fresh_confidence is copied from the"""
    family: str
    fresh_confidence: float
    adjusted_confidence: float
    reason: str

class PostCaseCalibration(BaseModel):
    """Additive phase-B block. References the frozen snapshot by hash so the split is"""
    fresh_snapshot_hash: str
    analogues: list[Analogue] = []
    lessons: list[str] = []
    confidence_adjustments: list[ConfidenceAdjustment] = []

# ── the emitted object: provenance of the split ───────────────────────────────

class FirewalledResult(BaseModel):
    fresh_snapshot_hash: str
    fresh_reasoning: FrozenSnapshot               # immutable phase-A reasoning
    post_case_calibration: Optional[PostCaseCalibration] = None

    @model_validator(mode="after")
    def _provenance_consistent(self) -> "FirewalledResult":
        if self.fresh_snapshot_hash != self.fresh_reasoning.content_hash:
            raise ValueError(
                "FirewalledResult: fresh_snapshot_hash must equal fresh_reasoning.content_hash."
            )
        cal = self.post_case_calibration
        if cal is not None and cal.fresh_snapshot_hash != self.fresh_snapshot_hash:
            raise ValueError(
                "FirewalledResult: post_case_calibration must reference the frozen snapshot "
                "hash (it is calibration OF the fresh reasoning, not a separate object)."
            )
        return self

# A phase-B calibrator: given the frozen snapshot + a phase-B retriever, produce additive
# calibration. Receiving the hash proves it ran AFTER the freeze.
Calibrator = Callable[[FrozenSnapshot, MemoryRetriever], PostCaseCalibration]

def default_calibrator(snapshot: FrozenSnapshot, retriever: MemoryRetriever) -> PostCaseCalibration:
    """Reference phase-B calibrator: read CASE analogues sharing a routed family, record a"""
    theme = snapshot.theme
    routed = {f.family for f in theme.strategy_families}

    analogues: list[Analogue] = []
    lessons: list[str] = []
    for slug in retriever.case_slugs():
        page = retriever.retrieve(slug)          # phase B: case pages now readable
        if page is None:
            continue
        shared = routed & set(page.frontmatter.get("strategy_families", []) or [])
        if shared:
            analogues.append(Analogue(
                slug=slug,
                note=f"prior case touching {sorted(shared)} — review how it closed before sizing.",
            ))
            lessons.append(
                f"[[{slug}]] is a prior analogue for {sorted(shared)}; calibrate, do not anchor."
            )

    adjustments = [
        ConfidenceAdjustment(
            family=f.family,
            fresh_confidence=f.confidence,
            adjusted_confidence=f.confidence,    # additive record; no silent change
            reason=("analogues found — review before sizing" if analogues
                    else "no case analogue; fresh confidence stands"),
        )
        for f in theme.strategy_families
    ]
    return PostCaseCalibration(
        fresh_snapshot_hash=snapshot.content_hash,
        analogues=analogues,
        lessons=lessons,
        confidence_adjustments=adjustments,
    )

# ── the two-phase runner ──────────────────────────────────────────────────────

def run_two_phase(
    provider: Provider,
    policy: PolicyConfig,
    pages: Optional[dict[str, WikiPage]] = None,
    *,
    retriever: Optional[MemoryRetriever] = None,
    calibrator: Optional[Calibrator] = default_calibrator,
    now: Optional[str] = None,
) -> FirewalledResult:
    """Run the firewalled two-phase pass and emit a FirewalledResult."""
    if retriever is None:
        retriever = MemoryRetriever(pages or {}, phase="A")
    if retriever.phase != "A":
        raise RuntimeError("run_two_phase requires a retriever in phase A")

    # PHASE A — fresh reasoning (the firewalled discovery path; case memory is unreachable).
    theme, _memo = run_workflow(provider, policy, mode="discovery")
    if theme.status == "expression_complete":  # defensive: the firewall never expresses
        raise RuntimeError("phase A must not produce expression_complete")

    # FREEZE — record the immutable snapshot and publish its hash to the retriever.
    snapshot = freeze(theme, now=now)
    retriever.mark_frozen(snapshot.content_hash)

    # PHASE B — only now unlock case memory, and only for additive calibration.
    retriever.advance_to_phase_b()
    calibration = calibrator(snapshot, retriever) if calibrator is not None else None

    return FirewalledResult(
        fresh_snapshot_hash=snapshot.content_hash,
        fresh_reasoning=snapshot,
        post_case_calibration=calibration,
    )
