from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os
from src.process_data import request_and_save, normalize_and_partition_data


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))


default_args = {
    'owner': 'kerli.schroeder'
    'start_date': datetime(2025, 7, 3),
}


with DAG(
    'etl_breweries_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    ingest_task = PythonOperator(
        task_id='request_and_save',
        python_callable=request_and_save
    )

    spark_etl_task = PythonOperator(
        task_id='normalize_and_partition_data',
        python_callable=normalize_and_partition_data
    )

    ingest_task >> spark_etl_task 