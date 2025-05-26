# Real-Time Currency Rate ETL Pipeline (Airflow)

This is an end-to-end data engineering pipeline built using **Apache Airflow** that ingests real-time currency exchange rates from the [ExchangeRate.host API](https://exchangerate.host), processes the data, and stores it in a **PostgreSQL database**.

## Data Source

- **API Endpoint**: `https://api.exchangerate.host/live`
- **Currencies**: USD, AUD, CAD, PLN, MXN

## Tech Stack

- [Python 3.12](https://www.python.org/)
- [Apache Airflow](https://airflow.apache.org/)
- [PostgreSQL](https://www.postgresql.org/)
- `.env` file for secrets

## Project Structure

```

currency\_pipeline/
├── airflow/
│   └── dags/
│       └── currency\_dag.py         # Main Airflow DAG
│       └── fetch\_currency\_data.py  # Core ETL logic
├── .env                            # Stores API key and DB URL
└── README.md

````

## How to Run

1. Clone this repo:
   ```bash
   git clone https://github.com/thesimonk/realtime_currency_rate_etl_airflow.git
````

2. Set up your `.env` file:

   ```dotenv
   API_KEY=your_api_key_here
   DATABASE_URL=postgresql://user:password@localhost:5432/your_db
   ```

3. Start Airflow:

   ```bash
   airflow standalone
   ```

4. Trigger the DAG:

   * Visit `http://localhost:8080`
   * Enable and trigger `currency_etl_dag`

## Testing

Check the Airflow logs for the `fetch_and_store_currency` task to confirm successful data ingestion.

## Future Enhancements

* Add data validation with `Great Expectations`
* Schedule periodic refreshes
* Add historical data support
