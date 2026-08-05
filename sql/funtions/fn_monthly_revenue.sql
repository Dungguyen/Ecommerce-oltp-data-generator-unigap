CREATE OR REPLACE FUNCTION fn_monthly_revenue(p_start_date DATE, p_end_date DATE)
RETURNS TABLE (
    month_year DATE,
    total_orders BIGINT,
    total_quantity BIGINT,
    total_revenue NUMERIC(18,2)
) 
LANGUAGE SQL
AS
$$

SELECT 
    DATE_TRUNC('month',o.orders_date)::DATE as month_year,
    count(DISTINCT o.orders_id) as total_orders, 
    SUM(oi.quantity) as total_quantity, 
    SUM(o.total_amount)::NUMERIC(18,2) as total_revenue
FROM orders o
JOIN orders_item oi ON oi.orders_id = o.orders_id
WHERE o.order_date >= p_start_date and o.order_date < p_end_date + INTERVAL '1 day'
GROUP BY month_year, 
ORDER BY month_year ;
$$;