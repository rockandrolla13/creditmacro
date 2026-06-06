"""expand_causal seam: the generic skill-card prompt, ScriptedProvider returning a
hand-built chain from the CaseSpec, and the LLMProvider stub carrying the prompt."""
from __future__ import annotations

from pathlib import Path

import pytest

from engine.case_loader import load_case
from engine.cases import CausalPayload
from engine.prompts import CAUSAL_EXPANDER_PROMPT
from engine.schema import Axis, AxisHistory, CausalChain, CausalEdge, CausalNode
from engine.scripted_provider import ScriptedProvider

CASES = Path(__file__).resolve().parents[2] / "cases"


def _payload():
    axis = Axis(definition="A OAS − B OAS, bps", measurement="daily, bps",
                current_value=40.0,
                history=AxisHistory(mean=70.0, vol=30.0, percentile=10.0, regime_tags=["x"]))
    main = CausalNode(id="n_main", statement="tradeable theme", kind="theme",
                      axis=axis, axis_operational=True)
    chain = CausalChain(
        nodes=[CausalNode(id="n0", statement="driver", kind="cause"), main],
        edges=[CausalEdge(from_id="n0", to_id="n_main", mechanism="transmission", inferred=False)],
    )
    return CausalPayload(main_theme=main, causal_chain=chain, shared_factor="latent factor")


def test_scripted_provider_returns_payload_when_present():
    case = load_case(CASES / "french_banks.yaml").model_copy(update={"causal": _payload()})
    main, chain, factor = ScriptedProvider(case).expand_causal("text", "theme")
    assert isinstance(main, CausalNode) and main.kind == "theme"
    assert isinstance(chain, CausalChain) and len(chain.nodes) == 2
    assert factor == "latent factor"


def test_scripted_provider_returns_none_without_payload():
    case = load_case(CASES / "ai_issuance.yaml")  # no causal payload
    main, chain, factor = ScriptedProvider(case).expand_causal("text", "theme")
    assert main is None and chain is None and factor is None


def test_prompt_enforces_domain_agnostic_hard_rules():
    p = CAUSAL_EXPANDER_PROMPT.lower()
    # the causal ladder
    for term in ["association", "intervention", "counterfactual", "assumption"]:
        assert term in p
    # systems structure (Meadows)
    for term in ["feedback", "delay", "stock", "flow", "mediator"]:
        assert term in p
    # the standing confounder must be named
    assert "risk premium" in p and "spread" in p
    # hard structural rules
    assert "one main theme" in p or "one main_theme" in p
    assert "depth-first" in p
    assert "operational" in p and "axis" in p
    assert "dead end" in p and "never invent" in p
    assert "inferred" in p and "feedback" in p
    assert "shared_factor" in p and "non_identifiability" in p
    # emits exactly the three fields
    assert "main_theme" in p and "causal_chain" in p


def test_llm_provider_carries_prompt_and_stubs_live_call():
    from engine.llm_provider import LLMProvider

    prov = LLMProvider()
    assert prov.system_prompt is CAUSAL_EXPANDER_PROMPT
    with pytest.raises(NotImplementedError):
        prov.expand_causal("some research text", "a theme")
