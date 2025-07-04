import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()


def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return conn


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
