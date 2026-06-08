"""Live discovery harness — the single entry point that runs discovery with an automatic
semantic-contract gate BEFORE freezing a FreshReasoningSnapshot.

Order: select provider (live opt-in guard) → run discovery → AUTOMATIC validation → on any
violation FAIL CLOSED (capture the violation, do NOT freeze) → otherwise freeze the snapshot
and write a private capture record. Discovery only; no propose_scenario_candidates here.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from .capture import LiveRunRecord, input_hash, write_run_record
from .cases import PolicyConfig
from .firewall import FrozenSnapshot, freeze
from .provider_select import run_discovery, select_discovery_provider
from .schema import ThemeObject
from .semantic_contract import InputKind, validate_discovery_output

_PROMPT_NAMES = ["expand_causal", "define_axis", "build_system_map",
                 "diagnose_loops", "critique_mental_model"]


class SemanticContractViolation(RuntimeError):
    """Raised when a live discovery output fails the automatic semantic contract — fail
    closed: the snapshot is NOT frozen. Carries the violations and the captured record."""
    def __init__(self, violations: list[str], record: "LiveRunRecord"):
        self.violations = violations
        self.record = record
        super().__init__("semantic_contract_violation: " + "; ".join(violations))


@dataclass
class LiveDiscoveryResult:
    theme: ThemeObject
    snapshot: Optional[FrozenSnapshot]
    record: LiveRunRecord
    violations: list[str]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _validated_outputs(theme: ThemeObject) -> dict:
    out: dict = {}
    if theme.axis is not None:
        out["axis"] = theme.axis.model_dump()
    if theme.system_map is not None:
        out["system_map"] = theme.system_map.model_dump()
    if theme.loop_diagnosis is not None:
        out["loop_diagnosis"] = theme.loop_diagnosis.model_dump()
    if theme.bias_critique is not None:
        out["bias_critique"] = theme.bias_critique.model_dump()
    return out


def run_live_discovery(
    *,
    research_text: str,
    current_input_axes: Optional[list[str]] = None,
    current_sources: Optional[list[str]] = None,
    retriever=None,
    client=None,
    env: Optional[dict] = None,
    input_kind: Optional[InputKind] = None,
    policy: Optional[PolicyConfig] = None,
    capture: bool = True,
    capture_dir: str = "runs/live_discovery",
    slug: str = "adhoc",
    timestamp: Optional[str] = None,
    freeze_snapshot: bool = True,
) -> LiveDiscoveryResult:
    """Run live discovery with the automatic contract gate. Fails closed on violations."""
    provider = select_discovery_provider(
        "llm", research_text=research_text, current_input_axes=current_input_axes,
        current_sources=current_sources, retriever=retriever, client=client, env=env,
    )
    theme, _memo = run_discovery(provider, policy or PolicyConfig())

    # ── AUTOMATIC semantic-contract validation — BEFORE any snapshot ────────
    violations = validate_discovery_output(theme, input_kind=input_kind)

    mlog = getattr(provider, "memory_log", {})
    ts = timestamp or _now()
    record = LiveRunRecord(
        run_id=f"live-{input_hash(research_text)}", timestamp=ts,
        model_name=getattr(provider, "model", "n/a"), provider="llm",
        input_hash=input_hash(research_text), source_slugs=list(current_sources or []),
        method_pages_read=mlog.get("method_pages_read", []),
        case_pages_refused=mlog.get("case_pages_refused", []),
        prompt_names=_PROMPT_NAMES, validated_outputs=_validated_outputs(theme),
        validation_errors=violations, blocked_status=theme.block_reason,
        final_strategy_families=[f.family for f in theme.strategy_families],
        no_trade_confirmation=(theme.pricing is None and theme.sizing is None
                               and not theme.expressions),
    )

    if violations:                                   # FAIL CLOSED — never freeze a bad output
        if capture:
            write_run_record(record, base_dir=capture_dir, slug=slug)
        raise SemanticContractViolation(violations, record)

    snapshot = freeze(theme, now=ts) if freeze_snapshot else None
    if snapshot is not None:
        record.snapshot_hash = snapshot.content_hash
    if capture:
        write_run_record(record, base_dir=capture_dir, slug=slug)
    return LiveDiscoveryResult(theme=theme, snapshot=snapshot, record=record, violations=[])
