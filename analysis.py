"""
Canadian Office Supply Retailer - Sales & Profitability Analysis
Source data: public "Superstore Sales" dataset (curran/data on GitHub), 8,399 real orders.
"""
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

# -------- LOAD --------
# Source file is Windows-1252 / Latin-1 encoded (legacy export), not UTF-8 - it fails
# to load with default pandas settings and needs encoding='latin1'.
df = pd.read_csv("data/superstore_raw.csv", encoding="latin1", parse_dates=["Order Date", "Ship Date"])
print("Raw shape:", df.shape)

# -------- INSPECT DATA QUALITY --------
print("\nMissing values:\n", df.isna().sum()[df.isna().sum() > 0])
# Product Base Margin has 63 missing values out of 8,399 - too small a fraction to drop
# rows over, and margin isn't central to the questions below, so it's left as NaN
# rather than imputed (imputing a financial figure to force cleaner charts would be
# the kind of decision that quietly biases the profitability numbers below).

exact_dupes = df.duplicated().sum()
print(f"\nExact duplicate rows: {exact_dupes}")
key_dupes = df.duplicated(subset=["Order ID", "Product Name"]).sum()
print(f"Duplicate Order ID + Product Name combos: {key_dupes}")
df = df.drop_duplicates(subset=["Order ID", "Product Name"])

# -------- REAL DATA QUIRK: 'Region' is not a clean region field --------
# First pass grouping by Region turned up 8 values, not the ~5 Canadian regions
# expected: Ontario, Quebec, Atlantic, West, and "Prarie" - which is a misspelling
# of "Prairie" baked into the original dataset, not something introduced here.
# It's left as-is rather than "corrected", since renaming source category labels
# changes the data rather than cleaning it - the choice is noted here instead.
print("\nRegion values (note 'Prarie' typo is in the source data):")
print(df["Region"].value_counts())

# -------- ANALYSIS --------

# Q1: Profitability by region
region_profit = df.groupby("Region").agg(
    total_sales=("Sales", "sum"),
    total_profit=("Profit", "sum"),
    orders=("Order ID", "nunique")
).sort_values("total_profit", ascending=False)
region_profit["profit_margin_%"] = round(region_profit["total_profit"] / region_profit["total_sales"] * 100, 2)
print("\n--- Profitability by Region ---\n", region_profit)

# Q2: Which product categories are actually profitable vs which just have volume?
cat_profit = df.groupby("Product Category").agg(
    total_sales=("Sales", "sum"),
    total_profit=("Profit", "sum"),
    orders=("Order ID", "nunique")
)
cat_profit["profit_margin_%"] = round(cat_profit["total_profit"] / cat_profit["total_sales"] * 100, 2)
cat_profit = cat_profit.sort_values("profit_margin_%", ascending=False)
print("\n--- Category Profitability ---\n", cat_profit)

# Q3: Does higher discount actually correlate with lower profit margin?
# (a real question, not assumed - checked directly rather than asserted)
df["discount_bucket"] = pd.cut(df["Discount"], bins=[-0.01, 0, 0.05, 0.1, 0.15, 0.25],
                                 labels=["0%", "0-5%", "5-10%", "10-15%", "15-25%"])
discount_margin = df.groupby("discount_bucket", observed=True).apply(
    lambda g: round(g["Profit"].sum() / g["Sales"].sum() * 100, 2), include_groups=False
)
print("\n--- Profit Margin % by Discount Bucket ---\n", discount_margin)

# Q4: Ship mode cost-efficiency - which shipping mode eats into profit the most?
ship_profit = df.groupby("Ship Mode").agg(
    total_sales=("Sales", "sum"),
    total_shipping_cost=("Shipping Cost", "sum"),
    total_profit=("Profit", "sum")
)
ship_profit["shipping_cost_%_of_sales"] = round(ship_profit["total_shipping_cost"] / ship_profit["total_sales"] * 100, 2)
print("\n--- Shipping Cost as % of Sales, by Ship Mode ---\n", ship_profit)

# Q5: Top loss-making sub-categories (not just top revenue - what's actually losing money)
subcat_profit = df.groupby("Product Sub-Category")["Profit"].sum().sort_values()
print("\n--- 5 Least Profitable Sub-Categories (total $ loss/gain) ---\n", subcat_profit.head())

# -------- CHARTS --------
plt.style.use("seaborn-v0_8-whitegrid")

plt.figure(figsize=(9, 5))
region_profit["profit_margin_%"].sort_values().plot(kind="barh", color="#4C72B0")
plt.title("Profit Margin % by Region")
plt.xlabel("Profit Margin (%)")
plt.tight_layout()
plt.savefig("charts/profit_margin_by_region.png", dpi=150)
plt.close()

plt.figure(figsize=(7, 5))
cat_profit["profit_margin_%"].plot(kind="bar", color="#55A868")
plt.title("Profit Margin % by Product Category")
plt.ylabel("Profit Margin (%)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/profit_margin_by_category.png", dpi=150)
plt.close()

plt.figure(figsize=(7, 5))
discount_margin.plot(kind="bar", color="#C44E52")
plt.title("Profit Margin % by Discount Level")
plt.ylabel("Profit Margin (%)")
plt.xlabel("Discount Bucket")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/margin_by_discount.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
subcat_profit.head(8).plot(kind="barh", color="#8172B2")
plt.title("Least Profitable Product Sub-Categories (Total $ Profit)")
plt.xlabel("Total Profit ($)")
plt.tight_layout()
plt.savefig("charts/least_profitable_subcategories.png", dpi=150)
plt.close()

print("\nCharts saved.")
