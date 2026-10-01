"""
Project LegendsLeague
QA Runner

Purpose:
    Run the primary LegendsLeague validation modules from a single
    command-line entry point.

Responsibilities:
    - Launch core calculation validations.
    - Launch normalization and matchup validations.
    - Launch Retrosheet parser and matchup validations.
    - Provide one centralized QA entry point for final verification.

Design Principle:
    Major project validations should be runnable from one place so the
    complete LegendsLeague engine can be checked before release.
"""

# ========================================
# IMPORTS
# ========================================

from python.qa.validate_relative_metrics import validate_relative_avoidance
from python.qa.validate_plate_appearances import validate_plate_appearances
from python.qa.validate_strikeout_metrics import validate_strikeout_tendency
from python.qa.validate_normalization_metrics import main as run_normalization_qa
from python.qa.validate_matchup_metrics import main as run_matchup_metrics_qa

from python.qa.validate_plate_appearance_resolver import (
    main as run_plate_appearance_resolver_qa,
)

from python.qa.validate_matchup_simulator import (
    main as run_matchup_simulator_qa,
)

from python.qa.validate_player_id_mapping import (
    main as run_player_id_mapping_qa,
)

from python.qa.validate_retrosheet_event_parser import (
    main as run_retrosheet_event_parser_qa,
)

from python.qa.validate_retrosheet_matchup_metrics import (
    main as run_retrosheet_matchup_metrics_qa,
)

from python.qa.validate_probability_metrics import (
    main as run_probability_metrics_qa,
)
# ========================================
# MAIN
# ========================================

def main():

    print()
    print("========================================")
    print("CORE CALCULATION QA")
    print("========================================")
    validate_relative_avoidance()
    print()
    validate_plate_appearances()
    print()
    validate_strikeout_tendency()

    print()
    print("========================================")
    print("NORMALIZATION QA")
    print("========================================")
    run_normalization_qa()

    print()
    print("========================================")
    print("MATCHUP METRICS QA")
    print("========================================")
    run_matchup_metrics_qa()

    print()
    print("========================================")
    print("PLATE APPEARANCE RESOLVER QA")
    print("========================================")
    run_plate_appearance_resolver_qa()

    print()
    print("========================================")
    print("MATCHUP SIMULATOR QA")
    print("========================================")
    run_matchup_simulator_qa()

    print()
    print("========================================")
    print("PLAYER ID MAPPING QA")
    print("========================================")
    run_player_id_mapping_qa()

    print()
    print("========================================")
    print("RETROSHEET EVENT PARSER QA")
    print("========================================")
    run_retrosheet_event_parser_qa()

    print()
    print("========================================")
    print("RETROSHEET MATCHUP METRICS QA")
    print("========================================")
    run_retrosheet_matchup_metrics_qa()

    print()
    print("========================================")
    print("PROBABILITY METRICS QA")
    print("========================================")
    run_probability_metrics_qa()



    print()
    print("========================================")
    print("ALL LEGENDSLEAGUE QA CHECKS PASSED")
    print("========================================")
    print()

if __name__ == "__main__":
    main()
