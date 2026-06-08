"""Live-run capture + deterministic replay.

When LLMProvider runs live, write a PRIVATE (gitignored) run record under
runs/live_discovery/. It stores validated JSON outputs + memory-access audit + the snapshot
hash — never full copyrighted source text (only input_hash + source slugs). A captured record
can be REPLAYED through the engine validators with no LLM call (deterministic), and may become
a fixture only after human approval.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from .schema import Axis, BiasCritique, LoopDiagnosis, SystemMap

# validated-output key → engine schema to revalidate against on replay
_REPLAY_SCHEMAS = {"axis": Axis, "system_map": SystemMap,
                   "loop_diagnosis": LoopDiagnosis, "bias_critique": BiasCritique}


def input_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


class LiveRunRecord(BaseModel):
    run_id: str
    timestamp: str                      # caller-supplied (deterministic; no Date.now here)
    model_name: str
    provider: str = "llm"
    input_hash: str
    source_slugs: list[str] = []
    method_pages_read: list[str] = []
    case_pages_refused: list[str] = []
    prompt_names: list[str] = []
    validated_outputs: dict = {}        # seam → schema-valid JSON (e.g. {"axis": {...}})
    validation_errors: list[str] = []
    blocked_status: Optional[str] = None
    snapshot_hash: Optional[str] = None
    final_strategy_families: list[str] = []
    no_trade_confirmation: bool = True  # no legs / sizing / hedge ratios emitted


def write_run_record(record: LiveRunRecord, base_dir: str = "runs/live_discovery",
                     slug: str = "run") -> Path:
    """Write the record to runs/live_discovery/<timestamp>-<slug>.json (gitignored)."""
    out_dir = Path(base_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = record.timestamp.replace(":", "").replace("-", "").replace("T", "-")[:15]
    path = out_dir / f"{stamp}-{slug}.json"
    path.write_text(record.model_dump_json(indent=2), encoding="utf-8")
    return path


def replay(path) -> LiveRunRecord:
    """Load a captured record (re-validates the record schema). No LLM call. Deterministic."""
    return LiveRunRecord(**json.loads(Path(path).read_text(encoding="utf-8")))


def revalidate(record: LiveRunRecord) -> list[str]:
    """Re-run the engine schema validators over the captured validated_outputs, with NO LLM.
    Returns a list of validation errors (empty ⇒ the captured outputs still validate)."""
    errors: list[str] = []
    for key, schema in _REPLAY_SCHEMAS.items():
        if key in record.validated_outputs:
            try:
                schema(**record.validated_outputs[key])
            except Exception as exc:
                errors.append(f"{key}: {exc}")
    return errors
