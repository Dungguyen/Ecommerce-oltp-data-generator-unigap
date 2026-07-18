import random
from datetime import timedelta
from typing import List

from psycopg import Connection

from config.setting import NUM_ORDERS
from data.orders_constants import (
    ORDER_STATUS,
    ORDER_STATUS_WEIGHTS,
)
from utils.faker_utils import fake
from utils.logger import logger


def load_orders(conn: Connection) -> List[tuple]:

    with conn.cursor() as cur:

        cur.execute("""
            SELECT 
                orders_id,
                orders_date
            FROM orders
        """)

        return cur.fetchall()
    
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
    
def generate_orders_items(
    conn: Connection,

) -> List[tuple]:
    
    orders = load_orders(conn)

    products = load_products(conn)

    data = []

    for orders_id, orders_date in orders:

        num_items = random.choices(
            [1, 2, 3, 4, 5],
            weights=[35, 30, 20 ,10, 5],
        )[0]


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

            created_at = fake.date_time_between(
                start_date=orders_date,
                end_date=orders_date + timedelta(days=2),
            )

            data.append(
                (
                    orders_id,
                    product_id,
                    orders_date,
                    quantity,
                    price,
                    created_at,
                )
            )
    return data

def insert_orders_items(
    conn: Connection,
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

    data = generate_orders_items(conn)

    try:

        with conn.cursor() as cur:

            cur.executemany(
                sql,
                data,
            )

        conn.commit()

        logger.info(
            "Inserted %s order items.",
            len(data),
        )

    except Exception:

        conn.rollback()

        raise
