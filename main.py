"""
main.py
-------
Entry point for the Data Analytics project.

Run this script to execute the full pipeline:
  1. Load the sample dataset.
  2. Inspect the raw data.
  3. Clean the data (remove duplicates, handle missing values).
  4. Perform exploratory data analysis (EDA).
  5. Generate and save all visualizations.
  6. Print a final summary of key insights.

Usage
-----
    python main.py
    python main.py --data path/to/your_data.csv
"""

import argparse
import os
import sys

# Ensure the project root is on the Python path when run directly
sys.path.insert(0, os.path.dirname(__file__))

from src.data_loader import load_data, inspect_data
from src.data_cleaning import clean_data
from src.eda import run_eda
from src.visualization import generate_all_visualizations


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the Data Analytics pipeline.")
    parser.add_argument(
        "--data",
        default=None,
        help="Path to a custom CSV data file. Defaults to data/sample_data.csv.",
    )
    return parser.parse_args()


def print_insights(eda_results: dict) -> None:
    """Print a human-readable summary of the most important insights.

    Parameters
    ----------
    eda_results : dict
        Dictionary returned by ``eda.run_eda``.
    """
    print("=" * 60)
    print("           KEY INSIGHTS FROM THE ANALYSIS")
    print("=" * 60)

    # Best-selling category
    by_cat = eda_results["by_category"]
    if not by_cat.empty:
        best_cat = by_cat["total_sales"].idxmax()
        best_cat_sales = by_cat.loc[best_cat, "total_sales"]
        print(f"  Top category by sales : {best_cat} (${best_cat_sales:,.2f})")

    # Best region
    by_reg = eda_results["by_region"]
    if not by_reg.empty:
        best_reg = by_reg["total_sales"].idxmax()
        best_reg_sales = by_reg.loc[best_reg, "total_sales"]
        print(f"  Top region by sales   : {best_reg} (${best_reg_sales:,.2f})")

    # Best product
    top_prods = eda_results["top_products"]
    if not top_prods.empty:
        best_prod = top_prods.index[0]
        best_prod_sales = top_prods.iloc[0]["total_sales"]
        print(f"  Best-selling product  : {best_prod} (${best_prod_sales:,.2f})")

    # Overall stats
    stats = eda_results["stats"]
    if "sales" in stats.columns:
        print(f"  Average order sales   : ${stats.loc['mean', 'sales']:,.2f}")
        print(f"  Highest single sale   : ${stats.loc['max', 'sales']:,.2f}")

    print("=" * 60)


def main() -> None:
    """Execute the full data analytics pipeline."""
    args = parse_args()

    # ── Step 1: Load ──────────────────────────────────────────────────────────
    kwargs = {"filepath": args.data} if args.data else {}
    df_raw = load_data(**kwargs)

    # ── Step 2: Inspect ───────────────────────────────────────────────────────
    inspect_data(df_raw)

    # ── Step 3: Clean ─────────────────────────────────────────────────────────
    df_clean = clean_data(df_raw)

    # ── Step 4: EDA ───────────────────────────────────────────────────────────
    eda_results = run_eda(df_clean)

    # ── Step 5: Visualize ─────────────────────────────────────────────────────
    saved_paths = generate_all_visualizations(df_clean, eda_results)
    print("Saved plots:")
    for p in saved_paths:
        print(f"  {p}")

    # ── Step 6: Insights ──────────────────────────────────────────────────────
    print_insights(eda_results)


if __name__ == "__main__":
    main()
