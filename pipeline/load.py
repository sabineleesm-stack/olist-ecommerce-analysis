import pandas as pd
from pathlib import Path


def load_raw_data(data_dir) -> pd.DataFrame:
    """
    Load selected raw CSV files for the Olist project.

    Parameters:
        data_dir (str or Path): Path to the data folder.

    Returns:
        dict: A dictionary of raw pandas DataFrames.
    """
    data_dir = Path(data_dir)

    data = {
        "orders": pd.read_csv(data_dir / "olist_orders_dataset.csv"),
        "items": pd.read_csv(data_dir / "olist_order_items_dataset.csv"),
        "customers": pd.read_csv(data_dir / "olist_customers_dataset.csv"),
        "products": pd.read_csv(data_dir / "olist_products_dataset.csv"),
        "category_translation": pd.read_csv(data_dir / "product_category_name_translation.csv"),
        "reviews": pd.read_csv(data_dir / "olist_order_reviews_dataset.csv"),
    }

    return data