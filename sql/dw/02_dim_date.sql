CREATE TABLE IF NOT EXISTS dw.dim_date
(
    date_key        INT PRIMARY KEY,
    full_date       DATE NOT NULL UNIQUE,

    year            INT NOT NULL,
    quarter         INT NOT NULL,
    month           INT NOT NULL,
    month_name      VARCHAR(20) NOT NULL,
    week            INT NOT NULL,
    day             INT NOT NULL
);

INSERT INTO dw.dim_date
(
    date_key,
    full_date,
    year,
    quarter,
    month,
    month_name,
    week,
    day
)
SELECT
    TO_CHAR(d, 'YYYYMMDD')::INT AS date_key,
    d::DATE AS full_date,
    EXTRACT(YEAR FROM d)::INT AS year,
    EXTRACT(QUARTER FROM d)::INT AS quarter,
    EXTRACT(MONTH FROM d)::INT AS month,
    TO_CHAR(d, 'Month') AS month_name,
    EXTRACT(WEEK FROM d)::INT AS week,
    EXTRACT(DAY FROM d)::INT AS day
FROM generate_series(
    '2025-01-01'::DATE,
    '2025-05-31'::DATE,
    INTERVAL '1 day'
) AS d
ON CONFLICT (date_key) DO NOTHING;