"""
Typed contracts for the source compiler. REUSES the firewall vocabulary from
engine.memory (does NOT fork it). These models are additive — the pipeline never
imports engine runtime, only the access_class constant, so the golden master is safe.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, field_validator

from engine.memory import VALID_ACCESS_CLASSES

SourceTypeT = Literal[
    "book", "paper", "report", "deck", "memo", "transcript", "market_data", "other"
]
MaturityT = Literal["active", "next", "schema_only", "deferred", "not_built"]


# ── PDF → normalized-md manifest (lives in raw/manifests/) ───────────────────

class ConversionManifest(BaseModel):
    slug: str
    source_pdf: str
    sha256: str
    n_pages: int
    engine: str                              # "pymupdf4llm" | "pdftotext"
    page_anchors: list[int]                  # page numbers emitted as <!-- page:N -->
    low_confidence_pages: list[int] = []
    table_heavy_pages: list[int] = []
    image_heavy_pages: list[int] = []
    assets: list[str] = []
    tables: list[str] = []
    created_at: str


# ── wiki/sources frontmatter (validated before writing the card) ─────────────

class SourceFrontmatter(BaseModel):
    type: Literal["source"] = "source"
    title: str
    slug: str
    access_class: str                        # method | case — the firewall key
    source_type: SourceTypeT
    aliases: list[str] = []
    tags: list[str] = []
    sources: list[str] = []
    status: Literal["draft", "active", "stub", "deprecated"] = "draft"
    source_date: Optional[str] = None
    author_or_publisher: Optional[str] = None
    raw_source_path: Optional[str] = None    # path into raw/ (immutable)
    ingestion_status: Literal["draft", "ingested", "linted"] = "draft"
    copyright: bool = True                    # True → paraphrase-only + leak-checked
    created: Optional[str] = None
    updated: Optional[str] = None

    @field_validator("access_class")
    @classmethod
    def _valid_access_class(cls, v: str) -> str:
        if v not in VALID_ACCESS_CLASSES:
            raise ValueError(f"access_class must be one of {VALID_ACCESS_CLASSES}, got {v!r}")
        return v


# ── evidence atoms (wiki/evidence/evidence_atoms.jsonl) ──────────────────────

class EvidenceAtom(BaseModel):
    evidence_id: str
    source_slug: str
    source_location: str                     # "page:N" / section anchor — REQUIRED, non-empty
    claim_type: str
    claim: str
    entities: list[str] = []
    concepts: list[str] = []
    themes: list[str] = []
    market_variables: list[str] = []
    numbers: list[float] = []
    causal_edges: list[dict] = []
    confidence: float = 0.5
    freshness: Optional[str] = None
    agent_use: str = ""
    is_synthesis: bool = False               # False = source fact; True = agent synthesis (labeled)

    @field_validator("source_location")
    @classmethod
    def _non_empty_location(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("source_location is required (e.g. 'page:3')")
        return v


# ── method cards (wiki/process) and engine specs (wiki/engines) ──────────────

class MethodCard(BaseModel):
    skill_name: str
    theoretical_source: str
    mathematical_primitive: str
    software_primitive: str
    pipeline_phase: str
    input_objects: list[str] = []
    output_objects: list[str] = []
    gates_created: list[str] = []
    confidence_effect: str = ""
    failure_modes: list[str] = []
    non_goals: list[str] = []
    test_requirements: list[str] = []
    implementation_maturity: MaturityT


class EngineSpec(BaseModel):
    engine_name: str
    maturity: MaturityT
    implements: str = ""                      # engine/ module.symbol it maps to (doc link)
    inputs: list[str] = []
    outputs: list[str] = []
    gates: list[str] = []
    depends_on: list[str] = []
    test_ref: str = ""
    non_goals: list[str] = []
