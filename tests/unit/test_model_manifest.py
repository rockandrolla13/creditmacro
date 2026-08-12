"""G7 — model pinning. A live call that is not the pinned configuration is refused."""
from __future__ import annotations

import pytest

from engine.grounding.model_manifest import (
    ENV_OVERRIDE,
    MANIFEST,
    ModelManifest,
    ModelPinMismatch,
    SamplingParams,
    SeamPin,
    assert_pinned,
    assert_verifier_independent,
    override_enabled,
    prompt_hash,
)


def test_the_four_generative_seams_are_pinned():
    """The seams `PLAN-authoritative-harness.md` G3 calls high-stakes."""
    assert {p.seam for p in MANIFEST.seams} == {
        "expand_causal", "define_axis", "propose_scenarios", "build_system_map"
    }


def test_every_pin_is_deterministic():
    """temperature=0 is not a style preference: at any other value, two identical runs
    are two different runs and capture/replay stops describing the system."""
    assert all(p.params.temperature == 0.0 for p in MANIFEST.seams)


# ── refusal ──────────────────────────────────────────────────────────────────

def test_a_different_model_is_refused():
    with pytest.raises(ModelPinMismatch, match="!= pinned"):
        assert_pinned("define_axis", model_id="some-other-model")


def test_different_params_are_refused():
    with pytest.raises(ModelPinMismatch, match="params"):
        assert_pinned("define_axis", model_id="claude-opus-5",
                      params=SamplingParams(temperature=0.7))


def test_an_unpinned_seam_is_refused_rather_than_waved_through():
    """A seam nobody pinned is a seam nobody reviewed."""
    with pytest.raises(ModelPinMismatch, match="not pinned"):
        assert_pinned("some_new_seam", model_id="claude-opus-5")


def test_the_matching_configuration_passes():
    pin = assert_pinned("define_axis", model_id="claude-opus-5",
                        params=SamplingParams())
    assert pin.seam == "define_axis"


def test_the_refusal_names_the_override_so_it_is_a_decision_not_a_mystery():
    with pytest.raises(ModelPinMismatch, match=ENV_OVERRIDE):
        assert_pinned("define_axis", model_id="wrong")


def test_the_override_is_a_parameter_not_an_ambient_env_read():
    """`assert_pinned` never reads the environment itself, so a bypass is visible at the
    call site rather than in whatever shell happened to launch the run."""
    assert assert_pinned("define_axis", model_id="wrong", allow_override=True) is not None
    assert override_enabled({}) is False
    assert override_enabled({ENV_OVERRIDE: "1"}) is True
    assert override_enabled({ENV_OVERRIDE: "true"}) is False      # exactly "1", as elsewhere


# ── prompt hashing ───────────────────────────────────────────────────────────

def test_prompt_hash_ignores_trailing_whitespace_but_not_edits():
    a = "You are a credit analyst.\nReturn JSON."
    assert prompt_hash(a) == prompt_hash("You are a credit analyst.   \nReturn JSON.\n")
    assert prompt_hash(a) != prompt_hash("You are a credit analyst.\nReturn YAML.")


def test_an_unpinned_prompt_hash_is_not_asserted_rather_than_accepted_blindly():
    """`prompt_hash=None` means "not yet pinned". The model and params are still checked,
    so the guard is useful before the prompts settle without refusing every live call."""
    assert MANIFEST.pin_for("define_axis").prompt_hash is None
    assert_pinned("define_axis", model_id="claude-opus-5", prompt_text="anything at all")


def test_a_pinned_prompt_hash_is_enforced():
    manifest = ModelManifest(
        version="test", verifier_model_id="claude-sonnet-5",
        seams=(SeamPin(seam="define_axis", model_id="claude-opus-5",
                       prompt_hash=prompt_hash("the reviewed prompt")),))
    assert_pinned("define_axis", model_id="claude-opus-5",
                  prompt_text="the reviewed prompt", manifest=manifest)
    with pytest.raises(ModelPinMismatch, match="prompt hash"):
        assert_pinned("define_axis", model_id="claude-opus-5",
                      prompt_text="the edited prompt", manifest=manifest)


# ── D3: verifier independence ────────────────────────────────────────────────

def test_the_manifest_refuses_a_verifier_that_is_also_a_proposer():
    """D3: a different prompt on the same model shares the failure mode it is meant to
    catch."""
    with pytest.raises(ValueError, match="D3"):
        ModelManifest(version="test", verifier_model_id="claude-opus-5",
                      seams=(SeamPin(seam="define_axis", model_id="claude-opus-5"),))


def test_the_shipped_manifest_has_an_independent_verifier():
    assert MANIFEST.verifier_model_id not in {p.model_id for p in MANIFEST.seams}


def test_assert_verifier_independent_refuses_a_self_check():
    assert_verifier_independent("claude-opus-5", "claude-sonnet-5")
    with pytest.raises(ModelPinMismatch, match="D3"):
        assert_verifier_independent("claude-opus-5", "claude-opus-5")


def test_a_seam_cannot_be_pinned_twice():
    with pytest.raises(ValueError, match="pinned twice"):
        ModelManifest(version="test", verifier_model_id="claude-sonnet-5",
                      seams=(SeamPin(seam="define_axis", model_id="claude-opus-5"),
                             SeamPin(seam="define_axis", model_id="claude-opus-5")))
