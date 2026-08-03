import random
from datetime import timedelta
from typing import List
from collections.abc import Iterator

from psycopg import Connection

from config.setting import (
    MAX_ITEMS_PER_ORDER,
    MIN_ITEMS_PER_ORDER,
    BATCH_SIZE,
)
from core.batch_insert import batch_insert
from utils.faker_utils import fake
from core.db_stream import stream_orders_headers

    
def load_products(conn: Connection) -> List[tuple]:

    with conn.cursor() as cur:

        cur.execute("""
            SELECT 
                product_id,
                price,
                stock_quantity
            FROM product
            WHERE stock_quantity > 0
        """)

        return cur.fetchall()
    
def generate_orders_items_batches(
    reader_conn,
    batch_size: int = BATCH_SIZE,
) -> Iterator[list[tuple]]:

    products = load_products(reader_conn)
    batch = []

    query = """
        SELECT
            orders_id,
            orders_date
        FROM orders
        ORDER BY orders_id
    """

    for orders_batch in stream_orders_headers(reader_conn):

        for orders_id, orders_date in orders_batch:

            num_items = random.randint(
                MIN_ITEMS_PER_ORDER,
                MAX_ITEMS_PER_ORDER
            )


            selected_products = random.sample(
                products,
                min(num_items, len(products))
            )

            for product_id, price, stock in selected_products:

                quantity = random.choices(
                    [1, 2, 3, 4],
                    weights = [60, 25, 10, 5],
                )[0]

                quantity = min(quantity, stock)

                offset_seconds = random.uniform(
                    0,
                    2 * 24 * 60 * 60,
                )

                created_at = orders_date + timedelta(
                    seconds=offset_seconds,
                )

                batch.append(
                    (
                        orders_id,
                        product_id,
                        orders_date,
                        quantity,
                        price,
                        created_at,
                    )
                )
                if len(batch) >= batch_size:

                    yield batch

                    batch = []

    if batch:

        yield batch

def insert_orders_items(
    reader_conn: Connection,
    writer_conn: Connection,
    batch_size: int = BATCH_SIZE,
) -> None:

    sql = """
        INSERT INTO orders_item
        (
            orders_id,
            product_id,
            orders_date,
            quantity,
            unit_price,
            created_at
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        );
    """


    batch_insert(
        conn=writer_conn,
        sql=sql,
        generator=generate_orders_items_batches(
            reader_conn,
            batch_size=batch_size,
        ),
        entity_name="orders_items",
    )
