"""
Project LegendsLeague
Player ID Mapping

Purpose:
    Build a reliable mapping between Retrosheet player IDs and Lahman
    player IDs for players required by LegendsLeague analysis.

Responsibilities:
    - Read Retrosheet and Lahman identifiers from the Lahman People dataset.
    - Include only Retrosheet IDs required by the current analysis.
    - Ignore records without Retrosheet identifiers.
    - Detect ambiguous Retrosheet IDs that map to more than one Lahman player.
    - Return a Retrosheet-to-Lahman ID dictionary for downstream matchup logic.

Design Principle:
    Player identity must be resolved explicitly and unambiguously before
    Retrosheet event data is joined with Lahman season statistics.
"""

# =============================================
# IMPORTS
# =============================================

import pandas as pd


# =============================================
# FUNCTION
# =============================================

def build_retrosheet_to_lahman_id_mapping(
    people_data,
    required_retrosheet_ids,
):

    player_id_mapping = {}

    for _, player_record in people_data.iterrows():
        retro_id = player_record["retroID"]
        lahman_player_id = player_record["playerID"]

        if (
            pd.notna(retro_id)
            and retro_id in required_retrosheet_ids
        ):
            if retro_id in player_id_mapping:
                existing_lahman_player_id = player_id_mapping[retro_id]
                raise ValueError(
                    f"Ambiguous Retrosheet ID '{retro_id}' maps to both "
                    f"'{existing_lahman_player_id}' and "
                    f"'{lahman_player_id}'."
                )

            player_id_mapping[retro_id] = lahman_player_id

    return player_id_mapping
