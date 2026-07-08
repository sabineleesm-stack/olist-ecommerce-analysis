import pandas as pd
from typing import Dict

def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    print("clean_orders")
    print(df)
    pass


def clean_items(df: pd.DataFrame) -> pd.DataFrame:
    print("clean_items")
    pass


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    print("clean_customers")
    pass


def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    print("clean_products")
    pass


def clean_category_translation(df: pd.DataFrame) -> pd.DataFrame:
    print("clean_category_translation")
    pass


def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    print("clean_reviews")
    pass


def clean_all_data(raw_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """전체 데이터 한 번에 정제 (편의 함수)"""
    cleaned = {}
    
    cleaned["orders"] = clean_orders(raw_data["orders"])
    cleaned["items"] = clean_items(raw_data["items"])
    cleaned["customers"] = clean_customers(raw_data["customers"])
    cleaned["products"] = clean_products(raw_data["products"])
    cleaned["category_translation"] = clean_category_translation(raw_data["category_translation"])
    cleaned["reviews"] = clean_reviews(raw_data["reviews"])
    
    return cleaned