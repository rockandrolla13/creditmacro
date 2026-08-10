"""Deterministic text similarity (embedder seam; a real embedding model is wired at
runtime per BLOCKED B-02). Bag-of-words cosine — used by the wiki-revision cosmetic
pre-filter (§Event) and the §Scoring novelty discount. Single source of truth so the
two call sites cannot drift.
"""
from __future__ import annotations

import math
from collections import Counter


def bow_cosine(a: str, b: str) -> float:
    ta, tb = Counter(a.lower().split()), Counter(b.lower().split())
    keys = set(ta) | set(tb)
    dot = sum(ta[k] * tb[k] for k in keys)
    na = math.sqrt(sum(v * v for v in ta.values()))
    nb = math.sqrt(sum(v * v for v in tb.values()))
    return dot / (na * nb) if na and nb else 0.0
