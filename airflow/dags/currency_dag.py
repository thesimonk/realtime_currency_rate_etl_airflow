from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from fetch_currency_data import fetch_and_store_currency

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='currency_etl_dag',
    default_args=default_args,
    description='A DAG to fetch and store currency data',
    schedule_interval='@hourly',
    start_date=datetime(2025, 5, 25),
    catchup=False,
    tags=['currency', 'etl'],
) as dag:

    fetch_task = PythonOperator(
        task_id='fetch_and_store_currency',
        python_callable=fetch_and_store_currency,
    )

    fetch_task
