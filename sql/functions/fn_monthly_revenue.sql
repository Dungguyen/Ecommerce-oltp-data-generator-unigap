CREATE OR REPLACE FUNCTION fn_monthly_revenue
(
    p_start_date DATE, 
    p_end_date DATE
)
RETURNS TABLE 
(
    report_month DATE,
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
        MAKE_DATE(fs.order_year, fs.order_month, 1) AS report_month,
        count(DISTINCT fs.orders_id)::BIGINT as total_orders, 
        SUM(fs.quantity)::BIGINT as total_quantity, 
        SUM(fs.total_amount)::NUMERIC(18,2) as total_revenue
    FROM vw_fact_sales fs
    WHERE fs.order_date >= p_start_date 
        AND fs.order_date < p_end_date + INTERVAL '1 day'
        AND fs.status = 'DELIVERED'
    GROUP BY fs.order_year, fs.order_month
    ORDER BY fs.order_year, fs.order_month;

END;
$$;