"""L1 — DiscoveryRunnerAgent: the registered agent now wraps engine.workflow.run_workflow.

Acceptance (plan §2 L1): the agent drives discovery through the registry, feeds the provider's
current-input seam, and returns a `strategy_family_routed` ThemeObject — never expression mode.
GM-neutral: these assert the SAME outcome the golden master already produces via run_workflow.
"""
from __future__ import annotations

from engine.case_loader import load_case
from engine.scripted_provider import ScriptedProvider
from engine.wiki_agents import (
    REGISTRY,
    DiscoveryRunnerInput,
    DiscoveryRunResult,
    run_agent,
)
from tests._helpers import CASES_DIR

JPM_DISCOVERY = CASES_DIR / "discovery" / "jpm_ai_capex.yaml"


def test_discovery_runner_routes_from_a_case_via_registry():
    case = load_case(JPM_DISCOVERY)
    res = REGISTRY.run_agent("DiscoveryRunnerAgent", DiscoveryRunnerInput(case=case))
    assert isinstance(res, DiscoveryRunResult)
    assert res.status == "strategy_family_routed"
    assert res.theme.strategy_families, "discovery must route >=1 strategy family"
    assert res.memo
    assert res.theme.status != "expression_complete"   # discovery STOP


def test_discovery_runner_accepts_provider_and_policy():
    case = load_case(JPM_DISCOVERY)
    res = run_agent("DiscoveryRunnerAgent", DiscoveryRunnerInput(
        provider=ScriptedProvider(case), policy=case.resolved_policy()))
    assert res.status == "strategy_family_routed"


def test_discovery_runner_matches_direct_run_workflow():
    # the wrapper must not alter the routed outcome vs calling run_workflow directly
    from engine.workflow import run_workflow
    case = load_case(JPM_DISCOVERY)
    direct_theme, _ = run_workflow(ScriptedProvider(case), case.resolved_policy(), mode="discovery")
    res = run_agent("DiscoveryRunnerAgent", DiscoveryRunnerInput(case=case))
    assert res.theme.status == direct_theme.status
    assert [f.family for f in res.theme.strategy_families] == \
           [f.family for f in direct_theme.strategy_families]


def test_discovery_runner_requires_input():
    import pytest
    with pytest.raises(ValueError):
        run_agent("DiscoveryRunnerAgent", DiscoveryRunnerInput())


def test_discovery_runner_listed_and_contract_valid():
    assert "DiscoveryRunnerAgent" in REGISTRY.list_agents()
    assert REGISTRY.validate_agent_contracts() == []   # no contract regressions
