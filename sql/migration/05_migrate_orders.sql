INSERT INTO orders
(
    orders_id,
    customer_id,
    orders_date,
    status,
    total_amount,
    created_at
)
SELECT 
    orders_id,
    customer_id,
    orders_date,
    status,
    total_amount,
    created_at
FROM orders_old;
