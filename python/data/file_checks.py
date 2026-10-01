"""
Project LegendsLeague
Required File Checks

Purpose:
    Verify that the required Lahman source files are present before
    downstream data loading or analysis begins.

Responsibilities:
    - Define the expected Lahman raw-data directory.
    - Define the required source files used by LegendsLeague.
    - Check whether each required file exists.
    - Report missing or available source files for development and QA.

Required Files:
    - People.csv
    - Batting.csv
    - Pitching.csv
    - Teams.csv
"""

# =====================================
# IMPORTS
# =====================================

from pathlib import Path


# =====================================
# CONFIGURATION
# =====================================

LAHMAN_DATA_DIR = Path(
    "data/raw/lahman/lahman_1871-2025_csv"
)


REQUIRED_FILES = [
    "People.csv",
    "Batting.csv",
    "Pitching.csv",
    "Teams.csv",
]


# =====================================
# FUNCTION
# =====================================

def check_required_files():

    for file_name in REQUIRED_FILES:
        file_path = LAHMAN_DATA_DIR / file_name
        if not file_path.exists():
            print(f"Missing required file: {file_name}")
        else:
            print(f"Found required file: {file_name}")
