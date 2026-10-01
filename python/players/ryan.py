"""
Project LegendsLeague
Nolan Ryan Player Metrics

Purpose:
    Calculate Nolan Ryan's 1973 pitching metrics and relative performance
    factors used by the LegendsLeague cross-era normalization model.

Responsibilities:
    - Calculate Ryan's 1973 batter-facing encounters.
    - Calculate Ryan's strikeout, walk, and hit tendencies.
    - Compare Ryan's tendencies against the 1973 American League baseline.
    - Calculate Ryan's relative strikeout, walk, and hit factors.
    - Convert Ryan's allowed hit types into probability distributions.
    - Calculate Ryan's hit-type factors relative to the 1973 American League.

Historical Scope:
    Nolan Ryan
    Season: 1973
    League: American League

Design Principle:
    Ryan's historical performance is first measured relative to the
    pitching environment of his own era before those relative factors
    are translated into a neutral cross-era matchup.
"""

# =============================================
# IMPORTS
# =============================================

from python.calculations.strikeout_metrics import calculate_strikeout_tendency
from python.calculations.walk_metrics import calculate_walk_tendency
from python.calculations.hit_metrics import calculate_hit_tendency
from python.helpers.relative_metrics import relative_rate, relative_generation

from python.calculations.retrosheet_matchup_metrics import (
    calculate_hit_types_probabilities,
)


# =============================================
# FUNCTIONS
# =============================================

def get_ryan_1973_encounters(
    pitching_data,
    verbose=True,
):

    ryan_1973_pitching = pitching_data[
        (pitching_data["playerID"] == "ryanno01")
        & (pitching_data["yearID"] == 1973)
    ]

    encounters = ryan_1973_pitching["BFP"].sum()

    if verbose:
        print("Nolan Ryan's 1973 encounters:")
        print(f"{encounters}")

    return encounters


def calculate_ryan_1973_strikeout_tendency(
    pitching_data,
    encounters,
    verbose=True,
):

    ryan_1973_pitching = pitching_data[
        (pitching_data["playerID"] == "ryanno01")
        & (pitching_data["yearID"] == 1973)
    ]

    strikeouts = ryan_1973_pitching["SO"].sum()

    ryan_strikeout_tendency = (
        calculate_strikeout_tendency(
            strikeouts,
            encounters,
        )
    )

    if verbose:
        print("\nNolan Ryan 1973 Strikeout Tendency Calculation:")
        print(f"Calculated Strikeouts: {strikeouts}")
        print(f"Strikeout Tendency: {ryan_strikeout_tendency * 100:.2f}%")

    return ryan_strikeout_tendency


def calculate_ryan_1973_relative_strikeout_factor(
    ryan_strikeout_tendency,
    al_strikeout_tendency,
    verbose=True,
):

    relative_ratio = relative_rate(
        ryan_strikeout_tendency,
        al_strikeout_tendency
    )

    ryan_relative_strikeout_generation = relative_generation(
        relative_ratio,
    )
    if verbose:
        print(" ")
        print("---------------------------------")
        print(" ")

        print(f"Ryan factor: {relative_ratio:.2f}")
        print(f"Nolan Ryan Relative Strikeout Generation: {ryan_relative_strikeout_generation:.2f}")

    return relative_ratio


def calculate_ryan_1973_walk_tendency(
    pitching_data,
    encounters,
    verbose=True,
):
    ryan_1973_pitching = pitching_data[
        (pitching_data["playerID"] == "ryanno01")
        & (pitching_data["yearID"] == 1973)
    ]

    walks = ryan_1973_pitching["BB"].sum()

    ryan_walk_tendency = (
        calculate_walk_tendency(
            walks,
            encounters,
        )
    )

    if verbose:
        print("\nNolan Ryan 1973 Walk Tendency Calculation:")
        print(f"Calculated walks: {walks}")
        print(f"Ryan 1973 Walk Tendency: {ryan_walk_tendency * 100:.2f}%")

    return ryan_walk_tendency


def calculate_ryan_1973_relative_walk_factor(
    ryan_walk_tendency,
    al_walk_tendency,
):

    relative_ratio = relative_rate(
        ryan_walk_tendency,
        al_walk_tendency,
    )

    return relative_ratio


def calculate_ryan_1973_hit_tendency(
    pitching_data,
    encounters,
    verbose=True,
):

    ryan_1973_pitching = pitching_data[
        (pitching_data["playerID"] == "ryanno01")
        & (pitching_data["yearID"] == 1973)
    ]

    hits = ryan_1973_pitching["H"].sum()

    ryan_hit_tendency = (
        calculate_hit_tendency(
            hits,
            encounters,
        )
    )

    if verbose:
        print("\nNolan Ryan 1973 Hit Tendency Calculation:")
        print(f"Calculated Hits: {hits}")
        print(f"Hit Tendency:    {ryan_hit_tendency * 100:.2f}%")

    return ryan_hit_tendency


def calculate_ryan_1973_relative_hit_factor(
    ryan_hit_tendency,
    al_hit_tendency,
):
    relative_ratio = relative_rate(
        ryan_hit_tendency,
        al_hit_tendency
    )

    return relative_ratio


def calculate_ryan_1973_relative_hit_type_factors(
    ryan_hit_types,
    al_1973_hit_type_probabilities,
):

    ryan_hit_probabilities = calculate_hit_types_probabilities(
        ryan_hit_types
    )

    ryan_relative_single_factor = (
        ryan_hit_probabilities["single"]
        / al_1973_hit_type_probabilities["single"]
    )

    ryan_relative_double_factor = (
        ryan_hit_probabilities["double"]
        / al_1973_hit_type_probabilities["double"]
    )

    ryan_relative_triple_factor = (
        ryan_hit_probabilities["triple"]
        / al_1973_hit_type_probabilities["triple"]
    )

    ryan_relative_home_run_factor = (
        ryan_hit_probabilities["home_run"]
        / al_1973_hit_type_probabilities["home_run"]
    )

    ryan_1973_relative_hit_factors = {
        "single": ryan_relative_single_factor,
        "double": ryan_relative_double_factor,
        "triple": ryan_relative_triple_factor,
        "home_run": ryan_relative_home_run_factor,
    }

    return ryan_1973_relative_hit_factors
