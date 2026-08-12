CREATE OR REPLACE FUNCTION fn_seller_performance
(
    p_start_date DATE,
    p_end_date DATE,
    p_category_ids INT[] DEFAULT NULL,
    p_brand_ids INT[] DEFAULT NULL
)

RETURNS TABLE
(
    seller_id INT,
    seller_name VARCHAR(150),
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
        fs.seller_id,
        fs.seller_name,
        count(DISTINCT fs.orders_id) as total_orders, 
        sum(fs.quantity)::BIGINT as total_quantity, 
        sum(fs.subtotal)::NUMERIC(18,2) as total_revenue
    FROM vw_fact_sales fs
    WHERE fs.order_date >= p_start_date 
        AND fs.order_date < p_end_date + INTERVAL '1 DAY' 
        AND  (p_category_ids IS NULL OR fs.category_id = ANY(p_category_ids)) 
        AND (p_brand_ids IS NULL OR fs.brand_id = ANY(p_brand_ids))
        AND fs.status = 'DELIVERED'
    GROUP BY fs.seller_id, fs.seller_name
    ORDER BY
        total_quantity DESC,
        total_revenue DESC;
END;

$$;

