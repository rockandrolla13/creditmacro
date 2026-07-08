# SIGN_AUDIT.md — scheduled firewall-inversion hunt (post-Phase-4)

**Scope:** every site in `engine/ledger/` that computes a direction, polarity, or
sign product, verified against `d(θ) = σ·Πs` (ONTOLOGY §Theme) and the polarity
rule. **Date:** 2026-07-08. **Overall:** 🟡 one spec/code inconsistency to fix
(the code is correct; the ONTOLOGY shorthand is not), one minor robustness gap.

## Enumeration of sign sites

| # | Site | Computes | Verified against | Verdict |
|---|------|----------|------------------|---------|
| 1 | `substrate/hypothesis.py:48` `Mechanism.sign_product()` | `Π_j s_j` | §Theme | ✅ correct |
| 2 | `substrate/hypothesis.py:86` `derived_direction()` | `σ · Πs` | `d(θ)=σ·Πs` | ✅ exact |
| 3 | `substrate/identity.py:36` `equiv()` | sign-product equality | §Identity (ii) | ✅ correct |
| 4 | `substrate/identity.py:65` `wf_predicate` clause e | `stated_dir == d(θ)` | I8e | ✅ correct |
| 5 | `substrate/identity.py:77` `classify_event` | σ-flip → RETIRE+CREATE | §Event | ✅ correct |
| 6 | `ingest/pass_b.py:58` `polarity()` | `dir × d(θ) × sign(X)` | §EvidenceLink / §Theme d_X | ⚠️ **CR-BUG-001** |
| 7 | `wiki/wiki_import.py:110` `replay()` | σ-flip → RETIRE+CREATE | §Event | ✅ correct |
| 8 | `vocab.py:137` `axis_sign()` | `sign(X)` lookup | §Theme | ⚠️ **CR-BUG-002** (robustness) |

Six of eight sites are exactly correct. The two flagged are below.

## Findings

### CR-BUG-001: ONTOLOGY §EvidenceLink polarity formula omits `sign(X)`
- **Severity:** 🟠 Major (latent inversion trap)
- **Pillar:** Correctness
- **Location:** `ingest/pass_b.py:56-58` vs `docs/ledger/ONTOLOGY.md` §EvidenceLink

BEFORE (ONTOLOGY §EvidenceLink):
```
polarity = claim.direction × d(θ)
```
BEFORE (code, `pass_b.py:58`):
```python
return claim.direction * derived_direction(definition) * vocab.axis_sign(definition.operational_axis)
```

WHY: The two disagree. §Theme itself defines the predicted **axis** direction as
`d_X(θ) = d(θ)·sign(X)`, and the `test_axis_flip_remap` gate proves polarity must
carry `sign(X)` — an inverted-convention axis (e.g. `IG_EXCESS_RETURN`, sign −1)
flips every stored polarity, which is exactly why AXIS_REVISED mandates a remap. The
**code is correct**; the ONTOLOGY §EvidenceLink shorthand is the bug. Anyone
re-implementing from the literal shorthand would silently invert polarity on any
inverted-convention axis and every downstream `S_θ` sign would be wrong.
**Fix:** amend ONTOLOGY §EvidenceLink to `polarity = claim.direction × d(θ) × sign(X)`
and record the convention (polarity is stored in the operational-axis frame) in
ONTOLOGY_DELTA D-07. No code change.

### CR-BUG-002: `polarity()` KeyErrors on an axis outside the tracked registry
- **Severity:** 🟡 Minor (robustness / clarity of precondition)
- **Pillar:** Correctness
- **Location:** `ingest/pass_b.py:58` → `vocab.py:137` `axis_sign`

BEFORE:
```python
return claim.direction * derived_direction(definition) * vocab.axis_sign(definition.operational_axis)
# axis_sign -> TRACKED_AXES[axis_id].sign  → raises KeyError if X ∉ registry
```
WHY: WF clause (c) guarantees `X ∈ tracked-axis registry` for **admitted** themes, but
`polarity()` can be called with any `ThemeDefinitionView` (WF is not enforced at this
call site). An untracked axis yields an uncaught `KeyError` rather than a clear
contract error. **Fix:** make the precondition explicit — raise a descriptive error
(or route the definition to NEEDS_STRUCTURING upstream). Low-risk; add a guard.

### Convention note (not a defect): uniform `sign(X)`
`polarity()` applies `sign(X)` to **every** claim, including those whose
`market_variable` is the vk rather than the axis. This is a deliberate convention —
evidence polarity is stored in the **operational-axis frame** (what the Breach Buffer
observes), so a vk-measured claim's stored polarity is expressed on the theme's axis.
Consequence: the same vk-claim mapped to two themes measured on opposite-sign axes
carries opposite stored polarity — correct under axis-frame semantics. This must be
stated explicitly in the ONTOLOGY (folded into the D-07 amendment) so it is a chosen
convention, not an accident.

## Positive highlights
- `sign_product` and `derived_direction` mirror `d(θ)=σ·Πs` exactly.
- Polarity is **computed**, never LLM-emitted (I3); the `test_axis_flip_remap` gate
  and the manual "null `axis_sign`" probe both confirm `sign(X)` is load-bearing.
- Identity/event classification consistently routes σ-flips and sign-product changes
  to RETIRE+CREATE, never to a silent mutation.

## Handoff

| Severity | Pillar | Location | Finding | Finding ID |
|----------|--------|----------|---------|------------|
| 🟠 Major | Correctness | `ONTOLOGY.md §EvidenceLink` vs `pass_b.py:58` | polarity formula omits sign(X); code correct, spec wrong | CR-BUG-001 |
| 🟡 Minor | Correctness | `pass_b.py:58` / `vocab.py:137` | `polarity()` KeyErrors on untracked axis (WF precondition not enforced at call site) | CR-BUG-002 |

**Resolution (applied this checkpoint):** CR-BUG-001 → amend ONTOLOGY §EvidenceLink +
ONTOLOGY_DELTA D-07 (spec fix, no behaviour change). CR-BUG-002 → add an explicit
guard in `axis_sign`/`polarity`. Both applied before proceeding to Phase 5.
