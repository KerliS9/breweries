from utils import get_db_connection, cur_fetchall, delete_data_from_table


def insert_raw_data(response_data):
  table_name = 'rw_list_breweries'
  delete_data_from_table(table_name)
  insert_query = """
    INSERT INTO rw_list_breweries (data) VALUES (%s)"
    """

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                for data in response_data:
                    cur.execute(insert_query, json.dumps(data))
            conn.commit()
            print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def insert_silver_data(response_data):
    table_name = 'silver_list_breweries'
    delete_data_from_table(table_name)
    insert_query = """
    INSERT INTO breweries (
        id, name, brewery_type, address_1, address_2, address_3,
        city, state_province, postal_code, country,
        longitude, latitude, phone, website_url, state, street
    )
    VALUES (
        %(id)s, %(name)s, %(brewery_type)s, %(address_1)s, %(address_2)s, %(address_3)s,
        %(city)s, %(state_province)s, %(postal_code)s, %(country)s,
        %(longitude)s, %(latitude)s, %(phone)s, %(website_url)s, %(state)s, %(street)s
    )
    """

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                for data in response_data:
                    cur.execute(insert_query, (data))
            conn.commit()
            print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")