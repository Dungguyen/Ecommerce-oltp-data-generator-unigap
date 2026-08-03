import random
from datetime import datetime
from typing import Iterator
from psycopg import Connection
from config.setting import (
    PRODUCTS_PER_BRAND,
    BATCH_SIZE,
    DATA_START_DATE,
    DATA_END_DATE,
)
from utils.faker_utils import fake
from data.product_catalog import PRODUCT_CATALOG
from data.product_rules import (
    PRICE_RULES,
    STOCK_RULES,
    RATING_VALUES,
    RATING_WEIGHTS,
)
from core.batch_insert import batch_insert

def load_brands(conn: Connection):
    with conn.cursor() as cur:

        cur.execute("""
            SELECT brand_id, brand_name
            FROM brand
        """)

        return cur.fetchall()
    
def load_categories(conn: Connection):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT category_id,
                    category_name
            FROM category
            WHERE level = 2
        """)

        return cur.fetchall()
    
def load_sellers(conn: Connection):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT seller_id
            FROM seller
        """)

        return [row[0] for row in cur.fetchall()]
    
def generate_products_batches(
    conn: Connection,
    products_per_brand: int = PRODUCTS_PER_BRAND,
    batch_size: int = BATCH_SIZE
) -> Iterator[list[tuple]]:

    brands = load_brands(conn)
    categories = load_categories(conn)
    sellers = load_sellers(conn)

    category_dict = {
        category_name : category_id
        for category_id, category_name in categories
    }

    batch = []

    for brand_id, brand_name in brands:
        if brand_name not in PRODUCT_CATALOG:
            continue
        catalog = PRODUCT_CATALOG[brand_name]

        for category_name, product_names in catalog.items():

            if category_name not in category_dict:
                continue

            category_id = category_dict[category_name]

            min_price, max_price = PRICE_RULES[category_name]
            min_stock, max_stock = STOCK_RULES[category_name]

            for _ in range(products_per_brand):

                batch.append(
                    (
                        random.choice(product_names),
                        category_id,
                        brand_id,
                        random.choice(sellers),
                        round(random.uniform(min_price, max_price), 2),
                        random.randint(min_stock, max_stock),
                        random.choices(
                            RATING_VALUES,
                            weights=RATING_WEIGHTS,
                            k=1
                        )[0],
                        fake.date_time_between(
                            start_date=DATA_START_DATE,
                            end_date=DATA_END_DATE
                        ),
                        True,
                    )
                )
                if len(batch) >= batch_size:
                    yield batch
                    batch = []

    if batch:   
        yield batch

def insert_products(
    conn: Connection,
    products_per_brand: int = PRODUCTS_PER_BRAND,
    batch_size: int = BATCH_SIZE,
) -> None:

    sql = """
        INSERT INTO product
        (
            product_name,
            category_id,
            brand_id,
            seller_id,
            price,
            stock_quantity,
            rating,
            created_at,
            is_active
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,%s
        );
    """

    batch_insert(
        conn=conn,
        sql=sql,
        generator=generate_products_batches(
            conn,
            products_per_brand=products_per_brand,
            batch_size=batch_size,
        ),
        entity_name="products",
    )

            
    
