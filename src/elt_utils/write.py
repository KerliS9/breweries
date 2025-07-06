from pyspark.sql import DataFrame


def write_delta(df: DataFrame, output_path: str):
    df.write.format("delta") \
        .mode("overwrite") \
        .option("overwriteSchema", "true") \
        .save(output_path)


def write_delta_partitioned(df: DataFrame, output_path: str, partition_column: str):
    df.write.format("delta") \
        .mode("overwrite") \
        .option("overwriteSchema", "true") \
        .partitionBy(partition_column) \
        .save(output_path)
