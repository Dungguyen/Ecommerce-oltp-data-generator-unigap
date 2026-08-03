import random   
import uuid
from typing import Iterator

from psycopg import Connection
from core.batch_insert import batch_insert
from data.constants import GENDERS
from utils.faker_utils import fake
from config.setting import (
    DATA_START_DATE,
    DATA_END_DATE,
    BATCH_SIZE,
    NUM_CUSTOMERS,
)

def generate_customers_batches(
    total_records: int = NUM_CUSTOMERS,
    batch_size: int = BATCH_SIZE,
) -> Iterator[list[tuple]]:

    generated = 0

    while generated < total_records:

        batch = []

        while len(batch) < batch_size and generated < total_records:

            batch.append(
                (
                    fake.name(),
                    f"{uuid.uuid4().hex}@gmail.com",
                    "09" + "".join(random.choices("0123456789", k=8)),
                    random.choice(GENDERS),
                    fake.address(),
                    fake.city(),
                    fake.date_time_between(
                        start_date=DATA_START_DATE,
                        end_date=DATA_END_DATE,
                    ),
                )
            )

            generated += 1

        if batch:
            yield batch

def insert_customers(
    conn: Connection,
    total_records: int = NUM_CUSTOMERS,
    batch_size: int = BATCH_SIZE,
) -> None:
    
    sql = """
        INSERT INTO customer
        (
        customer_name,
        email,
        phone, 
        gender,
        address,
        city, 
        created_at
        )

        VALUES (%s,%s,%s,%s,%s,%s,%s)

        ON CONFLICT DO NOTHING;
"""

    batch_insert(
    conn=conn,
    sql=sql,
    generator=generate_customers_batches(
        total_records=total_records,
        batch_size=batch_size,
    ),
    entity_name="customers",
)