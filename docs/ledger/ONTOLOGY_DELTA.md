# ONTOLOGY_DELTA.md — institutional memory of design decisions

Every decision NOT directly derivable from the original ONTOLOGY, recorded
at the moment it was made. Format: ID | decision | rationale | alternatives
rejected | affected files.

---

### D-01 — Relocate the build from `src/` to `engine/ledger/`
**Decision.** The Theme Hypothesis Ledger is built as a subpackage of the
existing `engine/` tree, not the `src/themes` / `src/ingest` / `src/vocab`
layout named in BUILD_PROMPT.
**Rationale.** A `src/` twin would duplicate `schema`, the two-phase memory
firewall, `surveillance_agent`, `llm_provider`, `firewall.freeze`, and
`discovery` — producing two sources of truth for "what is a theme" that
drift. The ledger is the re-founded Stage-0/1 front end plus a temporal
lifecycle; `ThemeObject` is downstream and becomes a projection.
**Rejected.** (a) `src/` greenfield sibling — creates the twin-engine
disaster. (b) Full replacement of `engine/` — unnecessary; engines 2–4 are
sound and unchanged.
**Affected.** All Tier-1 CI grep/import paths retarget `engine/ledger/…`.

### D-02 — Tier-1 enforcement is grep + AST, not import-linter
**Decision.** The repo has no `pyproject.toml` / import-linter dependency.
I2/I3 import firewalls are enforced by an AST walk in
`tools/ledger_invariants.py`; I1/I5/I6 by grep. Runnable with stdlib only.
**Rationale.** Zero new dependencies; matches the existing `tools/leak_check.py`
style.
**Rejected.** Adding import-linter + pyproject — heavier, and the AST check
is equivalent for these contracts.
**Affected.** `tools/ledger_invariants.py`.

### D-03 — Population path is forward re-ingest (user decision, 2026-07-07)
**Decision.** The registry is rebuilt by running Pass A fresh over the
source corpus (`markdowns/`, `wiki/sources/`) → orphan pool → admission.
The 82 non-WF-surviving theme cards are discarded as themes and kept only
as provenance breadcrumbs (`wiki/breadcrumbs.py`, card→source map).
**Rationale.** WF-survival spike: 82/86 existing theme pages fail WF(a)
(k ≤ 1). Importing them would inject vibes; admission must reconstruct
themes from claims with the discipline gate applied.
**Rejected.** (a) Reuse evidence atoms as seed claims — deferred, not chosen.
(b) Treat each card as a pre-clustered claim group — risks importing vibes.
**Affected.** `ingest/pass_a.py`, `ingest/admission.py`, `wiki/wiki_import.py`
(now handles only 4 curated themes), `wiki/breadcrumbs.py`.

### D-04 — `wiki_import` scope: only the 4 WF survivors
**Decision.** `wiki_import` emits CREATED + prior-mass for exactly
`ai-capex-funding-credit-ecosystem`, `hyperscaler-project-bond-basis`,
`hy-hpc-crowding-and-supply`, `data-center-index-inclusion-technicals`.
**Rationale.** These are the only current `wiki/themes/` pages carrying a
k≥2 chain + operational axis + falsifier (the curated core-theme set).
**Affected.** `wiki/wiki_import.py`, Phase-2 gate tests.

### D-05 — ONTOLOGY amendments A1/A2/A3 + fixes F1/F2 (see ONTOLOGY.md)
**Decision.** Folded five amendments into ONTOLOGY.md: A1 vocabulary
crosswalk (V ↔ CausalNode/wiki concepts), A2 wiki-inversion scoped to
theme case pages only, A3 three-status-axis reconciliation, F1 prior-mass
is wiki-import-only (RETIRED+CREATED starts empty), F2 identity-vs-merge
tie-break.
**Rationale.** The original ONTOLOGY was written blind to `engine/`; per its
own preamble ("conflict is a bug") these reconcile it with the existing
tree and fix two internal under-specifications.
**Rejected.** Leaving them for code-time — the ONTOLOGY is the contract;
resolving in code would let deltas silently contradict it.
**Affected.** `docs/ledger/ONTOLOGY.md`, `vocab.py`, `projection.py`,
`wiki/render.py`, `substrate/fold.py`, `substrate/identity.py`.

### D-06 — ONTOLOGY constants live in `constants.py` as module-level names
**Decision.** `engine/ledger/constants.py` mirrors §Constants as
module-level named values (not a Pydantic config object). Runtime settings
(paths, provider) use a separate Pydantic `LedgerRunConfig`.
**Rationale.** §Constants mandates single-point named references and treats
a change as an ONTOLOGY edit — these are invariants, not serialisable config.
**Affected.** `constants.py`, `runner.py`.
