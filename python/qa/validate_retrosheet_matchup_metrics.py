"""
Project LegendsLeague
Retrosheet Matchup Metrics Validation

Purpose:
    Validate the matchup metrics derived from Retrosheet play data and
    Lahman historical statistics.

Responsibilities:
    - Validate pitcher-batter matchup aggregation.
    - Validate batter strikeout profile construction.
    - Validate multi-stint batter season aggregation.
    - Confirm missing batter seasons and statistics are rejected.
    - Validate pitcher-batter expected strikeout comparisons.
    - Validate strikeout tendency calculations excluding direct matchups.
    - Validate inherited strikeout responsibility.
    - Validate excluded-matchup comparison calculations.
    - Validate pitcher hit-type aggregation.
    - Validate hit-type probability calculations.
    - Confirm Nolan Ryan's 1973 hit totals and hit-type probabilities.
    - Confirm Ty Cobb's 1911 hit totals and hit-type probabilities.
    - Validate singles derived from total hit components.

Historical Cross-Checks:
    Nolan Ryan (1973)
        - Total Hits Allowed: 238
        - Singles: 162
        - Doubles: 53
        - Triples: 5
        - Home Runs: 18

    Ty Cobb (1911)
        - Total Hits: 248
        - Singles: 169
        - Doubles: 47
        - Triples: 24
        - Home Runs: 8

Validation Principle:
    Retrosheet-derived matchup metrics and Lahman season statistics must
    reconcile with known historical totals before they are used for
    cross-era normalization or simulation.
"""

# =============================================
# IMPORTS
# =============================================

import math
import pandas as pd

from python.calculations.retrosheet_matchup_metrics import (
    aggregate_pitcher_batter_matchups,
    build_batter_strikeout_profiles,
    build_pitcher_batter_comparisons,
    calculate_strikeout_tendency_excluding_matchup,
    build_excluded_matchup_comparisons,
    aggregate_pitcher_hit_types,
    calculate_hit_types_probabilities,
    calculate_singles_from_hit_totals,
)

from python.data.retrosheet_event_parser import (
    parse_retrosheet_event_directory,
)

from python.data.load_lahman_data import (
    load_required_files,
)

from python.players.cobb import calculate_cobb_1911_singles


# =============================================
# FUNCTIONS
# =============================================

def validate_pitcher_batter_matchup_aggregation():

    play_data = [
        {
            "batter_id": "patef101",
            "responsible_batter_id": "patef101",
            "pitcher_id": "ryann001",
            "is_pitcher_encounter": True,
            "is_strikeout": True,
        },
        {
            "batter_id": "patef101",
            "responsible_batter_id": "patef101",
            "pitcher_id": "ryann001",
            "is_pitcher_encounter": True,
            "is_strikeout": False,
        },
        {
            "batter_id": "rojac101",
            "responsible_batter_id": "rojac101",
            "pitcher_id": "ryann001",
            "is_pitcher_encounter": True,
            "is_strikeout": True,
        },
        {
            "batter_id": "otisa001",
            "responsible_batter_id": "otisa001",
            "pitcher_id": "ryann001",
            "is_pitcher_encounter": False,
            "is_strikeout": False,
        },
        {
            "batter_id": "maybj101",
            "responsible_batter_id": "maybj101",
            "pitcher_id": "busbs101",
            "is_pitcher_encounter": True,
            "is_strikeout": True,
        },
    ]

    expected_matchups = {
        "patef101": {
            "encounters": 2,
            "strikeouts": 1,
        },
        "rojac101": {
            "encounters": 1,
            "strikeouts": 1,
        },
    }

    pitcher_batter_matchups = aggregate_pitcher_batter_matchups(
        play_data,
        "ryann001",
    )

    if pitcher_batter_matchups != expected_matchups:
        raise AssertionError(
            "Test Failed: Pitcher-batter matchup totals did not match."
        )

    print("Test Passed: Pitcher-batter matchup totals matched.")
    print(f"Expected matchups: {expected_matchups}")
    print(f"Actual matchups:   {pitcher_batter_matchups}")


def validate_batter_strikeout_profile():

    batting_data = pd.DataFrame([
        {
            "playerID": "patekfr01",
            "yearID": 1973,
            "AB": 501,
            "BB": 54,
            "HBP": 3,
            "SH": 11,
            "SF": 2,
            "SO": 63,
        }
    ])

    player_id_mapping = {
        "patef101": "patekfr01",
    }

    year_id = 1973

    expected_profile = {
        "patef101": {
            "lahman_player_id": "patekfr01",
            "plate_appearances": 571,
            "strikeouts": 63,
            "strikeout_tendency": 63 / 571,
        }
    }

    batter_strikeout_profile = build_batter_strikeout_profiles(
        batting_data,
        player_id_mapping,
        year_id,
    )

    actual_patek_profile = batter_strikeout_profile["patef101"]
    expected_patek_profile = expected_profile["patef101"]

    if (
        actual_patek_profile["lahman_player_id"]
        != expected_patek_profile["lahman_player_id"]
    ):
        raise AssertionError(
            "Test Failed: Patek's Lahman player ID did not match."
        )

    if (
        actual_patek_profile["plate_appearances"]
                             != expected_patek_profile["plate_appearances"]
    ):
        raise AssertionError(
            "Test Failed: Patek's plate appearances did not match."
        )

    if (
        actual_patek_profile["strikeouts"]
        != expected_patek_profile["strikeouts"]
    ):
        raise AssertionError(
            "Test Failed: Patek's strikeouts did not match."
        )

    if not math.isclose(
        actual_patek_profile["strikeout_tendency"],
        expected_patek_profile["strikeout_tendency"],
    ):
        raise AssertionError(
            "Test Failed: Patek's strikeout tendency did not match."
        )

    print("Test Passed: Patek's batter strikeout profile matched.")
    print(f"Expected profile: {expected_profile}")
    print(f"Actual profile: {batter_strikeout_profile}")


def validate_multi_stint_batter_strikeout_profile():

    batting_data = pd.DataFrame([
        {
            "playerID": "thompm01",
            "yearID": 1973,
            "stint": 1,
            "AB": 80,
            "BB": 15,
            "HBP": 2,
            "SH": 2,
            "SF": 1,
            "SO": 10,
        },
        {
            "playerID": "thompm01",
            "yearID": 1973,
            "stint": 2,
            "AB": 170,
            "BB": 20,
            "HBP": 3,
            "SH": 4,
            "SF": 3,
            "SO": 40,
        },
    ])

    player_id_mapping = {
        "thompsoma001": "thompm01"
    }

    year_id = 1973

    expected_profile = {
        "thompsoma001": {
            "lahman_player_id": "thompm01",
            "plate_appearances": 300,
            "strikeouts": 50,
            "strikeout_tendency": 50 / 300,
        }
    }

    batter_profile = build_batter_strikeout_profiles(
        batting_data,
        player_id_mapping,
        year_id,
    )


    actual_player_profile = batter_profile["thompsoma001"]
    expected_player_profile = expected_profile["thompsoma001"]


    if actual_player_profile != expected_player_profile:
        raise AssertionError(
            "Test Failed: The actual player profile did not match the expected player profile."
        )

    print("Test Passed: The actual player profile matched the expected player profile.")
    print(f"Expected Profile:      {expected_player_profile}")
    print(f"Actual Player Profile: {actual_player_profile}")


def validate_missing_batter_season():

    batting_data = pd.DataFrame([
            {
                "playerID": "patekfr01",
                "yearID": 1972,
                "AB": 501,
                "BB": 54,
                "HBP": 3,
                "SH": 11,
                "SF": 2,
                "SO": 63,
            }
        ])

    player_id_mapping = {
            "patef101": "patekfr01",
        }

    year_id = 1973

    try:
        build_batter_strikeout_profiles(
            batting_data,
            player_id_mapping,
            year_id,
        )
    except ValueError:
        print("Test Passed: Missing batter season was rejected.")
        return

    raise AssertionError(
        "Test Failed: Missing batter season was accepted."
    )


def validate_missing_batter_statistic():

    batting_data = pd.DataFrame([
                {
                    "playerID": "patekfr01",
                    "yearID": 1973,
                    "AB": 501,
                    "BB": 54,
                    "HBP": 3,
                    "SH": 11,
                    "SF": 2,
                    "SO": pd.NA,
                }
            ])

    player_id_mapping = {
            "patef101": "patekfr01",
        }

    year_id = 1973

    try:
        build_batter_strikeout_profiles(
            batting_data,
            player_id_mapping,
            year_id,
        )
    except ValueError:
        print("Test Passed: Missing batter statistic was rejected.")
        return

    raise AssertionError(
        "Test Failed: Missing batter statistic was accepted."
    )


def validate_pitcher_batter_comparisons():

    pitcher_batter_matchups = {
        "batter_a": {
            "encounters": 10,
            "strikeouts": 3,
        },
        "batter_b": {
            "encounters": 20,
            "strikeouts": 5,
        },
    }

    batter_strikeout_profiles = {
        "batter_a": {
            "strikeout_tendency": 0.10,
        },
        "batter_b": {
            "strikeout_tendency": 0.40,
        },
    }

    pitcher_probability = 0.20
    league_probability = 0.20

    expected_comparisons = {
        "batter_a": {
            "encounters": 10,
            "actual_strikeouts": 3,
            "expected_strikeouts": 1.0,
            "strikeout_difference": 2.0,
        },
        "batter_b": {
            "encounters": 20,
            "actual_strikeouts": 5,
            "expected_strikeouts": 8.0,
            "strikeout_difference": -3.0,
        },
    }

    actual_comparisons = build_pitcher_batter_comparisons(
        pitcher_batter_matchups,
        batter_strikeout_profiles,
        pitcher_probability,
        league_probability,
    )

    if actual_comparisons.keys() != expected_comparisons.keys():
        raise AssertionError(
            "Test failed: Comparison batter IDs did not match."
        )

    for batter_id in expected_comparisons:
        actual_comparison = actual_comparisons[batter_id]
        expected_comparison = expected_comparisons[batter_id]

        if actual_comparison["encounters"] != expected_comparison["encounters"]:
            raise AssertionError(
                f"Test Failed: Encounters did not match for {batter_id}."
            )

        if (
            actual_comparison["actual_strikeouts"]
            != expected_comparison["actual_strikeouts"]
        ):
            raise AssertionError(
                f"Test Failed: Actual strikeouts did not match for {batter_id}."
            )

        if not math.isclose(
            actual_comparison["expected_strikeouts"],
            expected_comparison["expected_strikeouts"],
            abs_tol=1e-9,
        ):

            raise AssertionError(
                f"Test Failed: Expected strikeouts did not match for {batter_id}."
            )

        if not math.isclose(
            actual_comparison["strikeout_difference"],
            expected_comparison["strikeout_difference"],
            abs_tol=1e-9,
        ):

            raise AssertionError(
                f"Test Failed: Strikeout difference did not match for {batter_id}."
            )

    print("Test Passed: Both batter comparisons matched expected results.")
    print(f"Expected comparisons: {expected_comparisons}")
    print(f"Actual comparisons:   {actual_comparisons}")


def validate_strikeout_tendency_excluding_matchup():

    season_strikeouts = 20
    season_encounters = 100
    matchup_strikeouts = 8
    matchup_encounters = 25

    expected_tendency = 0.16

    strikeout_tendency = calculate_strikeout_tendency_excluding_matchup(
        season_strikeouts,
        season_encounters,
        matchup_strikeouts,
        matchup_encounters,
    )

    if not math.isclose(strikeout_tendency, expected_tendency):
        raise AssertionError(
            "Test Failed: Strikeout tendency exluding matchup did not match."
        )

    print("Test Passed: Strikeout tendency excluding matchup matched.")
    print(f"Expected tendency: {expected_tendency}")
    print(f"Actual tendency: {strikeout_tendency}")


def validate_exclusion_with_no_remaining_encounters():

    season_strikeouts = 20
    season_encounters = 100
    matchup_strikeouts = 20
    matchup_encounters = 100

    try:
        calculate_strikeout_tendency_excluding_matchup(
            season_strikeouts,
            season_encounters,
            matchup_strikeouts,
            matchup_encounters,
        )
    except ValueError:
        print("Test Passed: Expected error occurred.")
        return

    raise AssertionError(
        "Test Failed: Expected error did not occur."
    )


def validate_exclusion_with_zero_remaining_strikeouts():

    season_strikeouts = 5
    season_encounters = 100
    matchup_strikeouts = 5
    matchup_encounters = 20

    expected_tendency = 0.0

    strikeout_tendency = calculate_strikeout_tendency_excluding_matchup(
        season_strikeouts,
        season_encounters,
        matchup_strikeouts,
        matchup_encounters,
    )

    if not math.isclose(strikeout_tendency, expected_tendency):
        raise AssertionError(
            "Test Failed: Exclusion w/zero remaining strikeouts did not match."
        )

    print("Test Passed: Exclusion w/zero remaining strikeouts matched.")
    print(f"Expected tendency: {expected_tendency}")
    print(f"Actual tendency: {strikeout_tendency}")


def validate_exclusion_with_negative_remaining_strikeouts():

    season_strikeouts = 5
    season_encounters = 100
    matchup_strikeouts = 6
    matchup_encounters = 20

    try:
        calculate_strikeout_tendency_excluding_matchup(
            season_strikeouts,
            season_encounters,
            matchup_strikeouts,
            matchup_encounters,
        )
    except ValueError:
        print("ValueError check")
        print("Test Passed: Expected error occurred.")
        return

    raise AssertionError(
        "Test Failed: Expected error did not occur."
    )


def validate_exclusion_with_strikeouts_exceeding_encounters():

    season_strikeouts = 20
    season_encounters = 100
    matchup_strikeouts = 0
    matchup_encounters = 90

    try:
        calculate_strikeout_tendency_excluding_matchup(
            season_strikeouts,
            season_encounters,
            matchup_strikeouts,
            matchup_encounters,
        )
    except ValueError:
        print("ValueError check - strikeouts exceeding encounters.")
        print("Test Passed: Expected error occurred.")
        return

    raise AssertionError(
        "Test Failed: Expected error did not occur."
    )


def validate_inherited_strikeout_matchup_aggregation():

    play_data = [
        {
            "batter_id": "hende103",
            "responsible_batter_id": "wille101",
            "pitcher_id": "thompm001",
            "is_pitcher_encounter": True,
            "is_strikeout": True,
        },
    ]


    expected_matchups = {
        "wille101": {
            "encounters": 1,
            "strikeouts": 1,
        },
    }

    actual_matchups = aggregate_pitcher_batter_matchups(
        play_data,
        "thompm001",
    )

    print(f"Expected matchups: {expected_matchups}")
    print(f"Actual matchups:   {actual_matchups}")

    if actual_matchups != expected_matchups:
            raise AssertionError(
                "Inherited strikeout was assigned to the wrong batter."
            )

    print("PASS: Inherited strikeout assigned to Williams.")


def validate_excluded_matchup_comparisons():

    pitcher_batter_matchups = {
        "batter_a": {"encounters": 10, "strikeouts": 5},
    }
    batter_strikeout_profiles = {
        "batter_a": {
            "plate_appearances": 100,
            "strikeouts": 20,
        },
    }

    comparisons = build_excluded_matchup_comparisons(
        pitcher_batter_matchups,
        batter_strikeout_profiles,
        30,     # Pitcher season strikeouts
        100,    # Pitcher season encounters
        0.20,   # League strikeout probability
    )

    print(f"Excluded matchup comparison: {comparisons['batter_a']}")

    comparison = comparisons["batter_a"]

    expected_pitcher_only_strikeouts = 25 / 9

    if not math.isclose(
        comparison["pitcher_only_expected_strikeouts"],
        expected_pitcher_only_strikeouts,
    ):

        raise AssertionError(
            "Pitcher-only expected strikeouts did not match."
        )

    expected_probability = 4 / 17

    if not math.isclose(
        comparison["matchup_probability"],
        expected_probability,
    ):
        raise AssertionError(
            "Excluded matchup probability did not match the expected result."
        )

    expected_strikeouts = 40 / 17

    if not math.isclose(
        comparison["expected_strikeouts"],
        expected_strikeouts,
    ):
        raise AssertionError(
            "Excluded matchup strikeouts did not match the expected results."
        )

    print("PASS: Excluded matchup probability and strikeouts matched.")


def validate_aggregate_pitcher_hit_types():

    play_data = [
        {
            "pitcher_id": "ryann001",
            "is_pitcher_encounter": True,
            "hit_type": "single",
        },

        {
            "pitcher_id": "ryann001",
            "is_pitcher_encounter": True,
            "hit_type": "double"
        },

        {
            "pitcher_id": "thompm001",
            "is_pitcher_encounter": True,
            "hit_type": "home_run"
        },
    ]

    expected_ryan_counts = {
        "single": 1,
        "double": 1,
        "triple": 0,
        "home_run": 0,
    }

    ryan_hit_counts = aggregate_pitcher_hit_types(play_data, "ryann001")

    if ryan_hit_counts != expected_ryan_counts:
        raise AssertionError(
            f"Test Failed: Classified hits: {ryan_hit_counts} did not match expected counts: {expected_ryan_counts}"
        )

    print(f"Test Passed: Ryan hit counts: {ryan_hit_counts} matched expected counts: {expected_ryan_counts}")


def validate_ryan_1973_hit_type_total(directory_path):

    all_plays = parse_retrosheet_event_directory(directory_path)

    ryan_hit_counts = aggregate_pitcher_hit_types(all_plays, "ryann001")

    expected_total = 238

    ryan_total = sum(ryan_hit_counts.values())

    if ryan_total != expected_total:
        raise AssertionError(
            "Test Failed: Ryan's total and expected total do not match."
        )

    print(f"Test Passed: Ryan's totals {ryan_total}, and expected total {expected_total} match.")


def validate_pitcher_hit_type_probabilities():

    allowed_hits = {
        "single": 125,
        "double": 50,
        "triple": 20,
        "home_run": 5,
    }

    expected_hits = {
        "single": 0.625,
        "double":  0.25,
        "triple": 0.1,
        "home_run": 0.025,
    }

    actual_hits = calculate_hit_types_probabilities(allowed_hits)

    if actual_hits != expected_hits:
        raise AssertionError(
            "Test Failed: Actual and expected hits did not match."
        )

    print(
        f"Test Passed: Actual hit probabilities {actual_hits} "
        f"matched expected hit probabilities {expected_hits}"
    )


def validate_ryan_1973_hit_type_probabilities(directory_path):

    all_plays = parse_retrosheet_event_directory(
        directory_path,
    )

    ryan_hit_counts = aggregate_pitcher_hit_types(
        all_plays,
        "ryann001",
    )

    ryan_hit_probabilities = calculate_hit_types_probabilities(
        ryan_hit_counts
    )

    expected_probabilities = {
        "single": 162 / 238,
        "double": 53 / 238,
        "triple": 5 / 238,
        "home_run": 18 / 238,
    }

    for hit_type in expected_probabilities:
        if not math.isclose(
            ryan_hit_probabilities[hit_type],
            expected_probabilities[hit_type],
        ):
            raise AssertionError(
                f"Test Failed: Ryan's {hit_type} probability did not match."
            )

    total_probability = sum(
        ryan_hit_probabilities.values()
    )

    if not math.isclose(total_probability, 1.0):
        raise AssertionError(
            "Test Failed: Ryan's hit type probabilities did not sum to 1.0."
        )

    print(
        "Test Passed: Ryan's 1973 hit type probabilities matched "
        "expected values and summed to 1.0"
    )


def validate_singles_from_hit_totals():

    total_hits = 20
    doubles = 5
    triples = 2
    home_runs = 3

    expected_singles = 10

    actual_singles = calculate_singles_from_hit_totals(
        total_hits,
        doubles,
        triples,
        home_runs,
    )

    if actual_singles != expected_singles:
        raise AssertionError(
            f"Test Failed: Actual singles {actual_singles} "
            f"and expected singles {expected_singles} did not match."
        )

    print(f"Test Passed: Actual {actual_singles} and expected singles {expected_singles} matched.")


def validate_cobb_1911_hit_type_totals(batting_data):

    cobb_1911_batting_data = batting_data[
        (batting_data["playerID"] == 'cobbty01')
        & (batting_data["yearID"] == 1911)
    ]

    hits = cobb_1911_batting_data["H"].sum()
    doubles = cobb_1911_batting_data["2B"].sum()
    triples = cobb_1911_batting_data["3B"].sum()
    home_runs = cobb_1911_batting_data["HR"].sum()

    singles = calculate_singles_from_hit_totals(
        hits,
        doubles,
        triples,
        home_runs,
    )

    expected_hits = 248

    cobb_hits = sum(
        [
            singles,
            doubles,
            triples,
            home_runs,
        ]
    )

    if cobb_hits != expected_hits:
        raise AssertionError(
            "Test Failed: Cobb's hits did not match the expected hits. "
        )

    print(f"Test Passed: Cobb's Hits {cobb_hits} matched expected hits { expected_hits}.")


def validate_cobb_1911_hit_type_probabilities(batting_data):

    cobb_hit_counts = calculate_cobb_1911_singles(batting_data)

    cobb_hit_probabilities = calculate_hit_types_probabilities(
        cobb_hit_counts,
    )

    expected_probabilities = {
        "single": 169 / 248,
        "double": 47 / 248,
        "triple": 24 / 248,
        "home_run": 8 / 248,
    }

    for hit_type in expected_probabilities:
        if not math.isclose(
            cobb_hit_probabilities[hit_type],
            expected_probabilities[hit_type],
        ):
            raise AssertionError(
                f"Test Failed: Cobb's {hit_type} probability did not match."
            )

    total_probability = sum(
        cobb_hit_probabilities.values()
    )

    if not math.isclose(total_probability, 1.0):
        raise AssertionError(
            "Test Failed: Cobb's hit type probabilities did not sum to 1.0."
        )

    print(
        "Test Passed: Cobb's 1911 hit type probabilities matched "
        "expected values and summed to 1.0"
    )


# =============================================
# MAIN
# =============================================

def main():

    directory_path = "data/raw/retrosheet/1973"

    loaded_files = load_required_files(
        verbose=False,
    )

    batting_data = loaded_files["Batting.csv"]

    print()
    print("=============================================")
    print()

    validate_pitcher_batter_matchup_aggregation()

    print()
    print("=============================================")
    print()

    validate_batter_strikeout_profile()

    print()
    print("=============================================")
    print()

    validate_multi_stint_batter_strikeout_profile()

    print()
    print("=============================================")
    print()

    validate_missing_batter_season()

    print()
    print("=============================================")
    print()

    validate_missing_batter_statistic()

    print()
    print("=============================================")
    print()

    validate_pitcher_batter_comparisons()

    print()
    print("=============================================")
    print()

    validate_strikeout_tendency_excluding_matchup()

    print()
    print("=============================================")
    print()

    validate_exclusion_with_no_remaining_encounters()

    print()
    print("=============================================")
    print()

    validate_exclusion_with_zero_remaining_strikeouts()

    print()
    print("=============================================")
    print()

    validate_exclusion_with_negative_remaining_strikeouts()

    print()
    print("=============================================")
    print()

    validate_exclusion_with_strikeouts_exceeding_encounters()

    print()
    print("=============================================")
    print()

    validate_inherited_strikeout_matchup_aggregation()

    print()
    print("=============================================")
    print()

    validate_excluded_matchup_comparisons()

    print()
    print("=============================================")
    print()

    validate_aggregate_pitcher_hit_types()

    print()
    print("=============================================")
    print()

    validate_ryan_1973_hit_type_total(directory_path)

    print()
    print("=============================================")
    print()

    validate_pitcher_hit_type_probabilities()

    print()
    print("=============================================")
    print()

    validate_ryan_1973_hit_type_probabilities(directory_path)

    print()
    print("=============================================")
    print()

    validate_singles_from_hit_totals()

    print()
    print("=============================================")
    print()

    validate_cobb_1911_hit_type_totals(batting_data)

    print()
    print("=============================================")
    print()

    validate_cobb_1911_hit_type_probabilities(batting_data)

    print()
    print("=============================================")
    print()











if __name__ == "__main__":
    main()
