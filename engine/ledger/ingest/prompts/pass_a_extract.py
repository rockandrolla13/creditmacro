"""Pass A extraction prompt (blind — the document only; no theme registry, I2)."""

EXTRACT_SYSTEM = (
    "You extract atomic market claims from a single research document. "
    "You output JSON only, with no commentary."
)

EXTRACT_PROMPT = """Document {doc_id} from {institution}, dated {doc_date}.

Extract every atomic market claim. One object per (market_variable, direction, horizon):
  - market_variable: a tracked axis id or a terminal market term
  - direction: +1 (up/wider), -1 (down/tighter), or 0 (conditional/neutral)
  - horizon_days: integer
  - stated_conviction: 1, 2, or 3 (from the document's own language)
  - mechanism_tags: a subset of the transmission vocabulary below
  - text: a one-sentence paraphrase

Do NOT summarize the document's overall stance; extract atomic claims only.

Transmission vocabulary: {vocab}

Return JSON: {{"claims": [ ... ]}}

DOCUMENT:
{text}
"""
