"""G8 — the brief gate. **SCAFFOLD ONLY (Phase 3). Not implemented.**

Every function raises `NotImplementedError`. The schema it gates
(`engine/schema/source_brief.py`) is real; the behaviour is not.

**Why a stub.** G8 has two halves and only one of them is deterministic. The gate below
could be written today. The WRITER cannot: it needs a live model producing 3-5 bullets
over a closed atom vocabulary, and the bounded re-ask in step 5 is a live-call protocol,
not a pure function. Shipping the gate alone would leave a checker with nothing to check
and a second, dormant definition of the brief format to drift against the writer that
eventually arrives. Shipping a fake writer would be worse: a brief that passed a gate
fed by invented bullets is precisely the unsourced paragraph G8 exists to stop, now
wearing a passing verdict.

**The contract, fixed here so both halves are built against it.**

`assert_brief_grounded(brief, atoms, index)` checks, in order:

1. every referenced `atom_id` exists in the KEPT set for that (source, theme) pair;
2. every NUMBER in the brief text appears in a referenced atom's verified numbers
   (via `engine.grounding.numbers.numbers_in`) — no new figures at summary time;
3. every named ENTITY in the brief appears in a referenced atom's `entities` — no new
   names;
4. bullet count, total word count and per-bullet word count within
   `engine/schema/source_brief.py`'s constants;
5. one bounded re-ask on failure; a second failure DROPS the brief and the theme carries
   `brief_status="unavailable"`.

Checks 2 and 3 are the load-bearing ones. Formatting is what a model gets right; a
number or a name that was not in any atom is what it gets wrong, and both are invisible
to a reader who cannot see the atom set.

**Composes with:** G1/G2 (the atom set), G4 (its confidence — the harness's, never the
model's), G5 (structurally immune: the writer never sees raw source text), G6 (a brief
is a `synthesis` node, so the emit gate's stricter every-parent-grounded rule already
applies).
"""
from __future__ import annotations

from typing import Any, Iterable, Optional, Sequence

from engine.schema.source_brief import SourceThemeBrief

_PHASE = "G8 — Phase 3 (source-to-theme brief)"


class BriefRejected(RuntimeError):
    """A brief failed the gate. After the bounded re-ask this means the brief is
    dropped, not repaired — `brief_status="unavailable"` beats an ungated paragraph."""


def assert_brief_grounded(
    brief: SourceThemeBrief,
    atoms: Sequence[Any],
    index: Any,
) -> None:
    """Run the five checks above. Raise `BriefRejected` on the first failure.

    Not implemented — see the module docstring.
    """
    raise NotImplementedError(f"{_PHASE}: the brief writer does not exist yet")


def write_brief(
    source_slug: str,
    theme_id: str,
    atoms: Sequence[Any],
    provider: Any,
    *,
    reask_limit: int = 1,
) -> Optional[SourceThemeBrief]:
    """Closed-vocabulary brief writer: sees ONLY `atoms`, never the raw markdown.

    Returns `None` when the brief is dropped after the bounded re-ask — the caller sets
    `brief_status="unavailable"`.

    Not implemented — see the module docstring.
    """
    raise NotImplementedError(f"{_PHASE}: needs a live model over a closed atom vocabulary")


def brief_numbers(brief: SourceThemeBrief) -> Iterable[float]:
    """Every numeric token in the brief's text, for check 2.

    Not implemented — see the module docstring. It would be a thin wrapper over
    `engine.grounding.numbers.numbers_in`, and writing it before the writer exists would
    fix a tokenizing decision no brief has yet exercised.
    """
    raise NotImplementedError(f"{_PHASE}: no briefs exist to tokenize")


__all__ = ["BriefRejected", "assert_brief_grounded", "brief_numbers", "write_brief"]
