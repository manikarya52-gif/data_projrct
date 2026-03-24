"""
visualization.py
----------------
Generates and saves the following plots:
  1. Bar chart  – Total sales by category
  2. Line plot  – Monthly sales trend
  3. Histogram  – Distribution of sales amounts
  4. Heatmap    – Correlation between numeric variables
  5. Bar chart  – Total sales by region

All figures are saved to the ``outputs/`` directory in the project root.
"""

import os

import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend (safe for scripts & CI)
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd

# ── Styling ──────────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
FIGURE_SIZE = (10, 6)
DPI = 120

# ── Output directory (relative to project root) ───────────────────────────────
_HERE = os.path.dirname(__file__)
OUTPUT_DIR = os.path.abspath(os.path.join(_HERE, "..", "outputs"))


def _ensure_output_dir() -> None:
    """Create the outputs directory if it does not already exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def _save(fig: plt.Figure, filename: str) -> str:
    """Save *fig* to the outputs directory and return the full path."""
    _ensure_output_dir()
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, bbox_inches="tight", dpi=DPI)
    plt.close(fig)
    print(f"[visualization] Saved → {path}")
    return path


# ── 1. Bar chart: Sales by Category ──────────────────────────────────────────

def plot_sales_by_category(by_category: pd.DataFrame) -> str:
    """Bar chart of total sales per product category.

    Parameters
    ----------
    by_category : pd.DataFrame
        Aggregated DataFrame with index=category, column 'total_sales'.

    Returns
    -------
    str
        Path to the saved figure.
    """
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)

    colors = sns.color_palette("muted", len(by_category))
    bars = ax.bar(by_category.index, by_category["total_sales"], color=colors)

    # Annotate each bar with its value
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 50,
            f"${height:,.0f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    ax.set_title("Total Sales by Category", fontsize=14, fontweight="bold")
    ax.set_xlabel("Category", fontsize=11)
    ax.set_ylabel("Total Sales ($)", fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    fig.tight_layout()

    return _save(fig, "01_sales_by_category.png")


# ── 2. Line plot: Monthly Sales Trend ────────────────────────────────────────

def plot_monthly_trend(monthly: pd.DataFrame) -> str:
    """Line plot of monthly total sales over time.

    Parameters
    ----------
    monthly : pd.DataFrame
        DataFrame with columns 'month_label', 'total_sales', 'total_profit'.

    Returns
    -------
    str
        Path to the saved figure.
    """
    if monthly.empty:
        print("[visualization] Skipping monthly trend – no data available.")
        return ""

    fig, ax = plt.subplots(figsize=FIGURE_SIZE)

    # Build a readable x-axis label: "Jan 2023", "Feb 2023", …
    monthly = monthly.copy()
    monthly["period"] = monthly["month_label"] + " " + monthly["year"].astype(str)

    ax.plot(
        monthly["period"],
        monthly["total_sales"],
        marker="o",
        linewidth=2,
        label="Total Sales",
        color="#2196F3",
    )
    ax.plot(
        monthly["period"],
        monthly["total_profit"],
        marker="s",
        linewidth=2,
        linestyle="--",
        label="Total Profit",
        color="#4CAF50",
    )

    ax.set_title("Monthly Sales & Profit Trend", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month", fontsize=11)
    ax.set_ylabel("Amount ($)", fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.legend(fontsize=10)
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()

    return _save(fig, "02_monthly_trend.png")


# ── 3. Histogram: Sales Distribution ─────────────────────────────────────────

def plot_sales_histogram(df: pd.DataFrame) -> str:
    """Histogram of the 'sales' column showing its distribution.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned DataFrame.

    Returns
    -------
    str
        Path to the saved figure.
    """
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)

    sns.histplot(
        data=df,
        x="sales",
        bins=30,
        kde=True,          # Overlay a kernel density estimate curve
        color="#5C6BC0",
        ax=ax,
    )

    # Vertical lines for mean and median
    mean_val = df["sales"].mean()
    median_val = df["sales"].median()
    ax.axvline(mean_val, color="red", linestyle="--", linewidth=1.5, label=f"Mean: ${mean_val:,.2f}")
    ax.axvline(median_val, color="orange", linestyle="-.", linewidth=1.5, label=f"Median: ${median_val:,.2f}")

    ax.set_title("Distribution of Sales Amounts", fontsize=14, fontweight="bold")
    ax.set_xlabel("Sales ($)", fontsize=11)
    ax.set_ylabel("Frequency", fontsize=11)
    ax.legend(fontsize=10)
    fig.tight_layout()

    return _save(fig, "03_sales_histogram.png")


# ── 4. Heatmap: Correlation Matrix ───────────────────────────────────────────

def plot_correlation_heatmap(corr: pd.DataFrame) -> str:
    """Heatmap of the Pearson correlation matrix.

    Parameters
    ----------
    corr : pd.DataFrame
        Correlation matrix (square DataFrame).

    Returns
    -------
    str
        Path to the saved figure.
    """
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)

    sns.heatmap(
        corr,
        annot=True,          # Print correlation coefficients in each cell
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        ax=ax,
    )

    ax.set_title("Correlation Heatmap (Numeric Variables)", fontsize=14, fontweight="bold")
    fig.tight_layout()

    return _save(fig, "04_correlation_heatmap.png")


# ── 5. Bar chart: Sales by Region ────────────────────────────────────────────

def plot_sales_by_region(by_region: pd.DataFrame) -> str:
    """Horizontal bar chart of total sales per region.

    Parameters
    ----------
    by_region : pd.DataFrame
        Aggregated DataFrame with index=region, column 'total_sales'.

    Returns
    -------
    str
        Path to the saved figure.
    """
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)

    colors = sns.color_palette("pastel", len(by_region))
    bars = ax.barh(by_region.index, by_region["total_sales"], color=colors)

    # Annotate each bar with its value
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 50,
            bar.get_y() + bar.get_height() / 2.0,
            f"${width:,.0f}",
            va="center",
            fontsize=9,
        )

    ax.set_title("Total Sales by Region", fontsize=14, fontweight="bold")
    ax.set_xlabel("Total Sales ($)", fontsize=11)
    ax.set_ylabel("Region", fontsize=11)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    fig.tight_layout()

    return _save(fig, "05_sales_by_region.png")


# ── Master function ───────────────────────────────────────────────────────────

def generate_all_visualizations(
    df: pd.DataFrame,
    eda_results: dict,
) -> list:
    """Generate and save all five visualizations.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned DataFrame.
    eda_results : dict
        Dictionary returned by ``eda.run_eda``.

    Returns
    -------
    list
        List of file paths for the saved plots.
    """
    print("\n=== Generating Visualizations ===")
    paths = [
        plot_sales_by_category(eda_results["by_category"]),
        plot_monthly_trend(eda_results["monthly"]),
        plot_sales_histogram(df),
        plot_correlation_heatmap(eda_results["correlation"]),
        plot_sales_by_region(eda_results["by_region"]),
    ]
    print("=== All Visualizations Saved ===\n")
    return [p for p in paths if p]  # Filter out empty strings
