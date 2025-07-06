import sys
import os
print("sys.path:", sys.path)
sys.path.insert(0, '/app')

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from process_data import request_and_save_breweries, normalize_and_partition_breweries


default_args = {
    'owner': 'kerli.schroeder',
    'start_date': datetime(2025, 7, 3),
    
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}


with DAG(
    dag_id='etl_breweries_dag',
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
) as dag:

    ingest_task = PythonOperator(
        task_id='request_and_save_breweries',
        python_callable=request_and_save_breweries
    )

    spark_etl_task = PythonOperator(
        task_id='normalize_and_partition_breweries',
        python_callable=normalize_and_partition_breweries
    )

    ingest_task >> spark_etl_task 