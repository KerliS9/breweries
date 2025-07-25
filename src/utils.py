def init_spark():
    from pyspark.sql import SparkSession
    spark = SparkSession.builder \
        .appName("ETL Breweries - Postgres to Delta") \
        .config("spark.jars", "/opt/bitnami/spark/jars/postgresql.jar") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.sql.debug.maxToStringFields", "1000") \
        .config("spark.ui.port", "4050") \
        .getOrCreate()
    return spark