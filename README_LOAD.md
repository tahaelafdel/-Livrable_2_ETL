# README_LOAD.md - Data Warehouse Integration

This document outlines the final stage of the ETL pipeline: loading the enriched Silver Zone data into a relational PostgreSQL database.

## 1. Destination Overview
- **Database Engine:** PostgreSQL
- **Database Name:** `immovision_db`
- **Table Name:** `elysee_listings_silver`
- **Rows Loaded:** 2,625

## 2. Technical Stack & Security
- **Loader:** Python with `SQLAlchemy` and `psycopg2`.
- **Method:** `to_sql` with `if_exists="replace"` for idempotence.
- **Secrets Management:** Database credentials (user, password, host, port) are stored in a `.env` file and loaded via `python-dotenv`. **The .env file is excluded from version control for security.**

## 3. SQL Schema Highlights
The table is automatically generated from the Pandas DataFrame, ensuring strict typing for key features:
- `id`: BigInt (Primary Identifier)
- `price`: Double Precision (Float)
- `host_response_rate`: Double Precision
- `host_is_superhost`: Integer (Binary)
- `standardization_score`: Integer (-1, 0, 1)
- `neighborhood_impact`: Integer (-1, 0, 1)

## 4. How to Run
1. Ensure PostgreSQL is running.
2. Create the database `immovision_db`.
3. Configure your `.env` file with correct credentials.
4. Execute `python scripts/06_load.py`.
