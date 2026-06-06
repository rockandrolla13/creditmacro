"""
Process-backtest record (Step 5) — contract only.

ThemeOutcomeRecord persists, at thesis-open time, everything needed to later judge
whether the engine's predicted edge was real: the probabilities (p), the priced-in
measure (q), the scenario axis values (X_s), the market level (X_mkt), and the
predicted edge ± its MC std. `realized_axis_at_horizon` stays None until the thesis
closes.

This is the ONLY mechanism that eventually separates true alpha from the risk premium
the risk-neutral q is gross of (see engine2 risk caveat). The calibration and edge-
realisation analyses need a corpus of CLOSED theses, so they are documented stubs here.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional, Union


@dataclass
class ThemeOutcomeRecord:
    theme_id: str
    p: list[float]
    q: list[float]
    X_s: list[float]
    X_mkt: float
    predicted_edge: float
    edge_std: float
    realized_axis_at_horizon: Optional[float] = None


def append_outcome(record: ThemeOutcomeRecord, path: Union[str, Path]) -> None:
    """Append one record as a single JSON line (JSONL append-only store)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(asdict(record)) + "\n")


def read_outcomes(path: Union[str, Path]) -> list[ThemeOutcomeRecord]:
    """Read all records from a JSONL store."""
    path = Path(path)
    if not path.exists():
        return []
    out: list[ThemeOutcomeRecord] = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line:
            out.append(ThemeOutcomeRecord(**json.loads(line)))
    return out


# ── Calibration analytics — documented stubs (need a corpus of CLOSED theses) ──

def calibration_report(records: list[ThemeOutcomeRecord]) -> dict:
    """STUB. Compare q-implied probabilities against realised state frequencies to
    test whether the priced-in measure was well-calibrated. Needs closed theses."""
    raise NotImplementedError(
        "calibration_report needs a corpus of closed theses (realized_axis_at_horizon "
        "populated) — implemented with the data layer, not here."
    )


def edge_realization(records: list[ThemeOutcomeRecord]) -> dict:
    """STUB. Regress realised axis move on predicted_edge to estimate how much of the
    (risk-neutral) edge was true alpha vs risk premium. Needs closed theses."""
    raise NotImplementedError(
        "edge_realization needs closed theses to disentangle alpha from risk premium "
        "— implemented with the data layer, not here."
    )
