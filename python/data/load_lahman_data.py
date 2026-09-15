import pandas as pd
from python.data.file_checks import (
    REQUIRED_FILES,
    LAHMAN_DATA_DIR,
)


def load_required_files():
    loaded_files = {}

    for file_name in REQUIRED_FILES:
        file_path = LAHMAN_DATA_DIR / file_name

        if not file_path.exists():
            print(f"Missing required file: {file_name}")
            continue

        print(f"Found required file: {file_name}")

        data = pd.read_csv(file_path)

        loaded_files[file_name] = data

        print(f"Loaded successfully: {file_name}")
        print(f"{file_name}: {data.shape}")
        print(data.columns.tolist())
        print(data.isna().sum())

        print("\n--------------------------------\n")

    return loaded_files