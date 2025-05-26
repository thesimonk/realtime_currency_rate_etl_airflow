import os
import requests
import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def fetch_and_store_currency():
    access_key = Variable.get("CURRENCY_API_KEY")
    url = f"http://api.currencylayer.com/live?access_key={access_key}&currencies=USD,AUD,CAD,PLN,MXN&format=1"

    response = requests.get(url)
    data = response.json()

    if not data.get("success"):
        raise Exception(f"API Error: {data.get('error')}")

    quotes = data["quotes"]
    timestamp = data["timestamp"]

    conn = psycopg2.connect(
        host="localhost",
        dbname="currency_db",
        user="airflow",
        password="airflow",
        port=5432
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS currency_rates (
            id SERIAL PRIMARY KEY,
            currency VARCHAR(10),
            rate FLOAT,
            timestamp TIMESTAMP
        )
    """)
    for currency_pair, rate in quotes.items():
        currency = currency_pair[3:]  # Strip 'USD' prefix
        cur.execute("""
            INSERT INTO currency_rates (currency, rate, timestamp)
            VALUES (%s, %s, to_timestamp(%s))
        """, (currency, rate, timestamp))
    conn.commit()
    cur.close()
    conn.close()

with DAG(
    dag_id="currency_etl_dag",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@hourly",
    catchup=False
) as dag:
    fetch_task = PythonOperator(
        task_id="fetch_and_store_currency",
        python_callable=fetch_and_store_currency
    )
