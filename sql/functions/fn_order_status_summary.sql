CREATE OR REPLACE FUNCTION fn_order_status_summary
(
    p_start_date DATE,
    p_end_date DATE,
    p_seller_ids int[] DEFAULT NULL,
    p_category_ids int[] DEFAULT NULL
)
RETURNS TABLE
(
    status VARCHAR(20),
    total_orders BIGINT,
    total_revenue NUMERIC(18,2)
)
LANGUAGE plpgsql
AS
$$
BEGIN 
    RETURN QUERY
    SELECT
        fs.status,
        count(DISTINCT fs.orders_id) as total_orders, 
        SUM(fs.subtotal)::NUMERIC(18,2) as total_revenue
    FROM vw_fact_sales fs
    WHERE fs.order_date >= p_start_date 
        AND fs.order_date < p_end_date + INTERVAL '1 day' 
        AND(
            p_seller_ids IS NULL 
            OR fs.seller_id = ANY(p_seller_ids)
        )
        AND (
            p_category_ids IS NULL 
            OR fs.category_id = ANY(p_category_ids)
        )
        
    GROUP BY fs.status  
    ORDER BY fs.status;

END;
$$