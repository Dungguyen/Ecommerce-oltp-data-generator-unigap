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
LANGUAGE plpgsql
AS 
$$
BEGIN 
    RETURN QUERY
    SELECT 
        fs.order_day AS report_date, 
        count(DISTINCT fs.orders_id) as total_orders, 
        sum(fs.quantity)::BIGINT as total_quantity,
        sum(fs.subtotal)::NUMERIC(18,2) AS total_revenue
    FROM vw_fact_sales fs 
    WHERE fs.order_date >= p_start_date 
        AND fs.order_date < p_end_date + INTERVAL '1 DAY' 
        AND (p_product_ids IS NULL or fs.product_id = ANY(p_product_ids))
        AND fs.status =  'DELIVERED'
    GROUP BY fs.order_date
    ORDER BY fs.order_date;

END;
$$;
