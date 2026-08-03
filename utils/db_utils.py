from psycopg import connect
from psycopg import Connection

from config.database import DB_CONFIG
def get_db_connection():    
    return connect(**DB_CONFIG)

def get_reader_connection() -> Connection:
    return connect(**DB_CONFIG)


def get_writer_connection() -> Connection:
    return connect(**DB_CONFIG)