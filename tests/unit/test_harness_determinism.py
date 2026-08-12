"""Invariant I8, made non-vacuous.

`PLAN-authoritative-harness.md` §0 states I8 as a shell grep over `engine/grounding.py`,
`engine/confidence.py` and `engine/emit_gate.py`. None of those paths exists — the layout
moved to the `engine/grounding/` package (`docs/SPEC_AND_STATE.md` §4.6), so the grep
matches nothing, produces no output, and reads as green. It has never been able to fail.

This file is the invariant as a test instead of as a shell line, which is strictly
better: it enumerates the package rather than a fixed list of filenames, so a module
added tomorrow is covered without anyone remembering to extend a grep.

**Why it matters.** A confidence that quietly means "as of whenever this ran" is a fact
about the process wearing the clothes of a fact about the evidence, and a provenance
record that changes between two replays of the same input is not provenance. `now` and
`current_date` are parameters everywhere in this package.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

_ENGINE = Path(__file__).resolve().parents[2] / "engine"
_HARNESS_DIR = _ENGINE / "grounding"

#: The modules I8 is about: the grounding kernel plus everything G3-G8 added.
_HARNESS_MODULES = sorted(p for p in _HARNESS_DIR.glob("*.py"))
#: Their schema contracts, which must not default a timestamp either.
_HARNESS_SCHEMAS = [
    _ENGINE / "schema" / name
    for name in ("grounding.py", "confidence.py", "provenance.py", "source_brief.py")
]

_WALL_CLOCK = re.compile(r"\bdatetime\.now\b|\bdate\.today\b|\btime\.time\b|\butcnow\b")


def _offending_lines(path: Path) -> list[str]:
    return [
        f"{path.name}:{i}: {line.strip()}"
        for i, line in enumerate(path.read_text().splitlines(), start=1)
        if _WALL_CLOCK.search(line) and not line.lstrip().startswith("#")
    ]


def test_the_module_list_is_not_empty():
    """The failure mode this whole file exists to prevent: a check over nothing."""
    assert len(_HARNESS_MODULES) >= 8
    assert all(p.exists() for p in _HARNESS_SCHEMAS)


@pytest.mark.parametrize("path", _HARNESS_MODULES + _HARNESS_SCHEMAS,
                         ids=lambda p: p.name)
def test_no_wall_clock_in_the_grounding_harness(path):
    assert not _offending_lines(path), (
        f"{path} reads the wall clock; `now` must be a parameter (I8)"
    )


def test_the_detector_would_actually_catch_a_violation(tmp_path):
    """A guard nobody has seen fail is a guard nobody should trust."""
    planted = tmp_path / "planted.py"
    planted.write_text("from datetime import datetime\nstamp = datetime.now()\n")
    assert _offending_lines(planted)


def test_the_provenance_migration_supplies_no_default_timestamp():
    """The same rule in SQL: `created_at` has no DEFAULT, so a replay is byte-identical."""
    from engine.grounding.provenance_ledger import MIGRATIONS_DIR

    sql = (MIGRATIONS_DIR / "0003_provenance_ledger.sql").read_text().lower()
    assert "created_at       text not null," in sql
    assert "default (datetime('now'))" not in sql
