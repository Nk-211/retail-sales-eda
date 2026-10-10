# Retail Sales EDA (Level 1 · Project 01)

Explore a sales dataset to find patterns and business insights.

## Setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/generate_data.py   # creates data/raw/retail_sales.csv (synthetic)
python src/eda.py             # cleans, analyses, saves charts, prints insights
jupyter lab                   # optional: explore interactively
```

## Structure
```
data/raw/            input CSV (replace with a real dataset)
src/generate_data.py synthetic data generator
src/eda.py           load -> clean -> engineer -> analyse -> visualise -> insights
outputs/figures/     generated charts
```

## Workflow
1. **Load** the CSV and inspect shape, types, `describe()`
2. **Clean**: missing values, duplicates
3. **Engineer** features: month, year, profit margin
4. **Analyse**: trend, category, region, discount vs margin, correlations
5. **Communicate**: charts + written insights

## To do next
- Replace synthetic data with a real dataset (Kaggle "Superstore Sales" / "Online Retail")
- Move the analysis into a Jupyter notebook with markdown commentary
- Add outlier handling and a customer-level view (repeat buyers, top customers)
- Write a one-page findings summary with recommendations
