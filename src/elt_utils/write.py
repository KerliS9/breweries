from pyspark.sql import DataFrame


def write_delta_partitioned(df: DataFrame, output_path: str, partition_column: str):
    df.write.format("delta") \
        .mode("overwrite") \
        .partitionBy(partition_column) \
        .save(output_path)
