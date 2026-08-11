"""Orchestration: doc → Pass A → Pass B → cluster → admit → score → activate.

Reuses the phase modules. `forward_ingest` is the population path (D-03): Pass A over
the corpus, Pass B against existing definitions, orphan clustering + admission rebuild
the registry. Runtime settings live in a Pydantic LedgerRunConfig (D-06), distinct from
the ONTOLOGY constants in constants.py.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

import yaml
from pydantic import BaseModel

from .constants import ACTIVATION_ABS_SCORE_MIN, ACTIVATION_BREADTH_MIN
from .ingest.admission import admit, cluster_orphans
from .ingest.pass_a import PassAExtractor, ScriptedClaimProvider
from .ingest.pass_b import StructuralSemanticMapper
from .ingest.scoring_view import score
from .substrate.hypothesis import ThemeDefinitionView


class LedgerRunConfig(BaseModel):
    corpus_dirs: tuple[Path, ...]
    events_store: Path = Path("data/ledger/events.jsonl")
    links_store: Path = Path("data/ledger/links.jsonl")
    provider: str = "scripted"
    embedder: str = "hash_stub"


@dataclass(frozen=True)
class AdmittedTheme:
    theme_id: str
    status: str                        # ACTIVE | CANDIDATE


@dataclass
class RegistryState:
    admitted: list[AdmittedTheme] = field(default_factory=list)
    orphan_claim_ids: list[str] = field(default_factory=list)
    needs_structuring: list[str] = field(default_factory=list)
    review_tags: list[str] = field(default_factory=list)


def _doc_meta(corpus_dir: Path, doc_id: str) -> dict:
    fm = yaml.safe_load((corpus_dir / f"{doc_id}.md").read_text().split("---", 2)[1])
    return {"source_institution": fm["source_institution"], "doc_date": str(fm["doc_date"])}


def forward_ingest(
    doc_ids: Sequence[str],
    corpus_dir: Path,
    existing_definitions: Sequence[ThemeDefinitionView] = (),
    theme_revisions: dict[str, int] | None = None,
) -> RegistryState:
    """Full forward-reingest pass over a corpus. Deterministic; returns the end-state."""
    extractor = PassAExtractor(ScriptedClaimProvider(corpus_dir))
    claims = []
    review_tags: set[str] = set()
    for doc_id in doc_ids:
        m = _doc_meta(corpus_dir, doc_id)
        res = extractor.extract(doc_id, text="", source_institution=m["source_institution"],
                                doc_date=m["doc_date"])
        claims.extend(res.claims)
        review_tags.update(res.out_of_vocab_tags)

    # Pass B against existing themes; unmatched claims fall to the orphan pool.
    mapped = StructuralSemanticMapper().map(claims, existing_definitions, theme_revisions or {})
    orphans = mapped.orphans

    admitted: list[AdmittedTheme] = []
    orphan_ids: list[str] = []
    needs: list[str] = []
    for cluster in cluster_orphans(orphans):
        out = admit(cluster)
        cluster_ids = [c.claim_id for c in cluster.claims]
        if out.status == "admitted":
            claims_by_id = {c.claim_id: c for c in cluster.claims}
            as_of = max(c.doc_date for c in cluster.claims)
            sv = score(out.theme_id, as_of, list(out.founding_links), claims_by_id,
                       horizon_days=out.definition.horizon_days)
            # §Lifecycle: B_θ ≥ 2 ∧ |S_θ| ≥ 2. The ABSOLUTE value is load-bearing —
            # S_θ < 0 with no breach is CONTESTED (a sub-state of ACTIVE), not dead
            # (§Theme "Interpretation", §Lifecycle; ONTOLOGY_DELTA D-09).
            active = sv.B >= ACTIVATION_BREADTH_MIN and abs(sv.S) >= ACTIVATION_ABS_SCORE_MIN
            admitted.append(AdmittedTheme(out.theme_id, "ACTIVE" if active else "CANDIDATE"))
        elif out.status == "needs_structuring":
            needs.extend(cluster_ids)
        else:                                      # rejected_gate | out_of_vocab → stays orphan
            if out.status == "out_of_vocab":
                review_tags.update(out.review_tags)
            orphan_ids.extend(cluster_ids)

    return RegistryState(
        admitted=sorted(admitted, key=lambda a: a.theme_id),
        orphan_claim_ids=sorted(orphan_ids),
        needs_structuring=sorted(needs),
        review_tags=sorted(review_tags),
    )
