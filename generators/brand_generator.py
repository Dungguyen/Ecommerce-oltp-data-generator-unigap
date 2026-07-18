from typing import List
import random

from psycopg import Connection
from data.brands import BRANDS
from utils.faker_utils import fake
from datetime import datetime
from utils.logger import logger

COUNTRIES = ["Vietnam", "USA", "Japan", "Germany", "France", "Italy", "China", "South Korea", "India", "Brazil"]

def generate_brands() -> List[tuple]:
    brands = []
    CREATED_AT_START = datetime(2024, 1, 1)
    CREATED_AT_END = datetime(2024, 12, 31)

    for brand in BRANDS:
        brands.append(
            (
                brand,
                random.choice(COUNTRIES),
                fake.date_time_between(start_date=CREATED_AT_START, end_date=CREATED_AT_END),
            )
        )
    return brands

def insert_brands(conn: Connection) -> None:
    sql = """
        INSERT INTO brand (brand_name, country, created_at)
        VALUES (%s, %s, %s)
        ON CONFLICT (brand_name)
        DO NOTHING;
    """
    data = generate_brands()
    try:
        with conn.cursor() as cursor:
            cursor.executemany(sql, data)
        conn.commit()
        logger.info("Inserted %s brands", len(data))
    except Exception as e:
        conn.rollback()
        print(f"Error inserting brands: {e}")   
        raise