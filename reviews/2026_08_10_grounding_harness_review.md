# Code Review Report

**Files reviewed:** `engine/schema/grounding.py`, `engine/grounding/__init__.py`, `engine/grounding/numbers.py`, `engine/evidence_extraction.py`, `engine/ledger/runner.py`, `engine/ledger/ingest/scoring_view.py`, `engine/ledger/substrate/store.py`, `engine/ledger/projection.py`, `engine/schema/probability.py`
**Reviewed against:** `PLAN-authoritative-harness.md` (G1–G8, I1–I8, D1–D6), `PLAN-theme-lifecycle.md` (L1–L5), `PLAN-wave1-grounding.md`
**Date:** 2026-08-10
**Overall health:** 🟡 Needs attention

## Executive Summary

The grounding kernel does what the plan asked and the fail-closed discipline is real — `enforce` blocks, verdicts are harness-authored, absence is representable. But the number tokenizer, which is now the sole authority on what figures exist in a source, **silently deletes real figures**. Any number followed by a suffix it doesn't know — `$1.1tn`, `$440bn`, `250k` — returns nothing at all. Measured: 31 such figures across eight real sources, 19 of them in a single credit research note.

That is the answer to the open question about switching to strict mode. **Do not switch yet.** In strict mode this defect turns a correctly-read claim into a halt.

Two further findings matter beyond style: the ledger projection asserts an axis is operational when it has no series at all, and `EvidenceAtom` throws away the upper half of every numeric range one line after the schema promises it won't.

## Findings

### CR-BUG-001: A figure with an unrecognised suffix is deleted, not flagged
- **Severity:** 🔴 Critical
- **Pillar:** Correctness
- **Location:** `engine/grounding/numbers.py:47`, `:61-64`

BEFORE:
```python
_BOUNDARY_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_")

def _is_embedded(text: str, start: int, end: int) -> bool:
    left_ok = start == 0 or text[start - 1] not in _BOUNDARY_CHARS
    right_ok = end == len(text) or text[end] not in _BOUNDARY_CHARS
    return not (left_ok and right_ok)
```

Measured behaviour:
```
'$1.2bn issuance'  -> []          'EUR 500mn deal' -> []
'a 250k position'  -> []          '30bn'           -> []
```

Real-corpus impact (8 files under `markdowns/`): 31 magnitude-suffixed figures dropped, 19 of
them in `79ef82a2-e1da-4bf3-9882-973affe041ae.md` alone — including `$1.1tn`, `$2.25tn`,
`$440bn`, `$35bn`, `$1.5tn`, `$1.3tn`.

AFTER:
```python
# A trailing token we do not understand is a token we must not swallow. `bn`,
# `mn`, `tn`, `k` carry a magnitude; recognise them, and let anything else that
# looks like a suffix surface as a warning rather than an empty result.
_MAGNITUDE = {"k": 1e3, "m": 1e6, "mn": 1e6, "bn": 1e9, "tn": 1e12}
```

WHY: The boundary guard exists to stop phantom numbers (`Q1`, `2022-12-28`) and it does that
well. But it cannot distinguish "this is not a number" from "this is a number wearing a hat I
don't recognise", and it treats both as silence. Because `verify_atom` uses this function as
ground truth for what a span contains, a producer that correctly reads `$440bn` gets its atom
marked **ungrounded** — a true claim rejected. Under `mode="strict"` (D2's product path) that is
a halt on correct work, which is the one failure the plan's fail-closed stance cannot absorb.

---

### CR-BUG-002: The upper half of every range is discarded at the atom boundary
- **Severity:** 🟠 Major
- **Pillar:** Correctness
- **Location:** `engine/evidence_extraction.py:248`, `engine/schema/probability.py:107`

BEFORE:
```python
nums = [n.value for n in numbers_in(sent)]   # evidence_extraction.py:248
...
numbers: list[float] = []                    # probability.py:107
```

AFTER:
```python
# Keep the token, not just its lower bound. `Number` already carries raw, unit
# and value_upper — flattening to a float here throws away all three.
numbers: list[Number] = []
```

WHY: `engine/schema/grounding.py:39-41` states *"a range is never silently flattened to a
point."* One call later it is: `"120-140bp"` becomes `[120.0]` and the 140 is gone. This also
drops the raw token and unit that D6 explicitly requires be stored **both** ways, leaving D6
satisfied inside `Number` and unsatisfied everywhere the atom actually travels.

---

### CR-BUG-003: `edges[0]` crashes on a hypothesis the same function already defends against
- **Severity:** 🟠 Major
- **Pillar:** Correctness
- **Location:** `engine/ledger/projection.py:48` (cf. `:29`)

BEFORE:
```python
name=theme.mechanism.v0 or "driver",     # line 29 — defends against empty edges
...
node_ids = [edges[0].v_from] + [e.v_to for e in edges]   # line 48 — does not
```

AFTER:
```python
if not edges:
    raise ValueError(f"theme {theme.theme_id} has no transmission edges to project")
```

WHY: `substrate/hypothesis.py:42-46` returns `None` from `v0`/`vk` when `edges` is empty, so an
edge-less mechanism is a representable state. Line 29 handles it; line 48 raises `IndexError` on
the same input. Either the state is legal and both lines must handle it, or it is illegal and it
should be refused by name, not by subscript.

---

### CR-SOLID-004: A named-only axis is asserted operational
- **Severity:** 🟠 Major
- **Pillar:** Correctness / Single Responsibility
- **Location:** `engine/ledger/projection.py:41-44`, `:59-62`

BEFORE:
```python
axis = Axis(definition=f"ledger axis {theme.operational_axis}",
            measurement=theme.operational_axis)      # no current_value, no history
...
main_theme = CausalNode(..., axis=axis, axis_operational=True)
```

AFTER:
```python
# The ledger names an axis; it has not measured one. axis_operational is a claim
# about data that exists, so it cannot be asserted from a name alone.
main_theme = CausalNode(..., axis=axis, axis_operational=False)
```

WHY: `CLAUDE.md` hard gate 1 defines operational as *"a named spread/slope with a real historical
time series."* Wave 1 correctly replaced the fabricated `0.0` levels with `None` — which makes
this line's claim provably false rather than merely unsupported. It is not cosmetic:
`workflow.py:222` passes `axis_operational` as `has_operational_axis` into strategy-family
routing, so a name-only axis routes as though it were measured.

---

### CR-BUG-005: `enforce` collapses the distinction `verify_atom` spends nine lines protecting
- **Severity:** 🟠 Major
- **Pillar:** Correctness
- **Location:** `engine/grounding/__init__.py:180-197`

BEFORE:
```python
if not verdict.is_grounded:
    bundle.rejected.append((atom, verdict))
...
return [f"ungrounded_evidence:{getattr(a, 'evidence_id', None)}: {v.reason}" ...]
```

AFTER:
```python
# unverifiable = the producer never quoted (a broken pipeline).
# ungrounded   = it quoted and the text is absent (a bad claim).
label = "unquoted_claim" if v.status == "unverifiable" else "ungrounded_evidence"
```

WHY: `verify_atom`'s own docstring says *"Collapsing them would let a producer that forgot to
quote read as a clean rejection."* `enforce` then collapses them, and labels both
`ungrounded_evidence`. An extractor emitting no quotes at all would surface as "N ungrounded
claims", pointing the operator at the source document when the fault is upstream.

---

### CR-BUG-006: The grounding mode is decided by the callee, which D2 forbids
- **Severity:** 🟠 Major
- **Pillar:** Correctness
- **Location:** `engine/evidence_extraction.py:270`

BEFORE:
```python
grounded = enforce(atoms, index, GroundingPolicy(mode="lint"))
```

AFTER:
```python
# on EvidenceExtractionInput, beside require_current_date:
grounding_mode: GroundingMode = "strict"
...
grounded = enforce(atoms, index, GroundingPolicy(mode=inp.grounding_mode))
```

WHY: D2 reads *"The mode is an explicit parameter on the grounding policy, never inferred.
Default is HALT; lint mode must be asked for."* Here no caller can ask for anything —
`extract_evidence` chooses lint for everyone, and the default is inverted.
`EvidenceExtractionInput.require_current_date` (line 40) is the same fail-closed switch done the
right way, so the pattern is already established in this file.

**Sequencing note:** this change is only safe after CR-BUG-001. Flipping to strict on the
current tokenizer halts on correctly-read claims.

---

### CR-TYPE-007: `enforce` accepts anything and passes non-models through unstamped
- **Severity:** 🟡 Minor
- **Pillar:** Types
- **Location:** `engine/grounding/__init__.py:173`, `:186-191`

BEFORE:
```python
def enforce(atoms: Sequence[Any], index: SourceIndex, ...) -> EnforcedBundle:
    ...
    copier = getattr(atom, "model_copy", None)
    bundle.kept.append(copier(update={...}) if copier else atom)
```

AFTER:
```python
class Groundable(Protocol):
    source_span: Optional[str]
    numbers: list[float]
    def model_copy(self, *, update: dict) -> "Groundable": ...
```

WHY: An object without `model_copy` is kept as *grounded* while carrying no verdict — the one
fail-open path in a module built to fail closed. The repo already uses `Protocol` structurally in
`engine/protocols.py` and `ledger/substrate/store.py`, so the idiom is at hand.

---

### CR-BUG-008: A space before the unit loses the unit
- **Severity:** 🟡 Minor
- **Pillar:** Correctness
- **Location:** `engine/grounding/numbers.py:19-45`

BEFORE:
```python
(?P<suffix> (?P<suffix_value>{_SIGNED_NUMBER}) (?P<suffix_unit>{_SUFFIX_UNIT}) )
```
`'widened 75 bp'` → `unit=None`. 307 figures across `markdowns/` are written this way.

AFTER:
```python
(?P<suffix_value>{_SIGNED_NUMBER})\s?(?P<suffix_unit>{_SUFFIX_UNIT})
```

WHY: Harmless today because `verify_atom` matches on `value` alone, which is exactly why it will
be missed until someone makes matching unit-aware — at which point 307 figures compare as
unitless against a `bp` claim.

---

### CR-STYLE-009: `ACTIVATION_ABS_SCORE_MIN` no longer describes what it gates
- **Severity:** 🟡 Minor
- **Pillar:** Style
- **Location:** `engine/ledger/runner.py:84`

BEFORE:
```python
active = sv.B >= ACTIVATION_BREADTH_MIN and sv.S >= ACTIVATION_ABS_SCORE_MIN
```

WHY: The `abs()` was removed — correctly — but the name still says absolute, which invites the
next reader to restore the symmetry it advertises. The plan barred changing the constant's
*value*; its name is a separate question. See also AR-DRY-002 in the companion architecture
review: the same rule is still stated with `|S|` in `engine/ledger/lifecycle.py`.

---

### CR-PERF-010: Every ledger query re-reads and re-parses the entire log
- **Severity:** 🟡 Minor
- **Pillar:** Performance
- **Location:** `engine/ledger/substrate/store.py:67-85`

WHY: `_read_all()` does a full file read plus `model_validate_json` per line, and both
`events_as_of` and `events_for` call it fresh. On an append-only store that grows for the life of
the system, per-query cost grows with total history. Fine now, and cheapest to cache while the
store is still small.

---

### CR-BUG-011: Invariant I8's gate command cannot fail
- **Severity:** 🟡 Minor
- **Pillar:** Correctness
- **Location:** `PLAN-authoritative-harness.md:31`

BEFORE:
```
grep -rInE "datetime\.now|..." engine/grounding.py engine/confidence.py engine/emit_gate.py → none
```
Run today: three `No such file or directory` warnings, no matches, and a reader following the
plan records "none — green".

AFTER:
```
grep -rInE "datetime\.now|date\.today|time\.time" engine/grounding/ → none
```

WHY: The module layout moved to `engine/grounding/` (AR-BND-001, recorded in the same plan at
§1), but I8 still names the pre-decision paths. The determinism invariant is currently vacuous.
The code itself is clean — there is no wall clock in `engine/grounding/` — so this costs one line
to make real.

---

### CR-BUG-012: `_doc_meta` assumes frontmatter it does not check for
- **Severity:** 🔵 Suggestion
- **Pillar:** Correctness
- **Location:** `engine/ledger/runner.py:47-49`

WHY: `.split("---", 2)[1]` raises `IndexError` and `fm["source_institution"]` raises `KeyError`
on any corpus file missing frontmatter — an unhelpful failure for what is otherwise a clear
ingestion error.

## Summary Table

| Finding ID | Severity | Pillar | Location | Finding |
|---|---|---|---|---|
| CR-BUG-001 | 🔴 Critical | Correctness | `engine/grounding/numbers.py:47,61-64` | Figures with unknown suffixes (`$440bn`) silently vanish; causes false ungrounded rejections |
| CR-BUG-002 | 🟠 Major | Correctness | `engine/evidence_extraction.py:248` | Range upper bound, raw token and unit dropped at the atom boundary (breaks D6) |
| CR-BUG-003 | 🟠 Major | Correctness | `engine/ledger/projection.py:48` | `edges[0]` IndexError on a state line 29 already guards |
| CR-SOLID-004 | 🟠 Major | Correctness | `engine/ledger/projection.py:59-62` | `axis_operational=True` asserted for an axis with no series |
| CR-BUG-005 | 🟠 Major | Correctness | `engine/grounding/__init__.py:180-197` | `enforce` collapses `unverifiable` into `ungrounded` |
| CR-BUG-006 | 🟠 Major | Correctness | `engine/evidence_extraction.py:270` | Grounding mode hardcoded to lint; D2 requires a caller-supplied strict default |
| CR-TYPE-007 | 🟡 Minor | Types | `engine/grounding/__init__.py:173` | `Sequence[Any]` lets a non-model pass through unstamped |
| CR-BUG-008 | 🟡 Minor | Correctness | `engine/grounding/numbers.py:19-45` | `"75 bp"` loses its unit (307 occurrences in corpus) |
| CR-STYLE-009 | 🟡 Minor | Style | `engine/ledger/runner.py:84` | `ACTIVATION_ABS_SCORE_MIN` name outlived the `abs()` |
| CR-PERF-010 | 🟡 Minor | Performance | `engine/ledger/substrate/store.py:67-85` | Full log re-parsed on every query |
| CR-BUG-011 | 🟡 Minor | Correctness | `PLAN-authoritative-harness.md:31` | I8 gate names non-existent paths; invariant cannot fail |
| CR-BUG-012 | 🔵 Suggestion | Correctness | `engine/ledger/runner.py:47-49` | Frontmatter parsed without checking it exists |

## Positive Highlights

1. **The fail-closed rule is tested as a blocker, not a warning.** `test_grounding_enforce.py:91`
   asserts strict mode *raises*. The plan's definition-of-done item 5 asks for exactly this, and
   it is the item most projects skip.
2. **Absence is genuinely representable now.** Replacing the fabricated `0.0` levels in
   `projection.py` with `None` was the right call and the comment explains why in terms of what a
   reader would wrongly conclude — which is what makes it hold up under later edits.
3. **The `bps`-before-`bp` ordering comment** (`numbers.py:15-18`) explains a first-match hazard
   that would otherwise look like arbitrary ordering. That is the comment a future editor needs
   and would not have written.

## Handoff

| Severity | Pillar | Location | Finding | Finding ID |
|---|---|---|---|---|
| 🔴 Critical | Correctness | `engine/grounding/numbers.py:47,61-64` | Figures with unrecognised suffixes silently vanish; false ungrounded rejections | CR-BUG-001 |
| 🟠 Major | Correctness | `engine/evidence_extraction.py:248` | Range upper bound, raw token and unit dropped at atom boundary; breaks D6 | CR-BUG-002 |
| 🟠 Major | Correctness | `engine/ledger/projection.py:48` | IndexError on edge-less mechanism the same function elsewhere guards | CR-BUG-003 |
| 🟠 Major | Correctness | `engine/ledger/projection.py:59-62` | `axis_operational=True` for an axis with no measured series | CR-SOLID-004 |
| 🟠 Major | Correctness | `engine/grounding/__init__.py:180-197` | `unverifiable` collapsed into `ungrounded` | CR-BUG-005 |
| 🟠 Major | Correctness | `engine/evidence_extraction.py:270` | Grounding mode hardcoded to lint; D2 requires strict default | CR-BUG-006 |
| 🟡 Minor | Types | `engine/grounding/__init__.py:173` | Non-model atoms pass through unstamped | CR-TYPE-007 |
| 🟡 Minor | Correctness | `engine/grounding/numbers.py:19-45` | Space-separated units lost (307 corpus occurrences) | CR-BUG-008 |
| 🟡 Minor | Style | `engine/ledger/runner.py:84` | Constant name outlived the `abs()` it described | CR-STYLE-009 |
| 🟡 Minor | Performance | `engine/ledger/substrate/store.py:67-85` | Whole log re-parsed per query | CR-PERF-010 |
| 🟡 Minor | Correctness | `PLAN-authoritative-harness.md:31` | I8 gate paths do not exist; invariant cannot fail | CR-BUG-011 |
| 🔵 Suggestion | Correctness | `engine/ledger/runner.py:47-49` | Frontmatter parsed unguarded | CR-BUG-012 |
