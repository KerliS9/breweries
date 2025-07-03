from pyspark.sql import SparkSession
from etl_utils.read import read_from_postgres
from etl_utils.write import write_delta_partitioned
from etl_utils.transform import normalize_schema
from fetch_api import get_list_breweries
from insert_data import insert_raw_data

spark = SparkSession.builder \
    .appName("ETL Breweries - Postgres to Delta") \
    .config("spark.jars", "/opt/bitnami/spark/jars/postgresql.jar") \
    .getOrCreate()

def request_and_save():
    response_data = get_list_breweries()
    print(response_data)
    insert_raw_data(response_data)


def normalize_and_partition_data():
    df_raw = read_from_postgres(spark, 'rw_list_breweries')
    df_normalized = normalize_schema(df_raw, brewery_schema)
    write_delta_partitioned(df_normalized, '/warehouse/delta/particionado', 'location')
