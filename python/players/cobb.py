"""
Project LegendsLeague
Ty Cobb Player Metrics

Purpose:
    Calculate Ty Cobb's 1911 batting metrics and relative performance
    factors used by the LegendsLeague cross-era normalization model.

Responsibilities:
    - Calculate Cobb's 1911 plate appearances.
    - Calculate Cobb's strikeout, walk, and hit tendencies.
    - Compare Cobb's tendencies against the 1911 American League baseline.
    - Calculate Cobb's relative strikeout, walk, and hit factors.
    - Derive Cobb's 1911 single, double, triple, and home run totals.
    - Convert Cobb's hit-type totals into probability distributions.
    - Calculate Cobb's hit-type factors relative to the 1911 American League.

Historical Scope:
    Ty Cobb
    Season: 1911
    League: American League

Design Principle:
    Cobb's historical performance is first measured relative to the
    offensive environment of his own era before those relative factors
    are translated into a neutral cross-era matchup.
"""

# ============================================
# IMPORTS
# ============================================

from python.calculations.plate_appearances import calculate_plate_appearances
from python.calculations.strikeout_metrics import calculate_strikeout_tendency
from python.calculations.walk_metrics import calculate_walk_tendency
from python.calculations.hit_metrics import calculate_hit_tendency
from python.helpers.relative_metrics import relative_rate, relative_avoidance

from python.calculations.league_metrics import (
    calculate_1911_al_hit_type_distribution,
    calculate_1911_al_hit_type_probabilities,
)

from python.calculations.retrosheet_matchup_metrics import (
    calculate_singles_from_hit_totals,
    calculate_hit_types_probabilities,
)


# ============================================
# FUNCTIONS
# ============================================

def calculate_cobb_1911_plate_appearances(
    batting_data,
    verbose=True,
):

    ty_cobb_1911_batting = batting_data[
        (batting_data["playerID"] == "cobbty01")
        & (batting_data["yearID"] == 1911)
    ]

    plate_appearances = calculate_plate_appearances(
        ty_cobb_1911_batting["AB"].sum(),
        ty_cobb_1911_batting["BB"].sum(),
        ty_cobb_1911_batting["HBP"].sum(),
        ty_cobb_1911_batting["SH"].sum()
    )

    if verbose:
        print("\nTy Cobb 1911 Plate Appearance Calculation:")
        print(f"Calculated Plate Appearances: {plate_appearances}")

    return plate_appearances


def calculate_cobb_1911_strikeout_tendency(
    batting_data,
    plate_appearances,
    verbose=True,
):
    ty_cobb_1911_batting = batting_data[
        (batting_data["playerID"] == "cobbty01")
        & (batting_data["yearID"] == 1911)
    ]

    strikeouts = ty_cobb_1911_batting["SO"].sum()

    cobb_strikeout_tendency = (
        calculate_strikeout_tendency(strikeouts, plate_appearances)
    )

    if verbose:
        print("\nTy Cobb 1911 Strikeout Tendency Calculation:")
        print(f"Calculated Strikeouts: {strikeouts}")
        print(f"Strikeout Tendency: {cobb_strikeout_tendency * 100:.2f}%")

    return cobb_strikeout_tendency


def calculate_cobb_1911_relative_strikeout_factor(
    cobb_strikeout_tendency,
    al_strikeout_tendency,
    verbose=True,
):

    relative_ratio = relative_rate(
        cobb_strikeout_tendency,
        al_strikeout_tendency
    )

    cobb_relative_strikeout_avoidance = relative_avoidance(
        relative_ratio
    )
    if verbose:
        print(" ")
        print("---------------------------------")
        print(" ")

        print(f"Cobb factor: {relative_ratio:.2f}")
        print(f"Ty Cobb's Relative Strikeout Avoidance: {cobb_relative_strikeout_avoidance:.2f}")

    return relative_ratio


def calculate_cobb_1911_walk_tendency(
    batting_data,
    plate_appearances,
    verbose=True,
):
    ty_cobb_batting = batting_data[
        (batting_data["playerID"] == "cobbty01")
        & (batting_data["yearID"] == 1911)
    ]

    walks = ty_cobb_batting["BB"].sum()

    cobb_walk_tendency = (
        calculate_walk_tendency(walks, plate_appearances)
    )

    if verbose:
        print("\nTy Cobb 1911 Walk Tendency Calculation:")
        print(f"Calculated Walks: {walks}")
        print(f"Walk Tendency:    {cobb_walk_tendency * 100:.2f}%")

    return cobb_walk_tendency


def calculate_cobb_1911_relative_walk_factor(
    cobb_walk_tendency,
    al_walk_tendency,
):

    relative_ratio = relative_rate(
        cobb_walk_tendency,
        al_walk_tendency,
    )

    return relative_ratio


def calculate_cobb_1911_hit_tendency(
    batting_data,
    plate_appearances,
    verbose=True,
):

    ty_cobb_1911_batting = batting_data[
        (batting_data["playerID"] == "cobbty01")
        & (batting_data["yearID"] == 1911)
    ]

    hits = ty_cobb_1911_batting["H"].sum()

    cobb_hit_tendency = (
        calculate_hit_tendency(hits, plate_appearances)
    )

    if verbose:
        print("\nTy Cobb 1911 Hit Tendency Calculation:")
        print(f"Calculated Hits: {hits}")
        print(f"Hit Tendency:    {cobb_hit_tendency * 100:.2f}%")

    return cobb_hit_tendency


def calculate_cobb_1911_relative_hit_factor(
    cobb_hit_tendency,
    al_hit_tendency,
):

    relative_ratio = relative_rate(
        cobb_hit_tendency,
        al_hit_tendency,
    )

    return relative_ratio


def calculate_cobb_1911_singles(
    batting_data,
):

    ty_cobb_1911_batting = batting_data[
        (batting_data["playerID"] == "cobbty01")
        & (batting_data["yearID"] == 1911)
    ]

    hits = ty_cobb_1911_batting["H"].sum()
    doubles = ty_cobb_1911_batting["2B"].sum()
    triples = ty_cobb_1911_batting["3B"].sum()
    home_runs = ty_cobb_1911_batting["HR"].sum()

    singles = calculate_singles_from_hit_totals(
        hits,
        doubles,
        triples,
        home_runs,
    )

    cobb_1911_hit_types = {
        "single": singles,
        "double": doubles,
        "triple": triples,
        "home_run": home_runs,
    }


    return cobb_1911_hit_types


def calculate_cobb_1911_hit_probabilities(
    cobb_1911_hit_types,
):

    cobb_1911_hit_probabilities = calculate_hit_types_probabilities(
        cobb_1911_hit_types,
    )

    return cobb_1911_hit_probabilities


def calculate_cobb_relative_hit_type_factors(
    batting_data,
    cobb_1911_hit_types,
):

    al_1911_hit_type_counts = calculate_1911_al_hit_type_distribution(batting_data)
    al_1911_hit_probabilities = calculate_1911_al_hit_type_probabilities(al_1911_hit_type_counts)

    cobb_hit_probabilities = calculate_hit_types_probabilities(
        cobb_1911_hit_types
    )

    cobb_relative_single_factor = (
        cobb_hit_probabilities["single"]
        / al_1911_hit_probabilities["single"]
    )
    cobb_relative_double_factor = (
        cobb_hit_probabilities["double"]
        / al_1911_hit_probabilities["double"]
    )
    cobb_relative_triple_factor = (
        cobb_hit_probabilities["triple"]
        / al_1911_hit_probabilities["triple"]
    )
    cobb_relative_home_run_factor = (
        cobb_hit_probabilities["home_run"]
        / al_1911_hit_probabilities["home_run"]
    )

    cobb_1911_relative_hit_factors = {
        "single": cobb_relative_single_factor,
        "double": cobb_relative_double_factor,
        "triple": cobb_relative_triple_factor,
        "home_run": cobb_relative_home_run_factor,
    }

    return cobb_1911_relative_hit_factors
