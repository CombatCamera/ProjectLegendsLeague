"""
Project LegendsLeague
Matchup Metrics

Purpose:
    Combine normalized batter, pitcher, and neutral-era probabilities
    into a single matchup probability.

Responsibilities:
    - Convert batter, pitcher, and neutral probabilities into odds.
    - Combine player effects relative to the neutral environment.
    - Convert the resulting matchup odds back into probability form.
    - Reject invalid zero neutral probabilities.
    - Provide reusable matchup probability logic for cross-era simulation.

Design Principle:
    Batter and pitcher performance are combined relative to a shared
    neutral baseline so neither player's original era is treated as
    the default environment.
"""

# ==============================================
# IMPORTS
# ==============================================

from python.helpers.probability_metrics import (
    calculate_odds,
    calculate_probability_from_odds
)

# ==============================================
# FUNCTIONS
# ==============================================

def calculate_matchup_probability(
    batter_probability,
    pitcher_probability,
    neutral_probability
):

    if neutral_probability == 0:
        raise ValueError(
            "Neutral probability must be greater than 0."
        )

    batter_odds = calculate_odds(batter_probability)

    pitcher_odds = calculate_odds(pitcher_probability)

    neutral_odds = calculate_odds(neutral_probability)


    matchup_odds = (batter_odds * pitcher_odds) / neutral_odds

    matchup_probability = calculate_probability_from_odds(
        matchup_odds
    )

    return matchup_probability
