"""
Project LegendsLeague
Strikeout Metrics Validation

Purpose:
    Validate the strikeout tendency calculation used by LegendsLeague.

Responsibilities:
    - Confirm strikeout tendency is calculated correctly from strikeouts
      and plate appearances.
    - Validate the expected historical-style result.
    - Protect downstream normalization calculations from regression.

Validation Case:
    Strikeouts: 42
    Plate Appearances: 654
    Expected Strikeout Tendency: 0.0642
"""

# =======================================
# IMPORTS
# =======================================

from python.calculations.strikeout_metrics import calculate_strikeout_tendency


# =======================================
# FUNCTION
# =======================================

def validate_strikeout_tendency():

    strikeouts = 42
    plate_appearances = 654

    calculated_tendency = calculate_strikeout_tendency(
        strikeouts,
        plate_appearances
    )

    rounded_tendency = round(calculated_tendency, 4)

    if rounded_tendency != 0.0642:
        raise AssertionError(
            f"Strikeout Tendency Validation Failed. "
            f"Expected: 0.0642, Got: {rounded_tendency}"
        )

    print(
        f"Strikeout Tendency Validation Passed. "
        f"Calculated Strikeout Tendency: {rounded_tendency}"
    )
