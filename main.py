from pathlib import Path

from pipeline.load import load_raw_data
from pipeline.clean import clean_all_data


def main():
    # Get the project folder where main.py is located
    project_dir = Path(__file__).resolve().parent

    # Set the path to the data folder
    data_dir = project_dir / "data"

    # 1. Load raw data
    raw_data = load_raw_data(data_dir)

    # 2. Clean
    cleaned_data = clean_all_data(raw_data)

    # Check each dataset shape
    for name, df in cleaned_data.items():
        print(df)
        #print(f"{name}: {df.shape} | Null : {df.isna().sum().sum()}")

main()