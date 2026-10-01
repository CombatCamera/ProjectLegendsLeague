"""
Project LegendsLeague
Plate Appearance Resolver Validation

Purpose:
    Validate that the plate appearance resolver maps controlled random
    values to the correct matchup outcome ranges.

Responsibilities:
    - Test each supported plate appearance outcome independently.
    - Use deterministic mocked random values.
    - Confirm cumulative probability boundaries resolve correctly.
    - Protect the simulation engine from outcome-routing regressions.

Validated Outcomes:
    - Strikeout
    - Walk
    - Single
    - Double
    - Triple
    - Home Run
    - Other Out

Validation Strategy:
    Controlled random values are injected with unittest.mock.patch so
    each probability range can be tested deterministically without relying
    on unpredictable random simulation results.
"""

# ===============================================
# IMPORTS
# ===============================================

from python.simulation.plate_appearance_resolver import resolve_plate_appearance

from unittest.mock import patch


# ===============================================
# FUNCTIONS
# ===============================================

def validate_strikeout_resolution():

    matchup_outcome_probabilities = {
        "strikeout": 0.20,
        "walk": 0.10,
        "single": 0.10,
        "double": 0.10,
        "triple": 0.10,
        "home_run": 0.10,
        "other_out": 0.30,
    }

    with patch(
        "python.simulation.plate_appearance_resolver.random.random",
        return_value=0.05,
    ):
        actual_outcome = resolve_plate_appearance(
            matchup_outcome_probabilities
        )

    expected_outcome = "strikeout"

    if actual_outcome != expected_outcome:
        raise AssertionError(
            f"Test Failed: The actual outcome did not match the expected outcome. "
        )
    print(
        f"Test Passed: The actual outcome {actual_outcome} "
        f"matched the expected outcome {expected_outcome}"
    )


def validate_walk_resolution():

    matchup_outcome_probabilities = {
        "strikeout": 0.20,
        "walk": 0.10,
        "single": 0.10,
        "double": 0.10,
        "triple": 0.10,
        "home_run": 0.10,
        "other_out": 0.30,
    }

    with patch(
        "python.simulation.plate_appearance_resolver.random.random",
        return_value=0.25,
    ):
        actual_outcome = resolve_plate_appearance(
            matchup_outcome_probabilities
        )

    expected_outcome = "walk"

    if actual_outcome != expected_outcome:
        raise AssertionError(
            f"Test Failed: The actual outcome did not match the expected outcome. "
        )
    print(
        f"Test Passed: The actual outcome {actual_outcome} "
        f"matched the expected outcome {expected_outcome}"
    )


def validate_single_resolution():

    matchup_outcome_probabilities = {
        "strikeout": 0.20,
        "walk": 0.10,
        "single": 0.10,
        "double": 0.10,
        "triple": 0.10,
        "home_run": 0.10,
        "other_out": 0.30,
    }

    with patch(
        "python.simulation.plate_appearance_resolver.random.random",
        return_value=0.35,
    ):
        actual_outcome = resolve_plate_appearance(
            matchup_outcome_probabilities
        )

    expected_outcome = "single"

    if actual_outcome != expected_outcome:
        raise AssertionError(
            f"Test Failed: The actual outcome did not match the expected outcome. "
        )
    print(
        f"Test Passed: The actual outcome {actual_outcome} "
        f"matched the expected outcome {expected_outcome}"
    )


def validate_double_resolution():

    matchup_outcome_probabilities = {
        "strikeout": 0.20,
        "walk": 0.10,
        "single": 0.10,
        "double": 0.10,
        "triple": 0.10,
        "home_run": 0.10,
        "other_out": 0.30,
    }

    with patch(
        "python.simulation.plate_appearance_resolver.random.random",
        return_value=0.45,
    ):
        actual_outcome = resolve_plate_appearance(
            matchup_outcome_probabilities
        )

    expected_outcome = "double"

    if actual_outcome != expected_outcome:
        raise AssertionError(
            f"Test Failed: The actual outcome did not match the expected outcome. "
        )
    print(
        f"Test Passed: The actual outcome {actual_outcome} "
        f"matched the expected outcome {expected_outcome}"
    )


def validate_triple_resolution():

    matchup_outcome_probabilities = {
        "strikeout": 0.20,
        "walk": 0.10,
        "single": 0.10,
        "double": 0.10,
        "triple": 0.10,
        "home_run": 0.10,
        "other_out": 0.30,
    }

    with patch(
        "python.simulation.plate_appearance_resolver.random.random",
        return_value=0.55,
    ):
        actual_outcome = resolve_plate_appearance(
            matchup_outcome_probabilities
        )

    expected_outcome = "triple"

    if actual_outcome != expected_outcome:
        raise AssertionError(
            f"Test Failed: The actual outcome did not match the expected outcome. "
        )
    print(
        f"Test Passed: The actual outcome {actual_outcome} "
        f"matched the expected outcome {expected_outcome}"
    )


def validate_home_run_resolution():

    matchup_outcome_probabilities = {
        "strikeout": 0.20,
        "walk": 0.10,
        "single": 0.10,
        "double": 0.10,
        "triple": 0.10,
        "home_run": 0.10,
        "other_out": 0.30,
    }

    with patch(
        "python.simulation.plate_appearance_resolver.random.random",
        return_value=0.65,
    ):
        actual_outcome = resolve_plate_appearance(
            matchup_outcome_probabilities
        )

    expected_outcome = "home_run"

    if actual_outcome != expected_outcome:
        raise AssertionError(
            f"Test Failed: The actual outcome did not match the expected outcome. "
        )
    print(
        f"Test Passed: The actual outcome {actual_outcome} "
        f"matched the expected outcome {expected_outcome}"
    )


def validate_other_out_resolution():

    matchup_outcome_probabilities = {
        "strikeout": 0.20,
        "walk": 0.10,
        "single": 0.10,
        "double": 0.10,
        "triple": 0.10,
        "home_run": 0.10,
        "other_out": 0.30,
    }

    with patch(
        "python.simulation.plate_appearance_resolver.random.random",
        return_value=0.80,
    ):
        actual_outcome = resolve_plate_appearance(
            matchup_outcome_probabilities
        )

    expected_outcome = "other_out"

    if actual_outcome != expected_outcome:
        raise AssertionError(
            f"Test Failed: The actual outcome did not match the expected outcome. "
        )
    print(
        f"Test Passed: The actual outcome {actual_outcome} "
        f"matched the expected outcome {expected_outcome}"
    )


# ===============================================
# MAIN
# ===============================================

def main():

    print()

    validate_strikeout_resolution()
    validate_walk_resolution()
    validate_single_resolution()
    validate_double_resolution()
    validate_triple_resolution()
    validate_home_run_resolution()
    validate_other_out_resolution()

    print()

if __name__ == "__main__":
    main()
