import pytest
from pyspark.sql import SparkSession
from unittest.mock import MagicMock, PropertyMock
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from src.process_data import normalize_and_partition_breweries  # Replace with actual import
#from src.elt_utils.schemas import breweries_schema


@pytest.fixture
def spark_session():
    """Fixture to create a SparkSession for testing"""
    spark = (
        SparkSession.builder
        .master("local[1]")
        .appName("pytest-pyspark")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.jars", "/opt/spark/jars/delta-core_2.12-2.4.0.jar,/opt/spark/jars/delta-storage-2.4.0.jar")
        .getOrCreate()
    )
    yield spark
    spark.stop()

def test_normalize_and_partition_breweries(spark_session, mocker):
    """Test the complete normalization and partitioning workflow"""
    # Mock dependencies
    mock_init_spark = mocker.patch(
        'src.utils.init_spark', 
        return_value=spark_session
    )
    mock_write_delta = mocker.patch("src.elt_utils.write.write_delta_partitioned")

    # Create test data
    test_data = [
        {"data": '{"id": "1", "name": "Brew1", "country": "US"}', "timestamp_ingestion": "2023-01-01T00:00:00"},
        {"data": '{"id": "2", "name": "Brew2", "country": "UK"}', "timestamp_ingestion": "2023-01-01T00:00:00"}
    ]
    test_df = spark_session.createDataFrame(test_data)

    # Mock Spark read
    mocker.patch(
        'pyspark.sql.SparkSession.read',
        return_value=MagicMock(load=MagicMock(return_value=test_df))
    )
    mocker.patch.object(
        spark_session.read.option("inferSchema", "true"),
        'load',
        return_value=test_df
    )

    # Call the function
    normalize_and_partition_breweries()

    # Assertions
    mock_init_spark.assert_called_once()

    # Verify the write_delta_partitioned call
    args, kwargs = mock_write_delta.call_args
    assert kwargs['path'] == '/warehouse/delta/particionado/silver/silver_list_breweries'
    assert kwargs['partition_column'] == 'country'

    # Verify the DataFrame transformation
    result_df = args[0]
    assert sorted(result_df.columns) == sorted(['id', 'name', 'country', 'brewery_type', 'timestamp_ingestion'])
    assert result_df.count() == 2

def test_empty_data_handling(spark_session, mocker):
    """Test with empty input DataFrame"""
    mock_init_spark = mocker.patch(
        'src.utils.init_spark', 
        return_value=spark_session
    )
    mock_write_delta = mocker.patch("src.elt_utils.write.write_delta_partitioned")

    # Empty test data
    test_df = spark_session.createDataFrame([], "data: string, timestamp_ingestion: timestamp")

    # Mock Spark read
    mocker.patch(
        'pyspark.sql.SparkSession.read',
        return_value=MagicMock(load=MagicMock(return_value=test_df))
    )
    mocker.patch.object(
        spark_session.read.option("inferSchema", "true"),
        'load',
        return_value=test_df
    )

    # Call the function
    normalize_and_partition_breweries()

    # Verify empty DataFrame was processed
    args, _ = mock_write_delta.call_args
    assert args[0].count() == 0

def test_malformed_json_handling(spark_session, mocker, caplog):
    """Test handling of malformed JSON data"""
    mock_init_spark = mocker.patch(
        'src.utils.init_spark', 
        return_value=spark_session
    )
    mock_write_delta = mocker.patch("src.elt_utils.write.write_delta_partitioned")

    # Test data with malformed JSON
    test_data = [
        {"data": '{"id": "1", "name": "Good Brew"}', "timestamp_ingestion": "2023-01-01T00:00:00"},
        {"data": 'NOT VALID JSON', "timestamp_ingestion": "2023-01-01T00:00:00"}
    ]
    test_df = spark_session.createDataFrame(test_data)
    
    # Mock Spark read
    mocker.patch(
        'pyspark.sql.SparkSession.read',
        return_value=MagicMock(load=MagicMock(return_value=test_df))
    )
    mocker.patch.object(
        spark_session.read.option("inferSchema", "true"),
        'load',
        return_value=test_df
    )
    
    # Call the function
    normalize_and_partition_breweries()
    
    # Verify one record was processed and one failed
    args, _ = mock_write_delta.call_args
    assert args[0].count() == 1  # Only the good record
    
    # Check for error logs
    assert "Error parsing JSON" in caplog.text

def test_schema_validation(spark_session, mocker):
    """Test that the schema is properly applied"""
    mock_init_spark = mocker.patch(
        'src.utils.init_spark', 
        return_value=spark_session
    )
    mock_write_delta = mocker.patch("src.elt_utils.write.write_delta_partitioned")
    
    # Test data with extra field not in schema
    test_data = [
        {"data": '{"id": "1", "name": "Brew1", "country": "US", "extra_field": "value"}', 
        "timestamp_ingestion": "2023-01-01T00:00:00"}
    ]
    test_df = spark_session.createDataFrame(test_data)
    
    # Mock Spark read
    mocker.patch(
        'pyspark.sql.SparkSession.read',
        return_value=MagicMock(load=MagicMock(return_value=test_df))
    )
    mocker.patch.object(
        spark_session.read.option("inferSchema", "true"),
        'load',
        return_value=test_df
    )
    
    # Call the function
    normalize_and_partition_breweries()
    
    # Verify schema was enforced (extra field dropped)
    args, _ = mock_write_delta.call_args
    assert "extra_field" not in args[0].columns
    assert "id" in args[0].columns

def test_partitioning_logic(spark_session, mocker):
    """Test that partitioning column exists in final DataFrame"""
    mock_init_spark = mocker.patch(
        'src.utils.init_spark', 
        return_value=spark_session
    )
    mock_write_delta = mocker.patch("src.elt_utils.write.write_delta_partitioned")
    
    # Test data with country field
    test_data = [
        {"data": '{"id": "1", "name": "Brew1", "country": "US"}', "timestamp_ingestion": "2023-01-01T00:00:00"}
    ]
    test_df = spark_session.createDataFrame(test_data)
    
    # Mock Spark read
    mock_read = mocker.MagicMock()
    mock_read.option.return_value = mock_read
    mock_read.load.return_value = test_df

    mocker.patch.object(
        type(spark_session), "read",
        new_callable=PropertyMock,
        return_value=mock_read
    )

    # Call the function
    normalize_and_partition_breweries()
    assert mock_write_delta.called, "write_delta_partitioned was not called"
    # Verify partitioning column exists
    args, kwargs = mock_write_delta.call_args
    assert kwargs['partition_column'] == 'country'
    assert 'country' in args[0].columns
    
