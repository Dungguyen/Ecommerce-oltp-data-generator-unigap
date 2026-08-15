CREATE TABLE IF NOT EXISTS dw.dim_seller
(
    seller_key BIGSERIAL PRIMARY KEY,

    seller_id INT NOT NULL UNIQUE,

    seller_name VARCHAR(150),
    seller_type VARCHAR(100),
    rating NUMERIC(5,2),
    country VARCHAR(100),
    join_date DATE
);