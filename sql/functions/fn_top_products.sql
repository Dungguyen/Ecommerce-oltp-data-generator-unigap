CREATE OR REPLACE FUNCTION fn_top_products
(
    p_start_date DATE,
    p_end_date DATE,
    p_seller_ids INT[] DEFAULT NULL
)

RETURNS TABLE
(
    brand_id int,
    brand_name VARCHAR(255),
    product_id int,
    product_name VARCHAR(255),
    total_quantity BIGINT, 
    total_revenue NUMERIC(18,2)
)


LANGUAGE plpgsql
AS 
$$
BEGIN 
    RETURN QUERY 

    WITH product_sales as
    (
        SELECT 
            fs.brand_id,
            fs.brand_name,
            fs.product_id,
            fs.product_name,
            sum(fs.quantity)::BIGINT as total_quantity,
            sum(fs.subtotal)::NUMERIC(18,2) as total_revenue
        FROM vw_fact_sales fs
        WHERE fs.order_date >= p_start_date 
            AND fs.order_date < p_end_date + INTERVAL '1 DAY'
            AND (p_seller_ids IS NULL OR fs.seller_id = ANY(p_seller_ids))
            AND fs.status = 'DELIVERED'
        GROUP BY fs.brand_id, fs.brand_name, fs.product_id, fs.product_name
    ),

    ranked_products AS
    (
        SELECT 
            ps.*,
            ROW_NUMBER() OVER (
                PARTITION BY ps.brand_id
                ORDER BY ps.total_quantity DESC
            ) AS rn
        FROM product_sales ps
    )

    SELECT
        rp.brand_id,
        rp.brand_name,
        rp.product_id,
        rp.product_name,
        rp.total_quantity,
        rp.total_revenue

    FROM ranked_products rp

    WHERE rp.rn = 1

    ORDER BY
        rp.brand_id,
        rp.total_quantity DESC;

END;

$$;