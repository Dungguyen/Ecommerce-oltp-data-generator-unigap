import random
from datetime import datetime
from typing import List
from psycopg import Connection

from utils.faker_utils import fake
from data.product_catalog import PRODUCT_CATALOG
from data.product_rules import (
    PRICE_RULES,
    STOCK_RULES,
    RATING_VALUES,
    RATING_WEIGHTS,
)

CREATED_AT_START = datetime(2024, 1, 1)
CREATED_AT_END = datetime(2024, 12, 31)

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
    
def generate_products(
    conn: Connection,
    products_per_brand: int = 40
) -> List[tuple]:
    
    brands = load_brands(conn)
    categories = load_categories(conn)
    sellers = load_sellers(conn)

    category_dict = {
        name : category_id
        for category_id, name in categories
    }

    products = []

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
                product_name = random.choice(product_names)

                description = fake.paragraph(nb_sentences=3)

                price = round(
                    random.uniform(min_price,max_price), 2
                )

                stock_quantity = random.randint(
                    min_stock,
                    max_stock
                )

                rating = random.choices(
                    RATING_VALUES,
                    weights=RATING_WEIGHTS,
                    k=1
                )[0]

                sellers_id = random.choice(sellers)

                created_at = fake.date_time_between(
                    start_date=CREATED_AT_START,
                    end_date=CREATED_AT_END
                )

                products.append(
                    (
                        product_name,
                        category_id,
                        brand_id,
                        sellers_id,
                        price,
                        stock_quantity,
                        rating,
                        created_at,
                        True
                    )
                )

    return products

def insert_products(conn: Connection):

    sql ="""
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
        )
        
    """

    data = generate_products(conn)

    try:
        with conn.cursor() as cur:
            cur.executemany(sql, data)
        conn.commit()
        print(f"Inserted, {len(data)} products.")
    except Exception as e:

        conn.rollback()
        raise

            
    
