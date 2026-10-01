"""
Project LegendsLeague
Player ID Mapping Validation

Purpose:
    Validate the mapping between Retrosheet player IDs and Lahman player IDs.

Responsibilities:
    - Confirm required Retrosheet IDs map to the correct Lahman player IDs.
    - Ignore records that do not contain a Retrosheet ID.
    - Detect ambiguous Retrosheet IDs that map to more than one Lahman player.
    - Inspect Retrosheet ID uniqueness in the loaded Lahman People dataset.
    - Protect downstream Retrosheet matchup calculations from player identity errors.

Validation Strategy:
    Controlled DataFrames are used to verify expected mapping behavior and
    ambiguity rejection, while the full Lahman People dataset is inspected
    for duplicate Retrosheet identifiers.
"""

# ==================================================
# IMPORTS
# ==================================================

import pandas as pd

from python.data.player_id_mapping import (
    build_retrosheet_to_lahman_id_mapping,
)

from python.data.load_lahman_data import (
    load_required_files
)


# ==================================================
# FUNCTIONS
# ==================================================

def validate_retrosheet_to_lahman_id_mapping():


    people_data = pd.DataFrame([
        {
            "playerID": "adducji01",
            "retroID": "adduj001",
        },
        {
            "playerID": "adducji02",
            "retroID": "adduj002",
        },
        {
            "playerID": "thompm01",
            "retroID": pd.NA,
        },
    ])


    expected_id_map = {
        "adduj001": "adducji01",
        "adduj002": "adducji02",
    }

    required_retrosheet_ids = [
        "adduj001",
        "adduj002",
    ]
    id_map = build_retrosheet_to_lahman_id_mapping(
        people_data,
        required_retrosheet_ids,
    )

    if id_map != expected_id_map:
        raise AssertionError(
            "Test Failed: ID map does not match the expected ID map."
        )

    print("Test Passed: ID map matches the expected ID map.")
    print(f"ID Map:          {id_map}")
    print(f"Expected ID Map: {expected_id_map}")


def validate_retrosheet_id_uniqueness():

    loaded_files = load_required_files(
        verbose=False,
    )

    people_data = loaded_files["People.csv"]

    people_with_retrosheet_ids = people_data[
        people_data["retroID"].notna()
    ]

    duplicate_retro_id_mask = (
        people_with_retrosheet_ids["retroID"]
        .duplicated(keep=False)
    )

    duplicate_retro_id_records = people_with_retrosheet_ids[
        duplicate_retro_id_mask
    ]

    print(
        f"Retrosheet ID duplicate records found: "
        f"{len(duplicate_retro_id_records)}"
    )


def validate_ambiguous_required_retrosheet_id():

    people_data = pd.DataFrame([
        {
            "playerID": "brownb01",
            "retroID": "browb107",
        },
        {
            "playerID": "brownba02",
            "retroID": "browb107",
        },
    ])

    required_retrosheet_ids = [
        "browb107",
    ]

    try:
        build_retrosheet_to_lahman_id_mapping(
            people_data,
            required_retrosheet_ids,
        )
    except ValueError:
        print("Test Passed: Ambiguous required Retrosheet ID was rejected.")
        return

    raise AssertionError(
            "Test Failed: Ambiguous required Retrosheet ID was accepted."
        )



# ==================================================
# MAIN
# ==================================================

def main():

    print()

    validate_retrosheet_to_lahman_id_mapping()

    print()

    validate_retrosheet_id_uniqueness()

    print()

    validate_ambiguous_required_retrosheet_id()

    print()

if __name__ == "__main__":
    main()
