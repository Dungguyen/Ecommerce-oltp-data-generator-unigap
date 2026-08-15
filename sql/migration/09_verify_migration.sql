-- =========================================================
-- Verify orders
-- =========================================================

SELECT COUNT(*) AS orders_count
FROM orders;

SELECT COUNT(*) AS orders_old_count
FROM orders_old;


-- =========================================================
-- Verify orders_item
-- =========================================================

SELECT COUNT(*) AS orders_item_count
FROM orders_item;

SELECT COUNT(*) AS orders_item_old_count
FROM orders_item_old;


-- =========================================================
-- Verify partitions
-- =========================================================

SELECT
    tableoid::regclass AS partition_name,
    COUNT(*) AS total_rows
FROM orders
GROUP BY tableoid
ORDER BY partition_name;


SELECT
    tableoid::regclass AS partition_name,
    COUNT(*) AS total_rows
FROM orders_item
GROUP BY tableoid
ORDER BY partition_name;


-- =========================================================
-- Verify view
-- =========================================================

SELECT COUNT(*)
FROM vw_fact_sales;


-- =========================================================
-- Verify index
-- =========================================================

SELECT
    indexname
FROM pg_indexes
WHERE tablename = 'orders_item';