"""
visualize.py

Visualization functions for the Olist e-commerce project.

Seaborn creates the charts.
Matplotlib is used only for figure size, axis range, labels, annotations,
date formatting, and saving files.

The analysis data is not filtered to remove outliers. When a chart needs a
smaller visible range, only the graph settings are changed.
"""

import os
from typing import Dict, Tuple

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter


# Use one simple style for every chart.
sns.set_theme(style="whitegrid")
MAIN_COLOR = "#4C72B0"
ACCENT_COLOR = "#C44E52"

# Q2 uses the full monthly result, but only this date range is displayed.
Q2_DISPLAY_START = pd.Timestamp("2016-10-01")
Q2_DISPLAY_END = pd.Timestamp("2018-08-01")


def _compact_number(value, _=None) -> str:
    """Change a large number such as 1,500,000 to 1.5M."""
    value = float(value)

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.0f}k"
    return f"{value:,.0f}"


def _compact_currency(value: float) -> str:
    """Return a short BRL value label such as R$ 850k or R$ 1.2M."""
    return f"R$ {_compact_number(value)}"


def _iqr_bounds(values: pd.Series) -> Tuple[float, float]:
    """
    Calculate the standard 1.5-IQR lower and upper outlier limits.

    The function only calculates limits. It does not remove any values.
    """
    clean_values = pd.to_numeric(values, errors="coerce").dropna()

    if clean_values.empty:
        return 0.0, 0.0

    q1 = clean_values.quantile(0.25)
    q3 = clean_values.quantile(0.75)
    iqr = q3 - q1

    return q1 - (1.5 * iqr), q3 + (1.5 * iqr)


def plot_revenue_by_category(
    result: pd.DataFrame,
    top_n: int,
) -> plt.Figure:
    """
    Q1: Show the Top N product categories by total item sales.

    The analysis result contains every category. Top N is only a display
    choice for this graph.

    Parameters:
        result: DataFrame with category and revenue.
        top_n: Number of categories to show in the chart.

    Returns:
        Matplotlib Figure containing a Seaborn bar chart.
    """
    display_data = (
        result.nlargest(top_n, "revenue")
        .sort_values("revenue", ascending=False)
        .copy()
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.barplot(
        data=display_data,
        x="revenue",
        y="category",
        order=display_data["category"],
        color=MAIN_COLOR,
        errorbar=None,
        ax=ax,
    )

    ax.set_title(f"Top {len(display_data)} Product Categories by Total Item Sales")
    ax.set_xlabel("Total Item Sales (BRL)")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(FuncFormatter(_compact_number))

    # Leave a small space for the value labels.
    max_revenue = display_data["revenue"].max()
    ax.set_xlim(0, max_revenue * 1.10)

    # Matplotlib adds exact values to the Seaborn bars.
    for container in ax.containers:
        labels = [f"R$ {bar.get_width():,.0f}" for bar in container]
        ax.bar_label(container, labels=labels, padding=4, fontsize=9)

    fig.tight_layout()
    return fig


def plot_monthly_revenue(
    result: pd.DataFrame,
    start_date: pd.Timestamp = Q2_DISPLAY_START,
    end_date: pd.Timestamp = Q2_DISPLAY_END,
) -> plt.Figure:
    """
    Q2: Show monthly item sales over time.

    Seaborn receives the full monthly result. Matplotlib only limits the
    visible x-axis to January 2017 through September 2018.

    Parameters:
        result: DataFrame with month and revenue.
        start_date: First date shown on the x-axis.
        end_date: Last date shown on the x-axis.

    Returns:
        Matplotlib Figure containing a Seaborn line chart.
    """
    fig, ax = plt.subplots(figsize=(14, 6))

    # The full result is passed to Seaborn. No monthly rows are removed.
    sns.lineplot(
        data=result,
        x="purchase_month",
        y="revenue",
        marker="o",
        color=MAIN_COLOR,
        errorbar=None,
        ax=ax,
    )

    ax.set_title("Monthly item sales by purchase month for delivered orders")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Item Sales (BRL)")
    ax.yaxis.set_major_formatter(FuncFormatter(_compact_number))

    # Change only the graph range. The original monthly data stays unchanged.
    ax.set_xlim(start_date, end_date)

    # Show one tick every two months to keep the dates readable.
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))

    # Add compact value labels only to points inside the visible range.
    visible_points = result[
        result["purchase_month"].between(start_date, end_date, inclusive="both")
    ]

    for index, row in visible_points.reset_index(drop=True).iterrows():
        vertical_offset = 8 if index % 2 == 0 else -16
        ax.annotate(
            _compact_currency(row["revenue"]),
            xy=(row["purchase_month"], row["revenue"]),
            xytext=(0, vertical_offset),
            textcoords="offset points",
            ha="center",
            fontsize=8,
        )

    start_label = start_date.strftime("%b %Y")
    end_label = end_date.strftime("%b %Y")

    ax.text(
        0.99,
        0.03,
        f"Display range: {start_label} to {end_label}\n",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
    )

    fig.tight_layout()
    return fig


def plot_delivery_histogram(result: pd.Series) -> plt.Figure:
    """
    Q3: Show the distribution of delivery time.

    The full delivery Series is used to create the histogram. The visible
    x-axis uses the standard 1.5-IQR limits, so extreme values are outside the
    displayed range. Those values remain in the original data.

    Parameters:
        result: Series of delivery days, one value per order.

    Returns:
        Matplotlib Figure containing a Seaborn histogram.
    """
    values = pd.to_numeric(result, errors="coerce").dropna()
    lower_limit, upper_limit = _iqr_bounds(values)

    # Delivery time cannot normally be negative, so do not show negative days.
    display_start = max(0.0, lower_limit)
    display_end = max(display_start + 1.0, upper_limit)

    outlier_mask = (values < lower_limit) | (values > upper_limit)
    outlier_count = int(outlier_mask.sum())

    fig, ax = plt.subplots(figsize=(13, 6))

    # Seaborn receives every valid value, including the outliers.
    sns.histplot(
        x=values,
        binwidth=1,
        color=MAIN_COLOR,
        ax=ax,
    )

    median_days = values.median()
    ax.axvline(
        median_days,
        color=ACCENT_COLOR,
        linestyle="--",
        linewidth=2,
        label=f"Median = {median_days:.1f} days",
    )

    ax.set_title("Distribution of Delivery Time")
    ax.set_xlabel("Delivery Time (Days)")
    ax.set_ylabel("Number of Orders")

    # Only the visible axis range changes. No delivery rows are deleted.
    ax.set_xlim(display_start, display_end)
    ax.margins(y=0.15)

    # Add the count above each visible histogram bar.
    for container in ax.containers:
        labels = []
        for bar in container:
            bar_center = bar.get_x() + (bar.get_width() / 2)
            bar_height = bar.get_height()
            is_visible = display_start <= bar_center <= display_end

            if is_visible and bar_height > 0:
                labels.append(f"{int(bar_height):,}")
            else:
                labels.append("")

        ax.bar_label(container, labels=labels, padding=2, fontsize=7)

    ax.text(
        0.98,
        0.86,
        f"IQR outliers not shown: {outlier_count:,}\n",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
    )

    ax.legend()
    fig.tight_layout()
    return fig


def _count_category_outliers(
    data: pd.DataFrame,
) -> Tuple[int, float, float]:
    """
    Count 1.5-IQR outliers inside each category.

    The function returns the total count and graph limits. It does not remove
    rows from the DataFrame.
    """
    total_outliers = 0
    lower_limits = []
    upper_limits = []

    for _, group in data.groupby("category"):
        lower_limit, upper_limit = _iqr_bounds(group["delivery_days"])
        values = pd.to_numeric(group["delivery_days"], errors="coerce")

        total_outliers += int(
            ((values < lower_limit) | (values > upper_limit)).sum()
        )
        lower_limits.append(lower_limit)
        upper_limits.append(upper_limit)

    if not lower_limits:
        return 0, 0.0, 1.0

    display_start = max(0.0, min(lower_limits))
    display_end = max(display_start + 1.0, max(upper_limits))

    return total_outliers, display_start, display_end


def plot_delivery_by_category(
    result: pd.DataFrame,
    top_n: int,
) -> plt.Figure:
    """
    Q4: Compare delivery time across top revenue categories.

    The analysis result contains all categories and all delivery values.
    This chart shows the Top N revenue categories as a display choice.

    The category order is the same as the revenue ranking in Q1.
    Seaborn hides outlier points in the graph only. No rows are removed.

    Parameters:
        result: DataFrame with category, delivery_days, and category_revenue.
        top_n: Number of revenue categories to show.

    Returns:
        Matplotlib Figure containing a Seaborn box plot.
    """
    # Rank categories by total revenue from highest to lowest.
    category_ranking = (
        result.groupby("category")["category_revenue"]
        .first()
        .sort_values(ascending=False)
        .head(top_n)
    )

    # Keep the same category order as the first chart.
    order = category_ranking.index.tolist()

    # Select only the Top N categories for the visible graph.
    display_data = result[result["category"].isin(order)].copy()

    # Calculate medians without changing the revenue ranking order.
    medians = (
        display_data.groupby("category")["delivery_days"]
        .median()
        .reindex(order)
    )

    outlier_count, display_start, display_end = _count_category_outliers(
        display_data
    )

    fig, ax = plt.subplots(figsize=(13, 8))

    sns.boxplot(
        data=display_data,
        x="delivery_days",
        y="category",
        order=order,
        color=MAIN_COLOR,
        showfliers=False,
        ax=ax,
    )

    ax.set_title(
        f"Delivery Time Across Top {len(order)} Revenue Categories"
    )
    ax.set_xlabel("Delivery Time (Days)")
    ax.set_ylabel("")

    # Change only the visible graph range.
    ax.set_xlim(display_start, display_end)

    # Show the median value beside each box.
    for y_position, category in enumerate(order):
        median_value = medians.loc[category]

        ax.annotate(
            f"Median: {median_value:.1f} days",
            xy=(median_value, y_position),
            xytext=(7, 0),
            textcoords="offset points",
            va="center",
            fontsize=9,
        )

    ax.text(
        0.98,
        0.04,
        f"IQR outliers not shown: {outlier_count:,}\n",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
    )

    fig.tight_layout()
    return fig


def visualize_all(
    results: Dict[str, object],
    output_dir: str = "outputs",
) -> None:
    """
    Create all four charts and save them as PNG files.

    Parameters:
        results: Dictionary returned by analyze.analyze_all().
        output_dir: Folder used to save the PNG files.

    Returns:
        None. Four image files are saved in output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)

    figures = {
        "q1_revenue_by_category": plot_revenue_by_category(
            results["revenue_by_category"],
            top_n=10,
        ),
        "q2_monthly_revenue": plot_monthly_revenue(
            results["monthly_revenue"],
        ),
        "q3_delivery_distribution": plot_delivery_histogram(
            results["delivery_distribution"],
        ),
        "q4_delivery_by_category": plot_delivery_by_category(
            results["delivery_by_category"],
            top_n=10,
        ),
    }

    for name, fig in figures.items():
        path = os.path.join(output_dir, f"{name}.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"[visualize] saved {path}")