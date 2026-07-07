"""Tier-1 invariant CI harness for the Theme Hypothesis Ledger (stdlib only).

Enforces the greppable/AST invariants from docs/ledger/BUILD_PROMPT.md:

    I1  no stored theme score field in substrate/hypothesis.py
    I2  ingest/pass_a.py MUST NOT import engine.ledger.substrate  (AST)
    I3  no 'polarity' in ingest/prompts/*; no 'EvidenceLink' in pass_b prompt builders
    I5  ThemeHypothesis( constructed only in substrate/fold.py (+ tests)
    I6  no `predicted_direction` field anywhere under engine/ledger/
    I_STORE  substrate/store.py exposes no update/delete method names

Run:  python3 tools/ledger_invariants.py        (exit 1 on any violation)
This is intentionally simple and dependency-free (mirrors tools/leak_check.py).
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "engine" / "ledger"


def _fail(msg: str) -> str:
    return f"  VIOLATION: {msg}"


def check_i1() -> list[str]:
    f = LEDGER / "substrate" / "hypothesis.py"
    out = []
    for i, line in enumerate(f.read_text().splitlines(), 1):
        # a stored score field: `<name>score<name>: float`
        if re.search(r"\bscore\w*\s*:\s*float", line):
            out.append(_fail(f"I1 stored score field at hypothesis.py:{i}: {line.strip()}"))
    return out


def check_i2() -> list[str]:
    f = LEDGER / "ingest" / "pass_a.py"
    tree = ast.parse(f.read_text(), filename=str(f))
    out = []
    for node in ast.walk(tree):
        mod = None
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            # resolve relative `from ..substrate ...`
            if node.level and node.level >= 2:
                mod = "engine.ledger.substrate" if (node.module or "").startswith("substrate") else mod
        elif isinstance(node, ast.Import):
            mod = ",".join(a.name for a in node.names)
        if mod and "substrate" in mod:
            out.append(_fail(f"I2 pass_a imports substrate ('{mod}') — Pass A must be blind"))
    return out


def check_i3() -> list[str]:
    # Pass B prompt bodies (what the LLM sees) live in ingest/prompts/. Neither
    # 'polarity' (computed, never asked) nor 'EvidenceLink' (the output type) may
    # appear there. Comment lines are exempt (they document the ban itself).
    out = []
    prompts = LEDGER / "ingest" / "prompts"
    for f in prompts.rglob("*.py"):
        for i, line in enumerate(f.read_text().splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue
            for token in ("polarity", "EvidenceLink"):
                if token.lower() in line.lower():
                    out.append(_fail(f"I3 '{token}' in prompts/{f.name}:{i}"))
    return out


def check_i5() -> list[str]:
    out = []
    for f in LEDGER.rglob("*.py"):
        if f.name == "fold.py":
            continue
        for i, line in enumerate(f.read_text().splitlines(), 1):
            if "ThemeHypothesis(" in line and not line.lstrip().startswith("class "):
                out.append(_fail(f"I5 ThemeHypothesis( constructed outside fold.py: {f.relative_to(ROOT)}:{i}"))
    return out


def check_i6() -> list[str]:
    out = []
    for f in LEDGER.rglob("*.py"):
        for i, line in enumerate(f.read_text().splitlines(), 1):
            if re.search(r"predicted_direction\s*[:=]", line):
                out.append(_fail(f"I6 predicted_direction field/assign at {f.relative_to(ROOT)}:{i}"))
    return out


def check_store_append_only() -> list[str]:
    f = LEDGER / "substrate" / "store.py"
    tree = ast.parse(f.read_text(), filename=str(f))
    out = []
    banned = {"update", "delete", "remove", "set", "overwrite"}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            name = node.name.lower().lstrip("_")
            if any(name == b or name.startswith(b + "_") for b in banned):
                out.append(_fail(f"I4 store.py defines a mutating method '{node.name}'"))
    return out


CHECKS = [
    ("I1 no stored score", check_i1),
    ("I2 Pass A blind", check_i2),
    ("I3 prompts polarity-free", check_i3),
    ("I5 fold sole constructor", check_i5),
    ("I6 no predicted_direction", check_i6),
    ("I4 store append-only", check_store_append_only),
]


def main() -> int:
    violations = []
    for label, fn in CHECKS:
        found = fn()
        status = "FAIL" if found else "ok"
        print(f"[{status:4}] {label}")
        violations.extend(found)
    if violations:
        print("\n".join(violations))
        print(f"\n{len(violations)} Tier-1 violation(s).")
        return 1
    print("\nAll Tier-1 invariants hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
