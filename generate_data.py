import numpy as np
import pandas as pd

np.random.seed(42)

n = 3000
regions = ["North", "South", "East", "West", "Central"]
categories = {
    "Electronics": ["Headphones", "Smartphone", "Laptop", "Smartwatch", "Tablet"],
    "Furniture": ["Office Chair", "Bookshelf", "Study Table", "Sofa"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers"],
    "Groceries": ["Rice 5kg", "Cooking Oil 1L", "Snacks Pack", "Tea 250g"],
}
segments = ["Consumer", "Corporate", "Small Business"]

rows = []
dates = pd.date_range("2024-01-01", "2024-12-31", freq="D")

for i in range(n):
    cat = np.random.choice(list(categories.keys()), p=[0.35, 0.15, 0.30, 0.20])
    product = np.random.choice(categories[cat])
    region = np.random.choice(regions)
    segment = np.random.choice(segments, p=[0.55, 0.25, 0.20])
    date = np.random.choice(dates)

    base_price = {
        "Electronics": np.random.uniform(1500, 60000),
        "Furniture": np.random.uniform(2000, 25000),
        "Clothing": np.random.uniform(400, 4000),
        "Groceries": np.random.uniform(50, 600),
    }[cat]

    qty = np.random.randint(1, 6)
    discount = np.random.choice([0, 0.05, 0.10, 0.15, 0.20], p=[0.4, 0.2, 0.2, 0.1, 0.1])
    revenue = round(base_price * qty * (1 - discount), 2)
    cost = round(revenue * np.random.uniform(0.55, 0.8), 2)
    profit = round(revenue - cost, 2)

    rows.append([i+1, date, region, segment, cat, product, qty, base_price, discount, revenue, cost, profit])

df = pd.DataFrame(rows, columns=[
    "order_id", "order_date", "region", "customer_segment", "category",
    "product", "quantity", "unit_price", "discount", "revenue", "cost", "profit"
])

# introduce realistic messiness for a data-cleaning story
dupe_rows = df.sample(15, random_state=1)
df = pd.concat([df, dupe_rows], ignore_index=True)

missing_idx = df.sample(40, random_state=2).index
df.loc[missing_idx, "customer_segment"] = np.nan

region_typo_idx = df.sample(20, random_state=3).index
df.loc[region_typo_idx, "region"] = df.loc[region_typo_idx, "region"].str.lower()

df.to_csv("data/retail_sales.csv", index=False)
print(df.shape)
print(df.head())
