"""
Project LegendsLeague
Normalization Metrics Validation

Purpose:
    Validate the probability calculations used to normalize historical
    player performance and construct cross-era matchup outcomes.

Responsibilities:
    - Validate neutral-era probability calculations.
    - Validate neutral player probability calculations.
    - Validate matchup hit-type probability normalization.
    - Confirm conditional hit-type probabilities sum to 1.0.
    - Validate conversion from conditional hit probabilities to overall
      plate-appearance probabilities.
    - Validate calculation of the Other Out probability.
    - Confirm the complete matchup outcome distribution sums to 1.0.

Validated Outcomes:
    - Strikeout
    - Walk
    - Single
    - Double
    - Triple
    - Home Run
    - Other Out

Validation Principle:
    Controlled inputs are used to produce known expected results so each
    normalization step can be verified independently before being used
    by the matchup simulation engine.
"""


# ======================================================
# IMPORTS
#=======================================================

import math

from python.helpers.normalization_metrics import (
    calculate_neutral_probability,
    calculate_neutral_player_probability,
    calculate_matchup_hit_type_probabilities,
    calculate_overall_hit_type_probabilities,
    calculate_other_outs,
)


# ======================================================
# FUNCTIONS
#=======================================================

def validate_neutral_probability():

    first_era_probability = 0.09

    second_era_probability = 0.16

    expected_neutral_probability = 0.12

    test_neutral_probability = calculate_neutral_probability(
        first_era_probability,
        second_era_probability
    )

    if not math.isclose(
        test_neutral_probability,
        expected_neutral_probability
    ):
        raise AssertionError("Test Failed, neutral probabilities did not match.")
    else:
        print("Test Passed, neutral probability matches expected probability.")
        print(f"Test neutral probability: {test_neutral_probability}")
        print(f"Expected neutral probability: {expected_neutral_probability}")


def validate_neutral_player_probability():

    neutral_probability = 0.12

    relative_factor = 0.50

    expected_result = 0.06


    neutral_player_probability = calculate_neutral_player_probability(
        neutral_probability,
        relative_factor
    )

    if not math.isclose(
        neutral_player_probability,
        expected_result
    ):
        raise AssertionError("Test Failed, neutral player probability does not match expected results.")
    else:
        print("Test Passed, neutral player probability matches expected results.")
        print(f"Neutral player probability: {neutral_player_probability}")
        print(f"Expected results: {expected_result}")


   # ======================================================
   # MAIN
   #=======================================================


def validate_matchup_hit_type_probabilities():

    batter_relative_hit_factors = {
        "single": 1.0,
        "double": 2.0,
        "triple": 1.0,
        "home_run": 2.0,
    }

    pitcher_relative_hit_factors = {
        "single": 1.0,
        "double": 1.0,
        "triple": 3.0,
        "home_run": 1.0,
    }

    expected_probabilities = {
        "single": 1 / 8,
        "double": 2 / 8,
        "triple": 3 / 8,
        "home_run": 2 / 8
    }

    actual_probabilities = calculate_matchup_hit_type_probabilities(
        batter_relative_hit_factors,
        pitcher_relative_hit_factors,
    )
    for hit_type in expected_probabilities:
        if not math.isclose(
            actual_probabilities[hit_type],
            expected_probabilities[hit_type],
        ):
            raise AssertionError(
                f"Test Fail: {hit_type} probability did not match."
            )
    print(
        f"Test Passed: Actual probabilites {actual_probabilities} "
        f"and expected probabilities {expected_probabilities} match."
    )

    total_probability = sum(
        actual_probabilities.values()
    )

    if not math.isclose(total_probability, 1.0):
        raise AssertionError(
            "Test Failed: Matchup hit type probabilities did not sum to 1.0"
        )
    print("Test Passed: matchup hit type probabilities summed to 1.0")


def validate_overall_hit_type_probabilities():

    matchup_hit_probability = 0.40

    matchup_hit_type_probabilities = {
        "single": 0.25,
        "double": 0.25,
        "triple": 0.25,
        "home_run": 0.25,
    }

    expected_probabilities = {
        "single": 0.10,
        "double": 0.10,
        "triple": 0.10,
        "home_run": 0.10,
    }

    actual_probabilities = calculate_overall_hit_type_probabilities(
        matchup_hit_probability,
        matchup_hit_type_probabilities,
    )

    if actual_probabilities != expected_probabilities:
        raise AssertionError(
            "Test Failed: Probabilities did not match."
        )
    print(
        f"Test Passed: Actual probabilities {actual_probabilities} "
        f"matched expected probabilities {expected_probabilities}"
    )


    total_hit_type_probability = sum(
        actual_probabilities.values()
    )

    if not math.isclose(
        total_hit_type_probability,
        matchup_hit_probability,
    ):
        raise AssertionError(
            f"Test Fialed: Probabilities did not sum to {matchup_hit_probability}"
        )

    print(
        f"Test Passed: probabilities summed to {matchup_hit_probability}"
    )


def validate_other_out_probability():

    strikeout_probability = 0.10
    walk_probability = 0.10
    single_probability = 0.10
    double_probability = 0.10
    triple_probability = 0.10
    home_run_probability = 0.10

    expected_other_out_probability = 0.40

    actual_other_out_probability = calculate_other_outs(
        strikeout_probability,
        walk_probability,
        single_probability,
        double_probability,
        triple_probability,
        home_run_probability,
    )

    if not math.isclose(
        actual_other_out_probability,
        expected_other_out_probability,
    ):
        raise AssertionError(
            "Test Failed: Probabilities did not match"
        )
    print(
        f"Test Passed: Actual other out probability "
        f"{actual_other_out_probability:.2f} "
        f"matched expected probability "
        f"{expected_other_out_probability:.2f}."
    )


def validate_matchup_outcome_probabilities():

    matchup_outcome_probabilities = {
        "strikeout": 0.10,
        "walk": 0.10,
        "single": 0.10,
        "double": 0.10,
        "triple": 0.10,
        "home_run": 0.10,
        "other_out": 0.40,
    }

    total_probability = sum(
        matchup_outcome_probabilities.values()
    )


    if not math.isclose(total_probability, 1.0):
        raise AssertionError(
            "Test Failed: Probabilities did not sum to 1.0."
        )
    print(f"Test Passed: total probability, {total_probability}, summed to 1.0.")


# ======================================================
# MAIN
#=======================================================

def main():

    print("========================================")

    print()

    validate_neutral_probability()

    print()

    validate_neutral_player_probability()

    print()

    validate_matchup_hit_type_probabilities()

    print()

    validate_overall_hit_type_probabilities()

    print()

    validate_other_out_probability()

    print()

    validate_matchup_outcome_probabilities()

    print()

    print("========================================")

if __name__ == "__main__":
    main()
