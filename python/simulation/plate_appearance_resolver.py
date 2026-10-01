"""
Project LegendsLeague
Plate Appearance Resolver

Purpose:
    Resolve a single simulated plate appearance from the normalized
    matchup outcome probability distribution.

Responsibilities:
    - Generate a random probability value for each plate appearance.
    - Compare that value against cumulative matchup probability ranges.
    - Return exactly one supported plate appearance outcome.
    - Preserve the normalized probability distribution during simulation.

Supported Outcomes:
    - Strikeout
    - Walk
    - Single
    - Double
    - Triple
    - Home Run
    - Other Out

Design Principle:
    Each plate appearance samples from the matchup model exactly once,
    using cumulative probability thresholds to determine the outcome.
"""

# ================================
# IMPORTS
# ================================

import random


# ================================
# FUNCTIONS
# ================================

def resolve_plate_appearance(
    matchup_outcome_probabilities,
):

    random_value = random.random()

    if random_value < matchup_outcome_probabilities["strikeout"]:
        return "strikeout"

    elif random_value < (
        matchup_outcome_probabilities["strikeout"]
        + matchup_outcome_probabilities["walk"]
    ):
        return "walk"

    elif random_value < (
        matchup_outcome_probabilities["strikeout"]
        + matchup_outcome_probabilities["walk"]
        + matchup_outcome_probabilities["single"]
    ):
        return "single"

    elif random_value < (
        matchup_outcome_probabilities["strikeout"]
        + matchup_outcome_probabilities["walk"]
        + matchup_outcome_probabilities["single"]
        + matchup_outcome_probabilities["double"]
    ):
        return "double"

    elif random_value < (
        matchup_outcome_probabilities["strikeout"]
        + matchup_outcome_probabilities["walk"]
        + matchup_outcome_probabilities["single"]
        + matchup_outcome_probabilities["double"]
        + matchup_outcome_probabilities["triple"]
    ):
        return "triple"

    elif random_value < (
        matchup_outcome_probabilities["strikeout"]
        + matchup_outcome_probabilities["walk"]
        + matchup_outcome_probabilities["single"]
        + matchup_outcome_probabilities["double"]
        + matchup_outcome_probabilities["triple"]
        + matchup_outcome_probabilities["home_run"]
    ):
        return "home_run"

    else:
        return "other_out"
