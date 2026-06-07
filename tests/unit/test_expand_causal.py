"""expand_causal seam: the generic skill-card prompt, ScriptedProvider returning a"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine.case_loader import load_case
from engine.cases import CausalPayload
from engine.prompts import CAUSAL_EXPANDER_PROMPT
from engine.schema import Axis, AxisHistory, CausalChain, CausalEdge, CausalNode
from engine.scripted_provider import ScriptedProvider

CASES = Path(__file__).resolve().parents[2] / "cases"

def test_llm_provider_is_a_causal_expander_not_a_full_provider():
    from engine.llm_provider import LLMProvider
    from engine.protocols import CausalExpander, Provider
    p = LLMProvider(client=object())
    assert isinstance(p, CausalExpander)      # satisfies the narrow seam it implements
    assert not isinstance(p, Provider)        # but cannot drive run_workflow (one seam only)

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

# ── a VALID causal JSON object (one cause node, one operational theme node, one edge) ──

def _valid_causal_obj() -> dict:
    return {
        "main_theme": {
            "id": "n_theme",
            "statement": "hyperscaler IG curve steepens",
            "kind": "theme",
            "axis": {
                "definition": "hyperscaler IG OAS - duration-matched IG index OAS, bps",
                "measurement": "daily close, bps, Bloomberg",
                "current_value": 12.0,
                "history": {"mean": 8.0, "vol": 5.0, "percentile": 75.0,
                            "regime_tags": ["expansion"]},
            },
            "axis_operational": True,
        },
        "causal_chain": {
            "nodes": [
                {"id": "n_cause", "statement": "AI capex surge drives bond supply",
                 "kind": "cause", "axis": None, "axis_operational": False},
                {
                    "id": "n_theme",
                    "statement": "hyperscaler IG curve steepens",
                    "kind": "theme",
                    "axis": {
                        "definition": "hyperscaler IG OAS - duration-matched IG index OAS, bps",
                        "measurement": "daily close, bps, Bloomberg",
                        "current_value": 12.0,
                        "history": {"mean": 8.0, "vol": 5.0, "percentile": 75.0,
                                    "regime_tags": ["expansion"]},
                    },
                    "axis_operational": True,
                },
            ],
            "edges": [
                {"from_id": "n_cause", "to_id": "n_theme",
                 "mechanism": "supply pushes spreads wider at the long end",
                 "inferred": True, "feedback": False},
            ],
        },
        "shared_factor": "AI-capex credit risk premium",
    }

class _FakeContentBlock:
    """Mirrors a real SDK text content block: .type == 'text', .text holds the string."""
    def __init__(self, text: str) -> None:
        self.type = "text"
        self.text = text

class _FakeResponse:
    """Mirrors anthropic Message: .content is a list of content blocks."""
    def __init__(self, text: str) -> None:
        self.content = [_FakeContentBlock(text)]

class _FakeMessages:
    def __init__(self, text: str, calls: list) -> None:
        self._text = text
        self._calls = calls

    def create(self, **kwargs):
        self._calls.append(kwargs)
        return _FakeResponse(self._text)

class _FakeClient:
    """Injected stand-in for anthropic.Anthropic() — exposes client.messages.create."""
    def __init__(self, text: str) -> None:
        self.calls: list = []
        self.messages = _FakeMessages(text, self.calls)

# ── ScriptedProvider contract (unchanged) ────────────────────────────────────

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

# ── LIVE LLMProvider — construction needs NO api key (lazy client) ────────────

def test_llm_provider_constructs_without_api_key(monkeypatch):
    """Constructing must never build a client or need a key — the client is lazy."""
    from engine.llm_provider import LLMProvider

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    prov = LLMProvider()  # must not raise even with no key in the environment
    assert prov.system_prompt is CAUSAL_EXPANDER_PROMPT

# ── LIVE LLMProvider — parse + validate via an injected fake client ───────────

def test_expand_causal_happy_path_parses_and_validates():
    from engine.llm_provider import LLMProvider

    fake = _FakeClient(json.dumps(_valid_causal_obj()))
    prov = LLMProvider(client=fake)
    main, chain, factor = prov.expand_causal("AI issuance steepens IG curves", "AI theme")

    assert isinstance(main, CausalNode)
    assert main.kind == "theme"
    assert main.axis_operational is True and main.axis is not None
    assert isinstance(chain, CausalChain) and len(chain.nodes) == 2
    assert factor == "AI-capex credit risk premium"
    # main_theme id is present among the chain nodes
    assert main.id in {n.id for n in chain.nodes}

    # the SDK was called with system=CAUSAL_EXPANDER_PROMPT and a user message
    assert len(fake.calls) == 1
    call = fake.calls[0]
    assert call["system"] is CAUSAL_EXPANDER_PROMPT
    assert call["messages"][0]["role"] == "user"
    assert "AI issuance steepens IG curves" in call["messages"][0]["content"]

def test_expand_causal_robust_to_fences_and_prose():
    from engine.llm_provider import LLMProvider

    wrapped = (
        "Sure! Here is the causal object you asked for:\n\n"
        "```json\n" + json.dumps(_valid_causal_obj()) + "\n```\n"
        "Let me know if you need anything else."
    )
    prov = LLMProvider(client=_FakeClient(wrapped))
    main, chain, factor = prov.expand_causal("text", "theme")
    assert isinstance(main, CausalNode) and main.kind == "theme"
    assert isinstance(chain, CausalChain)
    assert factor == "AI-capex credit risk premium"

def test_expand_causal_raises_valueerror_on_non_json():
    from engine.llm_provider import LLMProvider

    prov = LLMProvider(client=_FakeClient("I cannot help with that request."))
    with pytest.raises(ValueError):
        prov.expand_causal("text", "theme")

def test_expand_causal_rejects_theme_node_without_axis():
    """Bad LLM output (a theme node with axis=null) must NOT enter the engine —"""
    from engine.llm_provider import LLMProvider

    bad = _valid_causal_obj()
    # break the theme node: declare kind=theme but null axis
    for node in bad["causal_chain"]["nodes"]:
        if node["id"] == "n_theme":
            node["axis"] = None
            node["axis_operational"] = False
    bad["main_theme"]["axis"] = None
    bad["main_theme"]["axis_operational"] = False

    prov = LLMProvider(client=_FakeClient(json.dumps(bad)))
    with pytest.raises(ValueError):
        prov.expand_causal("text", "theme")
