import os
import psycopg2
import pandas as pd

# Render injects this environment variable automatically when linked
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    """Establishes an active connection to the cloud PostgreSQL database."""
    if not DATABASE_URL:
        raise ValueError("❌ DATABASE_URL environment variable is missing on Render configuration settings!")
    return psycopg2.connect(DATABASE_URL)

def initialize_database():
    """Creates the PostgreSQL market history table structure if it does not exist."""
    print("🗄️ Checking Cloud PostgreSQL infrastructure...")
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_history (
            id SERIAL PRIMARY KEY,
            coin_id VARCHAR(50) NOT NULL,
            symbol VARCHAR(20) NOT NULL,
            name VARCHAR(50) NOT NULL,
            current_price NUMERIC NOT NULL,
            market_cap NUMERIC,
            total_volume NUMERIC,
            price_change_24h NUMERIC,
            captured_at TIMESTAMP NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ PostgreSQL Table schema verified successfully.")

def save_dataframe_to_sql(df):
    """Appends cleansed Pandas DataFrame records straight into the cloud table rows."""
    if df is None or df.empty:
        print("⚠️ DataFrame is empty. Ingestion upload process skipped.")
        return
        
    conn = get_connection()
    cursor = conn.cursor()
    
    # Bulk SQL stream engine integration
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO market_history (coin_id, symbol, name, current_price, market_cap, total_volume, price_change_24h, captured_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['coin_id'], row['symbol'], row['name'], 
            row['current_price'], row['market_cap'], row['total_volume'],
            row['price_change_percentage_24h'], row['captured_at']
        ))
        
    conn.commit()
    cursor.close()
    conn.close()
    print(f"💾 SUCCESS: Appended {len(df)} records into PostgreSQL cloud server storage.")

if __name__ == "__main__":
    initialize_database()

