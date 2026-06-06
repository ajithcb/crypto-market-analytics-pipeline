import sqlite3
import pandas as pd

DB_NAME = "crypto_analytics.db"

def run_analytical_queries():
    """Connects to the database and runs analytical business reports."""
    conn = sqlite3.connect(DB_NAME)
    
    print("\n==================================================")
    print("📈 REPORT 1: Tracked Assets & Total Database Records")
    print("==================================================")
    
    query1 = """
        SELECT coin_id, COUNT(*) as total_records, AVG(current_price) as average_tracked_price
        FROM market_history
        GROUP BY coin_id;
    """
    df1 = pd.read_sql_query(query1, conn)
    print(df1.to_string(index=False))

    print("\n==================================================")
    print("⚠️ REPORT 2: High Volatility Alert (> 2% Asset Shifts)")
    print("==================================================")
    
    query2 = """
        SELECT coin_id, current_price, price_change_24h, captured_at
        FROM market_history
        WHERE ABS(price_change_24h) > 2.0
        ORDER BY captured_at DESC;
    """
    df2 = pd.read_sql_query(query2, conn)
    
    if df2.empty:
        print("No extreme volatility events found in current history logs.")
    else:
        print(df2.to_string(index=False))

    conn.close()

if __name__ == "__main__":
    print("📊 Executing SQL Data Analysis Suite...")
    run_analytical_queries()
