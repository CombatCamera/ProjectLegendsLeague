"""
Project LegendsLeague
Relative Metrics

Purpose:
    Calculate player performance relative to a comparison baseline.

Responsibilities:
    - Calculate a relative performance rate.
    - Convert relative rates below baseline into avoidance percentages.
    - Convert relative rates above baseline into generation percentages.
    - Provide reusable relative metrics for era-normalized player analysis.

Design Principle:
    Player performance is measured relative to the surrounding league
    environment before being translated into a neutral matchup context.
"""

#==========================================
# FUNCTIONS
# =========================================

def relative_rate(value, comparison_value):

    return value / comparison_value


def relative_avoidance(relative_rate):

    return (1 - relative_rate) * 100


def relative_generation(relative_rate):

    return (relative_rate - 1) * 100
