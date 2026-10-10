"""Generate a synthetic retail sales dataset (stand-in until you download a real one).

Swap it later: put a real CSV (e.g. Kaggle "Superstore" or "Online Retail") in
data/raw/ and point eda.py at it. Column names below mirror a typical sales file.
"""
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 5000

CATEGORIES = {
    "Technology": (["Phone", "Laptop", "Headphones", "Monitor"], 250, 0.18),
    "Furniture": (["Chair", "Desk", "Bookcase", "Lamp"], 180, 0.08),
    "Office Supplies": (["Paper", "Binder", "Pen", "Stapler"], 25, 0.25),
}
REGIONS = {"West": 0.32, "East": 0.30, "Central": 0.23, "South": 0.15}
SEGMENTS = ["Consumer", "Corporate", "Home Office"]

dates = pd.to_datetime("2023-01-01") + pd.to_timedelta(rng.integers(0, 730, N), unit="D")
# Seasonality: boost Nov/Dec
keep = rng.random(N) < np.where(dates.month.isin([11, 12]), 1.0, 0.7)
dates = dates[keep]
n = len(dates)

cat = rng.choice(list(CATEGORIES), n, p=[0.25, 0.2, 0.55])
product = [rng.choice(CATEGORIES[c][0]) for c in cat]
base = np.array([CATEGORIES[c][1] for c in cat])
quantity = rng.integers(1, 8, n)
discount = rng.choice([0, 0.1, 0.2, 0.3, 0.5], n, p=[0.5, 0.2, 0.15, 0.1, 0.05])
sales = base * rng.lognormal(0, 0.4, n) * quantity * (1 - discount)
margin = np.array([CATEGORIES[c][2] for c in cat]) - discount * 0.9 + rng.normal(0, 0.04, n)
profit = sales * margin

df = pd.DataFrame(
    {
        "order_id": [f"ORD-{100000 + i}" for i in range(n)],
        "order_date": dates,
        "customer_id": [f"C{rng.integers(1, 900):04d}" for _ in range(n)],
        "segment": rng.choice(SEGMENTS, n, p=[0.52, 0.30, 0.18]),
        "region": rng.choice(list(REGIONS), n, p=list(REGIONS.values())),
        "category": cat,
        "product": product,
        "quantity": quantity,
        "discount": discount,
        "sales": sales.round(2),
        "profit": profit.round(2),
    }
)

# Add a little mess so the cleaning step is realistic
df.loc[rng.choice(n, 40, replace=False), "region"] = None
df = pd.concat([df, df.sample(15, random_state=1)], ignore_index=True)  # duplicates

out = Path(__file__).resolve().parents[1] / "data" / "raw" / "retail_sales.csv"
df.sort_values("order_date").to_csv(out, index=False)
print(f"Wrote {len(df)} rows -> {out}")
