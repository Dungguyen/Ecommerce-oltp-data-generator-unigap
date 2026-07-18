from datetime import datetime
from typing import List

from psycopg import Connection

from data.categories import CATEGORY_DATA
from utils.faker_utils import fake


CREATED_AT_START = datetime(2024, 1, 1)
CREATED_AT_END = datetime(2024, 12, 31)


def generate_parent_categories() -> List[tuple]:
    """
    Generate level-1 categories.
    """

    parents = []

    for item in CATEGORY_DATA:

        parents.append(
            (
                item["category_name"],
                None,
                1,
                fake.date_time_between(
                    start_date=CREATED_AT_START,
                    end_date=CREATED_AT_END
                )
            )
        )

    return parents


def generate_sub_categories(category_map: dict) -> List[tuple]:
    """
    Generate level-2 categories.
    """

    children = []

    for item in CATEGORY_DATA:

        parent_name = item["category_name"]
        parent_id = category_map[parent_name]

        for sub in item["subcategories"]:

            children.append(
                (
                    sub,
                    parent_id,
                    2,
                    fake.date_time_between(
                        start_date=CREATED_AT_START,
                        end_date=CREATED_AT_END
                    )
                )
            )

    return children


def insert_categories(conn: Connection):

    parent_sql = """
    INSERT INTO category
    (
        category_name,
        parent_category_id,
        level,
        created_at
    )

    VALUES
    (%s, %s, %s, %s)

    ON CONFLICT (category_name)
    DO NOTHING;
    """

    child_sql = parent_sql

    # =====================================================
    # Insert level-1 categories
    # =====================================================

    parent_data = generate_parent_categories()

    with conn.cursor() as cur:

        cur.executemany(parent_sql, parent_data)

    conn.commit()

    # =====================================================
    # Load parent IDs
    # =====================================================

    with conn.cursor() as cur:

        cur.execute("""
            SELECT category_name,
                   category_id
            FROM category
            WHERE level = 1
        """)

        category_map = {
            row[0]: row[1]
            for row in cur.fetchall()
        }

    # =====================================================
    # Insert level-2 categories
    # =====================================================

    child_data = generate_sub_categories(category_map)

    with conn.cursor() as cur:

        cur.executemany(child_sql, child_data)

    conn.commit()

    print(
        f"Inserted {len(parent_data)} parent categories."
    )

    print(
        f"Inserted {len(child_data)} sub categories."
    )