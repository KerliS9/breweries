from elt_utils.read import read_from_postgres
from elt_utils.write import write_delta_partitioned
from elt_utils.transform import normalize_schema
from fetch_api import get_list_breweries
from insert_data import insert_raw_data


def init_spark():
  from pyspark.sql import SparkSession
  spark = SparkSession.builder \
      .appName("ETL Breweries - Postgres to Delta") \
      .config("spark.jars", "/opt/bitnami/spark/jars/postgresql.jar") \
      .getOrCreate()
  return spark

def request_and_save_breweries():
    response_data = get_list_breweries()
    print('request_and_save_breweries:', response_data[0])
    insert_raw_data(response_data)
request_and_save_breweries()

def normalize_and_partition_breweries():
    spark = init_spark()
    df_raw = read_from_postgres(spark, 'rw_list_breweries')
    df_normalized = normalize_schema(df_raw, brewery_schema)
    write_delta_partitioned(df_normalized, '/warehouse/delta/particionado', 'location')
