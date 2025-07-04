from utils import get_db_connection, delete_data_from_table
from psycopg2.extras import execute_values 


def insert_raw_data(response_data):
    table_name = 'rw_list_breweries'
    delete_data_from_table(table_name)
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                raw_data = [(json.dumps(d),) for d in response_data]
                execute_values("INSERT INTO rw_list_breweries (data) VALUES (%s)", raw_data)
            conn.commit()
            print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")



