from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


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

    # ==================================================
    # 1. CHECK OLTP
    # ==================================================

    check_oltp = SQLExecuteQueryOperator(
        task_id="check_oltp",
        conn_id="ecommerce_oltp",
        sql="""
            SELECT
                COUNT(*) AS total_orders,
                COUNT(DISTINCT orders_id) AS distinct_orders
            FROM orders;
        """,
    )

    # ==================================================
    # 2. DEFINE MONTHS
    # ==================================================

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

    # ==================================================
    # 3. LOAD EACH MONTH
    #
    # IMPORTANT:
    # max_active_tis_per_dag=1
    # => only ONE mapped task runs at a time
    # ==================================================

    @task(max_active_tis_per_dag=1)
    def load_month(month_info):

        hook = PostgresHook(
            postgres_conn_id="ecommerce_dw"
        )

        month = month_info["month"]
        start_date = month_info["start_date"]
        end_date = month_info["end_date"]

        # --------------------------------------------------
        # STEP 1: Check expected rows in OLTP
        # --------------------------------------------------

        source_count_sql = f"""
            SELECT COUNT(*)
            FROM dblink(
                'host=host.docker.internal
                 port=5432
                 dbname=ecommerce_oltp
                 user=nguyendung
                 password=123456',
                $$
                    SELECT oi.orders_item_id
                    FROM orders o
                    JOIN orders_item oi
                        ON oi.orders_id = o.orders_id
                       AND oi.orders_date = o.orders_date
                    JOIN product p
                        ON p.product_id = oi.product_id
                    WHERE o.orders_date >= '{start_date}'
                      AND o.orders_date < '{end_date}'
                $$
            ) AS source_data(
                orders_item_id BIGINT
            );
        """

        source_result = hook.get_first(source_count_sql)
        expected_rows = source_result[0]

        print(
            f"[MONTH {month}] "
            f"Expected OLTP rows: {expected_rows}"
        )

        # --------------------------------------------------
        # STEP 2: Check current DW rows
        # --------------------------------------------------

        dw_count_sql = f"""
            SELECT COUNT(*)
            FROM dw.fact_sales fs
            JOIN dw.dim_date dd
                ON fs.date_key = dd.date_key
            WHERE dd.full_date >= '{start_date}'
              AND dd.full_date < '{end_date}';
        """

        dw_result = hook.get_first(dw_count_sql)
        current_rows = dw_result[0]

        print(
            f"[MONTH {month}] "
            f"Current DW rows: {current_rows}"
        )

        # --------------------------------------------------
        # STEP 3: SKIP if month is already complete
        # --------------------------------------------------

        if current_rows >= expected_rows:
            print(
                f"[MONTH {month}] "
                f"SKIP - month already complete."
            )
            return {
                "month": month,
                "status": "SKIPPED",
                "expected": expected_rows,
                "before": current_rows,
                "after": current_rows,
            }

        # --------------------------------------------------
        # STEP 4: Load missing rows
        # --------------------------------------------------

        print(
            f"[MONTH {month}] "
            f"LOAD - missing "
            f"{expected_rows - current_rows} rows."
        )

        # Disable parallel workers for this session.
        # This helps avoid the previous shared-memory
        # DiskFull error.
        hook.run(
            "SET max_parallel_workers_per_gather = 0;"
        )

        load_sql = f"""
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
                 password=123456
                 options=''-c max_parallel_workers_per_gather=0''',
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
                    WHERE o.orders_date >= '{start_date}'
                      AND o.orders_date < '{end_date}'
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

        hook.run(load_sql)

        # --------------------------------------------------
        # STEP 5: Validate this month after loading
        # --------------------------------------------------

        after_result = hook.get_first(dw_count_sql)
        after_rows = after_result[0]

        print(
            f"[MONTH {month}] "
            f"After load: {after_rows}"
        )

        if after_rows < expected_rows:
            raise ValueError(
                f"Month {month} is still incomplete. "
                f"Expected={expected_rows}, "
                f"Actual={after_rows}"
            )

        print(
            f"[MONTH {month}] "
            f"SUCCESS - month complete."
        )

        return {
            "month": month,
            "status": "LOADED",
            "expected": expected_rows,
            "before": current_rows,
            "after": after_rows,
        }

    load_tasks = load_month.expand(
        month_info=months
    )

    # ==================================================
    # 4. FINAL VALIDATION
    # ==================================================

    validate_dw = SQLExecuteQueryOperator(
        task_id="validate_dw",
        conn_id="ecommerce_dw",
        sql="""
            SELECT
                COUNT(*) AS total_fact_rows,
                COUNT(DISTINCT orders_item_id)
                    AS distinct_orders_items,
                COUNT(DISTINCT orders_id)
                    AS distinct_orders
            FROM dw.fact_sales;
        """,
    )

    validate_months = SQLExecuteQueryOperator(
        task_id="validate_months",
        conn_id="ecommerce_dw",
        sql="""
            SELECT
                DATE_TRUNC(
                    'month',
                    dd.full_date
                )::date AS month,

                COUNT(*) AS fact_rows,

                COUNT(DISTINCT fs.orders_id)
                    AS orders,

                COUNT(DISTINCT fs.orders_item_id)
                    AS items

            FROM dw.fact_sales fs

            JOIN dw.dim_date dd
                ON fs.date_key = dd.date_key

            GROUP BY 1
            ORDER BY 1;
        """,
    )

    # ==================================================
    # DEPENDENCIES
    # ==================================================

    check_oltp >> months >> load_tasks
    load_tasks >> validate_dw >> validate_months