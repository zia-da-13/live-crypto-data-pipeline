# Live Crypto Data Pipeline

A live cryptocurrency data engineering and analytics project that extracts market data from the CoinGecko API, transforms it with Python, stores historical snapshots in PostgreSQL and CSV, and visualizes the results through an interactive Streamlit and Plotly dashboard.

## Project Architecture

```text
CoinGecko API
      |
      v
Python Extraction
      |
      v
Data Transformation
      |
      v
+-------------------+
|                   |
v                   v
CSV              PostgreSQL
                     |
                     v
                 SQL Views
                     |
                     v
                 Streamlit
                     |
                     v
                  Plotly
                     |
                     v
          Interactive Dashboard
```

## Technologies

- Python
- PostgreSQL
- Pandas
- Requests
- Psycopg
- Streamlit
- Plotly
- CoinGecko API
- Git and GitHub
- VS Code

## Cryptocurrencies

The pipeline currently collects market data for:

- Bitcoin (BTC)
- Ethereum (ETH)
- Solana (SOL)

The cryptocurrency list can be changed in:

```text
src/config.py
```

## Data Pipeline

The project follows an ETL workflow.

### Extract

`crypto_api.py` retrieves cryptocurrency market information from the CoinGecko API.

### Transform

`transform.py` selects and cleans the fields required by the project.

### Load

`save_data.py` stores the transformed data in:

- PostgreSQL
- CSV

The pipeline collects historical snapshots at a configurable interval.

## Data Collected

The pipeline stores:

- Cryptocurrency ID
- Symbol
- Name
- Current price
- Market capitalization
- Trading volume
- 24-hour high
- 24-hour low
- 24-hour price change percentage
- API last-updated timestamp
- Pipeline collection timestamp

## Duplicate Protection

Duplicate market snapshots are prevented using:

```text
coin_id + last_updated
```

PostgreSQL uses a unique constraint/index together with:

```sql
ON CONFLICT (coin_id, last_updated)
DO NOTHING
```

The CSV storage layer also removes duplicate snapshots.

## PostgreSQL

The main table is:

```text
crypto_market_data
```

The project also contains analytical views:

```text
latest_crypto_prices
crypto_price_summary
```

Database initialization is available in:

```text
sql/init_database.sql
```

Analytical SQL queries are available in:

```text
sql/analytics.sql
```

## Dashboard

The Streamlit dashboard provides:

- Current cryptocurrency prices
- 24-hour price changes
- Market capitalization
- Trading volume
- BTC vs ETH vs SOL relative performance
- Historical price trends
- Percentage returns
- High and low price analysis
- Market-cap trends
- Volume trends
- Cryptocurrency correlation analysis
- Time-range filtering
- Individual cryptocurrency analysis
- Historical database records
- Pipeline status
- Manual and automatic dashboard refresh

## Project Structure

```text
live_crypto_project/
|
|-- data/
|   `-- crypto_market_data.csv
|
|-- logs/
|   `-- crypto_pipeline.log
|
|-- sql/
|   |-- analytics.sql
|   `-- init_database.sql
|
|-- src/
|   |-- app.py
|   |-- config.py
|   |-- crypto_api.py
|   |-- database_service.py
|   |-- logger_config.py
|   |-- main.py
|   |-- save_data.py
|   `-- transform.py
|
|-- .env
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/zia-da-13/live-crypto-data-pipeline.git
```

Enter the project:

```bash
cd live-crypto-data-pipeline
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root.

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=crypto_db
DB_USER=postgres
DB_PASSWORD=your_database_password
```

Do not commit `.env` to GitHub.

## Initialize PostgreSQL

Create the PostgreSQL database:

```sql
CREATE DATABASE crypto_db;
```

Then execute:

```text
sql/init_database.sql
```

For example, from `psql`:

```sql
\i 'C:/path/to/live-crypto-data-pipeline/sql/init_database.sql'
```

## Run One Pipeline Collection

From the project root:

```bash
python src/crypto_api.py
```

## Run the Live Data Collector

```bash
python src/main.py
```

The default collection interval is configured in:

```text
src/config.py
```

## Run the Dashboard

Open another terminal, activate the virtual environment, and run:

```bash
streamlit run src/app.py
```

Streamlit will provide a local dashboard address, typically:

```text
http://localhost:8501
```

## Running the Complete Project

Use two terminals.

### Terminal 1

```bash
python src/main.py
```

This continuously collects cryptocurrency data.

### Terminal 2

```bash
streamlit run src/app.py
```

This runs the analytics dashboard.

## Logging

Pipeline activity is written to:

```text
logs/crypto_pipeline.log
```

Logs include successful pipeline runs, failures, and shutdown events.

## Configuration

Project settings are centralized in:

```text
src/config.py
```

This includes:

- CoinGecko API URL
- Cryptocurrency list
- Currency
- Collection interval
- CSV file location

## Future Improvements

Potential future enhancements include:

- Docker containerization
- Cloud PostgreSQL
- Streamlit deployment
- Automated testing
- Additional cryptocurrencies
- Data quality validation
- Scheduled orchestration
- Cloud deployment
- Cryptocurrency alerts
- Technical indicators
- Longer-term historical analysis

## Purpose

This project demonstrates an end-to-end data engineering workflow combining API extraction, Python transformation, persistent database storage, SQL analytics, automated data collection, and interactive business intelligence visualization.