"""
LLMProvider — the generative counterpart to ScriptedProvider.

For now it carries the EXPAND_CAUSAL system prompt (the generic skill-card payload).
The live model call is NOT wired in this milestone: expand_causal builds the messages
and raises NotImplementedError at the API boundary, so the contract (same shape as
ScriptedProvider.expand_causal) is fixed and the prompt is inspectable/testable. The
stage references NO specific case or issuer — only the domain-agnostic prompt.
"""
from __future__ import annotations

from .prompts import CAUSAL_EXPANDER_PROMPT


class LLMProvider:
    """Carries the generic causal-expander prompt. Other Provider seams are wired in a
    later milestone; this class exists to fix the expand_causal contract + prompt."""

    def __init__(self, system_prompt: str = CAUSAL_EXPANDER_PROMPT) -> None:
        self.system_prompt = system_prompt

    def expand_causal(self, research_text: str, parsed_theme: str):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Research text:\n{research_text}\n\nParsed theme: {parsed_theme}"},
        ]
        raise NotImplementedError(
            "LLMProvider.expand_causal: live model call not wired in this milestone. "
            "Messages are prepared; connect the LLM client and parse the JSON response "
            f"into (CausalNode, CausalChain, str). ({len(messages)} messages prepared.)"
        )
