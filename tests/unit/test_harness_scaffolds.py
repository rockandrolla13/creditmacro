"""G3 and G8 are scaffolds, and these tests keep them honest.

A stub that silently returns a permissive default is worse than no guardrail: the
pipeline gains a guardrail-shaped object that certifies whatever it is handed. So the
contract for an unbuilt guardrail is that CALLING it fails loudly and names its phase.

These tests fail the day someone implements one of these functions, which is the point —
implementing it means deleting the test that says it does not exist.
"""
from __future__ import annotations

import pytest

from engine.grounding import adjudication, brief_gate
from engine.schema.source_brief import (
    MAX_BULLETS,
    MAX_BULLET_WORDS,
    MAX_WORDS,
    MIN_BULLETS,
    BriefBullet,
    SourceThemeBrief,
)


@pytest.mark.parametrize("call,phase", [
    (lambda: adjudication.adjudicate("define_axis", None, None, ""), "G3"),
    (lambda: adjudication.assert_adjudicated(()), "G3"),
    (lambda: adjudication.AdjudicatedProvider(None, None, ""), "G3"),
    (lambda: brief_gate.assert_brief_grounded(None, [], None), "G8"),
    (lambda: brief_gate.write_brief("s", "t", [], None), "G8"),
    (lambda: list(brief_gate.brief_numbers(None)), "G8"),
])
def test_an_unbuilt_guardrail_refuses_rather_than_passing(call, phase):
    with pytest.raises(NotImplementedError) as exc:
        call()
    assert phase in str(exc.value)
    assert "Phase" in str(exc.value)


# ── the G3 verdict type is real, so the shape is fixed before the model lands ──

def test_an_adjudication_verdict_records_the_verifier_and_its_objection():
    verdict = adjudication.AdjudicationVerdict(
        seam="define_axis", agree=False, objection="no series named in the source",
        verifier_model_id="claude-sonnet-5")
    assert verdict.grounding_spans == ()
    with pytest.raises(Exception):
        verdict.agree = True                      # frozen


# ── the G8 schema is real; the writer and gate are not ────────────────────────

def _bullet(text: str = "Data-center issuance reached $440bn.") -> BriefBullet:
    return BriefBullet(text=text, atom_ids=("jpm-001",))


def test_a_bullet_must_name_at_least_one_atom():
    """An unreferenced bullet is an unsourced sentence with a bullet point in front."""
    with pytest.raises(ValueError):
        BriefBullet(text="Spreads will widen.", atom_ids=())


def test_the_bullet_count_limits_are_enforced_by_the_schema():
    for n in (MIN_BULLETS - 1, MAX_BULLETS + 1):
        with pytest.raises(ValueError):
            SourceThemeBrief(source_slug="s", theme_id="t",
                             bullets=tuple(_bullet() for _ in range(n)),
                             word_count=40, direction="supports")


def test_an_abstained_confidence_is_representable_as_absence_not_zero():
    brief = SourceThemeBrief(source_slug="s", theme_id="t",
                             bullets=tuple(_bullet() for _ in range(MIN_BULLETS)),
                             word_count=40, direction="qualifies")
    assert brief.confidence is None


def test_the_format_constants_are_the_plan_s_hard_limits():
    assert (MIN_BULLETS, MAX_BULLETS, MAX_WORDS, MAX_BULLET_WORDS) == (3, 5, 120, 25)
