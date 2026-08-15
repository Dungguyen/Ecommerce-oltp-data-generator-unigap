CREATE TABLE IF NOT EXISTS dw.dim_customer
(
    customer_key BIGSERIAL PRIMARY KEY,

    customer_id INT NOT NULL UNIQUE,

    customer_name VARCHAR(255),
    gender VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),

    customer_created_at TIMESTAMP
);


INSERT INTO dw.dim_customer
(
    customer_id,
    customer_name,
    gender,
    address,
    city,
    state,
    customer_created_at
)
SELECT
    customer_id,
    customer_name,
    gender,
    address,
    city,
    state,
    created_at
FROM dblink(
    'dbname=ecommerce_oltp',
    '
        SELECT
            customer_id,
            customer_name,
            gender,
            address,
            city,
            state,
            created_at
        FROM customer
    '
) AS t
(
    customer_id INT,
    customer_name VARCHAR(255),
    gender VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    created_at TIMESTAMP
)
ON CONFLICT (customer_id)
DO UPDATE SET
    customer_name = EXCLUDED.customer_name,
    gender = EXCLUDED.gender,
    address = EXCLUDED.address,
    city = EXCLUDED.city,
    state = EXCLUDED.state,
    customer_created_at = EXCLUDED.customer_created_at;

