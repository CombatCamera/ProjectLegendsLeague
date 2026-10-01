"""
Project LegendsLeague
Probability Metrics

Purpose:
    Convert between probability values and odds for matchup calculations.

Responsibilities:
    - Convert probabilities into odds.
    - Convert odds back into probabilities.
    - Reject invalid probability values.
    - Reject negative odds.
    - Reject non-numeric inputs.
    - Provide reusable probability helpers for normalization and matchup logic.

Validation Rules:
    - Probability must be greater than or equal to 0 and less than 1.
    - Odds must be greater than or equal to 0.
"""

#=========================================
# FUNCTIONS
# ========================================

def calculate_odds(probability):

    if not isinstance(probability, (int, float)):
        raise TypeError(
            "Probability must be a number."
        )

    if probability < 0 or probability >= 1:
        raise ValueError(
            "Probability must be greater than or equal to 0 and less than 1."
        )

    odds = probability / (1 - probability)

    return odds


def calculate_probability_from_odds(odds):

    if not isinstance(odds, (int, float)):
        raise TypeError(
            "odds must be a number."
        )

    if odds < 0:
        raise ValueError(
            "Odds must be greater than or equal to 0."
        )

    probability = odds / (1 + odds)

    return probability
