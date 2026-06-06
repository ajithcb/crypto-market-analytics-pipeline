import sqlite3
import os

DB_NAME = "crypto_analytics.db"

def initialize_database():
    """Creates a local SQLite database file and defines the schema table."""
    print("🗄️ Initializing SQLite database storage...")
    
   
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
   
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coin_id TEXT NOT NULL,
            symbol TEXT NOT NULL,
            name TEXT NOT NULL,
            current_price REAL NOT NULL,
            market_cap REAL,
            total_volume REAL,
            price_change_24h REAL,
            captured_at TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"✅ Database connection active. File created: '{DB_NAME}'")

def save_dataframe_to_sql(df):
    """Appends data rows directly from a Pandas DataFrame into the SQL table."""
    if df is None or df.empty:
        print("⚠️ No data available to save to the database.")
        return
        
    conn = sqlite3.connect(DB_NAME)
    
   
    df_to_insert = df.rename(columns={
        "price_change_percentage_24h": "price_change_24h"
    })
    
    
    df_to_insert.to_sql("market_history", conn, if_exists="append", index=False)
    
    conn.close()
    print(f"💾 SUCCESS: Appended {len(df)} rows into 'market_history' SQL table.")

if __name__ == "__main__":
   
    initialize_database()
