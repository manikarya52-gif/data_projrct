"""
eda.py
------
Exploratory Data Analysis (EDA) functions.

Computes and prints:
  - Basic descriptive statistics (mean, median, std, min, max)
  - Sales and profit aggregations by category and by region
  - Monthly revenue trends
  - Correlation matrix of numeric columns
  - Top-performing products
"""

import pandas as pd


def basic_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Print and return descriptive statistics for numeric columns.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned DataFrame.

    Returns
    -------
    pd.DataFrame
        Descriptive statistics table.
    """
    print("\n--- Basic Descriptive Statistics ---")
    stats = df.describe().round(2)
    print(stats)
    print()
    return stats


def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate total sales and average profit by product category.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned DataFrame.

    Returns
    -------
    pd.DataFrame
        Aggregated sales/profit per category.
    """
    agg = (
        df.groupby("category")
        .agg(
            total_sales=("sales", "sum"),
            avg_profit=("profit", "mean"),
            order_count=("order_id", "count"),
        )
        .round(2)
        .sort_values("total_sales", ascending=False)
    )
    print("--- Sales by Category ---")
    print(agg)
    print()
    return agg


def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate total sales and order count by region.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned DataFrame.

    Returns
    -------
    pd.DataFrame
        Aggregated sales per region.
    """
    agg = (
        df.groupby("region")
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            order_count=("order_id", "count"),
        )
        .round(2)
        .sort_values("total_sales", ascending=False)
    )
    print("--- Sales by Region ---")
    print(agg)
    print()
    return agg


def monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """Compute monthly total sales and profit trends.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned DataFrame (must contain 'year' and 'month' columns).

    Returns
    -------
    pd.DataFrame
        Monthly aggregation sorted by year and month.
    """
    if "year" not in df.columns or "month" not in df.columns:
        print("[eda] Warning: derived date columns missing – skipping monthly trends.")
        return pd.DataFrame()

    agg = (
        df.groupby(["year", "month", "month_label"])
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
        )
        .round(2)
        .reset_index()
        .sort_values(["year", "month"])
    )
    print("--- Monthly Sales Trends ---")
    print(agg.to_string(index=False))
    print()
    return agg


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Compute the Pearson correlation matrix for numeric columns.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned DataFrame.

    Returns
    -------
    pd.DataFrame
        Correlation matrix.
    """
    numeric_df = df.select_dtypes(include="number")
    corr = numeric_df.corr().round(3)
    print("--- Correlation Matrix ---")
    print(corr)
    print()
    return corr


def top_products(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Identify the top-N products by total sales.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned DataFrame.
    n : int
        Number of top products to return.

    Returns
    -------
    pd.DataFrame
        Top-N products sorted by total sales descending.
    """
    agg = (
        df.groupby("product")
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            units_sold=("quantity", "sum"),
        )
        .round(2)
        .sort_values("total_sales", ascending=False)
        .head(n)
    )
    print(f"--- Top {n} Products by Sales ---")
    print(agg)
    print()
    return agg


def run_eda(df: pd.DataFrame) -> dict:
    """Execute the full EDA pipeline and return results as a dictionary.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned DataFrame.

    Returns
    -------
    dict
        Dictionary with keys: 'stats', 'by_category', 'by_region',
        'monthly', 'correlation', 'top_products'.
    """
    print("\n=== Starting Exploratory Data Analysis ===")
    results = {
        "stats": basic_statistics(df),
        "by_category": sales_by_category(df),
        "by_region": sales_by_region(df),
        "monthly": monthly_trends(df),
        "correlation": correlation_matrix(df),
        "top_products": top_products(df),
    }
    print("=== EDA Complete ===\n")
    return results
