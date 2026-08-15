CREATE TABLE IF NOT EXISTS dw.dim_category
(
    category_key BIGSERIAL PRIMARY KEY,

    category_id INT NOT NULL UNIQUE,

    category_name VARCHAR(255),
    level INT
);