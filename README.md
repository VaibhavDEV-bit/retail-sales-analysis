# Retail Sales Analysis — Regional Performance & Profitability

A self-directed data analysis project examining a year of retail order data across regions,
product categories, and customer segments, to identify where revenue and profit are actually
coming from.

## Business Questions
1. Which region generates the most revenue and profit?
2. Which product category has the highest profit margin?
3. How does revenue trend month-over-month across the year?
4. What are the top 5 products by revenue?
5. Which customer segment has the highest average order value?

## Data
`data/retail_sales.csv` — 3,000+ synthetic but realistic retail orders (Jan–Dec 2024) across
5 regions, 4 product categories, and 3 customer segments. The raw file intentionally includes
common real-world data issues (duplicate order IDs, missing customer segment values,
inconsistent region capitalization) to demonstrate a full cleaning workflow.

## Tools Used
- **Python** (pandas, matplotlib) — cleaning, aggregation, and visualization
- **MySQL** — equivalent SQL queries for the same business questions (`sql/schema_and_queries.sql`)
- **Excel/Tableau** — used in an earlier Deloitte simulation; this project extends that with
  fully independent Python + SQL analysis

## Workflow
1. **Clean** — removed 15 duplicate orders, standardized region names (e.g. `south` → `South`),
   filled missing customer segment values as `"Unknown"` rather than dropping rows.
2. **Analyze** — grouped and aggregated data in pandas to answer each business question.
3. **Visualize** — generated 4 charts (`charts/`) summarizing the key findings.
4. **Validate in SQL** — rewrote each pandas aggregation as a MySQL query to confirm results
   and demonstrate SQL proficiency independent of Python.

## Key Findings
- **Central region** leads in both total revenue (₹2.50 Cr) and profit (₹0.81 Cr), narrowly
  ahead of West and South.
- **Electronics** drives the largest share of revenue (~86% of total), while **Groceries**
  edges out other categories slightly on profit margin (~32.6%), showing margins are fairly
  consistent (~32%) across categories despite very different order volumes.
- Revenue peaked in **March** and stayed relatively stable through the year, with a dip in May.
- **Laptop** and **Smartwatch** are the top 2 products by revenue.
- **Consumer** and **Corporate** segments have similar average order values (~₹37,500);
  orders with unknown segment data are notably lower — a possible data-collection gap worth
  flagging to a business stakeholder.

## Charts
| Chart | Description |
|---|---|
| `monthly_revenue_trend.png` | Revenue trend across all 12 months |
| `revenue_by_region.png` | Total revenue split by region |
| `profit_margin_by_category.png` | Profit margin % by product category |
| `top_products.png` | Top 5 products by revenue |

## How to Run
```bash
pip install pandas numpy matplotlib
python generate_data.py   # creates data/retail_sales.csv
python analysis.py        # cleans data, runs analysis, saves charts to charts/
```

For the SQL version, load `data/retail_sales_clean.csv` into MySQL using the schema in
`sql/schema_and_queries.sql`, then run the queries in that file.

## Files
```
├── generate_data.py              # creates the synthetic dataset
├── analysis.py                   # cleaning + analysis + chart generation
├── data/
│   ├── retail_sales.csv          # raw data (with intentional quality issues)
│   └── retail_sales_clean.csv    # cleaned data
├── sql/
│   └── schema_and_queries.sql    # MySQL schema + business-question queries
├── charts/
│   ├── monthly_revenue_trend.png
│   ├── revenue_by_region.png
│   ├── profit_margin_by_category.png
│   └── top_products.png
└── README.md
```

---
*Author: Vaibhav — BS Data Science & AI, IIT Guwahati*
