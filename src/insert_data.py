from utils import get_db_connection, ensure_table_exists
from psycopg2.extras import execute_values
from psql_queries import create_rw_list_breweries, insert_rw_list_breweries


def insert_raw_data(spark, response_data):
    table_name = 'rw_list_breweries'
    if ensure_table_exists.startswith(f'Table {table_name}')
        spark.sql(create_rw_list_breweries)
    else:
        spark.sql(f'DELETE FROM {table_name}')
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                raw_data = [(json.dumps(d),) for d in response_data]
                execute_values("INSERT INTO rw_list_breweries (data) VALUES (%s)", raw_data)
            conn.commit()
            print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")



