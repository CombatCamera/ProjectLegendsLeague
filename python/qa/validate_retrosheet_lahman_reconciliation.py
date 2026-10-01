"""
Project LegendsLeague
Retrosheet-Lahman Reconciliation Validation

Purpose:
    Validate documented season-level differences between Retrosheet
    matchup totals and Lahman batter statistics.

Responsibilities:
    - Compare Retrosheet opponent encounter totals against Lahman
      plate appearance totals.
    - Compare Retrosheet strikeout totals against Lahman strikeout totals.
    - Record only players with mismatched historical totals.
    - Confirm observed differences match the documented reconciliation set.
    - Protect downstream matchup analysis from unexplained source discrepancies.

Validation Scope:
    - Opponent plate appearances / encounters
    - Opponent strikeouts
    - Known Retrosheet-Lahman season discrepancies

Validation Principle:
    Historical data sources can disagree in small, documented ways.
    LegendsLeague should preserve and explicitly validate those known
    differences rather than silently forcing the sources to match.
"""
# ================================================
# FUNCTION
# ================================================

def validate_opponent_season_differences(
    opponent_retrosheet_totals,
    batter_strikeout_profiles,
):

    mismatch_differences = {}

    for batter_id in opponent_retrosheet_totals:
        retrosheet_totals = opponent_retrosheet_totals[batter_id]
        lahman_profile = batter_strikeout_profiles[batter_id]

        if (
            retrosheet_totals["encounters"]
            != lahman_profile["plate_appearances"]
            or retrosheet_totals["strikeouts"]
            != lahman_profile["strikeouts"]
        ):
            mismatch_differences[batter_id] = {
                "encounters": (
                    retrosheet_totals["encounters"]
                    - lahman_profile["plate_appearances"]
                ),
                "strikeouts": (
                    retrosheet_totals["strikeouts"]
                    - lahman_profile["strikeouts"]
                ),
            }

    documented_differences = {
        "munst101": {"encounters": 0, "strikeouts": 1},
        "alouf101": {"encounters": 0, "strikeouts": -1},
        "murcb101": {"encounters": 0, "strikeouts": 1},
        "may-c101": {"encounters": 0, "strikeouts": -1},
        "reicr101": {"encounters": 1, "strikeouts": 0},
        "herre102": {"encounters": -1, "strikeouts": 1},
        "sharb102": {"encounters": 1, "strikeouts": 0},
        "aloum101": {"encounters": 0, "strikeouts": -1},
        "lowej001": {"encounters": 1, "strikeouts": 0},
        "downb001": {"encounters": 0, "strikeouts": 1},
    }

    if mismatch_differences != documented_differences:
        raise AssertionError(
            "Season differences do not match documented values."
        )

    print("PASS: Season differences match documented values.")
