"""
Project LegendsLeague
Lahman Raw Data Inspection

Purpose:
    Inspect the raw SABR Lahman Baseball Database files before any
    transformation or standardization occurs.

Responsibilities:
    - Verify required Lahman source files exist.
    - Confirm source files can be loaded successfully.
    - Inspect dataset dimensions and column structures.
    - Identify missing values and potential duplicate-key issues.
    - Provide an initial understanding of the raw source data.

Data Policy:
    Files stored in data/raw/ are immutable source data.
    This module must never modify or overwrite raw Lahman files.

Source:
    SABR Lahman Baseball Database
    Coverage: 1871-2025
"""

# ============================================
# IMPORTS
# ============================================

from python.data.load_lahman_data import load_required_files

from python.data.retrosheet_event_parser import (
    parse_retrosheet_event_directory,
)

from python.calculations.retrosheet_matchup_metrics import (
    aggregate_pitcher_hit_types,
)

from python.calculations.league_metrics import (
    calculate_1911_al_hbp_total,
    calculate_1911_al_plate_appearances,
    calculate_1911_al_strikeout_tendency,
    calculate_1911_al_hit_tendency,
    calculate_1911_al_walk_tendency,
    calculate_1973_al_strikeout_tendency,
    calculate_1973_al_encounters,
    calculate_1973_al_walk_tendency,
    calculate_1973_al_hit_tendency,
    calculate_1973_al_allowed_hit_type_distribution,
    calculate_1973_al_allowed_hit_type_probabilities,
)

from python.calculations.matchup_metrics import (
    calculate_matchup_probability,
)

from python.players.cobb import (
    calculate_cobb_1911_plate_appearances,
    calculate_cobb_1911_strikeout_tendency,
    calculate_cobb_1911_relative_strikeout_factor,
    calculate_cobb_1911_walk_tendency,
    calculate_cobb_1911_relative_walk_factor,
    calculate_cobb_1911_hit_tendency,
    calculate_cobb_1911_relative_hit_factor,
    calculate_cobb_1911_singles,
    calculate_cobb_relative_hit_type_factors,
)

from python.players.ryan import (
    get_ryan_1973_encounters,
    calculate_ryan_1973_strikeout_tendency,
    calculate_ryan_1973_relative_strikeout_factor,
    calculate_ryan_1973_walk_tendency,
    calculate_ryan_1973_relative_walk_factor,
    calculate_ryan_1973_hit_tendency,
    calculate_ryan_1973_relative_hit_factor,
    calculate_ryan_1973_relative_hit_type_factors,
)

from python.helpers.normalization_metrics import (
    calculate_neutral_probability,
    calculate_neutral_player_probability,
    calculate_matchup_hit_type_probabilities,
    calculate_overall_hit_type_probabilities,
    calculate_other_outs,
    build_matchup_outcome_probabilities,
)


# ============================================
# MAIN
# ============================================

def main(
    verbose=True,
):

    directory_path = "data/raw/retrosheet/1973"

    loaded_files = load_required_files(
        verbose=False,
    )

    batting_data = loaded_files["Batting.csv"]
    pitching_data = loaded_files["Pitching.csv"]


    # ============================================
    # 1911 AL
    # ============================================

    calculate_1911_al_hbp_total(
        batting_data,
        verbose=False,
    )

    al_1911_plate_appearances = calculate_1911_al_plate_appearances(
        batting_data,
    )

    al_1911_strikeout_tendency = calculate_1911_al_strikeout_tendency(
        batting_data,
        al_1911_plate_appearances,
        verbose=False,
    )

    al_1911_walk_tendency = calculate_1911_al_walk_tendency(
        batting_data,
        al_1911_plate_appearances,
        verbose=False,
    )

    al_1911_hit_tendency = calculate_1911_al_hit_tendency(
        batting_data,
        al_1911_plate_appearances,
        verbose=False,
    )


    # ============================================
    # 1911 COBB
    # ============================================

    plate_appearance = calculate_cobb_1911_plate_appearances(
        batting_data,
        verbose=False,
    )

    cobb_1911_strikeout_tendency = calculate_cobb_1911_strikeout_tendency(
        batting_data,
        plate_appearance,
        verbose=False,
    )

    cobb_relative_strikeout_factor = calculate_cobb_1911_relative_strikeout_factor(
        cobb_1911_strikeout_tendency,
        al_1911_strikeout_tendency,
        verbose=False,
    )

    cobb_1911_walk_tendency = calculate_cobb_1911_walk_tendency(
        batting_data,
        plate_appearance,
        verbose=False,
    )

    cobb_walk_factor = calculate_cobb_1911_relative_walk_factor(
        cobb_1911_walk_tendency,
        al_1911_walk_tendency,
    )

    cobb_1911_hit_tendency = calculate_cobb_1911_hit_tendency(
        batting_data,
        plate_appearance,
        verbose=False,
    )

    cobb_hit_factor = calculate_cobb_1911_relative_hit_factor(
        cobb_1911_hit_tendency,
        al_1911_hit_tendency,
    )

    cobb_1911_hit_types = calculate_cobb_1911_singles(
        batting_data,
    )

    cobb_1911_relative_hit_factors = calculate_cobb_relative_hit_type_factors(
        batting_data,
        cobb_1911_hit_types,
    )


    # ============================================
    # 1973 AL
    # ============================================

    all_plays = parse_retrosheet_event_directory(
        directory_path,
    )

    al_1973_strikeout_tendency = calculate_1973_al_strikeout_tendency(
        pitching_data,
        verbose=False,
    )

    al_1973_encounters = calculate_1973_al_encounters(
        pitching_data,
    )

    al_1973_walk_tendency = calculate_1973_al_walk_tendency(
        pitching_data,
        al_1973_encounters,
        verbose=False,
    )

    al_1973_hit_tendency = calculate_1973_al_hit_tendency(
        pitching_data,
        al_1973_encounters,
        verbose=False,
    )

    al_1973_allowed_hit_type_counts = calculate_1973_al_allowed_hit_type_distribution(
        directory_path,
    )

    al_1973_allowed_hit_type_probabilities = calculate_1973_al_allowed_hit_type_probabilities(
        al_1973_allowed_hit_type_counts,
    )



    # ============================================
    # 1973 RYAN
    # ============================================

    encounters = get_ryan_1973_encounters(
        pitching_data,
        verbose=False,
    )

    ryan_1973_strikeout_tendency = calculate_ryan_1973_strikeout_tendency(
        pitching_data,
        encounters,
        verbose=False,
    )

    ryan_relative_strikeout_factor = calculate_ryan_1973_relative_strikeout_factor(
        ryan_1973_strikeout_tendency,
        al_1973_strikeout_tendency,
        verbose=False,
    )

    ryan_1973_walk_tendency = calculate_ryan_1973_walk_tendency(
        pitching_data,
        encounters,
        verbose=False,
    )

    ryan_walk_factor = calculate_ryan_1973_relative_walk_factor(
        ryan_1973_walk_tendency,
        al_1973_walk_tendency,
    )

    ryan_1973_hit_tendency = calculate_ryan_1973_hit_tendency(
        pitching_data,
        encounters,
        verbose=False,
    )

    ryan_hit_factor = calculate_ryan_1973_relative_hit_factor(
        ryan_1973_hit_tendency,
        al_1973_hit_tendency,
    )

    ryan_hit_types = aggregate_pitcher_hit_types(
        all_plays,
        "ryann001",
    )

    ryan_1973_relative_hit_factors = calculate_ryan_1973_relative_hit_type_factors(
        ryan_hit_types,
        al_1973_allowed_hit_type_probabilities,
    )


    # ============================================
    # NEUTRAL ERA
    # ============================================

    neutral_strikeout_probability = calculate_neutral_probability(
        al_1911_strikeout_tendency,
        al_1973_strikeout_tendency,
    )

    neutral_walk_probability = calculate_neutral_probability(
        al_1911_walk_tendency,
        al_1973_walk_tendency,
    )

    neutral_hit_probability = calculate_neutral_probability(
        al_1911_hit_tendency,
        al_1973_hit_tendency,
    )


    # ============================================
    # NEUTRAL COBB
    # ============================================

    cobb_neutral_strikeout_probability = (
        calculate_neutral_player_probability(
            neutral_strikeout_probability,
            cobb_relative_strikeout_factor
        )
    )

    cobb_neutral_walk_probability = (
        calculate_neutral_player_probability(
            neutral_walk_probability,
            cobb_walk_factor,
        )
    )

    cobb_neutral_hit_probability = (
        calculate_neutral_player_probability(
            neutral_hit_probability,
            cobb_hit_factor,
        )
    )


    # ============================================
    # NEUTRAL RYAN
    # ============================================

    ryan_neutral_strikeout_probability = (
        calculate_neutral_player_probability(
            neutral_strikeout_probability,
            ryan_relative_strikeout_factor
        )
    )

    ryan_neutral_walk_probability = (
        calculate_neutral_player_probability(
            neutral_walk_probability,
            ryan_walk_factor,
        )
    )

    ryan_neutral_hit_probability = (
        calculate_neutral_player_probability(
            neutral_hit_probability,
            ryan_hit_factor,
        )
    )


    # ============================================
    # NEUTRAL COBB v. RYAN
    # ============================================

    cobb_vs_ryan_strikeout_probability = (
        calculate_matchup_probability(
            cobb_neutral_strikeout_probability,
            ryan_neutral_strikeout_probability,
            neutral_strikeout_probability
        )
    )

    cobb_vs_ryan_walk_probability = (
        calculate_matchup_probability(
            cobb_neutral_walk_probability,
            ryan_neutral_walk_probability,
            neutral_walk_probability,
        )
    )

    cobb_vs_ryan_hit_probability = (
        calculate_matchup_probability(
            cobb_neutral_hit_probability,
            ryan_neutral_hit_probability,
            neutral_hit_probability,
        )
    )

    cobb_vs_ryan_hit_type_probabilities = calculate_matchup_hit_type_probabilities(
        cobb_1911_relative_hit_factors,
        ryan_1973_relative_hit_factors,
    )

    overall_hit_type_probabilities = calculate_overall_hit_type_probabilities(
        cobb_vs_ryan_hit_probability,
        cobb_vs_ryan_hit_type_probabilities,
    )

    other_out_probability = calculate_other_outs(
        cobb_vs_ryan_strikeout_probability,
        cobb_vs_ryan_walk_probability,
        overall_hit_type_probabilities["single"],
        overall_hit_type_probabilities["double"],
        overall_hit_type_probabilities["triple"],
        overall_hit_type_probabilities["home_run"],
    )

    matchup_outcome_probabilities = build_matchup_outcome_probabilities(
        cobb_vs_ryan_strikeout_probability,
        cobb_vs_ryan_walk_probability,
        overall_hit_type_probabilities,
        other_out_probability,
    )

    if verbose:
        print()
        print("Normalization pipeline completed successfully.")
        print()

    return matchup_outcome_probabilities


if __name__ == "__main__":
    main()
