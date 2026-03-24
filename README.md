# Data Analytics Project

A beginner-friendly Python project for data analytics using **pandas**, **numpy**, **matplotlib**, and **seaborn**.

## Project Structure

```
data_projrct/
├── data/
│   └── sample_data.csv        # Sample retail sales dataset (100+ rows)
├── src/
│   ├── __init__.py
│   ├── data_loader.py         # Load & inspect the CSV dataset
│   ├── data_cleaning.py       # Remove duplicates, handle missing values
│   ├── eda.py                 # Exploratory Data Analysis & statistics
│   └── visualization.py       # Generate bar charts, line plots, histogram, heatmap
├── outputs/                   # Auto-generated visualization images
├── analysis.ipynb             # Jupyter Notebook (step-by-step walkthrough)
├── main.py                    # Main script – runs the full pipeline
├── requirements.txt           # Python dependencies
└── README.md
```

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the analysis

```bash
python main.py
```

This will:
- Load `data/sample_data.csv`
- Clean the data (remove 2 duplicate rows, fill 10 missing values)
- Print descriptive statistics, category/region aggregations, and monthly trends
- Save 5 visualizations to the `outputs/` folder
- Print a summary of key business insights

### 3. (Optional) Interactive Notebook

```bash
jupyter notebook analysis.ipynb
```

## Visualizations Generated

| File | Description |
|------|-------------|
| `outputs/01_sales_by_category.png` | Bar chart – total sales per product category |
| `outputs/02_monthly_trend.png`     | Line plot – monthly sales & profit trend |
| `outputs/03_sales_histogram.png`   | Histogram – distribution of order values |
| `outputs/04_correlation_heatmap.png` | Heatmap – correlations between numeric variables |
| `outputs/05_sales_by_region.png`   | Horizontal bar – sales by geographic region |

## Dataset

`data/sample_data.csv` is a synthetic retail dataset with **102 rows** (including 2 duplicates and ~10 missing values) and the following columns:

| Column | Description |
|--------|-------------|
| `order_id` | Unique order identifier |
| `customer_name` | Customer full name |
| `category` | Product category (Electronics, Furniture, Clothing, Office Supplies) |
| `product` | Product name |
| `quantity` | Units ordered |
| `unit_price` | Price per unit ($) |
| `sales` | Total order revenue ($) |
| `discount` | Discount fraction applied |
| `profit` | Net profit ($) |
| `region` | Sales region (North, South, East, West) |
| `date` | Order date (YYYY-MM-DD) |

## Module Reference

| Module | Key function | Purpose |
|--------|-------------|---------|
| `src/data_loader.py` | `load_data()`, `inspect_data()` | Read CSV and print a summary |
| `src/data_cleaning.py` | `clean_data()` | Full cleaning pipeline |
| `src/eda.py` | `run_eda()` | Statistics & aggregations |
| `src/visualization.py` | `generate_all_visualizations()` | Save all 5 plots |

## Key Findings (sample data)

- **Top category**: Electronics ($20,097 in sales)
- **Top region**: South ($10,994 in sales)
- **Best-selling product**: Laptop ($5,200 in sales)
- **Average order value**: $402
- **Strong correlation** (r = 0.93) between `sales` and `profit`

