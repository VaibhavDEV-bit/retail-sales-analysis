-- ============================================
-- RETAIL SALES ANALYSIS - SQL SCHEMA & QUERIES
-- ============================================

-- 1. CREATE TABLE
CREATE TABLE retail_sales (
    order_id INT PRIMARY KEY,
    order_date DATE,
    region VARCHAR(20),
    customer_segment VARCHAR(30),
    category VARCHAR(30),
    product VARCHAR(50),
    quantity INT,
    unit_price DECIMAL(10,2),
    discount DECIMAL(4,2),
    revenue DECIMAL(12,2),
    cost DECIMAL(12,2),
    profit DECIMAL(12,2)
);

-- Load data (run in MySQL Workbench / CLI, adjust path):
-- LOAD DATA LOCAL INFILE 'data/retail_sales_clean.csv'
-- INTO TABLE retail_sales
-- FIELDS TERMINATED BY ',' ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;

-- ============================================
-- BUSINESS QUESTIONS AS SQL QUERIES
-- ============================================

-- Q1: Total revenue and profit by region
SELECT region,
       SUM(revenue) AS total_revenue,
       SUM(profit)  AS total_profit
FROM retail_sales
GROUP BY region
ORDER BY total_revenue DESC;

-- Q2: Profit margin % by category
SELECT category,
       SUM(revenue) AS total_revenue,
       SUM(profit)  AS total_profit,
       ROUND(SUM(profit) / SUM(revenue) * 100, 2) AS profit_margin_pct
FROM retail_sales
GROUP BY category
ORDER BY profit_margin_pct DESC;

-- Q3: Monthly revenue trend
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
       SUM(revenue) AS monthly_revenue
FROM retail_sales
GROUP BY month
ORDER BY month;

-- Q4: Top 5 products by revenue
SELECT product,
       SUM(revenue) AS total_revenue
FROM retail_sales
GROUP BY product
ORDER BY total_revenue DESC
LIMIT 5;

-- Q5: Average order value by customer segment
SELECT customer_segment,
       ROUND(AVG(revenue), 2) AS avg_order_value,
       COUNT(*) AS num_orders
FROM retail_sales
GROUP BY customer_segment
ORDER BY avg_order_value DESC;

-- Q6: Regions where profit margin is below company average (subquery example)
SELECT region, ROUND(SUM(profit)/SUM(revenue)*100, 2) AS region_margin
FROM retail_sales
GROUP BY region
HAVING region_margin < (
    SELECT SUM(profit)/SUM(revenue)*100 FROM retail_sales
);
