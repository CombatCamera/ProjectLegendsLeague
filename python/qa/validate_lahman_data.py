"""
Project LegendsLeague
Lahman Data Validation

Purpose:
    Validate the historical Lahman data required by the LegendsLeague
    normalization and simulation pipelines.

Responsibilities:
    - Confirm required historical statistics are available.
    - Validate league-level data completeness for selected seasons.
    - Compare player-level and team-level aggregates where appropriate.
    - Detect missing or inconsistent statistics before normalization.
    - Protect downstream calculations from invalid historical inputs.

Current Validation Scope:
    - 1911 American League batting data
    - 1973 American League pitching data
    - Ty Cobb 1911 supporting statistics
    - Nolan Ryan 1973 supporting statistics

Data Source:
    SABR Lahman Baseball Database

Validation Principle:
    Historical inputs must be verified before they are used to construct
    era baselines, player tendencies, or normalized matchup probabilities.
"""

# =====================================================
# FUNCTIONS
# =====================================================

def validate_1911_al_hbp_availability(batting_data):
    al_1911_batting = batting_data[
        (batting_data["lgID"] == "AL")
        & (batting_data["yearID"] == 1911)
    ]

    missing_hbp_count = al_1911_batting["HBP"].isna().sum()

    print("\n1911 AL individual HBP availability:")
    print(f"Missing HBP values: {missing_hbp_count}")

    if missing_hbp_count == 0:
        print("PASS: 1911 AL individual HBP data is complete.")
    else:
        print("FAIL: 1911 AL individual HBP data is incomplete.")

    print("\n--------------------------------\n")


def validate_1911_al_hr_aggregation(batting_data, teams_data):
    al_1911_batting = batting_data[
        (batting_data["lgID"] == "AL")
        & (batting_data["yearID"] == 1911)
    ]

    al_1911_teams = teams_data[
        (teams_data["lgID"] == "AL")
        & (teams_data["yearID"] == 1911)
    ]

    player_hr_total = al_1911_batting["HR"].sum()
    team_hr_total = al_1911_teams["HR"].sum()

    print("\n1911 AL Home Run Aggregation QA:")
    print(f"Player-level HR total: {player_hr_total}")
    print(f"Team-level HR total:   {team_hr_total}")

    if player_hr_total == team_hr_total:
        print("PASS: Player and team HR totals match.")
    else:
        print("FAIL: Player and team HR totals do not match.")

    print("\n--------------------------------\n")


def validate_1911_al_sh_availability(batting_data):
    al_1911_batting = batting_data[
        (batting_data["lgID"] == "AL")
        & (batting_data["yearID"] == 1911)
    ]

    missing_sh_count = al_1911_batting["SH"].isna().sum()

    print("\n1911 AL individual SH availability:")
    print(f"Missing SH values: {missing_sh_count}")

    if missing_sh_count == 0:
        print("PASS: 1911 AL individual SH data is complete.")
    else:
        print("FAIL: 1911 AL individual SH data is incomplete.")

    print("\n--------------------------------\n")


def validate_1973_al_bfp_availability(pitching_data):
    al_1973_pitching = pitching_data[
        (pitching_data["lgID"] == "AL")
        & (pitching_data["yearID"] == 1973)
    ]

    missing_bfp_count = al_1973_pitching["BFP"].isna().sum()

    print("\n1973 AL individual BFP availability:")
    print(f"Missing BFP values: {missing_bfp_count}")

    if missing_bfp_count == 0:
        print("PASS: 1973 AL individual BFP data is complete.")
    else:
        print("FAIL: 1973 AL individual BFP data is incomplete.")

    print("\n--------------------------------\n")
