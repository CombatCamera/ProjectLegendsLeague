"""
Project LegendsLeague
Strikeout Metrics

Purpose:
    Calculate strikeout tendency from total strikeouts and total encounters.

Responsibilities:
    - Convert strikeout totals into a probability-style strikeout tendency.
    - Safely handle zero-encounter inputs.
    - Provide a reusable strikeout metric for league, player, and matchup calculations.
"""

# ==========================================================
# FUNCTION
# ==========================================================

def calculate_strikeout_tendency(strikeouts, encounters):

    if encounters == 0:
        return 0.0
    return (strikeouts / encounters)
