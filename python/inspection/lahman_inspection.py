def inspect_ty_cobb_batting(batting_data):
    cobb_data = batting_data[
        batting_data["playerID"] == "cobbty01"
    ]

    print("\nTy Cobb batting records:")
    print(
        cobb_data[
            [
                "yearID",
                "G",
                "AB",
                "H",
                "2B",
                "3B",
                "HR",
                "BB",
                "SO",
                "HBP",
            ]
        ]
    )

    print("\n--------------------------------\n")


def inspect_nolan_ryan_pitching(pitching_data):
    ryan_data = pitching_data[
        pitching_data["playerID"] == "ryanno01"
    ]

    print("\nNolan Ryan pitching records:")
    print(
        ryan_data[
            [
                "yearID",
                "G",
                "GS",
                "IPouts",
                "H",
                "HR",
                "BB",
                "SO",
                "HBP",
                "BFP",
                "ERA",
            ]
        ]
    )

    print("\n--------------------------------\n")
    

def inspect_1911_al_environment(teams_data):
    al_1911_teams = teams_data[
        (teams_data["lgID"] == "AL")
        & (teams_data["yearID"] == 1911)
    ]

    print("\n1911 American League teams:")
    print(
        al_1911_teams[
            [
                "teamID",
                "name",
                "G",
                "AB",
                "H",
                "2B",
                "3B",
                "HR",
                "BB",
                "SO",
                "HBP",
            ]
        ]
    )

    print("\n--------------------------------\n")
    

def inspect_cobb_1911_plate_appearance(batting_data):
    
    ty_cobb_1911_batting = batting_data[
        (batting_data["playerID"] == "cobbty01")
        & (batting_data["yearID"] == 1911)
    ]
    
    print("\nTy Cobb 1911 Plate Appearance Validation:")
    print(
        ty_cobb_1911_batting[
            [
                "AB",
                "BB",
                "HBP",
                "SF",
                "SH",
            ]
        ]
    )
