import random
from datetime import date, timedelta
from collections.abc import Iterator
from psycopg import Connection

from config.setting import BATCH_SIZE, NUM_PROMOTIONS, PROMOTION_CREATED_END, PROMOTION_CREATED_START
from data.promotions import (
    PROMOTION_NAMES,
    PROMOTION_TYPES,
    DISCOUNT_TYPES,
    PERCENTAGE_VALUES,
    FIXED_AMOUNT_VALUES,
)
from utils.faker_utils import fake
from utils.logger import logger
from core.batch_insert import batch_insert

def generate_promotions_batches(
    total_records: int = NUM_PROMOTIONS, 
    batch_size: int = BATCH_SIZE, 
) -> Iterator[list[tuple]]:

    batch = []

    for i in range(total_records):

        promotion_name = (random.choice(PROMOTION_NAMES) + f" #{i+1}")

        promotion_type = random.choice(PROMOTION_TYPES)

        discount_type = random.choice(DISCOUNT_TYPES)

        if discount_type == "percentage":
            discount_value = random.choice(PERCENTAGE_VALUES)
        else:
            discount_value = random.choice(FIXED_AMOUNT_VALUES)

        created_at = fake.date_time_between(
            start_date=PROMOTION_CREATED_START,
            end_date=PROMOTION_CREATED_END,
        )

        start_date = fake.date_between(
            start_date=created_at.date(),
            end_date="+30d",
        )

        end_date = start_date + timedelta(
            days = random.randint(30,60)
        )

        batch.append(
            (
                promotion_name,
                promotion_type,
                discount_type,
                discount_value,
                start_date,
                end_date,
                created_at,
            )
        )
        if len(batch) >= BATCH_SIZE:
            yield batch
            batch = []
    if batch:   
        yield batch

def insert_promotions(
    conn: Connection,
    num_records: int = NUM_PROMOTIONS,
) -> None:
    
    sql = """
        INSERT INTO promotion
        (
            promotion_name,
            promotion_type,
            discount_type,
            discount_value,
            start_date,
            end_date,
            created_at
        )

        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s
        )

        ON CONFLICT DO NOTHING;
        
        """
    
    data = generate_promotions_batches(num_records)

    batch_insert(
    conn=conn,
    sql=sql,
    generator=generate_promotions_batches(total_records=num_records),
    entity_name="promotions",
)