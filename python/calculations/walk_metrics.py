"""
Project LegendsLeague
Walk Metrics

Purpose:
    Calculate walk tendency from total walks and total encounters.

Responsibilities:
    - Convert walk totals into a probability-style walk tendency.
    - Safely handle zero-encounter inputs.
    - Provide a reusable walk metric for league, player, and matchup calculations.
"""

# =============================================
# FUNCTION
# =============================================

def calculate_walk_tendency(walks, encounters):

    if encounters == 0:
        return 0.0
    return walks / encounters
