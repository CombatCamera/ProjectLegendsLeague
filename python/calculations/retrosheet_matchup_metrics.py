"""
Project LegendsLeague
Retrosheet Matchup Metrics

Purpose:
    Calculate matchup-oriented statistics from Retrosheet play data and
    Lahman player-season data.

Responsibilities:
    - Aggregate pitcher-batter encounter and strikeout totals.
    - Build batter strikeout profiles from Lahman statistics.
    - Compare actual matchup results against expected strikeout outcomes.
    - Calculate strikeout tendencies with direct matchups excluded.
    - Build excluded-matchup comparison metrics.
    - Derive singles from total hit components.
    - Aggregate hit types from Retrosheet play data.
    - Aggregate pitcher-specific hit-type totals.
    - Convert hit-type counts into probability distributions.

Design Principle:
    Matchup analysis should separate direct historical encounters from
    broader season performance when evaluating player tendencies, while
    preserving Retrosheet-derived event detail for strikeout and hit-type
    analysis.

Data Sources:
    - Retrosheet event data
    - SABR Lahman Baseball Database
"""

# ========================================================
# IMPORTS
# ========================================================

from python.calculations.plate_appearances import (
    calculate_plate_appearances
)

from python.calculations.strikeout_metrics import (
    calculate_strikeout_tendency
)

from python.calculations.matchup_metrics import (
    calculate_matchup_probability,
)


# ========================================================
# FUNCTIONS
# ========================================================

def aggregate_pitcher_batter_matchups(
    play_data,
    pitcher_id
):

    pitcher_batter_matchups = {}

    for play in play_data:
        if (
            play["pitcher_id"] == pitcher_id
            and play["is_pitcher_encounter"]
        ):
            batter_id = play["responsible_batter_id"]

            if batter_id not in pitcher_batter_matchups:

                pitcher_batter_matchups[batter_id] = {
                    "encounters": 0,
                    "strikeouts": 0,
                }

            pitcher_batter_matchups[batter_id]["encounters"] += 1

            if play["is_strikeout"]:
                pitcher_batter_matchups[batter_id]["strikeouts"] += 1

    return pitcher_batter_matchups


def build_batter_strikeout_profiles(
    batting_data,
    player_id_mapping,
    year_id,
):

    batter_strikeout_profiles = {}

    required_stat_columns = [
        "AB",
        "BB",
        "HBP",
        "SH",
        "SF",
        "SO",
    ]


    for retro_player_id in player_id_mapping:
        lahman_player_id = player_id_mapping[retro_player_id]
        batter_season_data = batting_data[
            (batting_data["playerID"] == lahman_player_id)
            & (batting_data["yearID"] == year_id)
        ]

        if batter_season_data.empty:
            raise ValueError(
                f"No {year_id} batting data found for "
                f"Retrosheet ID '{retro_player_id}' and "
                f"Lahman ID '{lahman_player_id}'."
            )

        for stat_column in required_stat_columns:
            missing_value_exists = (
                batter_season_data[stat_column]
                .isna()
                .any()
            )

            if missing_value_exists:
                raise ValueError(
                    f"Missing {stat_column} data for "
                    f"Lahman ID '{lahman_player_id}' "
                    f"in {year_id}."
                )

        at_bats = batter_season_data["AB"].sum()
        walks = batter_season_data["BB"].sum()
        hit_by_pitch = batter_season_data["HBP"].sum()
        sacrifice_hits = batter_season_data["SH"].sum()
        sacrifice_flies = batter_season_data["SF"].sum()
        strikeouts = batter_season_data["SO"].sum()

        plate_appearances = calculate_plate_appearances(
            at_bats,
            walks,
            hit_by_pitch,
            sacrifice_hits,
            sacrifice_flies,
        )

        strikeout_tendency = calculate_strikeout_tendency(
            strikeouts,
            plate_appearances
        )

        batter_strikeout_profiles[retro_player_id] = {
            "lahman_player_id": lahman_player_id,
            "plate_appearances": plate_appearances,
            "strikeouts": strikeouts,
            "strikeout_tendency": strikeout_tendency,
        }

    return batter_strikeout_profiles


def build_pitcher_batter_comparisons(
    pitcher_batter_matchups,
    batter_strikeout_profiles,
    pitcher_probability,
    league_probability,
):

    pitcher_batter_comparisons = {}

    for batter_id in pitcher_batter_matchups:
        batter_matchup = pitcher_batter_matchups[batter_id]
        batter_profile = batter_strikeout_profiles[batter_id]

        matchup_probability = calculate_matchup_probability(
            batter_profile["strikeout_tendency"],
            pitcher_probability,
            league_probability,
        )

        expected_strikeouts = (
            batter_matchup["encounters"] * matchup_probability
        )

        actual_strikeouts = batter_matchup["strikeouts"]

        strikeout_difference = actual_strikeouts - expected_strikeouts

        pitcher_batter_comparisons[batter_id] = {
            "encounters": batter_matchup["encounters"],
            "actual_strikeouts": actual_strikeouts,
            "expected_strikeouts": expected_strikeouts,
            "strikeout_difference": strikeout_difference,
        }

    return pitcher_batter_comparisons


def calculate_strikeout_tendency_excluding_matchup(
    season_strikeouts,
    season_encounters,
    matchup_strikeouts,
    matchup_encounters
):

    remaining_strikeouts = season_strikeouts - matchup_strikeouts
    remaining_encounters = season_encounters - matchup_encounters

    if remaining_encounters <= 0:
        raise ValueError(
            "Remaining encounters must be greater than zero."
        )

    if remaining_strikeouts < 0:
        raise ValueError(
            "Remaining strikeouts cannot be negative."
        )

    if remaining_strikeouts > remaining_encounters:
        raise ValueError(
            "Remaining strikeouts cannot exceed remaining encounters."
        )

    remaining_strikeout_tendency = calculate_strikeout_tendency(
        remaining_strikeouts,
        remaining_encounters,
    )

    return remaining_strikeout_tendency


def build_excluded_matchup_comparisons(
    pitcher_batter_matchups,
    batter_strikeout_profiles,
    pitcher_season_strikeout,
    pitcher_season_encounters,
    league_probability,
):
    excluded_matchup_comparisons = {}

    for batter_id in pitcher_batter_matchups:
        batter_matchup = pitcher_batter_matchups[batter_id]
        batter_profile = batter_strikeout_profiles[batter_id]

        batter_probability_without_pitcher = (
            calculate_strikeout_tendency_excluding_matchup(
                batter_profile["strikeouts"],
                batter_profile["plate_appearances"],
                batter_matchup["strikeouts"],
                batter_matchup["encounters"],
            )
        )

        pitcher_probability_without_batter = (
            calculate_strikeout_tendency_excluding_matchup(
                pitcher_season_strikeout,
                pitcher_season_encounters,
                batter_matchup["strikeouts"],
                batter_matchup["encounters"],
            )
        )

        pitcher_only_expected_strikeouts = (
            batter_matchup["encounters"]
            * pitcher_probability_without_batter
        )

        matchup_probability = calculate_matchup_probability(
            batter_probability_without_pitcher,
            pitcher_probability_without_batter,
            league_probability,
        )

        expected_strikeouts = (
            batter_matchup["encounters"] * matchup_probability
        )

        actual_strikeouts = batter_matchup["strikeouts"]

        strikeout_difference = actual_strikeouts - expected_strikeouts

        excluded_matchup_comparisons[batter_id] = {
            "encounters": batter_matchup["encounters"],
            "matchup_probability": matchup_probability,
            "pitcher_only_probability": pitcher_probability_without_batter,
            "pitcher_only_expected_strikeouts": pitcher_only_expected_strikeouts,
            "actual_strikeouts": actual_strikeouts,
            "expected_strikeouts": expected_strikeouts,
            "strikeout_difference": strikeout_difference,

        }

    return excluded_matchup_comparisons


def calculate_singles_from_hit_totals(
    total_hits,
    doubles,
    triples,
    home_runs,
):

    singles = total_hits - sum(
        [
            doubles,
            triples,
            home_runs,
        ]
    )

    return singles


def aggregate_hit_types(play_data):

    hit_type_counts = {
        "single": 0,
        "double": 0,
        "triple": 0,
        "home_run": 0,
    }

    for play in play_data:
        hit_type = play["hit_type"]
        if (
            play["is_pitcher_encounter"]
            and play["hit_type"] is not None
        ):

            hit_type_counts[hit_type] += 1

    return hit_type_counts


def aggregate_pitcher_hit_types(play_data, pitcher_id):


    pitcher_plays = [
        play
        for play in play_data
        if play["pitcher_id"] == pitcher_id
    ]

    hit_type_counts = aggregate_hit_types(pitcher_plays)


    return hit_type_counts


def calculate_hit_types_probabilities(hit_type_counts):

        total_hits = sum(
            hit_type_counts.values()
        )

        single_probability = hit_type_counts["single"] / total_hits
        double_probability = hit_type_counts["double"] / total_hits
        triple_probability = hit_type_counts["triple"] / total_hits
        home_run_probability = hit_type_counts["home_run"] / total_hits

        pitcher_hit_type_probabilities = {
            "single": single_probability,
            "double": double_probability,
            "triple": triple_probability,
            "home_run": home_run_probability,
        }

        return pitcher_hit_type_probabilities
