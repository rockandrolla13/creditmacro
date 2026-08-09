# Code Review Report

**Files reviewed:** `engine/firewall.py`, `engine/workflow.py`, `engine/evidence_extraction.py`,
`engine/llm_provider.py`, `engine/schema/` — the integration points that
`PLAN-authoritative-harness.md` and `PLAN-theme-lifecycle.md` will modify
**Date:** 2026-08-09
**Overall health:** 🟡 Needs attention — the code is well-factored, but its documentation was
damaged by an LOC-reduction pass, and one plan estimate does not survive contact with it

**Companion:** `reviews/2026_08_09_architecture_review.md` (system structure and blast radius).

## Executive Summary

The integration points are small, single-purpose and well-factored; `firewall.py` in particular
enforces its own invariant rather than trusting callers. Two findings matter. First, the June
shrink to hit a −20% LOC target truncated 24 docstrings mid-sentence across `engine/`, including
the one documenting the hash-exclusion contract that invariant I6 of both plans depends on — the
lost text is recoverable verbatim from commit `ed57d5a`. Second, `PLAN-authoritative-harness.md`
costs G1 as "Effort M · Risk low" on the premise that span offsets are trivially available from
`_iter_sentences`; that function discards position information three times over and splits
sentences at line boundaries, so the premise is false. Top priority: restore the docstrings
(mechanical, zero design risk) and re-scope G1 before Phase 1 begins.

## Findings

### CR-STYLE-001: 24 docstrings were truncated mid-sentence by the LOC shrink

- **Severity:** 🟠 Major
- **Pillar:** Style / Conciseness misapplied
- **Location:** `engine/` — 24 sites, incl. `firewall.py:33,49,56,88`, `cases.py:51,165,180,186`,
  `memory.py:17,111`, `discovery.py:183`, `engine2.py:132`, `example.py:87`, `outcomes.py:41`

BEFORE (`engine/firewall.py:33`, today):
```python
def _hash_theme(theme: ThemeObject) -> str:
    """SHA-256 over the CANONICAL JSON of the causal object + routed families, excluding"""
```

AFTER (the text as it stood at `ed57d5a`, recoverable verbatim):
```python
def _hash_theme(theme: ThemeObject) -> str:
    """SHA-256 over the CANONICAL JSON of the causal object + routed families, excluding
    volatile id/timestamps (`_HASH_EXCLUDE`) so identical reasoning hashes equal across runs."""
```

WHY: `PLAN-engine-shrink.md` step 5.1 collapsed multi-line docstrings to one-liners, taking the
first *physical line* rather than the first *sentence*. Every docstring whose opening sentence
wrapped was cut. The plan records this as *"only inline docstrings were collapsed to one-line
summaries"* and *"design narrative preserved"* — but a truncation is not a summary. The specific
casualty above is the sentence explaining **why** the content hash excludes fields, which is
precisely the mechanism invariant I6 relies on in both current plans. A reader arriving at
Phase 1 finds the word "excluding" and no object.

### CR-BUG-001: G1's span-offset premise is false, and the tokenizer splits sentences at line breaks

- **Severity:** 🟠 Major
- **Pillar:** Correctness
- **Location:** `engine/evidence_extraction.py:170-180`; claim at
  `PLAN-authoritative-harness.md:112-115`

BEFORE:
```python
def _iter_sentences(md: str):
    for raw_line in md.splitlines():          # position lost
        for sent in re.split(r"(?<=[.;])\s+", raw_line.strip()):   # and again
            s = sent.strip()                  # and again
            yield page, s                     # text only — no offsets
```

AFTER (sketch — derive offsets in the kernel, not the producer):
```python
# Producer emits the verbatim quote only:
EvidenceAtom(..., source_span=s)
# SourceIndex.find_span(quote) -> (start, end)   # already specified by the plan
```

WHY: The plan states offsets are *"trivial for the rule extractor — `_iter_sentences` already
walks the text; capture each sentence's offsets."* It does not walk positions: `splitlines()`,
`raw_line.strip()`, a lookbehind `re.split`, and a second `sent.strip()` each discard a variable
amount, so offsets cannot be recovered without rewriting the generator. The plan already
specifies `SourceIndex.find_span(quote) -> Optional[tuple[int, int]]`; letting the kernel locate
a producer-supplied quote removes the need for producer-side offsets entirely, and is the only
path that works for an LLM extractor anyway — a model cannot report byte offsets reliably.

Separately, splitting on lines *before* sentences means a sentence wrapped across two lines
yields two fragments. Those fragments still match as verbatim substrings, so grounding succeeds,
but the span is half a sentence and therefore weaker evidence than intended.
`[SUGGEST: add a test for a sentence wrapped across a line break, asserting what span is recorded]`

### CR-STYLE-002: Confidence literals are unnamed magic numbers

- **Severity:** 🟡 Minor
- **Pillar:** Style
- **Location:** `engine/evidence_extraction.py:241, 262, 339`

BEFORE:
```python
confidence=0.8,     # :241
confidence=0.5,     # :262
confidence=0.5,     # :339
```

AFTER:
```python
_RULE_EXTRACTED_CONFIDENCE = 0.8   # named, with the reason it is not 1.0
_UNSCORED_CONFIDENCE = 0.5
```

WHY: Three bare literals encoding a policy decision, with nothing naming what they mean or why
they differ. This independently confirms G4's diagnosis — *"`EvidenceAtom.confidence` defaults to
`0.5` and seam confidences are author-set — the false-precision trap"* — against the real code.
Naming them is worth doing now because G4 will replace them, and the replacement is easier to
review when the thing being replaced has a name.

### CR-BUG-002: `run_two_phase` silently ignores `pages` when a retriever is supplied

- **Severity:** 🟡 Minor
- **Pillar:** Correctness
- **Location:** `engine/firewall.py:138-139`

BEFORE:
```python
if retriever is None:
    retriever = MemoryRetriever(pages or {}, phase="A")
```

AFTER (sketch):
```python
if retriever is not None and pages is not None:
    raise ValueError("pass pages or retriever, not both — pages would be ignored")
```

WHY: Both parameters are optional and public, and supplying both silently discards one. In a
function whose entire purpose is enforcing the memory firewall, quietly dropping a caller's page
set is the wrong failure mode — the caller believes they constrained what phase A could see.

## Summary Table

| Finding ID | Severity | Pillar | Location | Finding |
|---|---|---|---|---|
| CR-STYLE-001 | 🟠 Major | Style | `engine/` ×24 | Docstrings truncated mid-sentence by the LOC shrink; recoverable from `ed57d5a` |
| CR-BUG-001 | 🟠 Major | Correctness | `evidence_extraction.py:170-180` | G1's "trivial offsets" premise is false; tokenizer also splits sentences at line breaks |
| CR-STYLE-002 | 🟡 Minor | Style | `evidence_extraction.py:241,262,339` | Unnamed confidence literals (confirms G4's diagnosis) |
| CR-BUG-002 | 🟡 Minor | Correctness | `firewall.py:138-139` | `pages` silently ignored when `retriever` is given |

## Positive Highlights

**`FirewalledResult._provenance_consistent` (`firewall.py:70-82`) validates its own invariant.**
It refuses construction unless the calibration references the frozen snapshot's hash — the
two-phase split cannot be faked by a caller assembling the object by hand. That is the right
place for that check.

**`_call_json` already separates channels.** Instructions go in `system`, content in the `user`
message (`llm_provider.py:105-109`). G5 is hardening a partial separation rather than inventing
one, which makes it a smaller change than the plan implies.

**Both plans' diagnoses check out against the real code.** G4's false-precision claim and G5's
injection surface are exactly as described. The design documents were written by someone who
read this code, which is rarer than it should be — and is why CR-BUG-001 is worth flagging
rather than assuming.

## Handoff

| Severity | Pillar | Location | Finding | Finding ID |
|---|---|---|---|---|
| 🟠 Major | Style | `engine/` ×24 sites | Docstrings truncated mid-sentence by the −20% LOC shrink, including the hash-exclusion contract that invariant I6 depends on; original text recoverable verbatim from commit `ed57d5a` | CR-STYLE-001 |
| 🟠 Major | Correctness | `engine/evidence_extraction.py:170-180` | `_iter_sentences` discards position three times, so G1's "trivial offsets" premise fails; it also splits sentences at line breaks, yielding fragment spans | CR-BUG-001 |
| 🟡 Minor | Style | `engine/evidence_extraction.py:241,262,339` | Bare confidence literals `0.8`/`0.5`/`0.5` encode policy with no name or rationale | CR-STYLE-002 |
| 🟡 Minor | Correctness | `engine/firewall.py:138-139` | `pages` is silently discarded when `retriever` is also supplied, in the function that enforces the memory firewall | CR-BUG-002 |
