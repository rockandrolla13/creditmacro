"""LLMProvider — the LIVE generative counterpart to ScriptedProvider."""
from __future__ import annotations

import json
from typing import Optional

from .prompts import CAUSAL_EXPANDER_PROMPT
from .schema import CausalChain, CausalNode

# Current Claude 4.x model id, verified from the claude-api reference (Models table).
# Sonnet 4.6 is the structured-extraction-appropriate default for this JSON-extraction
# task; override via the constructor for a different model.
_DEFAULT_MODEL = "claude-sonnet-4-6"
_DEFAULT_MAX_TOKENS = 4096

class LLMProvider:
    """Generative EXPAND_CAUSAL seam backed by the Anthropic Messages API."""

    def __init__(
        self,
        client=None,
        model: str = _DEFAULT_MODEL,
        max_tokens: int = _DEFAULT_MAX_TOKENS,
        system_prompt: str = CAUSAL_EXPANDER_PROMPT,
    ) -> None:
        self._client = client                 # injected; or built lazily on first call
        self.model = model
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt

    def _get_client(self):
        """Build the real Anthropic client lazily — only when actually needed, so that"""
        if self._client is None:
            import anthropic  # imported lazily so the dependency is optional at import time

            self._client = anthropic.Anthropic()
        return self._client

    def expand_causal(
        self, research_text: str, parsed_theme: str
    ) -> tuple[Optional[CausalNode], Optional[CausalChain], Optional[str]]:
        client = self._get_client()

        user_content = (
            f"Research text:\n{research_text}\n\nParsed theme: {parsed_theme}"
        )
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_content}],
        )

        text = _extract_text(response)
        obj = _parse_json_object(text)

        for key in ("main_theme", "causal_chain", "shared_factor"):
            if key not in obj:
                raise ValueError(
                    f"LLMProvider.expand_causal: model JSON is missing required key "
                    f"'{key}'. Got keys: {sorted(obj)}"
                )

        try:
            main_theme = CausalNode(**obj["main_theme"])
            causal_chain = CausalChain(**obj["causal_chain"])
        except Exception as exc:  # pydantic ValidationError or shape error
            raise ValueError(
                f"LLMProvider.expand_causal: model output failed schema validation "
                f"({exc}). Offending JSON: {json.dumps(obj)[:500]}"
            ) from exc

        shared_factor = obj["shared_factor"]
        if not isinstance(shared_factor, str) or not shared_factor.strip():
            raise ValueError(
                f"LLMProvider.expand_causal: shared_factor must be a non-empty string, "
                f"got {shared_factor!r}"
            )

        chain_ids = {n.id for n in causal_chain.nodes}
        if main_theme.id not in chain_ids:
            raise ValueError(
                f"LLMProvider.expand_causal: main_theme id '{main_theme.id}' is not "
                f"among the chain node ids {sorted(chain_ids)}."
            )

        # main_theme is the PROMOTED, routed theme — it must carry an operational axis.
        # (Non-promoted theme candidates in the chain may omit one; the routed one cannot.)
        if not main_theme.is_routable():
            raise ValueError(
                "LLMProvider.expand_causal: main_theme (the promoted, routed theme) must be "
                "a kind='theme' node carrying an operational axis before it can be routed."
            )

        return main_theme, causal_chain, shared_factor

def _extract_text(response) -> str:
    """Concatenate the text of every text content block in an Anthropic Message."""
    content = getattr(response, "content", None)
    if not content:
        raise ValueError(
            "LLMProvider.expand_causal: model response had no content blocks."
        )
    parts = [
        block.text
        for block in content
        if getattr(block, "type", None) == "text" and getattr(block, "text", None)
    ]
    if not parts:
        raise ValueError(
            "LLMProvider.expand_causal: model response contained no text blocks."
        )
    return "\n".join(parts)

def _parse_json_object(text: str) -> dict:
    """Parse the JSON object from the model text, tolerating prose / ```json fences by"""
    snippet = text.strip()
    start = snippet.find("{")
    end = snippet.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError(
            f"LLMProvider.expand_causal: no JSON object found in model output: "
            f"{snippet[:300]!r}"
        )
    candidate = snippet[start : end + 1]
    try:
        obj = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLMProvider.expand_causal: model output is not valid JSON ({exc}). "
            f"Offending snippet: {candidate[:300]!r}"
        ) from exc
    if not isinstance(obj, dict):
        raise ValueError(
            f"LLMProvider.expand_causal: model JSON is not an object, got "
            f"{type(obj).__name__}."
        )
    return obj
