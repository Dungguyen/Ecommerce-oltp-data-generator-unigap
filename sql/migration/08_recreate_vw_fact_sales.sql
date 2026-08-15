CREATE OR REPLACE VIEW vw_fact_sales AS
SELECT
    o.orders_date,
    DATE(o.orders_date) AS order_date,

    EXTRACT(YEAR FROM o.orders_date)::INT AS order_year,
    EXTRACT(QUARTER FROM o.orders_date)::INT AS order_quarter,
    EXTRACT(MONTH FROM o.orders_date)::INT AS order_month,
    EXTRACT(WEEK FROM o.orders_date)::INT AS order_week,
    EXTRACT(DAY FROM o.orders_date)::INT AS order_day,

    o.orders_id,
    o.customer_id,
    o.status,
    o.total_amount,

    CASE
        WHEN o.status = 'DELIVERED' THEN TRUE
        ELSE FALSE
    END AS is_completed,

    CASE
        WHEN o.status = 'CANCELLED' THEN TRUE
        ELSE FALSE
    END AS is_cancelled,

    CASE
        WHEN o.status = 'RETURNED' THEN TRUE
        ELSE FALSE
    END AS is_returned,

    cu.customer_name,
    cu.gender,
    cu.address,
    cu.city,
    cu.state,
    cu.created_at AS customer_created_at,

    oi.orders_item_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    oi.subtotal,

    p.product_name,
    p.price,
    p.stock_quantity,
    p.rating AS product_rating,
    p.is_active,
    p.created_at AS product_created_at,

    b.brand_id,
    b.brand_name,
    b.country AS brand_country,

    c.category_id,
    c.category_name,
    c.level AS category_level,

    s.seller_id,
    s.seller_name,
    s.seller_type,
    s.rating AS seller_rating,
    s.country AS seller_country,
    s.join_date

FROM orders o
JOIN customer cu
    ON cu.customer_id = o.customer_id

JOIN orders_item oi
    ON oi.orders_id = o.orders_id
   AND oi.orders_date = o.orders_date

JOIN product p
    ON p.product_id = oi.product_id

JOIN brand b
    ON b.brand_id = p.brand_id

JOIN category c
    ON c.category_id = p.category_id

JOIN seller s
    ON s.seller_id = p.seller_id;