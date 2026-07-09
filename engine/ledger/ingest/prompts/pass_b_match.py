"""Pass B semantic-match prompt (definitions only, I3).

The model rates how strongly a claim is evidence about a theme's transmission
mechanism/axis — a confidence in [0,1]. It is NEVER asked for a direction or an
agree/disagree sign: that is computed downstream from the claim direction and the
theme's derived direction.
"""

MATCH_SYSTEM = (
    "You judge how strongly a market claim is evidence about a theme's transmission "
    "mechanism and operational axis. You output JSON only, with no commentary."
)

MATCH_PROMPT = """THEME mechanism nodes: {nodes}
THEME operational axis: {axis}

CLAIM market_variable: {market_variable}
CLAIM mechanism_tags: {tags}
CLAIM text: {text}

Rate from 0.0 to 1.0 how strongly this claim is evidence about the theme's
mechanism and axis (0 = unrelated, 1 = squarely about this transmission).

Return JSON: {{"match_confidence": <float between 0 and 1>}}
"""
