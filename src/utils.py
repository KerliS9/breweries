import psycopg2
import os
from dotenv import load_dotenv
from psql_queries import create_tables


load_dotenv()


def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return conn


def ensure_table_exists(table_name):
    """Create table if it doesn't exist"""
    if table_name not in create_tables:
        return f"Table {table_name} doesn't exist"


def delete_data_from_table(table_name):
    delete_query = f"DELETE FROM {table_name};"
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(delete_query)
            conn.commit()
            print(f"All data deleted successfully: {table_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")
