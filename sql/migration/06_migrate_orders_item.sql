INSERT INTO orders_item
(
    orders_item_id,
    orders_id,
    product_id,
    orders_date,
    quantity,
    unit_price,
    created_at
)
SELECT 
    orders_item_id,
    orders_id,
    product_id,
    orders_date,
    quantity,
    unit_price,
    created_at
FROM orders_item_old;