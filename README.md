# Superstore Sales & Profitability Analysis

An analysis of a real Canadian office-supply retailer's order data, examining where profit
actually comes from versus where it's just volume.

## Data source
`data/superstore_raw.csv` — 8,399 real orders from the public **"Superstore Sales"** dataset
([curran/data](https://github.com/curran/data), commonly used in BI/analytics coursework).
This is not synthetic data — it's an actual historical order export, encoding quirks and all.

## Questions asked
1. Which regions are actually the most profitable, not just the highest-revenue?
2. Which product category has the best margin — and is it the one with the most sales?
3. Do bigger discounts really hurt profit margin, in a straight line?
4. Which shipping mode eats the most into profit as a % of sales?
5. Are there whole sub-categories that lose money overall, not just on individual orders?

## Data quality notes (real, not staged)
- The file is Windows-1252 / Latin-1 encoded, not UTF-8 — a straightforward
  `pd.read_csv()` fails outright until `encoding="latin1"` is passed. This is a genuine
  legacy-export quirk, not something introduced for the exercise.
- `Product Base Margin` is missing for 63 of 8,399 rows (~0.75%). Since margin isn't
  central to the questions above, these rows were kept rather than dropped or imputed —
  imputing a financial figure here would quietly bias the profitability numbers.
- 2 rows share the same Order ID + Product Name (likely a duplicate line item on the same
  order) — dropped before aggregating.
- The `Region` field contains **"Prarie"** — a misspelling of "Prairie" that exists in the
  original source data. It's left as-is rather than "corrected," since renaming a source
  category is a data change, not a cleaning step; it's just noted here instead.

## A real dead end
The initial assumption going in was that profit margin would decline steadily as discount
increases — a straightforward "bigger discount, thinner margin" story. The data doesn't
actually support that cleanly: margin at 10-15% discount (16.8%) is *higher* than at
5-10% discount (7.8%), before collapsing to -34.6% only at the steepest discount band
(15-25%). The relationship isn't linear, and this analysis doesn't have a firm explanation
for the 10-15% bump — it's flagged as an open question rather than smoothed over with a
tidier-sounding story.

## Key findings
- **Furniture has a razor-thin 2.27% profit margin**, compared to Technology's 14.81% and
  Office Supplies' 13.80% — despite Furniture generating nearly as much revenue as
  Technology. Volume isn't a proxy for profitability here.
- **Tables and Bookcases are net loss-makers overall** (-$99K and -$34K respectively across
  the dataset), not just occasionally unprofitable on individual orders.
- **Steep discounts (15-25%) produce a -34.6% average margin** — these orders are actively
  losing the business money, not just eating into profit.
- **Nunavut has by far the lowest regional margin (2.44%)**, though on a very small base
  (56 orders) — worth flagging as a small-sample result rather than a strong regional trend.
- Shipping cost as a % of sales is fairly stable across ship modes (0.64%-0.83%), so
  shipping mode choice isn't a major profit lever compared to discounting and category mix.

## Charts
| Chart | Description |
|---|---|
| `profit_margin_by_region.png` | Profit margin % across all 8 regions |
| `profit_margin_by_category.png` | Furniture vs Technology vs Office Supplies margin |
| `margin_by_discount.png` | The non-linear discount-to-margin relationship |
| `least_profitable_subcategories.png` | Sub-categories that are net loss-makers |

## How to run
```bash
pip install pandas matplotlib
python analysis.py
```

For the SQL version, load `data/superstore_raw.csv` into MySQL using the schema in
`sql/schema_and_queries.sql`, then run the queries in that file.

## Files
```
├── analysis.py                      # cleaning + analysis + chart generation
├── data/
│   └── superstore_raw.csv           # real source data (Latin-1 encoded)
├── sql/
│   └── schema_and_queries.sql       # MySQL schema + queries
├── charts/
│   ├── profit_margin_by_region.png
│   ├── profit_margin_by_category.png
│   ├── margin_by_discount.png
│   └── least_profitable_subcategories.png
└── README.md
```

---
*Author: Vaibhav — BS Data Science & AI, IIT Guwahati*
