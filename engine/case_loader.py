"""Case loading — read a YAML/JSON case file into a typed CaseSpec and resolve the"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Union

import yaml

from .cases import CaseSpec

def resolve_prior(
    prior: Union[list[float], str],
    n: int,
    hist_freq: Optional[list[Optional[float]]] = None,
) -> list[float]:
    """Resolve a prior specification to a length-n probability vector."""
    if prior == "uniform":
        return [1.0 / n] * n
    if prior == "historical":
        if hist_freq is None or any(h is None for h in hist_freq):
            raise ValueError(
                "prior='historical' requires every scenario to set hist_freq"
            )
        if len(hist_freq) != n:
            raise ValueError(
                f"hist_freq length {len(hist_freq)} != number of scenarios {n}"
            )
        total = float(sum(hist_freq))  # type: ignore[arg-type]
        if total <= 0:
            raise ValueError("hist_freq must sum to a positive value")
        return [float(h) / total for h in hist_freq]  # type: ignore[arg-type]
    if isinstance(prior, (list, tuple)):
        vec = [float(x) for x in prior]
        if len(vec) != n:
            raise ValueError(
                f"prior vector length {len(vec)} != number of scenarios {n}"
            )
        return vec
    raise ValueError(f"unrecognised prior specification: {prior!r}")

def load_case(path: Union[str, Path]) -> CaseSpec:
    """Read a case file, validate it into a CaseSpec, and resolve its prior."""
    path = Path(path)
    raw = path.read_text()
    data = json.loads(raw) if path.suffix == ".json" else yaml.safe_load(raw)

    cs = CaseSpec.model_validate(data)
    hist_freq = [s.hist_freq for s in cs.scenarios]
    resolved = resolve_prior(cs.prior, n=len(cs.scenarios), hist_freq=hist_freq)
    return cs.model_copy(update={"prior": resolved})
