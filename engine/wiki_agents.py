"""Wiki + agent scaling layer — a CONTROLLED registry of role-specific compilation workflows.

These are NOT unconstrained autonomous agents. Each is a contract-bound workflow with fixed
inputs/outputs, declared read/write paths, access-class rules, and required tests. They compile
raw sources into durable wiki memory (source pages, evidence atoms, theme/concept pages, and —
for METHOD sources — skill cards). None of them generate trades, scenarios, probabilities, or
sizing, and none let archived CASE memory influence Phase-A reasoning.

PART 1 (this file): the AgentContract, the six declared agents, and the AgentRegistry.
PART 2: SourceIntakeAgent is implemented (deterministic classification). The other five declare
full contracts; their run() is a later part and raises NotImplementedError.
"""
from __future__ import annotations

import re as _re
from datetime import date
from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict

from .evidence_extraction import EvidenceExtractionBundle
from .temporal import (
    ForecastHorizon,
    TemporalClaimStatus,
    TemporalContext,
    classify_temporal_context,
)

SourceTypeT = Literal["book", "paper", "report", "deck", "memo", "transcript", "market_data", "other"]
AccessClassT = Literal["method", "case", "mixed", "ignore"]
PageAccessT = Literal["method", "case", "ignore"]

_SOURCE_TYPES = frozenset(
    ("book", "paper", "report", "deck", "memo", "transcript", "market_data", "other"))
# PART 9 — exact warning fired when temporal context cannot be computed (current_date missing).
_TEMPORAL_MISSING_DATE_WARNING = "Temporal context not computed; current_date missing."


# ── contract ──────────────────────────────────────────────────────────────────

class AgentContract(BaseModel):
    """The fixed, declared contract every wiki agent must publish."""
    model_config = ConfigDict(frozen=True)
    agent_name: str
    purpose: str
    input_objects: list[str]
    output_objects: list[str]
    allowed_paths_to_read: list[str]
    allowed_paths_to_write: list[str]
    access_class_rules: list[str]
    provider_seams_used: list[str]
    non_goals: list[str]
    tests_required: list[str]


class WikiAgent:
    """Base role-workflow. Subclasses set `contract` and implement `run`."""
    contract: AgentContract

    def run(self, input):  # noqa: A002 - matches the registry vocabulary
        raise NotImplementedError(
            f"{self.contract.agent_name}: run() is implemented in a later part of the wiki "
            f"scaling build."
        )


# ── PART 2 schema: source intake ────────────────────────────────────────────────

class SourcePage(BaseModel):
    page_number: int
    text: str


class SourceIntakeInput(BaseModel):
    source_slug: str
    source_type: SourceTypeT = "other"
    path: Optional[str] = None
    pages: list[SourcePage] = []
    title: Optional[str] = None


class PageClassification(BaseModel):
    page_number: int
    access_class: PageAccessT
    rationale: str


class SourceClassification(BaseModel):
    source_slug: str
    source_type: SourceTypeT
    access_class: AccessClassT
    page_classifications: list[PageClassification] = []
    copyright_status: str
    ingestion_policy: str
    recommended_compilers: list[str] = []
    warnings: list[str] = []


# ── PART 2: SourceIntakeAgent (deterministic) ───────────────────────────────────

# Per-page keyword signatures, checked IGNORE → CASE → METHOD (most-specific disqualifiers first):
# a performance/bio page must never become a method rule; a named trade example is CASE.
_IGNORE_KEYS = (
    "past performance", "track record", "returns since inception", "since inception",
    "net return", "assets under management", " aum", "biograph", "team bio", "disclaimer",
    "important information", "this page intentionally", "contact us",
)
_CASE_KEYS = (
    "trade example", "worked example", "worked trade", "case study", "french bank",
    "we recommend", "we are long", "we are short", "specific trade", "example trade",
    "recommend the", "position in",
)
_METHOD_KEYS = (
    "process", "framework", "methodology", "four-step", "four step", "liquidity scoring",
    "risk framework", "macro cycle", "decision", "stocks and flows", "feedback loop",
    "do-calculus", "causal", "mental model", "leverage point", "investment process",
    "valuation framework", "how we",
)

# Source-type → base access class when no page manifest disambiguates.
_BASE_BY_TYPE: dict[str, AccessClassT] = {
    "book": "method", "paper": "method",
    "report": "case", "memo": "case", "transcript": "case", "market_data": "case",
    "deck": "mixed", "other": "mixed",
}
_COPYRIGHT_BY_TYPE: dict[str, str] = {
    "book": "copyrighted_paraphrase_only", "paper": "copyrighted_paraphrase_only",
    "deck": "copyrighted_paraphrase_only", "report": "copyrighted_paraphrase_only",
    "memo": "copyrighted_paraphrase_only", "transcript": "copyrighted_paraphrase_only",
    "market_data": "factual_data_paraphrase_only", "other": "unknown_paraphrase_only",
}
_INGESTION_POLICY = {
    "method": "compile_method_skills_paraphrase_only",
    "case": "extract_evidence_atoms_case",
    "mixed": "split_by_page_method_and_case",
    "ignore": "skip",
}
_COMPILERS = {
    "method": ["SkillCompilerAgent", "WikiIntegratorAgent", "WikiLintAgent"],
    "case": ["EvidenceExtractionAgent", "WikiIntegratorAgent", "WikiLintAgent"],
    "mixed": ["EvidenceExtractionAgent", "SkillCompilerAgent", "WikiIntegratorAgent", "WikiLintAgent"],
    "ignore": [],
}


def _classify_page(text: str) -> tuple[PageAccessT, str]:
    t = f" {text.lower()} "
    if any(k in t for k in _IGNORE_KEYS):
        return "ignore", "performance/biographical/boilerplate page — not a method rule"
    if any(k in t for k in _CASE_KEYS):
        return "case", "specific trade/case example — case memory"
    if any(k in t for k in _METHOD_KEYS):
        return "method", "process/framework/methodology — teaches reasoning"
    return "ignore", "no method/case signal — left out of compilation"


def _source_class_from_pages(pages: list[PageClassification]) -> AccessClassT:
    meaningful = {p.access_class for p in pages if p.access_class != "ignore"}
    if meaningful == {"method"}:
        return "method"
    if meaningful == {"case"}:
        return "case"
    if {"method", "case"} <= meaningful:
        return "mixed"
    return "ignore"


class SourceIntakeAgent(WikiAgent):
    contract = AgentContract(
        agent_name="SourceIntakeAgent",
        purpose="Classify a raw/normalized source as method | case | mixed | ignore (per page when "
                "a deck), and recommend which compilers should run — never reproducing source text.",
        input_objects=["raw_or_normalized_md_path", "source_metadata", "optional_page_manifest"],
        output_objects=["SourceClassification"],
        allowed_paths_to_read=["raw/", "markdowns/"],
        allowed_paths_to_write=[],  # classification only; the integrator writes the wiki
        access_class_rules=[
            "books/papers/process decks that teach reasoning → method",
            "reports/memos/transcripts/market_data/past outcomes → case",
            "mixed decks are split by page; performance & biographical pages never become method",
            "copyrighted full text stays in raw/private; wiki gets concise paraphrase only",
        ],
        provider_seams_used=[],  # deterministic heuristic; no LLM seam
        non_goals=["generate trades", "generate scenarios/probabilities", "reproduce source text",
                   "write wiki pages"],
        tests_required=["alaph process=method", "alaph performance=ignore/case",
                        "alaph french-bank=case", "xantium process=method", "jpm=case"],
    )

    def run(self, input: Union[SourceIntakeInput, dict]) -> SourceClassification:
        inp = input if isinstance(input, SourceIntakeInput) else SourceIntakeInput.model_validate(input)
        warnings: list[str] = []
        if not inp.source_slug:
            warnings.append("missing source_slug")

        page_cls = [
            PageClassification(page_number=p.page_number, access_class=ac, rationale=why)
            for p in inp.pages
            for ac, why in [_classify_page(p.text)]
        ]

        base = _BASE_BY_TYPE[inp.source_type]
        if base == "mixed":
            # decks / other are genuinely page-mixed → derive from per-page classes
            access = _source_class_from_pages(page_cls) if page_cls else "mixed"
            if not page_cls:
                warnings.append("no page manifest for a deck/other source — recommend a per-page split")
        else:
            # definitive types keep their class: a research REPORT is CASE even though its
            # analytical prose contains 'model'/'process' wording; a book/paper stays METHOD.
            access = base
            if page_cls and {"method", "case"} <= {p.access_class for p in page_cls}:
                warnings.append(f"{inp.source_type} kept as {base} despite mixed page signals")

        return SourceClassification(
            source_slug=inp.source_slug,
            source_type=inp.source_type,
            access_class=access,
            page_classifications=page_cls,
            copyright_status=_COPYRIGHT_BY_TYPE[inp.source_type],
            ingestion_policy=_INGESTION_POLICY[access],
            recommended_compilers=_COMPILERS[access],
            warnings=warnings,
        )


# ── the five later-part agents: full contracts, run() deferred ──────────────────

class EvidenceExtractionAgent(WikiAgent):
    contract = AgentContract(
        agent_name="EvidenceExtractionAgent",
        purpose="Extract concise, paraphrased, source-backed evidence atoms (with page/source "
                "provenance and claim_kind) plus causal claims, operational axes, confounders, "
                "candidate falsifiers and strategy-family hints from a CASE source — never "
                "reproducing source text and never generating trades/scenarios/probabilities.",
        input_objects=["EvidenceExtractionInput (case source markdown + metadata)"],
        output_objects=["EvidenceExtractionBundle"],
        allowed_paths_to_read=["raw/", "markdowns/"],
        allowed_paths_to_write=[],  # returns a bundle only; wiki writing is WikiIntegratorAgent
        access_class_rules=["runs ONLY on access_class=case sources", "output is CASE memory",
                            "current-input only enters Phase A via RunContext, never the archive",
                            "paraphrase + citation only — no long verbatim source text"],
        provider_seams_used=[],  # deterministic, rule-assisted v1 (LLM paraphrase is a later upgrade)
        non_goals=["invent facts", "generate scenarios/probabilities", "reproduce source text",
                   "emit trades/curve points/hedge ratios/sizing/execution", "write wiki pages"],
        tests_required=["atoms carry source_slug + page provenance + claim_kind", "no verbatim leak",
                        "different sources → different axes/families (no JPM collapse)"],
    )

    def run(self, input):  # noqa: A002
        from .evidence_extraction import (
            EvidenceExtractionInput,
            EvidenceExtractionBundle,
            extract_evidence,
        )
        inp = (input if isinstance(input, EvidenceExtractionInput)
               else EvidenceExtractionInput.model_validate(input))
        if inp.access_class != "case":
            raise ValueError("EvidenceExtractionAgent runs only on access_class=case sources")
        bundle: EvidenceExtractionBundle = extract_evidence(inp)
        self._attach_temporal_context(inp, bundle)
        return bundle

    @staticmethod
    def _attach_temporal_context(inp, bundle) -> None:
        """PART 9 — optionally enrich the bundle with temporal context. Computed ONLY when BOTH
        source_date AND current_date are supplied. current_date is NEVER implicit (no wall clock):
        if either is missing we leave temporal_context=None and emit the exact missing-date warning."""
        if not (inp.source_date and inp.current_date):
            bundle.extraction_warnings.append(_TEMPORAL_MISSING_DATE_WARNING)
            return
        try:
            current = date.fromisoformat(str(inp.current_date).strip())
        except ValueError:
            # an unparseable current_date is treated as missing — still never defaulted to today
            bundle.extraction_warnings.append(_TEMPORAL_MISSING_DATE_WARNING)
            return
        classification = SourceClassification(
            source_slug=inp.source_slug,
            source_type=inp.source_type if inp.source_type in _SOURCE_TYPES else "other",
            access_class="case",
            copyright_status="copyrighted_paraphrase_only",
            ingestion_policy="extract_evidence_atoms_case",
            recommended_compilers=["EvidenceExtractionAgent"],
        )
        out = TemporalContextAgent().run(TemporalContextInput(
            source_classification=classification, extraction_bundle=bundle,
            current_date=current, is_current_input=inp.is_current_input))
        bundle.temporal_context = out.temporal_context
        bundle.temporal_claim_statuses = out.claim_statuses
        bundle.forecast_horizons = out.forecast_horizons


class SkillCompilerAgent(WikiAgent):
    contract = AgentContract(
        agent_name="SkillCompilerAgent",
        purpose="Compile a METHOD source into paraphrased skill cards (process primitives), "
                "merging into existing cards where topics overlap.",
        input_objects=["SourceClassification", "normalized_md"],
        output_objects=[".claude/skills/<slug>/SKILL.md", "wiki/process pages"],
        allowed_paths_to_read=["raw/", "markdowns/"],
        allowed_paths_to_write=[".claude/skills/", "wiki/process/", "wiki/engines/"],
        access_class_rules=["method cards only", "register but do not auto-wire into SEAM_TO_SKILLS",
                            "no case conclusions, no long copyrighted passages"],
        provider_seams_used=["LLMProvider.compile_method (pending)"],
        non_goals=["compile case material", "change golden-master output", "reproduce source text"],
        tests_required=["card frontmatter valid", "method-only", "no verbatim leak"],
    )


class WikiIntegratorAgent(WikiAgent):
    contract = AgentContract(
        agent_name="WikiIntegratorAgent",
        purpose="Integrate compiled outputs into the wiki: source page, theme/concept/entity pages, "
                "scenario candidates (only if explicitly supplied), and index/log/memory-map updates.",
        input_objects=["SourceClassification", "EvidenceAtom[]", "compiled_cards"],
        output_objects=["wiki/sources", "wiki/themes", "wiki/concepts", "wiki/entities",
                        "wiki/scenarios", "index.md", "log.md", "memory-map.md"],
        allowed_paths_to_read=["wiki/"],
        allowed_paths_to_write=["wiki/"],
        access_class_rules=["stamp access_class per page", "never write trades/sizing/hedge ratios",
                            "scenarios only when explicitly present in the source"],
        provider_seams_used=[],
        non_goals=["generate trades/scenarios/probabilities", "overwrite contradicting claims silently"],
        tests_required=["links resolve", "frontmatter valid", "no trade legs emitted"],
    )


class WikiLintAgent(WikiAgent):
    contract = AgentContract(
        agent_name="WikiLintAgent",
        purpose="Validate wiki health: access_class present, links resolve, sources lists current, "
                "no verbatim leak, no trade/sizing leakage, investment-process fields present.",
        input_objects=["wiki_root"],
        output_objects=["lint_findings", "lint-scratch.md", "log.md"],
        allowed_paths_to_read=["wiki/", "markdowns/"],
        allowed_paths_to_write=["wiki/lint-scratch.md", "wiki/log.md"],
        access_class_rules=["read-only over content pages; only writes lint scratch/log"],
        provider_seams_used=[],
        non_goals=["produce trades", "delete contradictions", "web search"],
        tests_required=["flags broken links", "flags missing access_class", "flags verbatim leak"],
    )


class DiscoveryRunnerAgent(WikiAgent):
    contract = AgentContract(
        agent_name="DiscoveryRunnerAgent",
        purpose="Run the discovery workflow over a compiled CASE source as CURRENT input: load its "
                "evidence atoms, feed the current-input seam, and STOP at ranked strategy families.",
        input_objects=["source_slug", "supplied_scenarios_and_priors_if_present", "wiki_root"],
        output_objects=["ThemeObject", "ProbabilityUpdateAudit", "decision_memo"],
        allowed_paths_to_read=["wiki/", "markdowns/"],
        allowed_paths_to_write=["runs/"],
        access_class_rules=["current-input evidence only in Phase A", "archived CASE refused in Phase A",
                            "CASE analogues only after FreshReasoningSnapshot"],
        provider_seams_used=["Provider discovery seams (existing)"],
        non_goals=["generate scenarios/probabilities", "emit trades/sizing/hedge ratios/execution",
                   "wire expression-mode seams", "alter golden-master functions"],
        tests_required=["stops at strategy_family_routed", "posterior tilts only on supplied evidence",
                        "no trade output"],
    )


# ── TemporalContextAgent (PART 2) ───────────────────────────────────────────────

class TemporalContextInput(BaseModel):
    source_classification: SourceClassification
    extraction_bundle: EvidenceExtractionBundle
    current_date: date                       # caller-supplied — deterministic, replay-safe
    explicit_as_of_date: Optional[date] = None
    is_current_input: bool = False           # only a CURRENT input may be a 'current_report'


class TemporalContextOutput(BaseModel):
    temporal_context: TemporalContext
    claim_statuses: list[TemporalClaimStatus] = []
    forecast_horizons: list[ForecastHorizon] = []
    warnings: list[str] = []


def _page_of(source_location: Optional[str]) -> Optional[int]:
    m = _re.match(r"page:(\d+)", source_location or "")
    return int(m.group(1)) if m else None


class TemporalContextAgent(WikiAgent):
    contract = AgentContract(
        agent_name="TemporalContextAgent",
        purpose="Classify a source's temporality and extract forecast horizons: source date/age, "
                "current vs historical vs method, expired forecasts, stale claims, surviving "
                "mechanisms, per-claim allowed Phase-A use, and whether to route to current "
                "discovery / historical case / outcome-candidate generation.",
        input_objects=["SourceClassification", "EvidenceExtractionBundle", "current_date"],
        output_objects=["TemporalContext", "list[TemporalClaimStatus]", "list[ForecastHorizon]"],
        allowed_paths_to_read=["current input", "method memory"],
        allowed_paths_to_write=[],
        access_class_rules=["CASE stays CASE; METHOD stays METHOD", "old CASE cannot become METHOD",
                            "historical forecasts cannot become method_context",
                            "current_date is caller-supplied; no wall-clock time"],
        provider_seams_used=[],
        non_goals=["no trades", "no current market refresh", "no outcome scoring without data",
                   "no scenario probabilities", "no web search for outcomes"],
        tests_required=["European Equity Strategy regression", "method source regression",
                        "recent case regression"],
    )

    def run(self, input):  # noqa: A002
        inp = (input if isinstance(input, TemporalContextInput)
               else TemporalContextInput.model_validate(input))
        cls, bundle = inp.source_classification, inp.extraction_bundle
        # source date: explicit override → bundle's source_page_fields → None
        sd = inp.explicit_as_of_date
        if sd is None:
            raw = (bundle.source_page_fields or {}).get("source_date")
            if isinstance(raw, str) and raw.strip():
                try:
                    sd = date.fromisoformat(raw.strip())
                except ValueError:
                    sd = None
        # classify every evidence atom, causal claim, and strategy-family hint (PART-5)
        claims = [(a.evidence_id or f"c{i}", _page_of(a.source_location), a.claim)
                  for i, a in enumerate(bundle.evidence_atoms)]
        claims += [(f"causal-{i}", None, f"{c.driver} → {c.outcome}")
                   for i, c in enumerate(bundle.causal_claims)]
        claims += [(f"family-{i}", None, f"{h.family}: {h.rationale}")
                   for i, h in enumerate(bundle.strategy_family_hints)]
        mechanisms = [f"{c.driver} → {c.outcome}" for c in bundle.causal_claims]
        ctx, statuses, horizons, warnings = classify_temporal_context(
            source_slug=cls.source_slug, access_class=cls.access_class, source_date=sd,
            current_date=inp.current_date, claims=claims, mechanisms=mechanisms,
            explicit_as_of_date=inp.explicit_as_of_date, is_current_input=inp.is_current_input)
        return TemporalContextOutput(temporal_context=ctx, claim_statuses=statuses,
                                     forecast_horizons=horizons, warnings=warnings)


# ── PART 6: Multi-Source Theme Aggregator agent ──────────────────────────────────

class MultiSourceThemeAggregatorInput(BaseModel):
    bundles: list[EvidenceExtractionBundle]
    source_classifications: list[SourceClassification]
    temporal_contexts: list[TemporalContext] = []
    current_input_slugs: Optional[list[str]] = None   # CASE sources eligible as current input


class MultiSourceThemeAggregatorAgent(WikiAgent):
    """Stage-0 multi-source deduplicate + rank. Deterministic v1 (no provider seam). Reads only
    current-input bundles + method memory; writes nothing. The access/temporal firewall lives in
    engine.theme_aggregation (archived CASE blocked, METHOD = taxonomy only, historical CASE →
    historical/outcome)."""
    contract = AgentContract(
        agent_name="MultiSourceThemeAggregatorAgent",
        purpose="Deduplicate and rank theme candidates across a current source batch into one "
                "source-attributed, ranked MultiSourceThemeSet. STOP at discovery handoff.",
        input_objects=["EvidenceExtractionBundle[]", "SourceClassification[]", "TemporalContext[]"],
        output_objects=["MultiSourceThemeSet"],
        allowed_paths_to_read=["current input bundles", "method memory"],
        allowed_paths_to_write=[],
        access_class_rules=[
            "archived CASE blocked in Phase A",
            "METHOD allowed for taxonomy only (not market evidence)",
            "historical CASE marked historical/outcome candidate (cannot corroborate current)",
        ],
        provider_seams_used=[],  # deterministic v1
        non_goals=["no trades", "no sizing", "no scenario probabilities", "no execution"],
        tests_required=["dedup", "no overmerge", "access firewall", "temporal firewall",
                        "multi-asset generalization"],
    )

    def run(self, input):  # noqa: A002
        # lazy import: theme_aggregation imports SourceClassification from this module
        from engine.theme_aggregation import (
            ThemeAggregationPolicy,
            aggregate_theme_candidates,
        )
        inp = (input if isinstance(input, MultiSourceThemeAggregatorInput)
               else MultiSourceThemeAggregatorInput.model_validate(input))
        policy = ThemeAggregationPolicy(
            current_input_slugs=(frozenset(inp.current_input_slugs)
                                 if inp.current_input_slugs else None))
        return aggregate_theme_candidates(
            inp.bundles, inp.source_classifications, inp.temporal_contexts or None, policy)


# ── registry ────────────────────────────────────────────────────────────────────

class AgentRegistry:
    """A controlled registry of contract-bound wiki agents."""

    def __init__(self, agents: list[WikiAgent]) -> None:
        self._agents = {a.contract.agent_name: a for a in agents}

    def list_agents(self) -> list[str]:
        return sorted(self._agents)

    def get_agent(self, agent_name: str) -> WikiAgent:
        if agent_name not in self._agents:
            raise KeyError(f"unknown agent: {agent_name!r} (have {self.list_agents()})")
        return self._agents[agent_name]

    def validate_agent_contracts(self) -> list[str]:
        """Return one violation string per agent whose contract omits a required field."""
        # allowed_paths_to_write (read-only agents) and provider_seams_used (deterministic agents)
        # may legitimately be empty; the rest must be meaningfully populated.
        required = ("agent_name", "purpose", "input_objects", "output_objects",
                    "allowed_paths_to_read", "access_class_rules", "non_goals", "tests_required")
        violations: list[str] = []
        for name, agent in self._agents.items():
            c = agent.contract
            for field in required:
                if getattr(c, field) in (None, "", []):
                    violations.append(f"{name}: contract field '{field}' is empty")
        return violations

    def run_agent(self, agent_name: str, input):  # noqa: A002
        return self.get_agent(agent_name).run(input)


REGISTRY = AgentRegistry([
    SourceIntakeAgent(),
    EvidenceExtractionAgent(),
    TemporalContextAgent(),
    SkillCompilerAgent(),
    WikiIntegratorAgent(),
    WikiLintAgent(),
    DiscoveryRunnerAgent(),
    MultiSourceThemeAggregatorAgent(),
])


def run_agent(agent_name: str, input):  # noqa: A002
    """Module-level convenience: run a registered agent by name via the default REGISTRY."""
    return REGISTRY.run_agent(agent_name, input)
