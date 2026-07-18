import random 
from datetime import datetime
from typing import List 
from psycopg import Connection
from utils.faker_utils import fake
from utils.logger import logger

def load_promotions(conn: Connection) -> List[int]:

    with conn.cursor() as cur:
        cur.execute("""
            SELECT promotion_id
            FROM promotion
        """)
        return [row[0] for row in cur.fetchall()]
    
def load_products(conn: Connection) -> List[int]:

    with conn.cursor() as cur:
        cur.execute("""
            SELECT product_id
            FROM product
        """)
        return [row[0] for row in cur.fetchall()]
    
def generate_promotion_products(
    conn: Connection,
) -> List[tuple]:
    
    promotions = load_promotions(conn)

    products = load_products(conn)

    data = []

    used_pair = set()

    for promotion_id in promotions:
        num_products = random.randint(20,100)

        selected_products = random.sample(
            products,
            min(num_products, len(products))
        )

        for product_id in selected_products:

            pair = (
                promotion_id,
                product_id
            )

            if pair in used_pair:
                continue

            used_pair.add(pair)

            created_at = fake.date_time_between(
                start_date="-6M",
                end_date="now"
            )

            data.append(
                (
                    promotion_id,
                    product_id,
                    created_at
                )
            )
    return data

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

    data = generate_promotion_products(conn)

    try:

        with conn.cursor() as cur:
            cur.executemany(sql, data)
        conn.commit()

        logger.info(
           "Insert %s promotion_produc records.",
            len(data)
        )
    except Exception:
        
        conn.rollback()
        raise