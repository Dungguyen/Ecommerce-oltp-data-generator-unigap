from collections.abc import Iterator
from psycopg import Connection

from utils.logger import logger


def batch_insert(
    conn: Connection,
    sql: str,
    generator: Iterator[list[tuple]],
    entity_name: str,
) -> None:

    inserted = 0

    try:

        with conn.cursor() as cur:

            for batch in generator:

                cur.executemany(
                    sql,
                    batch,
                )

                conn.commit()

                inserted += len(batch)

                logger.info(
                    "Inserted %s %s.",
                    inserted,
                    entity_name,
                )

    except Exception:

        conn.rollback()

        raise