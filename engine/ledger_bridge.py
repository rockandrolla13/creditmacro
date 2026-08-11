"""SCAFFOLD — the ledger→discovery adapter (the seam, not the entrance).

    corpus doc → forward_ingest → ThemeHypothesis → to_theme_object → LedgerProvider
                                                                          ↓
                                                          run_workflow(mode="discovery")
                                                                          ↓
                                                            ranked strategy families → STOP

This module owns ONLY the middle arrow: it turns a ledger-projected `ThemeObject`
into something that satisfies the DISCOVERY half of `engine.protocols.Provider`, so
the existing `run_workflow` can route it. The corpus walk lives in
`engine.ledger_entrance`; the ledger→engine field mapping lives in
`engine/ledger/projection.py`.

Three design rules, each load-bearing:

1. **`projection.py` stays the only status-axis mapping site (ONTOLOGY AMEND A3).**
   This adapter is constructed FROM a projected `ThemeObject` and never reads
   `LifecycleStatus` itself. It reads the projected object's `status`/`block_reason`
   only to refuse to run — it never re-derives a pipeline status from market truth.

2. **Discovery seams only.** `enumerate_expressions`, `size_and_risk` and
   `assess_trap_implications` are DELIBERATELY absent, so `run_workflow(..., "expression")`
   raises `expression_mode_not_supported` by the same structural mechanism that fences
   `LLMProvider`. Absence is the guard; do not add them "for completeness".

3. **Nothing is invented.** Every value handed to a seam traces to a field of the
   folded `ThemeHypothesis`. Where the ledger has no data — scenarios, market value,
   axis history — the seam returns empty/None so downstream caps confidence rather
   than reading a fabricated zero as a measurement.

Discovery mode. No legs, no sizing, no hedge ratios; the pipeline stops at ranked
strategy families.
"""
from __future__ import annotations

from typing import Optional

from .protocols import RunContext, SizingRiskBundle  # noqa: F401  (SizingRiskBundle: see rule 2)
from .schema import (
    Axis,
    BiasCritique,
    CausalChain,
    CausalNode,
    LoopDiagnosis,
    Scenario,
    SystemMap,
    ThemeObject,
    Thesis,
)
from .stage0 import IngestionResult

# The seams a discovery-only provider MUST expose, and the seams it MUST NOT.
# `test_ledger_bridge_scaffold` asserts both halves — the second is a firewall, not
# a nicety: a ledger theme has no market mark, so an expression run on one would be
# pricing against a number nobody observed.
DISCOVERY_SEAMS: tuple[str, ...] = (
    "context",
    "parse",
    "extract_drivers",
    "expand_causal",
    "build_system_map",
    "critique_mental_model",
    "diagnose_loops",
    "propose_scenarios",
    "define_axis",
    "normal_fair_value",
    "critique",
)
EXPRESSION_SEAMS: tuple[str, ...] = (
    "enumerate_expressions",
    "size_and_risk",
    "assess_trap_implications",
)


class LedgerProjectionNotRoutable(RuntimeError):
    """The projected object cannot be routed — raised instead of routing a dead theme.

    `projection.to_theme_object` maps a non-live ledger status (FALSIFIED / EXPIRED /
    RETIRED / MERGED) to `status="blocked"`. Running discovery on such an object would
    manufacture a fresh pipeline status for a theme the market has already settled.
    """


class LedgerProvider:
    """Discovery-only `Provider` driven by a ledger-projected `ThemeObject`.

    Construct with the OUTPUT of `engine.ledger.projection.to_theme_object`, never with
    a `ThemeHypothesis` — that is what keeps the A3 mapping in one place.
    """

    # `run_workflow` reads this attribute to decide whether to call define_axis for
    # confirmation. False: the ledger's axis is a registry entry (WF clause c), already
    # gated at admission. Re-confirming it would invite a second opinion on a settled fact.
    confirm_axis = False

    def __init__(
        self,
        projected: ThemeObject,
        *,
        author: str = "engine.ledger_bridge (projected)",
    ) -> None:
        if projected.status == "blocked":
            raise LedgerProjectionNotRoutable(
                f"projected theme {projected.id!r} is blocked "
                f"({projected.block_reason}); discovery will not run on a dead theme."
            )
        self.projected = projected
        self.author = author

    # ── identity / stage 0 ───────────────────────────────────────────────────

    def context(self) -> RunContext:
        """Build the RunContext from the projected object.

        `x_mkt` MUST stay None: the ledger names an axis, it does not observe one.
        Discovery degrades gracefully (edge_survival="unknown", capped confidence).
        `prior` is uniform over zero scenarios, i.e. empty.
        """
        d_str = self.projected.thesis.direction_of_view
        try:
            sign_val = int(d_str)
            thesis_sign = -1 if sign_val < 0 else 1
        except ValueError:
            thesis_sign = -1 if "-" in d_str else 1

        return RunContext(
            statement=self.projected.statement,
            horizon=self.projected.horizon,
            author=self.author,
            x_mkt=None,
            prior=[],
            thesis_sign=thesis_sign,
            provenance=self.projected.provenance,
        )

    def parse(self, raw: str) -> IngestionResult:
        """Stage-0 streams. A ledger theme arrives already parsed into claims, so this
        returns EMPTY streams rather than re-deriving them — re-parsing here would be a
        second, unattributed extraction pass over text Pass A already read blind (I2)."""
        return IngestionResult(
            observations=[],
            candidate_themes=[],
            consensus_signals=[],
            ranked_candidates=[],
        )

    # ── engine 1 — thesis, causal object, axis ───────────────────────────────

    def extract_drivers(self, statement: str) -> Thesis:
        """Return the projected thesis verbatim. No re-derivation."""
        return self.projected.thesis

    def expand_causal(
        self, research_text: str, parsed_theme: str
    ) -> tuple[Optional[CausalNode], Optional[CausalChain], Optional[str]]:
        """Return the projected (main_theme, causal_chain, shared_factor)."""
        return (
            self.projected.main_theme,
            self.projected.causal_chain,
            self.projected.shared_factor,
        )

    def define_axis(self, thesis: Thesis) -> Axis:
        """The projected axis. Named, not measured: `current_value` and `history` stay unset."""
        return self.projected.axis

    def normal_fair_value(self, axis: Axis) -> float:
        """EXPRESSION-only seam. Discovery never calls it; a ledger theme has no observed
        level, so there is no honest number to return."""
        raise NotImplementedError(
            "LedgerProvider.normal_fair_value: discovery-only provider has no observed axis level"
        )

    # ── system map / critique / loops ────────────────────────────────────────

    def build_system_map(
        self, thesis: Thesis, causal_chain: Optional[CausalChain]
    ) -> Optional[SystemMap]:
        """None — the ledger carries a transmission chain, not a Meadows stock/flow map.
        Returning None is correct; synthesising one would be reasoning the ledger never did."""
        return None

    def critique_mental_model(
        self, statement: str, causal_chain: Optional[CausalChain]
    ) -> Optional[BiasCritique]:
        """None — no adversarial pass has run over a projected theme."""
        return None

    def diagnose_loops(self, system_map: Optional[SystemMap]) -> Optional[LoopDiagnosis]:
        """Carry the ledger falsifier F into `invalidation_evidence`.

        THIS IS THE GATE THAT DECIDES ROUTING. `run_workflow` promotes to
        `strategy_family_routed` only when `loop_diagnosis.invalidation_evidence` is
        non-empty (CLAUDE.md gate 4: a thesis with no falsifier is not a thesis). The
        ledger already guarantees a non-empty falsifier via WF clause (b), so the
        falsifier must arrive here — not in `provenance.evidence` alone, where nothing
        reads it.
        """
        invalidation_evidence: list[str] = []
        if self.projected.provenance and self.projected.provenance.evidence:
            for item in self.projected.provenance.evidence:
                if item.startswith("falsifier: "):
                    f_text = item[len("falsifier: "):].strip()
                    if f_text:
                        invalidation_evidence.append(f_text)
                elif item.startswith("falsifier:"):
                    f_text = item[len("falsifier:"):].strip()
                    if f_text:
                        invalidation_evidence.append(f_text)

        return LoopDiagnosis(
            dominant_loop_now="not diagnosed",
            possible_loop_shift="not diagnosed",
            invalidation_evidence=invalidation_evidence,
            decision="watchlist",
        )

    # ── scenarios ────────────────────────────────────────────────────────────

    def propose_scenarios(
        self, thesis: Thesis, axis: Axis, loop_diagnosis: Optional[LoopDiagnosis] = None
    ) -> list[Scenario]:
        """EMPTY. The ledger prices nothing. Families are still routed but confidence is
        capped (no scenarios ⇒ ≤0.45), which is the honest answer, not a degraded one."""
        return []

    def critique(self, theme: ThemeObject) -> list[str]:
        """No critique pass on a projected theme."""
        return []


def provider_for(projected: ThemeObject) -> LedgerProvider:
    """Convenience constructor — kept so callers never build the adapter from a
    `ThemeHypothesis` by accident."""
    return LedgerProvider(projected)
