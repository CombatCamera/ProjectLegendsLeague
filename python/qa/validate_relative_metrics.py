"""
Project LegendsLeague
Relative Metrics Validation

Purpose:
    Validate the relative avoidance calculation used by LegendsLeague
    normalization logic.

Responsibilities:
    - Confirm relative-rate calculations feed correctly into relative avoidance.
    - Validate below-baseline, equal-baseline, and above-baseline cases.
    - Confirm expected positive, zero, and negative avoidance results.
    - Protect downstream player normalization calculations from regression.

Validation Cases:
    - Value below comparison baseline
    - Value equal to comparison baseline
    - Value above comparison baseline
"""

# ========================================
# IMPORTS
# ========================================

from python.helpers.relative_metrics import relative_rate, relative_avoidance

# ========================================
# FUNCTION
# ========================================

def validate_relative_avoidance():

    test_cases = [
        (5, 10, 50.0),
        (10, 10, 0.0),
        (15, 10, -50.0),

    ]

    for value, comparison_value, expected_relative_avoidance in test_cases:

        relative_ratio = relative_rate(value, comparison_value)
        test_relative_avoidance = relative_avoidance(relative_ratio)

        print(f"Test Relative Avoidance: {test_relative_avoidance}")
        print(f"Expected Relative Avoidance: {expected_relative_avoidance}")
        print()

        if test_relative_avoidance != expected_relative_avoidance:
            raise AssertionError(
                "FAIL: Relative avoidance function is not working correctly."
            )

        print("PASS: Relative avoidance function is working correctly.")
