"""LLMProvider — the LIVE generative counterpart to ScriptedProvider.

Implements the DISCOVERY half only: expand_causal, define_axis, build_system_map,
diagnose_loops, critique_mental_model. Each makes one Anthropic Messages call behind a
purpose-specific prompt, then PARSES + VALIDATES the JSON into the existing engine schema.
Expression seams (enumerate_expressions, size_and_risk, propose_scenarios) are deliberately
NOT implemented here — they stay scripted.

Memory: an optional phase-A MemoryRetriever is injected; the seams pull METHOD pages only
(the retriever is fail-closed on CASE in phase A), so no case memory enters fresh reasoning.
"""
from __future__ import annotations

import json
from typing import Optional

from .prompts import (
    CAUSAL_EXPANDER_PROMPT,
    CRITIQUE_PROMPT,
    DEFINE_AXIS_PROMPT,
    DIAGNOSE_LOOPS_PROMPT,
    SYSTEM_MAP_PROMPT,
)
from .schema import (
    AxisCandidate,
    BiasCritique,
    CausalChain,
    CausalNode,
    LoopDiagnosis,
    SystemMap,
    Thesis,
)
from .schema.causal import Axis

_DEFAULT_MODEL = "claude-sonnet-4-6"
_DEFAULT_MAX_TOKENS = 4096


class NoCleanAxisError(ValueError):
    """define_axis found no clean operational axis — route to watchlist_only, do not
    fabricate a series. Carries the model's reason + data_needed_next."""
    def __init__(self, reason: str, data_needed_next: str) -> None:
        self.reason = reason
        self.data_needed_next = data_needed_next
        super().__init__(f"no clean axis: {reason} (data needed: {data_needed_next})")


class LLMProvider:
    """Live DISCOVERY seams backed by the Anthropic Messages API."""

    def __init__(
        self,
        client=None,
        model: str = _DEFAULT_MODEL,
        max_tokens: int = _DEFAULT_MAX_TOKENS,
        system_prompt: str = CAUSAL_EXPANDER_PROMPT,
        retriever=None,                      # optional phase-A MemoryRetriever (METHOD-only)
    ) -> None:
        self._client = client
        self.model = model
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt
        self.retriever = retriever
        self.last_axis_selection: Optional[AxisCandidate] = None

    def _get_client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic()
        return self._client

    # ── generic call + method-memory context ────────────────────────────────
    def _call_json(self, system_prompt: str, user_content: str) -> dict:
        response = self._get_client().messages.create(
            model=self.model, max_tokens=self.max_tokens, system=system_prompt,
            messages=[{"role": "user", "content": user_content}],
        )
        return _parse_json_object(_extract_text(response))

    def _method_context(self) -> str:
        """Pull METHOD pages only (fail-closed: the retriever never serves CASE in phase A)."""
        if self.retriever is None:
            return ""
        parts = []
        for slug in self.retriever.method_slugs():
            page = self.retriever.retrieve(slug)
            if page is not None:
                parts.append(f"[[{slug}]]: {page.body[:300]}")
        return ("\nMETHOD memory:\n" + "\n".join(parts)) if parts else ""

    @staticmethod
    def _validate(model_cls, obj: dict, seam: str):
        try:
            return model_cls(**obj)
        except Exception as exc:
            raise ValueError(
                f"LLMProvider.{seam}: model output failed schema validation ({exc}). "
                f"JSON: {json.dumps(obj)[:400]}"
            ) from exc

    # ── EXPAND_CAUSAL ───────────────────────────────────────────────────────
    def expand_causal(
        self, research_text: str, parsed_theme: str
    ) -> tuple[Optional[CausalNode], Optional[CausalChain], Optional[str]]:
        obj = self._call_json(
            self.system_prompt,
            f"Research text:\n{research_text}\n\nParsed theme: {parsed_theme}",
        )
        for key in ("main_theme", "causal_chain", "shared_factor"):
            if key not in obj:
                raise ValueError(f"expand_causal: missing key '{key}'. Got {sorted(obj)}")
        main_theme = self._validate(CausalNode, obj["main_theme"], "expand_causal")
        causal_chain = self._validate(CausalChain, obj["causal_chain"], "expand_causal")
        shared_factor = obj["shared_factor"]
        if not isinstance(shared_factor, str) or not shared_factor.strip():
            raise ValueError("expand_causal: shared_factor must be a non-empty string")
        if main_theme.id not in {n.id for n in causal_chain.nodes}:
            raise ValueError(f"expand_causal: main_theme '{main_theme.id}' not in chain nodes")
        if not main_theme.is_routable():
            raise ValueError("expand_causal: routed main_theme must carry an operational axis")
        return main_theme, causal_chain, shared_factor

    # ── DEFINE_AXIS ─────────────────────────────────────────────────────────
    def select_axis(self, thesis: Thesis) -> AxisCandidate:
        """Full axis decision (axis | watchlist + reason + data_needed_next). Prefers the
        source-derived candidates carried on the thesis drivers."""
        candidates = "\n".join(f"- {d.proxy_observable}" for d in thesis.drivers if d.proxy_observable)
        user = (f"Source-derived axis candidates (prefer these):\n{candidates}\n\n"
                f"Thesis direction: {thesis.direction_of_view}{self._method_context()}")
        cand = self._validate(AxisCandidate, self._call_json(DEFINE_AXIS_PROMPT, user), "define_axis")
        self.last_axis_selection = cand
        return cand

    def define_axis(self, thesis: Thesis) -> Axis:
        cand = self.select_axis(thesis)
        if cand.axis is None:
            raise NoCleanAxisError(cand.reason, cand.data_needed_next)
        return cand.axis

    # ── SYSTEM_MAP ──────────────────────────────────────────────────────────
    def build_system_map(self, thesis: Thesis, causal_chain: Optional[CausalChain]) -> Optional[SystemMap]:
        nodes = ", ".join(n.id for n in causal_chain.nodes) if causal_chain else ""
        user = (f"Causal chain nodes: {nodes}\nThesis: {thesis.direction_of_view}"
                f"{self._method_context()}")
        return self._validate(SystemMap, self._call_json(SYSTEM_MAP_PROMPT, user), "build_system_map")

    # ── DIAGNOSE_LOOPS ──────────────────────────────────────────────────────
    def diagnose_loops(self, system_map: Optional[SystemMap]) -> Optional[LoopDiagnosis]:
        if system_map is None:
            return None
        loops = "; ".join(f"{fl.id}:{fl.type}" for fl in system_map.feedback_loops)
        user = f"System loops: {loops}\nStocks: {[s.name for s in system_map.stocks]}"
        return self._validate(LoopDiagnosis, self._call_json(DIAGNOSE_LOOPS_PROMPT, user), "diagnose_loops")

    # ── CRITIQUE_MENTAL_MODEL ───────────────────────────────────────────────
    def critique_mental_model(self, statement: str, causal_chain: Optional[CausalChain]) -> Optional[BiasCritique]:
        nodes = ", ".join(n.statement for n in causal_chain.nodes) if causal_chain else ""
        user = f"Theme: {statement}\nCausal chain: {nodes}"
        return self._validate(BiasCritique, self._call_json(CRITIQUE_PROMPT, user), "critique_mental_model")


def _extract_text(response) -> str:
    content = getattr(response, "content", None)
    if not content:
        raise ValueError("LLMProvider: model response had no content blocks.")
    parts = [b.text for b in content
             if getattr(b, "type", None) == "text" and getattr(b, "text", None)]
    if not parts:
        raise ValueError("LLMProvider: model response contained no text blocks.")
    return "\n".join(parts)


def _parse_json_object(text: str) -> dict:
    snippet = text.strip()
    start, end = snippet.find("{"), snippet.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"LLMProvider: no JSON object in model output: {snippet[:300]!r}")
    try:
        obj = json.loads(snippet[start:end + 1])
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLMProvider: model output is not valid JSON ({exc}): "
                         f"{snippet[start:end + 1][:300]!r}") from exc
    if not isinstance(obj, dict):
        raise ValueError(f"LLMProvider: model JSON is not an object, got {type(obj).__name__}.")
    return obj
