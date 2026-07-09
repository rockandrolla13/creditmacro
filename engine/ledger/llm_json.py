"""Anthropic Messages-API response helpers for the ledger LLM seams.

Mirrors the extraction logic in engine/llm_provider.py (which uses
anthropic.Anthropic().messages.create) so the ledger providers parse responses
the same way, without importing that module's private helpers. Default model is
claude-opus-4-8 (the current most-capable model); the engine's discovery provider
uses claude-sonnet-4-6 — both are overridable per provider.
"""
from __future__ import annotations

import json

LEDGER_MODEL = "claude-opus-4-8"


def extract_text(response) -> str:
    """Concatenate the text blocks of an Anthropic Messages response."""
    content = getattr(response, "content", None)
    if not content:
        raise ValueError("LLM response had no content blocks.")
    parts = [
        b.text for b in content
        if getattr(b, "type", None) == "text" and getattr(b, "text", None)
    ]
    if not parts:
        raise ValueError("LLM response contained no text blocks.")
    return "\n".join(parts)


def parse_json_object(text: str) -> dict:
    """Extract the first JSON object from model output."""
    snippet = text.strip()
    start, end = snippet.find("{"), snippet.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"no JSON object in model output: {snippet[:200]!r}")
    obj = json.loads(snippet[start:end + 1])
    if not isinstance(obj, dict):
        raise ValueError(f"model JSON is not an object, got {type(obj).__name__}")
    return obj
