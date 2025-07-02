import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask import jsonify
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


def database_exists(conn, db_name):
    query = "SELECT 1 FROM pg_database WHERE datname=%s;"
    with conn.cursor() as cur:
        cur.execute(query, (db_name,))
        return cur.fetchone() is not None


def create_database(db_name):
    try:
        with get_db_connection() as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
            if database_exists(conn, db_name):
                print(f"Database '{db_name}' already exists.")
            else:
                query = f"CREATE DATABASE {db_name};"
                with conn.cursor() as cur:
                    cur.execute(query)
                    print(f"Database '{db_name}' created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

create_database(os.getenv('POSTGRES_DB'))


def cur_fetchone(query):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            db_version = cur.fetchone()
    return db_version


def cur_fetchall(select_query):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(select_query)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            results = [dict(zip(columns, row)) for row in rows]
    return results


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


def drop_table(table_name):
    delete_query = f"DROP TABLE {table_name};"
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(delete_query)
            conn.commit()
            print(f"Table dropped successfully: {table_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_table(query):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
            conn.commit()
            print(f"Table created successfully: {table_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")
