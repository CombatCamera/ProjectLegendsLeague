"""
Project LegendsLeague
Retrosheet Matchup Analysis Pipeline

Purpose:
    Build and evaluate historical pitcher-batter matchup metrics using
    Retrosheet event data and Lahman season statistics.

Responsibilities:
    - Load required Lahman source data.
    - Parse 1973 Retrosheet event files.
    - Aggregate Nolan Ryan pitcher-batter matchup totals.
    - Build Retrosheet-to-Lahman player ID mappings.
    - Build opponent strikeout profiles from Lahman season data.
    - Reconcile Retrosheet matchup totals with Lahman season totals.
    - Calculate expected pitcher-batter strikeout probabilities.
    - Compare expected strikeouts against recorded matchup results.
    - Exclude direct historical matchups when estimating player tendencies.
    - Evaluate matchup-model performance against pitcher-only baselines.
    - Calculate absolute error and Brier Score metrics.
    - Aggregate Nolan Ryan hit-type distributions.
    - Inspect Ty Cobb and Nolan Ryan hit-type probabilities.

Current Historical Scope:
    - Nolan Ryan (1973)
    - Ty Cobb (1911)
    - Ryan's 1973 American League opponents

Model Evaluation:
    - Expected vs. recorded strikeouts
    - Matchup-adjusted vs. pitcher-only estimates
    - Absolute error
    - Brier Score

Design Principle:
    Historical head-to-head performance should be evaluated against player
    and league baselines without allowing the direct matchup being tested
    to inflate those baseline tendencies.

Data Sources:
    - Retrosheet event data
    - SABR Lahman Baseball Database
"""
# ====================================================
# IMPORTS
# ====================================================
import pandas as pd

import math

from python.players.ryan import (
    get_ryan_1973_encounters,
    calculate_ryan_1973_strikeout_tendency,
)

from python.players.cobb import (
    calculate_cobb_1911_singles,
    calculate_cobb_1911_hit_probabilities,
)

from python.calculations.retrosheet_matchup_metrics import (
    aggregate_pitcher_batter_matchups,
    build_batter_strikeout_profiles,
    build_pitcher_batter_comparisons,
    calculate_strikeout_tendency_excluding_matchup,
    build_excluded_matchup_comparisons,
    aggregate_pitcher_hit_types,
    calculate_hit_types_probabilities,

)

from python.calculations.league_metrics import (
    calculate_1973_al_strikeout_tendency,
)

from python.calculations.matchup_metrics import (
    calculate_matchup_probability,
)

from python.calculations.strikeout_metrics import (
    calculate_strikeout_tendency,
)

from python.data.retrosheet_event_parser import (
    parse_retrosheet_event_directory,
)

from python.data.player_id_mapping import (
    build_retrosheet_to_lahman_id_mapping,
)

from python.data.load_lahman_data import (
    load_required_files,
)

from python.qa.validate_retrosheet_lahman_reconciliation import (
    validate_opponent_season_differences,
)

# =========================================
# main
# =========================================

def main():

    # ====================================================
    # FILES
    # ====================================================

    directory_path = "data/raw/retrosheet/1973"

    loaded_files = load_required_files(
        verbose=False,
    )

    people_data = loaded_files["People.csv"]
    batting_data = loaded_files["Batting.csv"]
    pitching_data = loaded_files["Pitching.csv"]

    # ====================================================
    # CALLS
    # ====================================================


    all_plays = parse_retrosheet_event_directory(
        directory_path
    )

    cobb_1911_hit_types = calculate_cobb_1911_singles(
        batting_data,
    )

    cobb_1911_hit_probabilities = calculate_cobb_1911_hit_probabilities(
        cobb_1911_hit_types,
    )

    ryan_allowed_hits = aggregate_pitcher_hit_types(
        all_plays,
        "ryann001",
    )

    ryan_hits_probabilities = calculate_hit_types_probabilities(
        ryan_allowed_hits,
    )

    ryan_total_hits = sum(ryan_allowed_hits.values())


    ryan_matchups = aggregate_pitcher_batter_matchups(
        all_plays,
        "ryann001",
    )

    player_id_mapping = build_retrosheet_to_lahman_id_mapping(
        people_data,
        ryan_matchups,
    )

    batter_strikeout_profiles = build_batter_strikeout_profiles(
        batting_data,
        player_id_mapping,
        1973,
    )

    # ====================================================
    # SEASON TOTAL COMPARISON
    # ====================================================
    opponent_retrosheet_totals = {}

    for play in all_plays:
        batter_id = play["responsible_batter_id"]

        if (
            batter_id in ryan_matchups
            and play["is_pitcher_encounter"]
        ):
            if batter_id not in opponent_retrosheet_totals:
                opponent_retrosheet_totals[batter_id] = {
                    "encounters": 0,
                    "strikeouts": 0,
                }

            opponent_retrosheet_totals[batter_id]["encounters"] += 1

            if play["is_strikeout"]:
                opponent_retrosheet_totals[batter_id]["strikeouts"] += 1

    validate_opponent_season_differences(
        opponent_retrosheet_totals,
        batter_strikeout_profiles,
    )

    # ====================================================
    # MORE CALLS
    # ====================================================

    ryan_encounters = get_ryan_1973_encounters(
        pitching_data,
    )

    ryan_strikeout_tendency = calculate_ryan_1973_strikeout_tendency(
        pitching_data,
        ryan_encounters,
    )

    al_1973_strikeout_tendency = calculate_1973_al_strikeout_tendency(
        pitching_data,
    )

    patek_strikeout_tendency = (
        batter_strikeout_profiles["patef101"]["strikeout_tendency"]
    )

    patek_ryan_strikeout_probability = calculate_matchup_probability(
        patek_strikeout_tendency,
        ryan_strikeout_tendency,
        al_1973_strikeout_tendency,
    )

    patek_ryan_encounters = ryan_matchups["patef101"]["encounters"]

    patek_ryan_actual_strikeouts = ryan_matchups["patef101"]["strikeouts"]

    patek_ryan_expected_strikeouts = (
        patek_ryan_encounters * patek_ryan_strikeout_probability
    )

    patek_other_pitcher_strikeout_tendency = (
        calculate_strikeout_tendency_excluding_matchup(
            batter_strikeout_profiles["patef101"]["strikeouts"],
            batter_strikeout_profiles["patef101"]["plate_appearances"],
            patek_ryan_actual_strikeouts,
            patek_ryan_encounters,
        )
    )

    pitcher_batter_comparisons = build_pitcher_batter_comparisons(
        ryan_matchups,
        batter_strikeout_profiles,
        ryan_strikeout_tendency,
        al_1973_strikeout_tendency,
    )

    # ====================================================
    # EXPECTED STRIKEOUT COMPARISON
    # ====================================================

    matchup_comparison_data = pd.DataFrame.from_dict(
        pitcher_batter_comparisons,
        orient="index",
    )

    total_expected_strikeouts = matchup_comparison_data[
        "expected_strikeouts"
    ].sum()

    sorted_matchup_comparisons = matchup_comparison_data.sort_values(
        by="strikeout_difference",
        ascending=False,
    )

    aggregate_strikeout_difference = sorted_matchup_comparisons[
        "strikeout_difference"
    ].sum()

    # ====================================================
    # MATCHUP SUMMARY TOTALS
    # ====================================================

    total_encounters = 0
    total_strikeouts = 0

    for batter_id in ryan_matchups:
        batter_matchup = ryan_matchups[batter_id]

        total_encounters += batter_matchup["encounters"]
        total_strikeouts += batter_matchup["strikeouts"]

    overall_strikeout_difference = (
            total_strikeouts - total_expected_strikeouts
        )

    if not math.isclose(
            aggregate_strikeout_difference,
            overall_strikeout_difference,
            abs_tol=1e-9,
        ):
            raise AssertionError(
                "Matchup differences did not reconcile with overall totals."
            )

    print("PASS: Matchup differences reconcile with overall totals.")

    comparison_encounters = matchup_comparison_data["encounters"].sum()
    comparison_actual_strikeouts = matchup_comparison_data[
        "actual_strikeouts"
    ].sum()

    if comparison_encounters != total_encounters:
        raise AssertionError(
            "Comparison Table encounters did not match source matchup totals."
        )

    if comparison_actual_strikeouts != total_strikeouts:
        raise AssertionError(
            "Comparison table strikeouts did not match source matchup totals."
        )

    print("PASS: Comparison table counts match source matchup totals.")

    # ====================================================
    # EVEN MORE CALLS
    # ====================================================

    excluded_matchup_comparisons = build_excluded_matchup_comparisons(
        ryan_matchups,
        batter_strikeout_profiles,
        total_strikeouts,
        total_encounters,
        al_1973_strikeout_tendency,
    )




    excluded_total_expected_strikeouts = 0.0
    excluded_total_actual_strikeouts = 0
    matchup_total_squared_error = 0.0
    pitcher_only_total_squared_error = 0.0

    for batter_id in excluded_matchup_comparisons:
        comparison = excluded_matchup_comparisons[batter_id]
        excluded_total_expected_strikeouts += comparison["expected_strikeouts"]
        excluded_total_actual_strikeouts += comparison["actual_strikeouts"]
        encounters = comparison["encounters"]
        strikeouts = comparison["actual_strikeouts"]
        matchup_probability = comparison["matchup_probability"]
        pitcher_only_probability = comparison["pitcher_only_probability"]

        matchup_total_squared_error += (
            strikeouts * (1 - matchup_probability) ** 2
            + (encounters - strikeouts) * matchup_probability ** 2
        )

        pitcher_only_total_squared_error += (
            strikeouts * (1 - pitcher_only_probability) ** 2
            + (encounters - strikeouts) * pitcher_only_probability ** 2
        )

        matchup_brier_score = matchup_total_squared_error / total_encounters
        pitcher_only_brier_score = (
            pitcher_only_total_squared_error / total_encounters
        )


    matchup_total_absolute_error = 0.0
    pitcher_only_total_absolute_error = 0.0

    for batter_id in excluded_matchup_comparisons:
        comparison = excluded_matchup_comparisons[batter_id]
        actual = comparison["actual_strikeouts"]
        matchup_total_absolute_error += abs(
            actual - comparison["expected_strikeouts"]
        )
        pitcher_only_total_absolute_error += abs(
            actual - comparison["pitcher_only_expected_strikeouts"]
        )



    ryan_other_batter_strikeout_tendency = (
        calculate_strikeout_tendency_excluding_matchup(
            total_strikeouts,
            total_encounters,
            patek_ryan_actual_strikeouts,
            patek_ryan_encounters,
        )
    )

    patek_ryan_excluded_matchup_probability = calculate_matchup_probability(
        patek_other_pitcher_strikeout_tendency,
        ryan_other_batter_strikeout_tendency,
        al_1973_strikeout_tendency,
    )

    # ====================================================
    # DISPLAY DATA
    # ====================================================

    print()
    print("===============================================================")
    print()

    print(f"Parsed play records: {len(all_plays)}")
    print(f"Batters credited with Ryan encounters: {len(ryan_matchups)}")

    print()
    print("===============================================================")
    print()

    print(f"Batter profiles built: {len(batter_strikeout_profiles)}")

    print()
    print("===============================================================")
    print()

    print(f"Patek's 1973 profile: {batter_strikeout_profiles['patef101']}")

    print()
    print("===============================================================")
    print()

    print(f"Patek vs. Ryan: {ryan_matchups['patef101']}")

    print()
    print("===============================================================")
    print()

    print(f"Aggregated encounters: {total_encounters}")
    print(f"Aggregated strikeouts: {total_strikeouts}")

    print()
    print("===============================================================")
    print()

    print(f"Lahman people records: {len(people_data)}")

    print()
    print("===============================================================")
    print()

    print(f"Mapped Player IDs: {len(player_id_mapping)}")

    print()
    print("===============================================================")
    print()

    print(f"Ryan's 1973 strikeout tendency: {ryan_strikeout_tendency}")
    print(f"AL 1973 strikeout tendency:     {al_1973_strikeout_tendency}")

    print()
    print("===============================================================")
    print()

    print(
        f"Patek vs. Ryan estimated strikeout probability: "
        f"{patek_ryan_strikeout_probability:.2%}"
    )

    print()
    print("===============================================================")
    print()

    print(f"Patek vs. Ryan encounters: {patek_ryan_encounters}")
    print(f"Expected strikeouts: {patek_ryan_expected_strikeouts:.2f}")
    print(f"Actual strikeouts: {patek_ryan_actual_strikeouts}")

    print()
    print("===============================================================")
    print()

    print(f"Model expected strikeouts: {total_expected_strikeouts:.2f}")
    print(f"Recorded strikeouts:       {total_strikeouts}")

    print()
    print("===============================================================")
    print()

    print(f"Batter comparisons built: {len(pitcher_batter_comparisons)}")
    print(f"Patek comparison: {pitcher_batter_comparisons['patef101']}")

    print()
    print("===============================================================")
    print()

    print(sorted_matchup_comparisons.head())
    print("\nLargest negative strikeout difference:")
    print(sorted_matchup_comparisons.tail())

    print()
    print("===============================================================")
    print()

    print(f"Aggregate strikeout difference: {aggregate_strikeout_difference:.2f}")

    print()
    print("===============================================================")
    print()

    print(
        f"Patek strikeout tendency excluding Ryan: "
        f"{patek_other_pitcher_strikeout_tendency:.2%}"
    )

    print()
    print("===============================================================")
    print()

    print(
        f"Ryan strikeout tendency excluding Patek: "
        f"{ryan_other_batter_strikeout_tendency:.2%}"
    )

    print()
    print("===============================================================")
    print()

    print(
        f"Patek vs Ryan estimate with their encounters excluded: "
        f"{patek_ryan_excluded_matchup_probability:.2%}"
    )

    print()
    print("===============================================================")
    print()

    print(f"Opponent season totals built: {len(opponent_retrosheet_totals)}")
    print(f"Patek Retrosheet totals: {opponent_retrosheet_totals['patef101']}")

    print()
    print("===============================================================")
    print()

    print(f"Excluded comparisons built: {len(excluded_matchup_comparisons)}")
    print(f"Patek excluded comparison: {excluded_matchup_comparisons['patef101']}")

    print()
    print("===============================================================")
    print()

    print(f"Total expected strikeouts: {excluded_total_expected_strikeouts}")
    print(f"Total actual strikeouts: {excluded_total_actual_strikeouts}")

    print()
    print("===============================================================")
    print()

    print(f"Matchup total absolute error: {matchup_total_absolute_error}")
    print(f"Pitcher only absolute error:  {pitcher_only_total_absolute_error}")

    print()
    print("===============================================================")
    print()

    print(f"Matchup Brier Score:      {matchup_brier_score}")
    print(f"Pitcher Only Brier Score: {pitcher_only_brier_score}")

    print()
    print("===============================================================")
    print()

    print(f"Ryan's Allowed Hits: {ryan_allowed_hits}")
    print(f"Ryan's Total Allowed Hits: {ryan_total_hits}")

    print()
    print("===============================================================")
    print()

    print(f"Ryan's Hit Probabilities: {ryan_hits_probabilities}")

    print()
    print("===============================================================")
    print()

    print(f"Cobb 1911 Hit Types: {cobb_1911_hit_types}")
    print(f"Cobb 1911 hit probabilities: {cobb_1911_hit_probabilities}")

    print()
    print("===============================================================")
    print()


if __name__ == "__main__":
    main()
