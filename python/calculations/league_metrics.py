"""
Project LegendsLeague
League Metrics

Purpose:
    Calculate historical league-level metrics used to normalize player
    performance across different baseball eras.

Responsibilities:
    - Calculate 1911 American League plate appearances.
    - Calculate 1911 American League strikeout, walk, and hit tendencies.
    - Calculate 1911 American League hit-type distributions and probabilities.
    - Calculate 1973 American League pitcher encounter totals.
    - Calculate 1973 American League strikeout, walk, and hit tendencies.
    - Calculate 1973 American League allowed hit-type distributions.
    - Exclude Ty Cobb and Nolan Ryan from their respective league baselines
      when constructing player-relative metrics.
    - Provide reusable league baselines for cross-era normalization.

Historical Scope:
    - 1911 American League batting environment
    - 1973 American League pitching environment

Design Principle:
    Player performance is evaluated relative to the competitive environment
    of the player's own era before being translated into a neutral matchup.

Data Sources:
    - SABR Lahman Baseball Database
    - Retrosheet event data
"""

# =========================================================
# IMPORTS
# =========================================================

from python.calculations.plate_appearances import calculate_plate_appearances
from python.calculations.walk_metrics import calculate_walk_tendency
from python.calculations.strikeout_metrics import calculate_strikeout_tendency
from python.calculations.hit_metrics import calculate_hit_tendency
from python.data.retrosheet_event_parser import parse_retrosheet_event_directory

from python.calculations.retrosheet_matchup_metrics import (
    calculate_singles_from_hit_totals,
    calculate_hit_types_probabilities,
    aggregate_hit_types,
)


# =========================================================
# 1911 American League
# =========================================================

def calculate_1911_al_hbp_total(
    batting_data,
    verbose=True,
):

    al_1911_batting = batting_data[
        (batting_data["lgID"] == "AL")
        & (batting_data["yearID"] == 1911)
    ]

    total_hbp = al_1911_batting["HBP"].sum()

    if verbose:
        print("\n1911 AL reconstructed HBP total:")
        print(f"Total HBP: {total_hbp}")

        print("\n--------------------------------\n")

    return total_hbp


def calculate_1911_al_plate_appearances(batting_data):
    al_1911_batting = batting_data[
        (batting_data["lgID"] == "AL")
        & (batting_data["yearID"] == 1911)
        & (batting_data["playerID"] != "cobbty01")

    ]

    total_plate_appearances = calculate_plate_appearances(
        al_1911_batting["AB"].sum(),
        al_1911_batting["BB"].sum(),
        al_1911_batting["HBP"].sum(),
        al_1911_batting["SH"].sum()
    )

    return total_plate_appearances


def calculate_1911_al_strikeout_tendency(
    batting_data,
    total_plate_appearances,
    verbose=True,
):

    al_1911_batting = batting_data[
        (batting_data["lgID"] == "AL")
        & (batting_data["yearID"] == 1911)
        & (batting_data["playerID"] != "cobbty01")

    ]

    total_strikeouts = al_1911_batting["SO"].sum()

    al_1911_strikeout_tendency = calculate_strikeout_tendency(
        total_strikeouts,
        total_plate_appearances
    )

    if verbose:
        print("\n1911 AL Strikeout Tendency Calculation:")
        print(f"Total Strikeouts: {total_strikeouts}")
        print(f"Total Plate Appearances: {total_plate_appearances}")
        print(f"Strikeout Tendency: {al_1911_strikeout_tendency * 100:.2f}%")

    return al_1911_strikeout_tendency


def calculate_1911_al_walk_tendency(
    batting_data,
    total_plate_appearances,
    verbose=True,
):

    al_1911_batting = batting_data[
        (batting_data["lgID"] == "AL")
        & (batting_data["yearID"] == 1911)
        & (batting_data["playerID"] != "cobbty01")
    ]

    total_walks = al_1911_batting["BB"].sum()

    al_1911_walk_tendency = calculate_walk_tendency(
        total_walks,
        total_plate_appearances,
    )

    if verbose:
        print("\n1911 AL Walk Tendency Calculation:")
        print(f"Total Walks: {total_walks}")
        print(f"Total Plate Appearances: {total_plate_appearances}")
        print(f"Walk Tendency: {al_1911_walk_tendency * 100:.2f}%")

    return al_1911_walk_tendency


def calculate_1911_al_hit_tendency(
    batting_data,
    total_plate_appearances,
    verbose=True,
):

    al_1911_batting = batting_data[
        (batting_data["lgID"] == "AL")
        & (batting_data["yearID"] == 1911)
        & (batting_data["playerID"] != "cobbty01")
    ]

    total_hits = al_1911_batting["H"].sum()

    al_1911_hit_tendency = calculate_hit_tendency(
        total_hits,
        total_plate_appearances,
    )

    if verbose:
        print("\n1911 AL Hit Tendency Calculation:")
        print(f"Total Hits: {total_hits}")
        print(f"Total Plate Appearances: {total_plate_appearances}")
        print(f"AL Hit Tendency: {al_1911_hit_tendency * 100:.2f}%")

    return al_1911_hit_tendency


def calculate_1911_al_hit_type_distribution(batting_data):

    al_1911_batting = batting_data[
        (batting_data["lgID"] == "AL")
        & (batting_data["yearID"] == 1911)
        & (batting_data["playerID"] != "cobbty01")
    ]

    hits = al_1911_batting["H"].sum()
    doubles = al_1911_batting["2B"].sum()
    triples = al_1911_batting["3B"].sum()
    home_runs = al_1911_batting["HR"].sum()

    singles = calculate_singles_from_hit_totals(
        hits,
        doubles,
        triples,
        home_runs,
    )

    hit_type_counts = {
        "single": singles,
        "double": doubles,
        "triple": triples,
        "home_run": home_runs,
    }

    return hit_type_counts


def calculate_1911_al_hit_type_probabilities(hit_type_counts):

    al_1911_hit_type_probabilities = calculate_hit_types_probabilities(hit_type_counts)

    return al_1911_hit_type_probabilities


# =========================================================
# 1973 American League
# =========================================================

def calculate_1973_al_strikeout_tendency(
    pitching_data,
    verbose=True,
):

    al_1973_pitching = pitching_data[
        (pitching_data["lgID"] == "AL")
        & (pitching_data["yearID"] == 1973)
        & (pitching_data["playerID"] != "ryanno01")
    ]

    total_strikeouts = al_1973_pitching["SO"].sum()

    total_encounters = al_1973_pitching["BFP"].sum()

    al_1973_strikeout_tendency = calculate_strikeout_tendency(
        total_strikeouts,
        total_encounters
    )
    if verbose:
        print("\n1973 AL Strikeout Tendency Calculation:")
        print(f"Total Strikeouts: {total_strikeouts}")
        print(f"Total Encounters: {total_encounters}")
        print(f"Strikeout Tendency: {al_1973_strikeout_tendency * 100:.2f}%")

    return al_1973_strikeout_tendency


def calculate_1973_al_encounters(pitching_data):
    al_1973_pitching = pitching_data[
        (pitching_data["lgID"] == "AL")
        & (pitching_data["yearID"] == 1973)
        & (pitching_data["playerID"] != "ryanno01")
    ]

    al_1973_encounters = al_1973_pitching["BFP"].sum()

    return al_1973_encounters


def calculate_1973_al_walk_tendency(
    pitching_data,
    total_encounters,
    verbose=True,
):

    al_1973_pitching = pitching_data[
        (pitching_data["lgID"] == "AL")
        & (pitching_data["yearID"] == 1973)
        & (pitching_data["playerID"] != "ryanno01")
    ]

    total_walks = al_1973_pitching["BB"].sum()

    al_1973_walk_tendency = calculate_walk_tendency(
        total_walks,
        total_encounters,
    )

    if verbose:
        print("\n1973 AL Walk Tendency Calculation:")
        print(f"Total Walks: {total_walks}")
        print(f"Total batters faced: {total_encounters}")
        print(f"Walk Tendency: {al_1973_walk_tendency * 100:.2f}%")

    return al_1973_walk_tendency


def calculate_1973_al_hit_tendency(
    pitching_data,
    total_encounters,
    verbose=True,
):

    al_1973_pitching = pitching_data[
        (pitching_data["lgID"] == "AL")
        & (pitching_data["yearID"] == 1973)
        & (pitching_data["playerID"] != "ryanno01")
    ]

    total_hits = al_1973_pitching["H"].sum()

    al_1973_hit_tendency = calculate_hit_tendency(
        total_hits,
        total_encounters,
    )

    if verbose:
        print("\n1973 AL Hit Tendency Calculation:")
        print(f"Total Hits: {total_hits}")
        print(f"Total Encounters: {total_encounters}")
        print(f"AL Hit Tendency: {al_1973_hit_tendency * 100:.2f}%")

    return al_1973_hit_tendency


def calculate_1973_al_allowed_hit_type_distribution(directory_path):

    all_plays = parse_retrosheet_event_directory(
        directory_path,
        league="AL",
    )

    al_1973_pitching_plays = [
        play
        for play in all_plays
        if play["pitcher_id"] != "ryann001"
    ]

    hit_type_counts = aggregate_hit_types(
        al_1973_pitching_plays
    )

    return hit_type_counts


def calculate_1973_al_allowed_hit_type_probabilities(hit_type_count):

    al_1973_allowed_hit_type_probabilities = calculate_hit_types_probabilities(
        hit_type_count
    )

    return al_1973_allowed_hit_type_probabilities
