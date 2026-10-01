"""
Project LegendsLeague
Matchup Simulator Validation

Purpose:
    Validate repeated plate appearance simulation and outcome aggregation.

Responsibilities:
    - Confirm repeated identical outcomes are counted correctly.
    - Confirm mixed outcomes are routed to the correct counters.
    - Validate simulated frequencies converge toward expected probabilities.
    - Protect the matchup simulation loop from counting and distribution regressions.

Validation Strategy:
    Controlled resolver outputs are used for deterministic counting tests.
    Large stochastic simulations are used for probability convergence checks.
"""

# =============================================
# IMPORTS
# =============================================

from unittest.mock import patch

from python.simulation.matchup_simulator import (
    simulate_matchup,
)

# =============================================
# FUNCTIONS
# =============================================

def validate_simulate_matchup():

    matchup_outcome_probabilities = {
        "strikeout": 0.20,
        "walk": 0.10,
        "single": 0.10,
        "double": 0.10,
        "triple": 0.10,
        "home_run": 0.10,
        "other_out": 0.30,
    }

    number_of_plate_appearances = 5

    with patch(
        "python.simulation.matchup_simulator.resolve_plate_appearance",
        return_value="strikeout"
    ):

        actual_counts = simulate_matchup(
            matchup_outcome_probabilities,
            number_of_plate_appearances,
        )

    expected_counts = {
        "strikeout": 5,
        "walk": 0,
        "single": 0,
        "double": 0,
        "triple": 0,
        "home_run": 0,
        "other_out": 0,
    }

    if actual_counts != expected_counts:
        raise AssertionError(
            "Test Failed: The actual and expected counts did not match."
        )
    print(
        f"Test Passed: Actual counts {actual_counts} "
        f"matched expected counts {expected_counts}"
    )


def validate_simulate_matchup_mixed_outcomes():

    matchup_outcome_probabilities = {
        "strikeout": 0.20,
        "walk": 0.10,
        "single": 0.10,
        "double": 0.10,
        "triple": 0.10,
        "home_run": 0.10,
        "other_out": 0.30,
    }

    number_of_plate_appearances = 5

    with patch(
        "python.simulation.matchup_simulator.resolve_plate_appearance",
        side_effect=[
            "strikeout",
            "walk",
            "single",
            "double",
            "home_run",
        ]
    ):

        actual_counts = simulate_matchup(
            matchup_outcome_probabilities,
            number_of_plate_appearances,
        )

    expected_counts = {
        "strikeout": 1,
        "walk": 1,
        "single": 1,
        "double": 1,
        "triple": 0,
        "home_run": 1,
        "other_out": 0,
    }

    if actual_counts != expected_counts:
        raise AssertionError(
            "Test Failed: Actual and expected counts did not match."
        )
    print(
        f"Test Passed: Actual counts {actual_counts} "
        f"matched expected counts {expected_counts}"
    )


def validate_simulation_convergence():

    matchup_outcome_probabilities = {
        "strikeout": 0.20,
        "walk": 0.10,
        "single": 0.10,
        "double": 0.10,
        "triple": 0.10,
        "home_run": 0.10,
        "other_out": 0.30,
    }

    number_of_plate_appearances = 10000

    simulation_results = simulate_matchup(
        matchup_outcome_probabilities,
        number_of_plate_appearances,
    )

    simulation_percentages = {}

    for outcome, count in simulation_results.items():
        simulation_percentages[outcome] = (
            count
            / number_of_plate_appearances
        )

    tolerance = 0.01

    for outcome in matchup_outcome_probabilities:
        expected_probability = matchup_outcome_probabilities[outcome]
        observed_probability = simulation_percentages[outcome]

        probability_differences = abs(
            observed_probability
            - expected_probability
        )

        if probability_differences > tolerance:
            raise AssertionError(
                f"Test Failed: {outcome} simulation did not converge within tolerance."
            )

    print(
        "Test Passed: All simulated outcome probabilities "
        "converged within the allowed tolerance."
    )


# =============================================
# MAIN
# =============================================

def main():

    print()

    validate_simulate_matchup()

    print()

    validate_simulate_matchup_mixed_outcomes()

    print()

    validate_simulation_convergence()

    print()

if __name__ == "__main__":
    main()
