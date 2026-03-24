"""
data_cleaning.py
----------------
Cleans the raw DataFrame by:
  1. Dropping exact duplicate rows.
  2. Parsing the 'date' column to datetime.
  3. Filling or dropping missing values with sensible defaults.
  4. Ensuring numeric columns have the correct dtype.
  5. Adding derived helper columns (year, month, month_label).
"""

import pandas as pd


# Numeric columns that must be present in the dataset
NUMERIC_COLS = ["quantity", "unit_price", "sales", "discount", "profit"]


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove exact duplicate rows and report how many were removed.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with duplicate rows removed.
    """
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    print(f"[data_cleaning] Removed {removed} duplicate row(s). Remaining: {len(df)}")
    return df


def parse_dates(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """Convert the date column from string to pandas datetime.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    date_col : str
        Name of the column that contains date strings.

    Returns
    -------
    pd.DataFrame
        DataFrame with the date column parsed.
    """
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        print(f"[data_cleaning] '{date_col}' column parsed to datetime.")
    else:
        print(f"[data_cleaning] Warning: '{date_col}' column not found.")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values in each column.

    Strategy
    --------
    - Numeric columns : fill with the column median.
    - String/object columns : fill with 'Unknown'.
    - Rows still missing after filling are dropped.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with missing values addressed.
    """
    print(f"[data_cleaning] Missing values before cleaning:\n{df.isnull().sum()}\n")

    # Fill numeric columns with their median value
    for col in NUMERIC_COLS:
        if col in df.columns:
            median_val = df[col].median()
            missing_count = df[col].isnull().sum()
            if missing_count:
                df[col] = df[col].fillna(median_val)
                print(
                    f"[data_cleaning]  '{col}': filled {missing_count} NaN(s) "
                    f"with median={median_val:.2f}"
                )

    # Fill categorical/text columns with 'Unknown'
    for col in df.select_dtypes(include="object").columns:
        missing_count = df[col].isnull().sum()
        if missing_count:
            df[col] = df[col].fillna("Unknown")
            print(
                f"[data_cleaning]  '{col}': filled {missing_count} NaN(s) with 'Unknown'"
            )

    # Drop any remaining rows that still have missing values
    before = len(df)
    df = df.dropna()
    dropped = before - len(df)
    if dropped:
        print(f"[data_cleaning] Dropped {dropped} row(s) still containing NaN.")

    print(f"[data_cleaning] Missing values after cleaning:\n{df.isnull().sum()}\n")
    return df


def add_derived_columns(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """Add helper columns derived from existing data.

    Added columns
    -------------
    - year        : integer year extracted from the date column.
    - month       : integer month (1-12).
    - month_label : abbreviated month name (e.g. 'Jan', 'Feb').

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame (date column must already be datetime).
    date_col : str
        Name of the datetime column.

    Returns
    -------
    pd.DataFrame
        DataFrame with derived columns appended.
    """
    if date_col in df.columns and pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df["year"] = df[date_col].dt.year
        df["month"] = df[date_col].dt.month
        df["month_label"] = df[date_col].dt.strftime("%b")
        print("[data_cleaning] Derived columns (year, month, month_label) added.")
    else:
        print(
            f"[data_cleaning] Warning: cannot derive date columns from '{date_col}'."
        )
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Run the full cleaning pipeline.

    Steps
    -----
    1. Drop duplicate rows.
    2. Parse the date column.
    3. Handle missing values.
    4. Add derived columns.

    Parameters
    ----------
    df : pd.DataFrame
        Raw DataFrame returned by ``data_loader.load_data``.

    Returns
    -------
    pd.DataFrame
        Fully cleaned DataFrame ready for analysis.
    """
    print("\n=== Starting Data Cleaning Pipeline ===")
    df = drop_duplicates(df)
    df = parse_dates(df)
    df = handle_missing_values(df)
    df = add_derived_columns(df)
    # Reset the index so it is contiguous after row removal
    df = df.reset_index(drop=True)
    print(f"=== Data Cleaning Complete – {len(df)} rows ready for analysis ===\n")
    return df
