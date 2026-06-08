"""Skill registry — loads METHOD skill cards from .claude/skills/ and maps Provider seams to
the cards that guide them. Only .claude/skills/ cards are loaded here; NO case pages, ever.
Fail closed: a seam that declares required skills raises if a card is missing.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / ".claude" / "skills"

# Provider seam → required skill cards (METHOD only).
SEAM_TO_SKILLS: dict[str, list[str]] = {
    "classify_iceberg": ["iceberg-classifier"],
    "parse_research_text": ["iceberg-classifier", "causal-compiler"],
    "expand_causal": ["causal-compiler"],
    "define_axis": ["causal-compiler", "scenario-pricing-engine"],
    "build_system_map": ["system-mapper"],
    "diagnose_loops": ["trap-detector"],
    "critique_mental_model": ["causal-compiler", "trap-detector"],
    "justify_probabilities": ["scenario-pricing-engine"],
    "run_pricing": ["scenario-pricing-engine"],
    "macro_context": ["macro-regime-classifier"],
}

# Newly compiled cards are REGISTERED (discoverable + loadable) but deliberately NOT added to
# SEAM_TO_SKILLS — i.e. not auto-wired into any live seam this PR.
#  - evidence-weighting: PENDING the Q4 posterior≠prior derivation (separate PR); must not feed
#    ConfidenceComponents yet.
#  - priced-in-estimator / edge-validity: READABLE in discovery as method context, but not
#    injected (they must not change any golden-master numerical output).
PENDING_WIRING_SKILLS = ("evidence-weighting",)
READABLE_DISCOVERY_SKILLS = ("priced-in-estimator", "edge-validity")

# Batch 4: six method cards compiled from the research/ papers (Hamilton, Stock-Watson,
# Giannone-Reichlin, Matheson, Vayanos-Vila, Brunner-Meltzer, Koopman-Wang-Wei) and the causal /
# factor / calibration books (Hernán-Robins, Angrist-Pischke, VanderWeele, Pearl, Ilmanen,
# Gneiting). REGISTERED + discoverable + loadable, but deliberately NOT added to SEAM_TO_SKILLS:
# the seam-mapping tests assert exact equality and the golden master must not change. Readable
# method context only; they mirror their engine specs in wiki/engines/.
REGISTERED_UNWIRED_SKILLS = (
    "macro-state-parser", "term-premium-estimator", "backdoor-identifiability-gate",
    "global-io-network", "factor-r2-router", "outcome-calibration-engine",
)

_REQUIRED_FRONTMATTER = ("skill_name", "access_class", "pipeline_phase", "provider_seam",
                         "input_objects", "output_objects")
# Sections kept when condensing for a prompt (token budget).
_CONDENSE = ("Purpose", "Inputs", "Outputs", "Validation rules", "Non-goals", "Example output")


class MissingSkillCard(RuntimeError):
    """Raised when a required skill card is absent — fail closed."""


def _card_path(slug: str) -> Path:
    return SKILLS_DIR / slug / "SKILL.md"


def load_skill_card(skill_slug: str) -> str:
    """Read .claude/skills/<slug>/SKILL.md. Fail closed if absent."""
    path = _card_path(skill_slug)
    if not path.exists():
        raise MissingSkillCard(f"missing skill card: {skill_slug} ({path})")
    return path.read_text(encoding="utf-8")


def list_available_skills() -> list[str]:
    if not SKILLS_DIR.exists():
        return []
    return sorted(p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md"))


def load_skills_for_seam(seam_name: str) -> list[str]:
    """Return the skill-card texts required for a seam (fail closed on any missing card).
    A seam with no mapping returns []."""
    return [load_skill_card(slug) for slug in SEAM_TO_SKILLS.get(seam_name, [])]


def skills_for_seam(seam_name: str) -> list[str]:
    """The skill slugs a seam declares (no I/O)."""
    return list(SEAM_TO_SKILLS.get(seam_name, []))


def _frontmatter(card_text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", card_text, re.DOTALL)
    if not m:
        return {}
    out: dict = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def validate_skill_frontmatter(card_text: str) -> bool:
    """True iff the card has the required frontmatter keys and access_class=method."""
    fm = _frontmatter(card_text)
    if not all(k in fm and fm[k] for k in _REQUIRED_FRONTMATTER):
        return False
    return fm.get("access_class") == "method"


def card_hash(card_text: str) -> str:
    return hashlib.sha256(card_text.encode("utf-8")).hexdigest()[:16]


def condense_card(card_text: str) -> str:
    """Keep only the token-budget sections (Purpose/Inputs/Outputs/Validation rules/Non-goals/
    Example output) + the skill_name, for injection as prompt context."""
    fm = _frontmatter(card_text)
    name = fm.get("skill_name", "skill")
    blocks = re.split(r"\n## ", card_text)
    kept = [f"# skill: {name}"]
    for blk in blocks[1:]:
        title = blk.split("\n", 1)[0].strip()
        if any(title.startswith(sec) for sec in _CONDENSE):
            kept.append("## " + blk.rstrip())
    return "\n\n".join(kept)
