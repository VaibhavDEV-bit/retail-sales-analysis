import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

# -------- 1. LOAD --------
df = pd.read_csv("data/retail_sales.csv", parse_dates=["order_date"])
print("Raw shape:", df.shape)

# -------- 2. CLEAN --------
before = len(df)
df = df.drop_duplicates(subset="order_id")
print(f"Removed {before - len(df)} duplicate orders")

df["region"] = df["region"].str.title()
df["customer_segment"] = df["customer_segment"].fillna("Unknown")

missing_report = df.isna().sum()
print("\nMissing values after cleaning:\n", missing_report[missing_report > 0])

df.to_csv("data/retail_sales_clean.csv", index=False)

# -------- 3. BUSINESS QUESTIONS --------

# Q1: Which region generates the most revenue and profit?
region_summary = df.groupby("region")[["revenue", "profit"]].sum().sort_values("revenue", ascending=False)
print("\n--- Revenue & Profit by Region ---\n", region_summary)

# Q2: Which product category is most profitable (by margin %)?
cat_summary = df.groupby("category").agg(
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
    orders=("order_id", "count")
)
cat_summary["profit_margin_%"] = (cat_summary["profit"] / cat_summary["revenue"] * 100).round(2)
cat_summary = cat_summary.sort_values("profit_margin_%", ascending=False)
print("\n--- Category Profitability ---\n", cat_summary)

# Q3: Monthly revenue trend
df["month"] = df["order_date"].dt.to_period("M")
monthly = df.groupby("month")["revenue"].sum()
print("\n--- Monthly Revenue Trend ---\n", monthly)

# Q4: Top 5 products by revenue
top_products = df.groupby("product")["revenue"].sum().sort_values(ascending=False).head(5)
print("\n--- Top 5 Products by Revenue ---\n", top_products)

# Q5: Which customer segment gives highest average order value?
segment_summary = df.groupby("customer_segment")["revenue"].mean().sort_values(ascending=False)
print("\n--- Avg Order Value by Segment ---\n", segment_summary)

# -------- 4. CHARTS --------
plt.style.use("seaborn-v0_8-whitegrid")

# Chart 1: Monthly revenue trend
plt.figure(figsize=(10, 5))
monthly.plot(kind="line", marker="o")
plt.title("Monthly Revenue Trend (2024)")
plt.ylabel("Revenue (INR)")
plt.xlabel("Month")
plt.tight_layout()
plt.savefig("charts/monthly_revenue_trend.png", dpi=150)
plt.close()

# Chart 2: Revenue by region
plt.figure(figsize=(8, 5))
region_summary["revenue"].plot(kind="bar", color="#4C72B0")
plt.title("Total Revenue by Region")
plt.ylabel("Revenue (INR)")
plt.xlabel("Region")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/revenue_by_region.png", dpi=150)
plt.close()

# Chart 3: Profit margin by category
plt.figure(figsize=(8, 5))
cat_summary["profit_margin_%"].plot(kind="bar", color="#55A868")
plt.title("Profit Margin % by Category")
plt.ylabel("Profit Margin (%)")
plt.xlabel("Category")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/profit_margin_by_category.png", dpi=150)
plt.close()

# Chart 4: Top products
plt.figure(figsize=(8, 5))
top_products.plot(kind="barh", color="#C44E52")
plt.title("Top 5 Products by Revenue")
plt.xlabel("Revenue (INR)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("charts/top_products.png", dpi=150)
plt.close()

print("\nCharts saved to charts/ folder.")
