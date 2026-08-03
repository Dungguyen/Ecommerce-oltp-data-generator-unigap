import random
from typing import Iterator
from psycopg import Connection

from config.setting import (
    DATA_START_DATE,
    DATA_END_DATE,
)

from data.brands import BRANDS
from utils.faker_utils import fake
from utils.logger import logger
from core.batch_insert import batch_insert

COUNTRIES = [
    "Vietnam",
    "USA",
    "Japan",
    "Germany",
    "France",
    "Italy",
    "China",
    "South Korea",
    "India",
    "Brazil",
]


def generate_brands_batches() -> Iterator[list[tuple]]:

    batch = []

    for brand in BRANDS:

        batch.append(
            (
                brand,
                random.choice(COUNTRIES),
                fake.date_time_between(
                    start_date=DATA_START_DATE,
                    end_date=DATA_END_DATE,
                ),
            )
        )

    yield batch


def insert_brands(conn: Connection) -> None:

    sql = """
        INSERT INTO brand
        (
            brand_name,
            country,
            created_at
        )

        VALUES
        (
            %s,
            %s,
            %s
        )

        ON CONFLICT (brand_name)
        DO NOTHING;
    """

    batch_insert(
        conn=conn,
        sql=sql,
        generator=generate_brands_batches(),
        entity_name="brands",
    )