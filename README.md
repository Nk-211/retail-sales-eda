# Retail Sales EDA (Level 1 · Project 01)

Exploratory analysis of the **Superstore Sales** dataset (9,994 US orders, 2015–2018):
where the business makes and loses money, and what to change.

**Start here → [`notebooks/retail_sales_eda.ipynb`](notebooks/retail_sales_eda.ipynb)** (outputs included, renders on GitHub)

## Headline findings
- $2.30M sales, $286K profit (12.5% margin); sales up ~50% from 2015 to 2018
- Nov–Dec are the peak months
- Discounts of 30% or more lose money (14% of orders, $135K lost); capping discounts at ~20% is the biggest lever
- Tables, Bookcases and Supplies are loss-making; Furniture margin is only 2.5%
- Texas, Ohio and Pennsylvania lose money; top 20% of customers = 48% of sales

## Setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab notebooks/retail_sales_eda.ipynb
```

## Structure
```
data/raw/superstore.csv       real dataset (Orders sheet + appended sheets, cleaned in the notebook)
notebooks/retail_sales_eda.ipynb   main analysis: load > clean > engineer > analyse > recommend
src/eda.py, src/generate_data.py   earlier script version on synthetic data (kept for reference)
```

## Ideas to extend
- Add a forecast of monthly sales (e.g. seasonal naive / Prophet)
- Profit-by-product-name deep dive for the loss-making sub-categories
- Interactive dashboard (Plotly / Streamlit / Power BI)
