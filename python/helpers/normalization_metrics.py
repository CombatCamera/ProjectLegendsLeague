"""
Project LegendsLeague
Normalization Metrics

Purpose:
    Provide reusable probability calculations used to translate historical
    player and league performance into a neutral cross-era matchup model.

Responsibilities:
    - Calculate a neutral-era probability from two historical era baselines.
    - Translate player-relative factors into neutral-era player probabilities.
    - Combine batter and pitcher hit-type factors into matchup hit-type weights.
    - Normalize hit-type weights into conditional hit probabilities.
    - Convert conditional hit-type probabilities into overall plate-appearance probabilities.
    - Calculate the remaining Other Out probability.
    - Build the complete seven-outcome matchup probability distribution.

Simulation Outcomes:
    - Strikeout
    - Walk
    - Single
    - Double
    - Triple
    - Home Run
    - Other Out

Design Principle:
    Historical players are first measured relative to their own eras.
    Those relative factors are then applied to a shared neutral environment
    before batter and pitcher effects are combined into matchup probabilities.
"""

# ======================================================
# IMPORTS
#=======================================================

import math


# ======================================================
# FUNCTIONS
#=======================================================

def calculate_neutral_probability(
    first_era_probability,
    second_era_probability
):

    neutral_probability = math.sqrt(
        first_era_probability
        * second_era_probability
    )

    return neutral_probability


def calculate_neutral_player_probability(
    neutral_probability,
    relative_factor
):
    neutral_player_probability = (
        neutral_probability
        * relative_factor
    )

    return neutral_player_probability


def calculate_matchup_hit_type_probabilities(
    batter_relative_hit_factors,
    pitcher_relative_hit_factors,
):

    single_weight = (
        batter_relative_hit_factors["single"]
        * pitcher_relative_hit_factors["single"]
    )

    double_weight = (
        batter_relative_hit_factors["double"]
        * pitcher_relative_hit_factors["double"]
    )

    triple_weight = (
        batter_relative_hit_factors["triple"]
        * pitcher_relative_hit_factors["triple"]
    )

    home_run_weight = (
        batter_relative_hit_factors["home_run"]
        * pitcher_relative_hit_factors["home_run"]
    )

    total_hit_type_weight = sum(
        [
            single_weight,
            double_weight,
            triple_weight,
            home_run_weight,
        ]
    )

    single_probability = (
        single_weight
        / total_hit_type_weight
    )

    double_probability = (
        double_weight
        / total_hit_type_weight
    )

    triple_probability = (
        triple_weight
        / total_hit_type_weight
    )

    home_run_probability = (
        home_run_weight
        / total_hit_type_weight
    )

    cobb_ryan_hit_type_probabilities = {
        "single": single_probability,
        "double": double_probability,
        "triple": triple_probability,
        "home_run": home_run_probability
    }

    return cobb_ryan_hit_type_probabilities


def calculate_overall_hit_type_probabilities(
    matchup_hit_probability,
    matchup_hit_type_probabilities,
):

    single_probability = (
        matchup_hit_probability
        * matchup_hit_type_probabilities["single"]
    )

    double_probability = (
        matchup_hit_probability
        * matchup_hit_type_probabilities["double"]
    )

    triple_probability = (
        matchup_hit_probability
        * matchup_hit_type_probabilities["triple"]
    )

    home_run_probability = (
        matchup_hit_probability
        * matchup_hit_type_probabilities["home_run"]
    )

    overall_hit_type_probabilities = {
        "single": single_probability,
        "double": double_probability,
        "triple": triple_probability,
        "home_run": home_run_probability,
    }

    return overall_hit_type_probabilities


def calculate_other_outs(
    strikeout_probability,
    walk_probability,
    single_probability,
    double_probability,
    triple_probability,
    home_run_probability,
):

    accounted_probability = sum(
        [
            strikeout_probability,
            walk_probability,
            single_probability,
            double_probability,
            triple_probability,
            home_run_probability,
        ]
    )

    other_out_probability = (
        1.0
        - accounted_probability
    )

    return other_out_probability


def build_matchup_outcome_probabilities(
    strikeout_probability,
    walk_probability,
    overall_hit_type_probabilities,
    other_out_probability,
):

    matchup_outcome_probabilities = {
        "strikeout": strikeout_probability,
        "walk": walk_probability,
        "single": overall_hit_type_probabilities["single"],
        "double": overall_hit_type_probabilities["double"],
        "triple": overall_hit_type_probabilities["triple"],
        "home_run": overall_hit_type_probabilities["home_run"],
        "other_out": other_out_probability,
    }

    return matchup_outcome_probabilities
