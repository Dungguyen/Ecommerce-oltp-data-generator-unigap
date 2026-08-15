CREATE TABLE IF NOT EXISTS dw.dim_brand
(
    brand_key BIGSERIAL PRIMARY KEY,

    brand_id INT NOT NULL UNIQUE,

    brand_name VARCHAR(255),
    country VARCHAR(100)
);