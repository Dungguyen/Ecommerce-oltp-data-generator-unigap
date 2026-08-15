CREATE TABLE IF NOT EXISTS dw.dim_product
(
    product_key BIGSERIAL PRIMARY KEY,

    product_id INT NOT NULL UNIQUE,

    product_name VARCHAR(255),
    price NUMERIC(12,2),
    stock_quantity INT,
    rating NUMERIC(5,2),
    is_active BOOLEAN,

    product_created_at TIMESTAMP,

    brand_id INT,
    category_id INT
);