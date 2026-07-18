import random
from datetime import datetime
from typing import List

from psycopg import Connection

from config.setting import NUM_ORDERS
from data.orders_constants import (
    ORDER_STATUS,
    ORDER_STATUS_WEIGHTS,
)
from utils.faker_utils import fake
from utils.logger import logger

ORDER_START = datetime(2025, 1, 1)
ORDER_END = datetime(2025, 12, 31)


def load_customers(conn: Connection) -> List[int]:

    with conn.cursor() as cur:

        cur.execute("""
            SELECT customer_id
            FROM customer
        """)

        return [row[0] for row in cur.fetchall()]


def generate_orders(
    conn: Connection,
    num_records: int = NUM_ORDERS,
) -> List[tuple]:

    customer_ids = load_customers(conn)

    orderss = []

    for _ in range(num_records):

        customer_id = random.choice(customer_ids)

        orders_date = fake.date_time_between(
            start_date=ORDER_START,
            end_date=ORDER_END,
        )

        status = random.choices(
            ORDER_STATUS,
            weights=ORDER_STATUS_WEIGHTS,
        )[0]

        created_at = orders_date

        # Sẽ được cập nhật sau khi sinh order_item
        total_amount = 0

        orderss.append(
            (
                customer_id,
                orders_date,
                status,
                total_amount,
                created_at,
            )
        )

    return orderss


def insert_orders(
    conn: Connection,
    num_records: int = NUM_ORDERS,
) -> None:

    sql = """
        INSERT INTO "orders"
        (
            customer_id,
            orders_date,
            status,
            total_amount,
            created_at
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s
        );
    """

    data = generate_orders(
        conn,
        num_records,
    )

    try:
        
        with conn.cursor() as cur:
            cur.executemany(sql,data)
        conn.commit()

        logger.info(
            "Inserted %s orders.",
            len(data),
        )
    except Exception as e:

        conn.rollback()
        raise