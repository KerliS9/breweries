import pytest
from pyspark.sql import SparkSession
from unittest.mock import MagicMock, PropertyMock
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from src.process_data import normalize_and_partition_breweries
#from src.elt_utils.schemas import breweries_schema


@pytest.fixture
def spark_session():
    """Fixture to create a SparkSession for testing"""
    spark = (
        SparkSession.builder
        .master("local[1]")
        .appName("pytest-pyspark")
        .config(
            "spark.jars",
            "/opt/spark/jars/delta-core_2.12-2.4.0.jar,/opt/spark/jars/delta-storage-2.4.0.jar"
        )
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )
    yield spark
    spark.stop()


def test_normalize_and_partition_breweries(spark_session, mocker):
    """Test the complete normalization and partitioning workflow"""
    mock_init_spark = mocker.patch(
        'src.process_data.init_spark', 
        return_value=spark_session
    )
    mock_write_delta = mocker.patch("src.process_data.write_delta_partitioned")

    test_data = [
        {"data": '{"id": "5128df48-79fc-4f0f-8b52-d06be54d0cec", "name": "(405) Brewing Co","brewery_type": "micro", "address_1": "1716 Topeka St", "address_2": null, "address_3": null, "city": "Norman", "state_province": "Oklahoma", "postal_code": "73069-8224", "country": "United States", "longitude": -97.46818222, "latitude": 35.25738891, "phone": "4058160490", "website_url": "http://www.405brewing.com", "state": "Oklahoma", "street": "1716 Topeka St"}',  "timestamp_ingestion": "2023-01-01T00:00:00"},
        {"data": '{ "id": "9c5a66c8-cc13-416f-a5d9-0a769c87d318", "name": "(512) Brewing Co", "brewery_type": "micro", "address_1": "407 Radam Ln Ste F200", "address_2": null, "address_3": null, "city": "Austin", "state_province": "Texas", "postal_code": "78745-1197", "country": "United States", "longitude": null, "latitude": null, "phone": "5129211545", "website_url": "http://www.512brewing.com", "state": "Texas", "street": "407 Radam Ln Ste F200"}', "timestamp_ingestion": "2023-01-01T00:00:00"}
    ]
    test_df = spark_session.createDataFrame(test_data)

    mock_read = mocker.MagicMock()
    mock_read.option.return_value = mock_read
    mock_read.load.return_value = test_df

    mocker.patch.object(
        type(spark_session), "read",
        new_callable=PropertyMock,
        return_value=mock_read
    )

    normalize_and_partition_breweries()

    mock_init_spark.assert_called_once()

    args, kwargs = mock_write_delta.call_args

    assert kwargs['output_path'] == '/warehouse/silver/silver_list_breweries'
    assert kwargs['partition_column'] == 'country'

    result_df = kwargs['df']

    assert sorted(result_df.columns) == sorted(['address_1', 'address_2', 'address_3', 'brewery_type', 'city', 'country', 'id', 'name', 'phone', 'postal_code', 'state', 'state_province', 'street', 'timestamp_ingestion', 'website_url'])
    assert result_df.count() == 2


def test_empty_data_handling(spark_session, mocker):
    """Test with empty input DataFrame"""
    mock_init_spark = mocker.patch(
        'src.process_data.init_spark', 
        return_value=spark_session
    )
    mock_write_delta = mocker.patch("src.process_data.write_delta_partitioned")

    test_df = spark_session.createDataFrame([], "data: string, timestamp_ingestion: timestamp")

    mock_read = mocker.MagicMock()
    mock_read.option.return_value = mock_read
    mock_read.load.return_value = test_df

    mocker.patch.object(
        type(spark_session), "read",
        new_callable=PropertyMock,
        return_value=mock_read
    )

    normalize_and_partition_breweries()

    args, kwargs = mock_write_delta.call_args

    assert kwargs['df'].count() == 0


def test_malformed_json_handling(spark_session, mocker, caplog):
    """Test handling of malformed JSON data"""
    mock_init_spark = mocker.patch(
        'src.process_data.init_spark', 
        return_value=spark_session
    )
    mock_write_delta = mocker.patch("src.process_data.write_delta_partitioned")

    test_data = [
        {"data": '{"id": "1", "name": "Good Brew"}', "timestamp_ingestion": "2023-01-01T00:00:00"},
        {"data": 'NOT VALID JSON', "timestamp_ingestion": "2023-01-01T00:00:00"}
    ]
    test_df = spark_session.createDataFrame(test_data)

    mock_read = mocker.MagicMock()
    mock_read.option.return_value = mock_read
    mock_read.load.return_value = test_df

    mocker.patch.object(
        type(spark_session), "read",
        new_callable=PropertyMock,
        return_value=mock_read
    )

    normalize_and_partition_breweries()

    args, kwargs = mock_write_delta.call_args
    print('test args', args)
    print('test kwargs', kwargs)
    print('test kwargs', kwargs['df'].count())
    print(caplog.text)
    assert kwargs['df'].count() == 1

    assert "Error parsing JSON" in caplog.text


def test_schema_validation(spark_session, mocker):
    """Test that the schema is properly applied"""
    mock_init_spark = mocker.patch(
        'src.process_data.init_spark', 
        return_value=spark_session
    )
    mock_write_delta = mocker.patch("src.process_data.write_delta_partitioned")

    test_data = [
        {"data": '{"id": "1", "name": "Brew1", "country": "US", "extra_field": "value"}', 
        "timestamp_ingestion": "2023-01-01T00:00:00"}
    ]
    test_df = spark_session.createDataFrame(test_data)

    mock_read = mocker.MagicMock()
    mock_read.option.return_value = mock_read
    mock_read.load.return_value = test_df

    mocker.patch.object(
        type(spark_session), "read",
        new_callable=PropertyMock,
        return_value=mock_read
    )

    normalize_and_partition_breweries()

    args, kwargs = mock_write_delta.call_args

    assert "data" not in kwargs['df'].columns
    assert "id" in kwargs['df'].columns


def test_partitioning_logic(spark_session, mocker):
    """Test that partitioning column exists in final DataFrame"""
    mock_init_spark = mocker.patch(
        'src.process_data.init_spark', 
        return_value=spark_session
    )
    mock_write_delta = mocker.patch("src.process_data.write_delta_partitioned")

    test_data = [
        {"data": '{"id": "1", "name": "Brew1", "country": "US"}', "timestamp_ingestion": "2023-01-01T00:00:00"}
    ]
    test_df = spark_session.createDataFrame(test_data)

    mock_read = mocker.MagicMock()
    mock_read.option.return_value = mock_read
    mock_read.load.return_value = test_df

    mocker.patch.object(
        type(spark_session), "read",
        new_callable=PropertyMock,
        return_value=mock_read
    )

    normalize_and_partition_breweries()

    args, kwargs = mock_write_delta.call_args

    assert kwargs['partition_column'] == 'country'
