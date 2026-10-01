"""
Project LegendsLeague
Lahman Data Loader

Purpose:
    Load the required Lahman source files used by LegendsLeague.

Responsibilities:
    - Iterate through the required Lahman source files.
    - Confirm each file exists before loading.
    - Load available CSV files into pandas DataFrames.
    - Return loaded datasets in a filename-keyed dictionary.
    - Optionally print file-level loading and inspection details.

Design Principle:
    Data loading should remain separate from downstream calculation and
    normalization logic so source access can be reused consistently.
"""

# =====================================
# IMPORTS
# =====================================
import pandas as pd

from python.data.file_checks import (
    REQUIRED_FILES,
    LAHMAN_DATA_DIR,
)


# =====================================
# FUNCTION
# =====================================

def load_required_files(
    verbose=True,
):

    loaded_files = {}

    for file_name in REQUIRED_FILES:
        file_path = LAHMAN_DATA_DIR / file_name

        if not file_path.exists():
            print(f"Missing required file: {file_name}")
            continue

        if verbose:
            print(f"Found required file: {file_name}")

        data = pd.read_csv(file_path)

        loaded_files[file_name] = data

        if verbose:
            print(f"Loaded successfully: {file_name}")
            print(f"{file_name}: {data.shape}")
            print(data.columns.tolist())
            print(data.isna().sum())

            print("\n--------------------------------\n")

    return loaded_files
