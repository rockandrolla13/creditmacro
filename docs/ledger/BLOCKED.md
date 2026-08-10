# BLOCKED.md — decisions requiring input the ONTOLOGY does not determine

Format: ID | question | proposed resolution (implemented behind a named
constant) | affected files. Nothing here is silently chosen.

---

### B-01 — Pass B `match_confidence` calibration
**Question.** τ_ORPHAN = 0.6 gates orphan routing, but `match_confidence`
is an LLM property, not a knob. Miscalibration → everything orphans or
nothing does. What calibration target / method?
**Proposed resolution.** Implement a calibration harness over the golden
corpus; gate Pass A/B with `scripted_provider` so gates are deterministic.
Expose `MATCH_CONFIDENCE_FLOOR = τ_ORPHAN` and measure precision/recall of
routing on the golden set before trusting live values.
**Status (2026-07-09).** LLM seams wired: `LLMClaimProvider` (Pass A) and
`LLMMatchScorer` (Pass B) call `anthropic.Anthropic().messages.create`
(default `claude-opus-4-8`), gated behind `ALLOW_LIVE_LLM_DISCOVERY=1`; a real
client is built only under the opt-in, tests inject a fake client. The
StructuralSemanticMapper default scorer stays deterministic (node-Jaccard) so
gates remain LLM-free. STILL OPEN: the calibration harness measuring
match_confidence precision/recall on the golden corpus.
**Affected.** `ingest/pass_a.py`, `ingest/pass_b.py`, `ingest/prompts/`,
`llm_json.py`, `tests/golden/corpus/`.

### B-02 — Embedding provider for novelty (ν) and clustering
**Question.** §Scoring ν and §Admission clustering need sentence
embeddings + cosine (COS_NOVELTY, COS_COSMETIC). Which embedding model,
and is it available offline for deterministic gates?
**Proposed resolution.** Behind an `Embedder` protocol; a deterministic
hash-based stub embedder for gates, real model wired at runtime via
`LedgerRunConfig`. Constant names unchanged.
**Affected.** `ingest/scoring_view.py`, `ingest/admission.py`,
`wiki/wiki_import.py` (cosmetic pre-filter).

### B-03 — Tracked-axis registry contents
**Question.** WF(c) requires X ∈ tracked-axis registry, but the registry's
membership (which OAS/CDX/curve series, with which sign conventions and
data feeds) is not enumerated in the ONTOLOGY.
**Proposed resolution.** Seed `vocab.py::TRACKED_AXES` from the operational
axes already named on the 4 curated theme pages + the standard credit
indices (C0A0, H0A0, CDX.IG/HY, 3M10Y); mark it a review-gated registry
like V. Out-of-registry axis → WF(c) fail → NEEDS_STRUCTURING.
**Affected.** `vocab.py`, `substrate/identity.py` (WF).
