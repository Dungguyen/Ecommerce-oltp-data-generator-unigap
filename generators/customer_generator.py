import random   
import uuid
from datetime import datetime   
from typing import List

from psycopg import Connection

from data.constants import GENDERS
from utils.faker_utils import fake
from config.setting import NUM_CUSTOMERS
from utils.logger import logger

CREATED_AT_START = datetime(2024, 1, 1)
CREATED_AT_END = datetime(2024, 12, 31)


def generate_customers(num_records: int = NUM_CUSTOMERS) -> List[tuple]:

    customers = []

    used_emails = set()
    used_phones = set()

    while len(customers) < num_records:

        email = f"{uuid.uuid4().hex}@gmail.com"
        phone = "09" + "".join(random.choices("0123456789", k = 8))

        if email in used_emails or phone in used_phones:
            continue

        used_emails.add(email)
        used_phones.add(phone)

        customers.append(
            (
                fake.name(),
                email,
                phone,
                random.choice(GENDERS),
                fake.address(),
                fake.city(),
                fake.date_time_between(start_date=CREATED_AT_START, end_date=CREATED_AT_END),
            )
        )
    return customers

def insert_customers(
    conn : Connection,
    num_records: int = 5000,
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
    data = generate_customers(num_records)

    try:
        
        with conn.cursor() as cursor:
            cursor.executemany(sql,data)
        conn.commit()

        logger.info("Inserted %s customer.", len(data))
    except Exception:
        conn.rollback()

        raise