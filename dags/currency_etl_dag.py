from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.join(os.environ["AIRFLOW_HOME"], "..", "scripts"))
from fetch_currency import fetch_and_store_currency

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 26),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'currency_etl_dag',
    default_args=default_args,
    description='Fetches currency rates and stores in PostgreSQL',
    schedule_interval='@hourly',
    catchup=False,
) as dag:

    run_etl = PythonOperator(
        task_id='fetch_currency_data',
        python_callable=fetch_and_store_currency,
    )

    run_etl
