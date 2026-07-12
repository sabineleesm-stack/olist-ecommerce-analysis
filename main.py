from pathlib import Path
 
from pipeline.load import load_raw_data
from pipeline.clean import clean_all_data
from pipeline.analyze import analyze_all
from pipeline.visualize import visualize_all
 
 
def main():
    # Get the project folder where main.py is located
    project_dir = Path(__file__).resolve().parent
 
    # Set the path to the data folder and the output folder
    # (both absolute, so it doesn't matter which directory you run
    # `python main.py` from)
    data_dir = project_dir / "data"
    output_dir = project_dir / "outputs"
 
    # 1. Load raw data
    raw_data = load_raw_data(data_dir)
 
    # 2. Clean
    cleaned_data = clean_all_data(raw_data)

    # 3. Analyze (Q1-Q4)
    results = analyze_all(cleaned_data)

    # 4. Visualize -> saves q1_*.png ... q4_*.png into <project_dir>/outputs/
    visualize_all(results, output_dir=str(output_dir))
 
 
if __name__ == "__main__":
    main()