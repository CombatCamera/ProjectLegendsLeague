"""
Project LegendsLeague
Matchup Simulator

Purpose:
    Run repeated simulated plate appearances using normalized matchup
    outcome probabilities.

Responsibilities:
    - Resolve each simulated plate appearance through the outcome resolver.
    - Count strikeouts, walks, hit types, and other outs.
    - Aggregate repeated simulation results into outcome totals.
    - Provide reusable simulation logic for matchup analysis and reporting.

Simulation Outcomes:
    - Strikeout
    - Walk
    - Single
    - Double
    - Triple
    - Home Run
    - Other Out

Design Principle:
    The simulator samples from the normalized matchup probability model
    without changing the underlying expected probabilities.
"""

# =============================
# IMPORTS
# =============================

from python.simulation.plate_appearance_resolver import (
    resolve_plate_appearance,
)


# =============================
# FUNCTIONS
# =============================

def simulate_matchup(
    matchup_outcome_probabilities,
    number_of_plate_appearances,
):
    outcome_counts = {
        "strikeout": 0,
        "walk": 0,
        "single": 0,
        "double": 0,
        "triple": 0,
        "home_run": 0,
        "other_out": 0,
    }

    for _ in range(number_of_plate_appearances):
        outcome = resolve_plate_appearance(
            matchup_outcome_probabilities
        )
        outcome_counts[outcome] += 1

    return outcome_counts
