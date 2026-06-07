"""Guard-rail tests for scoring/loader edge cases (CR-PERF-001, CR-TYPE-001)."""
from __future__ import annotations

import typing

import pytest

from engine.case_loader import resolve_prior
from engine.scoring import compute_omega


def test_compute_omega_rejects_empty_series():
    with pytest.raises((ValueError, ZeroDivisionError)):
        compute_omega([])


def test_resolve_prior_type_hints_resolve():
    # Optional must be importable in case_loader, else get_type_hints raises NameError.
    hints = typing.get_type_hints(resolve_prior)
    assert "hist_freq" in hints
