# Olist E-Commerce Data Analysis Project

This project analyzes the Olist e-commerce dataset. It automatically loads, cleans, analyzes, and visualizes the data.

## 📊 Data Source
* **Olist E-Commerce Dataset:** [Kaggle Link](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

## 📁 Project Structure

* `main.py`: The main script to run the whole data pipeline.
* `pipeline/`: Contains scripts for data processing (`load.py`, `clean.py`, `analyze.py`, `visualize.py`).
* `notebooks/`: Contains `check_data.ipynb` for initial data exploration.
* `data/`: Folder for raw CSV data files.
* `outputs/`: Folder where the final graph images are saved.
* `requirements.txt`: Detailed list of all installed packages and their exact versions.
* `.gitignore.txt`: Specifies intentionally untracked files that should not be uploaded to Git. Detailed reasons for ignoring each item are commented inside the file.

## 🚀 How to Run

### 1. Setup Environment & Install Packages
Open your terminal (CMD) and activate your virtual environment. Then, install the main packages directly:
```bash
# 1. Activate the virtual environment
venv\Scripts\activate

# 2. Install core packages
pip install pandas jupyter matplotlib numpy
```
(Note: The requirements.txt file is included just to document the detailed dependencies.)

### 2. Check Data Info & Null Rates (Optional)
Before running the main script, you can explore the data (CSV info, null rates, date ranges) here:
Open and run 
```bash
notebooks/check_data.ipynb
```

### 3. Run the Analysis Pipeline
To run the full analysis and generate graphs, run:
```bash
python main.py
```
After the script finishes, you can find the generated graph images in the outputs/ folder.

## 💡 Tip: How to print data results for debugging
If you want to view the actual data tables in your terminal after running the pipeline, you can temporarily add this code to your `main.py` file.
⚠️ Please make sure to delete this code after checking!
```bash
print("\nQ1 revenue_by_category:\n", results["revenue_by_category"])
    print("\nQ2 monthly_revenue:\n", results["monthly_revenue"])
    print("\nQ3 delivery_distribution stats:\n", results["delivery_distribution"].describe())
    print(
        "\nQ4 delivery_by_category:\n",
        results["delivery_by_category"].groupby("category")["delivery_days"].describe(),
    )
```

## 📈 Analysis Questions & Visualizations

This project answers four main business questions using the Olist e-commerce data. 

| Step | Analysis Question | Business Meaning |
| :---: | :--- | :--- |
| **Q1** | Which product category generated the highest sales? | Identify the most important product categories. |
| **Q2** | How did monthly sales change over time? | Understand the overall business growth trend. |
| **Q3** | How is the overall delivery time distributed? | Evaluate the general delivery performance. |
| **Q4** | How does delivery time differ across top revenue categories? | Compare logistics performance among key products. |

---

### Q1. Which product category generated the highest sales?
![Q1 Revenue by Category]
* **Chart Description:** A bar chart showing the top 10 product categories by total sales.
* **Analysis Result:** `health_beauty`, `watches_gifts`, and `bed_bath_table` recorded the highest sales (over 1 million BRL each). This shows they are the core revenue drivers for the business.

### Q2. How did monthly sales change over time?
![Q2 Monthly Revenue]
* **Chart Description:** A line chart showing the monthly sales trend from October 2016 to August 2018.
* **Analysis Result:** The business shows a clear upward growth trend over time. We can also see sales spikes in specific months (like November 2017, likely due to Black Friday events).

### Q3. How is the overall delivery time distributed?
![Q3 Delivery Distribution]
* **Chart Description:** A histogram showing the distribution of total delivery days (extreme outliers are hidden for better view).
* **Analysis Result:** The median delivery time is **10.0 days**. Most orders are successfully delivered between 5 and 15 days. However, the graph has a long right tail, meaning some orders experience long delivery delays.

### Q4. How does delivery time differ across top revenue categories?
![Q4 Delivery by Category]
* **Chart Description:** A box plot comparing the delivery times among the top 10 categories with the highest revenue.
* **Analysis Result:** Most top categories have a similar median delivery time of 9 to 10 days. `housewares` is delivered slightly faster (8.0 days median), while `computers_accessories` takes a bit longer (11.0 days median). This helps us easily compare the shipping performance of key products.