"""
Project LegendsLeague
Plate Appearance Calculation Validation

Purpose:
    Validate the plate appearance calculation used by LegendsLeague.

Responsibilities:
    - Confirm the plate appearance formula produces the expected result.
    - Use controlled historical-style inputs for verification.
    - Protect downstream player and league calculations from regression.

Validation Case:
    Inputs:
        AB = 591
        BB = 44
        HBP = 8
        SH = 11
        SF = 0

    Expected Plate Appearances:
        654
"""

# ========================================
# IMPORTS
# ========================================

from python.calculations.plate_appearances import calculate_plate_appearances

# ========================================
# FUNCTIONS
# ========================================

def validate_plate_appearances():
    calculated_plate_appearances = calculate_plate_appearances(591, 44, 8, 11, 0)

    if calculated_plate_appearances != 654:
        raise AssertionError(
            f"Plate Appearance Validation Failed. "
            f"Expected: 654, Got: {calculated_plate_appearances}"
        )
    print(
        f"Plate Appearance Validation Passed. "
        f"Calculated Plate Appearances: {calculated_plate_appearances}"
    )
