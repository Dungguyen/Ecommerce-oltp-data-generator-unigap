from psycopg import connect

from config.database import DB_CONFIG
def get_db_connection():    
    return connect(**DB_CONFIG)