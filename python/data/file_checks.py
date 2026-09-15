from pathlib import Path

LAHMAN_DATA_DIR = Path(
    "data/raw/lahman/lahman_1871-2025_csv"
)


REQUIRED_FILES = [
    "People.csv",
    "Batting.csv",
    "Pitching.csv",
    "Teams.csv",
]


def check_required_files():
    
    for file_name in REQUIRED_FILES:
        file_path = LAHMAN_DATA_DIR / file_name
        if not file_path.exists():
            print(f"Missing required file: {file_name}")
        else:
            print(f"Found required file: {file_name}")