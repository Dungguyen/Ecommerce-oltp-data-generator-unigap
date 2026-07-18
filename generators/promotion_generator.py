import random
from datetime import date, timedelta
from typing import List

from psycopg import Connection

from config.setting import NUM_PROMOTIONS
from data.promotions import (
    PROMOTION_NAMES,
    PROMOTION_TYPES,
    DISCOUNT_TYPES,
    PERCENTAGE_VALUES,
    FIXED_AMOUNT_VALUES,
)
from utils.faker_utils import fake
from utils.logger import logger

def generate_promotions(
    num_records: int = NUM_PROMOTIONS,
) -> List[tuple]:
    
    promotions =[]

    for _ in range(num_records):

        promotion_name = random.choice(PROMOTION_NAMES)

        promotion_type = random.choice(PROMOTION_TYPES)

        discount_type = random.choice(DISCOUNT_TYPES)

        if discount_type == "percentage":
            discount_value = random.choice(PERCENTAGE_VALUES)
        else:
            discount_value = random.choice(FIXED_AMOUNT_VALUES)

        created_at = fake.date_time_between(
            start_date="-6M",
            end_date="-4M"
        )

        start_date = fake.date_between(
            start_date=created_at.date(),
            end_date="+30d",
        )

        end_date = start_date + timedelta(
            days = random.randint(30,60)
        )

        promotions.append(
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

    return promotions

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
    
    data = generate_promotions(num_records)

    try:
        with conn.cursor() as cursor:
            cursor.executemany(sql, data)
        conn.commit()

        logger.info(
            "Inserted %s promotions.",
            len(data),
        )
    except Exception:
        conn.rollback()

        raise