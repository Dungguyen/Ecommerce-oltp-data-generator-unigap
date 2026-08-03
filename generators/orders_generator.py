import random
import calendar

from collections.abc import Iterator
from psycopg import Connection
from typing import List
from datetime import timedelta, datetime

from config.setting import(
    NUM_ORDERS,
    BATCH_SIZE,
)
from core.batch_insert import batch_insert
from data.orders_constants import (
    ORDER_STATUS,
    ORDER_STATUS_WEIGHTS,
)
from utils.faker_utils import fake



def load_customers(conn: Connection) -> List[int]:

    with conn.cursor() as cur:

        cur.execute("""
            SELECT customer_id
            FROM customer
        """)

        return [row[0] for row in cur.fetchall()]

def random_order_date() -> datetime:
    """
    Generate an order date distributed approximately
    evenly across months.
    """

    year = 2025

    month = random.choice([1, 2, 3, 4, 5])

    last_day = calendar.monthrange(
        year,
        month,
    )[1]

    start = datetime(
        year,
        month,
        1,
    )

    end = datetime(
        year,
        month,
        last_day,
        23,
        59,
        59,
    )

    total_seconds = (
        end - start
    ).total_seconds()

    offset = random.uniform(
        0,
        total_seconds,
    )

    return start + timedelta(
        seconds=offset,
    )
def generate_orders_batches(
    conn: Connection,
    total_records: int = NUM_ORDERS,
    batch_size: int = BATCH_SIZE,
) -> Iterator[list[tuple]]:

    customer_ids = load_customers(conn)

    generated = 0

    while generated < total_records:

        batch = []

        while len(batch) < batch_size and generated < total_records:

            customer_id = random.choice(customer_ids)

            orders_date = random_order_date()
            
            status = random.choices(
                ORDER_STATUS,
                weights=ORDER_STATUS_WEIGHTS,
                k=1,
            )[0]


            batch.append(
                (
                    customer_id,
                    orders_date,
                    status,
                    0,
                    orders_date,
                )
            )

            generated += 1

        if batch:
            yield batch


def insert_orders(
    conn: Connection,
    total_records: int = NUM_ORDERS,
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

    batch_insert(
        conn=conn,
        sql=sql,
        generator=generate_orders_batches(
            conn,
            total_records=total_records,
            batch_size=BATCH_SIZE,
        ),
        entity_name="orders",
    )