DROP VIEW IF EXISTS vw_fact_sales CASCADE;

CREATE OR REPLACE VIEW vw_fact_sales AS 

SELECT

    /* =====================================================
       Time Dimension
    ====================================================== */

    o.orders_date,
    DATE(o.orders_date) AS order_date,

    EXTRACT(YEAR FROM o.orders_date)::INT      AS order_year,
    EXTRACT(QUARTER FROM o.orders_date)::INT   AS order_quarter,
    EXTRACT(MONTH FROM o.orders_date)::INT     AS order_month,
    EXTRACT(WEEK FROM o.orders_date)::INT      AS order_week,
    EXTRACT(DAY FROM o.orders_date)::INT       AS order_day,

    /* =====================================================
       Order Dimension
    ====================================================== */

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

    /* =====================================================
       Customer Dimension
    ====================================================== */

    cu.customer_name,
    cu.gender,
    cu.address,
    cu.city,
    cu.state,
    cu.created_at AS customer_created_at,

    /* =====================================================
       Order Item
    ====================================================== */

    oi.orders_item_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    oi.subtotal,

    /* =====================================================
       Product Dimension
    ====================================================== */

    p.product_name,
    p.price,
    p.stock_quantity,
    p.rating AS product_rating,
    p.is_active,
    p.created_at AS product_created_at,

    /* =====================================================
       Brand Dimension
    ====================================================== */

    b.brand_id,
    b.brand_name,
    b.country AS brand_country,

    /* =====================================================
       Category Dimension
    ====================================================== */

    c.category_id,
    c.category_name,
    c.level AS category_level,

    /* =====================================================
       Seller Dimension
    ====================================================== */

    s.seller_id,
    s.seller_name,
    s.seller_type,
    s.rating AS seller_rating,
    s.country AS seller_country,
    s.join_date

FROM orders o

INNER JOIN customer cu
    ON cu.customer_id = o.customer_id

INNER JOIN orders_item oi
    ON oi.orders_id = o.orders_id

INNER JOIN product p
    ON p.product_id = oi.product_id

INNER JOIN brand b
    ON b.brand_id = p.brand_id

INNER JOIN category c
    ON c.category_id = p.category_id

INNER JOIN seller s
    ON s.seller_id = p.seller_id;