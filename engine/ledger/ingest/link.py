"""EvidenceLink — output of Pass B mapping (ONTOLOGY §EvidenceLink).

Frozen, append-only. `polarity` is COMPUTED (claim.direction × d(θ)), never
emitted by an LLM (I3). Corrections are new rows with `supersedes` set (I4).
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional, Sequence

from pydantic import BaseModel, ConfigDict


class EvidenceLink(BaseModel):
    model_config = ConfigDict(frozen=True)

    link_id: str
    theme_id: str
    theme_revision: int                  # fold count at mapping time
    claim_id: str
    polarity: int                        # ∈ {-1, 0, +1} = claim.direction × d(θ) × sign(X)
    match_confidence: float              # ∈ [0, 1]
    recorded_at: Optional[str] = None    # set by the link store (I7)
    supersedes: Optional[str] = None     # link_id | None


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class JsonlEvidenceLinkStore:
    """Append-only JSONL link store (I4), mirroring substrate.store.JsonlEventStore.
    recorded_at stamped here only (I7). No update/delete path exists. Corrections are
    new rows with `supersedes` set."""

    def __init__(self, path: str, *, clock: Callable[[], str] = _utc_now_iso) -> None:
        self._path = Path(path)
        self._clock = clock

    def append(self, link: EvidenceLink) -> EvidenceLink:
        stamped = link.model_copy(update={"recorded_at": self._clock()})
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a") as f:
            f.write(stamped.model_dump_json() + "\n")
        return stamped

    def _read_all(self) -> list[EvidenceLink]:
        if not self._path.exists():
            return []
        return [EvidenceLink.model_validate_json(ln) for ln in self._path.read_text().splitlines() if ln.strip()]

    def links_for(self, theme_id: str) -> Sequence[EvidenceLink]:
        return [l for l in self._read_all() if l.theme_id == theme_id]

    def all_links(self) -> Sequence[EvidenceLink]:
        return self._read_all()
