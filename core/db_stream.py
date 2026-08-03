from collections.abc import Iterator
from psycopg import Connection

DEFAULT_BATCH_SIZE = 50_000

def stream_orders_headers(
    conn: Connection,
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> Iterator[list[tuple]]:

    with conn.cursor(name="stream_orders_cursor") as cur:

        cur.execute("""
            SELECT
                orders_id,
                orders_date
            FROM orders
            ORDER BY orders_id
        """)

        while True:

            rows = cur.fetchmany(batch_size)

            if not rows:
                break

            yield rows