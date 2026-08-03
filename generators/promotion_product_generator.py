import random 
from typing import Iterator
from psycopg import Connection
from core.batch_insert import batch_insert
from utils.faker_utils import fake
from config.setting import (
    BATCH_SIZE,
    MAX_PRODUCTS_PER_PROMOTION,
    MIN_PRODUCTS_PER_PROMOTION,
    DATA_START_DATE,
    DATA_END_DATE,  
)

def load_promotions(conn: Connection) -> list[int]:

    with conn.cursor() as cur:
        cur.execute("""
            SELECT promotion_id
            FROM promotion
        """)
        return [row[0] for row in cur.fetchall()]
    
def load_products(conn: Connection) -> list[int]:

    with conn.cursor() as cur:
        cur.execute("""
            SELECT product_id
            FROM product
        """)
        return [row[0] for row in cur.fetchall()]
    
def generate_promotion_products_batches(
    conn: Connection,
    batch_size: int = BATCH_SIZE,
) -> Iterator[list[tuple]]:

    promotions = load_promotions(conn)
    products = load_products(conn)

    batch = []

    for promotion_id in promotions:

        num_products = random.randint(
            MIN_PRODUCTS_PER_PROMOTION,
            min(MAX_PRODUCTS_PER_PROMOTION, len(products)),
        )

        selected_products = random.sample(
            products,
            num_products,
        )

        for product_id in selected_products:

            created_at = fake.date_time_between(
                start_date=DATA_START_DATE,
                end_date=DATA_END_DATE,
            )

            batch.append(
                (
                    promotion_id,
                    product_id,
                    created_at,
                )
            )

            if len(batch) >= batch_size:
                yield batch
                batch = []

    if batch:
        yield batch

def insert_promotion_products(
    conn: Connection,
) -> None:
    
    sql = """
        INSERT INTO promotion_product
        (
            promotion_id,
            product_id,
            created_at
        )
        
        VALUES
        (
            %s,%s,%s
        )

        ON CONFLICT
        (
            promotion_id,
            product_id
        )
        DO NOTHING;
    """

    batch_insert(
        conn=conn,
        sql=sql,
        generator=generate_promotion_products_batches(conn),
        entity_name="promotion_products",
    )
