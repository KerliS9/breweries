import json
from pyspark.sql.functions import lit, current_timestamp, from_json, col, trim
from pyspark.sql.types import StringType

from utils import init_spark
from elt_utils.write import write_delta, write_delta_partitioned
from elt_utils.schemas import breweries_schema
from fetch_api import get_list_breweries


def request_and_save_breweries():
    spark = init_spark()
    table_name = 'rw_list_breweries'
    response_data = get_list_breweries()
    raw_data = [(json.dumps(record),) for record in response_data]
    df_raw = spark.createDataFrame(data=raw_data, schema=['data'])
    df_final = df_raw.withColumn('timestamp_ingestion', current_timestamp())
    print('request_and_save_breweries:', df_final.limit(1).collect())
    write_delta(df_final, f'/warehouse/bronze/{table_name}')


def normalize_and_partition_breweries():
    spark = init_spark()
    table_name = 'silver_list_breweries'
    df_raw = spark.read.load('/warehouse/bronze/rw_list_breweries')
    df_final = (
        df_raw
        .withColumn('json_data', from_json(col('data'), breweries_schema))
        .select(
          *[trim(col(f"json_data.{field.name}")).alias(field.name) 
            for field in breweries_schema.fields 
            if isinstance(field.dataType, StringType)],
          col("timestamp_ingestion")  # Mantém colunas não-string (opcional)
        )
    )
    print('normalize_and_partition_breweries:', df_final.limit(1).collect())
    write_delta_partitioned(df_final, f'/warehouse/silver/{table_name}', 'country')


def aggregated_breweries():
    spark = init_spark()
    table_name = 'ac_agg_breweries'
    df = spark.read.load('/warehouse/silver/silver_list_breweries')
    df_final = (
        df
        .groupBy('brewery_type', 'country')
        .count()
    )
    print('normalize_and_partition_breweries:', df_final.collect())
    write_delta(df_final, f'/warehouse/gold/{table_name}')

