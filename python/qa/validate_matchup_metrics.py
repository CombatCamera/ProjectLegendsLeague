"""
Project LegendsLeague
Matchup Metrics Validation

Purpose:
    Validate the probability calculations used to combine normalized
    batter and pitcher tendencies into a single matchup probability.

Responsibilities:
    - Validate standard batter-versus-pitcher matchup probability calculations.
    - Confirm expected behavior when the pitcher matches the neutral baseline.
    - Confirm expected behavior when both players match the neutral baseline.
    - Validate the current Cobb-versus-Ryan strikeout matchup calculation.
    - Confirm invalid zero-neutral-probability inputs are rejected.

Validation Strategy:
    Controlled probabilities are used to produce known expected matchup
    results so the matchup calculation can be verified independently
    before being used by the normalization pipeline.

Current Matchup Check:
    Ty Cobb (1911) vs. Nolan Ryan (1973)
"""

# ==============================================
# IMPORTS
# ==============================================

import math
from python.calculations.matchup_metrics import (
    calculate_matchup_probability,
)


# ==============================================
# FUNCTIONS
# ==============================================

def validate_matchup_probability():

    batter_probability = 0.20

    pitcher_probability = 0.50

    neutral_probability = 0.20

    expected_matchup = 0.50

    matchup_probability = calculate_matchup_probability(
        batter_probability,
        pitcher_probability,
        neutral_probability,
    )

    if not math.isclose(
        matchup_probability,
        expected_matchup
    ):
        raise AssertionError("Test Failed, matchup probability and expected result do not match.")
    else:
        print("Test Passed, matchup probability matches expected result.")
        print(f"Expected Result: {expected_matchup}")
        print(f"Matchup Probability: {matchup_probability}")


def validate_neutral_pitcher_matchup():

    batter_probability = 0.40

    pitcher_probability = 0.20

    neutral_probability = 0.20

    expected_matchup = 0.40

    matchup_probability = calculate_matchup_probability(
        batter_probability,
        pitcher_probability,
        neutral_probability,
    )

    if not math.isclose(
        matchup_probability,
        expected_matchup
    ):
        raise AssertionError("Test Failed, neutral pitcher matchup result and expected result do not match.")
    else:
        print("Test Passed, neutral pitcher matchup result matches expected result.")
        print(f"Expected Result: {expected_matchup}")
        print(f"Matchup Probability: {matchup_probability}")


def validate_fully_neutral_matchup():

    batter_probability = 0.20

    pitcher_probability = 0.20

    neutral_probability = 0.20

    expected_matchup = 0.20

    matchup_probability = calculate_matchup_probability(
        batter_probability,
        pitcher_probability,
        neutral_probability,
    )

    if not math.isclose(
        matchup_probability,
        expected_matchup
    ):
        raise AssertionError("Test Failed, neutral matchup result and expected result do not match.")
    else:
        print("Test Passed, neutral matchup result matches expected result.")
        print(f"Expected Result: {expected_matchup}")
        print(f"Matchup Probability: {matchup_probability}")


def validate_cobb_ryan_strikeout_matchup():

    cobb_probability = 0.06989483792874

    ryan_probability = 0.25970835334590436

    neutral_probability = 0.11905443595322326

    expected_matchup = 0.1632318018633694

    matchup_probability = calculate_matchup_probability(
        cobb_probability,
        ryan_probability,
        neutral_probability,
    )

    if not math.isclose(
        matchup_probability,
        expected_matchup
    ):
        raise AssertionError("Test Failed, Cobb/Ryan matchup result and expected result do not match.")
    else:
        print("Test Passed, Cobb/Ryan matchup result matches expected result.")
        print(f"Expected Result: {expected_matchup}")
        print(f"Matchup Probability: {matchup_probability}")


def validate_zero_neutral_probability():

    cobb_probability = 0.20

    ryan_probability = 0.20

    neutral_probability = 0.00

    try:
        calculate_matchup_probability(
            cobb_probability,
            ryan_probability,
            neutral_probability,
        )

    except ValueError:
        print(
            "PASS: Matchup calculator rejected "
            "a zero neutral probability."
        )
        return

    raise AssertionError(
        "Test Failed: Zero Neutral Probability was not rejected."
    )


# ==============================================
# MAIN
# ==============================================

def main():

    print()

    validate_matchup_probability()

    print()

    validate_neutral_pitcher_matchup()

    print()

    validate_fully_neutral_matchup()

    print()

    validate_cobb_ryan_strikeout_matchup()

    print()

    validate_zero_neutral_probability()

    print()

if __name__ == "__main__":
    main()
