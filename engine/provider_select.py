"""Discovery provider selection + the live opt-in guard.

ScriptedProvider is the default (tests, golden cases). LLMProvider is selected explicitly
("llm"); a REAL live call (no injected client) fails closed unless ALLOW_LIVE_LLM_DISCOVERY=1.
Selection is discovery-only — expression mode never uses LLMProvider (enforced in run_workflow).
"""
from __future__ import annotations

import os
from typing import Optional

from .cases import PolicyConfig
from .llm_provider import LLMProvider
from .scripted_provider import ScriptedProvider
from .workflow import run_workflow

ENV_FLAG = "ALLOW_LIVE_LLM_DISCOVERY"


class LiveDiscoveryNotEnabled(RuntimeError):
    """Raised when a live LLM discovery run is attempted without the explicit opt-in."""


def select_discovery_provider(
    provider: str = "scripted",
    *,
    case=None,
    research_text: str = "",
    current_input_axes: Optional[list[str]] = None,
    current_sources: Optional[list[str]] = None,
    retriever=None,
    client=None,
    env: Optional[dict] = None,
):
    """Return a discovery Provider. `provider` ∈ {"scripted","llm"}.

    "llm" with a real client (client=None ⇒ build the Anthropic SDK) requires
    ALLOW_LIVE_LLM_DISCOVERY=1 — otherwise raise LiveDiscoveryNotEnabled("live_discovery_not_enabled").
    An injected (fake) client bypasses the guard so offline tests can run.
    """
    env = os.environ if env is None else env
    if provider == "scripted":
        if case is None:
            raise ValueError("scripted provider requires a `case`")
        return ScriptedProvider(case)
    if provider == "llm":
        if client is None and env.get(ENV_FLAG) != "1":
            raise LiveDiscoveryNotEnabled("live_discovery_not_enabled")
        return LLMProvider(
            client=client, research_text=research_text,
            current_input_axes=current_input_axes, current_sources=current_sources,
            retriever=retriever,
        )
    raise ValueError(f"unknown provider {provider!r} (expected 'scripted' or 'llm')")


def run_discovery(provider, policy: PolicyConfig):
    """Run DISCOVERY only through the selected provider (never expression)."""
    return run_workflow(provider, policy, mode="discovery")
