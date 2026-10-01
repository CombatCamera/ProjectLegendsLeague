"""
Project LegendsLeague
Inspection Runner

Purpose:
    Run the primary human-readable Lahman inspection functions used during
    LegendsLeague development and historical data review.
"""


# ========================================
# IMPORTS
# ========================================
from python.data.load_lahman_data import load_required_files

from python.inspection.lahman_inspection import (
    inspect_ty_cobb_batting,
    inspect_nolan_ryan_pitching,
    inspect_1911_al_environment,
    inspect_cobb_1911_plate_appearance,
)


# ========================================
# MAIN
# ========================================

def main():

    loaded_files = load_required_files(
        verbose=False,
    )

    batting_data = loaded_files["Batting.csv"]
    pitching_data = loaded_files["Pitching.csv"]
    teams_data = loaded_files["Teams.csv"]

    inspect_ty_cobb_batting(batting_data)
    inspect_nolan_ryan_pitching(pitching_data)
    inspect_1911_al_environment(teams_data)
    inspect_cobb_1911_plate_appearance(batting_data)


if __name__ == "__main__":
    main()
