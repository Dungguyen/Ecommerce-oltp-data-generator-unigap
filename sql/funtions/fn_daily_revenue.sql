CREATE OR REPLACE FUNCTION fn_daily_revenue
(
    p_start_date DATE,
    p_end_date DATE,
    p_product_ids int[] DEFAULT NULL
)
RETURNS TABLE 
(
    report_date date,
    total_orders BIGINT,
    total_quantity BIGINT,
    total_revenue NUMERIC(18,2)
)
LANGUAGE SQL

AS 
$$
SELECT 
    o.orders_date::DATE as report_date, 
    count(DISTINCT o.orders_id) as total_orders, 
    sum(oi.orders_quantity) as total_quantity,
    sum(total_amount)::NUMERIC(18,2) AS total_revenue,
FROM orders o 
JOIN orders_item oi on oi.orders_id = o.order_id
WHERE 
    o.orders_date >= p_start_date and o.orders_date < p_end_date + INTERVAL '1 day' 
    and (p_product_ids IS NULL OR oi.product_id = ANY(p_product_ids))
GROUP BY report_date,
ORDER BY report_date;
$$;
