CREATE TABLE IF NOT EXISTS dw.fact_sales
(
    sales_key BIGSERIAL PRIMARY KEY,

    date_key INT NOT NULL,
    customer_key BIGINT NOT NULL,
    product_key BIGINT NOT NULL,
    seller_key BIGINT NOT NULL,
    brand_key BIGINT NOT NULL,
    category_key BIGINT NOT NULL,

    orders_id INT NOT NULL,
    orders_item_id BIGINT NOT NULL,

    status VARCHAR(20),

    quantity BIGINT,
    unit_price NUMERIC(12,2),
    subtotal NUMERIC(18,2),
    total_amount NUMERIC(18,2)
);