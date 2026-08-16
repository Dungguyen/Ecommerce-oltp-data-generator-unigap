from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


default_args = {
    "owner": "data_engineering",
    "retries": 1,
}


with DAG(
    dag_id="ecommerce_dw_etl",
    default_args=default_args,
    description="ETL pipeline from ecommerce OLTP to Data Warehouse",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ecommerce", "etl", "data-warehouse"],
) as dag:

    # --------------------------------------------------
    # 1. Check OLTP
    # --------------------------------------------------

    check_oltp = SQLExecuteQueryOperator(
        task_id="check_oltp",
        conn_id="ecommerce_oltp",
        sql="""
            SELECT COUNT(*) AS total_orders
            FROM orders;
        """,
    )

    # --------------------------------------------------
    # 2. Load Fact Sales - Jan to May 2025
    # --------------------------------------------------

    @task
    def get_months():
        return [
            {
                "month": 1,
                "start_date": "2025-01-01",
                "end_date": "2025-02-01",
            },
            {
                "month": 2,
                "start_date": "2025-02-01",
                "end_date": "2025-03-01",
            },
            {
                "month": 3,
                "start_date": "2025-03-01",
                "end_date": "2025-04-01",
            },
            {
                "month": 4,
                "start_date": "2025-04-01",
                "end_date": "2025-05-01",
            },
            {
                "month": 5,
                "start_date": "2025-05-01",
                "end_date": "2025-06-01",
            },
        ]

    months = get_months()

    @task(max_active_tis_per_dag=1)
    def load_month(month_info):
        from airflow.providers.postgres.hooks.postgres import PostgresHook

        hook = PostgresHook(postgres_conn_id="ecommerce_dw")

        sql = f"""
            INSERT INTO dw.fact_sales
            (
                date_key,
                customer_key,
                product_key,
                seller_key,
                brand_key,
                category_key,
                orders_id,
                orders_item_id,
                status,
                quantity,
                unit_price,
                subtotal,
                total_amount
            )
            SELECT
                dd.date_key,
                dc.customer_key,
                dp.product_key,
                ds.seller_key,
                db.brand_key,
                dcat.category_key,
                t.orders_id,
                t.orders_item_id,
                t.status,
                t.quantity,
                t.unit_price,
                t.subtotal,
                t.total_amount
            FROM dblink(
                'host=host.docker.internal
                 port=5432
                 dbname=ecommerce_oltp
                 user=nguyendung
                 password=123456',
                $$
                    SELECT
                        o.orders_id,
                        oi.orders_item_id,
                        o.customer_id,
                        oi.product_id,
                        p.seller_id,
                        p.brand_id,
                        p.category_id,
                        o.orders_date,
                        o.status,
                        oi.quantity,
                        oi.unit_price,
                        oi.subtotal,
                        o.total_amount
                    FROM orders o
                    JOIN orders_item oi
                        ON oi.orders_id = o.orders_id
                       AND oi.orders_date = o.orders_date
                    JOIN product p
                        ON p.product_id = oi.product_id
                    WHERE o.orders_date >= '{month_info["start_date"]}'
                      AND o.orders_date < '{month_info["end_date"]}'
                $$
            ) AS t
            (
                orders_id INT,
                orders_item_id BIGINT,
                customer_id INT,
                product_id INT,
                seller_id INT,
                brand_id INT,
                category_id INT,
                orders_date TIMESTAMP,
                status VARCHAR(20),
                quantity BIGINT,
                unit_price NUMERIC(12,2),
                subtotal NUMERIC(18,2),
                total_amount NUMERIC(18,2)
            )
            JOIN dw.dim_date dd
                ON dd.full_date = DATE(t.orders_date)
            JOIN dw.dim_customer dc
                ON dc.customer_id = t.customer_id
            JOIN dw.dim_product dp
                ON dp.product_id = t.product_id
            JOIN dw.dim_seller ds
                ON ds.seller_id = t.seller_id
            JOIN dw.dim_brand db
                ON db.brand_id = t.brand_id
            JOIN dw.dim_category dcat
                ON dcat.category_id = t.category_id

            ON CONFLICT (orders_item_id)
            DO NOTHING;
        """

        hook.run(sql)

    load_tasks = load_month.expand(month_info=months)

    # --------------------------------------------------
    # 3. Validate DW
    # --------------------------------------------------

    validate_dw = SQLExecuteQueryOperator(
        task_id="validate_dw",
        conn_id="ecommerce_dw",
        sql="""
            SELECT
                COUNT(*) AS total_fact_rows,
                COUNT(DISTINCT orders_item_id) AS distinct_orders_items
            FROM dw.fact_sales;
        """,
    )

    check_oltp >> months >> load_tasks >> validate_dw