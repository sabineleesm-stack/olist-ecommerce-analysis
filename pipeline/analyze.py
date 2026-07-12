"""
analyze.py

Analysis functions for the Olist e-commerce project.
Each function answers one project question.

Expected input:
    A dictionary returned by clean.clean_all_data().

Required keys:
    "orders", "items", "products", and "category_translation"

Important:
    The "orders" DataFrame must already contain "delivery_days".
"""

from typing import Dict

import pandas as pd


def merge_items_with_categories(cleaned: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Create one item-level table with order and category information.

    This table is used by Q1 and Q4.

    Merge steps:
        1. Merge items and orders with order_id.
        2. Merge products with product_id.
        3. Add English category names when they are available.

    Parameters:
        cleaned: Dictionary of cleaned DataFrames.

    Returns:
        DataFrame with these columns:
        order_id, product_id, price, delivery_days, and category
    """
    items = cleaned["items"]
    orders = cleaned["orders"][["order_id", "delivery_days"]]
    products = cleaned["products"]
    translation = cleaned["category_translation"]

    # Inner joins keep rows that have the keys needed for the analysis.
    df = items.merge(orders, on="order_id", how="inner")
    df = df.merge(products, on="product_id", how="inner")

    # A left join keeps the product even when an English name is missing.
    df = df.merge(translation, on="product_category_name", how="left")

    # Use the Portuguese name when there is no English translation.
    df["category"] = df["product_category_name_english"].fillna(
        df["product_category_name"]
    )

    return df[["order_id", "product_id", "price", "delivery_days", "category"]]


def analyze_revenue_by_category(
    cleaned: Dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Q1 (Group by): Which product categories had the highest total sales?

    Total sales means the sum of item prices.
    Freight cost is not included.

    This function returns every category. The Top 10 display choice is made
    later in visualize.py, so the analysis result is not cut here.

    Parameters:
        cleaned: Dictionary of cleaned DataFrames.

    Returns:
        DataFrame with category and revenue for every category.
        Rows are sorted from highest revenue to lowest revenue.
    """
    df = merge_items_with_categories(cleaned)

    result = (
        df.groupby("category", as_index=False)["price"]
        .sum()
        .rename(columns={"price": "revenue"})
        .sort_values("revenue", ascending=False)
        .reset_index(drop=True)
    )

    return result


def analyze_monthly_revenue(
    cleaned: Dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Q2 (Time trend): How did monthly sales change over time?

    This function groups all available item sales by purchase month.
    It does not remove months and it does not use a fixed date range.
    The visible date range is controlled later in visualize.py.

    Parameters:
        cleaned: Dictionary of cleaned DataFrames.

    Returns:
        DataFrame with one row per available month and these columns:
        month and revenue
    """
    items = cleaned["items"]
    orders = cleaned["orders"][["order_id", "order_purchase_timestamp"]]

    df = items.merge(orders, on="order_id", how="inner")

    # Convert each purchase date to the first day of its month.
    df["purchase_month"] = (
        df["order_purchase_timestamp"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    # Group all available rows by month. No date filter is used here.
    result = (
        df.groupby("purchase_month", as_index=False)["price"]
        .sum()
        .rename(columns={"price": "revenue"})
        .sort_values("purchase_month")
        .reset_index(drop=True)
    )

    return result


def analyze_delivery_distribution(
    cleaned: Dict[str, pd.DataFrame],
) -> pd.Series:
    """
    Q3 (Distribution): What is the distribution of delivery time?

    Delivery time is measured once per order.
    No outliers are removed in this function.

    Parameters:
        cleaned: Dictionary of cleaned DataFrames.

    Returns:
        Series of delivery days, with one value per order.
    """
    return cleaned["orders"]["delivery_days"].copy()


def analyze_delivery_by_category(
    cleaned: Dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Q4 (Category comparison): How does delivery time differ by category?

    This function returns all categories. The number of categories shown in
    the box plot is controlled later in visualize.py.

    One order can contain several items from the same category. The delivery
    time belongs to the order, not to each item. Therefore, the same
    order-category pair is counted only once. This avoids giving extra weight
    to orders that contain several items from one category.

    No delivery-time outliers are removed.

    Parameters:
        cleaned: Dictionary of cleaned DataFrames.

    Returns:
        DataFrame with these columns:
        order_id, category, delivery_days, and category_revenue
    """
    df = merge_items_with_categories(cleaned)

    # Calculate total revenue for every category without removing categories.
    category_revenue = (
        df.groupby("category", as_index=False)["price"]
        .sum()
        .rename(columns={"price": "category_revenue"})
    )

    # Keep one delivery value for each order-category pair.
    order_category_delivery = (
        df[["order_id", "category", "delivery_days"]]
        .drop_duplicates(subset=["order_id", "category"])
        .reset_index(drop=True)
    )

    result = order_category_delivery.merge(
        category_revenue,
        on="category",
        how="left",
    )

    return result.sort_values(
        ["category_revenue", "category"],
        ascending=[False, True],
    ).reset_index(drop=True)


def analyze_all(cleaned: Dict[str, pd.DataFrame]) -> Dict[str, object]:
    """
    Run all four analyses and return the results in one dictionary.

    Parameters:
        cleaned: Dictionary returned by clean.clean_all_data().

    Returns:
        Dictionary with these keys:
        revenue_by_category, monthly_revenue,
        delivery_distribution, and delivery_by_category
    """
    return {
        "revenue_by_category": analyze_revenue_by_category(cleaned),
        "monthly_revenue": analyze_monthly_revenue(cleaned),
        "delivery_distribution": analyze_delivery_distribution(cleaned),
        "delivery_by_category": analyze_delivery_by_category(cleaned),
    }