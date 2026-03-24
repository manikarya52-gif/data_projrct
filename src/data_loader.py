"""
data_loader.py
--------------
Responsible for loading the dataset from a CSV file and performing
an initial inspection (shape, dtypes, first rows, missing-value counts).
"""

import os
import pandas as pd


# Default path to the sample dataset (relative to the project root)
DEFAULT_DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "sample_data.csv"
)


def load_data(filepath: str = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame.

    Parameters
    ----------
    filepath : str
        Path to the CSV file.  Defaults to the bundled sample dataset.

    Returns
    -------
    pd.DataFrame
        Raw (uncleaned) DataFrame.
    """
    filepath = os.path.abspath(filepath)
    print(f"[data_loader] Loading data from: {filepath}")
    df = pd.read_csv(filepath)
    print(f"[data_loader] Loaded {len(df)} rows and {len(df.columns)} columns.")
    return df


def inspect_data(df: pd.DataFrame) -> None:
    """Print a concise summary of the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to inspect.
    """
    print("\n--- Data Inspection ---")
    print(f"Shape        : {df.shape}")
    print(f"\nColumn dtypes:\n{df.dtypes}")
    print(f"\nFirst 5 rows:\n{df.head()}")
    print(f"\nMissing values per column:\n{df.isnull().sum()}")
    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    print("--- End of Inspection ---\n")
