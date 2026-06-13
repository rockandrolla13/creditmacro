"""ForwardHorizon — the 3-4 month window a theme is given at discovery (Phase 1, §3.2).

A leaf schema module (pydantic + datetime only) so both `ThemeObject` (engine.schema.theme) and the
surveillance core (engine.surveillance) can import it without a circular dependency. The single
number every surveillance clock keys off is `window_days`; `opened`/`expected_close` are
caller-supplied (no wall-clock).
"""
from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class ForwardHorizon(BaseModel):
    opened: date                 # discovery date
    expected_close: date         # opened + window
    window_label: str            # "3w" | "6w" | "3m" | "4m" | ...
    window_days: int             # derived; the clock key
