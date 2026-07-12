import pandas as pd
from typing import Dict

def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    olist_orders_dataset
    Takes in a orders DataFrame, clean it, and returns the cleaned orders DataFrame
    """
    # Make a copy to avoid changing the original raw DataFrame
    orders = df.copy()

    # Keep only the columns needed for analysis
    selected_columns = [
        "order_id",
        "order_status",
        "order_purchase_timestamp",
        "order_delivered_customer_date",
    ]

    # Apply the selection to drop all other unnecessary columns
    orders = orders[selected_columns]

    # Keep only delivered orders(copied)
    orders = orders[orders["order_status"] == "delivered"].copy()

    # Convert the date column to datetime
    # Invalid values will become NaT (Not a Time)
    date_cols = [
        "order_purchase_timestamp", 
        "order_delivered_customer_date"
    ]
    orders[date_cols] = orders[date_cols].apply(pd.to_datetime, errors="coerce")

    # Drop rows where 'order_delivered_customer_date' is Null
    orders = orders.dropna(subset=["order_delivered_customer_date"])

    # Create delivery time in days (used in Q3 and Q4)
    orders["delivery_days"] = (
        orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]
    ).dt.days

    # Remove impossible values (delivered before purchase = data error)
    orders = orders[orders["delivery_days"] >= 0]

    # Return the cleaned orders DataFrame
    return orders


def clean_items(df: pd.DataFrame) -> pd.DataFrame:
    """
    olist_order_items_dataset
    Takes in a items DataFrame, clean it, and returns the cleaned items DataFrame
    """
    # Make a copy to avoid changing the original raw DataFrame
    items = df.copy()

    # Keep only the columns needed for analysis
    selected_columns = [
        "order_id",
        "product_id",
        "price",
    ]

    # Apply the selection to drop all other unnecessary columns
    items = items[selected_columns]

    return items



def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    """
    olist_products_dataset
    Takes in a products DataFrame, clean it, and returns the cleaned products DataFrame
    """
    # Make a copy to avoid changing the original raw DataFrame
    products = df.copy()

    # Keep only the columns needed for analysis
    selected_columns = [
        "product_id",
        "product_category_name",
    ]

    # Apply the selection to drop all other unnecessary columns
    products = products[selected_columns]

    # Drop missing values in 'product_category_name'
    products = products.dropna(subset=["product_category_name"])

    return products


def clean_category_translation(df: pd.DataFrame) -> pd.DataFrame:
    """
    product_category_name_translation
    Takes in a category_translation DataFrame, clean it, and returns the cleaned category_translation DataFrame
    """
    # Make a copy to avoid changing the original raw DataFrame
    category_translation = df.copy()

    # Keep only the columns needed for analysis
    selected_columns = [
        "product_category_name",
        "product_category_name_english",
    ]

    # Apply the selection to drop all other unnecessary columns
    category_translation = category_translation[selected_columns]

    return category_translation



def clean_all_data(raw_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Clean all raw Olist DataFrames and return cleaned DataFrames.

    Expected raw_data keys:
    - orders
    - items
    - products
    - category_translation
    """

    cleaned = {}

    cleaned["orders"] = clean_orders(raw_data["orders"])
    cleaned["items"] = clean_items(raw_data["items"])
    cleaned["products"] = clean_products(raw_data["products"])
    cleaned["category_translation"] = clean_category_translation(raw_data["category_translation"])

    return cleaned