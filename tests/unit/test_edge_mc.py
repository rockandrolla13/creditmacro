"""Tests for engine.engine2.compute_edge_mc — Monte-Carlo edge.

Key invariant: edge_mean is the DETERMINISTIC identity ⟨p−q,X⟩ at the point
estimates, NOT the MC sample mean. MC supplies only edge_std / SNR / P(success) /
infeasible_fraction. Draws are seeded with SeedSequence so results are reproducible
and order-independent (AR-PAR-001).
"""
from __future__ import annotations

import math

import pytest

from engine.engine2 import (
    EdgeMC,
    compute_edge,
    compute_edge_mc,
    level_constraint,
    solve_q_tilt,
)
from engine.schema import EdgeContribution

# AI-issuance
P = [0.40, 0.35, 0.15, 0.10]
X = [95.0, 75.0, 45.0, 40.0]
XMKT = 55.0
UNIFORM = [0.25, 0.25, 0.25, 0.25]
NAMES = ["AI Surge", "Base", "Risk-Off", "Capex Pause"]
ZERO = [0.0, 0.0, 0.0, 0.0]


def _mc(sigma=ZERO, thesis_sign=1, sigma_axis=15.0, n=2000, seed=0, kappa=1e6):
    return compute_edge_mc(
        p=P, X_s=X, sigma_g=sigma, X_mkt=XMKT, prior=UNIFORM,
        thesis_sign=thesis_sign, sigma_axis=sigma_axis,
        n_draws=n, kappa=kappa, seed=seed, scenario_names=NAMES,
    )


def test_returns_edge_mc():
    assert isinstance(_mc(), EdgeMC)


def test_edge_mean_is_the_deterministic_identity():
    res = _mc()
    q = solve_q_tilt(X, [level_constraint(XMKT)], UNIFORM).q
    identity = compute_edge(P, q, X)
    assert res.edge_mean == pytest.approx(identity, abs=1e-12)
    assert res.edge_mean == pytest.approx(20.0, abs=1e-6)  # the golden edge


def test_no_uncertainty_gives_tiny_std_and_large_snr():
    # σ_g=0 and high κ → near-deterministic draws → edge_std → 0, SNR → large
    res = _mc(sigma=ZERO, kappa=1e6)
    assert res.edge_std < 0.1
    assert res.snr > 100.0


def test_reproducible_with_same_seed():
    a = _mc(seed=7)
    b = _mc(seed=7)
    assert a.edge_std == b.edge_std
    assert a.snr == b.snr
    assert a.p_success == b.p_success


def test_different_seed_changes_the_sample():
    a = _mc(sigma=[10.0, 10.0, 10.0, 10.0], seed=1)
    b = _mc(sigma=[10.0, 10.0, 10.0, 10.0], seed=2)
    assert a.edge_std != b.edge_std  # different draws


def test_attribution_is_typed_sorted_and_names_the_top_scenario():
    res = _mc()
    assert all(isinstance(c, EdgeContribution) for c in res.attribution)
    contribs = [c.contribution for c in res.attribution]
    assert contribs == sorted(contribs, reverse=True)
    # edge comes from the AI-Surge state being under-weighted by the market
    assert res.attribution[0].scenario == "AI Surge"
    # contributions reconstruct the edge identity
    assert sum(contribs) == pytest.approx(20.0, abs=1e-6)


def test_direction_flag():
    assert _mc(thesis_sign=1).direction_ok is True
    assert _mc(thesis_sign=-1).direction_ok is False


def test_vol_adjusted_edge():
    res = _mc(sigma_axis=10.0)
    assert res.vol_adjusted_edge == pytest.approx(res.edge_mean / 10.0, abs=1e-9)


def test_infeasible_draws_are_counted_not_dropped_silently():
    # scenarios clustered just below X_mkt; with noise many draws fail to span 55
    res = compute_edge_mc(
        p=[0.25, 0.25, 0.25, 0.25],
        X_s=[50.0, 52.0, 54.0, 56.0],
        sigma_g=[5.0, 5.0, 5.0, 5.0],
        X_mkt=55.0,
        prior=UNIFORM,
        thesis_sign=1,
        sigma_axis=5.0,
        n_draws=1500,
        seed=0,
    )
    assert 0.0 < res.infeasible_fraction < 1.0


def test_p_success_in_unit_interval():
    res = _mc(sigma=[8.0, 8.0, 8.0, 8.0])
    assert 0.0 <= res.p_success <= 1.0
