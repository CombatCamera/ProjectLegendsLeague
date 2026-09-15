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
