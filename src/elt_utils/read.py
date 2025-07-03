from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os


load_dotenv()

def read_from_postgres(spark: SparkSession, table_name: str):
    return spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/airflow") \
        .option("dbtable", table_name) \
        .option("user", os.getenv('POSTGRES_USER')) \
        .option("password", os.getenv('POSTGRES_PASSWORD')) \
        .load()
