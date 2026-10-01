"""
Project LegendsLeague
Matchup Simulation Pipeline

Purpose:
    Run a normalized historical player matchup through the LegendsLeague
    simulation engine and present the expected and observed outcome results.

Responsibilities:
    - Build the normalized matchup outcome probabilities.
    - Run a configurable number of simulated plate appearances.
    - Calculate observed simulation percentages.
    - Compare observed outcomes against expected matchup probabilities.
    - Present a human-readable matchup results table.
    - Summarize the overall batter-versus-pitcher matchup probabilities.

Current Matchup:
    Ty Cobb (1911) vs. Nolan Ryan (1973)

Simulation Outcomes:
    - Strikeout
    - Walk
    - Single
    - Double
    - Triple
    - Home Run
    - Other Out

Design Principle:
    Normalization determines the expected matchup probabilities.
    Simulation tests those probabilities through repeated stochastic
    plate appearances without modifying the underlying model.

Output:
    Expected probability → Simulated frequency → Difference

Notes:
    The matchup summary defines:
        - Pitcher win: Strikeout or Other Out
        - Batter win: Walk or Hit

    Simulation results will vary between runs due to randomness, while
    the normalized expected probabilities remain constant.
"""

# ====================================================
# IMPORTS
# ====================================================

from python.simulation.matchup_simulator import simulate_matchup

from python.pipelines.normalization_pipeline import (
    main as build_normalized_matchup,
)


# ====================================================
# CONFIG
# ====================================================

DEFAULT_PLATE_APPEARANCES = 10000

OUTCOME_DISPLAY_NAME = {
    "strikeout": "Strikeout",
    "walk": "Walk",
    "single": "Single",
    "double": "Double",
    "triple": "Triple",
    "home_run": "Home Run",
    "other_out": "Other Out",
}


# ====================================================
# MAIN
# ====================================================

def main():

    matchup_outcome_probabilities = build_normalized_matchup(
        verbose=False,
    )

    simulation_results = simulate_matchup(
        matchup_outcome_probabilities,
        DEFAULT_PLATE_APPEARANCES,
    )

    simulation_percentages = {}

    for outcome, count in simulation_results.items():
        simulation_percentages[outcome] = (
            count / DEFAULT_PLATE_APPEARANCES
        )

    print("\nTy Cobb 1911 vs Nolan Ryan 1973")
    print("================================")
    print(f"Plate Appearances: {DEFAULT_PLATE_APPEARANCES:,}")
    print()
    print(
        f"{'Outcome':<12}"
        f"{'Expected':>12}"
        f"{'Observed':>12}"
        f"{'Difference':>12}"
    )
    print("-" * 48)

    ryan_win_probability = (
        matchup_outcome_probabilities["strikeout"]
        + matchup_outcome_probabilities["other_out"]
    )

    cobb_win_probability = (
        matchup_outcome_probabilities["walk"]
        + matchup_outcome_probabilities["single"]
        + matchup_outcome_probabilities["double"]
        + matchup_outcome_probabilities["triple"]
        + matchup_outcome_probabilities["home_run"]
    )

    for outcome in matchup_outcome_probabilities:
        expected = matchup_outcome_probabilities[outcome]
        observed = simulation_percentages[outcome]
        display_name = OUTCOME_DISPLAY_NAME[outcome]

        probability_difference = (
            observed
            - expected
        )

        print(
            f"{display_name:<12}"
            f"{expected * 100:>11.2f}%"
            f"{observed * 100:>11.2f}%"
            f"{probability_difference * 100:+11.2f}%"
        )

    print("=" * 48)
    print()
    print("Matchup Summary")
    print("=" * 48)
    print(
        f"Nolan Ryan Win Probability: "
        f"{ryan_win_probability * 100:.2f}%"
    )
    print(
        f"Ty Cobb Win Probability:    "
        f"{cobb_win_probability * 100:.2f}%"
    )
    print("=" * 48)
    print()



if __name__ == "__main__":
    main()
