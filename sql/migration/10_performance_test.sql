-- =========================================================
-- PERFORMANCE TEST
-- =========================================================

ANALYZE orders;
ANALYZE orders_item;


-- =========================================================
-- TEST 1: Partition pruning
-- =========================================================

EXPLAIN (ANALYZE, BUFFERS)
SELECT COUNT(*)
FROM orders
WHERE orders_date >= '2025-03-01'
  AND orders_date < '2025-04-01';


-- =========================================================
-- TEST 2: Monthly revenue
-- =========================================================

EXPLAIN (ANALYZE, BUFFERS)
SELECT
    DATE_TRUNC('month', orders_date)::DATE AS month,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS total_revenue
FROM orders
WHERE orders_date >= '2025-03-01'
  AND orders_date < '2025-04-01'
GROUP BY 1
ORDER BY 1;


-- =========================================================
-- TEST 3: Orders + Orders Item
-- =========================================================

EXPLAIN (ANALYZE, BUFFERS)
SELECT
    o.orders_date,
    COUNT(DISTINCT o.orders_id) AS total_orders,
    SUM(oi.quantity) AS total_quantity,
    SUM(oi.subtotal) AS total_revenue
FROM orders o
JOIN orders_item oi
    ON oi.orders_id = o.orders_id
   AND oi.orders_date = o.orders_date
WHERE o.orders_date >= '2025-03-01'
  AND o.orders_date < '2025-04-01'
GROUP BY o.orders_date
ORDER BY o.orders_date;


-- =========================================================
-- TEST 4: Product ID index
-- =========================================================

EXPLAIN (ANALYZE, BUFFERS)
SELECT
    product_id,
    SUM(quantity) AS total_quantity
FROM orders_item
WHERE product_id = 100
GROUP BY product_id;


-- =========================================================
-- TEST 5: vw_fact_sales
-- =========================================================

EXPLAIN (ANALYZE, BUFFERS)
SELECT
    fs.seller_id,
    fs.seller_name,
    SUM(fs.quantity) AS total_quantity,
    SUM(fs.subtotal) AS total_revenue
FROM vw_fact_sales fs
WHERE fs.order_date >= '2025-03-01'
  AND fs.order_date < '2025-04-01'
  AND fs.status = 'DELIVERED'
GROUP BY
    fs.seller_id,
    fs.seller_name
ORDER BY total_revenue DESC;