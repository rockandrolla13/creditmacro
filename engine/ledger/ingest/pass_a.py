"""Pass A — BLIND claim extraction (ONTOLOGY §AtomicClaim, invariant I2).

The extractor sees ONLY the document. The theme registry is unreachable BY
CONSTRUCTION: this module imports vocab (METHOD memory) + constants + claim only,
never `engine.ledger.substrate` (enforced by tools/ledger_invariants.py).

Two layers (mirrors the repo's provider seam):
  - ClaimProvider   : doc → raw claim proposals (LLM for prose, or scripted for
                      deterministic gates / offline runs).
  - PassAExtractor  : the tested production logic — validate schema domains, keep
                      only in-vocabulary tags (out-of-vocab → review), enforce
                      granularity (one claim per market_variable × direction ×
                      horizon), assign deterministic claim_ids.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, Sequence

import yaml

from .. import vocab                     # METHOD memory — allowed
from ..constants import CONVICTION_LEVELS, DIRECTIONS
from ..llm_json import LEDGER_MODEL, extract_text, parse_json_object
from .claim import AtomicClaim
from .prompts.pass_a_extract import EXTRACT_PROMPT, EXTRACT_SYSTEM

LIVE_ENV_FLAG = "ALLOW_LIVE_LLM_DISCOVERY"   # shared live-LLM opt-in with the engine


class ClaimProvider(Protocol):
    """Proposes raw claim dicts for a document. Blind to the theme registry."""
    def propose(self, doc_id: str, text: str, source_institution: str,
                doc_date: str) -> list[dict]: ...


@dataclass(frozen=True)
class PassAResult:
    claims: list[AtomicClaim]
    out_of_vocab_tags: list[str] = field(default_factory=list)   # → review queue
    rejected: list[dict] = field(default_factory=list)           # schema-invalid, dropped


class ScriptedClaimProvider:
    """Reads the golden corpus's `claims:` frontmatter block. Deterministic."""

    def __init__(self, corpus_dir: str | Path) -> None:
        self._dir = Path(corpus_dir)

    def propose(self, doc_id: str, text: str, source_institution: str,
                doc_date: str) -> list[dict]:
        fm = yaml.safe_load((self._dir / f"{doc_id}.md").read_text().split("---", 2)[1])
        return list(fm.get("claims", []))


class LLMClaimProvider:
    """Prose → raw claim proposals via the Anthropic Messages API (B-01).

    Blind: sees only the document + the vocabulary (METHOD memory). A real client
    is built only under the LIVE_ENV_FLAG opt-in; tests inject a fake client.
    """

    def __init__(self, client=None, *, model: str = LEDGER_MODEL, max_tokens: int = 4096) -> None:
        self._client = client
        self._model = model
        self._max_tokens = max_tokens

    def _get_client(self):
        if self._client is None:
            if os.environ.get(LIVE_ENV_FLAG) != "1":
                raise RuntimeError(f"live LLM not enabled (set {LIVE_ENV_FLAG}=1)")
            import anthropic
            self._client = anthropic.Anthropic()
        return self._client

    def propose(self, doc_id: str, text: str, source_institution: str,
                doc_date: str) -> list[dict]:
        user = EXTRACT_PROMPT.format(
            doc_id=doc_id, institution=source_institution, doc_date=doc_date,
            vocab=", ".join(sorted(vocab.NODES)), text=text,
        )
        response = self._get_client().messages.create(
            model=self._model, max_tokens=self._max_tokens, system=EXTRACT_SYSTEM,
            messages=[{"role": "user", "content": user}],
        )
        return list(parse_json_object(extract_text(response)).get("claims", []))


class PassAExtractor:
    """Provider-agnostic Pass-A logic. Blind by construction (I2)."""

    def __init__(self, provider: ClaimProvider) -> None:
        self._provider = provider

    def extract(self, doc_id: str, text: str, *, source_institution: str,
                doc_date: str) -> PassAResult:
        raws = self._provider.propose(doc_id, text, source_institution, doc_date)

        groups: dict[tuple, dict] = {}          # (market_variable, direction, horizon) → agg
        oov: list[str] = []
        rejected: list[dict] = []

        for raw in raws:
            direction = raw.get("direction")
            conviction = raw.get("stated_conviction")
            if direction not in DIRECTIONS or conviction not in CONVICTION_LEVELS:
                rejected.append(raw)
                continue

            kept: list[str] = []
            for tag in raw.get("mechanism_tags", []):
                (kept if vocab.is_node(tag) else oov).append(tag)

            key = (raw["market_variable"], direction, raw["horizon_days"])
            if key in groups:                    # granularity: merge same-tuple claims
                g = groups[key]
                g["tags"].update(kept)
                g["conviction"] = max(g["conviction"], conviction)
            else:
                groups[key] = {"tags": set(kept), "conviction": conviction,
                               "text": raw.get("text", "")}

        claims: list[AtomicClaim] = []
        for i, (key, g) in enumerate(groups.items()):
            market_variable, direction, horizon = key
            claims.append(AtomicClaim(
                claim_id=f"{doc_id}-{i:03d}", doc_id=doc_id,
                source_institution=source_institution, doc_date=doc_date,
                text=g["text"], market_variable=market_variable, direction=direction,
                horizon_days=horizon, stated_conviction=g["conviction"],
                mechanism_tags=tuple(sorted(g["tags"])),
            ))

        return PassAResult(claims=claims, out_of_vocab_tags=sorted(set(oov)), rejected=rejected)
