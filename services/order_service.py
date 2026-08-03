from psycopg import Connection
from utils.logger import logger

def update_order_total_amount(conn: Connection) -> None:
    """
    Update the total_amount column in the orders table
    based on the sum of the corresponding order items.
    """

    sql = """
        UPDATE "orders" o
        SET total_amount = s.total_amount
        FROM (
            SELECT orders_id, SUM(subtotal) AS total_amount
            FROM orders_item
            GROUP BY orders_id
        ) AS s
        WHERE o.orders_id = s.orders_id;
    """

    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
        logger.info("Updated total_amount in orders table successfully.")

    except Exception:
        conn.rollback()
        logger.error("Failed to update total_amount in orders table.")
        raise