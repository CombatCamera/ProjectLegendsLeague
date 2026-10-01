"""
Project LegendsLeague
Probability Metrics Validation

Purpose:
    Validate the probability and odds conversion helpers used by
    LegendsLeague matchup calculations.

Responsibilities:
    - Confirm probability-to-odds conversion produces expected results.
    - Confirm odds-to-probability conversion produces expected results.
    - Validate upper and lower probability boundaries.
    - Validate lower odds boundaries.
    - Confirm invalid input types are rejected.
    - Protect downstream probability calculations from invalid inputs.

Validation Strategy:
    Controlled numeric inputs are used to verify known probability and
    odds conversions, while invalid boundary and type inputs are used to
    confirm defensive error handling.
"""

# ====================================================
# IMPORTS
# ====================================================

import math
from python.helpers.probability_metrics import (
    calculate_odds,
    calculate_probability_from_odds,
)


# ====================================================
# FUNCTIONS
# ====================================================

def validate_odds():

    expected_odds = 0.25

    player_probability = 0.20

    player_odds = calculate_odds(player_probability)

    if not math.isclose(player_odds, expected_odds):
        raise AssertionError(
            "Test failed, player odds do not match expected odds."
        )

    print("Test Passed, player odds match expected odds.")
    print(f"Expected odds: {expected_odds}")
    print(f"Player odds: {player_odds}")

    return player_odds


def validate_probability(player_odds):

    expected_probability = 0.20

    player_probability = calculate_probability_from_odds(player_odds)

    if not math.isclose(player_probability, expected_probability):
        raise AssertionError(
            "Test Failed, player probability does not match expected probability."
        )

    print("Test Passed, player probability matches expected probability.")
    print(f"Expected Probability: {expected_probability}")
    print(f"Player probability: {player_probability}")

    return player_probability


def validate_probability_upper_boundary():

    invalid_probability = 1.0

    try:
        calculate_odds(invalid_probability)

    except ValueError:
        print("PASS: Probability upper boundary rejected 1.0.")
        return


    raise AssertionError(
        "Test Failed: Expected error was not raised."
    )


def validate_probability_lower_boundary():

    invalid_probability = -0.01

    try:
        calculate_odds(invalid_probability)

    except ValueError:
        print("PASS: Probability lower boundary rejected -0.01.")
        return

    raise AssertionError(
        "Test Failed: Expected error was not raised."
    )


def validate_odds_lower_boundary():

    invalid_odds = -0.01

    try:
        calculate_probability_from_odds(invalid_odds)

    except ValueError:
        print("PASS: Odds lower boundary rejected -0.01.")
        return

    raise AssertionError(
        "Test Failed: Expected error was not raised."
    )


def validate_probability_type():

    invalid_probability = "0.20"

    try:
        calculate_odds(invalid_probability)

    except TypeError:
        print("PASS: probability type rejected 0.20.")
        return

    raise AssertionError(
        "Test Failed: Expected error was not raised."
    )


def validate_odds_type():

    invalid_odds = "0.25"

    try:
        calculate_probability_from_odds(invalid_odds)

    except TypeError:
        print("PASS: odds type rejected 0.25.")
        return

    raise AssertionError(
        "Test Failed: Expected error was not raised."
    )


# ====================================================
# MAIN
# ====================================================

def main():

    print("========================================")

    print()

    player_odds = validate_odds()

    print()

    validate_probability(player_odds)

    print()

    validate_probability_upper_boundary()

    print()

    validate_probability_lower_boundary()

    print()

    validate_odds_lower_boundary()

    print()

    validate_probability_type()

    print()

    validate_odds_type()

    print()

    print("========================================")

if __name__ == "__main__":
    main()
