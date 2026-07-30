-- ============================================
-- SUPERSTORE SALES ANALYSIS - SQL
-- Source: real "Superstore Sales" dataset (curran/data, GitHub), 8,399 orders
-- ============================================

CREATE TABLE orders (
    row_id INT PRIMARY KEY,
    order_id INT,
    order_date DATE,
    order_priority VARCHAR(20),
    order_quantity INT,
    sales DECIMAL(12,2),
    discount DECIMAL(4,2),
    ship_mode VARCHAR(20),
    profit DECIMAL(12,2),
    unit_price DECIMAL(10,2),
    shipping_cost DECIMAL(10,2),
    customer_name VARCHAR(100),
    province VARCHAR(50),
    region VARCHAR(50),
    customer_segment VARCHAR(30),
    product_category VARCHAR(30),
    product_subcategory VARCHAR(50),
    product_name VARCHAR(150),
    product_container VARCHAR(30),
    product_base_margin DECIMAL(4,2),
    ship_date DATE
);

-- Q1: Profit margin % by region
SELECT region,
       ROUND(SUM(sales), 2)  AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit,
       ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct
FROM orders
GROUP BY region
ORDER BY profit_margin_pct DESC;

-- Q2: Category profitability (reveals Furniture's much lower margin vs Technology)
SELECT product_category,
       ROUND(SUM(sales), 2)  AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit,
       ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct
FROM orders
GROUP BY product_category
ORDER BY profit_margin_pct DESC;

-- Q3: Sub-categories that are net loss-makers overall
SELECT product_subcategory,
       ROUND(SUM(profit), 2) AS total_profit
FROM orders
GROUP BY product_subcategory
HAVING SUM(profit) < 0
ORDER BY total_profit ASC;

-- Q4: Shipping cost efficiency by ship mode
SELECT ship_mode,
       ROUND(SUM(sales), 2) AS total_sales,
       ROUND(SUM(shipping_cost), 2) AS total_shipping_cost,
       ROUND(SUM(shipping_cost) / SUM(sales) * 100, 2) AS shipping_pct_of_sales
FROM orders
GROUP BY ship_mode
ORDER BY shipping_pct_of_sales DESC;

-- Q5: Orders with steep discounts (15%+) and their profit outcome
-- (supports the finding that the top discount bucket runs a negative margin)
SELECT discount,
       COUNT(*) AS num_orders,
       ROUND(AVG(profit), 2) AS avg_profit_per_order
FROM orders
WHERE discount >= 0.15
GROUP BY discount
ORDER BY discount;
