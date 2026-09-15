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

from python.data.file_checks import check_required_files

from python.data.load_lahman_data import load_required_files

from python.calculations.league_metrics import (
    calculate_1911_al_hbp_total,
    calculate_1911_al_strikeout_tendency
)

from python.qa.validate_lahman_data import (
    validate_1911_al_hbp_availability,
    validate_1911_al_hr_aggregation,
    validate_1911_al_sh_availability
)

from python.inspection.lahman_inspection import (
    inspect_ty_cobb_batting,
    inspect_nolan_ryan_pitching,
    inspect_1911_al_environment,
    inspect_cobb_1911_plate_appearance,
)

from python.players.cobb import (
    calculate_cobb_1911_plate_appearances,
    calculate_cobb_1911_strikeout_tendency,
    calculate_cobb_strikeout_avoidance
)


# ============================================
# MAIN
# ============================================

def main(): 
    
    check_required_files()   

    loaded_files = load_required_files()

    people_data = loaded_files["People.csv"]
    batting_data = loaded_files["Batting.csv"]
    pitching_data = loaded_files["Pitching.csv"]
    teams_data = loaded_files["Teams.csv"]

    inspect_ty_cobb_batting(batting_data)
    inspect_nolan_ryan_pitching(pitching_data)
    inspect_1911_al_environment(teams_data)
    validate_1911_al_hbp_availability(batting_data)
    calculate_1911_al_hbp_total(batting_data)
    validate_1911_al_hr_aggregation(batting_data, teams_data)
    inspect_cobb_1911_plate_appearance(batting_data)
    plate_appearance = calculate_cobb_1911_plate_appearances(batting_data)
    cobb_1911_strikeout_tendency = calculate_cobb_1911_strikeout_tendency(batting_data, plate_appearance)
    validate_1911_al_sh_availability(batting_data)
    al_1911_strikeout_tendency = calculate_1911_al_strikeout_tendency(batting_data)
    calculate_cobb_strikeout_avoidance(cobb_1911_strikeout_tendency, al_1911_strikeout_tendency)
    

if __name__ == "__main__":
    main()