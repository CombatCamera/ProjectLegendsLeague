"""
Project LegendsLeague
Retrosheet Event Parser Validation

Purpose:
    Validate the Retrosheet event parsing and play-assembly logic used by
    LegendsLeague to reconstruct historical batter-pitcher encounters.

Responsibilities:
    - Validate raw Retrosheet record parsing.
    - Validate starting and relief pitcher state updates.
    - Confirm active pitcher tracking is preserved correctly.
    - Validate play-record extraction and non-play rejection.
    - Validate strikeout classification.
    - Validate plate appearance classification.
    - Validate pitcher-encounter classification.
    - Validate base-running and non-plate-appearance event handling.
    - Validate full Retrosheet play-data assembly.
    - Validate single-file and directory-level parsing behavior.
    - Confirm Nolan Ryan's 1973 reconstructed totals match Lahman.
    - Validate inherited batter responsibility on mid-count substitutions.
    - Validate batter responsibility resets after completed appearances.
    - Validate hit-event classification.

Validation Scope:
    - Retrosheet start, sub, and play records
    - Active pitcher state
    - Plate appearances
    - Pitcher encounters
    - Strikeouts
    - Singles
    - Doubles
    - Triples
    - Home Runs
    - Base-running events
    - Batter substitutions
    - Catcher interference

Historical Cross-Check:
    Nolan Ryan (1973)
    - Expected Batters Faced: 1,355
    - Expected Strikeouts: 383

Validation Principle:
    Retrosheet event data must reconstruct historical pitcher-batter
    encounters consistently before it can be used for matchup metrics,
    hit-type distributions, or cross-era normalization.
"""

# ================================================
# IMPORTS
# ================================================

from python.data.retrosheet_event_parser import (
    parse_retrosheet_record,
    extract_pitcher_update,
    update_active_pitcher_state,
    get_active_pitcher_for_play,
    extract_play_data,
    is_strikeout_event,
    is_plate_appearance_event,
    build_retrosheet_play_data,
    parse_retrosheet_event_file,
    parse_retrosheet_event_directory,
    is_pitcher_encounter_event,
    classify_hit_event,
)

# ================================================
# FUNCTIONS
# ================================================

def validate_parse_retrosheet_record():

    raw_record = 'start,ryann001,"Nolan Ryan",1,0,1'


    expected_record = [
        "start",
        "ryann001",
        "Nolan Ryan",
        "1",
        "0",
        "1",
    ]

    parsed_record = parse_retrosheet_record(raw_record)


    if parsed_record != expected_record:
        raise AssertionError(
            "Test Failed: Parsed record did not match expected record."
        )

    print("Test Passed, Parsed records matched.")
    print(f"Expected record: {expected_record}")
    print(f"Parsed record:   {parsed_record}")


def validate_starting_pitcher_update():

    raw_record = 'start,ryann001,"Nolan Ryan",1,0,1'

    expected_pitcher_update = {
        "team_side": 1,
        "pitcher_id": "ryann001",
    }

    parsed_record = parse_retrosheet_record(raw_record)

    pitcher_update = extract_pitcher_update(parsed_record)

    if pitcher_update != expected_pitcher_update:
        raise AssertionError(
            "Test Failed, pitcher update did not match expected pitcher update."

        )

    print("Test Passed, Parsed records matched.")
    print(f"Expected record: {expected_pitcher_update}")
    print(f"Parsed record:   {pitcher_update}")


def validate_relief_pitcher_update():

    parsed_record = [
        "sub",
        "chamb101",
        "Bill Champion",
        "0",
        "0",
        "1",
    ]

    expected_pitcher_update = {
        "team_side": 0,
        "pitcher_id": "chamb101",
    }

    relief_pitcher_update = extract_pitcher_update(parsed_record)

    if relief_pitcher_update != expected_pitcher_update:
        raise AssertionError(
            "Test Failed, relief pitcher update did not match expected pitcher update."

        )

    print("Test Passed, Parsed records matched.")
    print(f"Expected record: {expected_pitcher_update}")
    print(f"Parsed record:   {relief_pitcher_update}")


def validate_non_pitcher_record():

    parsed_record = [
        "start",
        "patef101",
        "Freddie Patek",
        "0",
        "1",
        "6",
    ]

    expected_pitcher_update = None

    pitcher_record = extract_pitcher_update(parsed_record)

    if pitcher_record != expected_pitcher_update:
        raise AssertionError(
            "Test Failed: Non-pitcher record detected."
        )

    print("Test Passed: Non-pitcher record was ignored.")


def validate_active_pitcher_state():

    active_pitchers = {
        0: None,
        1: None,
    }

    pitcher_update = {
        "team_side": 1,
        "pitcher_id": "ryann001",
    }

    expected_active_pitchers = {
        0: None,
        1: "ryann001",
    }

    active_pitchers = update_active_pitcher_state(
        active_pitchers,
        pitcher_update
    )

    if active_pitchers != expected_active_pitchers:
        raise AssertionError(
            "Test Failed: Active pitcher did not update."
        )

    print("Test Passed: Active pitcher updated.")
    print(f"Expected state: {expected_active_pitchers}")
    print(f"Active state:   {active_pitchers}")


def validate_active_pitcher_state_preservation():

    active_pitchers = {
        0: None,
        1: "ryann001",
    }

    pitcher_update = {
        "team_side": 0,
        "pitcher_id": "chamb101",
    }

    expected_active_pitchers = {
        0: "chamb101",
        1: "ryann001",
    }

    active_pitchers = update_active_pitcher_state(
        active_pitchers,
        pitcher_update
    )

    if active_pitchers != expected_active_pitchers:
        raise AssertionError(
            "Test Failed: Pitcher update erased existing pitcher state."
        )

    print("Test Passed: Pitcher state was preserved during update.")
    print(f"Expected state: {expected_active_pitchers}")
    print(f"Active state:   {active_pitchers}")


def validate_home_pitcher_for_visiting_play():

    active_pitchers = {
        0: "chamb101",
        1: "ryann001"
    }

    batting_team_side = "0"

    expected_pitcher = "ryann001"

    active_pitcher = get_active_pitcher_for_play(
        active_pitchers,
        batting_team_side
    )

    if active_pitcher != expected_pitcher:
        raise AssertionError(
            "Test Failed: Active pitcher did not match expected pitcher."
        )

    print("Test Passed: Active pitcher matched expected pitcher.")
    print(f"Active Pitcher:   {active_pitcher}")
    print(f"Expected Pitcher: {expected_pitcher}")


def validate_visiting_pitcher_for_home_play():

    active_pitchers = {
        0: "chamb101",
        1: "ryann001",
    }

    batting_team_side = "1"

    expected_pitcher = "chamb101"

    active_pitcher = get_active_pitcher_for_play(
        active_pitchers,
        batting_team_side
    )

    if active_pitcher != expected_pitcher:
        raise AssertionError(
            "Test Failed: Active pitcher did not match expected pitcher."
        )

    print("Test Passed: Active pitcher matched expected pitcher.")
    print(f"Active Pitcher:   {active_pitcher}")
    print(f"Expected Pitcher: {expected_pitcher}")


def validate_play_data_extraction():

    parsed_record = [
        "play",
        "1",
        "0",
        "patef101",
        "??",
        "",
        "K",
    ]

    active_pitchers = {
        0: None,
        1: "ryann001",
    }

    expected_play = {
        "inning": 1,
        "batting_team_side": 0,
        "batter_id": "patef101",
        "responsible_batter_id": "patef101",
        "count": "??",
        "pitcher_id": "ryann001",
        "event": "K",
        "hit_type": None,
        "is_strikeout": True,
        "is_plate_appearance": True,
        "is_pitcher_encounter": True,
    }

    active_play = extract_play_data(
        parsed_record,
        active_pitchers
    )

    if active_play != expected_play:
        raise AssertionError(
            "Test Failed: Active play did not match expected play."
        )

    print("Test Passed: Active play matches expected play.")
    print(f"Expected Play: {expected_play}")
    print(f"Active Play: {active_play}")


def validate_standard_strikeout_event():

    event = "K"

    expected_result = True

    strikeout_event = is_strikeout_event(event)

    if strikeout_event != expected_result:
        raise AssertionError(
            "Test Failed: Strikeout event did not match expected result."
        )

    print("Test Passed: Strikeout event matched expected result.")
    print(f"Expected Result: {expected_result}")
    print(f"Strikeout Event: {strikeout_event}")


def validate_modified_strikeout_event():

    event = "K/C"

    expected_result = True

    modified_event = is_strikeout_event(event)

    if modified_event != expected_result:
        raise AssertionError(
            "Test Failed: Modified strikeout event did not match expected result."
        )

    print("Test Passed: Strikeout event matched expected result.")
    print(f"Expected Result: {expected_result}")
    print(f"Modified Strikeout Event: {modified_event}")


def validate_non_strikeout_event():

    event = "SB2.1-3(E2/TH)"

    expected_result = False

    non_strikeout_event = is_strikeout_event(event)

    if non_strikeout_event != expected_result:
        raise AssertionError(
            "Test Failed: Non-strikeout event did not match expected result."
        )

    print("Test Passed: Strikeout event matched expected result.")
    print(f"Expected Result: {expected_result}")
    print(f"Non-Strikeout Event: {non_strikeout_event}")


def validate_non_play_data_rejection():

    parsed_record = [
        "sub",
        "chamb101",
        "Bill Champion",
        "0",
        "0",
        "1",
    ]

    active_pitchers = {
        0: "chamb101",
        1: "ryann001",
    }

    expected_result = None

    non_play_data = extract_play_data(
        parsed_record,
        active_pitchers
    )

    if non_play_data != expected_result:
        raise AssertionError(
            "Test Failed: Non-play data did not match expected result."
        )

    print("Test Passed: Non-play data matched expected result.")
    print(f"Expected Result: {expected_result}")
    print(f"Non-Play Data: {non_play_data}")


def validate_numeric_out_plate_appearance():

    event = "63/G"
    expected_result = True

    plate_appearance_result = is_plate_appearance_event(event)

    if plate_appearance_result != expected_result:
        raise AssertionError(
            "Test Failed: Event did not match expected result."
        )

    print("Test Passed: Event matched expected result.")
    print(f"Expected Event: {expected_result}")
    print(f"Event: {plate_appearance_result}")


def validate_stolen_base_not_plate_appearance():

    event = "SB2.1-3(E2/TH)"
    expected_result = False

    plate_appearance_result = is_plate_appearance_event(event)

    if plate_appearance_result != expected_result:
        raise AssertionError(
            "Test Failed: Plate appearance did not match expected results."
        )

    print("Test Passed: Plate appearance matched expected result.")
    print(f"Expected Result: {expected_result}")
    print(f"Plate Appearance: {plate_appearance_result}")


def validate_defensive_indifference_not_plate_appearance():

    event = "DI.1-2"
    expected_result = False

    plate_appearance_result = is_plate_appearance_event(event)

    if plate_appearance_result != expected_result:
        raise AssertionError(
            "Test Failed: Plate appearance did not match expected results."
        )

    print("Test Passed: Plate appearance matched expected result.")
    print(f"Expected Result: {expected_result}")
    print(f"Plate Appearance: {plate_appearance_result}")


def validate_named_plate_appearance_events():

    test_cases = {
        "K": True,
        "W": True,
        "IW": True,
        "HP": True,
        "S7": True,
        "D7/G5": True,
        "T9/F9LD": True,
        "HR/F78": True,
        "E6/G6": True,
        "FC5/G5": True,
        "C/E2": True,
        "NP": False,
        "WP.2-3": False,
        "FLE5/P5F": False,
    }

    for event, expected_result in test_cases.items():
        plate_appearance_result = is_plate_appearance_event(event)
        if plate_appearance_result != expected_result:
            raise AssertionError(
                f"Test Failed: {event} returned "
                f"{plate_appearance_result}, expected {expected_result}."
            )
    print("Test Passed: Named plate appearance events were classified correctly.")


def validate_base_running_play_extraction():

    parsed_record = [
        "play",
        "1",
        "0",
        "otisa001",
        "??",
        "",
        "SB2.1-3(E2/TH)",
    ]

    active_pitchers = {
        0: None,
        1: "ryann001",
    }

    expected_play = {
        "inning": 1,
        "batting_team_side": 0,
        "batter_id": "otisa001",
        "responsible_batter_id": "otisa001",
        "count": "??",
        "pitcher_id": "ryann001",
        "event": "SB2.1-3(E2/TH)",
        "hit_type": None,
        "is_strikeout": False,
        "is_plate_appearance": False,
        "is_pitcher_encounter": False,
    }

    base_running_play = extract_play_data(
        parsed_record,
        active_pitchers,
    )

    if base_running_play != expected_play:
        raise AssertionError(
            "Test Failed, The base running play did not match expected play."
        )

    print("Test Passed: The base running play matches the expected play.")
    print(f"Expected Play: {expected_play}")
    print(f"Base Running Play: {base_running_play}")


def validate_retrosheet_play_data_assembly():

    raw_records = [
        "id,CAL197304060",
        'start,ryann001,"Nolan Ryan",1,0,1',
        'start,patef101,"Freddie Patek",0,1,6',
        "play,1,0,patef101,??,,K",
        "play,1,0,otisa001,??,,SB2.1-3(E2/TH)",
    ]

    expected_plays = [
        {
            "inning": 1,
            "batting_team_side": 0,
            "batter_id": "patef101",
            "responsible_batter_id": "patef101",
            "count": "??",
            "pitcher_id": "ryann001",
            "event": "K",
            "hit_type": None,
            "is_strikeout": True,
            "is_plate_appearance": True,
            "is_pitcher_encounter": True,
            "game_id": "CAL197304060",
        },
        {
            "inning": 1,
            "batting_team_side": 0,
            "batter_id": "otisa001",
            "responsible_batter_id": "otisa001",
            "count": "??",
            "pitcher_id": "ryann001",
            "event": "SB2.1-3(E2/TH)",
            "hit_type": None,
            "is_strikeout": False,
            "is_plate_appearance": False,
            "is_pitcher_encounter": False,
            "game_id": "CAL197304060",
        },
    ]

    retrosheet_play_data = build_retrosheet_play_data(raw_records)

    if retrosheet_play_data != expected_plays:
        raise AssertionError(
            "Test Failed: Retrosheet play data does not match expected plays."
        )

    print("Test Passed: Retrosheet play data matches expected plays.")
    print(f"Expected Plays: {expected_plays}")
    print(f"Retrosheet Plays: {retrosheet_play_data}")


def validate_retrosheet_event_file_parsing():

    file_path = "data/raw/retrosheet/1973/1973CAL.EVA"

    expected_first_play = {
    "inning": 1,
    "batting_team_side": 0,
    "batter_id": "patef101",
    "responsible_batter_id": "patef101",
    "count": "??",
    "pitcher_id": "ryann001",
    "event": "K",
    "hit_type": None,
    "is_strikeout": True,
    "is_plate_appearance": True,
    "is_pitcher_encounter": True,
    "game_id": "CAL197304060",
}

    retrosheet_plays = parse_retrosheet_event_file(file_path)

    first_play = retrosheet_plays[0]

    if first_play != expected_first_play:
        raise AssertionError(
            "Test Failed: First play does not match expected first play."
        )

    print("Test Passed: First play matches expected first play.")
    print(f"Expected First Play: {expected_first_play}")
    print(f"First Play: {first_play}")

    print()
    print(f"Parsed play records: {len(retrosheet_plays)}")


def validate_chris_short_catcher_interference():

    # MIL197308070 - Chris Short vs. Nolan Ryan
    # Catcher interference ends the plate appearance, but it is excluded
    # from LegendsLeague's modeled batter-pitcher encounters because the
    # outcome is caused by the catcher rather than the batter or pitcher.
    event = "C/E2.1-2"

    expected_plate_appearance = True
    expected_pitcher_encounter = False

    if is_plate_appearance_event(event) != expected_plate_appearance:
        raise AssertionError(
            "Test Failed: Plate appearance event does not match expected plate appearance."
        )

    if is_pitcher_encounter_event(event) != expected_pitcher_encounter:
        raise AssertionError(
            "Test Failed: Pitcher encounter event does not match expected pitcher encounter."
        )

    print("\nChris Short catcher interference validation: ")
    print("Test Passed.")


def validate_ryan_1973_retrosheet_totals():

    directory_path = "data/raw/retrosheet/1973"

    expected_ryan_encounters = 1355
    expected_ryan_strikeouts = 383

    all_plays = parse_retrosheet_event_directory(
        directory_path
    )

    ryan_encounters = 0
    ryan_strikeouts = 0


    for play in all_plays:
        if play["pitcher_id"] == "ryann001":
            if play["is_pitcher_encounter"]:
                ryan_encounters += 1
                if play["is_strikeout"]:
                    ryan_strikeouts += 1

    if ryan_encounters != expected_ryan_encounters:
        raise AssertionError(
            "Test Failed: Ryan's Retrosheet encounters "
            "did not match his Lahman BFP."
        )

    if ryan_strikeouts != expected_ryan_strikeouts:
        raise AssertionError(
            "Test Failed: Ryan's Retrosheet strikeouts "
            "did not match his Lahman strikeouts."
        )

    print("Test Passed: Ryan's 1973 Retrosheet totals match Lahman.")
    print(f"Expected encounters: {expected_ryan_encounters}")
    print(f"Retrosheet encounters: {ryan_encounters}")
    print(f"Expected strikeouts: {expected_ryan_strikeouts}")
    print(f"Retrosheet strikeouts: {ryan_strikeouts}")


def validate_inherited_strikeout_responsibility():

    raw_records = [
        "id,TEST_GAME",
        "play,9,0,wille101,32,,NP",
        'sub, hende103,"Ellie Hendricks",0,5,11',
        "play,9,0,hende103,32,,K",
    ]

    parsed_plays = build_retrosheet_play_data(raw_records)

    strikeout_play = parsed_plays[-1]

    expected_batter_id = "hende103"

    expected_responsible_batter_id = "wille101"

    print(f"Returned strikeout play: {strikeout_play}")
    print(f"Expected responsible batter: {expected_responsible_batter_id}")

    if strikeout_play["batter_id"] != expected_batter_id:
        raise AssertionError(
            "Test Failed: The final batter's identity was not preserved."
        )

    if (
        strikeout_play["responsible_batter_id"]
        != expected_responsible_batter_id
    ):
        raise AssertionError(
            "Test Failed: Replacement batter responsibility was incorrect."
        )

    print("Test Passed: Inherited strikeout responsibility matched.")
    print(f"Final batter: {strikeout_play['batter_id']}")
    print(f"Responsible batter: {strikeout_play['responsible_batter_id']}")


def validate_replacement_batter_non_strikeout():

    raw_records = [
        "id,TEST_GAME",
        "play,9,0,wille101,32,,NP",
        'sub, hende103,"Ellie Hendricks",0,5,11',
        "play,9,0,hende103,32,,W",
    ]

    parsed_plays = build_retrosheet_play_data(raw_records)

    completed_play = parsed_plays[-1]

    expected_batter_id = "hende103"

    expected_responsible_batter_id = "hende103"

    print(f"Returned completed play: {completed_play}")
    print(f"Expected responsible batter: {expected_responsible_batter_id}")

    if completed_play["batter_id"] != expected_batter_id:
        raise AssertionError(
            "Test Failed: The final batter's identity was not preserved."
        )

    if (
        completed_play["responsible_batter_id"]
        != expected_responsible_batter_id
    ):
        raise AssertionError(
            "Test Failed: Inherited strikeout responsibility was incorrect."
        )

    print("Test Passed: Walk responsibility stayed with the replacement batter.")
    print(f"Final batter: {completed_play['batter_id']}")
    print(f"Responsible batter: {completed_play['responsible_batter_id']}")


def validate_replacement_batter_with_one_strike():

    raw_records = [
        "id,TEST_GAME",
        "play,9,0,wille101,31,,NP",
        'sub,hende103,"Ellie Hendrics",0,5,11',
        "play,9,0,hende103,32,,K",
    ]

    parsed_plays = build_retrosheet_play_data(raw_records)

    strikeout_play = parsed_plays[-1]

    expected_batter_id = "hende103"

    expected_responsible_batter_id = "hende103"

    print(f"Returned strikeout play: {strikeout_play}")
    print(f"Expected responsible batter: {expected_responsible_batter_id}")

    if strikeout_play["batter_id"] != expected_batter_id:
        raise AssertionError(
            "Test Failed: The final batter's identity was not preserved."
        )

    if (
        strikeout_play["responsible_batter_id"]
        != expected_responsible_batter_id
    ):
        raise AssertionError(
            "Test Failed: Inherited strikeout responsibility was incorrect."
        )

    print("Test Passed: Strikeout responsibility stayed with the replacement batter.")
    print(f"Final batter: {strikeout_play['batter_id']}")
    print(f"Responsible batter: {strikeout_play['responsible_batter_id']}")


def validate_batter_responsibility_reset_after_completed_appearance():

    raw_records = [
        "id,TEST_GAME",
        "play,9,0,wille101,32,,NP",
        'sub,hende103,"Ellie Hendricks",0,5,11',
        "play,9,0,hende103,32,,K",
        "play,9,0,crowt101,02,,K",
    ]

    parsed_plays = build_retrosheet_play_data(raw_records)

    strikeout_play = parsed_plays[-1]

    expected_batter_id = "crowt101"

    expected_responsible_batter_id = "crowt101"

    print(f"Returned strikeout play: {strikeout_play}")
    print(f"Expected responsible batter: {expected_responsible_batter_id}")

    if strikeout_play["batter_id"] != expected_batter_id:
        raise AssertionError(
            "Test Failed: The final batter's identity was not preserved."
        )

    if (
        strikeout_play["responsible_batter_id"]
        != expected_responsible_batter_id
    ):
        raise AssertionError(
            "Test Failed: Inherited strikeout responsibility was incorrect."
        )

    print("Test Passed: Batter responsibility reset after the completed appearance.")
    print(f"Final batter: {strikeout_play['batter_id']}")
    print(f"Responsible batter: {strikeout_play['responsible_batter_id']}")


def validate_classify_hit_event():

    expected_hit_types = {
        "S9": "single",
        "D7": "double",
        "T8": "triple",
        "HR/9": "home_run",
        "SB2": None,
        "DI": None,
        "HP": None,
    }

    for event in expected_hit_types:
        actual_hit_type = classify_hit_event(event)
        expected_hit_type = expected_hit_types[event]
        if actual_hit_type != expected_hit_type:
            raise AssertionError(
                f"{event}: expected {expected_hit_type}, got {actual_hit_type}"
            )

    print(f"Test Passed: All {len(expected_hit_types)} hit event cases matched.")



# ================================================
# MAIN
# ================================================

def main():

    print()

    validate_parse_retrosheet_record()

    print()
    print("==============================")
    print()

    validate_starting_pitcher_update()

    print()
    print("==============================")
    print()

    validate_relief_pitcher_update()

    print()
    print("==============================")
    print()

    validate_non_pitcher_record()

    print()
    print("==============================")
    print()

    validate_active_pitcher_state()

    print()
    print("==============================")
    print()

    validate_active_pitcher_state_preservation()

    print()
    print("==============================")
    print()

    validate_home_pitcher_for_visiting_play()

    print()
    print("==============================")
    print()

    validate_visiting_pitcher_for_home_play()

    print()
    print("==============================")
    print()

    validate_play_data_extraction()

    print()
    print("==============================")
    print()

    validate_standard_strikeout_event()

    print()
    print("==============================")
    print()

    validate_modified_strikeout_event()

    print()
    print("==============================")
    print()

    validate_non_strikeout_event()

    print()
    print("==============================")
    print()

    validate_non_play_data_rejection()

    print()
    print("==============================")
    print()

    validate_numeric_out_plate_appearance()

    print()
    print("==============================")
    print()

    validate_stolen_base_not_plate_appearance()

    print()
    print("==============================")
    print()

    validate_defensive_indifference_not_plate_appearance()

    print()
    print("==============================")
    print()

    validate_named_plate_appearance_events()

    print()
    print("==============================")
    print()

    validate_base_running_play_extraction()

    print()
    print("==============================")
    print()

    validate_retrosheet_play_data_assembly()

    print()
    print("==============================")
    print()

    validate_retrosheet_event_file_parsing()

    print()
    print("==============================")
    print()

    validate_chris_short_catcher_interference()

    print()
    print("==============================")
    print()

    validate_ryan_1973_retrosheet_totals()

    print()
    print("==============================")
    print()

    validate_inherited_strikeout_responsibility()

    print()
    print("==============================")
    print()

    validate_replacement_batter_non_strikeout()

    print()
    print("==============================")
    print()

    validate_replacement_batter_with_one_strike()

    print()
    print("==============================")
    print()

    validate_batter_responsibility_reset_after_completed_appearance()

    print()
    print("==============================")
    print()

    validate_classify_hit_event()

    print()






if __name__ == "__main__":
    main()
