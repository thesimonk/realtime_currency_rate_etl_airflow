from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import psycopg2

def fetch_and_store_currency():
    url = "https://api.exchangerate.host/latest?base=USD"
    response = requests.get(url)
    data = response.json()

    base = data["base"]
    date = data["date"]
    rates = data["rates"]

    df = pd.DataFrame(rates.items(), columns=["currency", "rate"])
    df["base"] = base
    df["date"] = date

    conn = psycopg2.connect(
        host="localhost",
        dbname="currency_db",
        user="airflow",
        password="airflow"
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS exchange_rates (
            base TEXT,
            currency TEXT,
            rate FLOAT,
            date DATE
        )
    """)

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO exchange_rates (base, currency, rate, date)
            VALUES (%s, %s, %s, %s)
        """, (row["base"], row["currency"], row["rate"], row["date"]))

    conn.commit()
    cur.close()
    conn.close()

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="currency_etl",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
) as dag:
    task = PythonOperator(
        task_id="fetch_and_store_currency",
        python_callable=fetch_and_store_currency
    )

