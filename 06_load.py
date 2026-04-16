import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# 1. Load Configuration
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "immovision_db")

INPUT_FILE = "data/processed/transformed_elysee.csv"
TABLE_NAME = "elysee_listings_silver"

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run transformation script first.")
        return

    # 2. Load Data
    print(f"Reading {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)

    # 3. Create Connection
    # Connection string format: postgresql://user:password@host:port/dbname
    connection_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_url)

    # 4. Load into PostgreSQL
    print(f"Loading {len(df)} rows into table '{TABLE_NAME}'...")
    try:
        df.to_sql(
            TABLE_NAME,
            engine,
            if_exists="replace",
            index=False,
            method="multi", # Optimization for faster loading
            chunksize=1000
        )
        print("Data loaded successfully.")

        # 5. Validation Query
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {TABLE_NAME}"))
            count = result.scalar()
            print(f"Validation: Table '{TABLE_NAME}' now contains {count} rows.")

    except Exception as e:
        print(f"Failed to load data into PostgreSQL: {e}")
        print("\nTIP: Make sure your PostgreSQL server is running and the database exists.")

if __name__ == "__main__":
    main()
