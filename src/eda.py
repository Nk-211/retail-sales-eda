"""Exploratory Data Analysis on retail sales.

Run:  python src/eda.py [path/to/data.csv]
Produces charts in outputs/figures/ and prints key business insights.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "outputs" / "figures"
FIG.mkdir(parents=True, exist_ok=True)
sns.set_theme(style="whitegrid")


def save(name: str) -> None:
    plt.tight_layout()
    plt.savefig(FIG / f"{name}.png", dpi=120)
    plt.close()


# 1. LOAD ---------------------------------------------------------------
path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "raw" / "retail_sales.csv"
df = pd.read_csv(path, parse_dates=["order_date"])
print(f"Loaded {df.shape[0]:,} rows x {df.shape[1]} columns\n")
print(df.head(), "\n")
print(df.describe(include="all").T[["count", "unique", "mean", "min", "max"]], "\n")

# 2. CLEAN --------------------------------------------------------------
print("Missing values:\n", df.isna().sum()[df.isna().sum() > 0], "\n")
dupes = df.duplicated().sum()
df = df.drop_duplicates()
df["region"] = df["region"].fillna("Unknown")
print(f"Dropped {dupes} duplicate rows; filled missing region with 'Unknown'\n")

# 3. FEATURE ENGINEERING ------------------------------------------------
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
df["profit_margin"] = df["profit"] / df["sales"]

# 4. ANALYSE + VISUALISE -----------------------------------------------
# Sales trend over time
monthly = df.groupby("month")[["sales", "profit"]].sum()
monthly.plot(figsize=(10, 4), title="Monthly sales and profit")
save("01_monthly_trend")

# Sales / profit by category
cat = df.groupby("category")[["sales", "profit"]].sum().sort_values("sales", ascending=False)
cat.plot.bar(figsize=(7, 4), title="Sales and profit by category", rot=0)
save("02_category")

# Regional performance
reg = df.groupby("region")[["sales", "profit"]].sum().sort_values("sales", ascending=False)
reg.plot.bar(figsize=(7, 4), title="Sales and profit by region", rot=0)
save("03_region")

# Distribution of order value (skew -> log scale)
plt.figure(figsize=(7, 4))
sns.histplot(df["sales"], bins=50, log_scale=True)
plt.title("Distribution of order value (log scale)")
save("04_sales_distribution")

# Discount vs profit margin (does discounting hurt?)
disc = df.groupby("discount")["profit_margin"].mean()
plt.figure(figsize=(7, 4))
disc.mul(100).plot.bar(rot=0, title="Average profit margin (%) by discount level")
save("05_discount_vs_margin")

# Correlation heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(df[["quantity", "discount", "sales", "profit"]].corr(), annot=True, cmap="coolwarm", center=0)
plt.title("Correlation matrix")
save("06_correlation")

# Top products
top = df.groupby("product")["profit"].sum().sort_values()
top.plot.barh(figsize=(7, 5), title="Total profit by product")
save("07_product_profit")

# 5. INSIGHTS -----------------------------------------------------------
best_month = df.groupby(df["order_date"].dt.month_name())["sales"].sum().idxmax()
loss_products = top[top < 0].index.tolist()
print("=== KEY INSIGHTS ===")
print(f"- Total sales: ${df['sales'].sum():,.0f} | profit: ${df['profit'].sum():,.0f} "
      f"({df['profit'].sum() / df['sales'].sum():.1%} margin)")
print(f"- Top category by sales: {cat.index[0]}; most profitable: {cat['profit'].idxmax()}")
print(f"- Top region by sales: {reg.index[0]}")
print(f"- Peak sales month of the year: {best_month}")
print(f"- Margin at 0% discount: {disc.get(0, float('nan')):.1%} vs at max discount: {disc.iloc[-1]:.1%}")
print(f"- Loss-making products: {loss_products or 'none'}")
print(f"\nCharts saved in {FIG}")
