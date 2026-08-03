import random
from datetime import date
from typing import List

from psycopg import Connection
from data.constants import SELLER_TYPES
from utils.faker_utils import fake
from config.setting import NUM_SELLERS
from utils.logger import logger


from config.setting import (
    DEFAULT_COUNTRY,
    NUM_SELLERS,
    DATA_START_DATE,
    DATA_END_DATE,
)

def generate_sellers(num_records: int = NUM_SELLERS) -> List[tuple]:
   
    sellers = []
    for _ in range(num_records):
        sellers.append(
            (
                fake.company(),
                fake.date_between(
                    start_date=DATA_START_DATE,
                    end_date=DATA_END_DATE,
                ),
                random.choice(SELLER_TYPES),
                round(random.uniform(3.0, 5.0), 1),
                DEFAULT_COUNTRY,
            )
        )
    return sellers

def insert_sellers(
    conn: Connection,
    num_records: int = NUM_SELLERS,
):
    sql = """
        INSERT INTO seller (seller_name, join_date, seller_type, rating, country)
        VALUES (%s, %s, %s, %s, %s)
    """
    data = generate_sellers(num_records)
    try:
        with conn.cursor() as cursor:
            cursor.executemany(sql, data)
        conn.commit()
        logger.info("Inserted %s sellers.", len(data))
    except Exception:
        conn.rollback()
        raise
