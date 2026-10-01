"""
Project LegendsLeague
Hit Metrics

Purpose:
    Calculate hit tendency from total hits and total encounters.

Responsibilities:
    - Convert hit totals into a probability-style hit tendency.
    - Safely handle zero-encounter inputs.
    - Provide a reusable hit metric for league, player, and matchup calculations.
"""

#==============================================
# FUNCTION
# =============================================
def calculate_hit_tendency(hits, encounters):

    if encounters == 0:
        return 0.0
    return hits/encounters
