"""
Project LegendsLeague
Plate Appearance Metrics

Purpose:
    Calculate total plate appearances from core batting statistics.

Responsibilities:
    - Combine at-bats, walks, hit-by-pitches, sacrifice hits, and sacrifice flies.
    - Support historical player and league plate appearance calculations.
    - Provide a reusable plate appearance metric for downstream normalization.

Calculation:
    Plate Appearances = AB + BB + HBP + SH + SF
"""

# =======================================================
# FUNCTION
# =======================================================

def calculate_plate_appearances(AB, BB, HBP, SH, SF=0):

    plate_appearances = AB + BB + HBP + SH + SF

    return plate_appearances
