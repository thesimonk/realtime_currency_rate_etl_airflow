import requests
import psycopg2
from datetime import datetime

def fetch_and_store_currency():
    url = "https://api.exchangerate.host/latest?base=USD&symbols=EUR,GBP,NGN"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        timestamp = datetime.utcnow()
        rates = data['rates']

        conn = psycopg2.connect(
            host="localhost",
            dbname="currency_db",
            user="airflow",
            password="airflow",
            port=5432
        )
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS currency_rates (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP,
                base VARCHAR(10),
                symbol VARCHAR(10),
                rate FLOAT
            )
        """)

        for symbol, rate in rates.items():
            cursor.execute("""
                INSERT INTO currency_rates (timestamp, base, symbol, rate)
                VALUES (%s, %s, %s, %s)
            """, (timestamp, data['base'], symbol, rate))

        conn.commit()
        cursor.close()
        conn.close()
        print("Currency rates saved successfully!")

    except Exception as e:
        print(f"Error: {e}")
