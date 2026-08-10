"""Single Python mirror of ONTOLOGY §Constants — referenced by name everywhere.

Changing any value here is an ONTOLOGY change: it requires an edit to
`docs/ledger/ONTOLOGY.md` §Constants plus an `ONTOLOGY_DELTA.md` entry. Never
override these locally in another module (Tier-1 discipline; see BUILD_PROMPT).
"""
from __future__ import annotations

from datetime import timedelta

# ── admission / well-formedness ───────────────────────────────────────────────
H_MAX = timedelta(days=120)          # WF(d): forward-horizon ceiling
N_MIN = 3                            # §Admission: min claims to promote a cluster
I_MIN = 2                            # §Admission: min distinct institutions
W_ADMIT = timedelta(days=30)        # §Admission: max doc-date span of a cluster

# ── identity / revision ───────────────────────────────────────────────────────
J_MERGE = 0.5                       # §Identity: edge-Jaccard merge threshold
COS_COSMETIC = 0.92                 # §Event: wiki-revision cosmetic pre-filter
COS_NOVELTY = 0.88                  # §Scoring: same-institution novelty cutoff

# ── scoring ───────────────────────────────────────────────────────────────────
NOVELTY_DISCOUNT = 0.15             # ν_i when a same-institution repeat is detected
CAP_INST = 3                        # per-institution net contribution clip (± )
SCORE_CLIP = 10                     # S_θ clipped to [-SCORE_CLIP, +SCORE_CLIP]
LAMBDA = 0.5                        # decay base; half-life h = H/2 ⇒ λ = 1/2
TAU_ORPHAN = 0.6                    # §EvidenceLink: below → orphan pool

# ── activation gate (§Lifecycle: CANDIDATE → ACTIVE) ──────────────────────────
ACTIVATION_BREADTH_MIN = 2          # B_θ ≥ 2
ACTIVATION_ABS_SCORE_MIN = 2        # |S_θ| ≥ 2

# ── conviction / direction domains (validation helpers) ───────────────────────
CONVICTION_LEVELS = (1, 2, 3)       # stated_conviction ∈ {1,2,3}; s_prior ∈ same
DIRECTIONS = (-1, 0, 1)             # claim.direction ∈ {-1,0,+1}
SHOCK_DIRECTIONS = (-1, 1)          # σ ∈ {-1,+1}


def half_life(horizon: timedelta) -> timedelta:
    """h = H/2 — the evidence half-life keyed to the theme's forward horizon."""
    return horizon / 2
