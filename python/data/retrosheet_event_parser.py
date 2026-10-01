"""
Project LegendsLeague
Retrosheet Event Parser

Purpose:
    Parse Retrosheet event files into structured play data that can be used
    for historical pitcher-batter matchup analysis.

Responsibilities:
    - Parse raw Retrosheet CSV-style records.
    - Track starting and relief pitcher changes.
    - Maintain active pitcher state for both teams.
    - Identify the pitcher responsible for each play.
    - Extract structured play records.
    - Classify strikeouts, plate appearances, pitcher encounters, and hit types.
    - Track game identifiers across event files.
    - Preserve batter responsibility during mid-count substitutions.
    - Reset plate appearance state after completed appearances.
    - Parse individual Retrosheet event files.
    - Parse directories containing American League and National League event files.

Historical Handling:
    - Catcher interference is treated as a plate appearance but excluded
      from modeled pitcher encounters.
    - Mid-count batter substitutions preserve strikeout responsibility
      according to the active count state.

Design Principle:
    Raw Retrosheet event data must be transformed into explicit,
    state-aware play records before it can support reliable matchup
    aggregation, reconciliation, or simulation.

Data Source:
    Retrosheet event files
"""

# ================================================
# IMPORTS
# ================================================
import csv

from pathlib import Path


# ================================================
# FUNCTIONS
# ================================================

def parse_retrosheet_record(line):

    parsed_records = csv.reader([line])

    parsed_record = next(parsed_records)

    return parsed_record


def extract_pitcher_update(parsed_record):

    if parsed_record[0] not in ("start", "sub"):
        return None

    if parsed_record[5] != "1":
        return None

    team_side = int(parsed_record[3])
    pitcher_id = parsed_record[1]

    pitcher_update = {
        "team_side": team_side,
        "pitcher_id": pitcher_id,
    }

    return pitcher_update


def update_active_pitcher_state(active_pitchers, pitcher_update):

    team_side = pitcher_update["team_side"]
    pitcher_id = pitcher_update["pitcher_id"]

    active_pitchers[team_side] = pitcher_id

    return active_pitchers


def get_active_pitcher_for_play(active_pitchers, batting_team_side):

    pitching_team_side = 1 - int(batting_team_side)

    active_pitcher = active_pitchers[pitching_team_side]

    return active_pitcher


def extract_play_data(parsed_record, active_pitchers):

    if parsed_record[0] != "play":
        return None

    inning = int(parsed_record[1])
    batting_team_side = int(parsed_record[2])
    batter_id = parsed_record[3]
    count = parsed_record[4]
    event = parsed_record[6]

    hit_type = classify_hit_event(event)

    is_pitcher_encounter = is_pitcher_encounter_event(event)

    is_strikeout = is_strikeout_event(event)

    is_plate_appearance = is_plate_appearance_event(event)

    pitcher_id = get_active_pitcher_for_play(
        active_pitchers,
        batting_team_side
    )

    play = {
        "inning": inning,
        "batting_team_side": batting_team_side,
        "batter_id": batter_id,
        "responsible_batter_id": batter_id,
        "count": count,
        "pitcher_id": pitcher_id,
        "event": event,
        "hit_type": hit_type,
        "is_strikeout": is_strikeout,
        "is_plate_appearance": is_plate_appearance,
        "is_pitcher_encounter": is_pitcher_encounter,
    }

    return play


def is_strikeout_event(event):

    if event.startswith("K"):
        return True

    return False


def is_plate_appearance_event(event):

    if event == "":
        return False

    if event == "NP":
        return False

    non_plate_appearance_prefixes = (
        "BK",   # Balk
        "CS",   # Caught stealing
        "DI",   # Defensive indifference
        "OA",   # Other advance
        "PB",   # Passed ball
        "PO",   # Pickoff
        "SB",   # Stolen base
        "WP",   # Wild pitch
        "FLE",  # Error on a foul fly; batter continues
    )

    if event.startswith(non_plate_appearance_prefixes):
        return False

    if event[0].isdigit():
        return True

    plate_appearance_prefixes = (
        "K",    # Strikeout
        "W",    # Walk
        "I",    # Intentional Walk: I or IW
        "H",    # Home run or hit by pitch
        "S",    # Single
        "D",    # Doble or ground-rule double
        "T",    # Triple
        "E",    # Batter reaches on an error
        "FC",   # Fielder's Choice
        "C/E",  # Catcher or fielder interference
    )

    if event.startswith(plate_appearance_prefixes):
        return True

    return False


def is_pitcher_encounter_event(event):

    # Exclude interference from our modeled pitcher encounters.
    # This reconciles Ryan's 1973 encounter total with Lahman BFP.
    # Do not assume this resolves every historical PA/BFP discrepancy.
    if event.startswith("C/E"):
        return False

    return is_plate_appearance_event(event)


def build_retrosheet_play_data(raw_records):

    parsed_plays = []

    active_pitchers = {
        0: None,
        1: None,
    }

    current_game_id = None
    active_plate_appearance = None

    for raw_record in raw_records:

        parsed_record = parse_retrosheet_record(raw_record)

        record_type = parsed_record[0]

        if record_type == "id":

            current_game_id = parsed_record[1]

            active_plate_appearance = None

            active_pitchers = {
                0: None,
                1: None,
            }
        elif record_type in ("start", "sub"):

            pitcher_update = extract_pitcher_update(parsed_record)

            if pitcher_update is not None:
                active_pitchers = update_active_pitcher_state(
                    active_pitchers,
                    pitcher_update,
                )
        elif record_type == "play":

            play = extract_play_data(
                parsed_record,
                active_pitchers,
            )

            if (
                active_plate_appearance is None
                or active_plate_appearance["inning"] != play["inning"]
                or active_plate_appearance["batting_team_side"]
                != play["batting_team_side"]
            ):
                active_plate_appearance = {
                    "inning": play["inning"],
                    "batting_team_side": play["batting_team_side"],
                    "batter_id": play["batter_id"],
                    "count": play["count"],
                    "strikeout_responsible_batter_id": None,
                }

            elif active_plate_appearance["batter_id"] != play["batter_id"]:
                previous_count = active_plate_appearance["count"]

                if (
                    previous_count in ("02", "12", "22", "32")
                    and active_plate_appearance[
                        "strikeout_responsible_batter_id"
                    ] is None
                ):
                    active_plate_appearance[
                        "strikeout_responsible_batter_id"
                    ] = active_plate_appearance["batter_id"]

            if (
                play["is_strikeout"]
                and active_plate_appearance[
                    "strikeout_responsible_batter_id"
                ] is not None
            ):

                play["responsible_batter_id"] = active_plate_appearance[
                    "strikeout_responsible_batter_id"
                ]

            play["game_id"] = current_game_id

            active_plate_appearance["batter_id"] = play["batter_id"]
            active_plate_appearance["count"] = play["count"]

            parsed_plays.append(play)

            if play["is_plate_appearance"]:
                active_plate_appearance = None

    return parsed_plays


def parse_retrosheet_event_file(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as event_file:

        parsed_plays = build_retrosheet_play_data(event_file)

    return parsed_plays


def parse_retrosheet_event_directory(
    directory_path,
    league=None,
):

    event_directory = Path(directory_path)

    if league == "AL":
        event_files = sorted(
            list(event_directory.glob("*.EVA"))
        )
    elif league == "NL":
        event_files = sorted(
            list(event_directory.glob("*.EVN"))
        )
    else:
        event_files = sorted(
            list(event_directory.glob("*.EVA"))
            + list(event_directory.glob("*.EVN"))
        )

    all_plays = []

    for event_file in event_files:
        file_plays = parse_retrosheet_event_file(event_file)
        all_plays.extend(file_plays)

    return all_plays


def classify_hit_event(event):

    if event.startswith("HR"):
        return "home_run"
    elif event.startswith("SB"):
        return None
    elif event.startswith("S"):
        return "single"
    elif event.startswith("DI"):
        return None
    elif event.startswith("D"):
        return "double"
    elif event.startswith("T"):
        return "triple"
    else:
        return None
